
from debyetools.ndeb import nDeb
import numpy as np
import debyetools.potentials as potentials
from debyetools.aux_functions import gen_Ts
import debyetools.tpropsgui.plotter as plot

from debyetools.debfunct import D_3
m = 0.026981500000000002
nu = 0.337
a0, m0 = 0, 1
s0, s1, s2 = 0, 0, 0
edef, sdef = 30,0
p_intanh = a0, m0
p_anh = s0, s1, s2
p_electronic = 3.58624e-01, -1.36715e+04, 5.30710e-04, -7.01007e-06
Tmelting = 933
p_defects = edef, sdef, Tmelting, 0.1

initial_parameters =  [-360773.02,9.92927E-06,77265300000,4.6043778]
eos_MU = potentials.BM()#MU()
eos_MU.fitEOS([9.94288E-06], 0, initial_parameters=initial_parameters, fit=False)
p_EOS = eos_MU.pEOS

ndeb = nDeb(nu, m, p_intanh, eos_MU, p_electronic,
            p_defects, p_anh, mode='')

T = np.arange(0,1020,20)#gen_Ts(0.1, 1000.1, 10)

#P = 0
stp = 1
step=2*stp/6
# V0_DM, a_DM, b_DM = initial_parameters[1], -0.5, 0.5
for P in np.arange(-stp,stp+step,step):
    print('\nPPPPPPPPPP',P)
    P = P*1e9
    T, V = ndeb.min_G(T, p_EOS[1]*.9, P)
    # T, V = ndeb.min_G(T, p_EOS[1]*1.3, P)

    tprops_dict = ndeb.eval_props(T, V, P)

    for i in range(len(T)):
        print( #tprops_dict['T'][i],tprops_dict['a'][i]/1e-5,
                tprops_dict['T'][i],P,tprops_dict['S'][i],tprops_dict['V'][i],tprops_dict['a'][i],
              tprops_dict['dSdP_T'][i], tprops_dict['Kt'][i], tprops_dict['dKtdT_P'][i],
              tprops_dict['Cp'][i], tprops_dict['dadP_T'][i],
              tprops_dict['dCpdP_T'][i], tprops_dict['ddSdT_PdP_T'][i]
              # tprops_dict['Cp'][i],tprops_dict['E0'][i]
              )
print('ok')
