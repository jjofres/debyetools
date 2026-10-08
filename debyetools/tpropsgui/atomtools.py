import csv
import re

import debyetools.potentials as dt_potentials
import numpy as np
from debyetools import pairanalysis as dt_pa_calc
from debyetools.ndeb import nDeb as dt_nDeb

atomic_symbols = [
    # 0
    'X',
    # 1
    'H', 'He',
    # 2
    'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    # 3
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar',
    # 4
    'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
    'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr',
    # 5
    'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd',
    'In', 'Sn', 'Sb', 'Te', 'I', 'Xe',
    # 6
    'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy',
    'Ho', 'Er', 'Tm', 'Yb', 'Lu',
    'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi',
    'Po', 'At', 'Rn',
    # 7
    'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk',
    'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr',
    'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc',
    'Lv', 'Ts', 'Og']

atomic_numbers = {}
for Z, symbol in enumerate(atomic_symbols):
    atomic_numbers[symbol] = Z

    # Atomic masses are based on:
    #
    #   Meija, J., Coplen, T., Berglund, M., et al. (2016). Atomic weights of
    #   the elements 2013 (IUPAC Technical Report). Pure and Applied Chemistry,
    #   88(3), pp. 265-291. Retrieved 30 Nov. 2016,
    #   from doi:10.1515/pac-2015-0305
    #
    # Standard atomic weights are taken from Table 1: "Standard atomic weights
    # 2013", with the uncertainties ignored.
    # For hydrogen, helium, boron, carbon, nitrogen, oxygen, magnesium, silicon,
    # sulfur, chlorine, bromine and thallium, where the weights are given as a
    # range the "conventional" weights are taken from Table 3 and the ranges are
    # given in the comments.
    # The mass of the most stable isotope (in Table 4) is used for elements
    # where there the element has no stable isotopes (to avoid NaNs): Tc, Pm,
    # Po, At, Rn, Fr, Ra, Ac, everything after Np
atomic_masses = np.array([
    1.0,  # X
    1.008,  # H [1.00784, 1.00811]
    4.002602,  # He
    6.94,  # Li [6.938, 6.997]
    9.0121831,  # Be
    10.81,  # B [10.806, 10.821]
    12.011,  # C [12.0096, 12.0116]
    14.007,  # N [14.00643, 14.00728]
    15.999,  # O [15.99903, 15.99977]
    18.998403163,  # F
    20.1797,  # Ne
    22.98976928,  # Na
    24.305,  # Mg [24.304, 24.307]
    26.9815385,  # Al
    28.085,  # Si [28.084, 28.086]
    30.973761998,  # P
    32.06,  # S [32.059, 32.076]
    35.45,  # Cl [35.446, 35.457]
    39.948,  # Ar
    39.0983,  # K
    40.078,  # Ca
    44.955908,  # Sc
    47.867,  # Ti
    50.9415,  # V
    51.9961,  # Cr
    54.938044,  # Mn
    55.845,  # Fe
    58.933194,  # Co
    58.6934,  # Ni
    63.546,  # Cu
    65.38,  # Zn
    69.723,  # Ga
    72.630,  # Ge
    74.921595,  # As
    78.971,  # Se
    79.904,  # Br [79.901, 79.907]
    83.798,  # Kr
    85.4678,  # Rb
    87.62,  # Sr
    88.90584,  # Y
    91.224,  # Zr
    92.90637,  # Nb
    95.95,  # Mo
    97.90721,  # 98Tc
    101.07,  # Ru
    102.90550,  # Rh
    106.42,  # Pd
    107.8682,  # Ag
    112.414,  # Cd
    114.818,  # In
    118.710,  # Sn
    121.760,  # Sb
    127.60,  # Te
    126.90447,  # I
    131.293,  # Xe
    132.90545196,  # Cs
    137.327,  # Ba
    138.90547,  # La
    140.116,  # Ce
    140.90766,  # Pr
    144.242,  # Nd
    144.91276,  # 145Pm
    150.36,  # Sm
    151.964,  # Eu
    157.25,  # Gd
    158.92535,  # Tb
    162.500,  # Dy
    164.93033,  # Ho
    167.259,  # Er
    168.93422,  # Tm
    173.054,  # Yb
    174.9668,  # Lu
    178.49,  # Hf
    180.94788,  # Ta
    183.84,  # W
    186.207,  # Re
    190.23,  # Os
    192.217,  # Ir
    195.084,  # Pt
    196.966569,  # Au
    200.592,  # Hg
    204.38,  # Tl [204.382, 204.385]
    207.2,  # Pb
    208.98040,  # Bi
    208.98243,  # 209Po
    209.98715,  # 210At
    222.01758,  # 222Rn
    223.01974,  # 223Fr
    226.02541,  # 226Ra
    227.02775,  # 227Ac
    232.0377,  # Th
    231.03588,  # Pa
    238.02891,  # U
    237.04817,  # 237Np
    244.06421,  # 244Pu
    243.06138,  # 243Am
    247.07035,  # 247Cm
    247.07031,  # 247Bk
    251.07959,  # 251Cf
    252.0830,  # 252Es
    257.09511,  # 257Fm
    258.09843,  # 258Md
    259.1010,  # 259No
    262.110,  # 262Lr
    267.122,  # 267Rf
    268.126,  # 268Db
    271.134,  # 271Sg
    270.133,  # 270Bh
    269.1338,  # 269Hs
    278.156,  # 278Mt
    281.165,  # 281Ds
    281.166,  # 281Rg
    285.177,  # 285Cn
    286.182,  # 286Nh
    289.190,  # 289Fl
    289.194,  # 289Mc
    293.204,  # 293Lv
    293.208,  # 293Ts
    294.214,  # 294Og
])
atomic_mass = {k:v for k, v in zip(atomic_symbols, atomic_masses)}

# Covalent radii from:
#
#  Covalent radii revisited,
#  Beatriz Cordero, Verónica Gómez, Ana E. Platero-Prats, Marc Revés,
#  Jorge Echeverría, Eduard Cremades, Flavia Barragán and Santiago Alvarez,
#  Dalton Trans., 2008, 2832-2838 DOI:10.1039/B801115J
missing = 0.2
covalent_radii = np.array([
    missing,  # X
    0.31,  # H
    0.28,  # He
    1.28,  # Li
    0.96,  # Be
    0.84,  # B
    0.76,  # C
    0.71,  # N
    0.66,  # O
    0.57,  # F
    0.58,  # Ne
    1.66,  # Na
    1.41,  # Mg
    1.21,  # Al
    1.11,  # Si
    1.07,  # P
    1.05,  # S
    1.02,  # Cl
    1.06,  # Ar
    2.03,  # K
    1.76,  # Ca
    1.70,  # Sc
    1.60,  # Ti
    1.53,  # V
    1.39,  # Cr
    1.39,  # Mn
    1.32,  # Fe
    1.26,  # Co
    1.24,  # Ni
    1.32,  # Cu
    1.22,  # Zn
    1.22,  # Ga
    1.20,  # Ge
    1.19,  # As
    1.20,  # Se
    1.20,  # Br
    1.16,  # Kr
    2.20,  # Rb
    1.95,  # Sr
    1.90,  # Y
    1.75,  # Zr
    1.64,  # Nb
    1.54,  # Mo
    1.47,  # Tc
    1.46,  # Ru
    1.42,  # Rh
    1.39,  # Pd
    1.45,  # Ag
    1.44,  # Cd
    1.42,  # In
    1.39,  # Sn
    1.39,  # Sb
    1.38,  # Te
    1.39,  # I
    1.40,  # Xe
    2.44,  # Cs
    2.15,  # Ba
    2.07,  # La
    2.04,  # Ce
    2.03,  # Pr
    2.01,  # Nd
    1.99,  # Pm
    1.98,  # Sm
    1.98,  # Eu
    1.96,  # Gd
    1.94,  # Tb
    1.92,  # Dy
    1.92,  # Ho
    1.89,  # Er
    1.90,  # Tm
    1.87,  # Yb
    1.87,  # Lu
    1.75,  # Hf
    1.70,  # Ta
    1.62,  # W
    1.51,  # Re
    1.44,  # Os
    1.41,  # Ir
    1.36,  # Pt
    1.36,  # Au
    1.32,  # Hg
    1.45,  # Tl
    1.46,  # Pb
    1.48,  # Bi
    1.40,  # Po
    1.50,  # At
    1.50,  # Rn
    2.60,  # Fr
    2.21,  # Ra
    2.15,  # Ac
    2.06,  # Th
    2.00,  # Pa
    1.96,  # U
    1.90,  # Np
    1.87,  # Pu
    1.80,  # Am
    1.69,  # Cm
    missing,  # Bk
    missing,  # Cf
    missing,  # Es
    missing,  # Fm
    missing,  # Md
    missing,  # No
    missing,  # Lr
    missing,  # Rf
    missing,  # Db
    missing,  # Sg
    missing,  # Bh
    missing,  # Hs
    missing,  # Mt
    missing,  # Ds
    missing,  # Rg
    missing,  # Cn
    missing,  # Nh
    missing,  # Fl
    missing,  # Mc
    missing,  # Lv
    missing,  # Ts
    missing,  # Og
])
atomic_radii = {k:v for k, v in zip(atomic_symbols, covalent_radii)}


atomic_colors = np.array([
[1.    ,0.   , 0.   ],
[1.    ,1.   , 1.   ],
[0.851 ,1.   , 1.   ],
[0.8   ,0.502, 1.   ],
[0.761 ,1.   , 0.   ],
[1.    ,0.71 , 0.71 ],
[0.565 ,0.565, 0.565],
[0.188 ,0.314, 0.973],
[1.    ,0.051, 0.051],
[0.565 ,0.878, 0.314],
[0.702 ,0.89 , 0.961],
[0.671 ,0.361, 0.949],
[0.541 ,1.   , 0.   ],
[0.749 ,0.651, 0.651],
[0.941 ,0.784, 0.627],
[1.    ,0.502, 0.   ],
[1.    ,1.   , 0.188],
[0.122 ,0.941, 0.122],
[0.502 ,0.82 , 0.89 ],
[0.561 ,0.251, 0.831],
[0.239 ,1.   , 0.   ],
[0.902 ,0.902, 0.902],
[0.749 ,0.761, 0.78 ],
[0.651 ,0.651, 0.671],
[0.541 ,0.6  , 0.78 ],
[0.612 ,0.478, 0.78 ],
[0.878 ,0.4  , 0.2  ],
[0.941 ,0.565, 0.627],
[0.314 ,0.816, 0.314],
[0.784 ,0.502, 0.2  ],
[0.49  ,0.502, 0.69 ],
[0.761 ,0.561, 0.561],
[0.4   ,0.561, 0.561],
[0.741 ,0.502, 0.89 ],
[1.    ,0.631, 0.   ],
[0.651 ,0.161, 0.161],
[0.361 ,0.722, 0.82 ],
[0.439 ,0.18 , 0.69 ],
[0.    ,1.   , 0.   ],
[0.58  ,1.   , 1.   ],
[0.58  ,0.878, 0.878],
[0.451 ,0.761, 0.788],
[0.329 ,0.71 , 0.71 ],
[0.231 ,0.62 , 0.62 ],
[0.141 ,0.561, 0.561],
[0.039 ,0.49 , 0.549],
[0.    ,0.412, 0.522],
[0.753 ,0.753, 0.753],
[1.    ,0.851, 0.561],
[0.651 ,0.459, 0.451],
[0.4   ,0.502, 0.502],
[0.62  ,0.388, 0.71 ],
[0.831 ,0.478, 0.   ],
[0.58  ,0.   , 0.58 ],
[0.259 ,0.62 , 0.69 ],
[0.341 ,0.09 , 0.561],
[0.    ,0.788, 0.   ],
[0.439 ,0.831, 1.   ],
[1.    ,1.   , 0.78 ],
[0.851 ,1.   , 0.78 ],
[0.78  ,1.   , 0.78 ],
[0.639 ,1.   , 0.78 ],
[0.561 ,1.   , 0.78 ],
[0.38  ,1.   , 0.78 ],
[0.271 ,1.   , 0.78 ],
[0.188 ,1.   , 0.78 ],
[0.122 ,1.   , 0.78 ],
[0.    ,1.   , 0.612],
[0.    ,0.902, 0.459],
[0.    ,0.831, 0.322],
[0.    ,0.749, 0.22 ],
[0.    ,0.671, 0.141],
[0.302 ,0.761, 1.   ],
[0.302 ,0.651, 1.   ],
[0.129 ,0.58 , 0.839],
[0.149 ,0.49 , 0.671],
[0.149 ,0.4  , 0.588],
[0.09  ,0.329, 0.529],
[0.816 ,0.816, 0.878],
[1.    ,0.82 , 0.137],
[0.722 ,0.722, 0.816],
[0.651 ,0.329, 0.302],
[0.341 ,0.349, 0.38 ],
[0.62  ,0.31 , 0.71 ],
[0.671 ,0.361, 0.   ],
[0.459 ,0.31 , 0.271],
[0.259 ,0.51 , 0.588],
[0.259 ,0.   , 0.4  ],
[0.    ,0.49 , 0.   ],
[0.439 ,0.671, 0.98 ],
[0.    ,0.729, 1.   ],
[0.    ,0.631, 1.   ],
[0.    ,0.561, 1.   ],
[0.    ,0.502, 1.   ],
[0.    ,0.42 , 1.   ],
[0.329 ,0.361, 0.949],
[0.471 ,0.361, 0.89 ],
[0.541 ,0.31 , 0.89 ],
[0.631 ,0.212, 0.831],
[0.702 ,0.122, 0.831],
[0.702 ,0.122, 0.729],
[0.702 ,0.051, 0.651],
[0.741 ,0.051, 0.529],
[0.78  ,0.   , 0.4  ],
[0.8   ,0.   , 0.349],
[0.82  ,0.   , 0.31 ],
[0.851 ,0.   , 0.271],
[0.878 ,0.   , 0.22 ],
[0.902 ,0.   , 0.18 ],
[0.922 ,0.   , 0.149]])
atomic_color = {k:v for k, v in zip(atomic_symbols, atomic_colors)}

