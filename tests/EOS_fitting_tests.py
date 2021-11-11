import unittest
import numpy as np
from debyetools.potentials import MP, BM

class EOSparametrizationTestCase(unittest.TestCase):
    def setUp(self):
        #self.NL = PairAnalysisCalculator()
        pass

    def test_EOS_Morse_Al_fcc_evaluations(self):
        """ Test evaluation of Morse potential using Al fcc DFT data."""

        V_DFT = [7.2328381349E-06,7.4766214899E-06,7.7258220323E-06,7.9804992917E-06,8.2407127976E-06,8.5065220794E-06,8.7779866668E-06,9.0551660893E-06,9.3381198763E-06,9.6269075575E-06,9.9215886624E-06,1.0222222720E-05,1.0528869261E-05,1.0841587814E-05,1.1160437909E-05,1.1485479075E-05,1.1816770842E-05,1.2154372740E-05,1.2498344297E-05,1.2848745044E-05,1.3205634510E-05]
        E_DFT = [-3.1142624910E+05,-3.2250917927E+05,-3.3187138662E+05,-3.3970381602E+05,-3.4613131971E+05,-3.5129770939E+05,-3.5530574212E+05,-3.5828253759E+05,-3.6027737577E+05,-3.6141349280E+05,-3.6177140584E+05,-3.6144576720E+05,-3.6049509535E+05,-3.5899479371E+05,-3.5699510714E+05,-3.5454316879E+05,-3.5173001277E+05,-3.4858366812E+05,-3.4518407309E+05,-3.4152425661E+05,-3.3764778189E+05]

        formula = 'AlAlAlAl'
        a = 4.0396918604
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        basis_vectors = np.array([[0,0,0],[0, .5,.5],[.5,0,.5],[.5,.5,0]])
        cutoff = 5.
        number_of_neighbor_levels = 3

        p_EOS = np.array([3.492281316e-01, 9.977375168e-01, 3.246481751e+00])
        eos_Morse = MP(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels, units='J/mol', parameters = p_EOS)

        E_model = [eos_Morse.E0(Vi) for Vi in V_DFT]

        self.assertTrue(np.sqrt(np.sum(np.array([(Ei-Emi)**2 for Ei, Emi in zip(E_DFT, E_model)])))/np.abs(np.mean(E_DFT))*100<0.5)

    def test_EOS_Morse_Al_fcc_evaluations_eV_units(self):
        """ Test evaluation of Morse potential using Al fcc DFT data."""

        V_DFT = np.array([7.2328381349E-06,7.4766214899E-06,7.7258220323E-06,7.9804992917E-06,8.2407127976E-06,8.5065220794E-06,8.7779866668E-06,9.0551660893E-06,9.3381198763E-06,9.6269075575E-06,9.9215886624E-06,1.0222222720E-05,1.0528869261E-05,1.0841587814E-05,1.1160437909E-05,1.1485479075E-05,1.1816770842E-05,1.2154372740E-05,1.2498344297E-05,1.2848745044E-05,1.3205634510E-05])
        E_DFT = np.array([-3.1142624910E+05,-3.2250917927E+05,-3.3187138662E+05,-3.3970381602E+05,-3.4613131971E+05,-3.5129770939E+05,-3.5530574212E+05,-3.5828253759E+05,-3.6027737577E+05,-3.6141349280E+05,-3.6177140584E+05,-3.6144576720E+05,-3.6049509535E+05,-3.5899479371E+05,-3.5699510714E+05,-3.5454316879E+05,-3.5173001277E+05,-3.4858366812E+05,-3.4518407309E+05,-3.4152425661E+05,-3.3764778189E+05])

        V_DFT = V_DFT/(1e-30*6.02e23)
        E_DFT = E_DFT/(0.160218e-18*6.02214e23)

        formula = 'AlAlAlAl'
        a = 4.0396918604
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        basis_vectors = np.array([[0,0,0],[0, .5,.5],[.5,0,.5],[.5,.5,0]])
        cutoff = 5.
        number_of_neighbor_levels = 3

        p_EOS = np.array([3.492281316e-01, 9.977375168e-01, 3.246481751e+00])
        eos_Morse = MP(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels, units='eV/atom', parameters = p_EOS)

        E_model = [eos_Morse.E0(Vi) for Vi in V_DFT]

        self.assertTrue(np.sqrt(np.sum(np.array([(Ei-Emi)**2 for Ei, Emi in zip(E_DFT, E_model)])))/np.abs(np.mean(E_DFT))*100<0.5)

    def test_EOS_Morse_Al_fcc_fitting(self):

        V_DFT = np.array([7.2328381349E-06,7.4766214899E-06,7.7258220323E-06,7.9804992917E-06,8.2407127976E-06,8.5065220794E-06,8.7779866668E-06,9.0551660893E-06,9.3381198763E-06,9.6269075575E-06,9.9215886624E-06,1.0222222720E-05,1.0528869261E-05,1.0841587814E-05,1.1160437909E-05,1.1485479075E-05,1.1816770842E-05,1.2154372740E-05,1.2498344297E-05,1.2848745044E-05,1.3205634510E-05])
        E_DFT = np.array([-3.1142624910E+05,-3.2250917927E+05,-3.3187138662E+05,-3.3970381602E+05,-3.4613131971E+05,-3.5129770939E+05,-3.5530574212E+05,-3.5828253759E+05,-3.6027737577E+05,-3.6141349280E+05,-3.6177140584E+05,-3.6144576720E+05,-3.6049509535E+05,-3.5899479371E+05,-3.5699510714E+05,-3.5454316879E+05,-3.5173001277E+05,-3.4858366812E+05,-3.4518407309E+05,-3.4152425661E+05,-3.3764778189E+05])
        formula = 'AlAlAlAl'
        a = 4.0396918604
        primitive_cell = np.array([[a, 0, 0], [0, a, 0], [0, 0, a]])
        basis_vectors = np.array([[0,0,0],[0, .5,.5],[.5,0,.5],[.5,.5,0]])
        cutoff = 5.
        number_of_neighbor_levels = 3
        eos_Morse = MP(formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels, units='J/mol')
        initial_parameters = np.array([0.35, 1, 3.5])

        eos_Morse.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters)

        bool_1 = None == np.testing.assert_array_almost_equal(eos_Morse.pEOS, np.array([3.492281316e-01, 9.977375168e-01, 3.246481751e+00]))

    def test_EOS_BM3_Al_fcc_fitting(self):
        V_DFT = np.array([7.2328381349E-06,7.4766214899E-06,7.7258220323E-06,7.9804992917E-06,8.2407127976E-06,8.5065220794E-06,8.7779866668E-06,9.0551660893E-06,9.3381198763E-06,9.6269075575E-06,9.9215886624E-06,1.0222222720E-05,1.0528869261E-05,1.0841587814E-05,1.1160437909E-05,1.1485479075E-05,1.1816770842E-05,1.2154372740E-05,1.2498344297E-05,1.2848745044E-05,1.3205634510E-05])
        E_DFT = np.array([-3.1142624910E+05,-3.2250917927E+05,-3.3187138662E+05,-3.3970381602E+05,-3.4613131971E+05,-3.5129770939E+05,-3.5530574212E+05,-3.5828253759E+05,-3.6027737577E+05,-3.6141349280E+05,-3.6177140584E+05,-3.6144576720E+05,-3.6049509535E+05,-3.5899479371E+05,-3.5699510714E+05,-3.5454316879E+05,-3.5173001277E+05,-3.4858366812E+05,-3.4518407309E+05,-3.4152425661E+05,-3.3764778189E+05])

        pEOS = np.array([-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00])
        eos_BM3 = BM(parameters=pEOS)

        E_model = [eos_BM3.E0(Vi) for Vi in V_DFT]

        self.assertTrue(np.sqrt(np.sum(np.array([(Ei-Emi)**2 for Ei, Emi in zip(E_DFT, E_model)])))/np.abs(np.mean(E_DFT))*100<0.5)

if __name__=='__main__':
    unittest.main()
