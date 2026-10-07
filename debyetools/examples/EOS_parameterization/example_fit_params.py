import numpy as np
import debyetools.potentials as potentials
from debyetools.constants import A3_ATOM_TO_M3_MOL, EV_ATOM_TO_J_MOL
V_data = np.array([12.01468,12.41964,12.83359,13.25664,
                   13.68889,14.13043,14.58137,15.04180,
                   15.51183,15.99154,16.48104,16.98044,
                   17.48982,18.00928,18.53893,19.07887,
                   19.62919,20.18999,20.76137,21.34343,
                   21.93627])*A3_ATOM_TO_M3_MOL
E_data = np.array([-3.21075,-3.32645,
    -3.42484,-3.50732,-3.57521,-3.62974,
    -3.67207,-3.70330,-3.72444,-3.73646,
                   -3.74027,-3.73669,-3.72652,-3.71050,
                   -3.68929,-3.66356,-3.63391,-3.60091,
                   -3.56513,-3.52708,
                   -3.48719])*EV_ATOM_TO_J_MOL
params_initial_guess = [-3e5, 1e-5, 7e10, 4]
Birch_Murnaghan = potentials.BM()
Birch_Murnaghan.fitEOS(V_data, E_data, params_initial_guess)
print(Birch_Murnaghan.pEOS)



