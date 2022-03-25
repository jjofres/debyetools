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
        T, V = ndeb_BM.min_G(T,self.p_EOS[1],P=0)

        self.assertAlmostEqual(35.165345471248784, ndeb_BM.eval_props(T[-1],V[-1],P=0)['Cp'],places=2)

    def test_Free_energy_minimization_Al_fcc_RV(self):
        """ Test V(T) calculation by free energy minimization. RV."""

        EOS_name = 'RV'
        EOS_BM = getattr(potentials, EOS_name)()
        EOS_BM.pEOS = self.p_EOS
        EOS_BM.V0 = self.p_EOS[1]
        ndeb_BM = nDeb(self.nu, self.m, self.p_intanh, EOS_BM, self.p_electronic, self.p_defects, self.p_anh, EOS_name)

        T = gen_Ts(self.T_initial, self.T_final, self.number_Temps)
        T, V = ndeb_BM.min_G(T,self.p_EOS[1],P=0)

        self.assertAlmostEqual(37.96690007966743, ndeb_BM.eval_props(T[-1],V[-1],P=0)['Cp'],places=2)

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
        T, V = ndeb_Morse.min_G(T, self.p_EOS[1],P=0)

        self.assertAlmostEqual(32.15627134521426, ndeb_Morse.eval_props(T[-1],V[-1],P=0)['Cp'],places=2)

    def test_Free_energy_minimization_Al_fcc_EAM(self):
        """ Test V(T) calculation by free energy minimization. EAM."""

        EOS_name = 'EAM'
        p_EOS = np.array([3.647649855e-03, 1.643670214e+00, 1.201433529e-02, 2.110843838e-02, 2.099552421e-01, 1.110019124e+00, 9.353164553e-01, 2.032247973e-06, 1.432174178e-01, 1.213592440e+00])

        formula = 'AlAlAlAl'
        a = 4.0396918604
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        basis_vectors = np.array([[0,0,0],[0, .5,.5],[.5,0,.5],[.5,.5,0]])
        cutoff = 5.
        number_of_neighbor_levels = 3
        EOS_BM = getattr(potentials, EOS_name)(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels, parameters=p_EOS)
        EOS_BM.V0 = 10E-6
        ndeb_Morse = nDeb(self.nu, self.m, self.p_intanh, EOS_BM, self.p_electronic, self.p_defects, self.p_anh,
                          formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels, mode='jj')
        T = gen_Ts(self.T_initial, self.T_final, self.number_Temps)
        T, V = ndeb_Morse.min_G(T,self.p_EOS[1],P=0)
        # print(T, V)

        self.assertAlmostEqual(32.76910671651026 , ndeb_Morse.eval_props(T[-1], V[-1],P=0)['Cp'],places=2)


if __name__=='__main__':
    unittest.main()
