import numpy as np
import debyetools.potentials as potentials
from debyetools.aux_functions import load_V_E
from debyetools.constants import A3_ATOM_TO_M3_MOL, EV_ATOM_TO_J_MOL
V_data, E_data = load_V_E('../Al_fcc/SUMMARY', '../Al_fcc/CONTCAR')
V_data, E_data = V_data*A3_ATOM_TO_M3_MOL, E_data*EV_ATOM_TO_J_MOL
params_initial_guess = [-3e5, 1e-5, 7e10, 4]
Birch_Murnaghan = potentials.BM()
Birch_Murnaghan.fitEOS(V_data, E_data, params_initial_guess)
print(Birch_Murnaghan.pEOS)
