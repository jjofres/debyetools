import numpy as np
from numpy.polynomial import Polynomial
from debyetools.constants import NAv, kB, eV

class Electronic:
    """
    Electronic contribution to the free energy (Sommerfeld, low-T expansion):

        F_el(T, V) = -(pi^2/6) * N_A * k_B^2 * T^2 * N(E_F)(V) / eV          [J/mol-atom]

    with N(E_F)(V) = q0 + q1*V + q2*V^2 + q3*V^3 the total electronic density of
    states at the Fermi level (both spins summed) in states/eV/atom, and V in
    m^3/mol-atom (so q1, q2, q3 are in states/eV/atom per (m^3/mol)^k). The
    parameters are obtained with :func:`fit_electronic`. S_el = -dF_el/dT and
    E_el = F_el + T*S_el = +(pi^2/6)*N_A*k_B^2*T^2*N(E_F)/eV.

    Note: the supplementary material of the paper writes the derivatives with
    pi^2/3 (equivalent to using the DOS of one spin channel); here the total DOS
    and pi^2/6 are used (review decision D4).

    :param float params: q0, q1, q2, q3 of N(E_F)(V).
    """
    def __init__(self, *params: np.ndarray):
        self.pel = params
        self.r=1
        for n,q in enumerate(params):
            setattr(self,'q'+str(n),q)

    def NfV(self, V: float) -> float:
        """
        N(Ef)(V)

        :param float V: Volume.
        :return: N(Ef)(V)
        :rtype: float
        """
        return self.q0*V**0 + self.q1*V**1 + self.q2*V**2 + self.q3*V**3

    def dNfVdV_T(self, V: float) -> float:
        """
        derivative of N(Ef)(V)

        :param V: Volume.
        :type V: float
        :return: derivative of N(Ef)(V)
        :rtype: float
        """
        return 3*V**2*self.q3+2*V*self.q2+self.q1

    def d2NfVdV2_T(self, V: float) -> float:
        """
        derivative of N(Ef)(V)

        :param V: Volume.
        :type V: float
        :return: derivative of N(Ef)(V)
        :rtype: float
        """
        return 6*V*self.q3+2*self.q2

    def d3NfVdV3_T(self, V: float) -> float:
        """
        derivative of N(Ef)(V)

        :param V: Volume.
        :type V: float
        :return: derivative of N(Ef)(V)
        :rtype: float
        """
        return 6*self.q3
    def d4NfVdV4_T(self, V: float) -> float:
        """
        derivative of N(Ef)(V)

        :param V: Volume.
        :type V: float
        :return: derivative of N(Ef)(V)
        :rtype: float
        """
        return 0

    def E(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Electronic energy

        :param T: Temperature.
        :type T: float|np.ndarray
        :param V: Volume.
        :type V: float|np.ndarray
        :return: E_el
        :rtype: float|np.ndarray
        """
        return (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.NfV(V)/eV

    def S(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Electronic entropy.

        :param T: Temperature.
        :type T: float|np.ndarray
        :param V: Volume.
        :type V: float|np.ndarray
        :return: S_el
        :rtype: float|np.ndarray
        """
        return (2/6)*np.pi**2*NAv*self.r*kB**2*T*self.NfV(V)/eV
    def F(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.NfV(V)/eV

    def dFdV_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.dNfVdV_T(V)/eV
    def dFdT_V(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - 2*T*np.pi**2*NAv*self.r*kB**2*self.NfV(V)*(1/6)/eV
    def d2FdT2_V(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - 2*np.pi**2*NAv*self.r*kB**2*self.NfV(V)*(1/6)/eV
    def d2FdV2_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.d2NfVdV2_T(V)/eV
    def d3FdV3_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.d3NfVdV3_T(V)/eV
    def d4FdV4_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.d4NfVdV4_T(V)/eV

    def d2FdVdT(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return -2*np.pi**2*NAv*self.r*kB**2*T*self.dNfVdV_T(V)*(1/6)/eV
    def d3FdV2dT(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return -2*np.pi**2*NAv*self.r*kB**2*T*self.d2NfVdV2_T(V)*(1/6)/eV
    def d3FdVdT2(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return -2*np.pi**2*NAv*self.r*kB**2*self.dNfVdV_T(V)*(1/6)/eV

def N_at_Fermi(E: np.ndarray, N: np.ndarray, Ef: float, sigma: float = 0.0) -> float:
    """
    Density of states at the Fermi level from one total DOS.

    :param np.ndarray E: Energy grid (eV), increasing.
    :param np.ndarray N: Total DOS on that grid (states/eV/atom).
    :param float Ef: Fermi level (eV, same reference as E).
    :param float sigma: Gaussian broadening (eV). 0 (default): linear interpolation of
        N at Ef. sigma > 0: Gaussian-weighted average of N around Ef (reduces the noise
        of a coarse DOS grid; the result depends on sigma).
    :return: N(E_F) in states/eV/atom.
    :rtype: float
    """
    E = np.asarray(E, dtype=float)
    N = np.asarray(N, dtype=float)
    if E.ndim != 1 or E.shape != N.shape or len(E) < 2:
        raise ValueError("E and N must be 1-d arrays of the same length (one total DOS).")
    if np.any(np.diff(E) <= 0):
        raise ValueError("Energy grid is not increasing; pass the total-DOS block only "
                         "(debyetools.aux_functions.load_doscar).")
    if not E[0] <= Ef <= E[-1]:
        raise ValueError("Fermi level %g eV outside the DOS energy range [%g, %g]." % (Ef, E[0], E[-1]))
    if sigma is None or sigma == 0:
        return float(np.interp(Ef, E, N))
    if sigma < 0:
        raise ValueError("sigma must be >= 0.")
    w = np.exp(-0.5 * ((E - Ef) / sigma) ** 2)
    return float(np.sum(w * N) / np.sum(w))


def fit_electronic(Vs: np.ndarray, p_el: np.ndarray, E: list, N: list, Ef: list, ixss: int = 0,
                   ixse: int = None, mode: str = 'dos', V0: float = None, sigma: float = 0.0,
                   order: int = 3) -> np.ndarray:
    """
    Fit N(E_F)(V) = q0 + q1*V + q2*V^2 + q3*V^3 for :class:`Electronic`.

    mode='dos' (default): N(E_F) is read from the total DOS at every volume (each DOS
    at its own Fermi level, see :func:`N_at_Fermi`).

    mode='scaling': free-electron scaling from one reference DOS,
    N(E_F)(V) = N(E_F)(V_ref) * (V/V_ref)^(2/3). V0 is required: with a single DOS
    (len(E) == 1) V_ref = V0; with one DOS per volume, the DOS of the volume closest to
    V0 is used and V_ref is that volume. Only that DOS is read.

    The polynomial is obtained by linear least squares in the reduced volume
    x = V/V_m - 1 (V_m = mean of the fitted volumes) and converted to coefficients in V.

    :param np.ndarray Vs: Volumes (m^3/mol-atom), in the same order as E, N, Ef.
    :param np.ndarray p_el: Not used (kept for compatibility; the fit is linear and
        needs no initial guess).
    :param list E: Energy grid of each total DOS (eV), e.g. from load_doscar.
    :param list N: Total DOS of each volume (states/eV/atom), e.g. from load_doscar.
    :param list Ef: Fermi level of each volume (eV).
    :param int ixss: First volume index used in the fit (default 0).
    :param int ixse: End index (exclusive, python slice) of the volumes used (default None:
        up to the last volume).
    :param str mode: 'dos' or 'scaling'.
    :param float V0: Reference volume for mode='scaling' (m^3/mol-atom).
    :param float sigma: Gaussian broadening of the DOS at E_F in eV (default 0: linear
        interpolation).
    :param int order: Polynomial order, 1 to 3 (default 3).
    :return: [q0, q1, q2, q3].
    :rtype: np.ndarray
    """
    V = np.asarray(Vs, dtype=float).ravel()
    if order not in (1, 2, 3):
        raise ValueError("order must be 1, 2 or 3.")
    Vfit = V[ixss:ixse]
    if mode == 'dos':
        if not (len(E) == len(N) == len(Ef) == len(V)):
            raise ValueError("Vs, E, N and Ef must have the same length (one DOS per volume, "
                             "same order); got %d, %d, %d, %d." % (len(V), len(E), len(N), len(Ef)))
        NF = np.array([N_at_Fermi(E[i], N[i], Ef[i], sigma) for i in range(len(V))])[ixss:ixse]
    elif mode == 'scaling':
        if V0 is None:
            raise ValueError("mode='scaling' needs V0.")
        if len(E) == 1:
            i0, Vref = 0, float(V0)
        elif len(E) == len(N) == len(Ef) == len(V):
            i0 = int(np.argmin(np.abs(V - V0)))
            Vref = V[i0]
        else:
            raise ValueError("mode='scaling': pass one DOS (with V0 its volume) or one DOS per volume.")
        NF = N_at_Fermi(E[i0], N[i0], Ef[i0], sigma) * (Vfit / Vref) ** (2 / 3)
    else:
        raise ValueError("mode must be 'dos' or 'scaling'.")
    if len(Vfit) < order + 1:
        raise ValueError("Need at least %d volumes for order %d." % (order + 1, order))
    Vm = float(np.mean(Vfit))
    x = Vfit / Vm - 1
    c = np.linalg.lstsq(np.polynomial.polynomial.polyvander(x, order), NF, rcond=None)[0]
    q = Polynomial(c)(Polynomial([-1.0, 1.0 / Vm])).coef
    out = np.zeros(4)
    out[:len(q)] = q
    return out


def NfV_poly_fun(V: float, _A: float, _B: float, _C: float, _D: float) -> float:
    """
    Polynomial model for N(E_F)(V).

    :param V: Volume (m^3/mol-atom).
    :type V: float
    :param _A: q0.
    :type _A: float
    :param _B: q1.
    :type _B: float
    :param _C: q2.
    :type _C: float
    :param _D: q3.
    :type _D: float
    :return: N(E_F) (states/eV/atom).
    :rtype: float
    """
    return _A + _B*V + _C*V**2 + _D*V**3

def NfV2m(P: np.ndarray, Vdata: np.ndarray, NfVdata: np.ndarray) -> np.ndarray:
    """
    Residuals of the N(E_F)(V) polynomial (not used by fit_electronic any more).

    :param P: Parameters q0..q3.
    :type P: np.ndarray
    :param Vdata: Volume data.
    :type Vdata: np.ndarray
    :param NfVdata: N(Ef)(V) data.
    :type NfVdata: np.ndarray
    :return: residuals.
    :rtype: np.ndarray
    """
    return NfV_poly_fun(np.asarray(Vdata, dtype=float), P[0], P[1], P[2], P[3]) - np.asarray(NfVdata, dtype=float)
