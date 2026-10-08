import itertools as it
import re
import numpy as np
import warnings
from debyetools.constants import A3_ATOM_TO_M3_MOL, EV_ATOM_TO_J_MOL
from typing import Tuple


class logging(object):
    def __init__(self, *files: ...) -> None:
        self.files = files

    def write(self, obj: str) -> None:
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self) -> None:
        for f in self.files:
            f.flush()


def c_types(atom_types: str) -> Tuple[list, list]:
    """
    returns all the pair types combinations.

    :param str atom_types: the types of each atom in the primitive cell in the same order as the basis vectors.
    :return: pair types and list wuth individual types.
    :rtype: Tuple[list, list]
    """
    types_all = re.findall('[A-Z][^A-Z]*', atom_types)
    ptypes = list(set([s for s in types_all]))
    ptypes.sort()
    combs_types = list(it.combinations_with_replacement(ptypes, r=2))
    combs_types = [A[0] + '-' + A[1] for A in combs_types]
    return combs_types, types_all


def generate_cells_coordinates(size: np.ndarray, primitive_cell: np.ndarray, center: np.ndarray) -> np.ndarray:
    """ generate the cell coordinates for which we are going
    to calculate the neighbor list.

    :param np.ndarray size: Number of times we are replicating the primitive cell
    :param np.ndarray primitive_cell: The primitive cell
    :param np.ndarray center: The position in space where the system of reference is
    :return: cell coordinates.
    :rtype: np.ndarray

    """

    cell_coords = np.array(list((it.product(np.arange(size[0]),
                                            np.arange(size[1]),
                                            np.arange(size[2])))))

    cell_coords_centered = cell_coords + center
    cell_coords_centered = np.dot(cell_coords_centered, primitive_cell)

    return cell_coords_centered


def gen_Ts(Ti: float, Tf: float, nTs: int) -> np.ndarray:
    """
    Function to generate a range of temperatures.

    :param float Ti: Initial temperature. (Try not to use the value 0. Use 0.1 instead.)
    :param float Tf: Final temperature.
    :param int nTs: Number of values between Ti and Tf, both included. Room temperature (298.15 K) is
                    added if it is not already one of them, so the result has nTs or nTs + 1 values.
    :return: Sorted temperatures.
    :rtype: np.ndarray
    """
    Ts = np.linspace(Ti, Tf, int(nTs))
    if not np.any(np.isclose(Ts, 298.15, rtol=0, atol=1e-9)):
        Ts = np.r_[Ts, [298.15]]
    Ts.sort()
    return Ts


def gen_Ps(Pi, Pf, nPs):
    """
    Function to generate a range of pressures.

    :param float Pi: Initial pressure.
    :param float Pf: Final pressure.
    :param int nPs: Number of values between Pi and Pf, both included.

    :return: Values of pressures from Pi to Pf.
    :rtype: np.ndarray
    """
    if nPs <= 1: return np.array([Pi])
    return np.linspace(Pi, Pf, int(nPs))


def load_doscar(filename_sufix: str, list_filetags: list = None) -> tuple[list, list, list]:
    """
    Read the total electronic DOS of a series of VASP DOSCAR files (one per volume).

    Only the total-DOS block (NEDOS lines after the 6-line header) is read; projected
    blocks are ignored. For spin-polarised files (ISPIN = 2, 5 columns) the two spin
    channels are summed; for ISPIN = 1 (3 columns) the DOS column is used. The DOS is
    divided by the number of atoms.

    :param filename_sufix: common part of the file names (path + prefix).
    :type filename_sufix: str
    :param list_filetags: filename tags appended to filename_sufix (default
        '-0.10' ... '0.10'), in the same order as the volumes.
    :type list_filetags: list
    :return: E (energy grids, eV), N (total DOS, states/eV/atom), Ef (Fermi levels, eV),
        one entry per file.
    :rtype: tuple[list,list,list]
    """
    if list_filetags is None:
        list_filetags = ['-0.10', '-0.09', '-0.08', '-0.07', '-0.06', '-0.05', '-0.04', '-0.03',
                         '-0.02', '-0.01', '-0.00', '0.01', '0.02', '0.03', '0.04', '0.05', '0.06',
                         '0.07', '0.08', '0.09', '0.10']

    E = []
    N = []
    Ef = []
    for tag in list_filetags:
        filename = filename_sufix + str(tag)
        with open(filename) as infile:
            lines = infile.read().splitlines()
        nat = int(lines[0].split()[0])
        head = lines[5].split()
        nedos = int(head[2])
        block = np.array([[float(v) for v in line.split()] for line in lines[6:6 + nedos]])
        if block.ndim != 2 or block.shape[0] != nedos:
            raise ValueError("%s: expected %d total-DOS lines." % (filename, nedos))
        if block.shape[1] == 5:
            dos = block[:, 1] + block[:, 2]
        elif block.shape[1] == 3:
            dos = block[:, 1]
        else:
            raise ValueError("%s: unexpected number of columns (%d) in the total-DOS block."
                             % (filename, block.shape[1]))
        E.append(block[:, 0])
        N.append(dos / nat)
        Ef.append(float(head[3]))

    return E, N, Ef


