"""load_V_E: energy read by label, E0= (sigma -> 0) by default, F= on request, positional fallback (C-DOC3)."""
import os
import tempfile
import unittest
import warnings
import numpy as np
from debyetools.aux_functions import load_V_E
from debyetools.constants import EV_ATOM_TO_J_MOL

HERE = os.path.dirname(os.path.abspath(__file__))
AL = os.path.join(HERE, 'inpt_files', 'Al_fcc')


def column(path, label):
    out = []
    for l in open(path).read().splitlines():
        t = l.split()
        if t:
            out.append(float(t[t.index(label) + 1]))
    return np.array(out)


class LoadVETestCase(unittest.TestCase):

    def setUp(self):
        self.summ, self.cont = AL + '/SUMMARY.fcc', AL + '/CONTCAR.5'

    def test_default_reads_E0(self):
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            V, E = load_V_E(self.summ, self.cont)
        np.testing.assert_allclose(E, column(self.summ, 'E0=') / 4, rtol=1e-14)

    def test_F_on_request(self):
        V, F = load_V_E(self.summ, self.cont, energy='F')
        np.testing.assert_allclose(F, column(self.summ, 'F=') / 4, rtol=1e-14)
        V0, E0 = load_V_E(self.summ, self.cont)
        np.testing.assert_array_equal(V, V0)
        # Fermi smearing, SIGMA = 0.1 eV: F < E0 by 2-4 meV/atom, more at larger volume
        self.assertTrue(np.all((F - E0 < -2e-3) & (F - E0 > -4.1e-3)))
        self.assertLess((F - E0)[-1], (F - E0)[0])

    def test_units_J_mol(self):
        _, E = load_V_E(self.summ, self.cont)
        _, EJ = load_V_E(self.summ, self.cont, units='J/mol')
        np.testing.assert_allclose(EJ, E * EV_ATOM_TO_J_MOL, rtol=1e-14)

    def test_unlabelled_lines_read_column_4_with_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, 'SUMMARY')
            with open(p, 'w') as f:
                f.write('0.00 x x -14.9\n0.01 x x -14.8\n')
            with self.assertWarns(UserWarning):
                _, E = load_V_E(p, self.cont)
        np.testing.assert_allclose(E, [-14.9 / 4, -14.8 / 4])

    def test_E0_placeholder_reads_F(self):
        """Some test sets (CaO, InP, NaCl, Si) write 'E0= 0' as a placeholder: F= is read, with a warning."""
        d = os.path.join(HERE, 'inpt_files', 'CaO_Fm3m')
        with self.assertWarns(UserWarning):
            _, E = load_V_E(d + '/SUMMARY.fcc', d + '/CONTCAR.5')
        _, F = load_V_E(d + '/SUMMARY.fcc', d + '/CONTCAR.5', energy='F')
        np.testing.assert_array_equal(E, F)
        self.assertTrue(np.all(E < -5))

    def test_label_without_space(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, 'SUMMARY')
            with open(p, 'w') as f:
                f.write('0.00 1 F=-.12E+02 E0=-.11E+02 d E =-.1E-01\n')
            self.assertAlmostEqual(load_V_E(p, self.cont)[1][0], -11 / 4)
            self.assertAlmostEqual(load_V_E(p, self.cont, energy='F')[1][0], -12 / 4)

    def test_invalid_energy(self):
        with self.assertRaises(ValueError):
            load_V_E(self.summ, self.cont, energy='TOTEN')


if __name__ == '__main__':
    unittest.main()
