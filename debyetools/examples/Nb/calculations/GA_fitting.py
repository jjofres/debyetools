import load_data_from_DFT as ldft
import numpy as np
import debyetools.potentials as potentials
from matplotlib import pyplot as plt
from debyetools.electronic import fit_electronic
from debyetools.poisson import poisson_ratio
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts
dir_list_initial = [d for d in dir()]+['dir_list_initial']


#############
# load data #
#############
#------------------------------------------------------------
VASPrun_Data = ldft.extract_from_DFT('..')

print('Data loaded')
#------------------------------------------------------------

########################
# EOS parameterization #
########################
#------------------------------------------------------------
E_data = VASPrun_Data.E
V_data = VASPrun_Data.V

V_DFT, E_DFT = np.array([Vi*(1e-30 * 6.02e23) for Vi in V_data]), np.array([Ei*(0.160218e-18 * 6.02214e23) for Ei in E_data])
initial_parameters = np.array([-4e+05, 1e-05, 7e+10, 4])
eos_BM = potentials.BM()
eos_BM.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters, fit=True)

print('EOS parameterization done. \n\tParameters:', eos_BM.pEOS)
#------------------------------------------------------------

###########################
# electronic contribution #
###########################
#------------------------------------------------------------
p_el_inittial = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
E,N,Ef = VASPrun_Data.electric
p_electronic = fit_electronic(V_DFT, p_el_inittial,E,N,Ef)#

print(f'Electronic contribution parameterization done. \n\tParameters: {p_electronic}')
#------------------------------------------------------------

##################
# poissons ratio #
##################
#------------------------------------------------------------
nu = poisson_ratio(VASPrun_Data.EM)
print('Elastic constants:')
for c in VASPrun_Data.EM:
    print(f'\t', end='')
    for ci in c:
        print(f'{ci:.3f}', end='\t')
    print()
print(f'Poisson ratio: {nu}')
#------------------------------------------------------------

#######################
# other contributions #
#######################
#------------------------------------------------------------
Tmelting = 2750
p_defects = 1e10, 0, Tmelting, 0.1#6, 2, Tmelting, 0.1# 5, 1.5, 2750, 0.1 #
p_intanh = 0, 1
p_anh = 0, 0, 0
print('Other contributions set to:')
print(f'\t Tmelting: {Tmelting}, pdefects: {p_defects}, pintanh: {p_intanh}, anh: {p_anh}')
#------------------------------------------------------------

#########
# min G #
#########
#------------------------------------------------------------
ndeb_BM = nDeb(nu, VASPrun_Data.mass, p_intanh, eos_BM, p_electronic, p_defects, p_anh,mode='jjsl')
T_initial, T_final, number_Temps = 0.1, Tmelting, 100
T = gen_Ts(T_initial, T_final, number_Temps)
T, V = ndeb_BM.min_G(T,eos_BM.V0*.8,P=0)

print(f'Gibbs free energy minimization done. \n\tT: [{T[0]} ... {T[-1]}] \n\tV: [{V[0]} ... {V[-1]}]')
#------------------------------------------------------------

##########################################
# evaluation of thermodynamic properties #
##########################################
#------------------------------------------------------------
kB = 8.31446261815324
tprops_dict = ndeb_BM.eval_props(T,V,P=0)
Cp = tprops_dict['Cp']
a = tprops_dict['a']
Ks = tprops_dict['Ks']

print(f'Evaluation of thermodynamic properties done. \n\tCp: [{Cp[0]} ... {Cp[-1]}] \n\ta: [{a[0]} ... {a[-1]}] \n\tKs: [{Ks[0]} ... {Ks[-1]}]')
#------------------------------------------------------------

#################################
# save inputs from previous run #
#################################
#------------------------------------------------------------
dir_list_final = [d for d in dir()]+['dir_list_final']

E0, V0, K0, K0p = ndeb_BM.EOS.pEOS
nu0 = ndeb_BM.nu
a0, m0, Va = ndeb_BM.intanh.pintanh
s0, s1, s2 = ndeb_BM.anh.panh

edef, sdef, Tmdef, adef, Pdef, vdef = ndeb_BM.deff.pdef

pel0, pel1, pel2, pel3 = ndeb_BM.el.pel
xs0, xs1, xs2, xs3, xs4, xs5 = [ndeb_BM.xs.xs0, ndeb_BM.xs.xs1, ndeb_BM.xs.xs2, ndeb_BM.xs.xs3, ndeb_BM.xs.xs4, ndeb_BM.xs.xs5]

params = E0, V0, K0, K0p, nu, a0, m0, s0, s1, s2, edef, sdef, adef, pel0, pel1, pel2, pel3, xs0, xs1, xs2, xs3, xs4, xs5


T_dt_vib_el = T
Cp_dt_vib_el = Cp
a_dt_vib_el = a
Ks_dt_vib_el = Ks

print('\nImputs from previous calculations saved.')
#------------------------------------------------------------

########################
# load literature data #
########################
#------------------------------------------------------------

# kB = 8.31446261815324
dL = type('dataLiterature', (object,), {})()
list_lit = ['exp', 'DFT', 'MTP', 'eMTP', 'eMTPup']
for lit in list_lit:
    for prop in ['Cp', 'alpha', 'Ks']:
        setattr(dL, f'{prop}_{lit}', np.loadtxt(f'data_literature/data{prop}_{lit}'))

T_exp = dL.Cp_exp[:,0]
Cp_exp = dL.Cp_exp[:,1]*kB

print('Literature data loaded.')
#------------------------------------------------------------

####################
# delete variables #
####################
#------------------------------------------------------------
for d in [d for d in dir_list_final if d not in dir_list_initial+['VASPrun_Data']]:
    del globals()[d]
print('Variables reset.')
#------------------------------------------------------------

#######################################
# Genetic algorithm parameter fitting #
#######################################
#------------------------------------------------------------
from debyetools.optim import ga_fitting, props, random_sample_with_min_distance_2d, get_params_list

eos_BM = potentials.BM()
eos_BM.fitEOS([V0], [E0], initial_parameters=[E0, V0, K0, K0p], fit=False)

mass = VASPrun_Data.mass

# lst_str = ['E0', 'V0', 'K0', 'K0p', 'nu', 'a0', 'm0', 's0', 's1', 's2',
#                'edef', 'sdef', 'vdef', 'pel0', 'pel1', 'pel2', 'pel3', 'xs0', 'xs1', 'xs2', 'xs3', 'xs4', 'xs5']
str_params2fit = ['edef', 'sdef']
initial_guess = [10, 1]

# for iiii in range(1):

def f2fit(Temp, pf):
    return props(Temp, get_params_list(params, pf, str_params2fit), mass, eos_BM, Tmdef)['Cp']


ix_highT = list(np.where(T_exp > 300)[0])

# Take a random sample of 10 numbers from ix_T_exp
new_T = T_exp[ix_highT]
my_lst2sample = np.array([ix_highT, new_T])
sampled_data = random_sample_with_min_distance_2d(my_lst2sample, 15, 150, 200)

ix_sample = [int(s) for s in sampled_data[0]]

T_data_fit = T_exp[ix_sample]
Cp_data_fit = Cp_exp[ix_sample]

print('Fitting: '+', '.join(str_params2fit))
best_params = ga_fitting (f2fit, T_data_fit, Cp_data_fit, initial_guess, param_range=(0.8, 1.2),
                        stagnant_gens=10, npop=20, ngen=50, pcross=0.5, pmut=0.5, verbose=True, tol=0.1)

print('\tBest parameters:', ', '.join([f'{s}:{b}' for s, b in zip(str_params2fit, best_params)]))
#------------------------------------------------------------

################
# Plot Fitting #
################
#------------------------------------------------------------
T= np.linspace(0.1, Tmdef, 100)
params_afer_fit = get_params_list(params, best_params, str_params2fit)
tprops = props(T, params_afer_fit, mass, eos_BM, Tmdef, v=True)
Cp = tprops['Cp']
a = tprops['a']
Ks = tprops['Ks']

fig1, ax1 = plt.subplots()
ax1.plot(T, Cp, 'k-')
ax1.plot(T_data_fit, Cp_data_fit, 'o')

ax1.set_xlabel('Temperature [K]')
ax1.set_ylabel(r'$C_P/k_B$ ')

#------------------------------------------------------------

######################################
# plot thermodynamic properties vs T #
######################################
#------------------------------------------------------------

# load literature data
kB = 8.31446261815324

dL = type('dataLiterature', (object,), {})()
list_lit = ['exp', 'DFT', 'MTP', 'eMTP', 'eMTPup']
for lit in list_lit:
    for prop in ['Cp', 'alpha', 'Ks']:
        setattr(dL, f'{prop}_{lit}', np.loadtxt(f'data_literature/data{prop}_{lit}'))

# plot Cp vs T, alpha vs T, Ks vs T
fig, ax = plt.subplots(1,3, figsize=(14,5))

labelst = [r'debyetools (vib+el)', r'debyetools (vib+el+def$^{fitted}$)', 'Exp', 'DFT', 'MTP', 'eMTP', 'eMTPup']
mtype = ['o', '-', '-', '-', '-', '-']
zorders = [11, 2, 2, 2, 2, 2]
colors = ['C0', 'purple', 'pink', 'skyblue', 'gray']


ax[0].plot(T_dt_vib_el,Cp_dt_vib_el/kB, label=labelst[0], c='k', linewidth=3, zorder=10)
ax[1].plot(T_dt_vib_el,a_dt_vib_el/3/1e-5, label=labelst[0], c='k', linewidth=3, zorder=10)
ax[2].plot(T_dt_vib_el,Ks_dt_vib_el/1e9, label=labelst[0], c='k', linewidth=3, zorder=10)

ax[0].plot(T,Cp/kB, label=labelst[1], c='b', linewidth=3, zorder=10)
ax[1].plot(T,a/3/1e-5, label=labelst[1], c='b', linewidth=3, zorder=10)
ax[2].plot(T,Ks/1e9, label=labelst[1], c='b', linewidth=3, zorder=10)


for i, lit in enumerate(list_lit):
    for j, prop in enumerate(['Cp', 'alpha', 'Ks']):
        XY = getattr(dL, f'{prop}_{lit}')
        ax[j].plot(XY[:,0], XY[:,1],mtype[i], label=labelst[i+2], zorder=zorders[i], linewidth=3, color=colors[i], markerfacecolor='none')

ax[0].set_xlabel(r'Temperature $(K)$')
ax[0].set_ylabel(r'$C_P/k_B$ ')
ax[0].legend()

ax[1].set_xlabel(r'Temperature $(K)$')
ax[1].set_ylabel(r'$\alpha_L$ $(10^{-5}/K)$')
ax[1].legend()

ax[2].set_xlabel(r'Temperature $(K)$')
ax[2].set_ylabel(r'$K_s$ $(GPa)$')
ax[2].set_ylim(110, 180)
ax[2].legend()

#------------------------------------------------------------

plt.show()



print('done')
print('done')