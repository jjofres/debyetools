import itertools as it
import re
import numpy as np
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
    :param int nTs: Number of values. This does not include room temperature, which is included anyways.

    :retun np.ndarray: Values of temperatures between Ti and Tf, inclusive, plus room temperature.
    """
    minF_step = (Tf - Ti) / (nTs - 1.)
    Ts = np.arange(Ti, Tf + minF_step, minF_step)
    Ts = np.r_[Ts, [298.15]]
    Ts.sort()
    return Ts


def gen_Ps(Pi, Pf, nPs):
    """
    Function to generate a range of pressures.

    :param float Pi: Initial pressure.
    :param float Pf: Final pressure.
    :param int nPs: Number of values. This does not include room pressure, which is included anyways.

    :retun: Values of pressures between Pi and Pf.
    :rtype: np.ndarray
    """
    if nPs <= 1: return np.array([Pi])
    minF_step = (Pf - Pi) / (nPs - 1.)
    Ps = np.arange(Pi, Pf + 1, minF_step)

    return Ps


def load_doscar(filename_sufix: str, list_filetags: list = None) -> tuple[list, list, list]:
    """
    Extract electronic density, energies and Fermi level as function of volume from DOSCAR's.
    :param filename_sufix: folder path.
    :type filename_sufix: str
    :param list_filetags: filename tags.
    :type list_filetags: list
    :return: E,N,Ef.
    :rtype: tuple[list,list,list]
    """
    if list_filetags is None:
        list_filetags = ['-0.10', '-0.09', '-0.08', '-0.07', '-0.06', '-0.05', '-0.04', '-0.03',
                         '-0.02', '-0.01', '-0.00', '0.01', '0.02', '0.03', '0.04', '0.05', '0.06',
                         '0.07', '0.08', '0.09', '0.10']

    list_filetags = [str(li) for li in list_filetags]
    E = []
    N = []
    Ef = []
    nat = 0
    for dosfile in list_filetags:
        countline = 0
        EN = []

        filename = filename_sufix + dosfile
        with open(filename) as infile:
            for line in infile:
                if countline == 0:
                    nat = float(line.split()[0])
                if countline == 5:
                    Ef.append(float(line.split()[3]))
                if countline > 5:
                    EN.append(line.split()[0:2])

                countline += 1
        ENAl = np.array(EN)
        # print(dosfile, EN)
        E.append([float(s) for s in list(ENAl[:, 0])])
        N.append([float(s) / nat for s in list(ENAl[:, 1])])

    return E, N, Ef


def load_V_E(energy_dir_summary: str, energy_dir_contcar: str, units: str = 'eV/atom') -> tuple[np.ndarray, np.ndarray]:
    """
    Loads Energy curve as function of volume from VASP outputs.
    :param energy_dir_summary: Summary file path.
    :type energy_dir_summary: str
    :param energy_dir_contcar: Atoms positions file path.
    :type energy_dir_contcar: str
    :param units: units.
    :type units: str
    :return: Energy as function of volume
    :rtype: tuple[np.ndarray,np.ndarray]
    """
    with open(energy_dir_contcar, 'r') as f_poscar:
        f_poscar_lines = f_poscar.readlines()
        cell_poscar = f_poscar_lines[2:5]

        cell_lst = [c.split() for c in cell_poscar]
        diag_cell = [float(c[i]) for i, c in enumerate(cell_lst)]

        try:
            nat = sum([int(li) for li in np.fromstring(f_poscar_lines[5], dtype=int, sep=' ')])
            1 / nat
        except:
            nat = sum([int(li) for li in np.fromstring(f_poscar_lines[6], dtype=int, sep=' ')])
            1 / nat
    with open(energy_dir_summary) as f_summary:
        f_summary_lines = f_summary.readlines()
        f_summary_lines = list(dict.fromkeys(f_summary_lines))
        ds = []
        E = []
        for l in f_summary_lines:
            l_lst = l.split(' ')
            ds.append(float(l_lst[0]))
            E.append(float(l_lst[3]) / nat)

    V = []
    for di in ds:
        V.append(np.product(np.array(diag_cell) * (1 + di)) / nat)

    uconvV, uconvE = None, None
    if units == 'J/mol':
        uconvE = (0.160218e-18 * 6.02214e23)
        uconvV = (1e-30 * 6.02e23)
    elif units == 'eV/atom':
        uconvE, uconvV = 1, 1
    return np.array(V).T * uconvV, np.array(E).T * uconvE


def load_EM(filename_outcar_eps: str) -> np.ndarray:
    """
    Extract the stiffness tensor from the VASP output (OUTCAR for IBRION=6).
    :param filename_outcar_eps: file path.
    :type filename_outcar_eps: str
    :return: Stiffness tensor.
    :rtype: np.ndarray
    """
    EM = []

    with open(filename_outcar_eps) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith('  SYMMETRIZED ELASTIC MODULI (kBar)'):
                j = i + 3
                data = lines[j:j + 6]
                break

    for line in data:
        EM += [[float(x) for x in line.split()[1:]]]
    EM = np.array(EM)

    return EM


def load_cell(filename_contcar: str) -> tuple[str, np.ndarray, np.ndarray]:
    """
    Extract crystal structure from file in VASP format (POSCAR or CONTCAR).
    :param filename_contcar: File path
    :type filename_contcar: str
    :return: formula,, cell, and basis.
    :rtype: tuple[str,np.ndarray,np.ndarray]
    """
    with open(filename_contcar) as f:
        poscar_lines = f.readlines()
    mult = float(poscar_lines[1])
    cell = np.array([np.fromstring(line_i, dtype=float, sep=' ') for line_i in poscar_lines[2:5]])
    cell = cell * mult

    ix_nats = 6
    re.findall('[A-Z][^A-Z]*', 'ABC')
    ats_types = re.findall('[A-Z][^A-Z]*',
                           poscar_lines[ix_nats - 1].replace('  ', '').replace(' ', '').replace('\n', ''))
    ats_types = [ai + 'x' for ai in ats_types]
    nats = np.fromstring(poscar_lines[ix_nats], dtype=int, sep=' ')

    formula_lst = []
    for at_i, na_i in zip(ats_types, nats):
        formula_lst.append(at_i * na_i)
    formula = ''.join(formula_lst)
    tots_nats = sum(nats)

    basis = np.array([np.fromstring(line_i, dtype=float, sep=' ') for line_i in poscar_lines[8:8 + tots_nats]])
    # basis = np.dot(basis,cell)

    return formula.replace('x', ''), cell, basis

#####
import os
import numpy as np
import re
from scipy.optimize import curve_fit

# Function to parse energy and volume from OUTCAR
def parse_outcar(outcar_path):
    with open(outcar_path, 'r') as file:
        lines = file.readlines()

    energy = None
    volume = None

    # Find the last occurrence of energy and volume in the OUTCAR
    for line in lines[::-1]:
        if "FREE ENERGIE OF THE ION-ELECTRON SYSTEM" in line:
            energy = float(re.findall(r"[-+]?\d*\.\d+|\d+", lines[lines.index(line)+2])[0])
        if "volume of cell :" in line:
            volume = float(line.split()[-1])

    return energy, volume

# Quadratic function for fitting
def quadratic_fun(delta, eps, E0, V0):
    return E0 + V0/2 * eps * delta**2

def get_EM(base_dir):

    # Base directory containing d1 to d6 folders
    # base_dir = './elastic/'

    # Prepare a list to store the epsilon values
    epsilons = []

    # Loop over each d* folder
    for d in range(1, 10):
        d_folder = os.path.join(base_dir, f'eps{d}')

        strains = []
        energies = []

        # Loop over subfolders '98' to '102'
        for delta_folder in ['98', '99', '100', '101', '102']:
            sub_folder = os.path.join(d_folder, delta_folder)
            outcar_path = os.path.join(sub_folder, 'OUTCAR')

            # Parse energy and volume from OUTCAR
            energy, volume = parse_outcar(outcar_path)

            # For the '100' subfolder, get E0 and V0
            if delta_folder == '100':
                E0 = energy
                V0 = volume

            # Calculate strain (delta) from folder name
            delta = (int(delta_folder) - 100) / 100.0
            strains.append(delta)
            energies.append(energy)

        # Convert to numpy arrays for fitting
        strains = np.array(strains)
        energies = np.array(energies)

        # Fit the quadratic function to the energy vs. strain data
        quadratic = lambda delta, eps: quadratic_fun(delta, eps, E0, V0)
        popt, _ = curve_fit(quadratic, strains, energies)

        # Extract the epsilon (eps) for this deformation
        epsilon = popt[0]
        epsilons.append(epsilon)

    # Now solve the system of equations using the epsilons to get the Cij constants
    C11 = epsilons[0]
    C22 = epsilons[1]
    C33 = epsilons[2]
    C44 = epsilons[3]/4
    C55 = epsilons[4]/4
    C66 = epsilons[5]/4
    C12 = (epsilons[0]+epsilons[1]-epsilons[6])/2
    C13 = (epsilons[0]+epsilons[2]-epsilons[7])/2
    C23 = (epsilons[1]+epsilons[2]-epsilons[8])/2
    # Store the calculated elastic constants
    EM =np.zeros((6,6))
    elastic_constants = {
        'C11': C11*160.21766208,
        'C12': C12*160.21766208,
        'C13': C13*160.21766208,
        'C14': 0,
        'C15': 0,
        'C16': 0,
        'C21': C12*160.21766208,
        'C22': C22*160.21766208,
        'C23': C23*160.21766208,
        'C24': 0,
        'C25': 0,
        'C26': 0,
        'C31': C13*160.21766208,
        'C32': C23*160.21766208,
        'C33': C33*160.21766208,
        'C34': 0,
        'C35': 0,
        'C36': 0,
        'C41': 0,
        'C42': 0,
        'C43': 0,
        'C44': C44*160.21766208,
        'C45': 0,
        'C46': 0,
        'C51': 0,
        'C52': 0,
        'C53': 0,
        'C54': 0,
        'C55': C55*160.21766208,
        'C56': 0,
        'C61': 0,
        'C62': 0,
        'C63': 0,
        'C64': 0,
        'C65': 0,
        'C66': C66*160.21766208,

    }

    for i in range(0,6):
        for j in range(0,6):
            EM[i,j] = elastic_constants[f'C{i+1}{j+1}']
    return EM

#####
from debyetools.tpropsgui.atomtools import atomic_mass
import pandas as pd
from debyetools.aux_functions import load_doscar
# from get_elastic import get_EM


class Vdata:
    def __init__(self):
        pass


def parse_contcar(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")

    if len(lines) < 7:
        print("Error: The CONTCAR file is too short to be valid.")

    line6 = lines[5]
    line7 = lines[6]

    # Determine if line6 contains species or counts
    if all(item.isdigit() for item in line6.split()):
        # Line6 contains counts, species not provided
        print("Error: Element symbols not provided in the CONTCAR file.")
    else:
        species = line6.split()
        counts = list(map(int, line7.split()))
        if len(species) != len(counts):
            print("Error: The number of species and counts do not match.")

        formula = []
        for elem, count in zip(species, counts):
            formula.extend([elem] * count)

        return formula


def average_mass(elements):
    # Calculate the sum of the masses of the elements in the list
    atomic_mass['VA'] = 0
    total_mass = sum(atomic_mass[element] for element in elements)
    # Calculate the average mass
    average = total_mass / len(elements)
    return average


def load_energies(file_path):
    # Read the data into a DataFrame, skipping the first line and using whitespace as the delimiter
    df = pd.read_csv(file_path, skiprows=1, sep=r'\s+', header=None)
    # Assign column names based on the header information in the data
    df.columns = ["Element", "Structure", "Total-energy", "Mag", "A-conv", "Vol-conv", "Vol-at", "R-at", "B/A", "C/A"]

    return df


def get_energy(potential):
    energies_df = load_energies('elements_energies.out')
    # Query the DataFrame to find the total energy of the element
    total_energy = energies_df[energies_df['Element'] == potential]['Total-energy'].iloc[0]
    # print(f"Energy of {element}: {total_energy}")
    return total_energy


def extract_from_DFT(file_path):
    vdata = Vdata()

    # Extract total energy from DFT calculations
    path = file_path  # '.'
    E = []
    V = []
    nats = 0
    E0 = 0
    vi = 70
    vf = 130
    step = 3
    potentials_set = []
    for i in range(vi, vf + step, step):
        try:
            with open(f'{path}/EvV/{i}/OUTCAR') as f:
                Ei = 0
                Vi = 0
                natsi = 0
                lines = f.readlines()
            for line in lines:
                if 'volume of cell' in line:
                    Vi = float(line.split()[-1])
                if 'TOTEN' in line:
                    Ei = float(line.split()[4])
                if 'NIONS' in line:
                    natsi = float(line.split()[-1])
                if 'POTCAR:' in line:
                    potentials_set.append(line.split()[2])
            E.append(Ei / natsi)
            V.append(Vi / natsi)
            nats = natsi
            if i == 100:
                E0 = Ei / natsi

        except Exception as e:
            print(f'Warning [process_configurations]: {e}\n')
    vdata.V = V
    vdata.E = E
    potentials_set = set(potentials_set)
    vdata.potentials = {p.split('_')[0]: p for p in potentials_set}
    vdata.potentials['VA'] = 'VA'

    vdata.formula = parse_contcar(f'{path}/relaxation/CONTCAR')
    vdata.nats = nats
    # compound.multiplicities = multiplicities
    vdata.mass = average_mass(vdata.formula) / 1000
    vdata.Ef = E0 - sum([get_energy(vdata.potentials[fi]) for fi in vdata.formula]) / nats  # sum(multiplicities)
    vdata.E0 = E0
    vdata.path = path

    list_filetags = [f'/EvV/{i}/DOSCAR' for i in range(70, 130 + 3, 3)]
    vdata.electric = load_doscar(path, list_filetags=list_filetags)

    EM = get_EM(f'{path}/elastic')
    # try:
    #     EM = load_EM(f'{path}/elastic/OUTCAR')
    # except Exception as e:
    #     EM = None
    #     print( f'Warning [process_configurations]: Elastic Moduli not found for {path}.\n')
    #     print(e)
    vdata.EM = EM

    return vdata