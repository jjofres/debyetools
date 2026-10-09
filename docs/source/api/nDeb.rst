.. _thermoprops:

========================
Thermodynamic Properties
========================

.. contents:: Table of contents
   :local:
   :backlinks: none
   :depth: 3

Units
=====

All inputs and outputs of the library are SI per mole of atoms: temperature in K, volume in
m\ :sup:`3`/mol-at, energies in J/mol-at, pressures and moduli in Pa, mass in kg/mol-at (mean atomic mass).
Results per formula unit are obtained by multiplying by the number of atoms in the formula. The VASP loaders
convert to these units (``load_V_E(..., units='J/mol')``); ``debyetools.constants`` holds the constants and the
conversion factors used everywhere (e.g. ``EV_ATOM_TO_J_MOL``, ``A3_ATOM_TO_M3_MOL``).

EOS parametrization
===================

The EOS's
----------

The EOS implemented are:

- Third order Birch-Murnaghan (``BM``; ``BM3`` is a deprecated alias)
- Rose-Vinet (``RV``)
- Mie-Gruneisen (``MG``)
- Tight-binding second-moment-approximation (``TB``)
- Murnaghan (``MU``)
- Poirier-Tarantola (``PT``)

Two descriptions of the internal energy through inter-atomic potentials have been included as well; they are
built from the crystal structure (formula, cell, basis, cut-off radius and number of neighbour shells, see
:ref:`pair analysis <pairanalysis>`):

- Morse (``MP``): three parameters (D, a, r0) per pair type
- EAM (``EAM``): six parameters per pair type and four per element type

The parameters can be entered by the user (``fit=False``) or fitted to energy-volume data. ``fitEOS`` returns
the parameters and also stores them in ``pEOS``; ``V0`` is the equilibrium volume. Each fit is checked (rms below
``rel_tol`` times the energy range of the data, a minimum with a positive bulk modulus near the data); if it is not
acceptable other starting points are tried, up to ``max_starts``. When none is acceptable ``EOSFitError`` is raised
(``on_failure='raise'``, default) or the best attempt is kept with a warning (``on_failure='warn'``). The analytic EOS
need no initial parameters (the start is taken from the data); ``fit_info`` records the accepted start and all
attempts.

Example
-------

E(V) data in Å\ :sup:`3` and eV per atom converted to SI per mol-atom:

>>> import numpy as np
>>> import debyetools.potentials as potentials
>>> from debyetools.constants import A3_ATOM_TO_M3_MOL, EV_ATOM_TO_J_MOL
>>> V_data = np.array([11.89,12.29,12.70,13.12,13.55,13.98,14.43,14.88,15.35,15.82,16.31,16.80,17.31,17.82,18.34,18.88,19.42,19.98,20.54,21.12,21.71]) * A3_ATOM_TO_M3_MOL
>>> E_data = np.array([-2.97,-3.06,-3.14,-3.20,-3.26,-3.30,-3.33,-3.36,-3.37,-3.38,-3.38,-3.38,-3.37,-3.36,-3.34,-3.32,-3.30,-3.27,-3.24,-3.21,-3.17]) * EV_ATOM_TO_J_MOL
>>> eos = potentials.BM()
>>> p_EOS = eos.fitEOS(V_data, E_data)
>>> print('E0 = %.4e J/mol-at, V0 = %.4e m3/mol-at, K0 = %.3e Pa, K0p = %.2f' % tuple(p_EOS))
E0 = -3.2641e+05 J/mol-at, V0 = 9.8032e-06 m3/mol-at, K0 = 6.299e+10 Pa, K0p = 4.51
>>> eos.fit_info['accepted']
'from data'

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
.. autoclass:: debyetools.potentials.MP
  :members: fitEOS, E0
.. autoclass:: debyetools.potentials.EAM
  :members: fitEOS, E0
.. autoclass:: debyetools.potentials.EOSFitError

Poisson's ratio
===============

The Poisson's ratio used in the calculation of the Debye temperature can be entered manually by the user or
calculated from the elastic moduli matrix (Voigt-Reuss-Hill averages). ``load_EM`` reads a VASP ``IBRION = 6``
OUTCAR and returns the matrix in kBar, in VASP order (XX, YY, ZZ, XY, YZ, ZX); by default the relaxed-ion moduli
(``block='relaxed'``), or the clamped-ion ones with ``block='clamped'``. With ``quiet=True``, ``poisson_ratio``
returns all the averages.

