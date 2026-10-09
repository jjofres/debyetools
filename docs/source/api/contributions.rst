..  _contributions:

================================
Contributions to the free energy
================================

.. contents:: Table of contents
   :local:
   :backlinks: none
   :depth: 3

Anharmonicity
=============

Two anharmonic terms are available. The explicit anharmonicity (``p_anh = (s0, s1, s2)`` in ``nDeb``) adds
:math:`F_{anh}=-\frac{1}{2}A(V)T^2` with :math:`A(V)=s_0+s_1V+s_2V^2`. The intrinsic anharmonicity
(``p_intanh = (a0, m0)``) makes the Debye temperature depend on temperature,
:math:`\theta_D(T,V)=\theta_D(V)\exp(a(V)T/2)` with :math:`a(V)=a_0(V/V_0)^{m_0}`; ``(0, 1)`` switches it off.

Source code
-----------

.. automodule:: debyetools.anharmonicity
  :members:

Defects
=======

The defects due to mono-vacancies can be taken into account if the parameters are provided
(``p_defects = (Evac00, Svac00, Tm, a)``: formation energy :math:`E_{vac}=Evac00\,k_BT_m`, entropy
:math:`S_{vac}=Svac00\,k_B`, melting temperature :math:`T_m` in K, and a dimensionless coefficient of the volume
dependence of :math:`E_{vac}`). A very large ``Evac00`` (e.g. ``1e10``) switches the term off.

Source code
-----------

.. automodule:: debyetools.defects
  :members:

Electronic Contribution
=======================

The electronic contribution uses the Sommerfeld expression :math:`F_{el}=-\frac{\pi^2}{6}N_A k_B^2 T^2 N(E_F)(V)`, with :math:`N(E_F)(V)=q_0+q_1V+q_2V^2+q_3V^3` the total electronic density of states at the Fermi level (both spins, states/eV/atom) and V in m\ :sup:`3`/mol-atom. The parameters can be entered manually or fitted with ``fit_electronic`` to DFT densities of states: by default N(E_F) is read from the total DOS at every volume (``load_doscar`` reads the total-DOS block of each VASP DOSCAR and sums the spin channels); with ``mode='scaling'`` a single DOS at V0 is extended with the free-electron law :math:`N(E_F)\propto (V/V_0)^{2/3}`.

Source code
-----------

.. automodule:: debyetools.electronic
    :members:

Excess contribution
===================

An excess term in the form of a FactSage-like polynomial (``xsparams`` in ``nDeb``, default all zero),
:math:`F_{xs}=A_0+A_1T+A_2T^2+A_3T^3+A_4T\ln T+A_5T^{-2}` in J/mol-at. Each coefficient is a number
(volume-independent, the usual case) or a sequence of polynomial coefficients in V (lowest order first), which
makes the term contribute to the pressure, bulk modulus and thermal expansion.

Source code
-----------

.. automodule:: debyetools.XS
    :members:

Vibrational
===========

The vibrational free energy is calculated with the Debye model. The mean atomic mass (kg/mol-at) and the
Poisson's ratio are input parameters; the internal energy is passed as an EOS object (``debyetools.potentials``).
The Debye temperature follows from the EOS and the Poisson's ratio; its volume dependence is set by ``mode``:
``'jjsl'`` (Slater, default), ``'jjdm'`` (Dugdale-MacDonald), ``'jjfv'`` (free volume), and ``'Sl'``, ``'DM'``,
``'VZ'``, ``'mfv'`` (Grüneisen parameter from the EOS with a fixed reference volume).

Source code
-----------

.. automodule:: debyetools.vibrational
  :members:
