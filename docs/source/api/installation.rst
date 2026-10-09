============
Installation
============

Source Code
===========

All the code is in ``debyetools`` repository on GitHub_.

Requirements
============

* Python_ 3.10, 3.11 or 3.12
* NumPy_ 1.26 or 2.x (base N-dimensional array package)
* SciPy_ 1.11 or newer (fundamental algorithms for scientific computing in Python)

For the graphical interface and plotting:

* Matplotlib_ (plots in the GUI and in the examples)
* PySide6_ (the GUI; PySide6 is the official Python module from the Qt for Python project)

Running the tests needs pytest_ (``python -m pytest`` from the repository folder); the GUI tests run headless
(``QT_QPA_PLATFORM=offscreen``) and are skipped when PySide6 cannot be loaded.

Installation using pip
======================

The simplest way to install ``debyetools`` is to use pip_ which will automatically get the source code from PyPI_::

    $ pip install --upgrade debyetools

Version 3.0.0 gives different results than 2.8.3 for the same inputs (corrected formulas and changed defaults);
the list of changes, and the arguments that restore the old behaviour where possible, are in the CHANGELOG_.

.. _Python: https://www.python.org/
.. _NumPy: https://docs.scipy.org/doc/numpy/reference/
.. _PyPI: https://pypi.org/project/debyetools/
.. _SciPy: https://scipy.org
.. _PIP: https://pip.pypa.io/en/stable/
.. _Matplotlib: https://matplotlib.org/
.. _PySide6: https://pypi.org/project/PySide6/
.. _pytest: https://docs.pytest.org/
.. _GitHub: https://github.com/jjofres/debyetools
.. _CHANGELOG: https://github.com/jjofres/debyetools/blob/main/CHANGELOG.md
