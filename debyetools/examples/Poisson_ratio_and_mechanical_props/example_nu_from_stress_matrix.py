import numpy as np
from debyetools.poisson import poisson_ratio
EM = np.array([[122.3,35.0,35.0,0.,0.,0.],
[35.0,122.3,35.0,0.,0.,0.],
[35.0,35.0,122.3,0.,0.,0.],
[0.,0.,0.,41.4,0.,0.],
[0.,0.,0.,0.,41.4,0.],
[0.,0.,0.,0.,0.,41.4]])
print(poisson_ratio(EM))