Example
-------

>>> import os
>>> import debyetools
>>> from debyetools.aux_functions import load_EM
>>> from debyetools.poisson import poisson_ratio
>>> folder = os.path.join(os.path.dirname(debyetools.__file__), 'examples', 'Al_fcc')
>>> EM = load_EM(folder + '/OUTCAR_elastic')
>>> print('%.4f' % poisson_ratio(EM))
0.3370
>>> B_R, B_V, B, G_R, G_V, G, A_U, nu = poisson_ratio(EM, quiet=True)
>>> print('B = %.1f GPa, G = %.1f GPa, A_U = %.2f' % (B, G, A_U))
B = 78.0 GPa, G = 28.5 GPa, A_U = 1.80

Source Code
-----------

.. automodule:: debyetools.poisson
    :members:

Thermodynamic Properties
========================

The thermodynamic properties are calculated by first creating an ``nDeb`` object with the parameters of every
contribution, F = E0 + F\ :sub:`vib` + F\ :sub:`el` + F\ :sub:`def` + F\ :sub:`anh` + F\ :sub:`xs`
(see :ref:`contributions <contributions>`). ``nDeb.min_G`` gives the equilibrium volume at each temperature and
pressure; ``nDeb.eval_props`` evaluates the properties at those (T, V). If no mechanically stable volume exists
at some temperature, ``min_G`` stops there with a warning and returns the stable part; ``nDeb.min_G_info`` holds
the status of every temperature.

Example: minimization of the Gibbs energy
-----------------------------------------

>>> from debyetools.aux_functions import load_V_E, gen_Ts
>>> from debyetools.ndeb import nDeb
>>> V, E = load_V_E(folder + '/SUMMARY', folder + '/CONTCAR', units='J/mol')
>>> eos = potentials.BM()
>>> p_EOS = eos.fitEOS(V, E)
>>> p_intanh, p_electronic, p_defects, p_anh = (0, 1), (0, 0, 0, 0), (1e10, 0, 933, 0.1), (0, 0, 0)
>>> ndeb = nDeb(poisson_ratio(EM), 0.0269815385, p_intanh, eos, p_electronic, p_defects, p_anh, mode='jjsl')
>>> T, V = ndeb.min_G(gen_Ts(0.1, 2500, 6), eos.V0, P=0)
>>> print(T)
[1.00000e-01 2.98150e+02 5.00080e+02 1.00006e+03 1.50004e+03]
>>> ndeb.min_G_info['status']
['ok', 'ok', 'ok', 'ok', 'ok', 'unstable', 'not computed']

Here the lattice has no stable volume at 2000 K with this EOS, so ``min_G`` stopped after 1500 K.

Example: evaluation of the thermodynamic properties
---------------------------------------------------

``eval_props`` returns a dictionary of arrays, for example ``'V'``, ``'tD'`` (Debye temperature, K), ``'g'``
(Grüneisen parameter), ``'Kt'`` and ``'Ks'`` (isothermal and adiabatic bulk moduli, Pa), ``'a'`` (volumetric
thermal expansion, 1/K), ``'Cv'``, ``'Cp'`` and ``'S'`` (J/mol-at/K), ``'E'``, ``'F'``, ``'G'`` (J/mol-at), and
the individual contributions (``'Fvib'``, ``'Fel'``, ``'Fdef'``, ``'Fa'``, ``'Fxs'``, …).

>>> tprops = ndeb.eval_props(T, V, P=0)
>>> i = list(T).index(298.15)
>>> print('tD = %.1f K, g = %.3f, Kt = %.3e Pa, a = %.3e 1/K, Cp = %.3f, S = %.3f J/mol-at/K'
...       % tuple(tprops[k][i] for k in ('tD', 'g', 'Kt', 'a', 'Cp', 'S')))
tD = 403.4 K, g = 2.184, Kt = 6.983e+10 Pa, a = 7.011e-05 1/K, Cp = 23.842, S = 26.820 J/mol-at/K

Source code
-----------

.. automodule:: debyetools.ndeb
  :members:
