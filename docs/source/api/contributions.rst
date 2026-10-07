================================
Contributions to the free energy
================================

.. contents:: Table of contents
   :local:
   :backlinks: none
   :depth: 3

Anharmonicity
=============

The anharmonicity can be included in the calculations as an excess contribution which is called just 'anharmonicity'.
The temperature dependence of the phonon frequencies con be introduced using what its called 'intrinsic anharmonicity'.

Source code
-----------

.. automodule:: debyetools.anharmonicity
  :members:

Defects
=======

The defects due to mono-vacancies can be taken into account if the parameters are provided.

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

Vibrational
===========

The evaluation of the thermal behavior of compounds  are  calculating using the Debye approximation.
The mass of the compound and the Poisson's ration must be entered as input parameters. The information about the internal energy is passed as an ``potential.EOS`` object.

Source code
-----------

.. automodule:: debyetools.vibrational
  :members:
