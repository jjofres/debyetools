from debyetools.ndeb import nDeb as dt_nDeb
import debyetools.potentials as dt_potentials
from debyetools import pairanalysis as dt_pa_calc

import numpy as np
import re

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


atomic_colors = np.array([[1.    ,0.   , 0.   ],
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


class atomSingle:
    def __init__(self, type, coords):
        self.type = type
        self.position = coords
        self.mass = atomic_mass[type]
        self.radii = atomic_radii[type]

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
            atom = atomSingle(self.types[self._current_index], self.positions[self._current_index])
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
                         self.p_el, self.p_def, self.p_xs, mode=mode)

    def set_eos(self, eos_str, args):
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
