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

def Cp_LiFePO4(T, params,eval=''):
    print('>',end='')
    V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef = params
    p_intanh = a0, m0
    p_anh =  s0, s1, s2

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

    if eval=='min':
        tprops_dict = ndeb_MU.eval_Cp(T, V, P=0)
        return [tprops_dict['Cp']]
    else:
        tprops_dict = ndeb_MU.eval_props(T, V, P=0)
        return tprops_dict['Cp'], tprops_dict['Sa'], tprops_dict['Fel'], tprops_dict['Fdef'], tprops_dict['tD'], \
               tprops_dict['a'], tprops_dict['Kt'], tprops_dict['G'], tprops_dict['V'], tprops_dict['dSdP_T'], \
               tprops_dict['dadP_T'], tprops_dict['dKtdT_P']

def mutate(params, n_chidren, mrate, mvar, signs):
    res = []
    for i in range(n_chidren):
        new_params = []
        for pi, mvars, sign in zip(params, mvar, signs):
            if rnd.randint(0, 100) / 100. <= mrate:
                step = (2 * mvars[1]) / 30
                lst1 = np.arange(mvars[0] - mvars[1], mvars[0] + mvars[1] + step, step)
                sig = [-1, 1][rnd.randint(0, 2)] if sign == 1 else 1
                var = lst1[rnd.randint(0, len(lst1))] * sig
                new_params.append(var)
            else:
                new_params.append(pi)

        res.append(new_params)
    return res

def evaluate(fc, T, pi, yexp):
    evalfunc = fc(T, pi, eval='min')
    try:
        # if evalfunc[5][-1]<max(evalfunc[5]):return 1e10
        errtotal = np.sqrt(np.sum(((evalfunc[0] - yexp) / yexp) ** 2)) / len(T)

        return errtotal
    except:
        return 1e10

def select_bests(fn, T, params, ngen, yexp):
    len_p = len(params)
    Ts = [T] * len_p
    yexps = [yexp] * len_p
    funcs = [fn] * len_p
    evaluations = list(map(evaluate, funcs, Ts, params, yexps))
    arr = list(enumerate(evaluations))
    print(arr)

    arr = np.array(arr)
    sorted_arr = arr[np.argsort(arr[:, 1])]
    tops_ix = sorted_arr[:ngen, 0]

    return [params[int(j)] for j in tops_ix], [arr[int(j), 1] for j in tops_ix]

def mate(params, ngen,mvar, signs):
    res = [params[0],params[1]]
    ns = int(max(2,ngen-2)/2)

    for i in range(ns):
        cutsite = rnd.randint(0,len(params[0]))
        param1 = mutate(params[0][:cutsite]+params[1][cutsite:], 1, 0, mvar, signs)[0]
        param2 = mutate(params[1][:cutsite]+params[0][cutsite:], 1, 0, mvar, signs)[0]

        res.append(param1)
        res.append(param2)

    res.append(params[0])
    res.append(params[1])

    # print(np.array(res).T)
    return res


