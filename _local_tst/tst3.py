from debyetools.aux_functions import load_cell
import numpy as np
from debyetools.pairanalysis import pair_analysis
from debyetools.potentials import MP
from debyetools.potentials import EAM_tst
from time import time

tic =  time()

folder_name = 'C:/Users/Javier/Documents/GitRepos/debyetools/tests/inpt_files/Al_fcc'
formula, primitive_cell, basis_vectors = load_cell(folder_name+'/CONTCAR.5')
supcell_size, cutoff, center = np.array([1, 1, 1]), 7, np.array([0, 0, 0])
distances, num_bonds_per_formula, combs_types = pair_analysis(formula, supcell_size, cutoff, center, basis_vectors, primitive_cell)

txt2print = 'distances  | # of pairs per type\n'
combs_types = [ct.replace('x', '') for ct in combs_types]
txt2print = txt2print + '           | ' + '  '.join(['%s' for _ in combs_types]) % tuple(combs_types) + '\n'

for d, n in zip(distances, num_bonds_per_formula):
  txt2print = txt2print + '%.6f  '%(d) + ' | ' + ' '.join(['%.2f' for _ in n]) % tuple(n) + '\n'

print(txt2print)

number_of_neighbor_levels = 6
MP_eos = MP(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels)
EAM_eos = EAM_tst(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels)

V_data = np.array([7.23E-06, 7.48E-06, 7.73E-06, 7.98E-06, 8.24E-06, 8.51E-06, 8.78E-06, 9.06E-06, 9.34E-06, 9.63E-06, 9.92E-06, 1.02E-05, 1.05E-05, 1.08E-05, 1.12E-05, 1.15E-05, 1.18E-05, 1.22E-05, 1.25E-05, 1.28E-05, 1.32E-05])
E_data = np.array([-3.10E+05, -3.21E+05, -3.30E+05, -3.38E+05, -3.45E+05, -3.50E+05, -3.54E+05, -3.57E+05, -3.59E+05, -3.61E+05, -3.61E+05, -3.61E+05, -3.60E+05, -3.58E+05, -3.56E+05, -3.53E+05, -3.51E+05, -3.47E+05, -3.44E+05, -3.40E+05, -3.36E+05])

from matplotlib import pyplot as plt

plt.figure()
plt.plot(V_data, E_data, '.',label='DFT')
#plt.show()
initial_parameters_MP = [0.35, 1, 3.2]*len(MP_eos.comb_types)
initial_parameters_EAM = [2.24098838,2.60561286,1.31314414,0.90204254,0.89988286,0.95601975] \
                         * len(EAM_eos.comb_types) + [0.71921005, 0.95031406, 1.09550997, 1.21785] * EAM_eos.ntypes
MP_eos.fitEOS(V_data, E_data, initial_parameters = initial_parameters_MP)
EAM_eos.fitEOS(V_data, E_data, initial_parameters = initial_parameters_EAM)

E_model_MP = [MP_eos.E0(Vi) for Vi in V_data]
E_model_EAM = [EAM_eos.E0(Vi) for Vi in V_data]
plt.plot(V_data, E_model_MP, 'x', label='Morse')
plt.plot(V_data, E_model_EAM, '+', label='EAM', markersize=10)
plt.legend()
print('done. Took:', time()-tic, 'seconds')
print(EAM_eos.pEOS)
plt.show()