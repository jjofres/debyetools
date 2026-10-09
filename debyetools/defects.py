import numpy as np
np.seterr(divide='ignore')

from debyetools.constants import kB, NAv

class Defects:
    """
    Contribution of thermally activated mono-vacancies to the free energy (J/mol-at):
    F_def = -r N_A k_B T exp((T S_vac - E_vac(V)) / (k_B T))  (SM eq. S.61),
    E_vac(V) = Evac00 k_B Tm - (V0 / r) a (V - V0) P2 / (N_A V)  (J per vacancy; V0 / (r N_A) = volume per atom),
    S_vac = Svac00 k_B.

    :param float Evac00: Formation energy of vacancies in units of k_B Tm (dimensionless).
    :param float Svac00: Formation entropy of vacancies in units of k_B (dimensionless).
    :param float Tm: Melting temperature in K.
    :param float a: Dimensionless coefficient of the volume dependence of E_vac.
    :param float P2: Bulk modulus in Pa (nDeb passes B0 = V0 E0''(V0) of the EOS).
    :param float V0: Equilibrium volume in m^3/mol-at (nDeb passes EOS.V0).
    :param float r: Number of atoms in the chemical formula (default 1; keep 1 for per-mol-atom inputs);
        E, S, F and all derivatives carry the factor r.
    """
    def __init__(self, Evac00: float, Svac00: float, Tm: float, a: float, P2: float, V0: float, r: float = 1):
        self.r = r
        self.pdef = Evac00,Svac00,Tm,a,P2,V0
        self.Evac00 = Evac00
        self.Svac00 = Svac00
        self.Svac0 = Svac00*kB
        self.Evac0 = Evac00*kB*Tm
        self.Tm=Tm
        self.a = a
        self.P2 = P2
        self.V0=V0

    def Svac(self, V: float) -> float:
        """
        Entropy of formation of vacancies.

        :param float V: Volume.
        :return: Svac0
        :rtype: float
        """

        return self.Svac0
    def dSvacdV_T(self, V: float) -> float:
        """
        Volume-derivative of the entropy of formation of vacancies.

        :param float V: Volume.
        :return: 0
        """
        return 0
    def d2SvacdV2_T(self, V: float) -> float:
        """
        Volume-derivative of the entropy of formation of vacancies.

        :param float V: Volume.
        :return: 0
        """
        return 0
    def d3SvacdV3_T(self, V: float) -> float:
        """
        Volume-derivative of the entropy of formation of vacancies.

        :param float V: Volume.
        :return: 0
        """
        return 0
    def d4SvacdV4_T(self, V: float) -> float:
        """
        Volume-derivative of the entropy of formation of vacancies.

        :param float V: Volume.
        :return: 0
        """
        return 0
    def Evac(self, V: float) -> float:
        """
        Enthalpy of formation of vacancies.

        :param float V: Volume.
        :return: Ef(V)
        :rtype: float
        """
        return self.Evac0 - self.V0*self.a/self.r*(V - self.V0)*self.P2/(NAv*V)
    def dEvacdV_T(self, V: float) -> float:
        """
        Volume-derivative of the enthalpy of formation of vacancies.

        :param float V: Volume.
        :return: Volume-derivative of the enthalpy of formation of vacancies.
        :rtype: float
        """
        return -self.V0*self.a/self.r*self.P2/(NAv*V)+self.V0*self.a/self.r*(V-self.V0)*self.P2/(NAv*V**2)
    def d2EvacdV2_T(self, V: float) -> float:
        """
        Volume-derivative of the enthalpy of formation of vacancies.

        :param float V: Volume.
        :return: Volume-derivative of the enthalpy of formation of vacancies.
        :rtype: float
        """
        return 2*self.V0*self.a/self.r*self.P2/(NAv*V**2)-2*self.V0*self.a/self.r*(V-self.V0)*self.P2/(NAv*V**3)
    def d3EvacdV3_T(self, V: float) -> float:
        """
        Volume-derivative of the enthalpy of formation of vacancies.

        :param float V: Volume.
        :return: Volume-derivative of the enthalpy of formation of vacancies.
        :rtype: float
        """
        return -6*self.V0*self.a/self.r*self.P2/(NAv*V**3)+6*self.V0*self.a/self.r*(V-self.V0)*self.P2/(NAv*V**4)
    def d4EvacdV4_T(self, V: float) -> float:
        """
        Volume-derivative of the enthalpy of formation of vacancies.

        :param float V: Volume.
        :return: Volume-derivative of the enthalpy of formation of vacancies.
        :rtype: float
        """
        return 24*self.V0*self.a/self.r*self.P2/(NAv*V**4)-24*self.V0*self.a/self.r*(V-self.V0)*self.P2/(NAv*V**5)

    def _E_1(self, T: float, V: float) -> float:
        """
        Defects energy.

        :param float T: Temperature.
        :param float V: Volume
        :return: E_def
        :rtype: float
        """
        return self.Evac(V)*NAv*np.exp(self.Svac(V)/kB - self.Evac(V)/(kB*T))
    def _S_1(self, T: float, V: float) -> float:
        """
        Defects entropy.

        :param float T: Temperature.
        :param float V: Volume
        :return: S_def
        :rtype: float
        """
        return (T*kB+self.Evac(V))*NAv*np.exp(self.Svac(V)/kB - self.Evac(V)/(kB*T))/T
    def _F_1(self, T: float, V: float) -> float:
        """
        Implementation of the defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: energy
        :rtype: float
        """
        return -NAv*T*kB*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))
    def _dFdV_T_1(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))

    def _dFdT_V_1(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*kB*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*T*kB*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))
    def _d2FdT2_V_1(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*self.Evac(V)**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T**3*kB)
    def _d2FdV2_T_1(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -(-(self.d2EvacdV2_T(V))*T*kB+(self.d2SvacdV2_T(V))*T**2*kB+((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))**2)*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))*NAv/(T*kB)
    def _d3FdV3_T_1(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*(self.d3SvacdV3_T(V)*T-self.d3EvacdV3_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-3*NAv*(self.d2SvacdV2_T(V)*T-self.d2EvacdV2_T(V))*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)-NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))**3*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T**2*kB**2)
    def _d4FdV4_T_1(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        # F = -NAv kB T exp(u), u = g/(kB T), g = T Svac - Evac; Faa di Bruno for exp(u):
        # d4F/dV4 = -NAv exp(u) [g4 + (4 g1 g3 + 3 g2^2)/(kB T) + 6 g1^2 g2/(kB T)^2 + g1^4/(kB T)^3]
        # (the last two terms were missing, finding 5.5)
        kT = kB*T
        g1 = self.dSvacdV_T(V)*T - self.dEvacdV_T(V)
        g2 = self.d2SvacdV2_T(V)*T - self.d2EvacdV2_T(V)
        g3 = self.d3SvacdV3_T(V)*T - self.d3EvacdV3_T(V)
        g4 = self.d4SvacdV4_T(V)*T - self.d4EvacdV4_T(V)
        eu = np.exp((self.Svac(V)*T-self.Evac(V))/kT)
        return -NAv*eu*(g4 + (4*g1*g3 + 3*g2**2)/kT + 6*g1**2*g2/kT**2 + g1**4/kT**3)

    def _d2FdVdT_1(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))*(T*(T*kB+self.Evac(V))*(self.dSvacdV_T(V))-(self.dEvacdV_T(V))*self.Evac(V))*NAv/(T**2*kB)
    def _d3FdV2dT_1(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*(self.d2SvacdV2_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*((self.d2SvacdV2_T(V))*T-(self.d2EvacdV2_T(V)))*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-2*NAv*((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))*(self.dSvacdV_T(V))/(T*kB)+NAv*((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T**2*kB)-NAv*((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))**2*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)
    def _d3FdVdT2_1(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -2*NAv*self.dSvacdV_T(V)*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*(-2*self.Svac(V)/(T**2*kB)+(2*(self.Svac(V)*T-self.Evac(V)))/(T**3*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))

    # Public methods: r times the r = 1 expressions above, so that every derivative carries the same
    # factor r as the function itself (review decision D5).
    def E(self, T: float, V: float) -> float:
        """E of F_def (r times the r = 1 value)."""
        return self.r * self._E_1(T, V)

    def S(self, T: float, V: float) -> float:
        """S of F_def (r times the r = 1 value)."""
        return self.r * self._S_1(T, V)

    def F(self, T: float, V: float) -> float:
        """F of F_def (r times the r = 1 value)."""
        return self.r * self._F_1(T, V)

    def dFdV_T(self, T: float, V: float) -> float:
        """(dF/dV)_T of F_def (r times the r = 1 value)."""
        return self.r * self._dFdV_T_1(T, V)

    def dFdT_V(self, T: float, V: float) -> float:
        """(dF/dT)_V of F_def (r times the r = 1 value)."""
        return self.r * self._dFdT_V_1(T, V)

    def d2FdT2_V(self, T: float, V: float) -> float:
        """(d2F/dT2)_V of F_def (r times the r = 1 value)."""
        return self.r * self._d2FdT2_V_1(T, V)

    def d2FdV2_T(self, T: float, V: float) -> float:
        """(d2F/dV2)_T of F_def (r times the r = 1 value)."""
        return self.r * self._d2FdV2_T_1(T, V)

    def d3FdV3_T(self, T: float, V: float) -> float:
        """(d3F/dV3)_T of F_def (r times the r = 1 value)."""
        return self.r * self._d3FdV3_T_1(T, V)

    def d4FdV4_T(self, T: float, V: float) -> float:
        """(d4F/dV4)_T of F_def (r times the r = 1 value)."""
        return self.r * self._d4FdV4_T_1(T, V)

    def d2FdVdT(self, T: float, V: float) -> float:
        """d2F/dVdT of F_def (r times the r = 1 value)."""
        return self.r * self._d2FdVdT_1(T, V)

    def d3FdV2dT(self, T: float, V: float) -> float:
        """d3F/dV2dT of F_def (r times the r = 1 value)."""
        return self.r * self._d3FdV2dT_1(T, V)

    def d3FdVdT2(self, T: float, V: float) -> float:
        """d3F/dVdT2 of F_def (r times the r = 1 value)."""
        return self.r * self._d3FdVdT2_1(T, V)
