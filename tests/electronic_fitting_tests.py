import unittest
import numpy as np
from debyetools.electronic import fit_electronic, N_at_Fermi, NfV_poly_fun
from debyetools.aux_functions import load_doscar, load_V_E
import os
HERE = os.path.dirname(os.path.abspath(__file__))  # test data paths are relative to this file
AL = os.path.join(HERE, 'inpt_files', 'Al_fcc')
AL_TAGS = ['%02da' % i for i in range(1, 22)]


class ElectronicContributionFittingTestCase(unittest.TestCase):
    """N(E_F)(V) from the total DOS at every volume (review decision D4)."""

    def test_load_doscar_total_dos(self):
        """Total-DOS block only, spins summed, per atom: the DOS integrates to the valence count."""
        for folder, tags, valence in [(AL, AL_TAGS, 3), (os.path.join(HERE, 'inpt_files', 'Cu_fcc'), None, 11)]:
            E, N, Ef = load_doscar(folder + '/DOSCAR.EvV.', list_filetags=tags)
            self.assertEqual(len(E), 21)
            for e, n, ef in zip(E, N, Ef):
                self.assertEqual(len(e), 301)                 # NEDOS lines, no projected blocks
                self.assertTrue(np.all(np.diff(e) > 0))
                below = e <= ef
                ee = np.append(e[below], ef)
                nn = np.append(n[below], np.interp(ef, e, n))
                nel = np.sum(0.5 * (nn[1:] + nn[:-1]) * np.diff(ee))
                self.assertAlmostEqual(nel / valence, 1, delta=0.02)  # spin-up only would give 0.5

    def test_fit_exact_cubic(self):
        """A DOS whose N(E_F)(V) is an exact cubic is reproduced to round-off."""
        Vs = np.linspace(7.2e-6, 13.2e-6, 21)
        x = Vs / Vs.mean() - 1
        N_true = 0.5 + 0.8 * x - 0.6 * x ** 2 + 1.3 * x ** 3
        Eg = np.linspace(-5, 15, 301)
        E, N, Ef = [Eg] * 21, [0.1 + 0.05 * Eg] * 21, list((N_true - 0.1) / 0.05)
        q = fit_electronic(Vs, None, E, N, Ef)
        np.testing.assert_allclose(NfV_poly_fun(Vs, *q), N_true, rtol=1e-12)
        q1 = fit_electronic(Vs, None, E, N, Ef, order=1)
        self.assertEqual(q1[2], 0)
        self.assertEqual(q1[3], 0)

    def test_scaling_mode(self):
        """mode='scaling': N(E_F)(V) = N(E_F)(V0) (V/V0)^(2/3) from a single DOS."""
        Vs = np.linspace(7.2e-6, 13.2e-6, 21)
        V0 = 9.9e-6
        Eg = np.linspace(-5, 15, 301)
        q = fit_electronic(Vs, None, [Eg], [0.1 + 0.05 * Eg], [6.0], mode='scaling', V0=V0)
        np.testing.assert_allclose(NfV_poly_fun(Vs, *q), 0.4 * (Vs / V0) ** (2 / 3), rtol=1e-4)
        with self.assertRaises(ValueError):
            fit_electronic(Vs, None, [Eg], [0.1 + 0.05 * Eg], [6.0], mode='scaling')

    def test_length_mismatch(self):
        Vs = np.linspace(7.2e-6, 13.2e-6, 21)
        Eg = np.linspace(-5, 15, 301)
        with self.assertRaises(ValueError):
            fit_electronic(Vs, None, [Eg] * 20, [Eg] * 20, [1.0] * 20)

    def test_NfV_fitting_reading_from_DOSCAR(self):
        """Al fcc: fitted cubic follows N(E_F) of every DOSCAR; regression values."""
        V_DFT, E_DFT = load_V_E(AL + '/SUMMARY.fcc', AL + '/CONTCAR.5', units='J/mol')
        E, N, Ef = load_doscar(AL + '/DOSCAR.EvV.', list_filetags=AL_TAGS)
        NF = np.array([N_at_Fermi(E[i], N[i], Ef[i]) for i in range(21)])
        self.assertAlmostEqual(NF[10], 0.444126264408, places=10)
        p_el_optimal = fit_electronic(V_DFT, None, E, N, Ef)
        self.assertLess(np.sqrt(np.mean((NfV_poly_fun(V_DFT, *p_el_optimal) - NF) ** 2)), 0.03)
        np.testing.assert_allclose(p_el_optimal, [4.2770342390528375e+00, -6.1243936920817429e+05,
                                                  3.4610090270859642e+09, 1.9514025478772152e+15], rtol=1e-8)


if __name__ == '__main__':
    unittest.main()
