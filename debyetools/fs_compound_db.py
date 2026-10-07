
import numpy as np

Cp2fit = lambda T, P0, P1, P2, P3, P4, P5: P0*T**0 + P1*T**1 + P2*T**(-2) + P3*T**2 + P4*T**(-.5) + P5*T**(-3)
alpha2fit = lambda T, Q0, Q1, Q2, Q3: Q0*T**0 + Q1*T**1 + Q2*T**(-1) + Q3*T**(-2)
Ksinv2fit = lambda T, R0, R1, R2, R3: R0*T**0 + R1*T**1 + R2*T**2 + R3*T**3
Ksp2fit = lambda T, S0, S1: S0 + S1*(T-298.15)*np.log(T/298.15)

# basis functions of the four models (all are linear in their coefficients)
_BASIS = {'Cp': lambda T: [T**0, T, T**(-2), T**2, T**(-.5), T**(-3)],
          'a': lambda T: [T**0, T, T**(-1), T**(-2)],
          '1/Ks': lambda T: [T**0, T, T**2, T**3],
          'Ksp': lambda T: [T**0, (T-298.15)*np.log(T/298.15)]}


def _linear_fit(T: np.ndarray, y: np.ndarray, basis) -> np.ndarray:
    """
    Least-squares coefficients of y = sum_j c_j f_j(T). The columns are scaled to unit norm before the
    solve (the unscaled design matrix has a condition number up to ~1e16), so the result is the exact
    least-squares minimum, independent of any starting values.
    """
    A = np.vstack(basis(T)).T
    scale = np.linalg.norm(A, axis=0)
    coef, *_ = np.linalg.lstsq(A / scale, y, rcond=None)
    return coef / scale


def fit_FS(tprops: dict, T_from: float, T_to: float, cp_T3: bool = False) -> dict:
    """
    Procedure for the fitting of FS compound database parametes to thermodynamic properties.

    Fits, on the temperatures T_from <= T <= T_to (0.005 K tolerance, so T_from/T_to need not be grid points):
    Cp = P0 + P1 T + P2 T^-2 + P3 T^2 + P4 T^-0.5 + P5 T^-3, alpha = Q0 + Q1 T + Q2 T^-1 + Q3 T^-2,
    1/Ks = R0 + R1 T + R2 T^2 + R3 T^3, Ks' = S0 + S1 (T - 298.15) ln(T/298.15).
    All four models are linear in their coefficients and are solved by linear least squares on
    column-scaled design matrices (exact minimum).

    The T^-3 coefficient P5 is poorly determined on typical windows (e.g. 298-1000 K): fitting it gives
    large, mutually cancelling coefficients. By default (cp_T3=False) P5 is fixed at 0 and the other five
    are fitted; with cp_T3=True all six are fitted. (The former curve_fit version left P5 at its initial
    value 1.0, i.e. effectively the 5-term fit.)

    :param tprops: Dictionary with the thermodynamic properties ('T', 'Cp', 'a', 'Ks', 'Ksp').
    :type tprops: dict
    :param T_from: Initial temperature.
    :type T_from: float
    :param T_to: Final temperature.
    :type T_to: float
    :param cp_T3: fit the T^-3 term of Cp (default False: P5 = 0).
    :type cp_T3: bool
    :return: Dictionary with the optimal parameters ('Cp' (6 values), 'a', '1/Ks', 'Ksp').
    :rtype: dict
    """
    T = np.asarray(tprops['T'], dtype=float)
    m = (T >= T_from - 5e-3) & (T <= T_to + 5e-3)
    n = int(m.sum())
    n_cp = 6 if cp_T3 else 5
    if n < n_cp:
        raise ValueError('fit_FS: %d temperatures in [%g, %g] K; at least %d are needed for the Cp fit.' % (n, T_from, T_to, n_cp))
    Tw = T[m]
    data = {'Cp': np.asarray(tprops['Cp'], dtype=float)[m],
            'a': np.asarray(tprops['a'], dtype=float)[m],
            '1/Ks': 1 / np.asarray(tprops['Ks'], dtype=float)[m],
            'Ksp': np.asarray(tprops['Ksp'], dtype=float)[m]}
    out = {k: _linear_fit(Tw, data[k], _BASIS[k]) for k in ('a', '1/Ks', 'Ksp')}
    if cp_T3:
        out['Cp'] = _linear_fit(Tw, data['Cp'], _BASIS['Cp'])
    else:
        out['Cp'] = np.append(_linear_fit(Tw, data['Cp'], lambda T: _BASIS['Cp'](T)[:5]), 0.)
    return {k: out[k] for k in ('Cp', 'a', '1/Ks', 'Ksp')}