def _read_poscar(filename: str) -> dict:
    """
    Parse a VASP POSCAR/CONTCAR (VASP 4 or 5 format).

    Handles: scale factor (positive = lattice scale, negative = target cell volume in A^3, or three
    factors for the x, y, z Cartesian components), optional element-symbol line, optional "Selective dynamics" line (the T/F flags
    after the coordinates are ignored), Direct or Cartesian coordinates (Cartesian ones are scaled by the
    scale factor as VASP does and converted to fractional).

    :param str filename: path of the POSCAR/CONTCAR file.
    :return: dict with 'cell' (3x3, rows = lattice vectors in A, scale applied), 'species' (list of
             symbols or None for VASP 4 files), 'counts' (atoms per species), 'frac' (nat x 3 fractional
             coordinates), 'volume' (|det(cell)| in A^3), 'selective' (bool).
    :rtype: dict
    """
    with open(filename) as f:
        lines = [l.strip() for l in f.readlines()]
    scale = [float(v) for v in lines[1].split()]
    raw = np.array([[float(v) for v in lines[i].split()[:3]] for i in range(2, 5)])
    if len(scale) == 3:
        s_xyz = np.array(scale)                                   # factors for the x, y, z components
    elif scale[0] < 0:
        s_xyz = np.full(3, (-scale[0] / abs(np.linalg.det(raw))) ** (1 / 3))   # target volume
    else:
        s_xyz = np.full(3, scale[0])
    cell = raw * s_xyz[None, :]
    i = 5
    tokens = lines[i].split()
    if all(t.lstrip('+').isdigit() for t in tokens):
        species = None                                   # VASP 4: counts directly after the lattice
    else:
        species = [t.split('/')[0].split('_')[0] for t in tokens]   # VASP 5 (also "Al_pv" or "Al/<hash>")
        i += 1
    counts = [int(t) for t in lines[i].split()]
    nat = sum(counts)
    i += 1
    selective = lines[i][:1] in ('S', 's')
    if selective:
        i += 1
    cartesian = lines[i][:1] in ('C', 'c', 'K', 'k')
    i += 1
    coords = np.array([[float(v) for v in lines[i + j].split()[:3]] for j in range(nat)])
    if cartesian:
        frac = (coords * s_xyz[None, :]) @ np.linalg.inv(cell)
    else:
        frac = coords
    return {'cell': cell, 'species': species, 'counts': counts, 'frac': frac,
            'volume': abs(np.linalg.det(cell)), 'selective': selective}


def load_V_E(energy_dir_summary: str, energy_dir_contcar: str, units: str = 'eV/atom') -> tuple[np.ndarray, np.ndarray]:
    """
    Loads Energy curve as function of volume from VASP outputs.

    The reference volume per atom is the cell volume of the POSCAR/CONTCAR (absolute determinant of the lattice
    matrix, scale factor applied) divided by the number of atoms. Each SUMMARY line is read as
    "d  ...  ...  E": column 1 is the isotropic linear strain d of that calculation relative to the
    POSCAR/CONTCAR cell (V = V_ref (1 + d)^3), column 4 the total energy of the cell in eV.
    Exact duplicate lines are read once.

    :param energy_dir_summary: Summary file path.
    :type energy_dir_summary: str
    :param energy_dir_contcar: Atoms positions file path (reference cell, d = 0).
    :type energy_dir_contcar: str
    :param units: 'eV/atom' (V in A^3/atom, E in eV/atom) or 'J/mol' (m^3/mol-at, J/mol-at).
    :type units: str
    :return: Energy as function of volume
    :rtype: tuple[np.ndarray,np.ndarray]
    """
    pos = _read_poscar(energy_dir_contcar)
    nat = sum(pos['counts'])
    V_ref = pos['volume'] / nat
    with open(energy_dir_summary) as f_summary:
        f_summary_lines = f_summary.readlines()
        f_summary_lines = list(dict.fromkeys(f_summary_lines))
        ds = []
        E = []
        for l in f_summary_lines:
            l_lst = l.split()
            if not l_lst:
                continue
            ds.append(float(l_lst[0]))
            E.append(float(l_lst[3]) / nat)

    V = [V_ref * (1 + di) ** 3 for di in ds]

    uconvV, uconvE = None, None
    if units == 'J/mol':
        uconvE = EV_ATOM_TO_J_MOL
        uconvV = A3_ATOM_TO_M3_MOL
    elif units == 'eV/atom':
        uconvE, uconvV = 1, 1
    else:
        raise ValueError("load_V_E: units must be 'eV/atom' or 'J/mol'")
    return np.array(V).T * uconvV, np.array(E).T * uconvE


