import warnings
from debyetools.tpropsgui.atomtools import atomic_mass
from debyetools.aux_functions import load_doscar, _read_poscar
from debyetools.get_elastic import get_EM


class Vdata:
    def __init__(self):
        pass


def parse_contcar(file_path):
    """
    Element symbol of every atom in a VASP 5 POSCAR/CONTCAR (e.g. ['Nb', 'Nb']).

    :param str file_path: path of the POSCAR/CONTCAR.
    :return: list of symbols, one per atom.
    :rtype: list
    """
    pos = _read_poscar(file_path)
    if pos['species'] is None:
        raise ValueError("parse_contcar: element symbols not provided in '%s' (VASP 4 format)." % file_path)
    formula = []
    for elem, count in zip(pos['species'], pos['counts']):
        formula.extend([elem] * count)
    return formula


def average_mass(elements):
    """Mean atomic mass (g/mol) of a list of element symbols; 'VA' (vacancy) counts as 0."""
    masses = dict(atomic_mass, VA=0)
    return sum(masses[element] for element in elements) / len(elements)


_ENERGY_COLUMNS = ["Element", "Structure", "Total-energy", "Mag", "A-conv", "Vol-conv", "Vol-at", "R-at", "B/A", "C/A"]


def load_energies(file_path):
    """
    Read an elements_energies.out table (one header line, whitespace-separated columns).

    :param str file_path: path of the file.
    :return: dict column name -> list of values (strings for Element/Structure, floats otherwise).
    :rtype: dict
    """
    table = {c: [] for c in _ENERGY_COLUMNS}
    with open(file_path) as f:
        lines = f.readlines()[1:]
    for line in lines:
        tok = line.split()
        if len(tok) < len(_ENERGY_COLUMNS):
            continue
        for k, c in enumerate(_ENERGY_COLUMNS):
            table[c].append(tok[k] if k < 2 else float(tok[k]))
    return table


def get_energy(potential, current_path, energies_file=None):
    """Total energy per atom (eV) of the element/potential `potential` from current_path/elements_energies.out."""
    fname = energies_file if energies_file is not None else f'{current_path}/elements_energies.out'
    table = load_energies(fname)
    if potential not in table['Element']:
        raise KeyError(f"get_energy: '{potential}' not found in {fname}")
    return table['Total-energy'][table['Element'].index(potential)]


def extract_from_DFT(file_path, vi=70, vf=130, step=3, ref=100, energies_file=None):
    """
    Collect the DFT data of one compound from the folder layout
    path/EvV/<i>/OUTCAR and DOSCAR (i = vi, vi+step, ..., vf; i = ref is the reference volume),
    path/relaxation/CONTCAR, path/elastic/eps1..eps9 and path/elements_energies.out (or energies_file).

    Volumes whose OUTCAR is missing or unreadable are skipped with a UserWarning (the DOSCAR list
    follows the same volumes); a missing reference volume raises an error.

    :param str file_path: compound folder.
    :param int vi: first volume folder name.
    :param int vf: last volume folder name.
    :param int step: step between volume folder names.
    :param int ref: reference (equilibrium) volume folder name, used for E0 and the formation energy.
    :param str energies_file: elements_energies.out to use for the formation energy (default: in file_path).
    :return: Vdata with V (A^3/atom), E (eV/atom), E0, Ef (eV/atom), formula, nats, mass (kg/mol),
             potentials, electric (load_doscar output), EM (6x6, kBar), path.
    :rtype: Vdata
    """
    vdata = Vdata()

    path = file_path
    E = []
    V = []
    loaded = []
    skipped = []
    nats = 0
    E0 = None
    potentials_set = []
    for i in range(vi, vf + step, step):
        try:
            with open(f'{path}/EvV/{i}/OUTCAR') as f:
                lines = f.readlines()
            Ei = Vi = natsi = None
            for line in lines:
                if 'volume of cell' in line:
                    Vi = float(line.split()[-1])
                if 'TOTEN' in line:
                    Ei = float(line.split()[4])
                if 'NIONS' in line:
                    natsi = int(line.split()[-1])
                if 'POTCAR:' in line:
                    potentials_set.append(line.split()[2])
            if Ei is None or Vi is None or not natsi:
                raise ValueError('energy, volume or NIONS not found')
        except Exception as e:
            skipped.append((i, str(e)))
            continue
        E.append(Ei / natsi)
        V.append(Vi / natsi)
        loaded.append(i)
        nats = natsi
        if i == ref:
            E0 = Ei / natsi
    if skipped:
        warnings.warn('extract_from_DFT: %d volume(s) skipped in %s/EvV: %s'
                      % (len(skipped), path, '; '.join('%s (%s)' % s for s in skipped)), UserWarning, stacklevel=2)
    if E0 is None:
        raise ValueError(f'extract_from_DFT: reference volume {path}/EvV/{ref}/OUTCAR not loaded.')
    vdata.V = V
    vdata.E = E
    potentials_set = set(potentials_set)
    vdata.potentials = {p.split('_')[0]: p for p in potentials_set}
    vdata.potentials['VA'] = 'VA'

    vdata.formula = parse_contcar(f'{path}/relaxation/CONTCAR')
    vdata.nats = nats
    vdata.mass = average_mass(vdata.formula) / 1000
    current_folder = f'{path}'
    vdata.Ef = E0 - sum([get_energy(vdata.potentials[fi], current_folder, energies_file) for fi in vdata.formula]) / nats
    vdata.E0 = E0
    vdata.path = path

    list_filetags = [f'/EvV/{i}/DOSCAR' for i in loaded]
    vdata.electric = load_doscar(path, list_filetags=list_filetags)

    vdata.EM = get_EM(f'{path}/elastic')   # kBar (since B8b)

    return vdata
