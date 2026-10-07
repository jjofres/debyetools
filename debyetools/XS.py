import numpy as np
from scipy.optimize import leastsq

class Xs:
    """
    Excess contribution to the free energy (J/mol-at), a FactSage-like polynomial in T (no volume dependence):
    F_xs = xs0 + xs1 T + xs2 T^2 + xs3 T^3 + xs4 T ln T + xs5 T^-2.

    :param params: xs0 (J/mol-at), xs1 (J/mol-at/K), xs2 (J/mol-at/K^2), xs3 (J/mol-at/K^3),
        xs4 (J/mol-at/K), xs5 (J K^2/mol-at).
    """
    def __init__(self, *params: np.ndarray):
        self.xs0, self.xs1, self.xs2, self.xs3, self.xs4, self.xs5 = params

    def E(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Excess internal energy, E_xs = F_xs + T S_xs.

        :param T: Temperature.
        :type T: float|np.ndarray
        :param V: Volume.
        :type V: float|np.ndarray
        :return: E_xs
        :rtype: float|np.ndarray
        """
        return self.F(T, V) + T*self.S(T, V)

    def S(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Excess entropy, S_xs = -(dF_xs/dT)_V.

        :param T: Temperature.
        :type T: float|np.ndarray
        :param V: Volume.
        :type V: float|np.ndarray
        :return: S_xs
        :rtype: float|np.ndarray
        """
        return -(self.xs1 + 2 * self.xs2 * T + 3 * self.xs3 * T**2 + self.xs4 * (np.log(T) + 1) - 2 * self.xs5 * T**(-3))

    def F(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return self.xs0 + self.xs1 * T + self.xs2 * T**2 + self.xs3 * T**3 + self.xs4 * T * np.log(T) + self.xs5 * T**(-2)


    def dFdV_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return 0
    def dFdT_V(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return self.xs1 + 2 * self.xs2 * T + 3 * self.xs3 * T**2 + self.xs4 * (np.log(T) + 1) - 2 * self.xs5 * T**(-3)

    def d2FdT2_V(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return 2 * self.xs2 + 6 * self.xs3 * T + self.xs4 / T + 6 * self.xs5 * T**(-4)

    def d2FdV2_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return 0
    def d3FdV3_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return 0
    def d4FdV4_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return 0

    def d2FdVdT(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return 0
    def d3FdV2dT(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return 0
    def d3FdVdT2(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs (or the derivative named by the method)
        :rtype: float|np.ndarray
        """
        return 0


