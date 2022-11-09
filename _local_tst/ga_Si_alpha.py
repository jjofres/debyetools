import numpy as np
import debyetools.potentials as potentials
import numpy.random as rnd
from debyetools.ndeb import nDeb
import time
# import debyetools.tpropsgui.plotter as plot
from matplotlib import pyplot as plt


start = time.perf_counter()
tag = rnd.randint(0,100)
print('tag',str(tag)+'ax')


def a_Si(T, params):
    print('>',end='')
    V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef = params
    p_intanh = a0, m0
    p_anh = s0, s1, s2

    # EOS parametrization
    #=========================
    initial_parameters = [E0, V0, K0, K0p]
    eos_MU.fitEOS([V0], 0, initial_parameters=initial_parameters, fit=False)
    p_EOS = eos_MU.pEOS
    #=========================

    # Electronic Contributions
    #=========================
    #=========================

    # Other Contributions parametrization
    #=========================
    p_defects = edef, np.sqrt(sdef**2), Tmelting, 0.1
    #=========================

    # F minimization
    #=========================
    ndeb_MU = nDeb(nu, m, p_intanh, eos_MU, p_electronic,p_defects, p_anh, mode='jjsl')
    T, V = ndeb_MU.min_G(T, p_EOS[1], P=0)
    #=========================

    # Evaluations
    #=========================
    tprops_dict = ndeb_MU.eval_props(T, V, P=0)
    #=========================

    return tprops_dict['a'],tprops_dict['Cp'],tprops_dict['Sa'],tprops_dict['Fel'],tprops_dict['Fdef'],tprops_dict['tD']


def mutate(params, n_chidren, mrate, mvar, signs):
    res = []
    for i in range(n_chidren):
        new_params = []
        for pi, mvars, sign in zip(params, mvar, signs):
            if rnd.randint(0, 100)/100. <= mrate:
                step = (2*mvars[1])/30
                lst1 = np.arange(mvars[0]-mvars[1], mvars[0]+mvars[1]+step, step)
                sig = [-1, 1][rnd.randint(0, 2)] if sign == 1 else 1
                var = lst1[rnd.randint(0, len(lst1))]*sig
                new_params.append(var)
            else:
                new_params.append(pi)

        res.append(new_params)
    return res


def evaluate(fc, T, pi, yexp):
    try:
        errtotal = np.sqrt(np.sum(((fc(T, pi)[0] - yexp) / yexp) ** 2))/len(T)
        return errtotal
    except:
        return 1e10


def select_bests(fn, T, params, ngen, yexp):
    # for ix, pi in enumerate(params):
    #     arr.append([ix, evaluate(fn, T, pi, yexp)])
    len_p = len(params)
    Ts = [T]*len_p
    yexps = [yexp]*len_p
    funcs = [fn]*len_p
    evaluations  = list(map(evaluate, funcs, Ts, params, yexps))
    arr =  list(enumerate(evaluations))

    arr = np.array(arr)
    sorted_arr = arr[np.argsort(arr[:, 1])]
    tops_ix = sorted_arr[:ngen,0]

    return [params[int(j)] for j in tops_ix], [arr[int(j),1] for j in tops_ix]

def mate(params, ngen,mvar, signs):
    res = [params[0],params[1]]
    ns = int(max(2,ngen-2)/2)

    for i in range(ns):
        cutsite = rnd.randint(0,len(params[0]))
        param1 = mutate(params[0][:cutsite]+params[1][cutsite:], 1, 0.8, mvar, signs)[0]
        param2 = mutate(params[1][:cutsite]+params[0][cutsite:], 1, 0.9, mvar, signs)[0]

        res.append(param1)
        res.append(param2)

    res.append(params[0])
    res.append(params[1])

    return res

