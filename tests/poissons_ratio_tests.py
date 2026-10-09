import unittest
import numpy as np
from debyetools.poisson import poisson_ratio
from debyetools.aux_functions import load_EM
import os
HERE = os.path.dirname(os.path.abspath(__file__))  # test data paths are relative to this file
# expected values: exact Voigt-Reuss-Hill nu (checked against an independent tensor-invariant evaluation)
class PoissonsRatioTestCase(unittest.TestCase):
    def setUp(self):
        #self.NL = PairAnalysisCalculator()
        pass

    def test_nu_Al_fcc(self):
        """ Test the calculation of poisson ratio for Al fcc."""

        EM = np.array([[1176.3800,583.4239,583.4239,-0.0000,-0.0000,0.0000],
                       [583.4239,1176.3800,583.4239,0.0000,-0.0000,0.0000],
                       [583.4239,583.4239,1176.3800,-0.0000,0.0000,0.0000],
                       [-0.0000,0.0000,-0.0000,347.2682,-0.0000,-0.0000],
                       [-0.0000,-0.0000,0.0000,-0.0000,347.2682,-0.0000],
                       [0.0000,0.0000,0.0000,-0.0000,-0.0000,347.2682]])

        np.testing.assert_allclose(poisson_ratio(EM), 0.31681328927273705, rtol=1e-10)

    def test_nu_MgCl2_R3m(self):
        """ Test the calculation of poisson ratio for MgCl2 R3m."""

        EM = np.array([[580,150,20, -0.0000, -0.0000,  0.0000],
                       [150,580,20,  0.0000, -0.0000,  0.0000],
                       [20,20,20, -0.0000,  0.0000,  0.0000],
                       [-0.0000,  0.0000, -0.0000,3, -0.0000, -0.0000],
                       [-0.0000, -0.0000,  0.0000, -0.0000,3, -0.0000],
                       [0.0000,  0.0000,  0.0000, -0.0000, -0.0000,210]])

        np.testing.assert_allclose(poisson_ratio(EM), 0.250262495815555, rtol=1e-10)

    def test_nu_Al2O3_R3c(self):
        """ Test the calculation of poisson ratio for Al2O3 R3c."""

        EM = np.array([[ 4520, 1500, 1070,  200.0000,  -0.0000,   0.0000],
                       [1500, 4520, 1070, -200.0000,  -0.0000,   0.0000],
                       [1070, 1070, 4540, -0.0000,   0.0000,   0.0000],
                       [200,  -200,   -0,    1320,-0.0000,  -0.0000],
                       [0,-0,  -0,    0,  1320,  200],
                       [0,   0,    0,   -0,    200,    1510]])

        # exact VRH (S = C^-1, C6); the former closed form ignored the trigonal couplings (0.2362)
        np.testing.assert_allclose(poisson_ratio(EM), 0.2380209705349047, rtol=1e-10)

    def test_nu_Al2O3_R3c_read(self):
        """ Test the calculation of poisson ratio for Al2O3 R3c."""

        EM = load_EM(os.path.join(HERE, 'inpt_files', 'Al2O3_R3c', 'OUTCAR.eps'))

        np.testing.assert_allclose(poisson_ratio(EM), 0.2380209705349047, rtol=1e-10)

if __name__=='__main__':
    unittest.main()
