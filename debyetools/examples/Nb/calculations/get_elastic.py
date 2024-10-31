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
