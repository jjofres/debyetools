from debyetools import pairanalysis as pa_calc

import numpy as np

size = np.array([1, 1, 1])
cutoff =5
center = np.array([0, 0, 0])
primitive_cell = np.array([[4.0396918604, 0, 0], [0, 4.0396918604, 0], [0, 0, 4.0396918604]])
basis_vectors = np.array([[0, 0, 0], [.5, .5, 0], [.5, 0, .5], [0, .5, .5]])
atom_types = 'AlAlAlAl'

results =pa_calc.pair_analysis(atom_types, size, cutoff, center, basis_vectors, primitive_cell)

print(results)
