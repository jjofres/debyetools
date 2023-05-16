.. _thermoprops:

========================
Thermodynamic Properties
========================

.. contents:: Table of contents
   :local:
   :backlinks: none
   :depth: 3

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

Two description of the internal energy through inter-atomic potentials has been included as well:

- Morse
- EAM

The parameters can be entered by the user or fitted if there is data available.

Example
-------

.. code-block:: python

>>> import numpy as np
>>> import debyetools.potentials as potentials
>>> V_data = np.array([11.89,12.29,12.70,13.12,13.55,13.98,14.43,14.88,
... 15.35,15.82,16.31,16.80,17.31,17.82,18.34,18.88,19.42,19.98,20.54,
... 21.12,21.71])*(1E-30*6.02E+23)
>>> E_data = np.array([-2.97,-3.06,-3.14,-3.20,-3.26,-3.30,-3.33,-3.36,
... -3.37,-3.38,-3.38,-3.38,-3.37,-3.36,-3.34,-3.32,-3.30,-3.27,-3.24,
... -3.21,-3.17])*(1.60218E-19 * 6.02214E+23)
>>> params_initial_guess = [-3e5, 1e-5, 7e10, 4]
>>> Birch_Murnaghan = potentials.BM()
>>> Birch_Murnaghan.fitEOS(V_data, E_data, params_initial_guess)
array([-3.26551e+05,9.82096e-06,6.31727e+10,4.31057e+00])

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

.. code-block:: python

>>> from debyetools.poisson import poisson_ratio
>>> EM = EM = load_EM(folder_name+'/OUTCAR.eps')
>>> nu = poisson_ratio(EM)

Source Code
------

.. automodule:: debyetools.poisson
    :members:

Thermodynamic Properties
========================

The thermodynamic properties are calculated by first creating the instance of a ``nDeb`` object.
Once the parametrization is complete and the temperature and volumes are know (this can be done using the ``nDeb.min_F`` method), there is just an evaluation  of the thermodynamic properties left using ``nDeb.eval_tprops``.

Example: Minimization of the free energy.
-----------------------------------------

.. code-block:: python

>>> from debyetools.ndeb import nDeb
>>> from debyetools import potentials
>>> from debyetools.aux_functions import gen_Ts,load_V_E
>>> m = 0.021971375
>>> nu = poisson_ratio (EM)
>>> p_electronic = fit_electronic(V_data, p_el_inittial, E, N, Ef)
>>> p_defects = [8.46, 1.69, 933, 0.1]
>>> p_anh, p_intanh = [0,0,0], [0, 1]
>>> V_data, E_data = load_V_E('/path/to/SUMMARY', '/path/to/CONTCAR')
>>> eos = potentials.BM()
>>> peos = eos.fitEOS(V_data, E_data, params_initial_guess)
>>> ndeb = nDeb (nu , m, p_intanh , eos , p_electronic , p_defects , p_anh )
>>> T = gen_Ts ( T_initial , T_final , 10 )
>>> T, V = ndeb.min_G (T,  1e-5, P=0)
>>> V
array([9.98852539e-06, 9.99974297e-06, 1.00578469e-05, 1.01135875e-05,
       1.01419825e-05, 1.02392921e-05, 1.03467847e-05, 1.04650048e-05,
       1.05953063e-05, 1.07396467e-05, 1.09045695e-05, 1.10973163e-05])

Example: Evaluation of the thermodynamic properties:
----------------------------------------------------

.. code-block:: python

>>> trprops_dict=ndeb.eval_props(T,V)
>>> tprops_dict['Cp']
array([4.02097531e-05, 9.68739597e+00, 1.96115210e+01, 2.25070513e+01,
       2.34086394e+01, 2.54037595e+01, 2.68478029e+01, 2.82106379e+01,
       2.98214145e+01, 3.20143195e+01, 3.51848547e+01, 3.98791392e+01])

Source code
-----------

.. currentmodule:: debyetools.ndeb

.. autoclass:: debyetools.ndeb.nDeb
  :members:
