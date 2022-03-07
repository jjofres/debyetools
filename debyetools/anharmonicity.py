import numpy as np
np.seterr(divide='ignore')

class Anharmonicity:
    """
    Instance for the excess contribution to the free energy.

    :param float s0,s1,s2: Parameters of the A(V) term.
    """

    def __init__(self, s0, s1, s2):
        self.s0 = s0
        self.s1 = s1
        self.s2 = s2

    def A(self, V):
        """
        A(V) = s0+s0*V+s1*V**2, where A is the polynomial model for the excess contribution to the free energy, A(V)*T.

        :param float V: Volume
        :return: s0+s0*V+s1*V**2
        :rtype: float
        """
        return self.s0 + self.s1 * V + self.s2 * V ** 2

    def dAdV_T(self, V):
        """
        Volume derivative of A at fixed T.

        :param float V: Volume
        :return: s1+2*V*s2
        :rtype: float
        """
        return 2 * V * self.s2 + self.s1

    def d2AdV2_T(self, V):
        """
        Second order volume derivative of A at fixed T.

        :param float V: Volume
        :return: 2*s2
        :rtype: float
        """
        return 2 * self.s2

    def d3AdV3_T(self, V):
        """
        Third order volume derivative of A at fixed T.

        :param float V: Volume
        :return: 0
        :rtype: float
        """
        return 0

    def d4AdV4_T(self, V):
        """
        Fourth order volume derivative of A at fixed T.

        :param float V: Volume.
        :return: 0
        :rtype: float.
        """
        return 0

    def E(self, T, V):
        """
        Internal energy due the excess term.

        :param float T: Temperature.
        :param float V: Volume.
        :return: A(V)*T**2/2
        :rtype: float
        """
        return 1 / 2 * self.A(V) * T ** 2

    def S(self, T, V):
        """
        Entropy due the excess term.

        :param float T: Temperature.
        :param float V: Volume.
        :return: A(V)*T
        :rtype: float
        """
        return self.A(V) * T

    def F(self, T, V):
        """
        Free energy due the excess term.

        :param float T: Temperature.
        :param float V: Volume.
        :return: -A(V)*T**2/2
        :rtype: float
        """
        return -1 / 2 * self.A(V) * T ** 2

    def dFdV_T(self, T, V):
        """
        Volume derivative of the free energy due the excess term, at fixed T.

        :param float T: Temperature.
        :param float V: Volume.
        :return: -(dA(V)/dV)_T*T**2/2
        :rtype: float
        """
        return -1 / 2 * self.dAdV_T(V) * T ** 2

    def d2FdT2_V(self, T, V):
        """
        Second order Temperature derivative of the free energy due the excess term, at fixed V.

        :param float T: Temperature.
        :param float V: Volume.
        :return: -A(V)
        :rtype: float
        """
        return -self.A(V)

    def d2FdV2_T(self, T, V):
        """
        Second order volume derivative of the free energy due the excess term, at fixed T.

        :param float T: Temperature.
        :param float V: Volume.
        :return: -(d2A(V)/dV2)_T*T**2/2
        :rtype: float
        """
        return -self.d2AdV2_T(V) * T ** 2 / 2

    def d3FdV3_T(self, T, V):
        """
        Third order volume derivative of the free energy due the excess term, at fixed T.

        :param float T: Temperature.
        :param float V: Volume.
        :return: -(d3A(V)/dV3)_T*T**2/2
        :rtype: float
        """
        return -self.d3AdV3_T(V) * T ** 2 / 2

    def d4FdV4_T(self, T, V):
        """
        Fourth order volume derivative of the free energy due the excess term, at fixed T.

        :param float T: Temperature.
        :param float V: Volume.
        :return: -(d4A(V)/dV4)_T*T**2/2
        :rtype: float
        """
        return -self.d4AdV4_T(V) * T ** 2 / 2

    def d2FdVdT(self, T, V):
        """
        Second order derivative of the free energy due the excess term, with respect to T and V.

        :param float T: Temperature.
        :param float V: Volume.
        :return: -(dA(V)/dV)_T*T
        :rtype: float
        """
        return -self.dAdV_T(V) * T

    def d3FdV2dT(self, T, V):
        """
        Third order derivative of the free energy due the excess term, with respect to T, V, and V.

        :param float T: Temperature.
        :param float V: Volume.
        :return: -(d2A(V)/dV2)_T*T
        :rtype: float
        """
        return -self.d2AdV2_T(V) * T

    def d3FdVdT2(self, T, V):
        """
        Third order derivative of the free energy due the excess term, with respect to T, T, and V.

        :param float T: Temperature.
        :param float V: Volume.
        :return: -(dA(V)/dV)_T
        :rtype: float
        """
        return -self.dAdV_T(V)


class intAnharmonicity:
    def __init__(self, a0=0, m0=1, V0=1):
        """
        Instantiate the corrections required to consider temperature dependence on the Debye temperature.

        :param float a0: Parameter of the intrinsic anharmonicity correction function.
        :param float m0: Pseudo-Gruneisen parameter of the intrinsic anharmonicity correction function.
        :param float V0: Equilibrium volume.
        """
        self.d3AnhdV2dT_val = None
        self.d3AnhdVdT2_val = None
        self.d2AnhdVdT_val = None
        self.d3AnhdV3_T_val = None
        self.d2AnhdV2_T_val = None
        self.dAnhdV_T_val = None
        self.d4AnhdT4_V_val = None
        self.d3AnhdT3_V_val = None
        self.d2AnhdT2_V_val = None
        self.Anh_val = None
        self.an_val = None
        self.dAnhdT_V_val = None
        self.a0 = a0
        self.m0 = m0
        self.V0 = V0

    def an(self, V):
        """
        Intrinsic anharmonicity parameter.

        :param float V: Volume
        :return: a0*(V/V0)^m0
        :rtype: float
        """
        return self.a0 * (V / self.V0) ** self.m0

    def Anh(self, T, V):
        """
        Intrinsic anharmonicity correction to the Debye temperature.

        :param float T: Temperature.
        :param float V: Volume.
        :returns: Intrinsic anharmonicity correction
        :rtype: float
        """
        self.an_val = self.an(V)
        self.Anh_val = np.exp(1 / 2 * self.an_val * T)
        return self.Anh_val

    def dAnhdT_V(self):
        """
        Temperature derivative of the intrinsic anharmonicity correction of the Debye temperature, at fixed V.

        :param float V: Volume
        :return: an_val*Anh_val/2
        :rtype: float
        """
        self.dAnhdT_V_val = (1 / 2) * self.an_val * self.Anh_val
        return self.dAnhdT_V_val

    def d2AnhdT2_V(self):
        """
        Second order temperature derivative of the intrinsic anharmonicity correction of the Debye temperature,
        at fixed V.

        :param float V: Volume
        :return: an_val*(d2Anh_val/dT2)_V/2
        :rtype: float
        """
        self.d2AnhdT2_V_val = (1 / 2) * self.an_val * self.dAnhdT_V_val
        return self.d2AnhdT2_V_val

    def d3AnhdT3_V(self):
        """
        Third order temperature derivative of the intrinsic anharmonicity correction of the Debye temperature,
        at fixed V.

        :param float V: Volume
        :return: an_val*(d2Anh_val/dT2)_V/2
        :rtype: float
        """
        self.d3AnhdT3_V_val = (1 / 2) * self.an_val * self.d2AnhdT2_V_val
        return self.d3AnhdT3_V_val

    def d4AnhdT4_V(self):
        """
        Fourth order temperature derivative of the intrinsic anharmonicity correction of the Debye temperature,
        at fixed V.

        :param float V: Volume.
        :return: an_val*(d3Anh_val/dT3)_V/2
        :rtype: float
        """
        self.d4AnhdT4_V_val = (1 / 2) * self.an_val * self.d3AnhdT3_V_val
        return self.d4AnhdT4_V_val

    def dAnhdV_T(self, T, V):
        """
        Volume derivative of the intrinsic anharmonicity correction of the Debye temperature, at fixed T.

        :param float V: Volume
        :return: m0*T*an_val*Anh_val/(2*V)
        :rtype: float
        """
        self.dAnhdV_T_val = self.m0 * T * self.an_val * self.Anh_val / (2 * V)
        return self.dAnhdV_T_val

    def d2AnhdV2_T(self, T, V):
        """
        Second order Volume derivative of the intrinsic anharmonicity correction of the Debye temperature, at fixed T.

        :param float V: Volume
        :return: dAnhdV_T_val*(T*an_val*m0+2*m0-2)/(2*V)
        :rtype: float
        """

        self.d2AnhdV2_T_val = self.dAnhdV_T_val * (T * self.an_val * self.m0 + 2 * self.m0 - 2) / (2 * V)
        return self.d2AnhdV2_T_val

    def d3AnhdV3_T(self, T, V):
        """
        Third order Volume derivative of the intrinsic anharmonicity correction of the Debye temperature, at fixed T.

        :param float V: Volume
        :return: dAnhdV_T_val*(T^2*an_val^2*m0^2+6*T*an_val*m0^2-6*T*an_val*m0+4*m0^2-12*m0+8)/(4*V^2)
        :rtype: float
        """
        self.d3AnhdV3_T_val = self.dAnhdV_T_val * (
                    T ** 2 * self.an_val ** 2 * self.m0 ** 2 + 6 * T * self.an_val * self.m0 ** 2 - 6 * T * self.an_val * self.m0 + 4 * self.m0 ** 2 - 12 * self.m0 + 8) / (
                                          4 * V ** 2)
        return self.d3AnhdV3_T_val

    def d4AnhdV4_T(self, T, V):
        """
        Fourth order Volume derivative of the intrinsic anharmonicity correction of the Debye temperature, at fixed T.

        :param float V: Volume
        :return: dAnhdV_T_val*(T^3*an_val^3*m0^3+12*T^2*an_val^2*m0^3 - 12*T^2*an_val^2*m0^2+28*T*an_val*m0^3-72*T*an_val*m0^2+44T*an_val*m0+8+m0^3-48*m0^2+88*m0-48)/(8*V^3)
        :rtype: float
        """
        self.d4AnhdT4_V_val = self.dAnhdV_T_val * (
                    T ** 3 * self.an_val ** 3 * self.m0 ** 3 + 12 * T ** 2 * self.an_val ** 2 * self.m0 ** 3 - 12 * T ** 2 * self.an_val ** 2 * self.m0 ** 2 + 28 * T * self.an_val * self.m0 ** 3 - 72 * T * self.an_val * self.m0 ** 2 + 44 * T * self.an_val * self.m0 + 8 * self.m0 ** 3 - 48 * self.m0 ** 2 + 88 * self.m0 - 48) / (
                                          8 * V ** 3)
        return self.d4AnhdT4_V_val

    def d2AnhdVdT(self, T):
        """
        Second order derivative of the intrinsic anharmonicity correction of the Debye temperature,
        with respect to T and V.

        :param float V: Volume
        :return: dAnhdV_T_val * (1 / T + an_val / 2)
        :rtype: float
        """
        self.d2AnhdVdT_val = self.dAnhdV_T_val * (1 / T + self.an_val / 2)
        return self.d2AnhdVdT_val

    def d3AnhdVdT2(self, T):
        """
        Third order derivative of the intrinsic anharmonicity correction of the Debye temperature,
        with respect to T, T, and V.

        :param float V: Volume
        :return: dAnhdV_T_val * an_val * (1 / T + an_val / 4)
        :rtype: float
        """

        self.d3AnhdVdT2_val = self.dAnhdV_T_val * self.an_val * (1 / T + self.an_val / 4)
        return self.d3AnhdVdT2_val

    def d3AnhdV2dT(self, T, V):
        """
        Third order derivative of the intrinsic anharmonicity correction of the Debye temperature,
        with respect to T, V, and V.

        :param float V: Volume
        :return: dAnhdV_T_val/V*(m0/T-1/T+3/2*an_val*m0-an_val/2+an_val^2*m0*T/4)
        :rtype: float
        """
        self.d3AnhdV2dT_val = self.dAnhdV_T_val / V * (
                    self.m0 / T - 1 / T + 3 / 2 * self.an_val * self.m0 - self.an_val / 2 + self.an_val ** 2 * self.m0 * T / 4)
        return self.d3AnhdV2dT_val
