from debyetools.ndeb import nDeb
import numpy as np
import debyetools.potentials as potentials
from debyetools.aux_functions import gen_Ts
import debyetools.tpropsgui.plotter as plot

from debyetools.debfunct import D_3
m = 0.02922135#0.026981500000000002
nu = 0.244
a0, m0 = 0, 1
s0, s1, s2 = 0, 0, 0
edef, sdef = 30,0
p_intanh = a0, m0
p_anh = s0, s1, s2
p_electronic = 0,0,0,0
Tmelting = 1000
p_defects = edef, sdef, Tmelting, 0.1

initial_parameters =  [-326886.10,1.3944E-05,22910900000,4.4550105]#<-MU [-3.269309968e+05, 1.388820583e-05, 2.372651633e+10, 4.611094858e+00]#<-BM
eos_MU = potentials.MU()
eos_MU.fitEOS([1.3944E-05], 0, initial_parameters=initial_parameters, fit=False)
p_EOS = eos_MU.pEOS

ndeb = nDeb(nu, m, p_intanh, eos_MU, p_electronic,
p_defects, p_anh)

# T = np.arange(0,3060,60)#gen_Ts(0.1, 1000.1, 10)

P = 0
B0_DM, V0_DM, a_DM, b_DM = initial_parameters[2], initial_parameters[1], -0.5, 0.5
T = gen_Ts(0.1, 1000.1, 10)
T, V = ndeb.min_G(T, p_EOS[1], P, V0_DM, a_DM, b_DM)
T, V = ndeb.min_G(T, p_EOS[1], P, V[0], a_DM, b_DM)
# T = np.array([0,20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,320,340,360,380,400,420,440,460,480,500,520,540,560,580,600,620,640,660,680,700,720,740,760,780,800,820,840,860,880,900,920,940,960,980,1000])
# V = np.array([1.41555E-05,1.41557E-05,1.41593E-05,1.41701E-05,1.41885E-05,1.42127E-05,1.42411E-05,1.42724E-05,1.43059E-05,1.43411E-05,1.43776E-05,1.44153E-05,1.44539E-05,1.44934E-05,1.45336E-05,1.45745E-05,1.46161E-05,1.46583E-05,1.47011E-05,1.47445E-05,1.47885E-05,1.4833E-05,1.48781E-05,1.49237E-05,1.49698E-05,1.50165E-05,1.50638E-05,1.51116E-05,1.516E-05,1.52089E-05,1.52584E-05,1.53084E-05,1.53591E-05,1.54103E-05,1.54621E-05,1.55145E-05,1.55676E-05,1.56212E-05,1.56755E-05,1.57305E-05,1.57861E-05,1.58423E-05,1.58993E-05,1.59569E-05,1.60153E-05,1.60743E-05,1.61341E-05,1.61947E-05,1.6256E-05,1.63181E-05,1.63809E-05])
tprops_dict = ndeb.eval_props(T, V, P, V[0], a_DM, b_DM)

for i in range(len(T)):
    print(tprops_dict['T'][i], tprops_dict['a'][i]/1e-5
          )
print('ok')