if __name__ == '__main__':
    print('start')
    eos_MU = potentials.MU()
    E0, V0, K0, K0p = -5.349925844e+05, 1.232361446e-05, 9.863512037e+10, 4.109477393e+00
    nu = 0.204
    a0, m0 = -1e-05, -1
    s0, s1, s2 = 0.001, 100, 20000.0
    edef, sdef = 20, 0

    p_electronic = [0, 0, 0, 0]
    Tmelting = 1600

    m = 0.0280855

    T = np.array([38.00904977,97.8381096,148.8687783,205.5304173,270.2865762,338.9140272,399.0950226,458.2202112,511.0105581,563.800905,618.7028658,673.6048265,726.3951735,802.413273,859.4268477,920.6636501,979.7888386,1057.918552,1133.936652,1201.508296,1260.633484,1326.093514,1374.660633,1444.343891,1507.692308])
    a_exp = np.array([-0.153508116,-0.251420164,0.47133192,1.507877102,2.287255466,2.819052816,3.126692003,3.37029221,3.562636121,3.70375271,3.806458467,3.921971054,3.999053492,4.101855831,4.140537095,4.217658166,4.269155918,4.333547424,4.372315612,4.398238336,4.462542919,4.514069646,4.501484955,4.565837828,4.617354897])*1e-5
    T_exp_1 = np.array(
        [19.00452489, 40.12066365, 54.90196078, 78.12971342, 99.24585219, 116.1387632, 128.8084465, 143.5897436,
         154.147813, 168.9291101, 185.8220211, 202.7149321, 228.0542986, 253.3936652, 287.1794872, 320.9653092,
         356.8627451, 399.0950226, 458.2202112, 511.0105581, 563.800905, 618.7028658, 673.6048265, 726.3951735,
         802.413273, 859.4268477, 920.6636501, 979.7888386, 1057.918552, 1133.936652, 1201.508296, 1260.633484,
         1326.093514, 1374.660633, 1444.343891, 1507.692308])
    a_exp_1 = np.array([0.012893754,-0.140691627,-0.332726474,-0.371040724,-0.268489499,-0.114730269,0.090236965,0.359248009,0.551398755,0.884443951,1.191885144,1.512133168,1.819612994,2.139899651,2.43461128,2.703709248,2.934396384,3.126692003,3.37029221,3.562636121,3.70375271,3.806458467,3.921971054,3.999053492,4.101855831,4.140537095,4.217658166,4.269155918,4.333547424,4.372315612,4.398238336,4.462542919,4.514069646,4.501484955,4.565837828,4.617354897])*1e-5

    ix = 0
    max_iter = 1
    min_err = 0.001
    max_iter_change = 100
    gen_size = 1

    mvar = [  (V0,V0*0.01), (K0,K0*0.01), (K0p,K0p*0.01), (nu,nu*0.1),
        (a0, 1e-6), (m0, 0.5),
        (s0, 0.001), (s1, 100), (s2, 10000),
        (edef, 0.5), (sdef, 0.1),
    ]
    signs = [  0, 0, 0, 0,
        0, 0,
        0, 0, 0,
        0, 0
    ]
    parents_params = mutate(params=[   V0, K0, K0p, nu,
        a0, m0,
        s0, s1, s2,
        edef, sdef,
    ], n_chidren=2, mrate=0.0, mvar=mvar, signs=signs)

    counter_change = 0
    errs_old = 1

    while ix <= max_iter:
        # print('parents_params',parents_params)
        children_params = mate(parents_params, gen_size, mvar, signs)

        parents_params, errs_new = select_bests(a_Si, T, children_params, 2, a_exp)
        V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef = parents_params[0]
        # a0, m0, s0, s1, s2, edef, sdef = parents_params[0]
        mvar = [(V0, V0 * 0.01), (K0, K0 * 0.01), (K0p, K0p * 0.01), (nu, nu * 0.1),
                (a0, 1e-6), (m0, 0.5),
                (s0, 0.001), (s1, 100), (s2, 10000),
                (edef, 0.5), (sdef, 0.1),
                ]

        if errs_old == np.round(errs_new[0], 4):
            counter_change += 1
        else:
            counter_change = 0
        ix += 1
        errs_old = np.round(errs_new[0], 4)
        print('iter:', ix, counter_change, errs_old, parents_params)
        if counter_change >= max_iter_change: break
        if errs_old <= min_err: break

    best_params = parents_params[0]
    best_params = [1.0339277339848946e-05, 206950022124.48837, 9.217316139291954, 0.003417465384860933, -3.5333333333337334e-05, -24.166666666664405, -0.010933333333333697, -3120.000000000022, 39333.33333333319, 24.733333333337647, -0.6066666666666783]
    print(best_params)

    T_exp_cp1 = np.array([2.5, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300])
    Cp_exp_cp1 = np.array([-0.000113386, -0.000916296, 0.00771948, 0.0305432, 0.0947676, 0.23857168, 0.4807416, 0.8209008, 1.2372088, 2.2058048, 3.23214, 4.263496, 5.276024, 6.284368, 7.275976, 9.22572, 11.0876, 12.790488, 14.30928, 15.62724, 16.773656, 17.765264, 18.63972, 19.405392, 20.066464])
    T_exp_cp2 = np.array([298.15, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1687])
    Cp_exp_cp2 = np.array([20.007, 20.066, 21.324, 22.258, 23, 23.588, 24.047, 24.42, 24.748, 25.05, 25.334, 25.608, 25.865, 26.11, 26.344, 26.569, 26.988, 27.36, 27.707, 28.045, 28.372, 28.674, 28.93])

    T_JJ = np.array([1.00E-01,1.73E+01,3.44E+01,5.16E+01,6.88E+01,8.60E+01,1.03E+02,1.20E+02,1.37E+02,1.55E+02,1.72E+02,1.89E+02,2.06E+02,2.23E+02,2.40E+02,2.58E+02,2.75E+02,2.92E+02,2.98E+02,3.09E+02,3.26E+02,3.44E+02,3.61E+02,3.78E+02,3.95E+02,4.12E+02,4.29E+02,4.47E+02,4.64E+02,4.81E+02,4.98E+02,5.15E+02,5.32E+02,5.50E+02,5.67E+02,5.84E+02,6.01E+02,6.18E+02,6.35E+02,6.53E+02,6.70E+02,6.87E+02,7.04E+02,7.21E+02,7.38E+02,7.56E+02,7.73E+02,7.90E+02,8.07E+02,8.24E+02,8.41E+02,8.59E+02,8.76E+02,8.93E+02,9.10E+02,9.27E+02,9.44E+02,9.62E+02,9.79E+02,9.96E+02,1.01E+03,1.03E+03,1.05E+03,1.06E+03,1.08E+03,1.10E+03,1.12E+03,1.13E+03,1.15E+03,1.17E+03,1.18E+03,1.20E+03,1.22E+03,1.24E+03,1.25E+03,1.27E+03,1.29E+03,1.31E+03,1.32E+03,1.34E+03,1.36E+03,1.37E+03,1.39E+03,1.41E+03,1.43E+03,1.44E+03,1.46E+03,1.48E+03,1.49E+03,1.51E+03,1.53E+03,1.55E+03,1.56E+03,1.58E+03,1.60E+03,1.61E+03,1.63E+03,1.65E+03,1.67E+03,1.68E+03,1.70E+03])

    parameters_MU = [1.232361446e-05, 9.863512037e+10, 4.109477393e+00, 0.204,
                     0, 1,
                     0,0,0,
                     200, 0
                     ]
    a_JJ, Cp_JJ, Sa_JJ, Fel_JJ, Fdef_JJ, tD_JJ = a_Si(T_JJ, parameters_MU)
    a_JJ_fitted, Cp_JJ_fitted, Sa_JJ_fitted, Fel_JJ_fitted, Fdef_JJ_fitted, tD_JJ_fitted = a_Si(T_JJ, best_params)
    best_paramsCp = [1.232361446e-05, 9.863512037e+10, 4.109477393e+00, 0.204,
                     -9.099999999999985e-05, -8.09999999999998,
                     0.022333333333333344, -1733.3333333333362, 200000.0,
                     200, 0
                     ]
    a_JJ_fittedCp, Cp_JJ_fittedCp, Sa_JJ_fittedCp, Fel_JJ_fittedCp, Fdef_JJ_fittedCp, tD_JJ_fittedCp = a_Si(T_JJ, best_paramsCp)
    fig = plt.figure(figsize=(6,13))
    gs = fig.add_gridspec(6, hspace=0, right=0.99, top=.99, bottom=.05, left=0.12)
    ax = gs.subplots(sharex=True)
    ax[0].set_title(r'$\alpha(T)$', y=0.6)
    ax[0].plot(T, a_exp/1e-5, label = 'Glazov2001', marker='s', linestyle='None', markerfacecolor='None', markeredgecolor='purple')
    ax[0].plot(T_JJ, a_JJ/1e-5, label = 'Murnaghan', marker='None', linestyle='-', color='orchid')
    ax[0].plot(T_JJ, a_JJ_fitted/1e-5, label = r'Murnaghan+fitted ($\alpha$)', marker='None', linestyle='-', color='C3')
    ax[0].plot(T_JJ, a_JJ_fittedCp/1e-5, label = r'Murnaghan+fitted ($C_P$)', marker='None', linestyle='-', color='darkviolet')
    ax[0].legend(loc='lower right')

    ax[1].set_title(r'$C_{P}(T)$', y=0.8)
    ax[1].plot(T_exp_cp1, Cp_exp_cp1, label='Flubacher1959', marker='s', linestyle='None', markerfacecolor='None',
               markeredgecolor='purple')
    ax[1].plot(T_exp_cp2, Cp_exp_cp2, label='Desai1986', marker='s', linestyle='None', markerfacecolor='None',
               markeredgecolor='cornflowerblue')
    ax[1].plot(T_JJ, Cp_JJ, label='Murnaghan', marker='None', linestyle='-', color='orchid')
    ax[1].plot(T_JJ, Cp_JJ_fitted, label=r'Murnaghan+fitted ($\alpha$)', marker='None', linestyle='-', color='C3')
    ax[1].plot(T_JJ, Cp_JJ_fittedCp, label=r'Murnaghan+fitted ($C_P$) ', marker='None', linestyle='-', color='darkviolet')
    ax[1].legend(loc='center right')

    ax[2].set_title(r'$A(V)\cdot T$', y=0.7)
    ax[2].plot(T_JJ,Sa_JJ, label='Murnaghan', color='orchid')
    ax[2].plot(T_JJ,Sa_JJ_fitted, label=r'Murnaghan + fitting ($\alpha$)', color='C3')
    ax[2].plot(T_JJ,Sa_JJ_fittedCp, label=r'Murnaghan + fitting ($C_P$)', color='darkviolet')

    ax[2].legend(loc='lower left')

    ax[3].set_title(r'$F_{el}(T)$', y=0.7)
    ax[3].plot(T_JJ,Fel_JJ/1e-6, label='Murnaghan', color='orchid')
    ax[3].plot(T_JJ,Fel_JJ_fitted/1e-6, label=r'Murnaghan + fitting ($\alpha$)', color='C3')
    ax[3].plot(T_JJ,Fel_JJ_fittedCp/1e-6, label=r'Murnaghan + fitting ($C_P$)', color='C3')
    ax[3].legend(loc='lower right')

    ax[4].set_title(r'$F_{def}(T)$', y=0.7)
    ax[4].plot(T_JJ,Fdef_JJ/1e-6, label='Murnaghan', color='orchid')
    ax[4].plot(T_JJ,Fdef_JJ_fitted/1e-6, label=r'Murnaghan + fitting ($\alpha$)', color='C3')
    ax[4].plot(T_JJ,Fdef_JJ_fittedCp/1e-6, label=r'Murnaghan + fitting ($C_P)', color='darkviolet')
    ax[4].legend(loc='lower left')

    ax[5].set_title(r'$\theta_D(T)$',y=0.7)
    ax[5].plot(T_JJ, tD_JJ, label='Murnaghan', color='orchid')
    ax[5].plot(T_JJ, tD_JJ_fitted, label=r'Murnaghan + fitting ($\alpha$)', color='C3')
    ax[5].plot(T_JJ, tD_JJ_fittedCp, label=r'Murnaghan + fitting ($C_P)', color='darkviolet')
    ax[5].legend(loc='center left')

    print('tag',str(tag)+'ax')

    ax[0].set_ylabel('$[10^{-5}/K]$')
    ax[1].set_ylabel('$[J/K\cdot mol-at]$')
    ax[2].set_ylabel('$[J/K\cdot mol-at]$')
    ax[3].set_ylabel('$[10^{-6}J/mol-at]$')
    ax[4].set_ylabel('$[10^{-6}J/mol-at]$')
    ax[5].set_ylabel('$[K]$')
    ax[5].set_xlabel('Temperature $[K]$')

    ax[3].set_ylim((-4.1,4.1))
    ax[4].set_ylim((-4.1, 4.1))
    plt.show()



    end  = time.perf_counter()
    print(end-start)