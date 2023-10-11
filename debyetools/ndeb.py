import numpy as np
# from scipy.optimize import fmin
from scipy import optimize

from debyetools.anharmonicity import Anharmonicity, intAnharmonicity
from debyetools.electronic import Electronic
from debyetools.defects import Defects
from debyetools.vibrational import Vibrational
# import debyetools.potentials as pots
from debyetools.debfunct import D_3#, dD_3dx, d2D_3dx2, d3D_3dx3

from typing import Tuple

hbar = 0.1054571800e-33
NAv = 0.6022140857e24
kB = 0.138064852e-22


class nDeb:
    """
    Instantiate an object that contains all the parameters for the evaluation of
    the thermodynamic properties of a certain element or compound. Also contains
    the method that implements an original Debye formalism for the calculation of
    the thermodynamic properties.

    :param float nu: Poisson's ratio.
    :param float m: mass in Kg/mol-at
    :param np.ndarray p_intanh: Intrinsic anharmonicity parameters: a0, m0, V0.
    :param object EOS: Equation of state instance.
    :param np.ndarray p_electronic: Electronic contribution parameters.
    :param np.ndarray p_defects: Mono-vacancies defects contribution parameters: Evac00,Svac00,Tm,a,P2,V0.
    :param np.ndarray p_anh: Excess contribution parameters.
    :param str mode: Type of approximation of the Debye temperature (see vibrational contribution).
    """

    def __init__(self, nu: float, m: float, p_intanh: np.ndarray, EOS: object, p_electronic: np.ndarray, p_defects: np.ndarray, p_anh: np.ndarray, *args: object, units: str = 'J/mol',
                 mode: str = 'jjsl'):

        a0, m0 = p_intanh
        q0, q1, q2, q3 = p_electronic
        Evac00, Svac00, Tm, a = p_defects
        s0, s1, s2 = p_anh

        self.nu, self.r, self.m = nu, 1, m
        self.mode = mode

        self.kv = (2. / 3. * ((2. + 2. * nu) / (3. - 6. * nu)) ** (3. / 2.) + 1. / 3. * (
                    (1. + nu) / (3. - 3. * nu)) ** (3. / 2.)) ** (-1. / 3.)

        self.anh = Anharmonicity(s0, s1, s2)
        self.intanh = intAnharmonicity(a0, m0, EOS.V0)
        self.el = Electronic(q0, q1, q2, q3)
        self.deff = Defects(Evac00, Svac00, Tm, a, EOS.V0 * EOS.d2E0dV2_T(EOS.V0), EOS.V0)

        self.EOS = EOS  # getattr(pots,EOS_name)(*args,units=units, parameters = p_EOS)
        # self.EOS.pEOS = p_EOS
        self.vib = Vibrational(nu, self.EOS, m, self.intanh, mode)

        r = 1
        self.xDcte = hbar * 6 ** (1 / 3.) * (np.pi ** 2 * NAv * r) ** (1 / 3.)

    def f2min(self, T: float, V: float, P: float) -> float:
        """
        free energy for minimization.

        :param float T: Temperature.
        :param float V: Volume.
        :param float P: Pressure.

        :return: Free energy.
        :rtype: float
        """
        # self.vib.set_int_anh_4minF(T, V)
        # self.vib.set_theta_4minF(T,V)
        self.vib.set_int_anh(T, V)
        self.vib.set_theta(T, V)

        E0 = self.EOS.E0(V)
        Fvib = self.vib.F(T,V)
        Fel = self.el.F(T,V)
        Fdef = self.deff.F(T,V)
        Fa = self.anh.F(T,V)
        F = E0 + Fvib + Fel + Fdef + Fa
        return F+P*V#(dFdV_T + P)**2

    def min_G(self, T: np.ndarray, initial_V: float, P: float) -> Tuple[np.ndarray,np.ndarray]:
        """
        Procedure for the calculation of the volume as function of temperature.

        :param list_of_floats T: Temperature.
        :param float initial_V: initial guess.
        :param float P: Pressure.
        :return: Temperature and Volume
        :rtype: Tuple[np.ndarray,np.ndarray]

        """
        V0i = initial_V
        V = []
        for Ti in T[0:1]:
            f2min = lambda Vi: self.f2min(Ti, Vi, P)
            V0i = optimize.fmin(f2min, x0=V0i, disp=False)[0]
            # V0i = fmin(f2min, x0=V0i, disp=False)[0]
            V.append(V0i)
        if self.mode == '':
            pass
        else:
            self.vib.V0_DM = V[0]
        V = []
        for Ti in T:
            f2min = lambda Vi: self.f2min(Ti, Vi, P)
            # f2min = lambda Vi: 1e3*(self.dGdV_T(Ti,Vi,P=P))**2
            V0i = optimize.fmin(f2min, x0=V0i, disp=False)[0]
            V.append(V0i)


        newV = np.array(V)  # V[0]*np.exp(self.integrl())
        del V

        ixs = np.where(newV <= 1.5 * newV[0])
        # Tmax = T[-1]
        T, V = T[ixs], newV[ixs]

        return T, V

    def eval_props(self, T: np.ndarray, V: np.ndarray, P = None) -> dict:
        """
        Evaluates the thermodynamic properties of a given compound/element at (T,V).

        :param np.ndarray T: The temperature in Kelvin.
        :param np.ndarray V: The volume in "units".
        :return: A dictionary with the following keys: 'T': temperature, 'V': volume, 'tD': Debye temperature, 'g': Gruneisen parameter, 'Kt': isothermal bulk modulus, 'Ktp': pressure derivative of the isothermal bulk modulus, 'Ktpp': second order pressure derivative of the isothermal bulk modulus, 'Cv': constant-volume heat capacity, 'a': thermal expansion, 'Cp': constant-pressure heat capacity, 'Ks': adiabatic bulk modulus , 'Ksp': pressure derivative of the adiabatic bulk modulus, 'G': Gibbs free energy, 'E': total internal energy, 'S': entropy, 'E0': 'cold' internal energy defined by the EOS, 'Fvib': vibrational free energy, 'Evib': vibrational internal energy, 'Svib': vibrational entropy, 'Cvvib': vibrational heat capacity, 'Pcold': 'cold' pressure, 'dPdT_V': (dP/dT)_V, 'G^2': Ktp**2-2*Kt*Ktpp, 'dSdP_T': (dS/dP)_T, 'dKtdT_P': (dKt/dT)_P, 'dadP_T': (da/dP)_T, 'dCpdP_T': (dCp/dP)_T, 'ddSdT_PdP_T': (d2S/dTdP).
        :rtype: dict
        """
        del P
        # nu, r, m = self.nu, self.r, self.m

        # kv = self.kv

        self.vib.set_int_anh(T, V)
        self.vib.set_theta(T, V)

        E0 = self.EOS.E0(V)

        dE0dV_T   = self.EOS.dE0dV_T(V)
        d2E0dV2_T = self.EOS.d2E0dV2_T(V)
        d3E0dV3_T = self.EOS.d3E0dV3_T(V)
        d4E0dV4_T = self.EOS.d4E0dV4_T(V)
        dE0dT_V = 0
        d2E0dT2_V = 0
        d2E0dVdT = 0
        d3E0dV2dT = 0
        d3E0dVdT2 = 0

        Fvib = self.vib.F(T, V)
        Svib = -self.vib.dFdT_V(T, V)
        Evib = Fvib + T*Fvib

        dFvibdV_T = self.vib.dFdV_T(T,V)
        dFvibdT_V = self.vib.dFdT_V(T,V)
        d2FvibdT2_V = self.vib.d2FdT2_V(T,V)
        d2FvibdV2_T = self.vib.d2FdV2_T(T,V)
        d3FvibdV3_T = self.vib.d3FdV3_T(T,V)
        d4FvibdV4_T = self.vib.d4FdV4_T(T,V)
        d2FvibdVdT = self.vib.d2FdVdT(T,V)
        d3FvibdV2dT = self.vib.d3FdV2dT(T,V)
        d3FvibdVdT2 = self.vib.d3FdVdT2(T,V)

        # Eel = self.el.E(T, V)
        # Sel = self.el.S(T, V)
        Fel = self.el.F(T, V)
        dFeldV_T = self.el.dFdV_T(T, V)
        dFeldT_V = self.el.dFdT_V(T, V)
        d2FeldT2_V = self.el.d2FdT2_V(T, V)
        d2FeldV2_T = self.el.d2FdV2_T(T, V)
        d3FeldV3_T = self.el.d3FdV3_T(T, V)
        d4FeldV4_T = self.el.d4FdV4_T(T, V)
        d2FeldVdT = self.el.d2FdVdT(T, V)
        d3FeldV2dT = self.el.d3FdV2dT(T, V)
        d3FeldVdT2 = self.el.d3FdVdT2(T, V)

        # Edef = self.deff.E(T, V)
        # Sdef = self.deff.S(T, V)
        Fdef = self.deff.F(T, V)
        dFdefdV_T = self.deff.dFdV_T(T, V)
        dFdefdT_V = self.deff.dFdT_V(T, V)
        d2FdefdT2_V = self.deff.d2FdT2_V(T, V)
        d2FdefdV2_T = self.deff.d2FdV2_T(T, V)
        d3FdefdV3_T = self.deff.d3FdV3_T(T, V)
        d4FdefdV4_T = self.deff.d4FdV4_T(T, V)
        d2FdefdVdT = self.deff.d2FdVdT(T, V)
        d3FdefdV2dT = self.deff.d3FdV2dT(T, V)
        d3FdefdVdT2 = self.deff.d3FdVdT2(T, V)

        # Ea = self.anh.E(T, V)
        # Sa = self.anh.S(T, V)
        Fa = self.anh.F(T, V)
        dFadV_T = self.anh.dFdV_T(T, V)
        d2FadT2_V = self.anh.d2FdT2_V(T, V)
        dFadT_V = self.anh.dFdT_V(T, V)
        d2FadV2_T = self.anh.d2FdV2_T(T, V)
        d3FadV3_T = self.anh.d3FdV3_T(T, V)
        d4FadV4_T = self.anh.d4FdV4_T(T, V)
        d2FadVdT = self.anh.d2FdVdT(T, V)
        d3FadV2dT = self.anh.d3FdV2dT(T, V)
        d3FadVdT2 = self.anh.d3FdVdT2(T, V)

        dFdV_T = dE0dV_T + dFvibdV_T + dFeldV_T + dFdefdV_T + dFadV_T
        d2FdV2_T = d2E0dV2_T + d2FvibdV2_T + d2FeldV2_T + d2FdefdV2_T + d2FadV2_T
        d3FdV3_T = d3E0dV3_T + d3FvibdV3_T + d3FeldV3_T + d3FdefdV3_T + d3FadV3_T
        d4FdV4_T = d4E0dV4_T + d4FvibdV4_T + d4FeldV4_T + d4FdefdV4_T + d4FadV4_T
        d2FdT2_V = d2E0dT2_V + d2FvibdT2_V + d2FeldT2_V + d2FdefdT2_V + d2FadT2_V
        d2FdVdT = d2E0dVdT + d2FvibdVdT + d2FeldVdT + d2FdefdVdT + d2FadVdT
        d3FdV2dT = d3E0dV2dT + d3FvibdV2dT + d3FeldV2dT + d3FdefdV2dT + d3FadV2dT
        d3FdVdT2 = d3E0dVdT2 + d3FvibdVdT2 + d3FeldVdT2 + d3FdefdVdT2 + d3FadVdT2

        dFdT_V = dE0dT_V + dFvibdT_V + dFeldT_V + dFdefdT_V + dFadT_V

        tD = self.vib.tD
        g = -V / (tD) * self.vib.dtDdV_T
        dPdV_T = - d2FdV2_T
        d2PdV2_T = - d3FdV3_T
        d3PdV3_T = - d4FdV4_T
        Kt = - V * dPdV_T
        dKtdV_T = - dPdV_T - V * d2PdV2_T
        dKtdP_T = dKtdV_T / dPdV_T
        d2KtdV2_T = -2 * d2PdV2_T - V * d3PdV3_T
        d2KtdP2_T = (d2KtdV2_T / dPdV_T - dKtdV_T * d2PdV2_T / dPdV_T ** 2) / dPdV_T
        Ktp = dKtdP_T
        Ktpp = d2KtdP2_T
        Cv = -T * d2FdT2_V
        dPdT_V = - d2FdVdT
        dVdT_P = - dPdT_V / dPdV_T
        a = 1 / V * dVdT_P

        Cp = -T * (d2FdT2_V - (d2FdVdT) ** 2 / d2FdV2_T)

        Ks = Kt * Cp / Cv
        dCpdV_T = T * (
                    2 * d2FdVdT * d2FdV2_T * d3FdV2dT - d2FdVdT ** 2 * d3FdV3_T - d3FdVdT2 * d2FdV2_T ** 2) / d2FdV2_T ** 2
        dCvdV_T = -T * d3FdVdT2
        dKsdV_T = dKtdV_T * Cp / Cv + Kt * dCpdV_T / Cv - Kt * Cp * dCvdV_T / Cv ** 2

        dKsdP_T = dKsdV_T / dPdV_T
        Ksp = dKsdP_T

        S = -dFdT_V

        F = E0 + Fvib + Fel + Fdef + Fa
        E = F + T*S
        G = F - dFdV_T*V

        Cvvib = -T * d2FvibdT2_V
        dE0dV_T = self.EOS.dE0dV_T(V)
        Pcold = -dE0dV_T

        dSdV_T = - d2FdVdT
        dSdP_T = dSdV_T / dPdV_T

        #  _dKtdT_P = _dKtdT_V + _dKtdV_T*_dVdT_P
        d2PdVdT = - d3FdV2dT
        dKtdT_V = - V * d2PdVdT
        ddVdT_PdV_T = - d2PdVdT / dPdV_T + dPdT_V / (dPdV_T) ** 2 * d2PdV2_T
        dKtdT_P = dKtdT_V + dKtdV_T * dVdT_P
        dadV_T = -1 / V ** 2 * dVdT_P + 1 / V * ddVdT_PdV_T
        dadP_T = dadV_T / dPdV_T

        dCpdP_T = dCpdV_T / dPdV_T

        # dSdV_T = dSvibdV_T + dSdefdV_T + dSeldV_T + dSadV_T
        d2SdTdV = - d3FdVdT2  # d2SvibdVdT + d2SeldVdT + d2SdefdVdT + d2SadVdT
        d2SdV2_T = - d3FdV2dT  # _d2SvibdV2_T + d2SeldV2_T + d2SdefdV2_T + d2SadV2_T
        ddSdT_PdP_T = (d2SdTdV + d2SdV2_T * dVdT_P + dSdV_T * ddVdT_PdV_T) / dPdV_T
        return {'T': T, 'V': V, 'tD': tD, 'g': g, 'Kt': Kt, 'Ktp': Ktp, 'Ktpp': Ktpp,
                'Cv': Cv, 'a': a, 'Cp': Cp, 'Ks': Ks, 'Ksp': Ksp,
                'G': G, 'E': E, 'S': S, 'E0': E0, 'Fvib': Fvib, 'Evib': Evib, 'Svib': Svib,
                'Cvvib': Cvvib, 'Pcold': Pcold, 'dPdT_V': dPdT_V, 'G^2': Ktp ** 2 - 2 * Kt * Ktpp,
                'dSdP_T': dSdP_T, 'dKtdT_P': dKtdT_P, 'dadP_T': dadP_T, 'dCpdP_T': dCpdP_T, 'ddSdT_PdP_T': ddSdT_PdP_T,
                'P': -dFdV_T,
                'dtDdV_T':self.vib.dtDdV_T,'d2tDdV2_T':self.vib.d2tDdV2_T, 'D_3':D_3(tD/T),
                'd2E0dV2_T':d2E0dV2_T, 'dPdV_T':dPdV_T,
                'dE0dV_T':dE0dV_T, 'd3E0dV3_T':d3E0dV3_T, 'Fa':Fa, 'Fdef':Fdef, 'Fel': Fel
                }
