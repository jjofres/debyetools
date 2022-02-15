

def Cp_Al13Fe4(T, params):
    nu = params[0]
    p_intanh = 0,1
    p_anh = 0,0,0
    #=========================
    initial_parameters =  [-4.952592746e+05, 8.648457421e-06, 1.230588534e+11, 4.270810108e+00]
    eos_BM.fitEOS([V0], 0, initial_parameters=initial_parameters, fit=False)
    p_EOS = eos_BM.pEOS
    #=========================
    p_electronic = [3.00828e-01, -1.26011e+04, 5.30710e-04, -7.01007e-06]
    #=========================
    Tmelting = 1423
    p_defects = edef, sdef, Tmelting, 0.1
    #=========================
    m = 0.033772911764705885
    ndeb_BM = nDeb(nu, m, p_intanh, eos_BM, p_electronic,
                    p_defects, p_anh)
    T, V = ndeb_BM.min_G(T, p_EOS[1], P=0)
    #=========================
    tprops_dict = ndeb_BM.eval_props(T, V, P=0)
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

import numpy as np
import debyetools.potentials as potentials

eos_BM = potentials.BM()
V0, K0, K0p = 8.648457421e-06, 1.230588534e+11, 4.270810108e+00
nu = 0.1
a0, m0 = 0, 1
s0, s1, s2 = 0, 0, 0
edef, sdef = 30,0
T = np.array([321.1395695,350.9213645,380.7031595,410.4849545,440.2667495,470.0485445,499.8303395,529.6121345,559.3939295,589.1757245,618.9575195,648.7393145,678.5211095,708.3029045,738.0846995,767.8664945,797.6482895,827.4300845,857.2118795,886.9936745,916.7754695,946.5572645,976.3390595,1006.120855,1035.90265,1065.684445,1095.46624,1125.248035,1155.02983,1184.811625,1214.59342,1244.375215,1271.866102])
C_exp = np.array([25.03690425,25.83524651,26.63464199,27.36557804,28.03858688,28.64945562,29.2139826,29.73427426,30.2061177,30.64952416,31.05817428,31.43733419,31.79964255,32.13878003,32.47370462,32.7938841,33.11406358,33.43845595,33.76495476,34.10830512,34.47271993,34.85187984,35.25631708,35.69445742,36.17367342,36.69291185,37.25322594,37.87146724,38.53920998,39.27119925,40.06743506,40.9321303,41.78562309])

import numpy.random as rnd
from debyetools.ndeb import nDeb
ix = 0
max_iter = 500
print('initial err:', evaluate(Cp_Al13Fe4,T,[nu],C_exp))
mvar=[(nu,nu*0.01)]
parents_params = mutate(params = [nu], n_chidren = 2, mrate=0.7, mvar=mvar)
print('parents_params:', parents_params)

counter_change = 0
errs_old = 1
while ix <= max_iter:
    children_params = mate(parents_params, 10, mvar)
    parents_params, errs_new = select_bests(Cp_Al13Fe4, T, children_params,2, C_exp)
    nu,= parents_params[0]
    mvar=[(nu,nu*0.05)]

    if errs_old == errs_new[0]:
        counter_change+=1
    else:
        counter_change=0
    print(ix, counter_change, errs_new, parents_params, )
    ix+=1
    errs_old = errs_new[0]
    if counter_change>=10: break

T = np.arange(0.1,1500.1,20)
Cp1 = Cp_Al13Fe4(T, parents_params[0])

for Ti, Cp1i in zip(T, Cp1):
    print(Ti, Cp1i)

print('best parameters:',parents_params[0])
