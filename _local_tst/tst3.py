from debyetools.aux_functions import load_cell
import numpy as np
from debyetools.pairanalysis import pair_analysis
from debyetools.potentials import MP, EAM, BM, MU
from time import time
from matplotlib import pyplot as plt
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts
from debyetools.fs_compound_db \
  import \
  fit_FS, Cp2fit, alpha2fit, Ksinv2fit, Ksp2fit
tic =  time()

#################
# I. Pair analysis #
#################

# i.i. Inputs:
###############
folder_name = 'C:/Users/Javier/Documents/GitRepos/debyetools/tests/inpt_files/Al_fcc'
formula, primitive_cell, basis_vectors = load_cell(folder_name+'/CONTCAR.5')
supcell_size, cutoff, center = np.array([1, 1, 1]), 7, np.array([0, 0, 0])

# i.ii. Pair analysis
######################
distances, num_bonds_per_formula, \
combs_types = pair_analysis(formula, supcell_size,
                            cutoff, center, basis_vectors, primitive_cell)

# i.iii. Print results
#######################
txt2print = 'distances  | # of pairs per type\n'
combs_types = [ct.replace('x', '') for ct in combs_types]
txt2print = txt2print + '           | ' + '  '.join(['%s' for _ in combs_types]) % tuple(combs_types) + '\n'
for d, n in zip(distances,
                num_bonds_per_formula):
  txt2print = txt2print + '%.6f  '%(d) + ' | ' + ' '.join(['%.2f' for _ in n]) % tuple(n) + '\n'
print(txt2print)

###########################
# II. EOS parametrization #
###########################

# ii.i. Inputs
###############
number_of_neighbor_levels = 6
V_data = np.array([7.1616E-06, 7.4030E-06, 7.6497E-06, 7.9019E-06, 8.1595E-06, 8.4227E-06, 8.6915E-06, 8.9660E-06, 9.2461E-06, 9.5321E-06, 9.8239E-06, 1.0122E-05, 1.0425E-05, 1.0735E-05, 1.1051E-05, 1.1372E-05, 1.1700E-05, 1.2035E-05, 1.2375E-05, 1.2722E-05, 1.3076E-05])
E_data = np.array([-2.8672E+05, -2.9541E+05, -3.0278E+05, -3.0897E+05, -3.1407E+05, -3.1820E+05, -3.2141E+05, -3.2379E+05, -3.2541E+05, -3.2632E+05, -3.2660E+05, -3.2632E+05, -3.2553E+05, -3.2428E+05, -3.2263E+05, -3.2058E+05, -3.1821E+05, -3.1555E+05, -3.1266E+05, -3.0955E+05, -3.0625E+05])

# ii.ii. EOS instantiation
###########################
MP_eos = MP(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels)
EAM_eos = EAM(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels)
BM_eos = BM()
MU_eos = MU()

# ii.iii. Intial guess
#######################
initial_parameters_MP = [0.35, 1, 3.2]*len(MP_eos.comb_types)
initial_parameters_EAM = initial_parameters_EAM = [2.24098838,2.60561286,1.31314414,0.90204254,0.89988286,0.95601975] * len(EAM_eos.comb_types) + [0.71921005, 0.95031406, 1.09550997, 1.21785] * EAM_eos.ntypes
initial_parameters_BM = initial_parameters_MU = [-3.61E+05, 9.92E-06, 72e9, 4]

# ii.iv. Parameter adjusting
#############################
tic2=time()
print('\nfitEOS')
MP_eos.fitEOS(V_data, E_data, initial_parameters = initial_parameters_MP)
print('fitEOS MP time:',time()-tic2)
tic4 = time()
print('fitEOS EAM time:',time()-tic4)
tic3 = time()
EAM_eos.fitEOS(V_data, E_data, initial_parameters = initial_parameters_EAM)
print('fitEOS EAM time:',time()-tic3)
tic31 = time()
BM_eos.fitEOS(V_data, E_data, initial_parameters = initial_parameters_MU)
print('fitEOS EAM time:',time()-tic31)
tic32 = time()
MU_eos.fitEOS(V_data, E_data, initial_parameters = initial_parameters_MU)
print('fitEOS EAM time:',time()-tic32)

# ii.v. Plot results
#####################
E_model_MP = [MP_eos.E0(Vi) for Vi in V_data]
E_model_EAM = [EAM_eos.E0(Vi) for Vi in V_data]
E_model_BM = [BM_eos.E0(Vi) for Vi in V_data]
E_model_MU = [MU_eos.E0(Vi) for Vi in V_data]

fig1, ax1 = plt.subplots()
ax1.plot(V_data, E_data, '.',label='DFT')

ax1.plot(V_data, E_model_MP, 'x', label='Morse')
ax1.plot(V_data, E_model_EAM, '+', label='EAM', markersize=10)
ax1.plot(V_data, E_model_BM, '+', label='BM', markersize=10)
ax1.plot(V_data, E_model_MU, '+', label='MU', markersize=10)

ax1.legend()

#################################
# III. Free energy minimization #
#################################

# iii.i. Input parameter
#########################
nu, m, p_intanh, p_electronic, p_defects, p_anh = 0.229, 0.021971375, [0,1], [0,0,0,0], [1e4, 0, 1e4, 0.1], [0,0,0]
mode = 'DM'

# iii.ii. nDeb instantiation
#############################
ndeb_MP = nDeb(nu, m, p_intanh, MP_eos, p_electronic, p_defects, p_anh, mode=mode)
ndeb_EAM = nDeb(nu, m, p_intanh, EAM_eos, p_electronic, p_defects, p_anh, mode=mode)
ndeb_BM = nDeb(nu, m, p_intanh, BM_eos, p_electronic, p_defects, p_anh, mode=mode)
ndeb_MU = nDeb(nu, m, p_intanh, MU_eos, p_electronic, p_defects, p_anh, mode=mode)

# iii.iii. Range of temperature
################################
T_initial, T_final, number_Temps = 0.1, 1000, 30
T = gen_Ts(T_initial, T_final, number_Temps)
Pressure = 0

# iii.iv. Energy minimization
##############################
print('\nmin_G')
tic5 = time()
T_MP, V_MP = ndeb_MP.min_G(T,MP_eos.V0,Pressure)
print('min_G MP time:',time()-tic5)
tic6 = time()
print('min_G EAM time:',time()-tic6)
tic7 = time()
T_EAM, V_EAM = ndeb_EAM.min_G(T,EAM_eos.V0,Pressure)
print('min_G EAM time:',time()-tic7)
tic71 = time()
T_BM, V_BM = ndeb_BM.min_G(T,BM_eos.V0,Pressure)
print('min_G BM time:',time()-tic71)
tic72 = time()
T_MU, V_MU = ndeb_MU.min_G(T,MU_eos.V0,Pressure)
print('min_G MU time:',time()-tic72)

# iii.v. Plot results
######################
fig2, ax2 = plt.subplots()
ax2.plot(T_MP,V_MP,'+', color='C1', label='Morse')
ax2.plot(T_EAM,V_EAM, '-', color='C3', label='EAM')
ax2.plot(T_BM,V_BM, '-', color='C4', label='BM')
ax2.plot(T_MU,V_MU, '-', color='C5', label='MU')
ax2.legend()

##############################################
# IV. Evaluaiton of Thermodynamic properties #
##############################################

# iv.i. Evaluation
###################
print('\neval_tprops')
tic8=time()
tprops_MP = ndeb_MP.eval_props(T_MP,V_MP,Pressure)
print('eval_tprops MP time:', time()-tic8)
tic10=time()
tprops_EAM = ndeb_EAM.eval_props(T_EAM,V_EAM,Pressure)
print('eval_tprops EAM time:', time()-tic10)
tic101=time()
tprops_BM = ndeb_BM.eval_props(T_BM,V_BM,Pressure)
print('eval_tprops BM time:', time()-tic101)
tic102=time()
tprops_MU = ndeb_MU.eval_props(T_MU,V_MU,Pressure)
print('eval_tprops MU time:', time()-tic102)

# iv.ii. Plot results
######################
fig3, ax3 = plt.subplots(2, 2)
ax3[0, 0].plot(tprops_MP['T'],tprops_MP['Cp'],'--', color='C1', label='Morse')
ax3[0, 0].plot(tprops_EAM['T'],tprops_EAM['Cp'], '--', color='C3', label='EAM')
ax3[0, 0].plot(tprops_BM['T'],tprops_BM['Cp'], '--', color='C4', label='BM')
ax3[0, 0].plot(tprops_MU['T'],tprops_MU['Cp'], '--', color='C5', label='MU')

ax3[1, 0].plot(tprops_MP['T'],tprops_MP['a'],'--', color='C1', label='Morse')
ax3[1, 0].plot(tprops_EAM['T'],tprops_EAM['a'], '--', color='C3', label='EAM')
ax3[1, 0].plot(tprops_BM['T'],tprops_BM['a'], '--', color='C4', label='BM')
ax3[1, 0].plot(tprops_MU['T'],tprops_MU['a'], '--', color='C5', label='MU')

ax3[0, 1].plot(tprops_MP['T'],tprops_MP['Ks'],'--', color='C1', label='Morse')
ax3[0, 1].plot(tprops_EAM['T'],tprops_EAM['Ks'], '--', color='C3', label='EAM')
ax3[0, 1].plot(tprops_BM['T'],tprops_BM['Ks'], '--', color='C4', label='BM')
ax3[0, 1].plot(tprops_MU['T'],tprops_MU['Ks'], '--', color='C5', label='MU')

