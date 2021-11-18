import unittest
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts
import numpy as np
import debyetools.potentials as potentials

class FminTestCase(unittest.TestCase):
    def setUp(self):
        self.nu, self.m = 0.31681, 0.026981500000000002
        self.Tmelting = 933
        self.p_EOS = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
        self.p_intanh = 0, 1
        self.p_electronic = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
        self.p_defects = 8.46, 1.69, self.Tmelting, 0.1
        self.p_anh = 0,0,0
        self.T_initial, self.T_final = 0.1, 1000.1
        self.number_Temps = 51

    def test_Free_energy_minimization_Al_fcc_BM(self):
        """ Test V(T) calculation by free energy minimization. BM."""

        EOS_name = 'BM'
        EOS_BM = getattr(potentials, EOS_name)()
        EOS_BM.pEOS = self.p_EOS
        EOS_BM.V0 = self.p_EOS[1]
        ndeb_BM = nDeb(self.nu, self.m, self.p_intanh, EOS_BM, self.p_electronic, self.p_defects, self.p_anh, EOS_name)

        T = gen_Ts(self.T_initial, self.T_final, self.number_Temps)
        T, V = ndeb_BM.min_F(T,self.p_EOS[1])

        self.assertAlmostEqual(35.166117790049896, ndeb_BM.eval_props(T[-1],V[-1])['Cp'])

    def test_Free_energy_minimization_Al_fcc_RV(self):
        """ Test V(T) calculation by free energy minimization. RV."""

        EOS_name = 'RV'
        EOS_BM = getattr(potentials, EOS_name)()
        EOS_BM.pEOS = self.p_EOS
        EOS_BM.V0 = self.p_EOS[1]
        ndeb_BM = nDeb(self.nu, self.m, self.p_intanh, EOS_BM, self.p_electronic, self.p_defects, self.p_anh, EOS_name)

        T = gen_Ts(self.T_initial, self.T_final, self.number_Temps)
        T, V = ndeb_BM.min_F(T,self.p_EOS[1])

        self.assertAlmostEqual(37.96026289773106, ndeb_BM.eval_props(T[-1],V[-1])['Cp'])

    def test_Free_energy_minimization_Al_fcc_Morse(self):
        """ Test V(T) calculation by free energy minimization. Morse."""

        EOS_name = 'MP'
        p_EOS = np.array([3.492281316e-01, 9.977375168e-01, 3.246481751e+00])

        formula = 'AlAlAlAl'
        a = 4.0396918604
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        basis_vectors = np.array([[0,0,0],[0, .5,.5],[.5,0,.5],[.5,.5,0]])
        cutoff = 5.
        number_of_neighbor_levels = 6
        EOS_BM = getattr(potentials, EOS_name)(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels)
        EOS_BM.pEOS = p_EOS
        EOS_BM.V0 = p_EOS[1]
        ndeb_Morse = nDeb(self.nu, self.m, self.p_intanh, EOS_BM,
                        self.p_electronic, self.p_defects, self.p_anh, EOS_name, formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels)

        T = gen_Ts(self.T_initial, self.T_final, self.number_Temps)
        T, V = ndeb_Morse.min_F(T, self.p_EOS[1])

        self.assertAlmostEqual(32.15669813382092, ndeb_Morse.eval_props(T[-1],V[-1])['Cp'])

    def test_Free_energy_minimization_Al_fcc_EAM(self):
        """ Test V(T) calculation by free energy minimization. EAM."""

        EOS_name = 'EAM'
        p_EOS = np.array([1.864283e-02, 1.087716e+00, 1.267761e+00, 1.016616e+00, 1.005353e+00, 2.981997e+00, 2.563705e-07, 1.105120e+00,1.815219e+00, 1.493627e+00])
        formula = 'AlAlAlAl'
        a = 4.0396918604
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        basis_vectors = np.array([[0,0,0],[0, .5,.5],[.5,0,.5],[.5,.5,0]])
        cutoff = 5.
        number_of_neighbor_levels = 6
        EOS_BM = getattr(potentials, EOS_name)(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels, parameters=p_EOS)
        EOS_BM.V0 = 10E-6
        ndeb_Morse = nDeb(self.nu, self.m, self.p_intanh, EOS_BM,
                          self.p_electronic, self.p_defects, self.p_anh, EOS_name, formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels)

        T = gen_Ts(self.T_initial, self.T_final, self.number_Temps)
        T, V = ndeb_Morse.min_F(T,self.p_EOS[1])

        self.assertAlmostEqual(36.127494489465, ndeb_Morse.eval_props(T[-1], V[-1])['Cp'])


if __name__=='__main__':
    unittest.main()
