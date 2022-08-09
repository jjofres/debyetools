from debyetools.aux_functions import load_cell
import numpy as np
from debyetools.pairanalysis import pair_analysis

folder_name = 'C:/Users/Paul/Documents/Javier/GitRepos/debyetools/tests/inpt_files/Al_fcc'
formula, primitive_cell, basis_vectors = load_cell(folder_name+'/CONTCAR.5')
supcell_size, cutoff, center = np.array([1, 1, 1]), 5, np.array([0, 0, 0])
distances, num_bonds_per_formula, combs_types = pair_analysis(formula, supcell_size, cutoff, center, basis_vectors, primitive_cell)

txt2print = 'distances  | # of pairs per type\n'
combs_types = [ct.replace('x','') for ct in combs_types]
txt2print = txt2print + '           | ' + '  '.join(['%s' for _ in combs_types])%tuple(combs_types) + '\n'

for d, n in zip(distances, num_bonds_per_formula):
  txt2print = txt2print + '%.6f  '%(d)+' | ' + ' '.join(['%.2f' for _ in n])%tuple(n)+'\n'

print(txt2print)