ax3[1, 1].plot(tprops_MP['T'],tprops_MP['Ksp'],'--', color='C1', label='Morse')
ax3[1, 1].plot(tprops_EAM['T'],tprops_EAM['Ksp'], '--', color='C3', label='EAM')
ax3[1, 1].plot(tprops_BM['T'],tprops_BM['Ksp'], '--', color='C4', label='BM')
ax3[1, 1].plot(tprops_MU['T'],tprops_MU['Ksp'], '--', color='C5', label='MU')

############################################
# V. FactSage compound database parameters #
############################################

# v.i. Temperature range
#########################
T_from = 298.15
T_to = T_final

# v.ii. Parametrization
########################
print('\nfit_FS')
tic11 = time()
FS_db_params_MP = fit_FS(tprops_MP, T_from, T_to)
print('fit_FS MP time:', time()-tic11)
tic13 = time()
FS_db_params_EAM = fit_FS(tprops_EAM, T_from, T_to)
print('fit_FS EAM time:', time()-tic13)
tic131 = time()
FS_db_params_BM = fit_FS(tprops_BM, T_from, T_to)
print('fit_FS BM time:', time()-tic131)
tic132 = time()
FS_db_params_MU = fit_FS(tprops_MU, T_from, T_to)
print('fit_FS MU time:', time()-tic132)

# v.iii. Plot results
######################
C0, C1, C2, C3, C4, C5 = FS_db_params_MP['Cp']
ix_Tfrom_MP = np.where(np.round(T_MP,2) == np.round(T_from,2))[0][0]
Cp_FS_MP = [Cp2fit(Ti, C0, C1, C2, C3, C4, C5) for Ti in T_MP[ix_Tfrom_MP:]]
ax3[0,0].plot(T_MP[ix_Tfrom_MP:], Cp_FS_MP, '.', label='MP_FS', color='C1')
C0, C1, C2, C3, C4, C5 = FS_db_params_EAM['Cp']
ix_Tfrom_EAM = np.where(np.round(T_EAM,2) == np.round(T_from,2))[0][0]
Cp_FS_EAM = [Cp2fit(Ti, C0, C1, C2, C3, C4, C5) for Ti in T_EAM[ix_Tfrom_EAM:]]
ax3[0,0].plot(T_EAM[ix_Tfrom_EAM:], Cp_FS_EAM, '.', label='EAM_FS', color='C3')
C0, C1, C2, C3, C4, C5 = FS_db_params_BM['Cp']
ix_Tfrom_BM = np.where(np.round(T_BM,2) == np.round(T_from,2))[0][0]
Cp_FS_BM = [Cp2fit(Ti, C0, C1, C2, C3, C4, C5) for Ti in T_BM[ix_Tfrom_BM:]]
ax3[0,0].plot(T_BM[ix_Tfrom_BM:], Cp_FS_BM, '.', label='BM_FS', color='C4')
C0, C1, C2, C3, C4, C5 = FS_db_params_MU['Cp']
ix_Tfrom_MU = np.where(np.round(T_MU,2) == np.round(T_from,2))[0][0]
Cp_FS_MU = [Cp2fit(Ti, C0, C1, C2, C3, C4, C5) for Ti in T_MU[ix_Tfrom_MU:]]
ax3[0,0].plot(T_MU[ix_Tfrom_MU:], Cp_FS_MU, '.', label='MU_FS', color='C5')

C0, C1, C2, C3 = FS_db_params_MP['a']
ix_Tfrom_MP = np.where(np.round(T_MP,2) == np.round(T_from,2))[0][0]
Cp_FS_MP = [alpha2fit(Ti, C0, C1, C2, C3) for Ti in T_MP[ix_Tfrom_MP:]]
ax3[1,0].plot(T_MP[ix_Tfrom_MP:], Cp_FS_MP, '.', label='MP_FS', color='C1')
C0, C1, C2, C3 = FS_db_params_EAM['a']
ix_Tfrom_EAM = np.where(np.round(T_EAM,2) == np.round(T_from,2))[0][0]
Cp_FS_EAM = [alpha2fit(Ti, C0, C1, C2, C3) for Ti in T_EAM[ix_Tfrom_EAM:]]
ax3[1,0].plot(T_EAM[ix_Tfrom_EAM:], Cp_FS_EAM, '.', label='EAM_FS', color='C3')
C0, C1, C2, C3 = FS_db_params_BM['a']
ix_Tfrom_BM = np.where(np.round(T_BM,2) == np.round(T_from,2))[0][0]
Cp_FS_BM = [alpha2fit(Ti, C0, C1, C2, C3) for Ti in T_BM[ix_Tfrom_BM:]]
ax3[1,0].plot(T_BM[ix_Tfrom_BM:], Cp_FS_BM, '.', label='BM_FS', color='C4')
C0, C1, C2, C3 = FS_db_params_MU['a']
ix_Tfrom_MU = np.where(np.round(T_MU,2) == np.round(T_from,2))[0][0]
Cp_FS_MU = [alpha2fit(Ti, C0, C1, C2, C3) for Ti in T_MU[ix_Tfrom_MU:]]
ax3[1,0].plot(T_MU[ix_Tfrom_MU:], Cp_FS_MU, '.', label='MU_FS', color='C5')

