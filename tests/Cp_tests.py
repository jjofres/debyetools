import unittest
import numpy as np
from debyetools import pairanalysis as pa_calc
from debyetools import aux_functions as aux_fn

class GenerateCellCoordinatesTestCase(unittest.TestCase):
    def setUp(self):
        #self.NL = PairAnalysisCalculator()
        pass

    def test_Cp_Al_fcc(self):
        """ Test evaluation of Cp for Al fcc at a given T and V using the 3rd order Birch-Murnaghan EOS."""

        nu, r, m = 0.31681, 1, 0.026981500000000002
        Tmelting = 933
        pEOS = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
        a0, m0, V0 = 0, 1, pEOS[1]
        q0,q1,q2,q3 = [3.8027e-01, -1.8875e-02, 5.3071e-04, -7.0101e-06]
        Evac00,Svac00,a,P2 = 8.46, 1.69,0.1,pEOS[2]
        s0,s1,s2 = 0,0,0
        ndeb_BM = nDeb(nu, r, m, Tmelting, a0, m0, V0, pEOS, q0,q1,q2,q3, Evac00,Svac00,Tmelting,a,P2,s0,s1,s2)

        T,V = 9.3300000000000E+02,1.0779013128600E-05

        self.asserAlmosEqual(ndeb_BM.Cp(T,V),3.3249653530900E+01)

if __name__=='__main__':
    unittest.main()
