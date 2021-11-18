====================================
FS compound database parametrization
====================================

The calculated thermodynamic properties for each EOS selected are used to fit the models for heat capacity, thermal expansion, bulk modulus and pressure derivative of the bulk modulus. The resulting parameters can be used in FactSage as a compound database.

Example
-------

>>> from debyetools.fs_compound_db import fit_FS
>>>
>>> T_from = 298.15
>>> T_to = 1000
>>> FS_db_params = fit_FS(tprops_dict, T_from, T_to)
>>> print(FS_db_params)
[ 1.11898466e+02 -8.11995443e-02  7.22119591e+05  4.29282477e-05
 -1.31482568e+03  1.00000000e+00]

Source code
-----------

.. automodule:: debyetools.fs_compound_db
    :members:
