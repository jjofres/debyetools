# debyetools

Implementation of a tool for calculating self-consistent thermodynamic properties that can take into account all kinds of contributions to the free energy inluding explicit anharmonicity. The software presented here is based in the Debye approximation within the QHA using the crystal internal energetics parametrized at ground-state to project the thermodynamics properties at high temperatures. 

Made by Javier Jofre: javier.jofre@polymtl.ca
Please cite.

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

To start getting familiar with the interface `tProps` you can download `examples input files`.
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
from debyetools.aux_functions import load_doscar, load_V_E, load_EM
import debyetools.potentials as potentials
from debyetools.electronic import fit_electronic    
from debyetools.poisson import poisson_ratio
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts
from debyetools.fs_compound_db import fit_FS

folder_name = './inpt_files/Al_fcc'
# EOS parametrization
# =========================
V_DFT, E_DFT = load_V_E(folder_name, folder_name + '/CONTCAR.5', units='J/mol')
EOS_name = 'BM4'
initial_parameters = [-3.6e+05, 9.9e-06, 7.8e+10, 4.7e+00, 1.e-10]
eos_BM4 = getattr(potentials, EOS_name)()
eos_BM4.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters)
p_EOS = eos_BM4.pEOS
# =========================

# Electronic Contributions
# =========================
p_el_inittial = [3.8027342892e-01, -1.8875015171e-02,
                 5.3071034596e-04, -7.0100707467e-06]
E, N, Ef = load_doscar(folder_name + '/DOSCAR.EvV.')
p_electronic = fit_electronic(V_DFT, p_el_inittial, E, N, Ef)
# =========================

# Other Contributions parametrization
# =========================
Tmelting = 933
p_defects = 8.46, 1.69, Tmelting, 0.1
p_intanh = 0, 1
p_anh = 0, 0, 0
# =========================

# Poisson's ratio
# =========================
EM = load_EM(folder_name + '/OUTCAR.eps')
nu = poisson_ratio(EM)
# =========================

# F minimization
# =========================
m = 0.026981500000000002
ndeb_BM4 = nDeb(nu, m, p_intanh, eos_BM4, p_electronic, p_defects, p_anh, mode='jjsl')

T_initial, T_final, number_Temps = 0.1, 1000, 10
T = gen_Ts(T_initial, T_final, number_Temps)
Pressure = 0
T, V = ndeb_BM4.min_G(T, p_EOS[1] * .9, P=Pressure)
# =========================

# Evaluations
# =========================
tprops_dict = ndeb_BM4.eval_props(T, V, P=Pressure)

T_from = 298.15
T_to = 1000
# =========================

# FS comp db parameters
# =========================
FS_db_params = fit_FS(tprops_dict, T_from, T_to)
print( FS_db_params['Cp'])
```

To Do's:

- Add More Examples to Documentation
- Improve error handling
- Add 'Compatible input files formats'
- Improve Documentation
- Add handling of anisotropic materials
- Prediction of explicit anharmonicity parameters