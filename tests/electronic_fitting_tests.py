import unittest
import numpy as np
from debyetools.electronic import fit_electronic
from debyetools.aux_functions import load_doscar,load_V_E
class ElectronicContributionFittingTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_NfV_fitting(self):
        """ Test fitting of the NfV."""

        V_DFT = np.array([7.2328381349E-06,7.4766214899E-06,7.7258220323E-06,7.9804992917E-06,8.2407127976E-06,8.5065220794E-06,8.7779866668E-06,9.0551660893E-06,9.3381198763E-06,9.6269075575E-06,9.9215886624E-06,1.0222222720E-05,1.0528869261E-05,1.0841587814E-05,1.1160437909E-05,1.1485479075E-05,1.1816770842E-05,1.2154372740E-05,1.2498344297E-05,1.2848745044E-05,1.3205634510E-05])

        p_el_inittial = [2.828998e-01, -1.023899e+04,  0.000000e+00,  0.000000e+00]#[3.802734e-01, -1.887502e-02,  5.307103e-04, -7.010071e-06]

        # np.savetxt('E4test',E)
        # np.savetxt('N4test', N)
        E = np.loadtxt('../E4test')
        N = np.loadtxt('N4test')

        # print('XXXXXX', np.shape(E), np.shape(N))

        Ef =  [11.67302353, 11.25108797, 10.84338223, 10.44727947, 10.06067677, 9.68460247, 9.32198386, 8.97425327, 8.64003753, 8.31659488, 8.00285946, 7.69867685, 7.40309847, 7.11468182, 6.83256146, 6.55628297, 6.28531296, 6.01988332, 5.76265758, 5.51614726, 5.2808033]

        p_el_optimal = fit_electronic(V_DFT, p_el_inittial,E,N,Ef)
        print('XXXXXXXX', p_el_optimal)


        np.testing.assert_array_almost_equal(p_el_optimal, [2.23120482e-01, -8.33901442e+03,  0.00000000e+00,  0.00000000e+00],decimal=1)


    def test_NfV_fitting_reading_from_DOSCAR(self):
        """ Test fitting of the NfV."""
        folder_name = '../tests/inpt_files/Al_fcc'

        V_DFT, E_DFT = load_V_E(folder_name + '/SUMMARY.fcc', folder_name + '/CONTCAR.5', units='J/mol')

        p_el_inittial = [4.191757352e-01, -1.596432753e+04, 0.000000000e+00, 0.000000000e+00]#[3.802734e-01, -1.887502e-02,  5.307103e-04, -7.010071e-06]
        #4.19175580e-01 -1.59643128e+04  0.00000000e+00  0.00000000e+00
        #
        list_filetags = ['01a', '02a', '03a', '04a', '05a', '06a', '07a', '08a',
                         '09a', '10a', '11a', '12a', '13a', '14a', '15a', '16a', '17a',
                         '18a', '19a', '20a', '21a']
        E, N, Ef = load_doscar(folder_name+'/DOSCAR.EvV.', list_filetags=list_filetags)

        p_el_optimal = fit_electronic(V_DFT, p_el_inittial,E,N,Ef)

        np.testing.assert_array_almost_equal(p_el_optimal, [4.191757352e-01, -1.596432753e+04, 0.000000000e+00, 0.000000000e+00],decimal=1)


if __name__=='__main__':
    unittest.main()
