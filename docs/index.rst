.. Debye Tools documentation master file, created by
   sphinx-quickstart on Tue Nov  9 14:35:19 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Debye Tools's documentation!
=======================================

Debye tools is a set of tools written in Python_
for the calculation of thermodynamic properties.
The software presented here is based in the Debye approximation of the QHA using the crystal internal energetics parametrized at ground-state to project the :ref:`thermodynamics properties <thermoprops>` at high temperatures.
We present here how each contribution to the free energy are considered and a description of the architecture of the calculation engine and of the :ref:`GUI`.

The code_ is freely available under the GNU Affero General Public License.


.. _Python: https://www.python.org/
.. _code: https://github.com/jjofres/debyetools

- Using ``debyetools`` through the GUI ``tProps``:

.. _tProps2:
.. figure::  ./source/api/images/tprops_gui.jpeg
   :align:   center

   tProps v0.0

- Using ``debyetools`` as a Python_ library. Example: Al fcc using Morse Potential:

EOS parametrization:

>>> import numpy as np
>>> from debyetools.aux_functions import load_doscar, load_V_E, load_EM, load_cell
>>> import debyetools.potentials as potentials
>>>
>>> folder_name = '../tests/inpt_files/Al_fcc'
>>>
>>> V_DFT, E_DFT = load_V_E(folder_name, folder_name + '/CONTCAR.5', units='J/mol')
>>> formula, primitive_cell, sbasis_vectors = load_cell(folder_name+'/CONTCAR.5')
>>> EOS_name = 'MP'
>>> cutoff = 5
>>> number_of_neighbor_levels = 3
>>>
>>> eos_Morse = getattr(potentials,EOS_name)(formula, primitive_cell, sbasis_vectors, cutoff, number_of_neighbor_levels, units='J/mol')
>>>
>>> initial_parameters = np.array([0.35, 1, 3.5])
>>> eos_Morse.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters)

Electronic Contribution:

>>> from debyetools.electronic import fit_electronic
>>>
>>> p_el_inittial = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
>>> E, N, Ef = load_doscar(folder_name+'/DOSCAR.EvV.')
>>> p_electronic = fit_electronic(V_DFT, p_el_inittial,E,N,Ef)

Poisson's ratio:

>>> from debyetools.poisson import poisson_ratio
>>>
>>> EM = EM = load_EM(folder_name+'/OUTCAR.eps')
>>> nu = poisson_ratio(EM)

Free energy minimization:

>>> from debyetools.ndeb import nDeb
>>> from debyetools.aux_functions import gen_Ts
>>>
>>> m = 0.026981500000000002
>>> ndeb_Morse = nDeb(nu, m, p_intanh, eos_Morse, p_electronic, p_defects, p_anh)
>>> T_initial, T_final, number_Temps = 0.1, 1000, 10
>>> T = gen_Ts(T_initial, T_final, number_Temps)
>>>
>>> T, V = ndeb_Morse.min_F(T,ndeb_Morse.EOS.V0)

Evaluation of the thermodynamic properties:

>>> tprops_dict = ndeb_Morse.eval_props(T, V)

FS compound database parameters:

>>> from debyetools.fs_compound_db import fit_FS
>>>
>>> T_from = 298.15
>>> T_to = 1000
>>> FS_db_params = fit_FS(tprops_dict,T_from, T_to)
>>> print(FS_db_params)
[ 1.11898466e+02 -8.11995443e-02  7.22119591e+05  4.29282477e-05
 -1.31482568e+03  1.00000000e+00]


.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   source/api/installation
   source/api/pairanalysis
   source/api/nDeb
   source/api/contributions
   source/api/fsdb
   source/api/gui
   source/api/plot

Indices
=======

* :ref:`genindex`
* :ref:`modindex`

News
====
