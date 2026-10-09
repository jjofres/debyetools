..  _pairanalysis:

=========================
Pair Analysis Calculation
=========================

A pair analysis calculator was implemented  where the atom position can be read from a POSCAR file or entered manually. The neighbor list and binning are calculated to build up the pairs list.

Example
=======

>>> import numpy as np
>>> from debyetools.pairanalysis import pair_analysis
>>> formula = 'AaAaBbAa'
>>> cutoff = 10
>>> basis_vectors = np.array([[0,0,0], [.5,.5,0], [.5,0,.5], [0,.5,.5]])
>>> primitive_cell = np.array([[4,0,0] ,[0,4,0] ,[0,0,4]])
>>> distances, num_pairs_per_formula, combs_types = pair_analysis(formula, cutoff, basis_vectors, primitive_cell)
>>> print('distances | # of pairs per type')
distances | # of pairs per type
>>> print('          | ' + '  '.join(combs_types))
          | Aa-Aa  Aa-Bb  Bb-Bb
>>> for d, n in zip(distances, num_pairs_per_formula):
...     print(' %.6f |' % d + ''.join(' %6.2f' % ni for ni in n))
 2.828427 |   6.00   6.00   0.00
 4.000000 |   4.50   0.00   1.50
 4.898979 |  12.00  12.00   0.00
 5.656854 |   9.00   0.00   3.00
 6.324555 |  12.00  12.00   0.00
 6.928203 |   6.00   0.00   2.00
 7.483315 |  24.00  24.00   0.00
 8.000000 |   4.50   0.00   1.50
 8.485281 |  18.00  18.00   0.00
 8.944272 |  18.00   0.00   6.00
 9.380832 |  12.00  12.00   0.00
 9.797959 |  18.00   0.00   6.00

Source code
===========
.. currentmodule:: debyetools.pairanalysis

.. automodule:: debyetools.pairanalysis
    :members:
