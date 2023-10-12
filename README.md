# debyetools

Implementation of a tool for calculating self-consistent thermodynamic properties that can take into account all kinds of contributions to the free energy inluding explicit anharmonicity. The software presented here is based in the Debye approximation within the QHA using the crystal internal energetics parametrized at ground-state to project the thermodynamics properties at high temperatures. 

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

### Requirements for Python module:
- numpy
- mpmath
- scipy

### Requirements for Interface:
For the interface it will also be necesary:
- matplotlib
- PySide6

### Installation
```
pip install --upgrade debyetools
```

### Get started

To start getting familiar with the interface you can download `examples input files`.
The GUI can be launched by executing the interface script from the debyetools repository main folder:

```
python interface.py
```

Or you can launch  inside python:
```
from debyetools.tpropsgui.gui import interface
interface()
```

Debye tools can also be used as a library. Example: heat capacity of Al fcc using 3rd order Birch-Murnaghan EOS

```Python
import numpy as np
import debyetools.potentials as potentials
from debyetools.ndeb import nDeb

# EOS parametrization
# =========================
EOS_parameters = [-3.607736520e+05, 9.929277050e-06, 7.729289055e+10, 4.604381753e+00]
EOS = potentials.BM()
EOS.fitEOS([0], [0], initial_parameters=EOS_parameters, fit=False)

# Other Contributions parametrization
# =========================
p_electronic = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
mass = 0.026981500000000002
Tmelting = 933
p_defects = 8.46, 1.69, Tmelting, 0.1
p_anharmonicity = 0, 1
p_XS = 0, 0, 0
poissonsratio = 0.37

# F minimization using Slater approximaiton
# =========================
ndeb = nDeb(poissonsratio, mass, p_anharmonicity, EOS, p_electronic, p_defects, p_XS, mode='jjsl')
T_initial, T_final= 0.1, 1000
T = np.arange(T_initial, T_final, 10)
Pressure = 0
T, V = ndeb.min_G(T, EOS_parameters[0] * .9, P=Pressure)

# Evaluation of thermodynamic properties
# =========================
tprops_dict = ndeb.eval_props(T, V, P=Pressure)
```

To Do's:

- Improve error handling
- Improve Documentation
- Add handling of anisotropic materials
- Prediction of explicit anharmonicity parameters