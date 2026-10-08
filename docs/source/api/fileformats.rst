.. _fileformats:

==================
Input file formats
==================

.. contents:: Table of contents
   :local:
   :backlinks: none
   :depth: 3

Files and names
===============

``debyetools`` reads the following VASP results. The file names are free: every loader takes the path, so the
names below are only the conventions of the example data.

=========================  ===========================  ==========================  =============================
Content                    Loader                       ``tests/inpt_files``        ``debyetools/examples``
=========================  ===========================  ==========================  =============================
Reference structure        ``load_V_E``, ``load_cell``  ``CONTCAR.5``               ``CONTCAR``
Energy-volume series       ``load_V_E``                 ``SUMMARY.fcc``             ``SUMMARY``
Electronic DOS per volume  ``load_doscar``              ``DOSCAR.EvV.<tag>``        ``DOSCAR.EvV.01`` … ``.21``
Elastic moduli             ``load_EM``                  ``OUTCAR.eps``              ``OUTCAR_elastic``
=========================  ===========================  ==========================  =============================

A convenient layout is one folder per compound named by the formula and the space group, e.g. ``Al2O3_R3c``:

.. code-block:: text

    Al_fcc/
      CONTCAR.5
      SUMMARY.fcc
      DOSCAR.EvV.-0.10 … DOSCAR.EvV.-0.01, DOSCAR.EvV.-0.00, DOSCAR.EvV.0.01 … DOSCAR.EvV.0.10
      OUTCAR.eps

``load_V_E`` returns the volumes and energies per atom: in Å\ :sup:`3` and eV with the default
``units='eV/atom'``, in m\ :sup:`3`/mol-at and J/mol-at with ``units='J/mol'`` (the units ``nDeb`` needs).

Reference structure (CONTCAR)
=============================

The relaxed structure (VASP 5 format with the element line). Its cell volume divided by the number of atoms is the
reference volume of the energy-volume series (strain d = 0); for the Morse and EAM potentials ``load_cell`` returns
the formula, the cell and the fractional basis.

.. code-block:: text

    Al4
       1.00000000000000
         4.0396918604376202    0.0000000000000000    0.0000000000000000
         0.0000000000000000    4.0396918604376202    0.0000000000000000
         0.0000000000000000    0.0000000000000000    4.0396918604376202
       Al
         4
    Direct
      0.0000000000000000  0.0000000000000000  0.0000000000000000
      0.0000000000000000  0.5000000000000000  0.5000000000000000
      0.5000000000000000  0.0000000000000000  0.5000000000000000
      0.5000000000000000  0.5000000000000000  0.0000000000000000

Energy-volume series (SUMMARY)
==============================

