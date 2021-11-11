import unittest
import numpy as np
from debyetools.ndeb import nDeb
class CpTestCase(unittest.TestCase):
    def setUp(self):
        #self.NL = PairAnalysisCalculator()
        pass

    def test_Cp_Al_fcc(self):
        """ Test evaluation of Cp for Al fcc at a given T and V using the 3rd order Birch-Murnaghan EOS."""

        nu, m = 0.32, 0.026981500000000002
        Tmelting = 933
        p_EOS = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
        p_intanh = 0, 1, p_EOS[1]
        p_electronic = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
        p_defects = 8.46, 1.69, Tmelting, 0.1, p_EOS[2],p_EOS[1]
        p_anh = 0,0,0

        EOS_name = 'BM'
        ndeb_BM = nDeb(nu, m, p_intanh, p_EOS, p_electronic, p_defects, p_anh, EOS_name)

        T,V = 9.3300000000000E+02,1.0779013128600E-05

        self.assertAlmostEqual(ndeb_BM.eval_props(T,V)['Cp'],33.249439691599925)

if __name__=='__main__':
    unittest.main()
