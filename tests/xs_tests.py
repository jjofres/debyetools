import unittest
import numpy as np
from debyetools.XS import Xs
from debyetools.ndeb import nDeb
import debyetools.potentials as potentials


def fd(f, z, h):
    return (f(z + 3 * h) - 9 * f(z + 2 * h) + 45 * f(z + h) - 45 * f(z - h) + 9 * f(z - 2 * h) - f(z - 3 * h)) / (60 * h)


class XsTestCase(unittest.TestCase):
    """Excess term F_xs = sum_i A_i(V) g_i(T); A_i a number or a polynomial in V."""

    def test_constant_coefficients(self):
        x = Xs(10., 0.01, 1e-6, 1e-9, 0.1, 1e3)
        T = np.array([100., 500., 1200.])
        F = 10. + 0.01 * T + 1e-6 * T**2 + 1e-9 * T**3 + 0.1 * T * np.log(T) + 1e3 * T**-2
        np.testing.assert_allclose(x.F(T, 1e-5), F, rtol=1e-15)
        self.assertFalse(x.V_dependent)
        for name in ['dFdV_T', 'd2FdV2_T', 'd3FdV3_T', 'd4FdV4_T', 'd2FdVdT', 'd3FdV2dT', 'd3FdVdT2']:
            self.assertTrue(np.all(getattr(x, name)(T, 1e-5) == 0))

    def test_volume_dependent_derivatives(self):
        x = Xs([1., 2e5, -3e9, 4e13, 5e18], 0.01, [0.1, 1e3, -2e7, 3e11, -4e16], 1e-9, [0.1, -1e3], [1e3, 1e7])
        self.assertTrue(x.V_dependent)
        chain = [('dFdV_T', 'F', 'V'), ('dFdT_V', 'F', 'T'), ('d2FdT2_V', 'dFdT_V', 'T'),
                 ('d2FdV2_T', 'dFdV_T', 'V'), ('d3FdV3_T', 'd2FdV2_T', 'V'), ('d4FdV4_T', 'd3FdV3_T', 'V'),
                 ('d2FdVdT', 'dFdV_T', 'T'), ('d3FdV2dT', 'd2FdV2_T', 'T'), ('d3FdVdT2', 'd2FdVdT', 'T')]
        for T, V in [(300., 1e-5), (900., 1.1e-5)]:
            for hi, lo, var in chain:
                if var == 'V':
                    num = fd(lambda v: getattr(x, lo)(T, v), V, 1e-3 * V)
                else:
                    num = fd(lambda t: getattr(x, lo)(t, V), T, 1e-3 * T)
                self.assertAlmostEqual(getattr(x, hi)(T, V) / num, 1, delta=1e-9, msg=hi)
            self.assertAlmostEqual(x.E(T, V), x.F(T, V) + T * x.S(T, V), delta=1e-9 * abs(x.E(T, V)))

    def test_pressure_in_nDeb(self):
        """A0(V) = c0 + c1 V and A1(V) = d0 + d1 V shift P by -(c1 + d1 T) exactly."""
        eos = potentials.BM()
        eos.pEOS = np.array([-3.6e5, 9.9e-6, 7.6e10, 4.6])
        eos = potentials.BM(parameters=eos.pEOS)
        args = (0.33, 0.0269815, (0, 1), eos, (0, 0, 0, 0), (0, 0, 933, 0), (0, 0, 0))
        T = np.array([300., 800.])
        V = np.array([1.0, 1.03]) * eos.V0
        p0 = nDeb(*args).eval_props(T, V, P=0)
        p1 = nDeb(*args, xsparams=([10., 1e5], [0.01, 50.], 0, 0, 0, 0)).eval_props(T, V, P=0)
        np.testing.assert_allclose(p1['P'] - p0['P'], -(1e5 + 50. * T), rtol=1e-6)


if __name__ == '__main__':
    unittest.main()
