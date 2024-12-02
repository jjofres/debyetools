import numpy as np

from debyetools.pairanalysis import pair_analysis

formula = 'AABA'
cutoff = 10
basis_vectors = np.array([[0,0,0], [.5,.5,0], [.5,0,.5], [0,.5,.5]])
primitive_cell = np.array([[4,0,0] ,[0,4,0] ,[0,0,4]])
pa_result = pair_analysis(formula, cutoff, basis_vectors, primitive_cell)
distances , num_pairs_per_formula , combs_types = pa_result
print('distances| # of pairs per type')
print('         | '+'  '.join(['%s' for _ in combs_types])%tuple(combs_types))
for d, n in zip( distances , num_pairs_per_formula ):
    print(' %.6f' % (d) + '| ' + ' '.join([' %.2f' for _ in n]) % tuple(n))

