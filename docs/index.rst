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

>>>  ########################################################################
>>>  # Example: heat capacity of Al fcc using 3rd order Birch-Murnaghan EOS #
>>>  ########################################################################
>>> from debyetools.ndeb import nDeb
>>> nu, m = 0.32, 0.026981500000000002
>>> Tmelting = 933
>>> p_EOS = [-3.617047894e+05, 9.929931142e-06
>>>          7.618619745e+10, 4.591924487e+00]
>>> p_intanh = 0, 1, p_EOS[1]
>>> p_electronic = [3.8027342892e-01, -1.8875015171e-02,
>>>                 5.3071034596e-04, -7.0100707467e-06]
>>> p_defects = 8.46, 1.69, Tmelting, 0.1, p_EOS[2],p_EOS[1]
>>> p_anh = 0,0,0
>>> EOS_name = 'BM'
>>> ndeb_BM = nDeb(nu, m, p_intanh, p_EOS, p_electronic,
>>>                p_defects,p_anh,EOS_name)
>>> T,V = 9.33000000000e+02,1.07790131286e-05
>>> ndeb_BM.eval_props(T,V)['Cp']
33.249439691599925

.. toctree::
   :maxdepth: 2
   :caption: Documentation:

   source/api/installation
   source/api/pairanalysis
   source/api/nDeb

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

News
====
