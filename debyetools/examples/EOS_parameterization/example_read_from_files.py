import numpy as np
import debyetools.potentials as potentials
from debyetools.aux_functions import load_V_E
V_data, E_data = load_V_E('../Al_fcc/SUMMARY', '../Al_fcc/CONTCAR')
V_data, E_data = V_data*(1E-30*6.02E+23), E_data*(1.60218E-19 * 6.02214E+23)
params_initial_guess = [-3e5, 1e-5, 7e10, 4]
Birch_Murnaghan = potentials.BM()
Birch_Murnaghan.fitEOS(V_data, E_data, params_initial_guess)
print(Birch_Murnaghan.pEOS)