# Elemental reference energies, eV/atom, VASP PAW_PBE, keyed by the exact POTCAR name (e.g. 'Cr' and 'Cr_pv'
# differ). Removed (G2): Mg_pv = +1.66 and Mg_sv = +10.21 (positive, not a ground-state energy), Sb = Sm = 0
# (placeholders). Missing potentials are entered by the user in the Reference energies dialog.
atom_energy = {
'VA': -0.00001,
'Ac': -4.04728,
'Ag': -2.71722,
'Ag_pv': -2.70313,
'Al': -3.74653,
'Am': -13.82696,
'As': -4.66991,
'As_d': -4.67909,
'Au': -3.22003,
'B': -6.7048,
'Ba_sv': -1.90828,
'Ba': -1.90828,
'Be': -3.76614,
'Be_sv': -3.76461,
'Bi': -3.87346,
'C': -8.08239,
'Ca_pv': -1.92023,
'Ca_sv': -1.92906,
'Ca': -1.92906,
'Cd': -0.74601,
'Ce': -5.92536,
'Ce_3': -4.73202,
'Ce_h': -5.93196,
'Co': -7.035,
'Co_pv': -7.03163,
'Co_sv': -7.11559,
'Cr': -9.49622,
'Cr_pv': -9.52262,
'Cs_sv': -0.85218,
'Cs': -0.85218,
'Cu': -3.7272,
'Cu_pv': -3.74814,
'Dy': -10.23055,
'Dy_3': -4.53395,
'Er': -1.5556,
'Er_2': -1.5556,
'Er_3': -4.4975,
'Eu': -1.86128,
'Eu_2': -1.86128,
'Eu_3': -4.47305,
'Fe': -8.2367,
'Fe_pv': -8.25688,
'Fe_sv': -8.34199,
'Ga': -2.74138,
'Gd': -13.78906,
'Gd_3': -4.58055,
'Ge': -4.14661,
'Ge_d': -4.51857,
'Hf': -9.95772,
'Hf_pv': -9.92169,
'Hf_sv': -12.73094,
'Hg': -0.17556,
'Ho': -4.51272,
'Ho_3': -4.51272,
'In': -2.55989,
'Ir': -8.84813,
'K_pv': -1.02764,
'K': -1.02764,
'La': -4.88525,
'Li': -1.89944,
'Li_sv': -1.9043,
'Lu': -4.52114,
'Mg': -1.50604,
'Mn': -8.97821,
'Mn_pv': -8.99024,
'Mo': -10.94954,
'Mo_pv': -10.92331,
'Mo_sv': -10.93445,
'Na': -1.30717,
'Na_pv': -1.31099,
'Nb': -10.09319,
'Nb_pv': -10.09319,
'Nb_sv': -10.21612,
'Nd': -7.63427,
'Ni': -5.46695,
'Ni_pv': -5.48727,
'Os': -11.24042,
'Os_pv': -11.22026,
'Pb': -3.57266,
'Pb_d': -3.56435,
'Pd': -5.21615,
'Pd_pv': -5.20817,
'Pm': -6.64195,
'Pr': -6.50444,
'Pt': -6.09738,
'Pt_pv': -6.08161,
'Rb': -0.91693,
'Rb_pv': -0.91693,
'Rb_sv': -0.93605,
'Re': -12.42685,
'Re_pv': -12.37354,
'Rh': -7.2755,
'Rh_pv': -7.25713,
'Ru': -9.25325,
'Ru_pv': -9.2409,
'Ru_sv': -9.27694,
'Sc': -6.20186,
'Sc_sv': -6.24773,
'Se': -3.49831,
'Si': -5.17948,
'Sn': -3.82696,
'Sn_A4': -3.82696,
'Sn_A5': -3.62817,
'Sr': -1.63716,
'Sr_sv': -1.63716,
'Ta': -11.86253,
'Ta_pv': -11.81241,
'Tb': -12.02392,
'Tc': -10.37716,
'Tc_pv': -10.35554,
'Tc_sv': -10.14387,
'Te': -3.14231,
'Ti': -7.76229,
'Ti_pv': -7.80217,
'Ti_sv': -7.81431,
'Tl': -2.24522,
'Tl_d': -2.22995,
'Tm': -4.47605,
'Tm_3': -4.47605,
'V': -8.94078,
'V_pv': -8.95594,
'V_sv': -8.99057,
'W': -13.0194,
'W_pv': -12.95615,
'Y': -6.43328,
'Y_sv': -6.43328,
'Yb': -1.70986,
'Zn': -1.10764,
'Zr_sv': -8.52067,
}


def check_type_in_energies(ti):
    number_of_occurences = 0
    last_occurence = ''
    for key_ai in atom_energy.keys():
        if ti in key_ai:
            number_of_occurences+=1
            last_occurence = key_ai
            # print(key_ai)
    if number_of_occurences == 1:
        return last_occurence
    else:
        return ti

REF_FUNCTIONAL = 'PAW_PBE'  # POTCAR set of the atom_energy values


def read_potentials(path):
    """POTCAR names used in a VASP OUTCAR (or POTCAR), in POTCAR order, from the TITEL lines.

    Returns (functional, [potential, ...]), e.g. ('PAW_PBE', ['Li', 'Al']) or ('PAW_PBE', ['Cr_pv']).
    """
    functional, potentials = None, []
    with open(path, 'r', errors='replace') as f:
        for line in f:
            if 'TITEL' in line:
                words = line.split('=', 1)[1].split()
                functional, potentials = words[0], potentials + [words[1]]
            elif 'ions per type' in line:  # end of the POTCAR block of an OUTCAR
                break
    if not potentials:
        raise ValueError('no TITEL line (POTCAR name) found in %s' % path)
    return functional, potentials


def element_of(potential):
    """Element symbol of a POTCAR name: 'Cr_pv' -> 'Cr', 'H.75' -> 'H', 'Ca_sv_GW' -> 'Ca'."""
    m = re.match('[A-Z][a-z]?', potential)
    return m.group(0) if m else potential