C0, C1, C2, C3 = FS_db_params_MP['1/Ks']
ix_Tfrom_MP = np.where(np.round(T_MP,2) == np.round(T_from,2))[0][0]
Cp_FS_MP = [1/Ksinv2fit(Ti, C0, C1, C2, C3) for Ti in T_MP[ix_Tfrom_MP:]]
ax3[0,1].plot(T_MP[ix_Tfrom_MP:], Cp_FS_MP, '.', label='MP_FS', color='C1')
C0, C1, C2, C3 = FS_db_params_EAM['1/Ks']
ix_Tfrom_EAM = np.where(np.round(T_EAM,2) == np.round(T_from,2))[0][0]
Cp_FS_EAM = [1/Ksinv2fit(Ti, C0, C1, C2, C3) for Ti in T_EAM[ix_Tfrom_EAM:]]
ax3[0,1].plot(T_EAM[ix_Tfrom_EAM:], Cp_FS_EAM, '.', label='EAM_FS', color='C3')
C0, C1, C2, C3 = FS_db_params_BM['1/Ks']
ix_Tfrom_BM = np.where(np.round(T_BM,2) == np.round(T_from,2))[0][0]
Cp_FS_BM = [1/Ksinv2fit(Ti, C0, C1, C2, C3) for Ti in T_BM[ix_Tfrom_BM:]]
ax3[0,1].plot(T_BM[ix_Tfrom_BM:], Cp_FS_BM, '.', label='BM_FS', color='C4')
C0, C1, C2, C3 = FS_db_params_MU['1/Ks']
ix_Tfrom_MU = np.where(np.round(T_MU,2) == np.round(T_from,2))[0][0]
Cp_FS_MU = [1/Ksinv2fit(Ti, C0, C1, C2, C3) for Ti in T_MU[ix_Tfrom_MU:]]
ax3[0,1].plot(T_MU[ix_Tfrom_MU:], Cp_FS_MU, '.', label='MU_FS', color='C5')

C0, C1 = FS_db_params_MP['Ksp']
ix_Tfrom_MP = np.where(np.round(T_MP,2) == np.round(T_from,2))[0][0]
Cp_FS_MP = [Ksp2fit(Ti, C0, C1) for Ti in T_MP[ix_Tfrom_MP:]]
ax3[1,1].plot(T_MP[ix_Tfrom_MP:], Cp_FS_MP, '.', label='MP_FS', color='C1')
C0, C1 = FS_db_params_EAM['Ksp']
ix_Tfrom_EAM = np.where(np.round(T_EAM,2) == np.round(T_from,2))[0][0]
Cp_FS_EAM = [Ksp2fit(Ti, C0, C1) for Ti in T_EAM[ix_Tfrom_EAM:]]
ax3[1,1].plot(T_EAM[ix_Tfrom_EAM:], Cp_FS_EAM, '.', label='EAM_FS', color='C3')
C0, C1 = FS_db_params_BM['Ksp']
ix_Tfrom_BM = np.where(np.round(T_BM,2) == np.round(T_from,2))[0][0]
Cp_FS_BM = [Ksp2fit(Ti, C0, C1) for Ti in T_BM[ix_Tfrom_BM:]]
ax3[1,1].plot(T_BM[ix_Tfrom_BM:], Cp_FS_BM, '.', label='BM_FS', color='C4')
C0, C1 = FS_db_params_MU['Ksp']
ix_Tfrom_MU = np.where(np.round(T_MU,2) == np.round(T_from,2))[0][0]
Cp_FS_MU = [Ksp2fit(Ti, C0, C1) for Ti in T_MU[ix_Tfrom_MU:]]
ax3[1,1].plot(T_MU[ix_Tfrom_MU:], Cp_FS_MU, '.', label='MU_FS', color='C5')

ax3[0, 0].legend()
ax3[1, 0].legend()
ax3[0, 1].legend()
ax3[1, 1].legend()

print('\ndone. Took:', time()-tic, 'seconds')
plt.show()