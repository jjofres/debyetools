import os
import unittest
import warnings
import numpy as np
import debyetools.potentials as pot
from debyetools.aux_functions import load_V_E, load_cell

HERE = os.path.dirname(os.path.abspath(__file__))


def data(mat):
    d = os.path.join(HERE, 'inpt_files', mat)
    V, E = load_V_E(d + '/SUMMARY.fcc', d + '/CONTCAR.5', units='J/mol')
    return d, np.asarray(V, float), np.asarray(E, float)


class EOSFitRestartTestCase(unittest.TestCase):
    """fitEOS checks each fit and restarts from other starting points when it is not acceptable."""

    def test_good_start_is_kept(self):
        d, V, E = data('Al_fcc')
        eos = pot.BM()
        with warnings.catch_warnings():
            warnings.simplefilter('error', UserWarning)
            eos.fitEOS(V, E, initial_parameters=np.array([E.min(), V[np.argmin(E)], 1e11, 4.5]))
        self.assertEqual(eos.fit_info['accepted'], 'initial_parameters')
        self.assertEqual(len(eos.fit_info['attempts']), 1)

    def test_analytic_without_initial_parameters(self):
        d, V, E = data('Al_fcc')
        for name in ['BM', 'RV', 'MG', 'TB', 'MU', 'PT']:
            ref = getattr(pot, name)()
            ref.fitEOS(V, E, initial_parameters=np.array([E.min(), V[np.argmin(E)], 1e11, 4.5]))
            eos = getattr(pot, name)()
            eos.fitEOS(V, E)                      # start from a cubic fitted to the data
            self.assertEqual(eos.fit_info['accepted'], 'from data', msg=name)
            np.testing.assert_allclose(eos.E0(V), ref.E0(V), rtol=1e-6, err_msg=name)

    def test_bad_analytic_start_is_rescued(self):
        d, V, E = data('Al_fcc')
        eos = pot.BM()
        with self.assertWarns(UserWarning):
            eos.fitEOS(V, E, initial_parameters=np.array([0.0, 10 * V.max(), 1e6, 40.0]))
        self.assertNotEqual(eos.fit_info['accepted'], 'initial_parameters')
        rms = np.sqrt(np.mean((eos.E0(V) - E) ** 2))
        self.assertLess(rms / (E.max() - E.min()), 0.02)
        self.assertTrue(V.min() < eos.V0 < V.max())

    def test_morse_V_bcc_restart(self):
        """Morse for V bcc from (0.35, 1, 3.5) used to end at a wrong minimum (rms 24 kJ/mol, V0 = 3e-6)."""
        d, V, E = data('V_bcc')
        f, c, b = load_cell(d + '/CONTCAR.5')
        eos = pot.MP(f, c, b, 5, 3, units='J/mol')
        with self.assertWarns(UserWarning):
            eos.fitEOS(V, E, initial_parameters=np.array([0.35, 1, 3.5]))
        rms = np.sqrt(np.mean((eos.E0(V) - E) ** 2))
        self.assertLess(rms, 35.)                 # J/mol; the good fit has 33.0 J/mol (25.5 with the F= energies)
        self.assertAlmostEqual(eos.V0 / 8.1129e-6, 1, delta=1e-3)

    def test_failure_raises_or_warns(self):
        d, V, E = data('Al_fcc')
        p0 = np.array([E.min(), V[np.argmin(E)], 1e11, 4.5])
        with self.assertRaises(pot.EOSFitError):
            pot.BM().fitEOS(V, E, initial_parameters=p0, rel_tol=1e-12)
        eos = pot.BM()
        with self.assertWarns(UserWarning):
            eos.fitEOS(V, E, initial_parameters=p0, rel_tol=1e-12, on_failure='warn')
        self.assertIsNone(eos.fit_info['accepted'])
        self.assertTrue(np.all(np.isfinite(eos.pEOS)))


if __name__ == '__main__':
    unittest.main()


class DocsReviewTestCase(unittest.TestCase):
    """Docs review: fitEOS returns the parameters for every EOS (BM returned None); invalid Debye mode message."""

    def test_fitEOS_returns_parameters(self):
        d, V, E = data('Al_fcc')
        for name in ['BM', 'RV', 'MG', 'TB', 'MU', 'PT']:
            eos = getattr(pot, name)()
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                p = eos.fitEOS(V, E)
                q = eos.fitEOS(V, E, initial_parameters=eos.pEOS, fit=False)
            self.assertIsNotNone(p, name)
            np.testing.assert_array_equal(np.asarray(p), np.asarray(eos.pEOS), err_msg=name)
            np.testing.assert_array_equal(np.asarray(q), np.asarray(eos.pEOS), err_msg=name)

    def test_invalid_mode_names_the_valid_ones(self):
        from debyetools.ndeb import nDeb
        d, V, E = data('Al_fcc')
        eos = pot.BM()
        eos.fitEOS(V, E)
        with self.assertRaisesRegex(ValueError, "unknown mode 'jj'.*'jjsl'.*'jjdm'"):
            nDeb(0.3, 0.027, (0, 1), eos, (0, 0, 0, 0), (1e10, 0, 933, 0.1), (0, 0, 0), mode='jj')
