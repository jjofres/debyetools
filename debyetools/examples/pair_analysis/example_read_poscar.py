from debyetools.aux_functions import load_cell
from debyetools.pairanalysis import pair_analysis
formula, primitive_cell, basis_vectors = load_cell('../Al3Li_L12/CONTCAR')
cutoff = 5
pa_result = pair_analysis(formula, cutoff, basis_vectors, primitive_cell)
distances , num_pairs_per_formula , combs_types = pa_result
print('distances| # of pairs per type')
print('         | '+'  '.join(['%s' for _ in combs_types])%tuple(combs_types))
for d, n in zip( distances , num_pairs_per_formula ):
    print(' %.6f' % (d) + '| ' + ' '.join([' %.2f' for _ in n])%tuple(n))