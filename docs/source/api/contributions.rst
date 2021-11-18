================================
Contributions to the free energy
================================

Anharmonicity
=============

The anharmonicity can be included in the calculations as an excess contribution which is called just 'anharmonicity'.
The temperature dependence of phonon frequencies con be introduced usin what its called 'intrinsic anharmonicity'.

Source code
-----------

. currentmodule:: debyetools.anharmonicity

.. autoclass:: debyetools.anharmonicity.Anharmonicity
  :members:

.. autoclass:: debyetools.anharmonicity.intAnharmonicity
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

In order to take the electronic contribution intro account an approximation of the electronic DOS evaluated at the volume dependent Fermi level is implemented. The parameters can be entered manually or fitted to DOS data from DFT calculations.

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
