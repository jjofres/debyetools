=========================
Pair Analysis Calculation
=========================

A pair analysis calculator was build where the atom position can be read from a POSCAR file or eneterd manually. The neighbor list and binning are calculated to build up the pairs list.

Example
-------

>>> import numpy as np
>>> from debyetools.pairanalysis import pair_analysis
>>> formula = 'AABA'
>>> supcell_size = np.array([1,1,1])
>>> cutoff = 5
>>> center = np.array([0,0,0])
>>> basis_vectors = np.array([[0,0,0],[.5,.5,0],[.5,0,.5],[0,.5,.5]])
>>> primitive_cell =  np.array([[4, 0, 0], [0, 4, 0], [0, 0, 4]])
>>> distances, num_bonds_per_formula, combs_types = pair_analysis(formula, supcell_size, cutoff, center, basis_vectors, primitive_cell)
>>> print('distances  | # of pairs per type')
>>> print('           | ' + '  '.join(['%s' for _ in combs_types])%tuple(combs_types))
>>> for d, n in zip(distances, num_bonds_per_formula):
        print('%.6f  '%(d)+' | ' + ' '.join(['%.2f' for _ in n])%tuple(n))
distances  | # of pairs per type
           | A-A  A-B  B-B
2.828427   | 6.00 6.00 0.00
4.000000   | 4.50 0.00 1.50
4.898979   | 12.00 12.00 0.00

Source code
-----------
.. currentmodule:: debyetools.pairanalysis

.. automodule:: debyetools.pairanalysis
    :members:
