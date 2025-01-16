from debyetools.ndeb import nDeb
from debyetools import potentials
from debyetools.aux_functions import gen_Ts,load_V_E
from debyetools.poisson import poisson_ratio
from debyetools.electronic import fit_electronic
from debyetools.aux_functions import load_EM
from debyetools.aux_functions import load_doscar

m = 0.021971375
V_data, E_data = load_V_E('../Al3Li_L12/SUMMARY', '../Al3Li_L12/CONTCAR')
V_data, E_data = V_data*(1E-30*6.02E+23), E_data*(1.60218E-19 * 6.02214E+23)

params_initial_guess = [-3e5, 1e-5, 7e10, 4]
eos = potentials.BM()
eos.fitEOS(V_data, E_data, params_initial_guess)

EM = load_EM( '../Al3Li_L12/OUTCAR_elastic')
nu = poisson_ratio (EM)

p_el_initial = [3.8e-01,-1.9e-02,
                5.3e-04,-7.0e-06]

list_filetags = ['01','02','03','04',
                 '05','06','07','08',
                 '09','10','11','12',
                 '13','14','15','16',
                 '17','18','19','20','21']
E, N, Ef = load_doscar('../Al3Li_L12/DOSCAR.EvV.',
                       list_filetags=list_filetags)
params_electronic = fit_electronic(V_data, p_el_initial, E, N, Ef)


params_defects = [8.46, 1.69, 933, 0.1]
params_anh, params_intanh = [0,0,0], [0, 1]

ndeb = nDeb (nu , m, params_intanh , eos , params_electronic , params_defects , params_anh )
T_initial, T_final = 0.1, 1000.1
T = gen_Ts ( T_initial , T_final , 10 )
T,V = ndeb.min_G(T,initial_V=1e-5,P=0)
print(V)
# array([9.98852539e-06, 9.99974297e-06, 1.00578469e-05, 1.01135875e-05,
#        1.01419825e-05, 1.02392921e-05, 1.03467847e-05, 1.04650048e-05,
#        1.05953063e-05, 1.07396467e-05, 1.09045695e-05, 1.10973163e-05])
