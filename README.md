# debyetools

Implementation of a tool for calculating self-consistent thermodynamic properties that can take into account all kinds of contributions to the free energy including explicit anharmonicity. The software presented here is based in the Debye approximation within the QHA using the crystal internal energetics parametrized at ground-state to project the thermodynamics properties at high temperatures. 

Made by Javier Jofre: javier.jofre@polymtl.ca
If you use  ``debyetools`` in a publication, please refer to the `source code`.  If you use the implemented method for the calculation of the thermodynamic properties, please cite the following publication:

Jofre, J., Gheribi, A. E., & Harvey, J.-P. Development of a flexible quasi-harmonic-based approach for fast generation of self-consistent thermodynamic properties used in computational thermochemistry. Calphad 83 (2023) 102624. doi: https://doi.org/10.1016/j.calphad.2023.102624.

```
   @article{,
      author = {Javier Jofré and Aïmen E. Gheribi and Jean-Philippe Harvey},
      doi = {10.1016/j.calphad.2023.102624},
      issn = {03645916},
      journal = {Calphad},
      month = {12},
      pages = {102624},
      title = {Development of a flexible quasi-harmonic-based approach for fast generation of self-consistent thermodynamic properties used in computational thermochemistry},
      volume = {83},
      year = {2023},
   }
```

### Requirements
- Python 3.10 – 3.12
- numpy (1.26 or 2.x), scipy (≥ 1.11)
- for the graphical interface also: matplotlib, PySide6

### Installation
```
pip install --upgrade debyetools
```

Version 3.0.0 gives different results than 2.8.3 for the same inputs (corrected formulas and changed
defaults): see [CHANGELOG.md](CHANGELOG.md) before comparing with older results.

### Get started

Example input files (VASP outputs) are in `debyetools/examples` and `tests/inpt_files`.
The GUI can be launched from the debyetools repository main folder:

```
python dtgui.py
```

or inside Python:
```
from debyetools.tpropsgui.gui import dtgui
dtgui()
```

`debyetools` can also be used as a library. All inputs and outputs are SI per mole of atoms (V in m³/mol-at,
energies in J/mol-at, pressures in Pa, mass in kg/mol-at). Example: heat capacity of Al fcc with the third-order
Birch-Murnaghan EOS (parameters fitted to the VASP data in `debyetools/examples/Al_fcc`):

```Python
import numpy as np
import debyetools.potentials as potentials
from debyetools.ndeb import nDeb

# EOS parameters (E0 in J/mol-at, V0 in m^3/mol-at, K0 in Pa, K0'), used as given (fit=False)
# =========================
EOS_parameters = [-3.605783e+05, 9.931760e-06, 7.7683e+10, 4.5802]
EOS = potentials.BM()
EOS.fitEOS([EOS_parameters[1]], [EOS_parameters[0]], initial_parameters=EOS_parameters, fit=False)

# Other contributions
# =========================
p_electronic = [4.27703e+00, -6.12439e+05, 3.46101e+09, 1.95140e+15]  # N(E_F)(V) = q0 + q1 V + q2 V^2 + q3 V^3
mass = 0.0269815385                    # kg/mol-at
Tmelting = 933
p_defects = 8.46, 1.69, Tmelting, 0.1  # vacancies: E = 8.46 kB Tm, S = 1.69 kB
p_intanh = 0, 1                        # intrinsic anharmonicity (a0, m0): none
p_anh = 0, 0, 0                        # explicit anharmonicity (s0, s1, s2): none
poissonsratio = 0.337

# G minimization (Slater approximation for the Debye temperature)
# =========================
ndeb = nDeb(poissonsratio, mass, p_intanh, EOS, p_electronic, p_defects, p_anh, mode='jjsl')
T = np.arange(0.1, 1000, 10)
Pressure = 0
T, V = ndeb.min_G(T, EOS.V0, P=Pressure)   # starting volume: the EOS V0

# Evaluation of the thermodynamic properties
# =========================
tprops_dict = ndeb.eval_props(T, V, P=Pressure)
print('Cp(298.15 K) = %.2f J/mol-at/K' % np.interp(298.15, T, tprops_dict['Cp']))
```

To Do's:

- Improve error handling
- Improve Documentation
- Add handling of anisotropic materials
- Prediction of explicit anharmonicity parameters