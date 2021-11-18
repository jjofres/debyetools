.. _thermoprops:

========================
Thermodynamic Properties
========================

EOS parametrization
===================

The EOS's
----------

The EOS implemented are:

- Rose-Vinet (RV)
- Tight-binding second-moment-approximation (TB-SMA)
- Third order Birch-Murnaghan (BM3)
- Mie-Gruneisen (MG)
- Murnaghan (Mu1)
- Poirier-Tarantola (PT)
- Fourth order Birch-Murnaghan (BM4)
- Second order Murnaghan (Mu2)

Two description of the internal energy through interatomic potentials has been included as well:

- Morse
- EAM

The parameters can be entered by the user or fitted if there is data available.

Example
-------

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

Source code
-----------

The following is the source for the description of the third order Birch-Murnaghan EOS:

.. currentmodule:: debyetools.potentials

.. autoclass:: debyetools.potentials.BM
  :members:

The other potentials are:

.. autoclass:: debyetools.potentials.RV
.. autoclass:: debyetools.potentials.TB
.. autoclass:: debyetools.potentials.MG
.. autoclass:: debyetools.potentials.MU
.. autoclass:: debyetools.potentials.PT
.. autoclass:: debyetools.potentials.BM4
.. autoclass:: debyetools.potentials.MU2
.. autoclass:: debyetools.potentials.MP
.. autoclass:: debyetools.potentials.EAM

Poisson's ratio
========================

The Poisson's ratio used in the calculation of the Debye temperature can entered manually by the user or calculated from the Elastic moduli matrix.

Example
-------

>>> from debyetools.poisson import poisson_ratio
>>>
>>> EM = EM = load_EM(folder_name+'/OUTCAR.eps')
>>> nu = poisson_ratio(EM)

.. automodule:: debyetools.poisson
    :members:

Thermodynamic Properties
========================

The thermodynamic properties are calculated by first creating the instance of a ``nDeb`` object.
Once the parametrization is complete and the temperature and volumes are know (this can be done using the ``nDeb.min_F`` method), there is just an evaluation  of the thermodynamic properties left using ``nDeb.eval_tprops``.

Example: Minimization of the free energy.
-----------------------------------------

>>> from debyetools.ndeb import nDeb
>>> from debyetools.aux_functions import gen_Ts
>>>
>>> m = 0.026981500000000002
>>> ndeb_Morse = nDeb(nu, m, p_intanh, eos_Morse, p_electronic, p_defects, p_anh)
>>> T_initial, T_final, number_Temps = 0.1, 1000, 10
>>> T = gen_Ts(T_initial, T_final, number_Temps)
>>>
>>> T, V = ndeb_Morse.min_F(T,ndeb_Morse.EOS.V0)

Example: Evaluation of the thermodynamic properties:
----------------------------------------------------

>>> tprops_dict = ndeb_Morse.eval_props(T, V)

Source code
-----------

.. currentmodule:: debyetools.ndeb

.. autoclass:: debyetools.ndeb.nDeb
  :members:
