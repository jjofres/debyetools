from debyetools.aux_functions import load_doscar
from debyetools.electronic import fit_electronic
from debyetools.aux_functions import load_V_E

V_data, E_data = load_V_E('../Al3Li_L12/SUMMARY', '../Al3Li_L12/CONTCAR')
V_data, E_data = V_data*(1E-30*6.02E+23), E_data*(1.60218E-19 * 6.02214E+23)

p_el_initial = [3.8e-01,-1.9e-02,
                5.3e-04,-7.0e-06]
list_filetags = ['01','02','03','04',
                 '05','06','07','08',
                 '09','10','11','12',
                 '13','14','15','16',
                 '17','18','19','20','21']
E, N, Ef = load_doscar('../Al3Li_L12/DOSCAR.EvV.',
                       list_filetags=list_filetags)
params_el = fit_electronic(V_data, p_el_initial,
                           E, N, Ef)
print(params_el)
#1.733724914e-01, -6.877536975e+03, 0.000000000e+00, 0.000000000e+00