class ReferenceEnergies:
    """Elemental reference energies for the formation energy, for the current GUI session (G2).

    potentials: element -> POTCAR name, read from an OUTCAR / POTCAR or entered by the user;
    sources: element -> where the potential came from; edited: POTCAR name -> eV/atom entered by the user
    (overrides atom_energy, not saved to disk).
    Enthalpies at 298.15 K for the formation enthalpy DH298 (G14), J/mol-atom on the same energy scale as E0:
    h298_runs: POTCAR name -> (H298, source, Debye mode) stored by every pure-element run of the session;
    h298_edited: POTCAR name -> H298 entered by the user (overrides the runs; e.g. gases such as O2).
    """

    def __init__(self):
        self.potentials = {}
        self.sources = {}
        self.functional = None
        self.edited = {}
        self.h298_runs = {}
        self.h298_edited = {}
        self.table_path = None  # last reference table saved or loaded

    def read_outcar(self, path):
        """Set the potential of every element found in an OUTCAR / POTCAR; returns the {element: potential} read."""
        functional, potentials = read_potentials(path)
        found = {element_of(p): p for p in potentials}
        for el, p in found.items():
            self.potentials[el] = p
            self.sources[el] = path
        self.functional = functional
        return found

    def potential(self, element):
        """POTCAR name for an element; the plain symbol if none was read or entered (flagged by assumed())."""
        return self.potentials.get(element, element)

    def assumed(self, element):
        return element not in self.potentials

    def energy(self, potential):
        """eV/atom for an exact POTCAR name (no substring matching), None if unknown."""
        e = self.edited.get(potential, atom_energy.get(potential))
        return None if e is None else float(e)

    def h298(self, potential):
        """H at 298.15 K, J/mol-atom, for an exact POTCAR name: entered value, else pure-element run, else None."""
        if potential in self.h298_edited:
            return float(self.h298_edited[potential])
        if potential in self.h298_runs:
            return float(self.h298_runs[potential][0])
        return None


REFERENCES = ReferenceEnergies()


def interatomic_initial_guess(eos_str, n_pair_types):
    """Default initial parameters of the interatomic potentials for a crystal with n_pair_types pair types
    (n element types give n(n+1)/2 pair types): Morse 3 per pair type; EAM 6 per pair type (pair and density
    functions) + 4 per element type (embedding function). None for the analytic EOS."""
    ntypes = int(round(-0.5 + np.sqrt(0.25 + 2 * n_pair_types)))
    if eos_str == 'MP':
        return [0.35, 1, 3.2] * n_pair_types
    if eos_str == 'EAM':
        return ([3.65e-03, 1.24e-02, 2.68e-04, 1.03e-02, 1.49e-01, 5.22e-02] * n_pair_types
                + [2.26e+00, 6.61e-02, 3.01e-01, 5.31e-05] * ntypes)
    return None

REF_TABLE_COLUMNS = ['POTCAR', 'E_ref_eV_atom', 'H298_J_mol_atom', 'H298_from', 'Debye_model', 'source']


def save_reference_table(path, edited, h298_runs, h298_edited):
    """Write the session references to a CSV file (one row per POTCAR name), so element runs and entered values
    carry over between sessions. E_ref: only values entered by the user (the tabulated atom_energy values are not
    repeated); H298: the effective value – entered if there is one, else from a pure-element run (with its Debye
    model and source). Returns the number of rows written."""
    pots = sorted(set(edited) | set(h298_runs) | set(h298_edited))
    with open(path, 'w', newline='') as f:
        f.write('# debyetools reference energies (GUI). E_ref: static energy, eV/atom; H298: H at 298.15 K, J/mol-atom,\n'
                '# same energy scale as the E(V) data. Valid only with the same VASP settings (ENCUT, k-points, POTCAR).\n')
        w = csv.writer(f)
        w.writerow(REF_TABLE_COLUMNS)
        for pot in pots:
            E = '' if pot not in edited else repr(float(edited[pot]))
            if pot in h298_edited:
                H, frm, model, src = repr(float(h298_edited[pot])), 'entered', '', 'entered'
            elif pot in h298_runs:
                H, src, model = h298_runs[pot]
                H, frm = repr(float(H)), 'run'
            else:
                H, frm, model, src = '', '', '', ''
            w.writerow([pot, E, H, frm, model, src])
    return len(pots)


