# debyetools

A little library for the implementation of a Debye approximation tool for calculating self-consistent thermodynamic properties.The software presented here is based in the Debye approximation of the QHA using the crystal internal energetics parametrized at ground-state to project the thermodynamics properties at high temperatures. We present here how each contribution to the free energy are considered and a description of the architecture of the calculation engine and of the GUI.

### Requirements:
- numpy
- numpy
- scipy
- PySimpleGUI
- matplotlib

Made by Javier Jofre: javier.jofre@polymtl.ca
Please cite.

### Installation
```
pip install --update debyetools
```

### Get started
Example: heat capacity of Al fcc using 3rd order Birch-Murnaghan EOS

```Python
import numpy as np
from debyetools.ndeb import nDeb

nu, m = 0.32, 0.026981500000000002
Tmelting = 933

p_EOS = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
p_intanh = 0, 1, p_EOS[1]
p_electronic = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
p_defects = 8.46, 1.69, Tmelting, 0.1, p_EOS[2],p_EOS[1]
p_anh = 0,0,0

EOS_name = 'BM'

ndeb_BM = nDeb(nu, m, p_intanh, p_EOS, p_electronic, p_defects,p_anh,EOS_name)

T,V = 9.33000000000e+02,1.07790131286e-05
                       #
result = ndeb_BM.eval_props(T,V)['Cp']
```

To Do's:

- Add Examples to Documentation
- Improve error handling
- Add 'Compatible input files formats'