if __name__ == '__main__':
    print('start')
    eos_MU = potentials.MU()
    E0, V0, K0, K0p = -6.74512999E+05, 6.743261221165651e-06, 155029291717.2258, 3.8364351987698138
    nu = 0.32354891851851836
    a0, m0 = 0.0011, -3.8581341764549872
    s0, s1, s2 = 0.013001727590107095, -140.5200019440813, -4204422.942757982
    edef, sdef = 19.733333333334055, 0.9433333333333649

    p_electronic = [5.52122e-314, -2.35357e-308, 3.32430e-303, -1.55592e-298]
    Tmelting = 800

    m = 0.02253677142857143

    T = np.array([0.1, 71.62728127,147.5362319,207.2463768,268.4057971,327.8260869,388.9855072,448.6956522,509.8550725,570.1449275,630.4347826,690.4347826,751.0144927])
    C_exp = np.array([0.001,4.344789455,10.16393443,12.93676815,15.38173302,17.09601874,18.68852459,19.81264637,20.83372365,21.96721311,23.35362998,23.78454333,23.96252927])

    ix = 0
    max_iter = 1
    min_err = 0.03
    max_iter_change = 20
    gen_size = 1

    mvar = [(V0, V0 * 0.01), (K0, K0 * 0.01), (K0p, K0p * 0.01), (nu, nu * 0.1),
            (a0, 1e-3), (m0, 1),
            (s0, 1e-2), (s1, 1e3), (s2, 1e6),
            (edef, 1), (sdef, 0.5),
            ]
    signs = [0, 0, 0, 0,
             0, 0,
             0, 0, 0,
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
        mvar = [(V0, V0 * 0.01), (K0, K0 * 0.01), (K0p, K0p * 0.01), (nu, nu * 0.1),
                (a0, 1e-3), (m0, 1),
                (s0, 1e-2), (s1, 1e3), (s2, 1e6),
                (edef, 1), (sdef, 0.5),
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

    #T = np.arange(0.1,800.1,15)

    best_params = parents_params[0]



    T_exp = np.array([126.9565217,147.826087,167.826087,186.9565217,207.826087,226.9565217,248.6956522,267.826087,288.6956522,306.9565217,326.9565217,349.5652174,366.9565217,391.3043478,408.6956522,428.6956522,449.5652174,467.826087,488.6956522,510.4347826,530.4347826,548.6956522,571.3043478,590.4347826,608.6956522,633.0434783,649.5652174,670.4347826,689.5652174,711.3043478,730.4347826,750.4347826,772.173913])
    Cp_exp = np.array([9.049180328,10.14519906,11.29742389,12.05620609,12.92740047,13.82669789,14.61358314,15.45667447,16.07494145,16.55269321,17.00234192,17.73302108,18.21077283,18.60421546,19.25058548,19.53161593,19.78454333,20.12177986,20.4028103,20.90866511,21.18969555,21.52693208,21.89227166,22.4824356,22.96018735,23.40983607,23.69086651,23.88758782,23.71896956,23.7470726,23.85948478,23.83138173,24.19672131])
    T_exp22 = np.array([2.03,2.2,2.38,2.58,2.8,3.04,3.29,3.56,3.86,4.19,4.54,4.92,5.33,5.78,6.26,6.78,7.35,7.97,8.64,9.36,10.14,10.23,10.75,11.26,11.77,12.28,12.8,13.31,13.83,14.34,14.85,15.36,15.88,16.39,16.9,17.41,17.93,18.44,18.95,19.47,19.9752,20.49,21.0062,21.51,22.03,22.54,23.05,23.56,24.08,24.59,25.1,25.61,26.13,26.64,27.15,27.67,28.18,28.69,29.2,29.71,30.22,30.73,31.24,31.76,32.27,32.78,33.29,33.8,34.31,34.82,35.34,35.85,37.02,38.89,40.75,42.62,44.48,45.5,45.72,45.92,46.14,46.34,46.55,46.75,46.97,47.16,47.38,47.58,47.8,47.99,48.2,48.4,48.62,48.82,49.03,49.22,49.44,49.64,49.85,50.05,50.27,50.47,50.69,50.89,51.08,51.29,51.5,51.7,51.9,52.12,52.32,52.53,52.72,52.94,53.14,53.35,53.55,53.77,53.96,54.18,54.38,54.59,54.79,55,55.2,55.41,55.62,56.61,57.71,58.79,59.89,60.97,62.06,63.15,64.24,65.33,66.42,67.51,68.59,69.68,70.77,71.15,73.24,75.34,77.43,79.53,81.62,83.72,85.81,87.9,90,92.09,94.19,96.28,98.38,100.47,102.56,104.65,106.73,108.85,110.94,113.02,115.13,117.22,119.27,119.96,120.69,121.4,122.12,122.83,123.54,124.25,124.96,125.68,126.36,127.07,127.81,131.36,141.32,151.46,161.54,171.6,181.68,191.78,201.84,211.78,222.01,232.1,242.04,252.15,262.34,272.43,282.56,292.55,302.7,293.2,313.2,333.2,353.2,284.9,294.8,304.6,314.5,324.4,334.4,344.3,354.2,364.1,374,383.9,393.8,403.8,413.7,423.6,433.5,443.4,453.3,463.3,473.2,483.1,493,502.9,512.8,522.7,532.6,542.5,552.4,562.3,572.3,582.2,592.1,602,611.9,621.8,631.7,641.6,651.6,661.5,671.8,681.3,691.3,701.2,711.1,721,730.9,740.8,750.8,760.7,770.6])
    Cp_exp22 = np.array([0.0162,0.0187,0.0224,0.0243,0.0271,0.0309,0.0325,0.0401,0.048,0.0562,0.059,0.0709,0.0742,0.0903,0.101,0.12,0.138,0.173,0.22,0.276,0.364,0.46,0.535,0.615,0.706,0.808,0.917,1.038,1.171,1.314,1.467,1.631,1.797,1.977,2.169,2.363,2.571,2.79,3.015,3.249,3.484,3.75,3.99,4.26,4.55,4.83,5.13,5.43,5.74,6.06,6.4,6.75,7.09,7.45,7.84,8.22,8.63,9.04,9.47,9.92,10.36,10.82,11.31,11.78,12.28,12.78,13.28,13.81,14.35,14.9,15.46,16.03,17.18,19.19,21.8,24.74,28.1,30.18,30.67,31.15,31.65,32.17,32.68,33.24,33.77,34.33,34.9,35.53,36.14,36.79,37.43,38.11,38.7,39.3,39.72,40.03,39.73,38.83,36.64,33.84,30.69,28.52,26.66,25.59,24.86,24.3,23.89,23.58,23.36,23.13,22.99,22.88,22.83,22.74,22.69,22.66,22.66,22.66,22.66,22.69,22.68,22.73,22.77,22.82,22.85,22.91,22.95,23.28,23.69,24.17,24.67,25.19,25.78,26.36,26.97,27.59,28.2,28.84,29.48,30.12,30.78,31.26,32.53,33.86,35.17,36.46,37.8,39.15,40.41,41.69,42.91,44.24,45.59,46.89,48.18,49.44,50.67,52.08,53.17,54.37,55.54,56.62,58.05,59.3,60.39,60.87,61.12,61.55,61.93,62.24,62.63,63.1,63.45,63.84,64.12,64.49,64.96,66.82,71.82,76.8,81.23,85.36,89.21,93.16,97.49,100.3,103.27,105.66,108.22,110.6,112.67,114.97,117.79,120.06,120.5,120.85,125.4,128,130.1,120.8,122.5,126.1,128.2,129.7,132.2,134.8,136.3,137.9,140.2,142.9,145.5,147,148.9,150.3,151.6,152.8,154,155,156.3,157.5,159,160,161,162.2,163.4,165,166.2,167.1,168.3,169.6,170.4,171.1,173,173.6,174.2,174.9,175.7,176.8,177.4,178,178.7,179.4,180.6,181.6,182.4,183.5,184.5,185.7,186.9])
    T_ph = np.array([1.967263911, 24.08773869, 40.16838464, 51.99817063, 62.61346532, 71.62728127, 82.14182721, 95.16347545, 108.6874128, 123.7174904, 140.2528445, 158.7958422, 179.3467704, 202.4077519, 226.4743683, 250.5441451, 274.6162229, 299.1922033, 323.2681948, 347.8476048, 371.9269543, 396.0073777, 420.0891204, 444.171937, 468.7572464, 492.8416261, 516.9264916, 541.5140562, 565.6001558, 589.6869304, 613.7740731, 638.3634207, 662.4510066, 686.0373117, 711.1294163, 734.2134743, 764.3270346])
    Cp_ph =np.array([-0.375850956, -0.178378686, 1.227397939, 2.313383473, 3.431619848, 4.344789455, 5.478898585, 6.723965937, 7.953256737, 9.166990283, 10.40292814, 11.64187702, 12.87129914, 14.08268875, 15.21632722, 16.2118242, 17.10673273, 17.9153379, 18.63917154, 19.29786266, 19.87491167, 20.4050194, 20.87745642, 21.30295216, 21.70376428, 22.06093438, 22.39686914, 22.69910457, 22.98109412, 23.23357771, 23.46996716, 23.69426517, 23.91128202, 24.1000059, 24.28807125, 24.49073617, 24.58375529])

    T_JJ = np.array([1.00000E-01,1.64245E+01,3.27490E+01,4.90735E+01,6.53980E+01,8.17224E+01,9.80469E+01,1.14371E+02,1.30696E+02,1.47020E+02,1.63345E+02,1.79669E+02,1.95994E+02,2.12318E+02,2.28643E+02,2.44967E+02,2.61292E+02,2.77616E+02,2.93941E+02,2.98150E+02,3.10265E+02,3.26590E+02,3.42914E+02,3.59239E+02,3.75563E+02,3.91888E+02,4.08212E+02,4.24537E+02,4.40861E+02,4.57186E+02,4.73510E+02,4.89835E+02,5.06159E+02,5.22484E+02,5.38808E+02,5.55133E+02,5.71457E+02,5.87782E+02,6.04106E+02,6.20431E+02,6.36755E+02,6.53080E+02,6.69404E+02,6.85729E+02,7.02053E+02,7.18378E+02,7.34702E+02,7.51027E+02,7.67351E+02,7.83676E+02,8.00000E+02])

    parameters_MU = [6.405559904e-06, 1.555283892e+11, 4.095209375e+00, 0.2747222272342077,
                     0, 1,
                     0,0,0,
                     200, 0
                     ]
    print('best params:',best_params)
    Cp_JJ, Sa_JJ, Fel_JJ, Fdef_JJ, tD_JJ, \
    a_JJ, Kt_JJ, G_JJ, V_JJ, \
    dSdP_T_JJ, dadP_T_JJ, dKtdT_P_JJ = Cp_LiFePO4(T_JJ, parameters_MU)

    Cp_JJ_fitted, Sa_JJ_fitted, Fel_JJ_fitted, Fdef_JJ_fitted, tD_JJ_fitted, \
    a_JJ_fitted, Kt_JJ_fitted, G_JJ_fitted, V_JJ_fitted, \
    dSdP_T_JJ_fitted, dadP_T_JJ_fitted, dKtdT_P_JJ_fitted = Cp_LiFePO4(T_JJ, best_params)

    Cp_JJ_exp = Cp_LiFePO4(T_exp, best_params)[0]
    err = []
    for Ti, Cp, Cpexp in zip(T_exp, Cp_JJ_exp, Cp_exp):
        err.append(((Cp-Cpexp)/Cpexp)**2)

    fig = plt.figure(figsize=(10, 10))
    gs = fig.add_gridspec(ncols=2, nrows=5, hspace=0, right=0.99, top=.99, bottom=.05, left=0.09, wspace=0.2 )
    ax = gs.subplots(sharex=True)
    ax[0][0].set_title(r'$C_{P}(T)$', y=0.8)
    # ax[0].plot(T, C_exp, label = 'xxxx', marker='X', linestyle='None', markerfacecolor='None', markeredgecolor='black')
    ax[0][0].plot(T_exp, Cp_exp, label='BATT [140]', marker='s', linestyle='None', markerfacecolor='None',
                  markeredgecolor='purple')
    # ax[0][0].plot(T_exp22, Cp_exp22 / 7, label='Loos [xx]', marker='o', linestyle='None', markerfacecolor='None',
    #               markeredgecolor='mediumpurple')
    # ax[0].plot(T_ph, Cp_ph, label = 'phonon', marker='None', linestyle='--', color='cornflowerblue')
    ax[0][0].plot(T_JJ, Cp_JJ, label='Murnaghan', marker='None', linestyle='-', color='orchid')
    ax[0][0].plot(T_JJ, Cp_JJ_fitted, label='fitted ', marker='None', linestyle='-', color='C3')
    ax[0][0].legend(loc='lower right')
    ax[0][0].set_xticklabels([])
    ax[0][0].tick_params(axis="x", direction="in")

    # ax[1].plot(T_exp,err)
    ax[1][0].set_title(r'$F^{XS}(T)$', y=0.7)
    ax[1][0].plot(T_JJ, Sa_JJ/1000, label='Murnaghan', color='orchid')
    ax[1][0].plot(T_JJ, Sa_JJ_fitted/1000, label=r'fitted $C_P$', color='C3')
    ax[1][0].legend(loc='center right')
    ax[1][0].set_xticklabels([])
    ax[1][0].tick_params(axis="x", direction="in")

    ax[2][0].set_title(r'$F_{el}(T)$', y=0.7)
    ax[2][0].plot(T_JJ, Fel_JJ / 1e-4, label='Murnaghan', color='orchid')
    ax[2][0].plot(T_JJ, Fel_JJ_fitted / 1e-4, label=r'fitted $C_P$', color='C3')
    ax[2][0].legend(loc='lower right')
    ax[2][0].set_xticklabels([])
    ax[2][0].tick_params(axis="x", direction="in")

    ax[3][0].set_title(r'$F_{def}(T)$', y=0.7)
    ax[3][0].plot(T_JJ, Fdef_JJ / 1e-4, label='Murnaghan', color='orchid')
    ax[3][0].plot(T_JJ, Fdef_JJ_fitted / 1e-4, label=r'fitted $C_P$', color='C3')
    ax[3][0].legend(loc='center right')
    ax[3][0].set_xticklabels([])
    ax[3][0].tick_params(axis="x", direction="in")

    ax[4][0].set_title(r'$\theta_D(T)$', y=0.7)
    ax[4][0].plot(T_JJ, tD_JJ, label='Murnaghan', color='orchid')
    ax[4][0].plot(T_JJ, tD_JJ_fitted, label=r'fitted $C_P$', color='C3')
    ax[4][0].legend(loc='lower right')
    ax[4][0].set_xticks([x*100 for x in range(9)], labels=[str(x*100) for x in range(9)])
    ax[4][0].tick_params()

    ax[0][1].set_title(r'$\alpha(T)$', y=0.7)
    ax[0][1].plot(T_JJ, a_JJ/1e-5, label='Murnaghan', color='orchid')
    ax[0][1].plot(T_JJ, (a_JJ_fitted - min(a_JJ_fitted))/1e-5, label=r'fitted $C_P$', color='C3')
    ax[0][1].legend(loc='lower right')
    ax[0][1].set_xticklabels([])
    ax[0][1].tick_params(axis="x", direction="in")

    ax[1][1].set_title(r'$K_T(T)$', y=0.7)
    ax[1][1].plot(T_JJ, Kt_JJ/1e9, label='Murnaghan', color='orchid')
    ax[1][1].plot(T_JJ, Kt_JJ_fitted/1e9, label=r'fitted $C_P$', color='C3')
    ax[1][1].legend(loc='center right')
    ax[1][1].set_xticklabels([])
    ax[1][1].tick_params(axis="x", direction="in")

    ax[2][1].set_title(r'$G(T)$', y=0.8)
    ax[2][1].plot(T_JJ, G_JJ/1e3, label='Murnaghan', color='orchid')
    ax[2][1].plot(T_JJ, G_JJ_fitted/1e3, label=r'fitted $C_P$', color='C3')
    ax[2][1].legend(loc='upper right')
    ax[2][1].set_xticklabels([])
    ax[2][1].tick_params(axis="x", direction="in")

    ax[3][1].plot(T_JJ, np.array([a_JJi * V_JJi for a_JJi, V_JJi in zip(a_JJ, V_JJ)])/1e-10, label=r'$V\cdot \alpha$, Murn.',
                  marker='s', linestyle='None', markerfacecolor='None', markeredgecolor='orchid')
    ax[3][1].plot(T_JJ, -dSdP_T_JJ/1e-10, label=r'$-\left(\frac{\partial S}{\partial P}\right)_T$, Murn.', marker='x',
                  linestyle='None', markerfacecolor='None', markeredgecolor='orchid')
    ax[3][1].plot(T_JJ, np.array([(a_JJi - a_JJ_fitted[0]) * V_JJi for a_JJi, V_JJi in zip(a_JJ_fitted, V_JJ_fitted)])/1e-10,
                  label=r'$V\cdot \alpha$, fitted $C_P$', marker='s', linestyle='None', markerfacecolor='None',
                  markeredgecolor='C3')
    ax[3][1].plot(T_JJ, -(dSdP_T_JJ_fitted - dSdP_T_JJ_fitted[0])/1e-10,
                  label=r'$-\left(\frac{\partial S}{\partial P}\right)_T$, fitted $C_P$', marker='x', linestyle='None',
                  markerfacecolor='None', markeredgecolor='C3')
    ax[3][1].legend(loc='lower center', ncol=2, fontsize=8)
    ax[3][1].set_xticklabels([])
    ax[3][1].tick_params(axis="x", direction="in")

    ax[4][1].plot(T_JJ, np.array([dBti / Bti ** 2 for dBti, Bti in zip(dKtdT_P_JJ, Kt_JJ)])/1e-15,
                  label=r'$\frac{1}{K_T^2}\left(\frac{\partial K_T}{\partial T}\right)_P$, Murn.', marker='s',
                  linestyle='None', markerfacecolor='None', markeredgecolor='orchid')
    ax[4][1].plot(T_JJ, dadP_T_JJ/1e-15, label=r'$-\left(\frac{\partial \alpha}{\partial P}\right)_T$, Murn.', marker='x',
                  linestyle='None', markerfacecolor='None', markeredgecolor='orchid')
    ax[4][1].plot(T_JJ, [dBti / Bti ** 2/1e-15-dKtdT_P_JJ_fitted[0]/Kt_JJ_fitted[0]** 2/1e-15 for dBti, Bti in zip(dKtdT_P_JJ_fitted, Kt_JJ_fitted)],
                  label=r'$\frac{1}{K_T^2}\left(\frac{\partial K_T}{\partial T}\right)_P$, fitted $C_P$', marker='s',
                  linestyle='None', markerfacecolor='None', markeredgecolor='C3')
    ax[4][1].plot(T_JJ, (dadP_T_JJ_fitted-dadP_T_JJ_fitted[0])/1e-15, label=r'$-\left(\frac{\partial \alpha}{\partial P}\right)_T$, fitted $C_P$',
                  marker='x', linestyle='None', markerfacecolor='None', markeredgecolor='C3')
    ax[4][1].legend(loc='lower center', ncol=2, fontsize=8)
    ax[4][1].set_xticks([x * 100 for x in range(9)], labels=[str(x * 100) for x in range(9)])
    ax[4][1].tick_params()

    ax[0][0].set_ylabel('$[J/(K\cdot mol-at)]$')
    ax[1][0].set_ylabel('$[kJ/(mol-at)]$')
    ax[2][0].set_ylabel('$[10^{-4}J/mol-at]$')
    ax[3][0].set_ylabel('$[10^{-4}J/mol-at]$')
    ax[4][0].set_ylabel('$[K]$')
    ax[4][0].set_xlabel('Temperature $[K]$')

    ax[4][1].set_ylabel(r'$[10^{-6}/(GPa\cdot K)]$')
    ax[3][1].set_ylabel(r'$[10^{-10}m^3/(K\cdot mol-at)]$')
    ax[2][1].set_ylabel(r'$[kJ/mol-at]$')
    ax[1][1].set_ylabel(r'$[GPa]$')
    ax[0][1].set_ylabel(r'$[10^{-5}/K]$')
    ax[4][1].set_xlabel('Temperature $[K]$')


    ax[2][0].set_ylim((-3.1, 3.1))
    ax[3][1].set_ylim((-8.5, 11))
    ax[4][1].set_ylim((-2.5, 1))

    print(V_JJ_fitted)
    print(T_JJ)
    plt.show()

    end = time.perf_counter()
    print(end - start)