_EM_TITLES = {'symmetrized': 'SYMMETRIZED ELASTIC MODULI (kBar)',
              'ionic': 'ELASTIC MODULI CONTR FROM IONIC RELAXATION (kBar)',
              'total': 'TOTAL ELASTIC MODULI (kBar)'}


def _read_EM_block(lines: list, title: str):
    """Return the 6x6 block printed under `title` in a VASP OUTCAR, or None if the block is absent."""
    for i, line in enumerate(lines):
        if line.strip() == title:
            return np.array([[float(x) for x in row.split()[1:7]] for row in lines[i + 3:i + 9]])
    return None


def load_EM(filename_outcar_eps: str, block: str = 'relaxed') -> np.ndarray:
    """
    Extract the stiffness tensor from the VASP output (OUTCAR for IBRION=6, ISIF>=3).

    The matrix is returned in kBar, in VASP order (XX, YY, ZZ, XY, YZ, ZX).

    :param filename_outcar_eps: file path.
    :type filename_outcar_eps: str
    :param block: 'relaxed' (default) for the relaxed-ion stiffness, i.e. the VASP block
        "TOTAL ELASTIC MODULI"; if that block is absent it is computed as "SYMMETRIZED ELASTIC MODULI"
        + "ELASTIC MODULI CONTR FROM IONIC RELAXATION". 'clamped' for the clamped-ion stiffness
        ("SYMMETRIZED ELASTIC MODULI"), which was the behaviour before v2.9 (review decision D1).
    :type block: str
    :return: Stiffness tensor (kBar).
    :rtype: np.ndarray
    """
    if block not in ('relaxed', 'clamped'):
        raise ValueError("load_EM: block must be 'relaxed' or 'clamped', got %r" % (block,))
    with open(filename_outcar_eps) as f:
        lines = f.readlines()
    sym, ion, tot = (_read_EM_block(lines, _EM_TITLES[k]) for k in ('symmetrized', 'ionic', 'total'))
    if block == 'clamped':
        if sym is None:
            raise ValueError("load_EM: no '%s' block in %s" % (_EM_TITLES['symmetrized'], filename_outcar_eps))
        return sym
    if tot is not None:
        return tot
    if sym is not None and ion is not None:
        return sym + ion
    if sym is not None:
        warnings.warn("load_EM: %s has no relaxed-ion moduli (no '%s' or '%s' block); returning the clamped-ion "
                      "'%s' block." % (filename_outcar_eps, _EM_TITLES['total'], _EM_TITLES['ionic'], _EM_TITLES['symmetrized']),
                      UserWarning, stacklevel=2)
        return sym
    raise ValueError("load_EM: no elastic moduli block found in %s (looked for '%s', '%s', '%s')"
                     % (filename_outcar_eps, _EM_TITLES['total'], _EM_TITLES['symmetrized'], _EM_TITLES['ionic']))


def load_cell(filename_contcar: str) -> tuple[str, np.ndarray, np.ndarray]:
    """
    Extract crystal structure from file in VASP format (POSCAR or CONTCAR).

    VASP 4 and 5 formats, scale factor, "Selective dynamics" and Direct or Cartesian coordinates are
    supported (see _read_poscar). For VASP 4 files (no element line) the species are named A, B, C, ...

    :param filename_contcar: File path
    :type filename_contcar: str
    :return: formula (symbols repeated per atom, e.g. 'AlAlAlLi'), cell (rows = lattice vectors in A,
             scale applied) and basis (fractional coordinates).
    :rtype: tuple[str,np.ndarray,np.ndarray]
    """
    pos = _read_poscar(filename_contcar)
    species = pos['species'] if pos['species'] is not None else [chr(65 + k) for k in range(len(pos['counts']))]
    formula = ''.join(sp_i * n_i for sp_i, n_i in zip(species, pos['counts']))
    return formula, pos['cell'], pos['frac']

