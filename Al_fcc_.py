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
eos_MU.fitEOS([9.92927E-06], 0, initial_parameters=initial_parameters, fit=False)
p_EOS = eos_MU.pEOS

ndeb = nDeb(nu, m, p_intanh, eos_MU, p_electronic,
p_defects, p_anh)

T = np.arange(0,1020,20)#gen_Ts(0.1, 1000.1, 10)

#P = 0
stp = 1
step=2*stp/6
for P in np.arange(-stp,stp+step,step):
    print('\nPPPPPPPPPP',P)
    P = P*1e9
    T, V = ndeb.min_G(T, p_EOS[1]*1.3, P=P)
    tprops_dict = ndeb.eval_props(T, V, P=P)
    # T = np.array([0.1,100,200,300,400,500,600,700,800,900,1000])
    # V = np.array([1.00321E-05,1.00423E-05,1.00828E-05,1.01352E-05,1.01924E-05,1.02522E-05,1.03142E-05,1.03779E-05,1.04433E-05,1.05102E-05,1.05788E-05])
    #
    # V2plt = []
    # G2plt = []
    # dGdV2plt = []
    #
    # V02plt = []
    # G02plt = []
    # dG0dV2plt = []

    # for Ti, Vi in zip(T, V):
        # V0 = Vi*.99
        # V1 = Vi*1.01
        # Vstep = (V1 - V0)/(21 - 1.)
        #
        # Vs = np.arange(V0, V1+1.5*Vstep, Vstep)
        # Gs = [ndeb.G(Ti, Vii, P=P) for Vii in Vs]
        # dGdVs = [ndeb.dGdV_T(Ti, Vii, P=P) for Vii in Vs]
        #
        # V2plt.append(Vs)
        # G2plt.append(Gs)
        # dGdV2plt.append(dGdVs)
        #
        # V02plt.append(Vi)
        # G02plt.append(ndeb.G(Ti, Vi, P=P))
        # dG0dV2plt.append(ndeb.dGdV_T(Ti, Vi, P=P))


    # fig = plot.fig(r'G',r'V')
    # hola
    # for i in range(len(V)):
    #     fig.add_set(V2plt[i], G2plt[i], label = 'G['+str(i)+']', type='line', lcolor='gray')
    #     # print([V[i]], [G02plt[i]], dG0dV2plt[i])
    #     fig.add_set([V[i]], [G02plt[i]], label = 'Vmin', type='dots', mcolor='blue', mtype = 'x')

    # fig.plot(show=True)
    # print('asddddddddd')
    # print(T, V)
    tprops_dict = ndeb.eval_props(T, V, P=P)

    for i in range(len(T)):
        print(tprops_dict['T'][i],P,tprops_dict['S'][i],tprops_dict['V'][i],tprops_dict['a'][i], tprops_dict['dSdP_T'][i], tprops_dict['Kt'][i], tprops_dict['dKtdT_P'][i]
              #tprops_dict['Cp'][i],tprops_dict['E0'][i]
              )
print('ok')
