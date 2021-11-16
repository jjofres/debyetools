import unittest
import numpy as np
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts
from debyetools.fs_compound_db import fit_FS
import debyetools.potentials as potentials
from debyetools.electronic import fit_electronic
from debyetools.poisson import poisson_ratio
from debyetools.aux_functions import load_doscar, load_V_E, load_EM
# EOS parametrization
#=========================
V_DFT, E_DFT = load_V_E('../../tests/inpt_files/Al_fcc', '../../tests/inpt_files/Al_fcc/CONTCAR.5', units='J/mol')
EOS_name = 'BM4'
initial_parameters =  [-3.6e+05, 9.9e-06, -7.8e+10, 4.7e+00, 1.e-10]
eos_BM4 = getattr(potentials,EOS_name)()
eos_BM4.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters)
p_EOS = eos_BM4.pEOS
#=========================

# Electronic Contributions
#=========================
p_el_inittial = [3.8027342892e-01, -1.8875015171e-02,
                 5.3071034596e-04, -7.0100707467e-06]
E, N, Ef = load_doscar('../../tests/inpt_files/Al_fcc/DOSCAR.EvV.')
p_electronic = fit_electronic(V_DFT, p_el_inittial,E,N,Ef)
#=========================

# Other Contributions parametrization
#=========================
Tmelting = 933
p_defects = 8.46, 1.69, Tmelting, 0.1, p_EOS[2], p_EOS[1]
p_intanh = 0, 1, p_EOS[1]
p_anh = 0, 0, 0
#=========================

# Poisson's ratio
#=========================
EM = EM = load_EM('../../tests/inpt_files/Al_fcc/OUTCAR.eps')
nu = poisson_ratio(EM)
#=========================

# F minimization
#=========================
m = 0.026981500000000002
ndeb_BM4 = nDeb(nu, m, p_intanh, p_EOS, p_electronic,
                p_defects, p_anh, EOS_name)

T_initial, T_final, number_Temps = 0.1, 1000, 10
T = gen_Ts(T_initial, T_final, number_Temps)

T, V = ndeb_BM4.min_F(T,p_EOS[1])
#=========================

# Evaluations
#=========================
tprops_dict = ndeb_BM4.eval_props(T,V)

T_from = 298.15
T_to = 1000
#=========================

# FS comp db parameters
#=========================
FS_db_params = fit_FS(tprops_dict,T_from, T_to)
print(FS_db_params['Cp'])
#=========================