def load_reference_table(path):
    """Read a file written by save_reference_table. Returns (edited, h298_runs, h298_edited) dictionaries
    (same meaning as in ReferenceEnergies); ValueError with the line number for an unreadable row."""
    edited, h298_runs, h298_edited = {}, {}, {}
    with open(path, newline='') as f:
        rows = [(i + 1, r) for i, r in enumerate(csv.reader(f)) if r and not r[0].lstrip().startswith('#')]
    if not rows or [c.strip() for c in rows[0][1]] != REF_TABLE_COLUMNS:
        raise ValueError('%s: not a reference table (header %s expected)' % (path, ', '.join(REF_TABLE_COLUMNS)))
    for line, r in rows[1:]:
        r = [c.strip() for c in r] + [''] * (len(REF_TABLE_COLUMNS) - len(r))
        pot, E, H, frm, model, src = r[:6]
        try:
            if not pot:
                raise ValueError('empty POTCAR name')
            if E:
                edited[pot] = float(E)
            if H:
                if frm == 'run':
                    h298_runs[pot] = (float(H), src or 'run (file)', model)
                elif frm in ('entered', ''):
                    h298_edited[pot] = float(H)
                else:
                    raise ValueError("H298_from must be 'run' or 'entered', not '%s'" % frm)
        except ValueError as e:
            raise ValueError('%s, line %d: %s' % (path, line, e))
    return edited, h298_runs, h298_edited


class atomSingle:
    def __init__(self, type, coords):
        self.type = type
        self.position = coords
        self.mass = atomic_mass[type.split('_')[0]]
        self.radii = atomic_radii[type.split('_')[0]]
        # None when no reference energy is tabulated (e.g. O, N): the crystal dialog only plots the atoms and used
        # to stop with a KeyError for any oxide or nitride (G2)
        self.energy = atom_energy.get(check_type_in_energies(type))

class atomsPositions:
    def __init__(self, formula, cell, basis):
        self._current_index = 0
        self._nats = len(basis)

        self.types =  re.findall('[A-Z][^A-Z]*', formula)
        self.positions = np.dot(basis, cell)

    def __iter__(self):
        self._current_index = 0
        return self

    def __next__(self):
        if self._current_index < self._nats:
            type_i = self.types[self._current_index]
            atom = atomSingle(type_i, self.positions[self._current_index])
            self._current_index+=1
            return atom

        raise StopIteration

    def __len__(self):
        return self._nats



class Molecule:
    def __init__(self):
        pass

    def initialize_ndeb(self, mode):
        self.ndeb = dt_nDeb(self.nu, self.mass, self.p_anh, self.eos,
                         self.p_el, self.p_def, self.p_xs, mode=mode, r=self.r, xsparams = self.xsparams)

    def set_eos(self, eos_str, args):
        self.eos_str = eos_str
        self.eos = getattr(dt_potentials, eos_str)(*args)
        self.eos.fitEOS([1e-5], [0], initial_parameters=np.array(self.initial_params), fit=False)

    def min_G(self, T, P):
     self.P = P
     self.T, self.V = self.ndeb.min_G(T, self.eos.V0, P=P)


    def eval_props(self):
        self.tprops_dict = self.ndeb.eval_props(self.T, self.V, P=self.P)

    def update_fomula(self, types):
        self.types = types
        self.formula = ''.join([s for s in types])

    def run_pa(self, cutoff):
        self.cutoff = cutoff
        self.distances, self.num_bonds_per_formula, self.combs_types = dt_pa_calc.pair_analysis(self.formula, self.cutoff, self.basis, self.cell)
