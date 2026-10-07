import os
import numpy as np
import re
from scipy.optimize import curve_fit
from debyetools.constants import EV_A3_TO_GPA, KBAR_TO_GPA

# eV/A^3 -> kBar (same unit as aux_functions.load_EM and poisson.quiet_pa)
EV_A3_TO_KBAR = EV_A3_TO_GPA / KBAR_TO_GPA

def parse_outcar(outcar_path):
    """
    Read the final free energy and cell volume from a VASP OUTCAR.

    Both values are taken from the last occurrence in the file, so they refer
    to the same (final) cell. The first "volume of cell" line in an OUTCAR
    belongs to the symmetry analysis and can be the primitive-cell volume,
    which differs from the volume of the simulation cell.

    :param str outcar_path: path to the OUTCAR file.
    :return: energy (eV per cell) and volume (A^3 per cell).
    :rtype: tuple[float, float]
    """
    with open(outcar_path, 'r') as file:
        lines = file.readlines()

    energy = None
    volume = None

    # Scan backwards and keep the first match found, i.e. the last one in the file
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]
        if energy is None and "FREE ENERGIE OF THE ION-ELECTRON SYSTEM" in line:
            for toten in lines[i + 1:i + 4]:
                if "TOTEN" in toten:
                    energy = float(toten.split('=')[1].split()[0])
                    break
        if volume is None and "volume of cell :" in line:
            volume = float(line.split()[-1])
        if energy is not None and volume is not None:
            break

    if energy is None or volume is None:
        raise ValueError(f'parse_outcar: energy or volume not found in {outcar_path}.')

    return energy, volume

# Quadratic function for fitting
def quadratic_fun(delta, eps, E0, V0):
    return E0 + V0/2 * eps * delta**2

def get_EM(base_dir):
    """
    Elastic constants from energy-strain calculations.

    Expects base_dir/eps1 ... eps9, each with subfolders 98 ... 102 (strain
    -2% ... +2%) containing an OUTCAR. Energies are fitted to
    E = E0 + V0/2 * eps * delta**2, with E0 and V0 from the unstrained cell.

    :param str base_dir: folder containing eps1 ... eps9.
    :return: 6x6 stiffness matrix in kBar (Voigt order XX YY ZZ YZ ZX XY),
             same unit as aux_functions.load_EM.
    :rtype: np.ndarray
    """

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
        'C11': C11*EV_A3_TO_KBAR,
        'C12': C12*EV_A3_TO_KBAR,
        'C13': C13*EV_A3_TO_KBAR,
        'C14': 0,
        'C15': 0,
        'C16': 0,
        'C21': C12*EV_A3_TO_KBAR,
        'C22': C22*EV_A3_TO_KBAR,
        'C23': C23*EV_A3_TO_KBAR,
        'C24': 0,
        'C25': 0,
        'C26': 0,
        'C31': C13*EV_A3_TO_KBAR,
        'C32': C23*EV_A3_TO_KBAR,
        'C33': C33*EV_A3_TO_KBAR,
        'C34': 0,
        'C35': 0,
        'C36': 0,
        'C41': 0,
        'C42': 0,
        'C43': 0,
        'C44': C44*EV_A3_TO_KBAR,
        'C45': 0,
        'C46': 0,
        'C51': 0,
        'C52': 0,
        'C53': 0,
        'C54': 0,
        'C55': C55*EV_A3_TO_KBAR,
        'C56': 0,
        'C61': 0,
        'C62': 0,
        'C63': 0,
        'C64': 0,
        'C65': 0,
        'C66': C66*EV_A3_TO_KBAR,

    }

    for i in range(0,6):
        for j in range(0,6):
            EM[i,j] = elastic_constants[f'C{i+1}{j+1}']
    return EM
