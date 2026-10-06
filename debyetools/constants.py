"""
Physical constants and unit conversions used by debyetools.

Values are the exact SI-2019 definitions (CODATA 2018 and later): h, e, k_B and N_A are exact,
hbar = h / (2*pi). Every module must import its constants from here (review finding 1.1-1.3).
"""
import math

h = 6.62607015e-34            # Planck constant [J s]
hbar = h / (2 * math.pi)      # reduced Planck constant [J s] = 1.0545718176461565e-34
kB = 1.380649e-23             # Boltzmann constant [J/K]
NAv = 6.02214076e23           # Avogadro constant [1/mol]
eV = 1.602176634e-19          # electron volt [J]
R = kB * NAv                  # molar gas constant [J/(mol K)]

# unit conversions
EV_ATOM_TO_J_MOL = eV * NAv           # eV/atom   -> J/mol-atom
A3_ATOM_TO_M3_MOL = 1e-30 * NAv       # A^3/atom  -> m^3/mol-atom
EV_A3_TO_GPA = eV * 1e30 / 1e9        # eV/A^3    -> GPa (160.21766...)
KBAR_TO_GPA = 0.1                     # kBar      -> GPa
