.. _auxfunctions:

==============================
Input files, grids, constants
==============================

.. contents:: Table of contents
   :local:
   :backlinks: none
   :depth: 2

Loading VASP results
====================

``load_V_E`` (energy-volume curve from a SUMMARY file and the reference CONTCAR), ``load_doscar`` (total DOS of a
series of DOSCAR files), ``load_EM`` (elastic moduli from an ``IBRION = 6`` OUTCAR) and ``load_cell`` (formula,
cell and fractional basis of a CONTCAR, for the Morse and EAM potentials). File formats: :ref:`fileformats`.

Temperature and pressure grids
==============================

``gen_Ts`` (temperatures, 298.15 K added when missing) and ``gen_Ps`` (pressures).

Source code
-----------

.. automodule:: debyetools.aux_functions
    :members: load_V_E, load_doscar, load_EM, load_cell, gen_Ts, gen_Ps

Constants and unit conversions
==============================

``debyetools.constants`` (exact SI-2019 values):

.. literalinclude:: ../../../debyetools/constants.py
   :language: python
   :lines: 9-
