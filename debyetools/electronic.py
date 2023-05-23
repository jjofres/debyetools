import numpy as np
from scipy.optimize import leastsq

NAv  = 0.6022140857e24
kB   = 0.138064852e-22

class Electronic:
    """
    Implementation of the electronic contribution to the free energy.

    :param float params: N(Ef)(V) function parameters.
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
        return (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.NfV(V)/(0.160218e-18)

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
        return (2/6)*np.pi**2*NAv*self.r*kB**2*T*self.NfV(V)/(0.160218e-18)
    def F(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.NfV(V)/(0.160218e-18)

    def dFdV_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.dNfVdV_T(V)/(0.160218e-18)
    def dFdT_V(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - 2*T*np.pi**2*NAv*self.r*kB**2*self.NfV(V)*(1/6)/(0.160218e-18)
    def d2FdT2_V(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - 2*np.pi**2*NAv*self.r*kB**2*self.NfV(V)*(1/6)/(0.160218e-18)
    def d2FdV2_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.d2NfVdV2_T(V)/(0.160218e-18)
    def d3FdV3_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.d3NfVdV3_T(V)/(0.160218e-18)
    def d4FdV4_T(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.d4NfVdV4_T(V)/(0.160218e-18)

    def d2FdVdT(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return -2*np.pi**2*NAv*self.r*kB**2*T*self.dNfVdV_T(V)*(1/6)/(0.160218e-18)
    def d3FdV2dT(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return -2*np.pi**2*NAv*self.r*kB**2*T*self.d2NfVdV2_T(V)*(1/6)/(0.160218e-18)
    def d3FdVdT2(self, T: float|np.ndarray, V: float|np.ndarray) -> float|np.ndarray:
        """
        Derivative of the electronic contribution to the free energy.

        :param float|np.ndarray T: Temperature.
        :param float|np.ndarray V: Volume.
        :return: F_el
        :rtype: float|np.ndarray
        """
        return -2*np.pi**2*NAv*self.r*kB**2*self.dNfVdV_T(V)*(1/6)/(0.160218e-18)

def fit_electronic(Vs: np.ndarray, p_el: np.ndarray, E: np.ndarray, N: np.ndarray, Ef: np.ndarray, ixss: int = 8, ixse: int = -1) -> np.ndarray:
    """
    Fitting procedure for the N(Ef)(V) function.

    :param np.ndarray Vs: Volumes.
    :param np.ndarray p_el: Initial parameters.
    :param np.ndarray E: Matrix with energies at each level for each volume.
    :param np.ndarray N: Matrix with densities of state at each level for each volume.
    :param np.ndarray Ef: Fermi levels as function of temperature.
    :param int ixse: (optional) eDOS subset index.
    :param intixss: (optional) eDOS subset index.

    :retun np.ndarray: optimized parameters.
    """

    V = np.array(Vs)
    ix_V0=4
    EfV0 = float(Ef[ix_V0])
    ixs=[i for i,x in enumerate(E[ix_V0]) if x>=Ef[ix_V0]]
    E1 = float(E[ix_V0][ixs[0]-1])
    E2 = float(E[ix_V0][ixs[0]])
    N1 = float(N[ix_V0][ixs[0]-1])
    N2 = float(N[ix_V0][ixs[0]])
    NfV0 = (EfV0 - E1)*(N2 - N1)/(E2 - E1) + N1
    NfV = np.array([NfV0*np.sqrt(ef/EfV0) for ef in Ef][ixss:ixse])
    P2 = leastsq(NfV2m, p_el, args=(V[ixss:ixse], NfV),maxfev=1000)

    P2 = P2[0]

    return P2

def NfV_poly_fun(V: float, _A: float, _B: float, _C: float, _D: float) -> float:
    """
    Polynomial model for N(Ef)(V) for min.

    :param V: Volume/
    :type V: float
    :param _A: param.
    :type _A: float
    :param _B: param.
    :type _B: float
    :param _C: param.
    :type _C: float
    :param _D: param.
    :type _D: float
    :return: polynimial for minimization.
    :rtype: float
    """
    return _A + _B*V + _C*V**2 + _D*V**3

def NfV2m(P: np.ndarray, Vdata: np.ndarray, NfVdata: np.ndarray) -> np.ndarray:
    """
    Error function for minimizaiton.

    :param P: Parameters.
    :type P: np.ndarray
    :param Vdata: Volume data.
    :type Vdata: np.ndarray
    :param NfVdata: N(Ef)(V) data.
    :type NfVdata: np.ndarray
    :return: err.
    :rtype: np.ndarray
    """
    NfVcalc = [NfV_poly_fun(Vi, P[0], P[1], P[2], P[3]) for Vi in Vdata]
    return (NfVcalc-NfVdata)**2
