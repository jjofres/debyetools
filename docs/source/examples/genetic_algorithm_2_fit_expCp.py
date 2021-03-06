import numpy as np
from debyetools.ndeb import nDeb
import debyetools.potentials as potentials
import numpy.random as rnd

Pressure = 0
EOS_name = 'MU'
eos_MU = getattr(potentials,EOS_name)()
def Cp_LiFePO4(T, params):
    V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef = params
    p_intanh = a0, m0
    p_anh = s0, s1, s2

    # EOS parametrization
    #=========================
    initial_parameters =  [-6.745375544e+05, V0, K0, K0p]
    eos_MU.fitEOS([V0], 0, initial_parameters=initial_parameters, fit=False)
    p_EOS = eos_MU.pEOS
    #=========================

    # Electronic Contributions
    #=========================
    p_electronic = [0,0,0,0]
    #=========================

    # Other Contributions parametrization
    #=========================
    Tmelting = 800
    p_defects = edef, sdef, Tmelting, 0.1
    #=========================

    # F minimization
    #=========================
    m = 0.02253677142857143
    ndeb_MU = nDeb(nu, m, p_intanh, eos_MU, p_electronic,
                    p_defects, p_anh)
    T, V = ndeb_MU.min_G(T, p_EOS[1], P=Pressure)
    #=========================

    # Evaluations
    #=========================
    tprops_dict = ndeb_MU.eval_props(T, V, P=Pressure)
    #=========================

    return tprops_dict['Cp']

def mutate(params, n_chidren, mrate, mvar):
    res = []
    for i in range(n_chidren):
        new_params = []
        for pi, mvars in zip(params, mvar):
            if rnd.randint(0,100)/100.<=mrate:
                step = mvars[1]/10
                lst1 = np.arange(mvars[0]-mvars[1], mvars[0]+mvars[1]+step, step )
                var = lst1[rnd.randint(0,len(lst1))]
                new_params.append(var)
            else:
                new_params.append(pi)

        res.append(new_params)
    return res

def evaluate(fc, T, pi, yexp):
    return np.sqrt(np.sum((fc(T, pi)/T - yexp/T)**2))
    try:
        return np.sqrt(np.sum((fc(T, pi)/T - yexp/T)**2))
    except:
        print('these parameters are not working:',pi)
        return 1

def select_bests(fn, T, params, ngen, yexp):
    arr = []
    for ix, pi in enumerate(params):
        arr.append([ix, evaluate(fn, T, pi, yexp)])

    arr = np.array(arr)
    sorted_arr = arr[np.argsort(arr[:, 1])]
    tops_ix = sorted_arr[:ngen,0]

    return [params[int(j)] for j in tops_ix], [arr[int(j),1] for j in tops_ix]

def mate(params, ngen,mvar):
    res = [params[0],params[1]]
    ns = int(max(2,ngen-2)/2)

    for i in range(ns):
        cutsite = rnd.randint(0,len(params[0]))
        param1 = mutate(params[0][:cutsite]+params[1][cutsite:], 1, 0.5, mvar)[0]
        param2 = mutate(params[1][:cutsite]+params[0][cutsite:], 1, 0.5, mvar)[0]

        res.append(param1)
        res.append(param2)

    return res

V0, K0, K0p = 6.405559904e-06, 1.555283892e+11, 4.095209375e+00
nu = 0.2747222272342077
a0, m0 = 0, 1
s0, s1, s2 = 0, 0, 0
edef, sdef = 20,0
T = np.array([126.9565217,147.826087,167.826087,186.9565217,207.826087,226.9565217,248.6956522,267.826087,288.6956522,306.9565217,326.9565217,349.5652174,366.9565217,391.3043478,408.6956522,428.6956522,449.5652174,467.826087,488.6956522,510.4347826,530.4347826,548.6956522,571.3043478,590.4347826,608.6956522,633.0434783,649.5652174,670.4347826,689.5652174,711.3043478,730.4347826,750.4347826,772.173913])
C_exp = np.array([9.049180328,10.14519906,11.29742389,12.05620609,12.92740047,13.82669789,14.61358314,15.45667447,16.07494145,16.55269321,17.00234192,17.73302108,18.21077283,18.60421546,19.25058548,19.53161593,19.78454333,20.12177986,20.4028103,20.90866511,21.18969555,21.52693208,21.89227166,22.4824356,22.96018735,23.40983607,23.69086651,23.88758782,23.71896956,23.7470726,23.85948478,23.83138173,24.19672131])

ix = 0
max_iter = 100
print('initial err:', evaluate(Cp_LiFePO4,T,[V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef],C_exp))
mvar=[(V0,V0*0.01), (K0,K0*0.05), (K0p,K0p*0.01), (nu,nu*0.01), (a0,5e-6), (m0,5e-3), (s0,5e-5), (s1,5e-5), (s2,5e-5), (edef,0.5), (sdef, 0.1)]
parents_params = mutate(params = [V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef], n_chidren = 2, mrate=0.7, mvar=mvar)
print('parents_params:', parents_params)

while ix <= max_iter:
    children_params = mate(parents_params, 20, mvar)
    parents_params, errs = select_bests(Cp_LiFePO4, T, children_params,2, C_exp)
    V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef = parents_params[0]
    mvar=[(V0,V0*0.05), (K0,K0*0.05), (K0p,K0p*0.05), (nu,nu*0.05), (a0,5e-6), (m0,5e-3), (s0,5e-5), (s1,5e-5), (s2,5e-5), (edef,0.5), (sdef, 0.1)]

    print(ix, errs, parents_params)
    ix+=1

T = np.arange(0.1,800.1,20)
Cp1 = Cp_LiFePO4(T, parents_params[0])

for Ti, Cp1i in zip(T, Cp1):
    print(Ti, Cp1i)

print('best parameters:',parents_params[0])
