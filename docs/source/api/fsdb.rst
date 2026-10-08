==========================================
FactSage compound database parametrization
==========================================

The calculated thermodynamic properties for each EOS selected are used to fit the models for heat capacity,
thermal expansion, bulk modulus and its pressure derivative.
The resulting parameters can be used in FactSage as a compound database.

Example
-------

``fit_FS`` fits, between ``T_from`` and ``T_to``, the heat capacity
:math:`C_p=c_0+c_1T+c_2T^{-2}+c_3T^2+c_4T^{-1/2}+c_5T^{-3}` (``'Cp'``; :math:`c_5=0` unless ``cp_T3=True``),
the thermal expansion :math:`\alpha=a_0+a_1T+a_2T^{-1}+a_3T^{-2}` (``'a'``), the inverse bulk modulus
(``'1/Ks'``, a cubic in T) and its pressure derivative (``'Ksp'``, linear in T). Values per mol-atom; multiply
by the number of atoms of the formula for a FactSage compound entry. Example for Al fcc (BM, P = 0), as in the
:ref:`thermodynamic properties example <thermoprops>`:

>>> import os
>>> import debyetools
>>> import debyetools.potentials as potentials
>>> from debyetools.aux_functions import load_V_E, load_EM, gen_Ts
>>> from debyetools.poisson import poisson_ratio
>>> from debyetools.ndeb import nDeb
>>> folder = os.path.join(os.path.dirname(debyetools.__file__), 'examples', 'Al_fcc')
>>> V, E = load_V_E(folder + '/SUMMARY', folder + '/CONTCAR', units='J/mol')
>>> eos = potentials.BM()
>>> p_EOS = eos.fitEOS(V, E)
>>> nu = poisson_ratio(load_EM(folder + '/OUTCAR_elastic'))
>>> ndeb = nDeb(nu, 0.0269815385, (0, 1), eos, (0, 0, 0, 0), (1e10, 0, 933, 0.1), (0, 0, 0), mode='jjsl')
>>> T, V = ndeb.min_G(gen_Ts(0.1, 1000, 11), eos.V0, P=0)
>>> tprops = ndeb.eval_props(T, V, P=0)
>>> from debyetools.fs_compound_db import fit_FS
>>> FS_db_params = fit_FS(tprops, 298.15, 1000)
>>> for key, values in FS_db_params.items():
...     print(key, ', '.join('%.3e' % v for v in values))
Cp 5.253e+01, -2.276e-02, 1.237e+05, 1.526e-05, -4.250e+02, 0.000e+00
a -3.316e-05, 1.133e-07, 4.169e-02, -6.173e+00
1/Ks 1.302e-11, 2.531e-15, -1.887e-19, 1.168e-21
Ksp 4.788e+00, 1.024e-03

Source code
-----------

.. automodule:: debyetools.fs_compound_db
    :members:
