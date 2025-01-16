from debyetools.aux_functions import load_EM
from debyetools.poisson import poisson_ratio

EM = load_EM( '../Al3Li_L12/OUTCAR_elastic')
print(poisson_ratio(EM))