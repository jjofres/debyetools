import unittest
import numpy as np
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts
from debyetools.fs_compound_db import fit_FS, Cp2fit
import debyetools.potentials as potentials
from debyetools.electronic import fit_electronic
from debyetools.poisson import poisson_ratio
from debyetools.aux_functions import load_doscar, load_V_E, load_EM, load_cell
import os
HERE = os.path.dirname(os.path.abspath(__file__))  # test data paths are relative to this file

Pressure = 0
AL = os.path.join(HERE, 'inpt_files', 'Al_fcc')
AL_TAGS = ['%02da' % i for i in range(1, 22)]
# Regression values regenerated 2026-10-07 after the review fixes (D4 electronic, D7/D11 fit_FS with
# cp_T3=False). The test checks the whole chain: EOS fit, DOSCAR -> electronic fit, Poisson ratio,
# min_G, eval_props and the FactSage Cp fit (as the fitted curve, not the ill-conditioned coefficients).
T_CURVE = np.array([298.15, 500., 750., 1000.])


def run_chain(eos, V_start, m):
    V_DFT, E_DFT = load_V_E(AL + '/SUMMARY.fcc', AL + '/CONTCAR.5', units='J/mol')
    E, N, Ef = load_doscar(AL + '/DOSCAR.EvV.', list_filetags=AL_TAGS)
    p_electronic = fit_electronic(V_DFT, None, E, N, Ef)
    nu = poisson_ratio(load_EM(AL + '/OUTCAR.eps'))
    p_defects = 8.46, 1.69, 933, 0.1
    ndeb = nDeb(nu, m, (0, 1), eos, p_electronic, p_defects, (0, 0, 0), mode='jjsl')
    T = gen_Ts(0.1, 1000, 10)
    T, V = ndeb.min_G(T, V_start(eos), P=Pressure)
    tprops = ndeb.eval_props(T, V, P=Pressure)
    FS = fit_FS(tprops, 298.15, 1000)
    return T, tprops, FS


class CpTestCase(unittest.TestCase):

    def check(self, T, tprops, FS, Cp_expected, curve_expected):
        self.assertEqual(len(T), 11)                                   # no temperature dropped by min_G
        np.testing.assert_allclose(tprops['Cp'], Cp_expected, rtol=1e-6)
        self.assertEqual(FS['Cp'][5], 0)                               # T^-3 term off by default (D11)
        np.testing.assert_allclose(Cp2fit(T_CURVE, *FS['Cp']), curve_expected, rtol=1e-6)
        ok = T >= 298.15                                               # fit follows the model in its window
        self.assertLess(np.max(np.abs(Cp2fit(T[ok], *FS['Cp']) / tprops['Cp'][ok] - 1)), 5e-3)

    def test_Complete_Al_fcc_BM(self):
        """Complete chain for Al fcc with the 3rd-order Birch-Murnaghan EOS."""
        V_DFT, E_DFT = load_V_E(AL + '/SUMMARY.fcc', AL + '/CONTCAR.5', units='J/mol')
        eos = potentials.BM()
        eos.fitEOS(V_DFT, E_DFT, initial_parameters=[-3.6e+05, 9.9e-06, 7.8e+10, 4.7e+00])
        T, tprops, FS = run_chain(eos, lambda e: e.pEOS[1] * .9, 0.0269815)
        self.check(T, tprops, FS,
                   [1.065903754626e-04, 1.392659368475e+01, 2.213373640556e+01, 2.422394409468e+01,
                    2.488731521290e+01, 2.645669681196e+01, 2.774739094740e+01, 2.911062544999e+01,
                    3.085575711877e+01, 3.336597813656e+01, 3.716298085174e+01],
                   [24.255818597089, 27.165605733654, 30.319207087179, 37.128521663006])

    def test_Complete_Al_fcc_Morse(self):
        """Complete chain for Al fcc with the Morse pair potential."""
        V_DFT, E_DFT = load_V_E(AL + '/SUMMARY.fcc', AL + '/CONTCAR.5', units='J/mol')
        formula, primitive_cell, basis_vectors = load_cell(AL + '/CONTCAR.5')
        eos = potentials.MP(formula, primitive_cell, basis_vectors, 5, 3, units='J/mol')
        eos.fitEOS(V_DFT, E_DFT, initial_parameters=np.array([0.35, 1, 3.5]))
        T, tprops, FS = run_chain(eos, lambda e: e.V0, 0.026981500000000002)
        self.check(T, tprops, FS,
                   [1.068427865118e-04, 1.369450841661e+01, 2.189853578465e+01, 2.394966684406e+01,
                    2.458712831839e+01, 2.605040233977e+01, 2.719799756533e+01, 2.836744762890e+01,
                    2.983411811070e+01, 3.191364709465e+01, 3.498724882498e+01],
                   [23.973170416899, 26.677857251127, 29.392585815178, 34.962798319197])


if __name__ == '__main__':
    unittest.main()
