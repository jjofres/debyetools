import numpy as np
from numpy.polynomial import Polynomial


class Xs:
    """
    Excess contribution to the free energy (J/mol-at), a FactSage-like polynomial in T
    whose coefficients may depend on volume ([DT] eq. (5)):

        F_xs(T, V) = A0(V) + A1(V) T + A2(V) T^2 + A3(V) T^3 + A4(V) T ln T + A5(V) T^-2

    Each coefficient is given either as a number (V-independent, the usual case) or as
    a sequence of polynomial coefficients in V, lowest order first:
    A_i(V) = c_i0 + c_i1 V + c_i2 V^2 + ... with V in m^3/mol-at. With V-independent
    coefficients all volume derivatives are zero and F_xs does not contribute to the
    pressure, bulk modulus or thermal expansion.

    :param params: xs0..xs5 (A0..A5). Units: A0 J/mol-at, A1 J/mol-at/K, A2 J/mol-at/K^2,
        A3 J/mol-at/K^3, A4 J/mol-at/K, A5 J K^2/mol-at (per (m^3/mol)^k for the order-k
        coefficient of a V polynomial).
    """
    def __init__(self, *params):
        if len(params) != 6:
            raise ValueError("Xs needs 6 coefficients (xs0 ... xs5); got %d." % len(params))
        self.xs0, self.xs1, self.xs2, self.xs3, self.xs4, self.xs5 = params
        self._A = []
        for p in params:
            c = np.atleast_1d(np.asarray(p, dtype=float))
            if c.ndim != 1 or len(c) == 0:
                raise ValueError("Each Xs coefficient must be a number or a 1-d sequence of "
                                 "polynomial coefficients in V.")
            if len(c) == 1:
                self._A.append(float(c[0]))                 # V-independent
            else:
                P = Polynomial(c)
                self._A.append([P.deriv(k) for k in range(5)])
        self.V_dependent = any(not isinstance(a, float) for a in self._A)

    def _Ai(self, i, k, V):
        """k-th volume derivative of coefficient A_i at V."""
        a = self._A[i]
        if isinstance(a, float):
            return a if k == 0 else 0.0
        return a[k](V)

    @staticmethod
    def _g(T, n):
        """n-th temperature derivative (n = 0, 1, 2) of the six T functions."""
        if n == 0:
            return (1.0, T, T**2, T**3, T * np.log(T), T**(-2))
        if n == 1:
            return (0.0, 1.0, 2 * T, 3 * T**2, np.log(T) + 1, -2 * T**(-3))
        return (0.0, 0.0, 2.0, 6 * T, 1 / T, 6 * T**(-4))

    def _sum(self, T, V, nT, kV):
        g = self._g(T, nT)
        out = 0.0 * T * V          # zero with the broadcast shape of T and V
        for i in range(6):
            a = self._Ai(i, kV, V)
            if isinstance(a, float) and a == 0.0:
                continue
            out = out + a * g[i]
        return out

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
        return -self.dFdT_V(T, V)

    def F(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Excess contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_xs
        :rtype: float|np.ndarray
        """
        return self._sum(T, V, 0, 0)

    def dFdV_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """(dF_xs/dV)_T"""
        return self._sum(T, V, 0, 1)

    def dFdT_V(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """(dF_xs/dT)_V"""
        return self._sum(T, V, 1, 0)

    def d2FdT2_V(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """(d2F_xs/dT2)_V"""
        return self._sum(T, V, 2, 0)

    def d2FdV2_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """(d2F_xs/dV2)_T"""
        return self._sum(T, V, 0, 2)

    def d3FdV3_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """(d3F_xs/dV3)_T"""
        return self._sum(T, V, 0, 3)

    def d4FdV4_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """(d4F_xs/dV4)_T"""
        return self._sum(T, V, 0, 4)

    def d2FdVdT(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """d2F_xs/dVdT"""
        return self._sum(T, V, 1, 1)

    def d3FdV2dT(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """d3F_xs/dV2dT"""
        return self._sum(T, V, 1, 2)

    def d3FdVdT2(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """d3F_xs/dVdT2"""
        return self._sum(T, V, 2, 1)
