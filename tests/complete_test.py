import unittest
import numpy as np
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts
from debyetools.fs_compound_db import fit_FS
import debyetools.potentials as potentials
from debyetools.electronic import fit_electronic
from debyetools.poisson import poisson_ratio
from debyetools.aux_functions import load_doscar, load_V_E, load_EM, load_cell

Pressure = 0


class CpTestCase(unittest.TestCase):
    def setUp(self):
        # self.NL = PairAnalysisCalculator()
        pass

    def test_Complete_Al_fcc_BM4(self):
        """ Test complete algorithm to calculate TP for Al fcc using the 4th order Birch-Murnaghan EOS."""

        folder_name = './inpt_files/Al_fcc'
        # EOS parametrization
        # =========================
        V_DFT, E_DFT = load_V_E(folder_name, folder_name + '/CONTCAR.5', units='J/mol')
        EOS_name = 'BM4'
        initial_parameters = [-3.6e+05, 9.9e-06, 7.8e+10, 4.7e+00, 1.e-10]
        eos_BM4 = getattr(potentials, EOS_name)()
        eos_BM4.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters)
        p_EOS = eos_BM4.pEOS
        # =========================

        # Electronic Contributions
        # =========================
        p_el_inittial = [3.8027342892e-01, -1.8875015171e-02,
                         5.3071034596e-04, -7.0100707467e-06]
        E, N, Ef = load_doscar(folder_name + '/DOSCAR.EvV.')
        p_electronic = fit_electronic(V_DFT, p_el_inittial, E, N, Ef)
        # =========================

        # Other Contributions parametrization
        # =========================
        Tmelting = 933
        p_defects = 8.46, 1.69, Tmelting, 0.1
        p_intanh = 0, 1
        p_anh = 0, 0, 0
        # =========================

        # Poisson's ratio
        # =========================
        EM = EM = load_EM(folder_name + '/OUTCAR.eps')
        nu = poisson_ratio(EM)
        # =========================

        # F minimization
        # =========================
        m = 0.026981500000000002
        ndeb_BM4 = nDeb(nu, m, p_intanh, eos_BM4, p_electronic, p_defects, p_anh, mode='jj')

        T_initial, T_final, number_Temps = 0.1, 1000, 10
        T = gen_Ts(T_initial, T_final, number_Temps)

        T, V = ndeb_BM4.min_G(T, p_EOS[1] * .9, P=Pressure)
        # =========================

        # Evaluations
        # =========================
        tprops_dict = ndeb_BM4.eval_props(T, V, P=Pressure)

        T_from = 298.15
        T_to = 1000
        # =========================

        # FS comp db parameters
        # =========================
        FS_db_params = fit_FS(tprops_dict, T_from, T_to)
        print('yyyy', FS_db_params['Cp'])
        # =========================

        np.testing.assert_almost_equal(np.sum(FS_db_params['Cp'])/10,
                                       np.sum([1.55473717e+02, -1.22152871e-01, 1.22933082e+06, 6.37489482e-05,
                                               -1.97628077e+03, 1.00000000e+00])/10, decimal=1)

    def test_Complete_Al_fcc_Morse(self):
        """ Test complete algorithm to calculate TP for Al fcc using the 4th order Birch-Murnaghan EOS."""

        folder_name = './inpt_files/Al_fcc'
        # EOS parametrization
        # =========================
        V_DFT, E_DFT = load_V_E(folder_name, folder_name + '/CONTCAR.5', units='J/mol')

        formula, primitive_cell, sbasis_vectors = load_cell(folder_name + '/CONTCAR.5')

        EOS_name = 'MP'
        cutoff = 5
        number_of_neighbor_levels = 3
        eos_Morse = getattr(potentials, EOS_name)(formula, primitive_cell, sbasis_vectors, cutoff,
                                                  number_of_neighbor_levels, units='J/mol')
        initial_parameters = np.array([0.35, 1, 3.5])

        eos_Morse.fitEOS(V_DFT, E_DFT, initial_parameters=initial_parameters)
        p_EOS = eos_Morse.pEOS
        # =========================

        # Electronic Contributions
        # =========================
        p_el_inittial = [3.8027342892e-01, -1.8875015171e-02,
                         5.3071034596e-04, -7.0100707467e-06]
        E, N, Ef = load_doscar(folder_name + '/DOSCAR.EvV.')
        p_electronic = fit_electronic(V_DFT, p_el_inittial, E, N, Ef)
        # =========================

        # Other Contributions parametrization
        # =========================
        Tmelting = 933
        p_defects = 8.46, 1.69, Tmelting, 0.1
        p_intanh = 0, 1
        p_anh = 0, 0, 0
        # =========================

        # Poisson's ratio
        # =========================
        EM = EM = load_EM(folder_name + '/OUTCAR.eps')
        nu = poisson_ratio(EM)
        # =========================

        # F minimization
        # =========================
        m = 0.026981500000000002
        ndeb_Morse = nDeb(nu, m, p_intanh, eos_Morse, p_electronic,
                          p_defects, p_anh, mode='jj')

        T_initial, T_final, number_Temps = 0.1, 1000, 10
        T = gen_Ts(T_initial, T_final, number_Temps)

        T, V = ndeb_Morse.min_G(T, ndeb_Morse.EOS.V0, P=Pressure)
        # =========================

        # Evaluations
        # =========================
        tprops_dict = ndeb_Morse.eval_props(T, V, P=Pressure)
        # =========================

        # FS comp db parameters
        # =========================
        T_from = 298.15
        T_to = 1000
        FS_db_params = fit_FS(tprops_dict, T_from, T_to)
        print('xxxx', FS_db_params['Cp'])

        # =========================

        np.testing.assert_almost_equal(np.sum(FS_db_params['Cp'])/10,
                               np.sum([1.11506748e+02, -8.08764375e-02, 7.35338964e+05, 4.28319803e-05,
                                       -1.30713807e+03, 1])/10, decimal=1)


if __name__ == '__main__':
    unittest.main()
