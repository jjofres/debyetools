import unittest
import numpy as np
from debyetools.ndeb import nDeb
from debyetools.defects import Defects
import debyetools.potentials as potentials


def fd(f, z, h):
    return (f(z + 3 * h) - 9 * f(z + 2 * h) + 45 * f(z + h) - 45 * f(z - h) + 9 * f(z - 2 * h) - f(z - 3 * h)) / (60 * h)


def fd2(f, z, h):
    return (2 * f(z + 3 * h) - 27 * f(z + 2 * h) + 270 * f(z + h) - 490 * f(z) + 270 * f(z - h)
            - 27 * f(z - 2 * h) + 2 * f(z - 3 * h)) / (180 * h * h)


class RTestCase(unittest.TestCase):
    """r (types of atoms per formula unit) multiplies F_vib and F_def and all their derivatives (D5)."""

    def test_defects_scale_with_r(self):
        d1 = Defects(8.46, 1.69, 933, 0.1, 7.6e10, 9.9e-6)
        d2 = Defects(8.46, 1.69, 933, 0.1, 7.6e10, 9.9e-6, r=2)
        for name in ['E', 'S', 'F', 'dFdV_T', 'dFdT_V', 'd2FdT2_V', 'd2FdV2_T', 'd3FdV3_T', 'd4FdV4_T',
                     'd2FdVdT', 'd3FdV2dT', 'd3FdVdT2']:
            self.assertEqual(getattr(d2, name)(800., 1.01e-5), 2 * getattr(d1, name)(800., 1.01e-5), msg=name)

    def test_properties_consistent_with_F(self):
        """With r = 2, S, Cv, Kt, alpha and Cp from eval_props equal finite differences of F."""
        eos = potentials.BM(parameters=np.array([-3.6e5, 9.9e-6, 7.6e10, 4.6]))
        for mode in ('jjsl', 'DM'):
            nd = nDeb(0.33, 0.0269815, (-2e-5, 1.5), eos, (0.3, -1e4, 0, 0), (8.46, 1.69, 933, 0.1),
                      (1e-4, -1e-7, 1e-10), mode=mode, r=2)
            F = lambda T, V: nd.f2min(T, V, 0)
            for T, fv in [(300., 1.0), (800., 1.04)]:
                V = fv * eos.V0
                tp = nd.eval_props(np.array([T]), np.array([V]), P=0)
                hT, hV = 1e-3 * T, 1e-3 * V
                S = -fd(lambda t: F(t, V), T, hT)
                Cv = -T * fd2(lambda t: F(t, V), T, hT)
                Kt = V * fd2(lambda v: F(T, v), V, hV)
                a = -fd(lambda t: fd(lambda v: F(t, v), V, hV), T, hT) / Kt
                Cp = Cv + T * V * a ** 2 * Kt
                for key, ref in [('S', S), ('Cv', Cv), ('Kt', Kt), ('a', a), ('Cp', Cp)]:
                    self.assertAlmostEqual(tp[key][0] / ref, 1, delta=1e-6, msg='%s %s T=%g' % (mode, key, T))


if __name__ == '__main__':
    unittest.main()
