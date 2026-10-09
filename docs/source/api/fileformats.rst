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
the formula, the cell and the fractional basis. Example: ``debyetools/examples/Al_fcc/CONTCAR``.

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
reference cell (V = V\ :sub:`ref` (1 + d)\ :sup:`3`), followed by the last OSZICAR line of that run. The energy of
the cell (eV) is the value after ``E0=``, the energy extrapolated to zero smearing (σ → 0). The value after ``F=``
(VASP's free energy TOTEN, E − σS of the smeared electrons) contains an electronic entropy at the artificial
temperature σ/k\ :sub:`B`; ``nDeb`` adds the electronic free energy separately from the DOS, so it is not used by
default. ``load_V_E(..., energy='F')`` reads it and reproduces the results of debyetools 2.8.3 and earlier. A line
without a usable ``E0=`` value (no label, or ``E0= 0`` written as a placeholder) is read from ``F=``, and a line
without the requested label is read positionally (column 4); both give a warning. Duplicate lines are read once.
Example: ``debyetools/examples/Al_fcc/SUMMARY`` (Fermi smearing, σ = 0.1 eV):

.. code-block:: text

    -0.10 1 F= -.12843002E+02 E0= -.12831042E+02 d E =-.239200E-01 mag= 0.0024
    -0.09 1 F= -.13305793E+02 E0= -.13294142E+02 d E =-.233025E-01 mag= 0.0032
    -0.08 1 F= -.13699350E+02 E0= -.13688341E+02 d E =-.220184E-01 mag= 0.0056
    -0.07 1 F= -.14029281E+02 E0= -.14019019E+02 d E =-.205240E-01 mag= 0.0088
    -0.06 1 F= -.14300833E+02 E0= -.14291255E+02 d E =-.191560E-01 mag= 0.0115
    -0.05 1 F= -.14518966E+02 E0= -.14509928E+02 d E =-.180763E-01 mag= 0.0134
    -0.04 1 F= -.14688294E+02 E0= -.14679638E+02 d E =-.173103E-01 mag= 0.0146
    -0.03 1 F= -.14813193E+02 E0= -.14804784E+02 d E =-.168179E-01 mag= 0.0152
    -0.02 1 F= -.14897766E+02 E0= -.14889494E+02 d E =-.165438E-01 mag= 0.0155
    -0.01 1 F= -.14945857E+02 E0= -.14937636E+02 d E =-.164427E-01 mag= 0.0156
    -0.00 1 F= -.14961079E+02 E0= -.14952833E+02 d E =-.164908E-01 mag= 0.0156
    0.01 1 F= -.14946763E+02 E0= -.14938421E+02 d E =-.166842E-01 mag= 0.0067
    0.02 1 F= -.14906095E+02 E0= -.14897561E+02 d E =-.170675E-01 mag= 0.0067
    0.03 1 F= -.14841981E+02 E0= -.14833126E+02 d E =-.177092E-01 mag= 0.0068
    0.04 1 F= -.14757176E+02 E0= -.14747813E+02 d E =-.187255E-01 mag= 0.0072
    0.05 1 F= -.14654247E+02 E0= -.14644119E+02 d E =-.202543E-01 mag= 0.0082
    0.06 1 F= -.14535630E+02 E0= -.14524435E+02 d E =-.223900E-01 mag= 0.0100
    0.07 1 F= -.14403657E+02 E0= -.14391123E+02 d E =-.250677E-01 mag= 0.0124
    0.08 1 F= -.14260533E+02 E0= -.14246556E+02 d E =-.279546E-01 mag= 0.0143
    0.09 1 F= -.14108304E+02 E0= -.14093072E+02 d E =-.304643E-01 mag= 0.0145
    0.10 1 F= -.13948766E+02 E0= -.13932791E+02 d E =-.319510E-01 mag= 0.0140

Electronic DOS (DOSCAR)
=======================

One DOSCAR per volume of the series, in the same order as the volumes (``list_filetags`` gives the file-name tags in
that order). Line 2 starts with the volume per atom in Å\ :sup:`3` (the GUI uses it to pair each file with its
volume); line 6 holds E\ :sub:`max`, E\ :sub:`min`, the number of points NEDOS and the Fermi energy. Only the
total-DOS block (NEDOS lines after line 6) is read: for spin-polarised calculations (ISPIN = 2: energy, DOS up,
DOS down, integrated up, integrated down) the two spins are summed, for ISPIN = 1 the DOS column is used; the DOS is
divided by the number of atoms (line 1). Projected blocks, if present, are ignored. Example:
``debyetools/examples/Al_fcc/DOSCAR.EvV.11`` (d = 0, ISPIN = 2; first rows, rows around E\ :sub:`F` and last row):

.. code-block:: text

       4   4   1   0
      0.1648104E+02  0.4039692E-09  0.4039692E-09  0.4039692E-09  0.5000000E-15
      1.000000000000000E-004
      CAR
     unknown system
         18.69614174     -3.97184732  301      7.92448980      1.00000000
         -3.972  0.0000E+00  0.0000E+00  0.0000E+00  0.0000E+00
         -3.896  0.0000E+00  0.0000E+00  0.0000E+00  0.0000E+00
         .
         .
         .
          7.816  0.8870E+00  0.8872E+00  0.5911E+01  0.5911E+01
          7.891  0.7441E+00  0.7358E+00  0.5968E+01  0.5966E+01
          7.967  0.1080E+01  0.1073E+01  0.6049E+01  0.6047E+01
          8.042  0.9221E+00  0.9332E+00  0.6119E+01  0.6118E+01
         .
         .
         .
         18.696  0.0000E+00  0.0000E+00  0.1200E+02  0.1200E+02

Elastic moduli (OUTCAR)
=======================

The OUTCAR of an ``IBRION = 6`` calculation with ``ISIF >= 3``. ``load_EM`` returns the 6x6 matrix in kBar, in
VASP order (XX, YY, ZZ, XY, YZ, ZX): by default the relaxed-ion moduli (block ``TOTAL ELASTIC MODULI``, or
``SYMMETRIZED ELASTIC MODULI`` + ``ELASTIC MODULI CONTR FROM IONIC RELAXATION`` when it is absent), or the
clamped-ion moduli (``SYMMETRIZED ELASTIC MODULI``) with ``block='clamped'``. The Poisson's ratio and the
Voigt-Reuss-Hill averages do not depend on the order. Example: the last two blocks of
``debyetools/examples/Al_fcc/OUTCAR_elastic``:

.. code-block:: text

     ELASTIC MODULI CONTR FROM IONIC RELAXATION (kBar)
     Direction    XX          YY          ZZ          XY          YZ          ZX
     --------------------------------------------------------------------------------
     XX          -0.0000      0.0000      0.0000     -0.0000      0.0000     -0.0000
     YY           0.0000     -0.0000      0.0000      0.0000     -0.0000     -0.0000
     ZZ           0.0000      0.0000     -0.0000     -0.0000      0.0000     -0.0000
     XY          -0.0000      0.0000      0.0000     -0.0000      0.0000     -0.0000
     YZ           0.0000     -0.0000     -0.0000      0.0000     -0.0000     -0.0000
     ZX           0.0000     -0.0000     -0.0000     -0.0000      0.0000     -0.0000
     --------------------------------------------------------------------------------


     TOTAL ELASTIC MODULI (kBar)
     Direction    XX          YY          ZZ          XY          YZ          ZX
     --------------------------------------------------------------------------------
     XX         969.7070    685.3121    685.3121     -0.0000      0.0000     -0.0000
     YY         685.3121    969.7070    685.3121      0.0000      0.0000     -0.0000
     ZZ         685.3121    685.3121    969.7070     -0.0000     -0.0000     -0.0000
     XY          -0.0000      0.0000      0.0000    453.2428      0.0000     -0.0000
     YZ           0.0000      0.0000     -0.0000      0.0000    453.2428     -0.0000
     ZX          -0.0000     -0.0000     -0.0000     -0.0000      0.0000    453.2428
     --------------------------------------------------------------------------------

Direct inputs
=============

Instead of files, the data can be entered directly as numpy arrays (SI per mol-atom) or, in the GUI, as plain text.

In the EOS-fit dialog of the GUI the energy curve is entered in Å\ :sup:`3` and eV per atom (option "eV and A^3
(per at)", default) or in m\ :sup:`3` and J per mol-atom (option "J and m^3 (per mol-at)"); for example Al\ :sub:`3`\ Li L1\ :sub:`2`
as pasted by **load E(V) ...** from ``debyetools/examples/Al3Li_L12`` (``E0=`` energies):

.. code-block:: text

    #V	E
    1.188839e+01	-2.970830e+00
    1.228909e+01	-3.060906e+00
    1.269870e+01	-3.137254e+00
    1.311730e+01	-3.201375e+00
    1.354501e+01	-3.254179e+00
    1.398191e+01	-3.296948e+00
    1.442811e+01	-3.330094e+00
    1.488370e+01	-3.354793e+00
    1.534878e+01	-3.371532e+00
    1.582345e+01	-3.380978e+00
    1.630781e+01	-3.383945e+00
    1.680195e+01	-3.380984e+00
    1.730598e+01	-3.372775e+00
    1.781999e+01	-3.359778e+00
    1.834407e+01	-3.342554e+00
    1.887833e+01	-3.321314e+00
    1.942286e+01	-3.296706e+00
    1.997777e+01	-3.269100e+00
    2.054315e+01	-3.239036e+00
    2.111909e+01	-3.206765e+00
    2.170570e+01	-3.172441e+00

The elastic constants are entered in GPa in Voigt order (XX, YY, ZZ, YZ, ZX, XY), as pasted by the GUI when an
OUTCAR is loaded (which converts from the VASP order); for Al\ :sub:`3`\ Li L1\ :sub:`2`
(``debyetools/examples/Al3Li_L12/OUTCAR_elastic``):

.. code-block:: text

    # GPa, Voigt order: XX YY ZZ YZ ZX XY
    122.26 35.00 35.00 0.00 0.00 -0.00
    35.00 122.22 34.95 0.00 -0.00 -0.00
    35.00 34.95 122.22 0.00 0.00 0.00
    0.00 0.00 0.00 41.39 0.00 0.00
    0.00 -0.00 0.00 0.00 41.47 0.00
    -0.00 -0.00 0.00 0.00 0.00 41.47
