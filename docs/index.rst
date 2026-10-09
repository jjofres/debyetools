.. Debye Tools documentation master file, created by
   sphinx-quickstart on Tue Nov  9 14:35:19 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==========================================
Welcome to ``debyetools``'s documentation!
==========================================

``debyetools`` is a set of tools written in Python_
for the calculation of thermodynamic and thermophysical properties. It's a library in The Python Package Index (PyPI_).
The software presented here is based in the Debye approximation of the quasiharmonic approximation (QHA) using the crystal internal energetics parametrized at ground-state, (go to :ref:`input file formats <fileformats>` to see how DFT calculations results can be used as inputs) to project the :ref:`thermodynamics properties <thermoprops>` at high temperatures.
How to cite ``debyetools`` and a first example are in the :ref:`overview <overview>`. We present here how each contribution to the free energy are considered and a description of the architecture of the calculation engine and of the :ref:`GUI`.

The code_ is freely available under the GNU Affero General Public License.


.. _PyPI: https://pypi.org/project/debyetools/
.. _Python: https://www.python.org/
.. _code: https://github.com/jjofres/debyetools

.. toctree::
   :maxdepth: 2
   :caption: Content:

   source/api/overview
   source/api/installation
   source/api/gui
   source/api/examples
   source/api/nDeb
   source/api/utilities
   source/api/contributions
   source/api/fsdb
   source/api/pairanalysis
   source/api/fileformats


.. only:: html

   .. rubric:: Indices

   * :ref:`genindex`
   * :ref:`modindex`
