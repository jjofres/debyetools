import numpy as np
np.seterr(divide='ignore')

kB   = 0.138064852e-22
NAv  = 0.6022140857e24

class Defects:
    """
    Implementation of the defects contribution due to monovancies to the free energy.

    :param float Evac00: Fomration energy of vacancies.
    :param float Svac00: Fomration entropy of vacancies.
    :param float Tm: Melting temperature.
    :param float a: Volume ratio of a mono vacancie relative to the equilibrium volume.
    :param float P2: Bulk modulus.
    :param float V0: Equilibrium volume.
    """
    def __init__(self, Evac00: float, Svac00: float, Tm: float, a: float, P2: float, V0: float):
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
        return self.Evac0 - self.V0*self.a*(V - self.V0)*self.P2/(NAv*V)
    def dEvacdV_T(self, V: float) -> float:
        """
        Volume-derivative of the enthalpy of formation of vacancies.

        :param float V: Volume.
        :return: Volume-derivative of the enthalpy of formation of vacancies.
        :rtype: float
        """
        return -self.V0*self.a*self.P2/(NAv*V)+self.V0*self.a*(V-self.V0)*self.P2/(NAv*V**2)
    def d2EvacdV2_T(self, V: float) -> float:
        """
        Volume-derivative of the enthalpy of formation of vacancies.

        :param float V: Volume.
        :return: Volume-derivative of the enthalpy of formation of vacancies.
        :rtype: float
        """
        return 2*self.V0*self.a*self.P2/(NAv*V**2)-2*self.V0*self.a*(V-self.V0)*self.P2/(NAv*V**3)
    def d3EvacdV3_T(self, V: float) -> float:
        """
        Volume-derivative of the enthalpy of formation of vacancies.

        :param float V: Volume.
        :return: Volume-derivative of the enthalpy of formation of vacancies.
        :rtype: float
        """
        return -6*self.V0*self.a*self.P2/(NAv*V**3)+6*self.V0*self.a*(V-self.V0)*self.P2/(NAv*V**4)
    def d4EvacdV4_T(self, V: float) -> float:
        """
        Volume-derivative of the enthalpy of formation of vacancies.

        :param float V: Volume.
        :return: Volume-derivative of the enthalpy of formation of vacancies.
        :rtype: float
        """
        return 24*self.V0*self.a*self.P2/(NAv*V**4)-24*self.V0*self.a*(V-self.V0)*self.P2/(NAv*V**5)

    def E(self, T: float, V: float) -> float:
        """
        Defects energy.

        :param float T: Temperature.
        :param float V: Volume
        :return: E_def
        :rtype: float
        """
        return self.Evac(V)*NAv*np.exp(self.Svac(V)/kB - self.Evac(V)/(kB*T))
    def S(self, T: float, V: float) -> float:
        """
        Defects entropy.

        :param float T: Temperature.
        :param float V: Volume
        :return: S_def
        :rtype: float
        """
        return (T*kB+self.Evac(V))*NAv*np.exp(self.Svac(V)/kB - self.Evac(V)/(kB*T))/T
    def F(self, T: float, V: float) -> float:
        """
        Implementation of the defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: energy
        :rtype: float
        """
        return -NAv*T*kB*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))
    def dFdV_T(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))

    def dFdT_V(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*kB*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*T*kB*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))
    def d2FdT2_V(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*self.Evac(V)**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T**3*kB)
    def d2FdV2_T(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -(-(self.d2EvacdV2_T(V))*T*kB+(self.d2SvacdV2_T(V))*T**2*kB+((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))**2)*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))*NAv/(T*kB)
    def d3FdV3_T(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*(self.d3SvacdV3_T(V)*T-self.d3EvacdV3_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-3*NAv*(self.d2SvacdV2_T(V)*T-self.d2EvacdV2_T(V))*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)-NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))**3*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T**2*kB**2)
    def d4FdV4_T(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*(self.d4SvacdV4_T(V)*T-self.d4EvacdV4_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-4*NAv*(self.d3SvacdV3_T(V)*T-self.d3EvacdV3_T(V))*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)-3*NAv*(self.d2SvacdV2_T(V)*T-self.d2EvacdV2_T(V))**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)

    def d2FdVdT(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))*(T*(T*kB+self.Evac(V))*(self.dSvacdV_T(V))-(self.dEvacdV_T(V))*self.Evac(V))*NAv/(T**2*kB)
    def d3FdV2dT(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -NAv*(self.d2SvacdV2_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*((self.d2SvacdV2_T(V))*T-(self.d2EvacdV2_T(V)))*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-2*NAv*((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))*(self.dSvacdV_T(V))/(T*kB)+NAv*((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T**2*kB)-NAv*((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))**2*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)
    def d3FdVdT2(self, T: float, V: float) -> float:
        """
        Derivative of defects contribution to the free energy.

        :param float T: Temperature.
        :param float V:  Volume.
        :return: Derivative of F_def
        :rtype: float
        """
        return -2*NAv*self.dSvacdV_T(V)*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*(-2*self.Svac(V)/(T**2*kB)+(2*(self.Svac(V)*T-self.Evac(V)))/(T**3*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))
