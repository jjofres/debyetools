from debyetools.tpropsgui.atomtools import atomic_mass
import pandas as pd
from debyetools.aux_functions import load_doscar
from debyetools.get_elastic import get_EM


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


def get_energy(potential, current_path):
    energies_df = load_energies(f'{current_path}/elements_energies.out')
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
    current_folder = f'{path}'
    vdata.Ef = E0 - sum([get_energy(vdata.potentials[fi], current_folder) for fi in vdata.formula]) / nats  # sum(multiplicities)
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