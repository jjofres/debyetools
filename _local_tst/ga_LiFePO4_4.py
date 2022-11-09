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


def Cp_LiFePO4(T, params):
    print('>',end='')
    # s0, s1, s2 = params
    V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef = params
    # a0, m0 = params
    p_intanh = a0, m0
    p_anh = s0, s1, s2

    # EOS parametrization
    #=========================
    initial_parameters = [-6.74512999E+05, V0, K0, K0p]
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

    return tprops_dict['Cp'],tprops_dict['Sa']


def mutate(params, n_chidren, mrate, mvar, signs):
    res = []
    for i in range(n_chidren):
        new_params = []
        for pi, mvars, sign in zip(params, mvar, signs):
            if rnd.randint(0, 100)/100. <= mrate:
                step = mvars[0]/10
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
        return np.sqrt(np.sum(((fc(T, pi)[0] - yexp)/yexp)**2))
    except:
        return 1e10


def select_bests(fn, T, params, ngen, yexp):
    arr = []
    for ix, pi in enumerate(params):
        arr.append([ix, evaluate(fn, T, pi, yexp)])
    arr = np.array(arr)
    print(arr)
    sorted_arr = arr[np.argsort(arr[:, 1])]
    print(sorted_arr)
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
    V0, K0, K0p = 7.174584085576401e-06, 149556799431.6083, 4.894525988698603 #5.762390764886918e-06, 89047694703.46004, 3.636987441126467#6.405559904e-06, 155528389200.0, 3.931401
    nu = 0.3785070135864595#0.31888050585132893#0.2747222272342077
    a0, m0 = 0.0017137103573339513, 12.324800843121565#0.0023833244267004285, 9.969819526649578#0.00017496414802500057, -1.463874632286355
    s0, s1, s2 = 0.012801727590107302, -0.5200019440899462, -4551089.60942477#-3.969303090100795e-05, 2034.8571365979824, 10772545.326296955#0.009715033969061806, 8756.571746579899, -1435200717.6
    edef, sdef = 18.400000000000063, 1.7699999999999994#23.27956606428067, 1.6981192643056922#20, 2

    p_electronic = [5.52122e-314, -2.35357e-308, 3.32430e-303, -1.55592e-298]
    Tmelting = 800

    m = 0.02253677142857143

    T = np.array([0.1,40.16838464, 71.62728127,147.5362319,207.2463768,268.4057971,327.8260869,388.9855072,448.6956522,509.8550725,570.1449275,630.4347826,690.4347826,751.0144927])
    C_exp = np.array([0.001, 1.227397939,4.344789455,10.16393443,12.93676815,15.38173302,17.09601874,18.68852459,19.81264637,20.83372365,21.96721311,23.35362998,23.78454333,23.96252927])

    ix = 0
    max_iter = 1
    min_err = 0.15
    max_iter_change = 100
    gen_size = 5

    mvar = [(V0,V0*0.1), (K0,K0*0.1), (K0p,K0p*0.1), (nu,nu*0.1),
            (a0,a0*2), (m0,2*m0),
            (s0,2*s0), (s1,2*s1), (s2,2*s2),
            (edef,0.5), (sdef, 0.05),
            ]
    signs = [0, 0, 0, 0,
             1, 1,
             1, 1, 1,
             0, 0
             ]
    # mvar = [(V0,V0*0.01), (K0,K0*0.01), (K0p,K0p*0.01), (nu,nu*0.1), (a0,a0*0.1), (m0,m0*0.1),(s0,s0*0.1), (s1,s1*0.1), (s2,s2*0.1)]
    # signs = [0,0,0,0,0,0,1,1,1]
    parents_params = mutate(params = [V0, K0, K0p, nu,
                                      a0, m0,
                                      s0, s1, s2,
                                      edef, sdef,
                                      ], n_chidren=2, mrate=0.0, mvar=mvar, signs=signs)


    counter_change = 0
    errs_old = 1


    while ix <= max_iter:
        print('parents_params',parents_params)
        children_params = mate(parents_params, gen_size, mvar, signs)

        parents_params, errs_new = select_bests(Cp_LiFePO4, T, children_params,2, C_exp)
        print(parents_params, errs_new)
        V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef = parents_params[0]
        # s0, s1, s2 = parents_params[0]
        # V0, K0, K0p, nu, edef, sdef = parents_params[0]
        mvar = [(V0, V0 * 0.1), (K0, K0 * 0.1), (K0p, K0p * 0.1), (nu, nu * 0.1),
                (a0, a0*1.9), (m0, m0*1.9),
                (s0, s0*1.9), (s1, s1*1.9), (s2, s2*1.9),
                 (edef, edef*0.1), (sdef, sdef*0.1),
                ]

        if errs_old == np.round(errs_new[0],4):
            counter_change += 1
        else:
            counter_change=0
        ix += 1
        errs_old = np.round(errs_new[0], 4)
        print('iter:', ix, counter_change, errs_old, parents_params)
        if counter_change >= max_iter_change: break
        if errs_old <= min_err: break

    T = np.arange(0.1,800.1,15)

    best_params = parents_params[0]



    T_exp = np.array([126.9565217,147.826087,167.826087,186.9565217,207.826087,226.9565217,248.6956522,267.826087,288.6956522,306.9565217,326.9565217,349.5652174,366.9565217,391.3043478,408.6956522,428.6956522,449.5652174,467.826087,488.6956522,510.4347826,530.4347826,548.6956522,571.3043478,590.4347826,608.6956522,633.0434783,649.5652174,670.4347826,689.5652174,711.3043478,730.4347826,750.4347826,772.173913])
    Cp_exp = np.array([9.049180328,10.14519906,11.29742389,12.05620609,12.92740047,13.82669789,14.61358314,15.45667447,16.07494145,16.55269321,17.00234192,17.73302108,18.21077283,18.60421546,19.25058548,19.53161593,19.78454333,20.12177986,20.4028103,20.90866511,21.18969555,21.52693208,21.89227166,22.4824356,22.96018735,23.40983607,23.69086651,23.88758782,23.71896956,23.7470726,23.85948478,23.83138173,24.19672131])
    T_ph = np.array([1.967263911, 24.08773869, 40.16838464, 51.99817063, 62.61346532, 71.62728127, 82.14182721, 95.16347545, 108.6874128, 123.7174904, 140.2528445, 158.7958422, 179.3467704, 202.4077519, 226.4743683, 250.5441451, 274.6162229, 299.1922033, 323.2681948, 347.8476048, 371.9269543, 396.0073777, 420.0891204, 444.171937, 468.7572464, 492.8416261, 516.9264916, 541.5140562, 565.6001558, 589.6869304, 613.7740731, 638.3634207, 662.4510066, 686.0373117, 711.1294163, 734.2134743, 764.3270346])
    Cp_ph =np.array([-0.375850956, -0.178378686, 1.227397939, 2.313383473, 3.431619848, 4.344789455, 5.478898585, 6.723965937, 7.953256737, 9.166990283, 10.40292814, 11.64187702, 12.87129914, 14.08268875, 15.21632722, 16.2118242, 17.10673273, 17.9153379, 18.63917154, 19.29786266, 19.87491167, 20.4050194, 20.87745642, 21.30295216, 21.70376428, 22.06093438, 22.39686914, 22.69910457, 22.98109412, 23.23357771, 23.46996716, 23.69426517, 23.91128202, 24.1000059, 24.28807125, 24.49073617, 24.58375529])

    T_JJ = np.array([1.00000E-01,1.64245E+01,3.27490E+01,4.90735E+01,6.53980E+01,8.17224E+01,9.80469E+01,1.14371E+02,1.30696E+02,1.47020E+02,1.63345E+02,1.79669E+02,1.95994E+02,2.12318E+02,2.28643E+02,2.44967E+02,2.61292E+02,2.77616E+02,2.93941E+02,2.98150E+02,3.10265E+02,3.26590E+02,3.42914E+02,3.59239E+02,3.75563E+02,3.91888E+02,4.08212E+02,4.24537E+02,4.40861E+02,4.57186E+02,4.73510E+02,4.89835E+02,5.06159E+02,5.22484E+02,5.38808E+02,5.55133E+02,5.71457E+02,5.87782E+02,6.04106E+02,6.20431E+02,6.36755E+02,6.53080E+02,6.69404E+02,6.85729E+02,7.02053E+02,7.18378E+02,7.34702E+02,7.51027E+02,7.67351E+02,7.83676E+02,8.00000E+02])

    parameters_MU = [6.405559904e-06, 1.555283892e+11, 4.095209375e+00, 0.2747222272342077,
                     0, 1,
                     0,0,0,
                     20, 0
                     ]
    Cp_JJ, Sa_JJ = Cp_LiFePO4(T_JJ, parameters_MU)
    Cp_JJ_fitted, Sa_JJ_fitted = Cp_LiFePO4(T_JJ, best_params)


    Cp_JJ_exp = Cp_LiFePO4(T_exp, best_params)[0]
    err = []
    for Ti, Cp, Cpexp in zip(T_exp, Cp_JJ_exp, Cp_exp):
        err.append(((Cp-Cpexp)/Cpexp)**2)

    fig, ax = plt.subplots(3)

    ax[0].plot(T_exp, Cp_exp, label = 'exp', marker='s', linestyle='None', markerfacecolor='None', markeredgecolor='purple')
    ax[0].plot(T_ph, Cp_ph, label = 'phonon', marker='None', linestyle='--', color='cornflowerblue')
    ax[0].plot(T_JJ, Cp_JJ, label = 'Murnaghan', marker='None', linestyle='-', color='C3')
    ax[0].plot(T_JJ, Cp_JJ_fitted, label = 'Murnaghan+fitted '+str(tag)+'ax', marker='None', linestyle='-', color='orchid')

    ax[0].legend()

    ax[1].plot(T_exp,err)

    ax[2].plot(T_JJ,Sa_JJ, label='A(T) Murnaghan')
    ax[2].plot(T_JJ,Sa_JJ_fitted, label='A(T) Murnaghan + fitting')

    print('tag',str(tag)+'ax')



    plt.show()



    end  = time.perf_counter()
    print(end-start)