One line per fixed-volume calculation of the same cell: column 1 is the isotropic linear strain d relative to the
reference cell (V = V\ :sub:`ref` (1 + d)\ :sup:`3`) and column 4 the energy of the cell in eV (the value after
``F=``, VASP's free energy TOTEN). Duplicate lines are read once.

.. code-block:: text

    -0.10 1 F= -.12910797E+02 E0= -.12906918E+02 d E =-.775954E-02 mag= -0.0007
    -0.09 1 F= -.13370262E+02 E0= -.13366237E+02 d E =-.804932E-02 mag= -0.0011
    -0.08 1 F= -.13758391E+02 E0= -.13754102E+02 d E =-.857638E-02 mag= -0.0010
    -0.07 1 F= -.14083100E+02 E0= -.14078383E+02 d E =-.943565E-02 mag= -0.0003
    -0.06 1 F= -.14349565E+02 E0= -.14344316E+02 d E =-.104987E-01 mag= 0.0009
    -0.05 1 F= -.14563748E+02 E0= -.14558028E+02 d E =-.114391E-01 mag= 0.0019
    -0.04 1 F= -.14729909E+02 E0= -.14723867E+02 d E =-.120830E-01 mag= 0.0026
    -0.03 1 F= -.14853318E+02 E0= -.14847102E+02 d E =-.124328E-01 mag= 0.0029
    -0.02 1 F= -.14936018E+02 E0= -.14929721E+02 d E =-.125950E-01 mag= 0.0028
    -0.01 1 F= -.14983118E+02 E0= -.14976823E+02 d E =-.125893E-01 mag= 0.0022
    -0.00 1 F= -.14997956E+02 E0= -.14991733E+02 d E =-.124452E-01 mag= 0.0010
    0.01 1 F= -.14984456E+02 E0= -.14978268E+02 d E =-.123746E-01 mag= -0.0002
    0.02 1 F= -.14945044E+02 E0= -.14938772E+02 d E =-.125429E-01 mag= -0.0007
    0.03 1 F= -.14882846E+02 E0= -.14876412E+02 d E =-.128695E-01 mag= -0.0007
    0.04 1 F= -.14799945E+02 E0= -.14793346E+02 d E =-.131984E-01 mag= -0.0006
    0.05 1 F= -.14698295E+02 E0= -.14691567E+02 d E =-.134551E-01 mag= -0.0005
    0.06 1 F= -.14581670E+02 E0= -.14574842E+02 d E =-.136561E-01 mag= -0.0004
    0.07 1 F= -.14451232E+02 E0= -.14444380E+02 d E =-.137049E-01 mag= -0.0006
    0.08 1 F= -.14310295E+02 E0= -.14303519E+02 d E =-.135523E-01 mag= -0.0012
    0.09 1 F= -.14158570E+02 E0= -.14151879E+02 d E =-.133818E-01 mag= -0.0015
    0.10 1 F= -.13997863E+02 E0= -.13991236E+02 d E =-.132555E-01 mag= -0.0016

Electronic DOS (DOSCAR)
=======================

One DOSCAR per volume of the series, in the same order as the volumes (``list_filetags`` gives the file-name tags in
that order). Line 2 starts with the volume per atom in Å\ :sup:`3` (the GUI uses it to pair each file with its
volume); line 6 holds E\ :sub:`max`, E\ :sub:`min`, the number of points NEDOS and the Fermi energy. Only the
total-DOS block (NEDOS lines after line 6) is read: for spin-polarised calculations (ISPIN = 2: energy, DOS up,
DOS down, integrated up, integrated down) the two spins are summed, for ISPIN = 1 the DOS column is used; the DOS is
divided by the number of atoms (line 1). Projected blocks, if present, are ignored.

.. code-block:: text

       4   4   1   0
      0.1599154E+02  0.3999295E-09  0.3999295E-09  0.3999295E-09  0.5000000E-15
      1.00000000000000E-004
      CAR
     unknown system
         20.23257380     -4.13078501  301      8.31659488      1.00000000
         -4.131  0.0000E+00  0.0000E+00  0.0000E+00  0.0000E+00
         -4.050  0.0000E+00  0.0000E+00  0.0000E+00  0.0000E+00
         .
         .
         .
         -3.481  0.5925E-06  0.5691E-06  0.4812E-07  0.4622E-07
         .
         .
         .
         19.339  0.3717E-02  0.3257E-02  0.1200E+02  0.1200E+02

Elastic moduli (OUTCAR)
=======================

The OUTCAR of an ``IBRION = 6`` calculation with ``ISIF >= 3``. ``load_EM`` returns the 6x6 matrix in kBar, in
VASP order (XX, YY, ZZ, XY, YZ, ZX): by default the relaxed-ion moduli (block ``TOTAL ELASTIC MODULI``, or
``SYMMETRIZED ELASTIC MODULI`` + ``ELASTIC MODULI CONTR FROM IONIC RELAXATION`` when it is absent), or the
clamped-ion moduli (``SYMMETRIZED ELASTIC MODULI``) with ``block='clamped'``. The Poisson's ratio and the
Voigt-Reuss-Hill averages do not depend on the order.

.. code-block:: text

     ELASTIC MODULI CONTR FROM IONIC RELAXATION (kBar)
     Direction    XX          YY          ZZ          XY          YZ          ZX
     --------------------------------------------------------------------------------
     XX           0.0000      0.0000      0.0000      0.0000      0.0000     -0.0000
     YY           0.0000      0.0000      0.0000     -0.0000      0.0000     -0.0000
     ZZ           0.0000      0.0000     -0.0000      0.0000      0.0000     -0.0000
     XY           0.0000     -0.0000      0.0000      0.0000     -0.0000     -0.0000
     YZ           0.0000      0.0000      0.0000     -0.0000      0.0000     -0.0000
     ZX          -0.0000     -0.0000     -0.0000     -0.0000     -0.0000      0.0000
     --------------------------------------------------------------------------------


     TOTAL ELASTIC MODULI (kBar)
     Direction    XX          YY          ZZ          XY          YZ          ZX
     --------------------------------------------------------------------------------
     XX        4520    1500    1070     200.0000     -0.0000      0.0000
     YY        1500    4520    1070    -200.0000     -0.0000      0.0000
     ZZ        1070    1070    4540    -0.0000      0.0000      0.0000
     XY        200     -200   -0       1320        -0.0000     -0.0000
     YZ        -0     -0       0      -0           1320     200
     ZX         0      0       0      -0           200    1510
     --------------------------------------------------------------------------------

Direct inputs
=============

Instead of files, the data can be entered directly as numpy arrays (SI per mol-atom) or, in the GUI, as plain text.

In the EOS-fit dialog of the GUI the energy curve is entered in Å\ :sup:`3` and eV per atom (option "eV and A^3
(per at)", default) or in m\ :sup:`3` and J per mol-atom (option "J and m^3 (per mol-at)"); for example Al\ :sub:`3`\ Li L1\ :sub:`2`:

.. code-block:: text

    #V	E
    1.188839e+01	-2.971644e+00
    1.228909e+01	-3.061733e+00
    1.269870e+01	-3.138113e+00
    1.311730e+01	-3.202274e+00
    1.354501e+01	-3.255126e+00
    1.398191e+01	-3.297945e+00
    1.442811e+01	-3.331133e+00
    1.488370e+01	-3.355852e+00
    1.534878e+01	-3.372588e+00
    1.582345e+01	-3.382024e+00
    1.630781e+01	-3.384997e+00
    1.680195e+01	-3.382070e+00
    1.730598e+01	-3.373913e+00
    1.781999e+01	-3.360960e+00
    1.834407e+01	-3.343770e+00
    1.887833e+01	-3.322563e+00
    1.942286e+01	-3.298003e+00
    1.997777e+01	-3.270464e+00
    2.054315e+01	-3.240472e+00
    2.111909e+01	-3.208295e+00
    2.170570e+01	-3.174068e+00

The elastic constants are entered in GPa in Voigt order (XX, YY, ZZ, YZ, ZX, XY), as pasted by the GUI when an
OUTCAR is loaded (which converts from the VASP order); for Al\ :sub:`3`\ Li L1\ :sub:`2`:

.. code-block:: text

    # GPa, Voigt order: XX YY ZZ YZ ZX XY
    122.26  35.00  35.00 -0.00  0.00  0.00
     35.00 122.22  34.95 -0.00  0.00 -0.00
     35.00  34.95 122.22  0.00  0.00  0.00
     -0.00  -0.00   0.00 41.47  0.00  0.00
     0.00    0.00   0.00  0.00 41.39  0.00
     0.00   -0.00   0.00  0.00  0.00 41.47
