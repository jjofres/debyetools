.. Debye Tools documentation master file, created by
   sphinx-quickstart on Tue Nov  9 14:35:19 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Debye Tools's documentation!
=======================================

Debye tools is a set of tools written in Python_
for the calculation of thermodynamic properties.
The code is freely available under the GNU Affero General Public License.

.. _Python: https://www.python.org/

>>>  # Example: pair analysis
>>> from pairanalysis import PairAnalysisCalculator
>>> pa = PairAnalysisCalculator()
>>> primitive_cell = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
>>> basis_vectors = np.array([[0, 0, 0], [.5, .5, 0], [.5, 0, .5], [0, .5, .5]])
>>> pa.pair_analysis('AABA', np.array([1, 1, 1]), 2, np.array([0, 0, 0]), basis_vectors, primitive_cell)
(array([0.70710678, 1.        , 1.22474487, 1.41421356, 1.58113883,
       1.73205081, 1.87082869]), array([[ 6. ,  6. ,  0. ],
       [ 4.5,  0. ,  1.5],
       [12. , 12. ,  0. ],
       [ 9. ,  0. ,  3. ],
       [12. , 12. ,  0. ],
       [ 6. ,  0. ,  2. ],
       [28.5, 24. ,  1.5]]), ['A-A', 'A-B', 'B-B'])


.. toctree::
   :maxdepth: 2
   :caption: Python code:

   source/api/calculator

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

News
====

