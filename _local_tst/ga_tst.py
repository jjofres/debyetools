import numpy.random as rnd
from debyetools.ndeb import nDeb
import numpy as np
import debyetools.potentials as potentials

def tprops_eval(T, params):
    edef, sdef = params

    p_defects = edef, sdef, Tmelting, 0.1

    ndeb_MU = nDeb(nu, m, p_intanh, eos_obj, p_electronic,
                    p_defects, p_anh, mode='jjsl')
    T, V = ndeb_MU.min_G(T, p_EOS[1], P=0)
    #=========================
    tprops_dict = ndeb_MU.eval_props(T, V, P=0)
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
    eval_val = fc(T, pi)
    return np.sqrt(np.sum(((eval_val - yexp)/eval_val)**2))
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


m = 0.0509415
nu = 0.409
Tmelting = 2183

edef, sdef = 10,1

eos_obj = potentials.MU()
initial_parameters = [-8.680958045e+05, 8.124051364e-06, 1.757221171e+11, 3.712299840e+00]

# eos_obj = potentials.BM()
# initial_parameters = [-8.682582466e+05, 8.117162960e-06, 1.801699496e+11, 3.818903293e+00]
#
# eos_obj = potentials.BM4()
# initial_parameters = [-8.682838818e+05, 8.115328159e-06, 1.810526161e+11, 3.855537799e+00, 2.498535685e-11]


eos_obj.fitEOS([initial_parameters[1]], 0, initial_parameters=initial_parameters, fit=False)
p_EOS = eos_obj.pEOS
p_electronic = [1.52435e+00, -6.79663e+04, 5.30710e-04, -7.01007e-06]
p_intanh = 0, 1
p_anh = 0, 0, 0
T = np.array([63.305,143.885,216.42,294.25,323.815,382.4525,410.58,474.96,509.8475,572.14,615.07,686.2575,732.1925,795.935,850.86,1000,1200,1400,1600,1774.48,1926.88,2067.6225])
C_exp = np.array([8.9525,18.95,22.345,24.55,24.6125,25.125,25.8775,25.8175,26.6125,26.7025,27.1225,27.525,27.315,28.1525,28.4875,30.2375,32.1925,34.4075,36.8225,39.01,40.5375,42.5775])


ix = 0
max_iter = 500
mvar=[(edef,5), (sdef, 1)]
parents_params = mutate(params = [edef, sdef], n_chidren = 2, mrate=0.8, mvar=mvar)

counter_change = 0
errs_old = 1
while ix <= max_iter:
    children_params = mate(parents_params, 20, mvar)
    parents_params, errs_new = select_bests(tprops_eval, T, children_params,2, C_exp)
    edef, sdef = parents_params[0]
    errs_new = np.round(errs_new,5)
    mvar=[(edef,0.5), (sdef, 0.1)]

    if errs_old == errs_new[0]:
        counter_change+=1
    else:
        counter_change=0
    ix+=1
    errs_old = errs_new[0]
    print('iter:',ix,counter_change,errs_old, parents_params)
    if counter_change>=20: break

# T = np.arange(0.1,800.1,20)
# Cp1 = tprops_eval(T, parents_params[0])

best_params = parents_params[0]
print(best_params)