# #####
# from debyetools.tpropsgui.atomtools import atomic_mass
# import pandas as pd
# from debyetools.aux_functions import load_doscar
# from get_elastic import get_EM
#
#
# class Vdata:
#     def __init__(self):
#         pass
#
#
# def parse_contcar(file_path):
#     try:
#         with open(file_path, 'r') as f:
#             lines = [line.strip() for line in f if line.strip()]
#     except FileNotFoundError:
#         print(f"Error: File '{file_path}' not found.")
#
#     if len(lines) < 7:
#         print("Error: The CONTCAR file is too short to be valid.")
#
#     line6 = lines[5]
#     line7 = lines[6]
#
#     # Determine if line6 contains species or counts
#     if all(item.isdigit() for item in line6.split()):
#         # Line6 contains counts, species not provided
#         print("Error: Element symbols not provided in the CONTCAR file.")
#     else:
#         species = line6.split()
#         counts = list(map(int, line7.split()))
#         if len(species) != len(counts):
#             print("Error: The number of species and counts do not match.")
#
#         formula = []
#         for elem, count in zip(species, counts):
#             formula.extend([elem] * count)
#
#         return formula
#
#
# def average_mass(elements):
#     # Calculate the sum of the masses of the elements in the list
#     atomic_mass['VA'] = 0
#     total_mass = sum(atomic_mass[element] for element in elements)
#     # Calculate the average mass
#     average = total_mass / len(elements)
#     return average
#
#
# def load_energies(file_path):
#     # Read the data into a DataFrame, skipping the first line and using whitespace as the delimiter
#     df = pd.read_csv(file_path, skiprows=1, sep=r'\s+', header=None)
#     # Assign column names based on the header information in the data
#     df.columns = ["Element", "Structure", "Total-energy", "Mag", "A-conv", "Vol-conv", "Vol-at", "R-at", "B/A", "C/A"]
#
#     return df
#
#
# def get_energy(potential):
#     energies_df = load_energies('elements_energies.out')
#     # Query the DataFrame to find the total energy of the element
#     total_energy = energies_df[energies_df['Element'] == potential]['Total-energy'].iloc[0]
#     # print(f"Energy of {element}: {total_energy}")
#     return total_energy
#
#
# def extract_from_DFT(file_path):
#     vdata = Vdata()
#
#     # Extract total energy from DFT calculations
#     path = file_path  # '.'
#     E = []
#     V = []
#     nats = 0
#     E0 = 0
#     vi = 70
#     vf = 130
#     step = 3
#     potentials_set = []
#     for i in range(vi, vf + step, step):
#         try:
#             with open(f'{path}/EvV/{i}/OUTCAR') as f:
#                 Ei = 0
#                 Vi = 0
#                 natsi = 0
#                 lines = f.readlines()
#             for line in lines:
#                 if 'volume of cell' in line:
#                     Vi = float(line.split()[-1])
#                 if 'TOTEN' in line:
#                     Ei = float(line.split()[4])
#                 if 'NIONS' in line:
#                     natsi = float(line.split()[-1])
#                 if 'POTCAR:' in line:
#                     potentials_set.append(line.split()[2])
#             E.append(Ei / natsi)
#             V.append(Vi / natsi)
#             nats = natsi
#             if i == 100:
#                 E0 = Ei / natsi
#
#         except Exception as e:
#             print(f'Warning [process_configurations]: {e}\n')
#     vdata.V = V
#     vdata.E = E
#     potentials_set = set(potentials_set)
#     vdata.potentials = {p.split('_')[0]: p for p in potentials_set}
#     vdata.potentials['VA'] = 'VA'
#
#     vdata.formula = parse_contcar(f'{path}/relaxation/CONTCAR')
#     vdata.nats = nats
#     # compound.multiplicities = multiplicities
#     vdata.mass = average_mass(vdata.formula) / 1000
#     vdata.Ef = E0 - sum([get_energy(vdata.potentials[fi]) for fi in vdata.formula]) / nats  # sum(multiplicities)
#     vdata.E0 = E0
#     vdata.path = path
#
#     list_filetags = [f'/EvV/{i}/DOSCAR' for i in range(70, 130 + 3, 3)]
#     vdata.electric = load_doscar(path, list_filetags=list_filetags)
#
#     EM = get_EM(f'{path}/elastic')
#     # try:
#     #     EM = load_EM(f'{path}/elastic/OUTCAR')
#     # except Exception as e:
#     #     EM = None
#     #     print( f'Warning [process_configurations]: Elastic Moduli not found for {path}.\n')
#     #     print(e)
#     vdata.EM = EM
#
#     return vdata