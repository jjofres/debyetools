from __future__ import division
from scipy.optimize import least_squares, minimize

import numpy as np
import re
import warnings
from debyetools.constants import A3_ATOM_TO_M3_MOL, EV_ATOM_TO_J_MOL

# bounds for the 4-parameter analytic EOS fits (E0, V0, B0, B0'): V0 > 0 and B0 > 0 (review finding 3.8)
EOS4_BOUNDS = ([-np.inf, 0.0, 0.0, -np.inf], [np.inf, np.inf, np.inf, np.inf])
import itertools as it
import debyetools.pairanalysis as pairanalysis

def calculate_volume(aa, bb, cc):
    """
    Calculate the volume of a box defined by three 3D vectors.

    Parameters:
    a, b, c: 3D vectors (arrays or lists) representing three edges of the box.

    Returns:
    float: The volume of the box.
    """
    aa = np.array(aa)
    bb = np.array(bb)
    cc = np.array(cc)

    # Calculate the scalar triple product
    volume = np.abs(np.dot(aa, np.cross(bb, cc)))
    return volume


def _V0_from_dE0dV(eos, Vdata) -> float:
    """
    Equilibrium volume of an EOS without a V0 parameter (MP, EAM): root of dE0/dV = 0.

    The search starts at the data point with the lowest energy model value (mean of Vdata if only one
    point) and widens geometrically until dE0/dV changes sign from - to +; it is not limited to the data
    range. A UserWarning is issued if the minimum lies outside [min(Vdata), max(Vdata)] (more than one
    data volume), a ValueError if no minimum is found within a factor 3 of the start.
    """
    from scipy.optimize import brentq
    Vd = np.atleast_1d(np.asarray(Vdata, dtype=float))
    Vc = float(Vd[np.argmin([eos.E0(v) for v in Vd])]) if len(Vd) > 1 else float(Vd[0])
    lo = hi = Vc
    for _ in range(25):
        if eos.dE0dV_T(lo) < 0:
            break
        lo /= 1.05
    for _ in range(25):
        if eos.dE0dV_T(hi) > 0:
            break
        hi *= 1.05
    if not (eos.dE0dV_T(lo) < 0 < eos.dE0dV_T(hi)):
        raise ValueError('fitEOS: no minimum of E0(V) found between %.4g and %.4g.' % (lo, hi))
    V0 = brentq(eos.dE0dV_T, lo, hi, xtol=1e-15 * Vc, rtol=4 * np.finfo(float).eps)
    if len(Vd) > 1 and not (Vd.min() <= V0 <= Vd.max()):
        warnings.warn('fitEOS: the minimum of E0(V), V0 = %.6g, lies outside the data range [%.6g, %.6g].'
                      % (V0, Vd.min(), Vd.max()), UserWarning, stacklevel=3)
    return V0


class EOSFitError(RuntimeError):
    """Raised by fitEOS when no starting point gives an acceptable fit (see _fit_with_restarts)."""


def _analytic_start_from_data(Vdata, Edata):
    """
    Starting point (E0, V0, B0, B0') for the 4-parameter analytic EOS from the data alone: a cubic in
    x = V/V_m - 1 fitted to E(V), its minimum gives E0 and V0, V0 E2 gives B0 and -1 - V0 E3/E2 (E2, E3: 2nd and 3rd derivatives) gives
    B0' (clipped to [2, 8]). Falls back to the lowest data point, 100 GPa and 4.5 when the cubic has no
    minimum in the data range.
    """
    V = np.asarray(Vdata, dtype=float); E = np.asarray(Edata, dtype=float)
    i = int(np.argmin(E))
    fallback = np.array([E[i], V[i], 1e11, 4.5])
    if len(V) < 4:
        return fallback
    Vm = V.mean()
    P = np.polynomial.Polynomial.fit(V / Vm - 1, E, 3).convert()
    d1, d2, d3 = P.deriv(1), P.deriv(2), P.deriv(3)
    xs = [x.real for x in d1.roots() if abs(x.imag) < 1e-12 and d2(x.real) > 0]
    xs = [x for x in xs if V.min() <= Vm * (1 + x) <= V.max()]
    if not xs:
        return fallback
    x0 = min(xs, key=lambda x: P(x))
    V0 = Vm * (1 + x0)
    E2 = d2(x0) / Vm ** 2
    E3 = d3(x0) / Vm ** 3
    B0 = V0 * E2
    Bp = float(np.clip(-1 - V0 * E3 / E2, 2.0, 8.0))
    if not (np.isfinite(B0) and B0 > 0):
        return fallback
    return np.array([P(x0), V0, B0, Bp])


def _clip_into(p, bounds):
    """Starting point moved inside the bounds (a value on or below a finite lower bound is set just above it)."""
    lb, ub = (np.broadcast_to(np.asarray(b, dtype=float), np.shape(p)) for b in bounds)
    q = np.clip(np.array(p, dtype=float), lb, ub)
    eps_l = 1e-9 * np.where(np.isfinite(lb) & (lb != 0), np.abs(lb), 1.0)
    eps_u = 1e-9 * np.where(np.isfinite(ub) & (ub != 0), np.abs(ub), 1.0)
    q = np.where(np.isfinite(lb) & (q <= lb), lb + eps_l, q)
    q = np.where(np.isfinite(ub) & (q >= ub), ub - eps_u, q)
    return q


def _fit_check(eos, popt, Vdata, Edata, kind, rel_tol):
    """Set the parameters and judge the fit: finite, minimum found with B0 > 0, V0 within a factor 2 of the
    data range, rms of the residuals below rel_tol times the energy range of the data."""
    V = np.asarray(Vdata, dtype=float); E = np.asarray(Edata, dtype=float)
    info = {'params': np.array(popt, dtype=float)}
    if not np.all(np.isfinite(popt)):
        info['reason'] = 'non-finite parameters'; return False, info
    if hasattr(eos, '_set_fit_params'):
        eos._set_fit_params(popt)
    else:
        eos.pEOS = np.array(popt, dtype=float)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        try:
            res = np.asarray(eos.E0(V), dtype=float) - E
            V0 = float(popt[1]) if kind == 'analytic' else _V0_from_dE0dV(eos, V)
            B0 = V0 * float(eos.d2E0dV2_T(V0))
        except Exception as e:  # no minimum, overflow, ...
            info['reason'] = 'no minimum of E0(V) (%s)' % e; return False, info
    erange = max(float(E.max() - E.min()), 1e-300)
    info.update(rms=float(np.sqrt(np.mean(res ** 2))), V0=V0, B0=B0)
    info['rel_rms'] = info['rms'] / erange if len(E) > 1 else 0.0
    if not (np.isfinite(info['rms']) and np.isfinite(B0)):
        info['reason'] = 'non-finite energies'; return False, info
    if B0 <= 0:
        info['reason'] = 'B0 = V0 E0\'\'(V0) <= 0 (unstable)'; return False, info
    if len(V) > 1 and not (0.5 * V.min() <= V0 <= 2 * V.max()):
        info['reason'] = 'V0 = %.4g far outside the data range' % V0; return False, info
    if info['rel_rms'] > rel_tol:
        info['reason'] = 'rms %.3g J/mol = %.3g of the energy range > rel_tol %.3g' % (info['rms'], info['rel_rms'], rel_tol)
        return False, info
    info['reason'] = 'ok'
    return True, info


def _fit_with_restarts(eos, Vdata, Edata, p0, bounds, kind, rel_tol=0.02, max_starts=12, on_failure='raise',
                       x_scale='jac'):
    """
    Least-squares fit of an EOS with a check of the result and automatic restarts.

    The fit is started from p0 (the user's initial parameters). If the result fails the check (no minimum,
    B0 <= 0, V0 far from the data, or rms above rel_tol times the energy range of the data) other starting
    points are tried, one at a time, until one passes: for the analytic EOS (kind='analytic', parameters
    E0, V0, B0, B0') a start from a cubic fitted to the data and variations of B0 and B0'; for the pair
    potentials (kind='pair') deterministic random rescalings of p0 by factors 1/3 to 3. Every attempt is
    recorded in eos.fit_info. If none passes: on_failure='raise' raises EOSFitError (give better initial
    parameters), on_failure='warn' keeps the best attempt with a UserWarning.

    :return: fitted parameters.
    """
    V = np.asarray(Vdata, dtype=float); E = np.asarray(Edata, dtype=float)
    starts = []
    if p0 is not None and not (isinstance(p0, str) and p0 == ''):
        starts.append(('initial_parameters', np.array(p0, dtype=float)))
    if kind == 'analytic':
        d = _analytic_start_from_data(V, E)
        starts.append(('from data', d))
        for fB, Bp in [(1, 3.0), (1, 6.0), (0.5, 4.5), (2, 4.5), (0.5, 3.0), (2, 6.0), (1, 8.0), (0.25, 4.5), (4, 4.5)]:
            starts.append(('from data, B0 x %g, B0\' = %g' % (fB, Bp), np.array([d[0], d[1], d[2] * fB, Bp])))
    else:
        if not starts:
            raise ValueError('fitEOS: initial_parameters are required for this potential.')
        rng = np.random.default_rng(20261007)
        for k in range(max_starts):
            f = np.exp(rng.uniform(np.log(1 / 3), np.log(3), size=len(starts[0][1])))
            starts.append(('initial_parameters x random factors (%d)' % (k + 1), starts[0][1] * f))
    starts = starts[:max_starts]
    attempts = []
    best = None
    for label, x0 in starts:
        x0 = _clip_into(x0, bounds)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                sol = least_squares(eos.error2min, x0, args=(V, E), bounds=bounds, x_scale=x_scale)
            ok, info = _fit_check(eos, sol.x, V, E, kind, rel_tol)
        except Exception as e:
            ok, info = False, {'params': None, 'reason': 'fit failed (%s)' % e}
            sol = None
        info.update(start=label, x0=x0)
        attempts.append(info)
        if sol is not None and np.isfinite(info.get('rms', np.inf)) and (best is None or info['rms'] < best[1]['rms']):
            best = (sol, info)
        if ok:
            eos.fit_info = {'accepted': label, 'attempts': attempts}
            if len(attempts) > 1:
                warnings.warn('fitEOS (%s): the fit from %s was rejected (%s); accepted the fit from %s.'
                              % (type(eos).__name__, attempts[0]['start'], attempts[0]['reason'], label),
                              UserWarning, stacklevel=3)
            eos.eos_residuals = sol.fun
            return sol.x
    eos.fit_info = {'accepted': None, 'attempts': attempts}
    lines = '; '.join('%s: %s' % (a['start'], a['reason']) for a in attempts)
    if on_failure == 'warn' and best is not None:
        warnings.warn('fitEOS (%s): no starting point gave an acceptable fit; keeping the best one (%s, %s). '
                      'Tried: %s' % (type(eos).__name__, best[1]['start'], best[1]['reason'], lines),
                      UserWarning, stacklevel=3)
        if hasattr(eos, '_set_fit_params'):
            eos._set_fit_params(best[0].x)
        eos.eos_residuals = best[0].fun
        return best[0].x
    raise EOSFitError('fitEOS (%s): no starting point gave an acceptable fit. Please provide initial_parameters '
                      'closer to the solution (or use on_failure="warn" to keep the best attempt). Tried: %s'
                      % (type(eos).__name__, lines))


class BM:
    """
    Third order Birch-Murnaghan EOS and derivatives.

    """

    def __init__(self, *args, units='J/mol', parameters=''):
        self.V0 = None
        if list(parameters):
            self.pEOS = parameters[:4]
            self.V0 = float(self.pEOS[1])

    def fitEOS(self, Vdata: np.ndarray, Edata: np.ndarray, initial_parameters: np.ndarray = None, fit: bool = True, rel_tol: float = 0.02, max_starts: int = 12, on_failure: str = 'raise') -> None:
        """
        Parameters fitting.

        :param Vdata: Input volume data.
        :type Vdata: np.ndarray
        :param Edata: Target energy data.
        :type Edata: np.ndarray
        :param initial_parameters: Initial guess.
        :type initial_parameters: np.ndarray
        :param fit: True to run the fitting. False to just use the input parameters.
        :type fit: bool.
        :param rel_tol: A fit is accepted when its rms is below rel_tol times the energy range of the data (and it has
            a minimum with B0 > 0 within a factor 2 of the data volumes); otherwise other starting points are tried.
        :param max_starts: Maximum number of starting points.
        :param on_failure: 'raise' (EOSFitError, default) or 'warn' (keep the best attempt) when no start passes.

        :return: Optimal parameters.
        :rtype: np.ndarray
        """
        if fit:
            p0 = None if initial_parameters is None or (isinstance(initial_parameters, str) and initial_parameters == '') \
                else np.asarray(initial_parameters, dtype=float)[:4]
            self.pEOS = _fit_with_restarts(self, Vdata, Edata, p0, EOS4_BOUNDS, 'analytic', rel_tol, max_starts, on_failure)
        if not fit:
            self.pEOS = initial_parameters[:4]

        self.V0 = float(self.pEOS[1])  # the fitted V0 parameter is the minimum of E0 (was a bounded minimize, finding 3.10)

        # return self.pEOS

    def E04min(self, V: float, pEOS: np.ndarray) -> float:
        """
        Energy for minimization.

        :param V: Volume.
        :type V: float
        :param pEOS: parameters.
        :type pEOS: np.ndarray
        :return: E0.
        :rtype: float
        """
        E0, V0, B0, Bp0 = pEOS
        if B0<0:
            return 1
        P0, P1, P2, P3 = EVBBp_to_BMparams(pEOS)
        return P0 + P1 / V ** (2 / 3) + P2 / V ** (4 / 3) + P3 * V ** (-6 / 3)

    def E0(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: E0(V)
        :rtype: float|np.ndarray
        """
        return self.E04min(V, self.pEOS)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        P0, P1, P2, P3 = EVBBp_to_BMparams(self.pEOS)
        return -2 * P1 / (3 * V ** (5 / 3)) - 4 * P2 / (3 * V ** (7 / 3)) - 2 * P3 / V ** 3

    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        P0, P1, P2, P3 = EVBBp_to_BMparams(self.pEOS)
        return 10 * P1 / (9 * V ** (8 / 3)) + 28 * P2 / (9 * V ** (10 / 3)) + 6 * P3 / V ** 4

    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        P0, P1, P2, P3 = EVBBp_to_BMparams(self.pEOS)
        return -80 * P1 / (27 * V ** (11 / 3)) - 280 * P2 / (27 * V ** (13 / 3)) - 24 * P3 / V ** 5

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        P0, P1, P2, P3 = EVBBp_to_BMparams(self.pEOS)
        return 880 * P1 / (81 * V ** (14 / 3)) + 3640 * P2 / (81 * V ** (16 / 3)) + 120 * P3 / V ** 6

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        P0, P1, P2, P3 = EVBBp_to_BMparams(self.pEOS)
        return -12320 * P1 / (243 * V ** (17 / 3)) - 58240 * P2 / (243 * V ** (19 / 3)) - 720 * P3 / V ** 7

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        P0, P1, P2, P3 = EVBBp_to_BMparams(self.pEOS)
        return 209440 * P1 / (729 * V ** (20 / 3)) + 1106560 * P2 / (729 * V ** (22 / 3)) + 5040 * P3 / V ** 8

    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return np.asarray(Ecalc) - np.asarray(Edata)  # residuals; least_squares squares them (review finding 3.5)


class RV:  # Rose-Vinet
    """
    Rose-Vinet EOS and derivatives.

    """

    def __init__(self, *args, units='J/mol', parameters=''):
        if list(parameters):
            self.pEOS = parameters[:4]
            self.V0 = float(self.pEOS[1])

    def fitEOS(self, Vdata: np.ndarray, Edata: np.ndarray, initial_parameters: np.ndarray = None, fit: bool = True, rel_tol: float = 0.02, max_starts: int = 12, on_failure: str = 'raise') -> None:
        """
        Parameters fitting.

        :param Vdata: Input volume data.
        :type Vdata: np.ndarray
        :param Edata: Target energy data.
        :type Edata: np.ndarray
        :param initial_parameters: Initial guess.
        :type initial_parameters: np.ndarray
        :param fit: True to run the fitting. False to just use the input parameters.
        :type fit: bool.
        :param rel_tol: A fit is accepted when its rms is below rel_tol times the energy range of the data (and it has
            a minimum with B0 > 0 within a factor 2 of the data volumes); otherwise other starting points are tried.
        :param max_starts: Maximum number of starting points.
        :param on_failure: 'raise' (EOSFitError, default) or 'warn' (keep the best attempt) when no start passes.

        :return: Optimal parameters.
        :rtype: np.ndarray
        """
        if fit:
            p0 = None if initial_parameters is None or (isinstance(initial_parameters, str) and initial_parameters == '') \
                else np.asarray(initial_parameters, dtype=float)[:4]
            self.pEOS = _fit_with_restarts(self, Vdata, Edata, p0, EOS4_BOUNDS, 'analytic', rel_tol, max_starts, on_failure)
        if not fit:
            self.pEOS = initial_parameters[:4]

        self.V0 = float(self.pEOS[1])  # the fitted V0 parameter is the minimum of E0 (was a bounded minimize, finding 3.10)

        return self.pEOS

    def E04min(self, V: float, pEOS: np.ndarray) -> float:
        """
        Energy for minimization.

        :param V: Volume.
        :type V: float
        :param pEOS: parameters.
        :type pEOS: np.ndarray
        :return: E0.
        :rtype: float
        """
        E0, V0, B0, Bp0 = pEOS
        if B0<0:
            return 1
        return E0 - 2 * B0 * V0 * np.exp(-(1 / 2) * (3 * (Bp0 - 1)) * (-1 + (V / V0) ** (1 / 3))) * (
                    3 * (V / V0) ** (1 / 3) * Bp0 - 3 * Bp0 - 3 * (V / V0) ** (1 / 3) + 5) / (Bp0 - 1) ** 2 + (
                           4 * B0 * V0) / ((Bp0 - 1) ** 2)

    def E0(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: E0(V)
        :rtype: float|np.ndarray
        """
        return self.E04min(V, self.pEOS)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -(3 * (V0 - V ** (1 / 3) * V0 ** (2 / 3))) * np.exp(
            (3 * (Bp0 - 1)) * (V0 - V ** (1 / 3) * V0 ** (2 / 3)) / (2 * V0)) * B0 / (V0 ** (1 / 3) * V ** (2 / 3))

    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -(3 * Bp0 * (V / V0) ** (2 / 3) - 3 * (V / V0) ** (1 / 3) * Bp0 - 3 * (V / V0) ** (2 / 3) + 5 * (
                    V / V0) ** (1 / 3) - 4) * np.exp(-(1 / 2) * (3 * (Bp0 - 1)) * (-1 + (V / V0) ** (1 / 3))) * B0 / (
                           2 * V * (V / V0) ** (2 / 3))

    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return 3 * np.exp(-(1 / 2) * (3 * (Bp0 - 1)) * (-1 + (V / V0) ** (1 / 3))) * (
                    -(Bp0 - 1) * V0 * (Bp0 - 11 / 3) * (V / V0) ** (2 / 3) - (4 * (Bp0 - 13 / 9)) * V0 * (V / V0) ** (
                        1 / 3) + Bp0 ** 2 * V - 2 * Bp0 * V + V - 40 * V0 * (1 / 9)) * B0 / (
                           4 * (V / V0) ** (2 / 3) * V ** 2 * V0)

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -(3 * (-(8 * (Bp0 - 23 / 9)) * (Bp0 - 1) * V0 * (V / V0) ** (2 / 3) + (
                    Bp0 ** 3 * V - 3 * Bp0 ** 2 * V + (3 * V - 208 * V0 * (1 / 9)) * Bp0 - V + 848 * V0 * (1 / 27)) * (
                                  V / V0) ** (
                                  1 / 3) - Bp0 ** 3 * V + 9 * Bp0 ** 2 * V - 15 * Bp0 * V + 7 * V - 640 * V0 * (
                                  1 / 27))) * np.exp(-(1 / 2) * (3 * (Bp0 - 1)) * (-1 + (V / V0) ** (1 / 3))) * B0 / (
                           8 * (V / V0) ** (2 / 3) * V ** 3 * V0)

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -5 * np.exp((3 * (Bp0 - 1)) * (V0 - V ** (1 / 3) * V0 ** (2 / 3)) / (2 * V0)) * (
                    (1 / 40) * (3 * (Bp0 - 35 / 3)) * (Bp0 - 1) ** 3 * V ** (4 / 3) * V0 ** (2 / 3) - 3 * V0 ** (
                        1 / 3) * (Bp0 - 1) ** 4 * V ** (5 / 3) * (1 / 40) + 16 * V ** (2 / 3) * (Bp0 - 13 / 6) * (
                                Bp0 - 1) * V0 ** (4 / 3) * (1 / 3) + (1 / 3) * (40 * (Bp0 - 59 / 45)) * V ** (
                                1 / 3) * V0 ** (5 / 3) + V0 * (
                                Bp0 ** 3 * V - (19 / 3) * Bp0 ** 2 * V + (29 / 3) * Bp0 * V - (13 / 3) * V + (
                                    352 / 27) * V0)) * B0 / (2 * V0 ** (4 / 3) * V ** (14 / 3))

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        # exact 6th derivative (sympy, finding 3.6); x = (V/V0)^(1/3)
        x = (V / V0) ** (1 / 3)
        c0 = 394240
        c1 = 416640*Bp0 - 533120
        c2 = Bp0*(181440*Bp0 - 537600) + 356160
        c3 = Bp0*(Bp0*(41040*Bp0 - 222480) + 321840) - 140400
        c4 = Bp0*(Bp0*(Bp0*(4860*Bp0 - 47520) + 113400) - 103680) + 32940
        c5 = Bp0*(Bp0*(Bp0*(Bp0*(243*Bp0 - 5265) + 18630) - 26730) + 17415) - 4293
        c6 = -243*(Bp0 - 1)**5
        Q = c0 + x*(c1 + x*(c2 + x*(c3 + x*(c4 + x*(c5 + x*c6)))))
        return B0 / V0 ** 5 * np.exp(1.5 * (Bp0 - 1) * (1 - x)) * Q / (2592 * x ** 17)

    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return np.asarray(Ecalc) - np.asarray(Edata)  # residuals; least_squares squares them (review finding 3.5)


class MG:  # Mie-Gruneisen
    """
    Mie-Gruneisen EOS and derivatives.
    """

    def __init__(self, *args, units='J/mol', parameters=''):
        if list(parameters):
            self.pEOS = parameters[:4]
            self.V0 = float(self.pEOS[1])

    def fitEOS(self, Vdata: np.ndarray, Edata: np.ndarray, initial_parameters: np.ndarray = None, fit: bool = True, rel_tol: float = 0.02, max_starts: int = 12, on_failure: str = 'raise') -> None:
        """
        Parameters fitting.

        :param Vdata: Input volume data.
        :type Vdata: np.ndarray
        :param Edata: Target energy data.
        :type Edata: np.ndarray
        :param initial_parameters: Initial guess.
        :type initial_parameters: np.ndarray
        :param fit: True to run the fitting. False to just use the input parameters.
        :type fit: bool.
        :param rel_tol: A fit is accepted when its rms is below rel_tol times the energy range of the data (and it has
            a minimum with B0 > 0 within a factor 2 of the data volumes); otherwise other starting points are tried.
        :param max_starts: Maximum number of starting points.
        :param on_failure: 'raise' (EOSFitError, default) or 'warn' (keep the best attempt) when no start passes.

        :return: Optimal parameters.
        :rtype: np.ndarray
        """
        if fit:
            p0 = None if initial_parameters is None or (isinstance(initial_parameters, str) and initial_parameters == '') \
                else np.asarray(initial_parameters, dtype=float)[:4]
            self.pEOS = _fit_with_restarts(self, Vdata, Edata, p0, EOS4_BOUNDS, 'analytic', rel_tol, max_starts, on_failure)
        if not fit:
            self.pEOS = initial_parameters[:4]

        self.V0 = float(self.pEOS[1])  # the fitted V0 parameter is the minimum of E0 (was a bounded minimize, finding 3.10)

        return self.pEOS

    def E04min(self, V: float, pEOS: np.ndarray) -> float:
        """
        Energy for minimization.

        :param V: Volume.
        :type V: float
        :param pEOS: parameters.
        :type pEOS: np.ndarray
        :return: E0.
        :rtype: float
        """
        E0, V0, B0, Bp0 = pEOS
        if B0<0:
            return 1
        return (9 * ((3 * (B0 * V0 + (1 / 3) * Bp0 * E0 - (7 / 9) * E0)) * (Bp0 - 8 / 3) * (V / V0) ** (
                    1 / 3) + B0 * V0 * ((V / V0) ** (8 / 3 - Bp0) - 3 * Bp0 + 7))) / (
                           (V / V0) ** (1 / 3) * (9 * Bp0 ** 2 - 45 * Bp0 + 56))

    def E0(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: E0(V)
        :rtype: float|np.ndarray
        """
        return self.E04min(V, self.pEOS)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -(3 * (V ** (8 / 3 - Bp0) * V0 ** (Bp0 - 8 / 3) - 1)) * B0 * V0 ** (4 / 3) / (
                    V ** (4 / 3) * (3 * Bp0 - 8))

    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return (3 * Bp0 * (V / V0) ** (8 / 3 - Bp0) - 4 * (V / V0) ** (8 / 3 - Bp0) - 4) * B0 * V0 / (
                    V ** 2 * (3 * Bp0 - 8) * (V / V0) ** (1 / 3))

    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -3 * B0 * (-28 / 9 + (Bp0 ** 2 - (5 / 3) * Bp0 + 4 / 9) * (V / V0) ** (8 / 3 - Bp0)) * V0 / (
                    (V / V0) ** (1 / 3) * V ** 3 * (3 * Bp0 - 8))

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return 3 * B0 * (
                    -280 / 27 + (Bp0 ** 3 - Bp0 ** 2 - (2 / 3) * Bp0 + 8 / 27) * (V / V0) ** (8 / 3 - Bp0)) * V0 / (
                           (V / V0) ** (1 / 3) * V ** 4 * (3 * Bp0 - 8))

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -81 * V0 ** (4 / 3) * B0 * (-3640 / 81 + (1 / 81) * V0 ** (Bp0 - 8 / 3) * (
                    81 * Bp0 ** 4 + 54 * Bp0 ** 3 - 189 * Bp0 ** 2 - 66 * Bp0 + 40) * V ** (8 / 3 - Bp0)) / (
                           V ** (16 / 3) * (-216 + 81 * Bp0))

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -V0 ** (4 / 3) * B0 * V0 ** (Bp0 - 8 / 3) * (
                    81 * Bp0 ** 4 + 54 * Bp0 ** 3 - 189 * Bp0 ** 2 - 66 * Bp0 + 40) * V ** (8 / 3 - Bp0) * (
                           8 / 3 - Bp0) / (V ** (19 / 3) * (-216 + 81 * Bp0)) + 432 * V0 ** (4 / 3) * B0 * (
                           -3640 / 81 + (1 / 81) * V0 ** (Bp0 - 8 / 3) * (
                               81 * Bp0 ** 4 + 54 * Bp0 ** 3 - 189 * Bp0 ** 2 - 66 * Bp0 + 40) * V ** (8 / 3 - Bp0)) / (
                           V ** (19 / 3) * (-216 + 81 * Bp0))

    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return np.asarray(Ecalc) - np.asarray(Edata)  # residuals; least_squares squares them (review finding 3.5)


class TB:  # TB-SMA
    """
    Thight-Binding second-order-approximation EOS and derivatives.
    """

    def __init__(self, *args, units='J/mol', parameters=''):
        if list(parameters):
            self.pEOS = parameters[:4]
            self.V0 = float(self.pEOS[1])

    def fitEOS(self, Vdata, Edata, initial_parameters='', fit=True, rel_tol=0.02, max_starts=12, on_failure='raise'):
        """
        Parameters fitting.

        :param list_of_floats Vdata: Input data.
        :param list_of_floats Edata: Target data.
        :param list_of_floats initial_parameters: initial_parameters.

        :return list_of_floats: Optimal parameters.
        """
        if fit:
            p0 = None if initial_parameters is None or (isinstance(initial_parameters, str) and initial_parameters == '') \
                else np.asarray(initial_parameters, dtype=float)[:4]
            self.pEOS = _fit_with_restarts(self, Vdata, Edata, p0, EOS4_BOUNDS, 'analytic', rel_tol, max_starts, on_failure)
        if not fit:
            self.pEOS = initial_parameters[:4]

        self.V0 = float(self.pEOS[1])  # the fitted V0 parameter is the minimum of E0 (was a bounded minimize, finding 3.10)

        return self.pEOS

    def E04min(self, V, pEOS):

        E0, V0, B0, Bp0 = pEOS
        if B0<0:
            return 1
        p0, p1, p2, p3 = EVBBp_to_TBparams(pEOS)
        return p0 * np.exp(-p2 * V ** (1. / 3.)) + p1 * np.exp(-p3 * V ** (1. / 3.))

    def E0(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: E0(V)
        :rtype: float|np.ndarray
        """
        return self.E04min(V, self.pEOS)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        p0, p1, p2, p3 = EVBBp_to_TBparams(self.pEOS)
        return -(p0 * p2 * np.exp(-p2 * V ** (1 / 3)) + p1 * p3 * np.exp(-p3 * V ** (1 / 3))) / (3 * V ** (2 / 3))

    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        p0, p1, p2, p3 = EVBBp_to_TBparams(self.pEOS)
        return 2 * p0 * p2 * np.exp(-p2 * V ** (1 / 3)) / (9 * V ** (5 / 3)) + p0 * p2 ** 2 * np.exp(
            -p2 * V ** (1 / 3)) / (9 * V ** (4 / 3)) + 2 * p1 * p3 * np.exp(-p3 * V ** (1 / 3)) / (
                           9 * V ** (5 / 3)) + p1 * p3 ** 2 * np.exp(-p3 * V ** (1 / 3)) / (9 * V ** (4 / 3))

    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        p0, p1, p2, p3 = EVBBp_to_TBparams(self.pEOS)
        return -10 * p0 * p2 * np.exp(-p2 * V ** (1 / 3)) / (27 * V ** (8 / 3)) - 2 * p0 * p2 ** 2 * np.exp(
            -p2 * V ** (1 / 3)) / (9 * V ** (7 / 3)) - p0 * p2 ** 3 * np.exp(-p2 * V ** (1 / 3)) / (
                           27 * V ** 2) - 10 * p1 * p3 * np.exp(-p3 * V ** (1 / 3)) / (
                           27 * V ** (8 / 3)) - 2 * p1 * p3 ** 2 * np.exp(-p3 * V ** (1 / 3)) / (
                           9 * V ** (7 / 3)) - p1 * p3 ** 3 * np.exp(-p3 * V ** (1 / 3)) / (27 * V ** 2)

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        p0, p1, p2, p3 = EVBBp_to_TBparams(self.pEOS)
        return 80 * p0 * p2 * np.exp(-p2 * V ** (1 / 3)) / (81 * V ** (11 / 3)) + 52 * p0 * p2 ** 2 * np.exp(
            -p2 * V ** (1 / 3)) / (81 * V ** (10 / 3)) + 4 * p0 * p2 ** 3 * np.exp(-p2 * V ** (1 / 3)) / (
                           27 * V ** 3) + p0 * p2 ** 4 * np.exp(-p2 * V ** (1 / 3)) / (
                           81 * V ** (8 / 3)) + 80 * p1 * p3 * np.exp(-p3 * V ** (1 / 3)) / (
                           81 * V ** (11 / 3)) + 52 * p1 * p3 ** 2 * np.exp(-p3 * V ** (1 / 3)) / (
                           81 * V ** (10 / 3)) + 4 * p1 * p3 ** 3 * np.exp(-p3 * V ** (1 / 3)) / (
                           27 * V ** 3) + p1 * p3 ** 4 * np.exp(-p3 * V ** (1 / 3)) / (81 * V ** (8 / 3))

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        p0, p1, p2, p3 = EVBBp_to_TBparams(self.pEOS)
        return -(20 * (p0 * p2 * (
                    (1 / 20) * V ** (4 / 3) * p2 ** 4 + V * p2 ** 3 + 8 * p2 ** 2 * V ** (2 / 3) + 30 * p2 * V ** (
                        1 / 3) + 44) * np.exp(-p2 * V ** (1 / 3)) + np.exp(-p3 * V ** (1 / 3)) * p1 * p3 * (
                                   (1 / 20) * V ** (4 / 3) * p3 ** 4 + V * p3 ** 3 + 8 * p3 ** 2 * V ** (
                                       2 / 3) + 30 * p3 * V ** (1 / 3) + 44))) / (243 * V ** (14 / 3))

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        p0, p1, p2, p3 = EVBBp_to_TBparams(self.pEOS)
        return (380 * (p0 * p2 * ((1 / 380) * V ** (5 / 3) * p2 ** 5 + 3 * V ** (4 / 3) * p2 ** 4 * (
                    1 / 38) + V * p2 ** 3 + 126 * p2 ** 2 * V ** (2 / 3) * (1 / 19) + 434 * p2 * V ** (1 / 3) * (
                                              1 / 19) + 616 / 19) * np.exp(-p2 * V ** (1 / 3)) + np.exp(
            -p3 * V ** (1 / 3)) * p1 * p3 * ((1 / 380) * V ** (5 / 3) * p3 ** 5 + 3 * V ** (4 / 3) * p3 ** 4 * (
                    1 / 38) + V * p3 ** 3 + 126 * p3 ** 2 * V ** (2 / 3) * (1 / 19) + 434 * p3 * V ** (1 / 3) * (
                                                         1 / 19) + 616 / 19))) / (729 * V ** (17 / 3))

    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return np.asarray(Ecalc) - np.asarray(Edata)  # residuals; least_squares squares them (review finding 3.5)


class MP:  # Morse
    """
    Morse potential and derivatives.

    :param list args: formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels.
    :param list_of_floats parameters: Morse potential parameters.
    """

    def __init__(self, *args, units='J/mol', parameters='', prec=10):
        formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels = args
        self.formula, self.primitive_cell, self.basis_vectors = formula, primitive_cell, basis_vectors

        size = np.array([1, 1, 1])
        atom_types = formula * np.prod(size)
        neigbor_distances_at_Vstar, number_of_pairs_per_distance, comb_types = pairanalysis.pair_analysis(atom_types,
                                                                                                          cutoff,
                                                                                                          basis_vectors,
                                                                                                          primitive_cell,
                                                                                                          prec=prec)

        neigbor_distances_at_Vstar, number_of_pairs_per_distance = neigbor_distances_at_Vstar[
                                                                   :number_of_neighbor_levels], number_of_pairs_per_distance[
                                                                                                :number_of_neighbor_levels,
                                                                                                :]

        self.comb_types = comb_types
        primitive_cell = np.array(primitive_cell)
        aa, bb, cc = primitive_cell[0,:], primitive_cell[1,:], primitive_cell[2,:]
        # Vstar = np.linalg.det(primitive_cell) / len(basis_vectors)
        Vstar = calculate_volume(aa, bb, cc) / len(basis_vectors)

        self.ndist = neigbor_distances_at_Vstar
        self.npair = number_of_pairs_per_distance
        self.Vstar = Vstar

        if units == 'J/mol':
            self.mult_V = A3_ATOM_TO_M3_MOL
            self.mult_E = EV_ATOM_TO_J_MOL

        elif units == 'eV/atom':
            self.mult_V = 1
            self.mult_E = 1
        self.ixsss = 0

        if list(parameters):
            self.pEOS = parameters
        #### pr0nt('xxx',self.ndist,self.npair,self.Vstar)

    def default_initial_parameters(self, Vdata, Edata) -> np.ndarray:
        """
        Starting point when no initial_parameters are given: for every pair type D = 0.5 eV, alpha = 1.5 1/A and
        r0 = the nearest-neighbour distance at the data volume with the lowest energy.
        """
        V = np.asarray(Vdata, dtype=float); E = np.asarray(Edata, dtype=float)
        Vmin = V[np.argmin(E)] if V.size > 1 else float(np.ravel(V)[0])
        r_nn = float(self.ndist[0]) * (Vmin / self.mult_V / self.Vstar) ** (1 / 3)
        return np.tile([0.5, 1.5, r_nn], int(np.shape(self.npair)[1]))

    def fitEOS(self, Vdata: np.ndarray, Edata: np.ndarray, initial_parameters: np.ndarray = None, fit: bool = True, rel_tol: float = 0.02, max_starts: int = 12, on_failure: str = 'raise') -> None:
        """
        Parameters fitting.

        :param Vdata: Input volume data.
        :type Vdata: np.ndarray
        :param Edata: Target energy data.
        :type Edata: np.ndarray
        :param initial_parameters: Initial guess.
        :type initial_parameters: np.ndarray
        :param fit: True to run the fitting. False to just use the input parameters.
        :type fit: bool.
        :param rel_tol: A fit is accepted when its rms is below rel_tol times the energy range of the data (and it has
            a minimum with B0 > 0 within a factor 2 of the data volumes); otherwise other starting points are tried.
        :param max_starts: Maximum number of starting points.
        :param on_failure: 'raise' (EOSFitError, default) or 'warn' (keep the best attempt) when no start passes.

        :return: Optimal parameters.
        :rtype: np.ndarray
        """
        if fit:
            if initial_parameters is None:
                initial_parameters = self.default_initial_parameters(Vdata, Edata)
            self.pEOS = _fit_with_restarts(self, Vdata, Edata, np.asarray(initial_parameters, dtype=float), (0, np.inf),
                                           'pair', rel_tol, max_starts, on_failure)
        if not fit:
            self.pEOS = initial_parameters

        self.V0 = _V0_from_dE0dV(self, Vdata)  # root of dE0/dV (was a bounded minimize, finding 3.10)

        return self.pEOS

    def E04min(self, V: float, pEOS: np.ndarray) -> float:
        """
        Energy for minimization.

        :param V: Volume.
        :type V: float
        :param pEOS: parameters.
        :type pEOS: np.ndarray
        :return: E0.
        :rtype: float
        """
        if type(V) == np.ndarray:
            return np.array([self.E04min(Vi, pEOS) for Vi in V])

        V = V / self.mult_V

        pEOS = np.reshape(pEOS, (int(len(pEOS) / 3), 3))
        Ds, alphas, r0s = pEOS.T[:]
        ms = 0
        for njs, Dj, alphaj, r0j in zip(self.npair.T, Ds, alphas, r0s):
            for rstari, nij in zip(self.ndist, njs):
                ms += (nij / 2 * Dj * ((1 - np.exp(-alphaj * (rstari * (V / self.Vstar) ** (1 / 3) - r0j))) ** 2 - 1))

        return ms * (self.mult_E)

    def E0(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: E0(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.E0(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS = self.pEOS
        pEOS = pEOS.reshape((int(len(pEOS) / 3)), 3)
        Ds, alphas, r0s = pEOS.T[:]
        ms = []
        for njs, Dj, alphaj, r0j in zip(self.npair.T, Ds, alphas, r0s):
            for rstari, nij in zip(self.ndist, njs):
                ms.append(nij / 2 * Dj * ((1 - np.exp(-alphaj * (rstari * (V / self.Vstar) ** (1 / 3) - r0j))) ** 2 - 1))
        return np.sum(ms) * (self.mult_E)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.dE0dV_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS = self.pEOS
        pEOS = pEOS.reshape((int(len(pEOS) / 3)), 3)
        Ds, alphas, r0s = pEOS.T[:]
        ms = []
        for njs, Dj, alphaj, r0j in zip(self.npair.T, Ds, alphas, r0s):
            for rstari, nij in zip(self.ndist, njs):
                ms.append(-nij * Dj * (-1 + np.exp(alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (2 / 3)) / self.Vstar)) * alphaj * rstari * np.exp(alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (2 / 3)) / self.Vstar) / (3 * self.Vstar ** (1 / 3) * V ** (2 / 3)))
        return np.sum(ms) * (self.mult_E) / (self.mult_V)

    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d2E0dV2_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS = self.pEOS
        pEOS = pEOS.reshape((int(len(pEOS) / 3)), 3)
        Ds, alphas, r0s = pEOS.T[:]
        ms = []
        for njs, Dj, alphaj, r0j in zip(self.npair.T, Ds, alphas, r0s):
            for rstari, nij in zip(self.ndist, njs):
                ms.append(2*np.exp(alphaj*(r0j*self.Vstar-rstari*V**(1/3)*self.Vstar**(2/3))/self.Vstar)*nij*alphaj*rstari*Dj*((alphaj*rstari*V**(1/3)*self.Vstar**(2/3)+self.Vstar)*np.exp(alphaj*(r0j*self.Vstar-rstari*V**(1/3)*self.Vstar**(2/3))/self.Vstar)-(1/2)*alphaj*rstari*V**(1/3)*self.Vstar**(2/3)-self.Vstar)/(9*V**(5/3)*self.Vstar**(4/3)))
        return np.sum(ms) * (self.mult_E) / (self.mult_V) ** 2

    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d3E0dV3_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS = self.pEOS
        pEOS = pEOS.reshape((int(len(pEOS) / 3)), 3)
        Ds, alphas, r0s = pEOS.T[:]
        ms = []
        for njs, Dj, alphaj, r0j in zip(self.npair.T, Ds, alphas, r0s):
            for rstari, nij in zip(self.ndist, njs):
                ms.append(-nij*Dj*alphaj*rstari*np.exp(alphaj*(r0j*self.Vstar-rstari*V**(1/3)*self.Vstar**(2/3))/self.Vstar)*(4*np.exp(alphaj*(r0j*self.Vstar-rstari*V**(1/3)*self.Vstar**(2 / 3)) / self.Vstar) * alphaj ** 2 * rstari ** 2 * V ** (2 / 3) * self.Vstar ** (1 / 3) - alphaj ** 2 * rstari ** 2 * V ** (2 / 3) * self.Vstar ** (1 / 3) + 12 * alphaj * rstari * np.exp(alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (2 / 3)) / self.Vstar) * V ** (1 / 3) * self.Vstar ** (2 / 3) - 6 * alphaj * rstari * V ** (1 / 3) * self.Vstar ** (2 / 3) + 10 * self.Vstar * np.exp(alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (2 / 3)) / self.Vstar) - 10 * self.Vstar) / (27 * self.Vstar ** (4 / 3) * V ** (8 / 3)))
        return np.sum(ms) * (self.mult_E) / (self.mult_V) ** 3

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d4E0dV4_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS = self.pEOS
        pEOS = pEOS.reshape((int(len(pEOS) / 3)), 3)
        Ds, alphas, r0s = pEOS.T[:]
        ms = []
        for njs, Dj, alphaj, r0j in zip(self.npair.T, Ds, alphas, r0s):
            for rstari, nij in zip(self.ndist, njs):
                ms.append(8*nij*alphaj*np.exp(alphaj*(r0j*self.Vstar-rstari*V**(1/3)*self.Vstar**(2/3))/self.Vstar)*((V*alphaj**3*rstari**3+6*alphaj**2*rstari**2*V**(2/3)*self.Vstar**(1/3)+13*alphaj*rstari*V**(1/3)*self.Vstar**(2/3)+10*self.Vstar)*np.exp(alphaj*(r0j*self.Vstar-rstari*V**(1/3)*self.Vstar**(2/3))/self.Vstar)-(1/8)*V*alphaj**3*rstari**3-3*alphaj**2*rstari**2*V**(2/3)*self.Vstar**(1/3)*(1/2)-13*alphaj*rstari*V**(1/3)*self.Vstar**(2/3)*(1/2)-10*self.Vstar)*rstari*Dj/(81*self.Vstar**(4/3)*V**(11/3)))
        return np.sum(ms) * (self.mult_E) / (self.mult_V) ** 4

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d5E0dV5_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS = self.pEOS
        pEOS = pEOS.reshape((int(len(pEOS) / 3)), 3)
        Ds, alphas, r0s = pEOS.T[:]
        ms = []
        for njs, Dj, alphaj, r0j in zip(self.npair.T, Ds, alphas, r0s):
            for rstari, nij in zip(self.ndist, njs):
                ms.append(-nij * Dj * alphaj * rstari * np.exp(alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (2 / 3)) / self.Vstar) * (16 * np.exp(alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (  2 / 3)) / self.Vstar) * V ** (  4 / 3) * alphaj ** 4 * rstari ** 4 * self.Vstar ** (2 / 3) - V ** (  4 / 3) * alphaj ** 4 * rstari ** 4 * self.Vstar ** (2 / 3) + 160 * np.exp(alphaj * (  r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (  2 / 3)) / self.Vstar) * V * self.Vstar * alphaj ** 3 * rstari ** 3 - 20 * V * self.Vstar * alphaj ** 3 * rstari ** 3 + 640 * np.exp(  alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (  2 / 3)) / self.Vstar) * alphaj ** 2 * rstari ** 2 * V ** (  2 / 3) * self.Vstar ** (  4 / 3) - 160 * alphaj ** 2 * rstari ** 2 * V ** (  2 / 3) * self.Vstar ** (4 / 3) + 1200 * np.exp(alphaj * (  r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (  2 / 3)) / self.Vstar) * self.Vstar ** (5 / 3) * alphaj * rstari * V ** (  1 / 3) - 600 * self.Vstar ** (5 / 3) * alphaj * rstari * V ** (1 / 3) + 880 * np.exp(alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (  2 / 3)) / self.Vstar) * self.Vstar ** 2 - 880 * self.Vstar ** 2) / (  243 * V ** (14 / 3) * self.Vstar ** (7 / 3)))
        return np.sum(ms) * (self.mult_E) / (self.mult_V) ** 5

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d6E0dV6_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS = self.pEOS
        pEOS = pEOS.reshape((int(len(pEOS) / 3)), 3)
        Ds, alphas, r0s = pEOS.T[:]
        ms = []
        for njs, Dj, alphaj, r0j in zip(self.npair.T, Ds, alphas, r0s):
            for rstari, nij in zip(self.ndist, njs):
                ms.append(nij * Dj * alphaj * rstari * np.exp(
                    alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (2 / 3)) / self.Vstar) * (
                                  32 * np.exp(alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (
                                          2 / 3)) / self.Vstar) * V ** (
                                                  5 / 3) * alphaj ** 5 * rstari ** 5 * self.Vstar ** (1 / 3) - V ** (
                                          5 / 3) * alphaj ** 5 * rstari ** 5 * self.Vstar ** (
                                                  1 / 3) + 480 * np.exp(alphaj * (
                                          r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (
                                  2 / 3)) / self.Vstar) * V ** (
                                          4 / 3) * alphaj ** 4 * rstari ** 4 * self.Vstar ** (
                                                  2 / 3) - 30 * V ** (
                                                  4 / 3) * alphaj ** 4 * rstari ** 4 * self.Vstar ** (
                                          2 / 3) + 3040 * np.exp(alphaj * (
                                  r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (
                                              2 / 3)) / self.Vstar) * V * self.Vstar * alphaj ** 3 * rstari ** 3 + 10080 * np.exp(
                                  alphaj * (r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (
                                              2 / 3)) / self.Vstar) * alphaj ** 2 * rstari ** 2 * V ** (
                                                  2 / 3) * self.Vstar ** (
                                                  4 / 3) - 380 * V * self.Vstar * alphaj ** 3 * rstari ** 3 - 2520 * alphaj ** 2 * rstari ** 2 * V ** (
                                                  2 / 3) * self.Vstar ** (4 / 3) + 17360 * np.exp(alphaj * (
                                          r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (
                                              2 / 3)) / self.Vstar) * self.Vstar ** (5 / 3) * alphaj * rstari * V ** (
                                                  1 / 3) - 8680 * self.Vstar ** (5 / 3) * alphaj * rstari * V ** (
                                                  1 / 3) + 12320 * np.exp(alphaj * (
                                          r0j * self.Vstar - rstari * V ** (1 / 3) * self.Vstar ** (
                                              2 / 3)) / self.Vstar) * self.Vstar ** 2 - 12320 * self.Vstar ** 2) / (
                                      729 * self.Vstar ** (7 / 3) * V ** (17 / 3)))
        return np.sum(ms) * (self.mult_E) / (self.mult_V) ** 6

    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return np.asarray(Ecalc) - np.asarray(Edata)  # residuals; least_squares squares them (review finding 3.5)


class MU:  # Murnaghan
    """
    Murnaghan EOS and derivatives.
    """

    def __init__(self, *args, units='J/mol', parameters=''):
        self.V0 = None
        if list(parameters):
            self.pEOS = parameters[:4]
            self.V0 = float(self.pEOS[1])

    def fitEOS(self, Vdata: np.ndarray, Edata: np.ndarray, initial_parameters: np.ndarray = None, fit: bool = True, rel_tol: float = 0.02, max_starts: int = 12, on_failure: str = 'raise') -> None:
        """
        Parameters fitting.

        :param Vdata: Input volume data.
        :type Vdata: np.ndarray
        :param Edata: Target energy data.
        :type Edata: np.ndarray
        :param initial_parameters: Initial guess.
        :type initial_parameters: np.ndarray
        :param fit: True to run the fitting. False to just use the input parameters.
        :type fit: bool.
        :param rel_tol: A fit is accepted when its rms is below rel_tol times the energy range of the data (and it has
            a minimum with B0 > 0 within a factor 2 of the data volumes); otherwise other starting points are tried.
        :param max_starts: Maximum number of starting points.
        :param on_failure: 'raise' (EOSFitError, default) or 'warn' (keep the best attempt) when no start passes.

        :return: Optimal parameters.
        :rtype: np.ndarray
        """
        if fit:
            p0 = None if initial_parameters is None else np.asarray(initial_parameters, dtype=float)[:4]
            self.pEOS = _fit_with_restarts(self, Vdata, Edata, p0, ([-np.inf, 0, 0, 0], [0, np.inf, np.inf, np.inf]),
                                           'analytic', rel_tol, max_starts, on_failure)
        if not fit:
            self.pEOS = initial_parameters[:4]

        self.V0 = float(self.pEOS[1])  # the fitted V0 parameter is the minimum of E0 (was a bounded minimize, finding 3.10)

        return self.pEOS

    def E04min(self, V: float, pEOS: np.ndarray) -> float:
        """
        Energy for minimization.

        :param V: Volume.
        :type V: float
        :param pEOS: parameters.
        :type pEOS: np.ndarray
        :return: E0.
        :rtype: float
        """
        E0, V0, B0, Bp0 = pEOS
        if B0<0:
            return 1
        return E0 + B0 * V0 * (1 / (Bp0 * (Bp0 - 1)) * (V / V0) ** (1 - Bp0) + 1 / Bp0 * V / V0 - 1 / (Bp0 - 1))

    def E0(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: E0(V)
        :rtype: float|np.ndarray
        """
        return self.E04min(V, self.pEOS)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -B0 * (V / V0) ** (-Bp0) / Bp0 + B0 / Bp0

    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return B0 * (V / V0) ** (-Bp0) / V

    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -B0 * (V / V0) ** (-Bp0) * (Bp0 + 1) / V ** 2

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return B0 * (V / V0) ** (-Bp0) * (Bp0 ** 2 + 3 * Bp0 + 2) / V ** 3

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -B0 * (V / V0) ** (-Bp0) * (Bp0 ** 3 + 6 * Bp0 ** 2 + 11 * Bp0 + 6) / V ** 4

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return B0 * (V / V0) ** (-Bp0) * (Bp0 ** 4 + 10 * Bp0 ** 3 + 35 * Bp0 ** 2 + 50 * Bp0 + 24) / V ** 5

    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return np.asarray(Ecalc) - np.asarray(Edata)  # residuals; least_squares squares them (review finding 3.5)


class BM3(BM):  # deprecated alias of BM
    """
    Deprecated alias of :class:`BM` (third-order Birch-Murnaghan EOS).

    The former separate BM3 implementation had the same E0 as BM but all its volume derivatives
    had the wrong sign (debyetools review finding 3.1). BM3 now is BM and emits a DeprecationWarning.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn("BM3 is deprecated: use BM (same third-order Birch-Murnaghan EOS).",
                      DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)


class PT:  # Poirier-Tarantola
    """
    Poirier-Tarantola EOS and derivatives.
    """

    def __init__(self, *args, units='J/mol', parameters=''):
        if list(parameters):
            self.pEOS = parameters[:4]
            self.V0 = float(self.pEOS[1])

    def fitEOS(self, Vdata: np.ndarray, Edata: np.ndarray, initial_parameters: np.ndarray = None, fit: bool = True, rel_tol: float = 0.02, max_starts: int = 12, on_failure: str = 'raise') -> None:
        """
        Parameters fitting.

        :param Vdata: Input volume data.
        :type Vdata: np.ndarray
        :param Edata: Target energy data.
        :type Edata: np.ndarray
        :param initial_parameters: Initial guess.
        :type initial_parameters: np.ndarray
        :param fit: True to run the fitting. False to just use the input parameters.
        :type fit: bool.
        :param rel_tol: A fit is accepted when its rms is below rel_tol times the energy range of the data (and it has
            a minimum with B0 > 0 within a factor 2 of the data volumes); otherwise other starting points are tried.
        :param max_starts: Maximum number of starting points.
        :param on_failure: 'raise' (EOSFitError, default) or 'warn' (keep the best attempt) when no start passes.

        :return: Optimal parameters.
        :rtype: np.ndarray
        """
        if fit:
            p0 = None if initial_parameters is None or (isinstance(initial_parameters, str) and initial_parameters == '') \
                else np.asarray(initial_parameters, dtype=float)[:4]
            self.pEOS = _fit_with_restarts(self, Vdata, Edata, p0, EOS4_BOUNDS, 'analytic', rel_tol, max_starts, on_failure)
        if not fit:
            self.pEOS = initial_parameters[:4]

        self.V0 = float(self.pEOS[1])  # the fitted V0 parameter is the minimum of E0 (was a bounded minimize, finding 3.10)

        return self.pEOS

    def E04min(self, V: float, pEOS: np.ndarray) -> float:
        """
        Energy for minimization.

        :param V: Volume.
        :type V: float
        :param pEOS: parameters.
        :type pEOS: np.ndarray
        :return: E0.
        :rtype: float
        """
        E0, V0, B0, Bp0 = pEOS
        if B0<0:
            return 1

        # E0 + K/6*V0(ln(V/V0))^2 (3-(Kp-2)ln(V/V0))
        return E0 + (1 / 6) * B0 * V0 * np.log(V / V0) ** 2 * (3 - (Bp0 - 2) * np.log(V / V0))  # (1/6)*B0*V0*(Bp0-2)*np.log(V0/V)**3-(1/2)*B0*V0*np.log(V0/V)**2+E0

    def E0(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: E0(V)
        :rtype: float|np.ndarray
        """
        return self.E04min(V, self.pEOS)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -V0 * (-2 + (Bp0 - 2) * np.log(V / V0)) * B0 * np.log(V / V0) / (
                    2 * V)  # B0*(2+(Bp0-2)*np.log(V0/V))*V0*np.log(V0/V)/(2*V)

    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return V0 * B0 * (2 + (Bp0 - 2) * np.log(V / V0) ** 2 + (-2 * Bp0 + 2) * np.log(V / V0)) / (
                    2 * V ** 2)  # -(2+(Bp0-2)*np.log(V0/V)**2+(2*Bp0-2)*np.log(V0/V))*B0*V0/(2*V**2)

    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -V0 * B0 * ((Bp0 - 2) * np.log(V / V0) ** 2 + (-3 * Bp0 + 4) * np.log(
            V / V0) + Bp0 + 1) / V ** 3  # B0*((Bp0-2)*np.log(V0/V)**2+(3*Bp0-4)*np.log(V0/V)+Bp0+1)*V0/V**3

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return B0 * V0 * (3 * np.log(V / V0) ** 2 * Bp0 - 11 * np.log(V / V0) * Bp0 - 6 * np.log(
            V / V0) ** 2 + 6 * Bp0 + 16 * np.log(
            V / V0) - 1) / V ** 4  # -B0*V0*(3*np.log(V0/V)**2*Bp0+11*np.log(V0/V)*Bp0-6*np.log(V0/V)**2+6*Bp0-16*np.log(V0/V)-1)/V**4

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return -B0 * V0 * (12 * np.log(V / V0) ** 2 * Bp0 - 50 * np.log(V / V0) * Bp0 - 24 * np.log(
            V / V0) ** 2 + 35 * Bp0 + 76 * np.log(
            V / V0) - 20) / V ** 5  # B0*V0*(12*np.log(V0/V)**2*Bp0+50*np.log(V0/V)*Bp0-24*np.log(V0/V)**2+35*Bp0-76*np.log(V0/V)-20)/V**5

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0 = self.pEOS
        return B0 * V0 * (60 * np.log(V / V0) ** 2 * Bp0 - 274 * np.log(V / V0) * Bp0 - 120 * np.log(
            V / V0) ** 2 + 225 * Bp0 + 428 * np.log(
            V / V0) - 176) / V ** 6  # -B0*V0*(60*np.log(V0/V)**2*Bp0+274*np.log(V0/V)*Bp0-120*np.log(V0/V)**2+225*Bp0-428*np.log(V0/V)-176)/V**6

    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return np.asarray(Ecalc) - np.asarray(Edata)  # residuals; least_squares squares them (review finding 3.5)


class BM4:  # 4th-order Birch-Murnaghan (placeholder, not validated)
    """
    Fourth order Birch-Murnaghan EOS and derivatives.
    """

    def __init__(self, *args, units='J/mol', parameters=''):
        warnings.warn("BM4 is a placeholder, not validated (debyetools review decision D3). "
                      "Use BM, RV, MG, TB, MU or PT.", UserWarning, stacklevel=2)
        if list(parameters):
            self.pEOS = parameters[:5]
            self.pEOS[2] = -self.pEOS[2]

    def fitEOS(self, Vdata: np.ndarray, Edata: np.ndarray, initial_parameters: np.ndarray = None, fit: bool = True) -> None:
        """
        Parameters fitting.

        :param Vdata: Input volume data.
        :type Vdata: np.ndarray
        :param Edata: Target energy data.
        :type Edata: np.ndarray
        :param initial_parameters: Initial guess.
        :type initial_parameters: np.ndarray
        :param fit: True to run the fitting. False to just use the input parameters.
        :type fit: bool.

        :return: Optimal parameters.
        :rtype: np.ndarray
        """
        if fit:
            pEOS = initial_parameters[:5]
            # pEOS[2] = -pEOS[2]

            popt = least_squares(self.error2min, pEOS, args=(Vdata, Edata))['x']
            # popt[2] = -popt[2]
            self.pEOS = popt
        if not fit:
            self.pEOS = initial_parameters[:5]
            # self.pEOS[2] = -self.pEOS[2]

        mV = minimize(self.E0, [np.mean(Vdata)], bounds=[(min(Vdata), max(Vdata))], tol=1e-10)
        self.V0 = mV['x'][0]
        ### pr0nt(initial_parameters, self.pEOS)
        return self.pEOS

    def E04min(self, V: float, pEOS: np.ndarray) -> float:
        """
        Energy for minimization.

        :param V: Volume.
        :type V: float
        :param pEOS: parameters.
        :type pEOS: np.ndarray
        :return: E0.
        :rtype: float
        """
        E0, V0, B0, Bp0, Bpp0 = pEOS
        if B0<0:
            return 1
        B0 = - B0
        return E0 - 861 * V0 * B0 * (1 / 128) + 261 * V0 * B0 * Bp0 * (1 / 128) - 27 * V0 * B0 ** 2 * Bpp0 * (
                    1 / 128) - 27 * V0 * B0 * Bp0 ** 2 * (1 / 128) - 1791 * V * B0 * (V0 / V) ** (7 / 3) * (
                           1 / 64) - 207 * B0 * V0 ** 3 * Bp0 / (32 * V ** 2) + 675 * V * B0 * (V0 / V) ** (
                           7 / 3) * Bp0 * (1 / 64) + 501 * B0 * V0 ** 3 / (32 * V ** 2) - 27 * V * (V0 / V) ** (
                           11 / 3) * B0 ** 2 * Bpp0 * (1 / 128) + 27 * V0 ** 3 * B0 ** 2 * Bpp0 / (
                           32 * V ** 2) - 81 * V * (V0 / V) ** (7 / 3) * B0 ** 2 * Bpp0 * (1 / 64) - 27 * V * B0 * (
                           V0 / V) ** (11 / 3) * Bp0 ** 2 * (1 / 128) + 27 * B0 * V0 ** 3 * Bp0 ** 2 / (
                           32 * V ** 2) - 81 * V * B0 * (V0 / V) ** (7 / 3) * Bp0 ** 2 * (1 / 64) + 189 * V * B0 * (
                           V0 / V) ** (11 / 3) * Bp0 * (1 / 128) - 429 * V * B0 * (V0 / V) ** (11 / 3) * (
                           1 / 128) + 717 * V * B0 * (V0 / V) ** (5 / 3) * (1 / 32) - 243 * V * B0 * (V0 / V) ** (
                           5 / 3) * Bp0 * (1 / 32) + 27 * V * (V0 / V) ** (5 / 3) * B0 ** 2 * Bpp0 * (
                           1 / 32) + 27 * V * B0 * (V0 / V) ** (5 / 3) * Bp0 ** 2 * (1 / 32)

    def E0(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: E0(V)
        :rtype: float|np.ndarray
        """
        return self.E04min(V, self.pEOS)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        B0 = - B0
        return -81 * (V0 / V) ** (7 / 3) * B0 ** 2 * Bpp0 * (1 / 64) - 27 * B0 * (V0 / V) ** (11 / 3) * Bp0 ** 2 * (
                    1 / 128) - 81 * B0 * (V0 / V) ** (7 / 3) * Bp0 ** 2 * (1 / 64) - 27 * (V0 / V) ** (
                           11 / 3) * B0 ** 2 * Bpp0 * (1 / 128) + 675 * B0 * (V0 / V) ** (7 / 3) * Bp0 * (
                           1 / 64) - 45 * (V0 / V) ** (2 / 3) * B0 ** 2 * Bpp0 * V0 / (32 * V) - 45 * B0 * (V0 / V) ** (
                           2 / 3) * Bp0 ** 2 * V0 / (32 * V) + 189 * B0 * (V0 / V) ** (4 / 3) * Bp0 ** 2 * V0 / (
                           64 * V) - 693 * B0 * (V0 / V) ** (8 / 3) * Bp0 * V0 / (128 * V) + 405 * B0 * (V0 / V) ** (
                           2 / 3) * Bp0 * V0 / (32 * V) + 99 * (V0 / V) ** (8 / 3) * B0 ** 2 * Bpp0 * V0 / (
                           128 * V) + 189 * (V0 / V) ** (4 / 3) * B0 ** 2 * Bpp0 * V0 / (64 * V) + 99 * B0 * (
                           V0 / V) ** (8 / 3) * Bp0 ** 2 * V0 / (128 * V) - 1575 * B0 * (V0 / V) ** (
                           4 / 3) * Bp0 * V0 / (64 * V) - 501 * B0 * V0 ** 3 / (16 * V ** 3) + 1573 * B0 * (V0 / V) ** (
                           8 / 3) * V0 / (128 * V) - 1195 * B0 * (V0 / V) ** (2 / 3) * V0 / (
                           32 * V) - 27 * V0 ** 3 * B0 ** 2 * Bpp0 / (16 * V ** 3) - 27 * B0 * V0 ** 3 * Bp0 ** 2 / (
                           16 * V ** 3) + 4179 * B0 * (V0 / V) ** (4 / 3) * V0 / (64 * V) + 207 * B0 * V0 ** 3 * Bp0 / (
                           16 * V ** 3) + 717 * B0 * (V0 / V) ** (5 / 3) * (1 / 32) - 429 * B0 * (V0 / V) ** (
                           11 / 3) * (1 / 128) - 1791 * B0 * (V0 / V) ** (7 / 3) * (1 / 64) + 27 * B0 * (V0 / V) ** (
                           5 / 3) * Bp0 ** 2 * (1 / 32) + 27 * (V0 / V) ** (5 / 3) * B0 ** 2 * Bpp0 * (
                           1 / 32) - 243 * B0 * (V0 / V) ** (5 / 3) * Bp0 * (1 / 32) + 189 * B0 * (V0 / V) ** (
                           11 / 3) * Bp0 * (1 / 128)

    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        B0 = - B0
        return -1393 * B0 * (V0 / V) ** (1 / 3) * V0 ** 2 / (16 * V ** 3) - 621 * B0 * V0 ** 3 * Bp0 / (
                    16 * V ** 4) + 81 * V0 ** 3 * B0 ** 2 * Bpp0 / (16 * V ** 4) + 81 * B0 * V0 ** 3 * Bp0 ** 2 / (
                           16 * V ** 4) - 1573 * B0 * (V0 / V) ** (5 / 3) * V0 ** 2 / (
                           48 * V ** 3) + 1195 * B0 * V0 ** 2 / (
                           48 * V ** 3 * (V0 / V) ** (1 / 3)) + 1503 * B0 * V0 ** 3 / (
                           16 * V ** 4) - 135 * B0 * Bp0 * V0 ** 2 / (
                           16 * V ** 3 * (V0 / V) ** (1 / 3)) + 15 * B0 ** 2 * Bpp0 * V0 ** 2 / (
                           16 * V ** 3 * (V0 / V) ** (1 / 3)) + 15 * B0 * Bp0 ** 2 * V0 ** 2 / (
                           16 * V ** 3 * (V0 / V) ** (1 / 3)) + 525 * B0 * (V0 / V) ** (1 / 3) * Bp0 * V0 ** 2 / (
                           16 * V ** 3) - 33 * (V0 / V) ** (5 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (16 * V ** 3) - 63 * (
                           V0 / V) ** (1 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (16 * V ** 3) - 33 * B0 * (V0 / V) ** (
                           5 / 3) * Bp0 ** 2 * V0 ** 2 / (16 * V ** 3) - 63 * B0 * (V0 / V) ** (
                           1 / 3) * Bp0 ** 2 * V0 ** 2 / (16 * V ** 3) + 231 * B0 * (V0 / V) ** (
                           5 / 3) * Bp0 * V0 ** 2 / (16 * V ** 3)

    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        B0 = - B0
        return 55 * (V0 / V) ** (2 / 3) * B0 ** 2 * Bpp0 * V0 ** 3 / (16 * V ** 5) + 55 * B0 * (V0 / V) ** (
                    2 / 3) * Bp0 ** 2 * V0 ** 3 / (16 * V ** 5) - 385 * B0 * (V0 / V) ** (2 / 3) * Bp0 * V0 ** 3 / (
                           16 * V ** 5) + 189 * (V0 / V) ** (1 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (
                           16 * V ** 4) + 99 * B0 * (V0 / V) ** (5 / 3) * Bp0 ** 2 * V0 ** 2 / (
                           16 * V ** 4) + 189 * B0 * (V0 / V) ** (1 / 3) * Bp0 ** 2 * V0 ** 2 / (
                           16 * V ** 4) + 405 * B0 * Bp0 * V0 ** 2 / (
                           16 * V ** 4 * (V0 / V) ** (1 / 3)) - 45 * B0 ** 2 * Bpp0 * V0 ** 2 / (
                           16 * V ** 4 * (V0 / V) ** (1 / 3)) - 45 * B0 * Bp0 ** 2 * V0 ** 2 / (
                           16 * V ** 4 * (V0 / V) ** (1 / 3)) + 1195 * B0 * V0 ** 3 / (
                           144 * V ** 5 * (V0 / V) ** (4 / 3)) - 1195 * B0 * V0 ** 2 / (
                           16 * V ** 4 * (V0 / V) ** (1 / 3)) - 1503 * B0 * V0 ** 3 / (
                       4 * V ** 5) + 1393 * B0 * V0 ** 3 / (48 * V ** 5 * (V0 / V) ** (2 / 3)) - 693 * B0 * (
                           V0 / V) ** (5 / 3) * Bp0 * V0 ** 2 / (16 * V ** 4) - 1575 * B0 * (V0 / V) ** (
                           1 / 3) * Bp0 * V0 ** 2 / (16 * V ** 4) + 621 * B0 * V0 ** 3 * Bp0 / (
                           4 * V ** 5) - 81 * V0 ** 3 * B0 ** 2 * Bpp0 / (4 * V ** 5) - 81 * B0 * V0 ** 3 * Bp0 ** 2 / (
                       4 * V ** 5) + 7865 * B0 * (V0 / V) ** (2 / 3) * V0 ** 3 / (
                       144 * V ** 5) - 45 * B0 * Bp0 * V0 ** 3 / (
                           16 * V ** 5 * (V0 / V) ** (4 / 3)) + 5 * B0 ** 2 * Bpp0 * V0 ** 3 / (
                           16 * V ** 5 * (V0 / V) ** (4 / 3)) + 5 * B0 * Bp0 ** 2 * V0 ** 3 / (
                           16 * V ** 5 * (V0 / V) ** (4 / 3)) - 175 * B0 * Bp0 * V0 ** 3 / (
                           16 * V ** 5 * (V0 / V) ** (2 / 3)) + 21 * B0 ** 2 * Bpp0 * V0 ** 3 / (
                           16 * V ** 5 * (V0 / V) ** (2 / 3)) + 21 * B0 * Bp0 ** 2 * V0 ** 3 / (
                           16 * V ** 5 * (V0 / V) ** (2 / 3)) + 4179 * B0 * (V0 / V) ** (1 / 3) * V0 ** 2 / (
                           16 * V ** 4) + 1573 * B0 * (V0 / V) ** (5 / 3) * V0 ** 2 / (16 * V ** 4) + 99 * (V0 / V) ** (
                           5 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (16 * V ** 4)

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        B0 = - B0
        return -15 * B0 * Bp0 * V0 ** 4 / (4 * V ** 7 * (V0 / V) ** (7 / 3)) + 5 * B0 ** 2 * Bpp0 * V0 ** 4 / (
                    12 * V ** 7 * (V0 / V) ** (7 / 3)) - 7865 * B0 * (V0 / V) ** (2 / 3) * V0 ** 3 / (
                           18 * V ** 6) - 4179 * B0 * (V0 / V) ** (1 / 3) * V0 ** 2 / (4 * V ** 5) - 1573 * B0 * (
                           V0 / V) ** (5 / 3) * V0 ** 2 / (4 * V ** 5) + 385 * B0 * Bp0 * V0 ** 4 / (
                           24 * V ** 7 * (V0 / V) ** (1 / 3)) - 55 * B0 * Bp0 ** 2 * V0 ** 4 / (
                           24 * V ** 7 * (V0 / V) ** (1 / 3)) + 7 * B0 * Bp0 ** 2 * V0 ** 4 / (
                           8 * V ** 7 * (V0 / V) ** (5 / 3)) - 55 * B0 ** 2 * Bpp0 * V0 ** 4 / (
                           24 * V ** 7 * (V0 / V) ** (1 / 3)) + 7 * B0 ** 2 * Bpp0 * V0 ** 4 / (
                           8 * V ** 7 * (V0 / V) ** (5 / 3)) + 5 * B0 * Bp0 ** 2 * V0 ** 4 / (
                           12 * V ** 7 * (V0 / V) ** (7 / 3)) - 175 * B0 * Bp0 * V0 ** 4 / (
                           24 * V ** 7 * (V0 / V) ** (5 / 3)) + 45 * B0 * Bp0 * V0 ** 3 / (
                           2 * V ** 6 * (V0 / V) ** (4 / 3)) - 5 * B0 ** 2 * Bpp0 * V0 ** 3 / (
                           2 * V ** 6 * (V0 / V) ** (4 / 3)) - 5 * B0 * Bp0 ** 2 * V0 ** 3 / (
                           2 * V ** 6 * (V0 / V) ** (4 / 3)) + 1393 * B0 * V0 ** 4 / (
                           72 * V ** 7 * (V0 / V) ** (5 / 3)) - 7865 * B0 * V0 ** 4 / (
                           216 * V ** 7 * (V0 / V) ** (1 / 3)) + 1195 * B0 * V0 ** 4 / (
                           108 * V ** 7 * (V0 / V) ** (7 / 3)) + 7515 * B0 * V0 ** 3 / (
                           4 * V ** 6) - 3105 * B0 * V0 ** 3 * Bp0 / (4 * V ** 6) + 405 * V0 ** 3 * B0 ** 2 * Bpp0 / (
                           4 * V ** 6) + 405 * B0 * V0 ** 3 * Bp0 ** 2 / (
                           4 * V ** 6) - 21 * B0 ** 2 * Bpp0 * V0 ** 3 / (
                           2 * V ** 6 * (V0 / V) ** (2 / 3)) - 21 * B0 * Bp0 ** 2 * V0 ** 3 / (
                           2 * V ** 6 * (V0 / V) ** (2 / 3)) + 175 * B0 * Bp0 * V0 ** 3 / (
                           2 * V ** 6 * (V0 / V) ** (2 / 3)) - 405 * B0 * Bp0 * V0 ** 2 / (
                           4 * V ** 5 * (V0 / V) ** (1 / 3)) + 45 * B0 ** 2 * Bpp0 * V0 ** 2 / (
                           4 * V ** 5 * (V0 / V) ** (1 / 3)) + 45 * B0 * Bp0 ** 2 * V0 ** 2 / (
                           4 * V ** 5 * (V0 / V) ** (1 / 3)) + 693 * B0 * (V0 / V) ** (5 / 3) * Bp0 * V0 ** 2 / (
                           4 * V ** 5) - 99 * B0 * (V0 / V) ** (5 / 3) * Bp0 ** 2 * V0 ** 2 / (
                           4 * V ** 5) - 189 * B0 * (V0 / V) ** (1 / 3) * Bp0 ** 2 * V0 ** 2 / (
                           4 * V ** 5) + 385 * B0 * (V0 / V) ** (2 / 3) * Bp0 * V0 ** 3 / (2 * V ** 6) - 189 * (
                           V0 / V) ** (1 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (4 * V ** 5) - 55 * B0 * (V0 / V) ** (
                           2 / 3) * Bp0 ** 2 * V0 ** 3 / (2 * V ** 6) - 99 * (V0 / V) ** (
                           5 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (4 * V ** 5) - 55 * (V0 / V) ** (
                           2 / 3) * B0 ** 2 * Bpp0 * V0 ** 3 / (2 * V ** 6) + 1575 * B0 * (V0 / V) ** (
                           1 / 3) * Bp0 * V0 ** 2 / (4 * V ** 5) + 1195 * B0 * V0 ** 2 / (
                           4 * V ** 5 * (V0 / V) ** (1 / 3)) - 1393 * B0 * V0 ** 3 / (
                           6 * V ** 6 * (V0 / V) ** (2 / 3)) - 1195 * B0 * V0 ** 3 / (18 * V ** 6 * (V0 / V) ** (4 / 3))

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        B0 = - B0
        return -675 * B0 * Bp0 * V0 ** 3 / (4 * V ** 7 * (V0 / V) ** (4 / 3)) + 75 * B0 ** 2 * Bpp0 * V0 ** 3 / (
                    4 * V ** 7 * (V0 / V) ** (4 / 3)) + 75 * B0 * Bp0 ** 2 * V0 ** 3 / (
                           4 * V ** 7 * (V0 / V) ** (4 / 3)) + 8365 * B0 * V0 ** 5 / (
                           324 * V ** 9 * (V0 / V) ** (10 / 3)) - 22545 * B0 * V0 ** 3 / (
                           2 * V ** 7) + 6965 * B0 * V0 ** 5 / (
                           216 * V ** 9 * (V0 / V) ** (8 / 3)) - 7865 * B0 * V0 ** 5 / (
                           648 * V ** 9 * (V0 / V) ** (4 / 3)) + 825 * (V0 / V) ** (
                           2 / 3) * B0 ** 2 * Bpp0 * V0 ** 3 / (4 * V ** 7) - 105 * B0 * Bp0 ** 2 * V0 ** 4 / (
                           8 * V ** 8 * (V0 / V) ** (5 / 3)) + 35 * B0 * Bp0 ** 2 * V0 ** 5 / (
                       24 * V ** 9 * (V0 / V) ** (8 / 3)) - 55 * B0 * Bp0 ** 2 * V0 ** 5 / (
                       72 * V ** 9 * (V0 / V) ** (4 / 3)) + 35 * B0 ** 2 * Bpp0 * V0 ** 5 / (
                           24 * V ** 9 * (V0 / V) ** (8 / 3)) - 875 * B0 * Bp0 * V0 ** 5 / (
                           72 * V ** 9 * (V0 / V) ** (8 / 3)) - 55 * B0 ** 2 * Bpp0 * V0 ** 5 / (
                           72 * V ** 9 * (V0 / V) ** (4 / 3)) + 275 * B0 ** 2 * Bpp0 * V0 ** 4 / (
                           8 * V ** 8 * (V0 / V) ** (1 / 3)) + 875 * B0 * Bp0 * V0 ** 4 / (
                           8 * V ** 8 * (V0 / V) ** (5 / 3)) - 2625 * B0 * Bp0 * V0 ** 3 / (
                           4 * V ** 7 * (V0 / V) ** (2 / 3)) + 35 * B0 * Bp0 ** 2 * V0 ** 5 / (
                           36 * V ** 9 * (V0 / V) ** (10 / 3)) - 25 * B0 ** 2 * Bpp0 * V0 ** 4 / (
                           4 * V ** 8 * (V0 / V) ** (7 / 3)) - 25 * B0 * Bp0 ** 2 * V0 ** 4 / (
                           4 * V ** 8 * (V0 / V) ** (7 / 3)) - 105 * B0 ** 2 * Bpp0 * V0 ** 4 / (
                           8 * V ** 8 * (V0 / V) ** (5 / 3)) + 275 * B0 * Bp0 ** 2 * V0 ** 4 / (
                           8 * V ** 8 * (V0 / V) ** (1 / 3)) + 315 * B0 * Bp0 ** 2 * V0 ** 3 / (
                           4 * V ** 7 * (V0 / V) ** (2 / 3)) + 9315 * B0 * V0 ** 3 * Bp0 / (
                           2 * V ** 7) - 1215 * V0 ** 3 * B0 ** 2 * Bpp0 / (
                           2 * V ** 7) - 1215 * B0 * V0 ** 3 * Bp0 ** 2 / (2 * V ** 7) + 39325 * B0 * (V0 / V) ** (
                           2 / 3) * V0 ** 3 / (12 * V ** 7) + 2025 * B0 * Bp0 * V0 ** 2 / (
                           4 * V ** 6 * (V0 / V) ** (1 / 3)) - 225 * B0 ** 2 * Bpp0 * V0 ** 2 / (
                           4 * V ** 6 * (V0 / V) ** (1 / 3)) - 225 * B0 * Bp0 ** 2 * V0 ** 2 / (
                       4 * V ** 6 * (V0 / V) ** (1 / 3)) + 315 * B0 ** 2 * Bpp0 * V0 ** 3 / (
                           4 * V ** 7 * (V0 / V) ** (2 / 3)) + 385 * B0 * Bp0 * V0 ** 5 / (
                           72 * V ** 9 * (V0 / V) ** (4 / 3)) + 20895 * B0 * (V0 / V) ** (1 / 3) * V0 ** 2 / (
                           4 * V ** 6) + 7865 * B0 * (V0 / V) ** (5 / 3) * V0 ** 2 / (
                           4 * V ** 6) + 225 * B0 * Bp0 * V0 ** 4 / (
                           4 * V ** 8 * (V0 / V) ** (7 / 3)) + 35 * B0 ** 2 * Bpp0 * V0 ** 5 / (
                           36 * V ** 9 * (V0 / V) ** (10 / 3)) - 1925 * B0 * Bp0 * V0 ** 4 / (
                       8 * V ** 8 * (V0 / V) ** (1 / 3)) + 825 * B0 * (V0 / V) ** (2 / 3) * Bp0 ** 2 * V0 ** 3 / (
                           4 * V ** 7) - 7875 * B0 * (V0 / V) ** (1 / 3) * Bp0 * V0 ** 2 / (4 * V ** 6) + 495 * (
                           V0 / V) ** (5 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (4 * V ** 6) - 35 * B0 * Bp0 * V0 ** 5 / (
                           4 * V ** 9 * (V0 / V) ** (10 / 3)) + 945 * B0 * (V0 / V) ** (1 / 3) * Bp0 ** 2 * V0 ** 2 / (
                           4 * V ** 6) - 3465 * B0 * (V0 / V) ** (5 / 3) * Bp0 * V0 ** 2 / (4 * V ** 6) - 5775 * B0 * (
                           V0 / V) ** (2 / 3) * Bp0 * V0 ** 3 / (4 * V ** 7) + 945 * (V0 / V) ** (
                           1 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (4 * V ** 6) + 495 * B0 * (V0 / V) ** (
                           5 / 3) * Bp0 ** 2 * V0 ** 2 / (4 * V ** 6) - 5975 * B0 * V0 ** 4 / (
                           36 * V ** 8 * (V0 / V) ** (7 / 3)) + 39325 * B0 * V0 ** 4 / (
                           72 * V ** 8 * (V0 / V) ** (1 / 3)) - 6965 * B0 * V0 ** 4 / (
                       24 * V ** 8 * (V0 / V) ** (5 / 3)) - 5975 * B0 * V0 ** 2 / (
                           4 * V ** 6 * (V0 / V) ** (1 / 3)) + 5975 * B0 * V0 ** 3 / (
                           12 * V ** 7 * (V0 / V) ** (4 / 3)) + 6965 * B0 * V0 ** 3 / (4 * V ** 7 * (V0 / V) ** (2 / 3))

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        B0 = - B0
        return -2835 * B0 * (V0 / V) ** (1 / 3) * Bp0 ** 2 * V0 ** 2 / (2 * V ** 7) + 10395 * B0 * (V0 / V) ** (
                    5 / 3) * Bp0 * V0 ** 2 / (2 * V ** 7) + 175 * B0 * Bp0 ** 2 * V0 ** 6 / (
                           54 * V ** 11 * (V0 / V) ** (13 / 3)) - 875 * B0 * Bp0 * V0 ** 6 / (
                           27 * V ** 11 * (V0 / V) ** (11 / 3)) - 55 * B0 ** 2 * Bpp0 * V0 ** 6 / (
                           54 * V ** 11 * (V0 / V) ** (7 / 3)) + 35 * B0 ** 2 * Bpp0 * V0 ** 6 / (
                           9 * V ** 11 * (V0 / V) ** (11 / 3)) - 55 * B0 * Bp0 ** 2 * V0 ** 6 / (
                           54 * V ** 11 * (V0 / V) ** (7 / 3)) + 35 * B0 * Bp0 ** 2 * V0 ** 6 / (
                           9 * V ** 11 * (V0 / V) ** (11 / 3)) - 78650 * B0 * (V0 / V) ** (2 / 3) * V0 ** 3 / (
                           3 * V ** 8) + 315 * B0 ** 2 * Bpp0 * V0 ** 4 / (
                           2 * V ** 9 * (V0 / V) ** (5 / 3)) - 825 * B0 * Bp0 ** 2 * V0 ** 4 / (
                           2 * V ** 9 * (V0 / V) ** (1 / 3)) + 75 * B0 * Bp0 ** 2 * V0 ** 4 / (
                           V ** 9 * (V0 / V) ** (7 / 3)) - 35 * B0 ** 2 * Bpp0 * V0 ** 5 / (
                           V ** 10 * (V0 / V) ** (8 / 3)) - 35 * B0 * Bp0 ** 2 * V0 ** 5 / (
                           V ** 10 * (V0 / V) ** (8 / 3)) - 1485 * B0 * (V0 / V) ** (5 / 3) * Bp0 ** 2 * V0 ** 2 / (
                           2 * V ** 7) - 2835 * (V0 / V) ** (1 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (
                           2 * V ** 7) + 8505 * B0 * V0 ** 3 * Bp0 ** 2 / (2 * V ** 8) - 13930 * B0 * V0 ** 3 / (
                           V ** 8 * (V0 / V) ** (2 / 3)) + 1350 * B0 * Bp0 * V0 ** 3 / (
                           V ** 8 * (V0 / V) ** (4 / 3)) - 150 * B0 ** 2 * Bpp0 * V0 ** 3 / (
                           V ** 8 * (V0 / V) ** (4 / 3)) - 150 * B0 * Bp0 ** 2 * V0 ** 3 / (
                           V ** 8 * (V0 / V) ** (4 / 3)) + 5250 * B0 * Bp0 * V0 ** 3 / (
                           V ** 8 * (V0 / V) ** (2 / 3)) - 1650 * (V0 / V) ** (
                           2 / 3) * B0 ** 2 * Bpp0 * V0 ** 3 / V ** 8 - 630 * B0 ** 2 * Bpp0 * V0 ** 3 / (
                           V ** 8 * (V0 / V) ** (2 / 3)) - 1650 * B0 * (V0 / V) ** (
                           2 / 3) * Bp0 ** 2 * V0 ** 3 / V ** 8 + 210 * B0 * Bp0 * V0 ** 5 / (
                           V ** 10 * (V0 / V) ** (10 / 3)) - 675 * B0 * Bp0 * V0 ** 4 / (
                           V ** 9 * (V0 / V) ** (7 / 3)) + 75 * B0 ** 2 * Bpp0 * V0 ** 4 / (
                           V ** 9 * (V0 / V) ** (7 / 3)) - 630 * B0 * Bp0 ** 2 * V0 ** 3 / (
                           V ** 8 * (V0 / V) ** (2 / 3)) + 11550 * B0 * (V0 / V) ** (
                           2 / 3) * Bp0 * V0 ** 3 / V ** 8 - 16730 * B0 * V0 ** 5 / (
                           27 * V ** 10 * (V0 / V) ** (10 / 3)) - 6965 * B0 * V0 ** 5 / (
                           9 * V ** 10 * (V0 / V) ** (8 / 3)) + 315 * B0 * Bp0 ** 2 * V0 ** 4 / (
                           2 * V ** 9 * (V0 / V) ** (5 / 3)) + 5775 * B0 * Bp0 * V0 ** 4 / (
                           2 * V ** 9 * (V0 / V) ** (1 / 3)) - 62685 * B0 * (V0 / V) ** (1 / 3) * V0 ** 2 / (
                           2 * V ** 7) - 23595 * B0 * (V0 / V) ** (5 / 3) * V0 ** 2 / (
                           2 * V ** 7) + 385 * B0 * Bp0 * V0 ** 6 / (
                           54 * V ** 11 * (V0 / V) ** (7 / 3)) - 385 * B0 * Bp0 * V0 ** 5 / (
                           3 * V ** 10 * (V0 / V) ** (4 / 3)) - 70 * B0 ** 2 * Bpp0 * V0 ** 5 / (
                           3 * V ** 10 * (V0 / V) ** (10 / 3)) - 6075 * B0 * Bp0 * V0 ** 2 / (
                           2 * V ** 7 * (V0 / V) ** (1 / 3)) - 1485 * (V0 / V) ** (5 / 3) * B0 ** 2 * Bpp0 * V0 ** 2 / (
                           2 * V ** 7) + 157815 * B0 * V0 ** 3 / (2 * V ** 8) + 7865 * B0 * V0 ** 5 / (
                           27 * V ** 10 * (V0 / V) ** (4 / 3)) + 23625 * B0 * (V0 / V) ** (1 / 3) * Bp0 * V0 ** 2 / (
                           2 * V ** 7) - 2625 * B0 * Bp0 * V0 ** 4 / (
                           2 * V ** 9 * (V0 / V) ** (5 / 3)) - 825 * B0 ** 2 * Bpp0 * V0 ** 4 / (
                           2 * V ** 9 * (V0 / V) ** (1 / 3)) - 175 * B0 * Bp0 * V0 ** 6 / (
                           6 * V ** 11 * (V0 / V) ** (13 / 3)) + 175 * B0 ** 2 * Bpp0 * V0 ** 6 / (
                           54 * V ** 11 * (V0 / V) ** (13 / 3)) - 70 * B0 * Bp0 ** 2 * V0 ** 5 / (
                           3 * V ** 10 * (V0 / V) ** (10 / 3)) + 875 * B0 * Bp0 * V0 ** 5 / (
                           3 * V ** 10 * (V0 / V) ** (8 / 3)) + 55 * B0 ** 2 * Bpp0 * V0 ** 5 / (
                           3 * V ** 10 * (V0 / V) ** (4 / 3)) + 55 * B0 * Bp0 ** 2 * V0 ** 5 / (
                           3 * V ** 10 * (V0 / V) ** (4 / 3)) + 6965 * B0 * V0 ** 6 / (
                           81 * V ** 11 * (V0 / V) ** (11 / 3)) + 8505 * V0 ** 3 * B0 ** 2 * Bpp0 / (
                           2 * V ** 8) - 65205 * B0 * V0 ** 3 * Bp0 / (2 * V ** 8) + 17925 * B0 * V0 ** 2 / (
                           2 * V ** 7 * (V0 / V) ** (1 / 3)) - 11950 * B0 * V0 ** 3 / (
                           3 * V ** 8 * (V0 / V) ** (4 / 3)) + 675 * B0 ** 2 * Bpp0 * V0 ** 2 / (
                           2 * V ** 7 * (V0 / V) ** (1 / 3)) + 675 * B0 * Bp0 ** 2 * V0 ** 2 / (
                           2 * V ** 7 * (V0 / V) ** (1 / 3)) - 39325 * B0 * V0 ** 4 / (
                           6 * V ** 9 * (V0 / V) ** (1 / 3)) + 6965 * B0 * V0 ** 4 / (
                           2 * V ** 9 * (V0 / V) ** (5 / 3)) - 7865 * B0 * V0 ** 6 / (
                           486 * V ** 11 * (V0 / V) ** (7 / 3)) + 5975 * B0 * V0 ** 4 / (
                           3 * V ** 9 * (V0 / V) ** (7 / 3)) + 41825 * B0 * V0 ** 6 / (
                           486 * V ** 11 * (V0 / V) ** (13 / 3))

    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return (Ecalc - Edata)**2


class MU2:  # 2nd-order Murnaghan (placeholder, not validated)
    """
    Second order Murnaghan EOS and derivatives.
    """

    def __init__(self, *args, units='J/mol', parameters=''):
        warnings.warn("MU2 is a placeholder, not validated (debyetools review decision D2). "
                      "Use BM, RV, MG, TB, MU or PT.", UserWarning, stacklevel=2)
        if list(parameters):
            self.pEOS = parameters[:5]
            # self.pEOS[2] = - self.pEOS[2]

    def fitEOS(self, Vdata: np.ndarray, Edata: np.ndarray, initial_parameters: np.ndarray = None, fit: bool = True) -> None:
        """
        Parameters fitting.

        :param Vdata: Input volume data.
        :type Vdata: np.ndarray
        :param Edata: Target energy data.
        :type Edata: np.ndarray
        :param initial_parameters: Initial guess.
        :type initial_parameters: np.ndarray
        :param fit: True to run the fitting. False to just use the input parameters.
        :type fit: bool.

        :return: Optimal parameters.
        :rtype: np.ndarray
        """
        if fit:
            pEOS = initial_parameters[:5]
            # pEOS[2] = - pEOS[2]
            popt = least_squares(self.error2min, pEOS, args=(Vdata, Edata))['x']
            self.pEOS = popt
        if not fit:
            self.pEOS = initial_parameters[:5]
            self.pEOS[2] = - self.pEOS[2]

        mV = minimize(self.E0, [np.mean(Vdata)], bounds=[(min(Vdata), max(Vdata))], tol=1e-10)
        self.V0 = mV['x'][0]

        return self.pEOS

    def E04min(self, V: float, pEOS: np.ndarray) -> float:
        """
        Energy for minimization.

        :param V: Volume.
        :type V: float
        :param pEOS: parameters.
        :type pEOS: np.ndarray
        :return: E0.
        :rtype: float
        """
        E0, V0, B0, Bp0, Bpp0 = pEOS
        if B0<0:
            return 1
        B0 = - B0
        return E0 - 861 * V0 * B0 * (1 / 128) + 261 * V0 * B0 * Bp0 * (1 / 128) - 27 * V0 * B0 ** 2 * Bpp0 * (
                    1 / 128) - 27 * V0 * B0 * Bp0 ** 2 * (1 / 128) - 1791 * V * B0 * (V0 / V) ** (7 / 3) * (
                           1 / 64) - 207 * B0 * V0 ** 3 * Bp0 / (32 * V ** 2) + 675 * V * B0 * (V0 / V) ** (
                           7 / 3) * Bp0 * (1 / 64) + 501 * B0 * V0 ** 3 / (32 * V ** 2) - 27 * V * (V0 / V) ** (
                           11 / 3) * B0 ** 2 * Bpp0 * (1 / 128) + 27 * V0 ** 3 * B0 ** 2 * Bpp0 / (
                           32 * V ** 2) - 81 * V * (V0 / V) ** (7 / 3) * B0 ** 2 * Bpp0 * (1 / 64) - 27 * V * B0 * (
                           V0 / V) ** (11 / 3) * Bp0 ** 2 * (1 / 128) + 27 * B0 * V0 ** 3 * Bp0 ** 2 / (
                           32 * V ** 2) - 81 * V * B0 * (V0 / V) ** (7 / 3) * Bp0 ** 2 * (1 / 64) + 189 * V * B0 * (
                           V0 / V) ** (11 / 3) * Bp0 * (1 / 128) - 429 * V * B0 * (V0 / V) ** (11 / 3) * (
                           1 / 128) + 717 * V * B0 * (V0 / V) ** (5 / 3) * (1 / 32) - 243 * V * B0 * (V0 / V) ** (
                           5 / 3) * Bp0 * (1 / 32) + 27 * V * (V0 / V) ** (5 / 3) * B0 ** 2 * Bpp0 * (
                           1 / 32) + 27 * V * B0 * (V0 / V) ** (5 / 3) * Bp0 ** 2 * (1 / 32)

    def E0(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: E0(V)
        :rtype: float|np.ndarray
        """
        return self.E04min(V, self.pEOS)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        K, Kp, Kpp = B0, Bp0, Bpp0
        return (1) * (-2 * K / (Kp * (
                    np.sqrt(-2 * K * Kpp + Kp ** 2) * ((V0 / V) ** np.sqrt(-2 * K * Kpp + Kp ** 2) + 1) / (
                        Kp * ((V0 / V) ** np.sqrt(-2 * K * Kpp + Kp ** 2) - 1)) - 1)))

    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        K, Kp, Kpp = B0, Bp0, Bpp0
        return (1) * (-8 * K * (V0 / V) ** np.sqrt(-2 * K * Kpp + Kp ** 2) * (Kpp * K - (1 / 2) * Kp ** 2) / (((
                                                                                                                           Kp - np.sqrt(
                                                                                                                       -2 * K * Kpp + Kp ** 2)) * (
                                                                                                                           V0 / V) ** np.sqrt(
            -2 * K * Kpp + Kp ** 2) - Kp - np.sqrt(-2 * K * Kpp + Kp ** 2)) ** 2 * V))

    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        K, Kp, Kpp = B0, Bp0, Bpp0
        return (1) * ((16 * (((-(1 / 2) * Kp - 1 / 2) * np.sqrt(-2 * K * Kpp + Kp ** 2) - Kpp * K + (
                    1 / 2) * Kp ** 2 + (1 / 2) * Kp) * (V0 / V) ** (2 * np.sqrt(-2 * K * Kpp + Kp ** 2)) + (
                                         V0 / V) ** np.sqrt(-2 * K * Kpp + Kp ** 2) * (
                                         (-(1 / 2) * Kp - 1 / 2) * np.sqrt(-2 * K * Kpp + Kp ** 2) + Kpp * K - (
                                             1 / 2) * Kp ** 2 - (1 / 2) * Kp))) * K * (Kpp * K - (1 / 2) * Kp ** 2) / ((
                                                                                                                                   (
                                                                                                                                               Kp - np.sqrt(
                                                                                                                                           -2 * K * Kpp + Kp ** 2)) * (
                                                                                                                                               V0 / V) ** np.sqrt(
                                                                                                                               -2 * K * Kpp + Kp ** 2) - Kp - np.sqrt(
                                                                                                                               -2 * K * Kpp + Kp ** 2)) ** 3 * V ** 2))

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        K, Kp, Kpp = B0, Bp0, Bpp0
        return (1) * (-32 * K * (((-(1 / 2) * Kp ** 3 - 3 * Kp ** 2 * (1 / 2) + (K * Kpp - 1) * Kp + 3 * Kpp * K * (
                    1 / 2)) * np.sqrt(-2 * K * Kpp + Kp ** 2) + (1 / 2) * Kp ** 4 + 3 * Kp ** 3 * (1 / 2) + (
                                              1 - 3 * Kpp * K * (
                                                  1 / 2)) * Kp ** 2 - 3 * K * Kp * Kpp + K ** 2 * Kpp ** 2 - Kpp * K) * (
                                             V0 / V) ** (3 * np.sqrt(-2 * K * Kpp + Kp ** 2)) - (
                                             4 * (Kpp * K - (1 / 2) * Kp ** 2 + 1 / 2)) * Kpp * K * (V0 / V) ** (
                                             2 * np.sqrt(-2 * K * Kpp + Kp ** 2)) + (V0 / V) ** np.sqrt(
            -2 * K * Kpp + Kp ** 2) * (((1 / 2) * Kp ** 3 + 3 * Kp ** 2 * (1 / 2) + (
                    -K * Kpp + 1) * Kp - 3 * Kpp * K * (1 / 2)) * np.sqrt(-2 * K * Kpp + Kp ** 2) + (
                                                   1 / 2) * Kp ** 4 + 3 * Kp ** 3 * (1 / 2) + (1 - 3 * Kpp * K * (
                    1 / 2)) * Kp ** 2 - 3 * K * Kp * Kpp + K ** 2 * Kpp ** 2 - Kpp * K)) * (
                                  Kpp * K - (1 / 2) * Kp ** 2) / (((Kp - np.sqrt(-2 * K * Kpp + Kp ** 2)) * (
                    V0 / V) ** np.sqrt(-2 * K * Kpp + Kp ** 2) - Kp - np.sqrt(-2 * K * Kpp + Kp ** 2)) ** 4 * V ** 3))

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        K, Kp, Kpp = B0, Bp0, Bpp0
        return (1) * (-(64 * ((11 * (Kpp * K - (1 / 2) * Kp ** 2 + 1 / 2)) * Kpp * (
                    (-(1 / 2) * Kp - 9 / 11) * np.sqrt(-2 * K * Kpp + Kp ** 2) + Kpp * K - (
                        1 / 2) * Kp ** 2 - 9 * Kp * (1 / 11)) * K * (V0 / V) ** (
                                          2 * np.sqrt(-2 * K * Kpp + Kp ** 2)) - (
                                          11 * (Kpp * K - (1 / 2) * Kp ** 2 + 1 / 2)) * Kpp * (
                                          ((1 / 2) * Kp + 9 / 11) * np.sqrt(-2 * K * Kpp + Kp ** 2) + Kpp * K - (
                                              1 / 2) * Kp ** 2 - 9 * Kp * (1 / 11)) * K * (V0 / V) ** (
                                          3 * np.sqrt(-2 * K * Kpp + Kp ** 2)) + ((3 * Kpp ** 2 * (Kp + 2) * K ** 2 * (
                    1 / 2) - (1 / 4) * (7 * (Kp ** 3 + (30 / 7) * Kp ** 2 + (33 / 7) * Kp + 6 / 7)) * Kpp * K + (
                                                                                               1 / 2) * Kp ** 5 + 11 * Kp ** 3 * (
                                                                                               1 / 2) + 3 * Kp ** 4 + 3 * Kp ** 2) * np.sqrt(
            -2 * K * Kpp + Kp ** 2) - K ** 3 * Kpp ** 3 + 3 * Kpp ** 2 * (
                                                                                              Kp ** 2 + 3 * Kp + 11 / 6) * K ** 2 - 9 * Kpp * (
                                                                                              Kp ** 3 + (
                                                                                                  14 / 3) * Kp ** 2 + (
                                                                                                          55 / 9) * Kp + 2) * Kp * K * (
                                                                                              1 / 4) + 11 * Kp ** 4 * (
                                                                                              1 / 2) + 3 * Kp ** 3 + (
                                                                                              1 / 2) * Kp ** 6 + 3 * Kp ** 5) * (
                                          V0 / V) ** np.sqrt(-2 * K * Kpp + Kp ** 2) + (V0 / V) ** (
                                          4 * np.sqrt(-2 * K * Kpp + Kp ** 2)) * ((3 * Kpp ** 2 * (Kp + 2) * K ** 2 * (
                    1 / 2) - (1 / 4) * (7 * (Kp ** 3 + (30 / 7) * Kp ** 2 + (33 / 7) * Kp + 6 / 7)) * Kpp * K + (
                                                                                               1 / 2) * Kp ** 5 + 11 * Kp ** 3 * (
                                                                                               1 / 2) + 3 * Kp ** 4 + 3 * Kp ** 2) * np.sqrt(
            -2 * K * Kpp + Kp ** 2) + K ** 3 * Kpp ** 3 - 3 * Kpp ** 2 * (
                                                                                              Kp ** 2 + 3 * Kp + 11 / 6) * K ** 2 + 9 * Kpp * (
                                                                                              Kp ** 3 + (
                                                                                                  14 / 3) * Kp ** 2 + (
                                                                                                          55 / 9) * Kp + 2) * Kp * K * (
                                                                                              1 / 4) - (
                                                                                              1 / 2) * Kp ** 6 - 11 * Kp ** 4 * (
                                                                                              1 / 2) - 3 * Kp ** 5 - 3 * Kp ** 3))) * K * (
                                  Kpp * K - (1 / 2) * Kp ** 2) / (((Kp - np.sqrt(-2 * K * Kpp + Kp ** 2)) * (
                    V0 / V) ** np.sqrt(-2 * K * Kpp + Kp ** 2) - Kp - np.sqrt(-2 * K * Kpp + Kp ** 2)) ** 5 * V ** 4))

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        E0, V0, B0, Bp0, Bpp0 = self.pEOS
        K, Kp, Kpp = B0, Bp0, Bpp0
        return (1) * (-(128 * (-(26 * (Kpp * K - (1 / 2) * Kp ** 2 + 1 / 2)) * Kpp * K * ((-(Kp + 25 / 13) * Kpp * K + (
                    1 / 2) * Kp ** 3 + 25 * Kp ** 2 * (1 / 13) + 24 * Kp * (1 / 13)) * np.sqrt(
            -2 * K * Kpp + Kp ** 2) + K ** 2 * Kpp ** 2 - (1 / 2) * (3 * (
                    Kp ** 2 + (100 / 39) * Kp + 16 / 13)) * Kpp * K + (1 / 2) * (Kp + 2) * Kp ** 2 * (Kp + 24 / 13)) * (
                                           V0 / V) ** (2 * np.sqrt(-2 * K * Kpp + Kp ** 2)) - (
                                           26 * (Kpp * K - (1 / 2) * Kp ** 2 + 1 / 2)) * Kpp * K * (((
                                                                                                                 Kp + 25 / 13) * Kpp * K - (
                                                                                                                 1 / 2) * Kp ** 3 - 25 * Kp ** 2 * (
                                                                                                                 1 / 13) - 24 * Kp * (
                                                                                                                 1 / 13)) * np.sqrt(
            -2 * K * Kpp + Kp ** 2) + K ** 2 * Kpp ** 2 - (1 / 2) * (3 * (
                    Kp ** 2 + (100 / 39) * Kp + 16 / 13)) * Kpp * K + (1 / 2) * (Kp + 2) * Kp ** 2 * (Kp + 24 / 13)) * (
                                           V0 / V) ** (4 * np.sqrt(-2 * K * Kpp + Kp ** 2)) + (
                                           66 * (Kpp * K - (1 / 2) * Kp ** 2 + 1 / 2)) * (
                                           Kpp * K - (1 / 2) * Kp ** 2 + 12 / 11) * Kpp ** 2 * K ** 2 * (V0 / V) ** (
                                           3 * np.sqrt(-2 * K * Kpp + Kp ** 2)) + ((-(
                    2 * (Kp + 5 / 2)) * Kpp ** 3 * K ** 3 + (4 * (
                    Kp ** 3 + (45 / 8) * Kp ** 2 + (35 / 4) * Kp + 25 / 8)) * Kpp ** 2 * K ** 2 - 5 * Kpp * Kp * (
                                                                                                Kp ** 4 + 8 * Kp ** 3 + 21 * Kp ** 2 + 20 * Kp + 24 / 5) * K * (
                                                                                                1 / 2) + 5 * Kp ** 6 + (
                                                                                                1 / 2) * Kp ** 7 + 35 * Kp ** 5 * (
                                                                                                1 / 2) + 25 * Kp ** 4 + 12 * Kp ** 3) * np.sqrt(
            -2 * K * Kpp + Kp ** 2) + K ** 4 * Kpp ** 4 - 5 * Kpp ** 3 * (Kp ** 2 + 4 * Kp + 7 / 2) * K ** 3 + (
                                                                                               1 / 4) * (25 * (
                    Kp ** 4 + (32 / 5) * Kp ** 3 + (63 / 5) * Kp ** 2 + 8 * Kp + 24 / 25)) * Kpp ** 2 * K ** 2 - (3 * (
                    Kp ** 4 + (25 / 3) * Kp ** 3 + (70 / 3) * Kp ** 2 + 25 * Kp + 8)) * Kpp * Kp ** 2 * K + (
                                                                                               1 / 2) * Kp ** 8 + 5 * Kp ** 7 + 35 * Kp ** 6 * (
                                                                                               1 / 2) + 25 * Kp ** 5 + 12 * Kp ** 4) * (
                                           V0 / V) ** np.sqrt(-2 * K * Kpp + Kp ** 2) + (((2 * (
                    Kp + 5 / 2)) * Kpp ** 3 * K ** 3 - (4 * (
                    Kp ** 3 + (45 / 8) * Kp ** 2 + (35 / 4) * Kp + 25 / 8)) * Kpp ** 2 * K ** 2 + 5 * Kpp * Kp * (
                                                                                                      Kp ** 4 + 8 * Kp ** 3 + 21 * Kp ** 2 + 20 * Kp + 24 / 5) * K * (
                                                                                                      1 / 2) - 5 * Kp ** 6 - (
                                                                                                      1 / 2) * Kp ** 7 - 35 * Kp ** 5 * (
                                                                                                      1 / 2) - 25 * Kp ** 4 - 12 * Kp ** 3) * np.sqrt(
            -2 * K * Kpp + Kp ** 2) + K ** 4 * Kpp ** 4 - 5 * Kpp ** 3 * (Kp ** 2 + 4 * Kp + 7 / 2) * K ** 3 + (
                                                                                                     1 / 4) * (25 * (
                    Kp ** 4 + (32 / 5) * Kp ** 3 + (63 / 5) * Kp ** 2 + 8 * Kp + 24 / 25)) * Kpp ** 2 * K ** 2 - (3 * (
                    Kp ** 4 + (25 / 3) * Kp ** 3 + (70 / 3) * Kp ** 2 + 25 * Kp + 8)) * Kpp * Kp ** 2 * K + (
                                                                                                     1 / 2) * Kp ** 8 + 5 * Kp ** 7 + 35 * Kp ** 6 * (
                                                                                                     1 / 2) + 25 * Kp ** 5 + 12 * Kp ** 4) * (
                                           V0 / V) ** (5 * np.sqrt(-2 * K * Kpp + Kp ** 2)))) * K * (
                                  Kpp * K - (1 / 2) * Kp ** 2) / (((Kp - np.sqrt(-2 * K * Kpp + Kp ** 2)) * (
                    V0 / V) ** np.sqrt(-2 * K * Kpp + Kp ** 2) - Kp - np.sqrt(-2 * K * Kpp + Kp ** 2)) ** 6 * V ** 5))

    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return (Ecalc - Edata)**2


Chr_fix = ['Aa', 'Ba', 'Ca', 'Da', 'Ea', 'Fa', 'Ga', 'Ha', 'Ia', 'Ja', 'Ka', 'La', 'Ma', 'Na', 'Oa', 'Pa', 'Qa', 'Ra',
           'Sa', 'Ta', 'Ua', 'Va', 'Wa', 'Xa', 'Ya', 'Za', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Hb', 'Ib', 'Jb',
           'Kb', 'Lb', 'Mb', 'Nb', 'Ob', 'Pb', 'Qb', 'Rb', 'Sb', 'Tb', 'Ub', 'Vb', 'Wb', 'Xb', 'Yb', 'Zb',
           'Ac', 'Bc', 'Cc', 'Dc', 'Ec', 'Fc', 'Gc', 'Hc', 'Ic', 'Jc', 'Kc', 'Lc', 'Mc', 'Nc', 'Oc', 'Pc', 'Qc', 'Rc',
           'Sc', 'Tc', 'Uc', 'Vc', 'Wc', 'Xc', 'Yc', 'Zc', 'Ad', 'Bd', 'Cd', 'Dd', 'Ed', 'Fd', 'Gd', 'Hd', 'Id', 'Jd',
           'Kd', 'Ld', 'Md', 'Nd', 'Od', 'Pd', 'Qd', 'Rd', 'Sd', 'Td', 'Ud', 'Vd', 'Wd', 'Xd', 'Yd', 'Zd',
           'Ae', 'Be', 'Ce', 'De', 'Ee', 'Fe', 'Ge', 'He', 'Ie', 'Je', 'Ke', 'Le', 'Me', 'Ne', 'Oe', 'Pe', 'Qe', 'Re',
           'Se', 'Te', 'Ue', 'Ve', 'We', 'Xe', 'Ye', 'Ze', 'Af', 'Bf', 'Cf', 'Df', 'Ef', 'Ff', 'Gf', 'Hf', 'If', 'Jf',
           'Kf', 'Lf', 'Mf', 'Nf', 'Of', 'Pf', 'Qf', 'Rf', 'Sf', 'Tf', 'Uf', 'Vf', 'Wf', 'Xf', 'Yf', 'Zf']
nparams_F = 4
nparams_rhophi = 6


class EAM:  #
    """
    EAM potential and derivatives.

    :param Tuple[str,np.ndarray,np.ndarray, float, int] args: formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels.
    :param np.ndarray parameters: EAM potential parameters.
    """

    def __init__(self, *args, units='J/mol', parameters=''):
        formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels = [ai for ai in args]
        #
        # self.stat = 0
        self.nats = len(basis_vectors)
        formula_ABCD = ''.join([Chr_fix[i] for i in range(len(re.findall('[A-Z][^A-Z]*', formula)))])
        self.formula_ABCD = formula_ABCD
        # # ## pr0nt(formula_ABCD)
        #
        atom_types = self.formula_ABCD
        # print('ssssss', atom_types, formula)
        neigbor_distances_at_Vstar, number_of_pairs_per_distance, comb_types = pairanalysis.pair_analysis(atom_types,
                                                                                                          cutoff,
                                                                                                          basis_vectors,
                                                                                                          primitive_cell)
        neigbor_distances_at_Vstar, number_of_pairs_per_distance = neigbor_distances_at_Vstar[
                                                                   :number_of_neighbor_levels], number_of_pairs_per_distance[
                                                                                                :number_of_neighbor_levels,
                                                                                                :]
        #
        # self.comb_type_ABCD = comb_types
        primitive_cell = np.array(primitive_cell)
        aa, bb, cc = primitive_cell[0, :], primitive_cell[1, :], primitive_cell[2, :]
        # Vstar = np.linalg.det(primitive_cell) / len(basis_vectors)
        Vstar = calculate_volume(aa, bb, cc) / len(basis_vectors)

        #
        self.ndist = neigbor_distances_at_Vstar
        self.ndist = np.reshape(self.ndist, (-1, 1))
        self.npair = number_of_pairs_per_distance
        self.Vstar = Vstar
        #
        if units == 'J/mol':
            self.mult_V = A3_ATOM_TO_M3_MOL
            self.mult_E = EV_ATOM_TO_J_MOL
        #
        elif units == 'eV/atom':
            self.mult_V = 1
            self.mult_E = 1
        self.formula = formula
        # # ## pr0nt('#####',formula, primitive_cell, basis_vectors, cutoff, number_of_neighbor_levels)
        self.ntypes_A()
        #
        # if list(parameters):
        #     self.pEOS = parameters
        #     pEOS_pt, pEOS_et = self.paramos_raw_2_pt_et(self.pEOS)
        #
        #     self.params_pair_type(pEOS_pt)
        #     self.params_elmt_type(pEOS_et)
        pass

    def _set_fit_params(self, p) -> None:
        """Set the raw parameter vector and the pair / element parameters derived from it."""
        self.pEOS = np.array(p, dtype=float)
        pEOS_pt, pEOS_et = self.paramos_raw_2_pt_et(self.pEOS)
        self.params_pair_type(pEOS_pt)
        self.params_elmt_type(pEOS_et)

    def fitEOS(self, Vdata: np.ndarray, Edata: np.ndarray, initial_parameters: np.ndarray = None, fit: bool = True, rel_tol: float = 0.02, max_starts: int = 12, on_failure: str = 'raise') -> None:
        """
        Parameters fitting.

        :param Vdata: Input volume data.
        :type Vdata: np.ndarray
        :param Edata: Target energy data.
        :type Edata: np.ndarray
        :param initial_parameters: Initial guess.
        :type initial_parameters: np.ndarray
        :param fit: True to run the fitting. False to just use the input parameters.
        :type fit: bool.
        :param rel_tol: A fit is accepted when its rms is below rel_tol times the energy range of the data (and it has
            a minimum with B0 > 0 within a factor 2 of the data volumes); otherwise other starting points are tried.
        :param max_starts: Maximum number of starting points.
        :param on_failure: 'raise' (EOSFitError, default) or 'warn' (keep the best attempt) when no start passes.

        :return: Optimal parameters.
        :rtype: np.ndarray
        """
        if fit:
            self.pEOS = _fit_with_restarts(self, Vdata, Edata, initial_parameters, (-np.inf, np.inf), 'pair',
                                           rel_tol, max_starts, on_failure)
        if not fit:
            self.pEOS = initial_parameters
    #
        pEOS_pt, pEOS_et = self.paramos_raw_2_pt_et(self.pEOS)

        self.params_pair_type(pEOS_pt)
        self.params_elmt_type(pEOS_et)
        self.V0 = _V0_from_dE0dV(self, Vdata)  # root of dE0/dV (was a bounded minimize, finding 3.10)
        # pr0nt('xxxxx')
    #
        return self.pEOS
    #
    def phiii(self, r, alpha, beta, r_alpha):
        return -alpha * (1 + beta * (r / r_alpha - 1)) * np.exp(-beta * (r / r_alpha - 1))
    #
    def dphiii(self, r, alpha, beta, r_alpha):
        return -alpha * beta * np.exp(-beta * (r / r_alpha - 1)) / r_alpha + alpha * (
                    1 + beta * (r / r_alpha - 1)) * beta * np.exp(-beta * (r / r_alpha - 1)) / r_alpha
    #
    def d2phiii(self, r, alpha, beta, r_alpha):
        return 2 * alpha * beta ** 2 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 2 - alpha * (
                    1 + beta * (r / r_alpha - 1)) * beta ** 2 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 2
    #
    def d3phiii(self, r, alpha, beta, r_alpha):
        return -3 * alpha * beta ** 3 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 3 + alpha * (
                    1 + beta * (r / r_alpha - 1)) * beta ** 3 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 3

    def d4phiii(self, r, alpha, beta, r_alpha):
        return 4 * alpha * beta ** 4 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 4 - alpha * (
                    1 + beta * (r / r_alpha - 1)) * beta ** 4 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 4

    def d5phiii(self, r, alpha, beta, r_alpha):
        return -5 * alpha * beta ** 5 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 5 + alpha * (
                    1 + beta * (r / r_alpha - 1)) * beta ** 5 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 5

    def d6phiii(self, r, alpha, beta, r_alpha):
        return 6 * alpha * beta ** 6 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 6 - alpha * (
                    1 + beta * (r / r_alpha - 1)) * beta ** 6 * np.exp(-beta * (r / r_alpha - 1)) / r_alpha ** 6
    #

    def rhoii(self, r, r_e, f_e, x):
        return f_e * np.exp(-x * (r - r_e))
    #

    def drhoii(self, r, r_e, f_e, x):
        return -f_e * x * np.exp(-x * (r - r_e))
    #

    def d2rhoii(self, r, r_e, f_e, x):
        return f_e * x ** 2 * np.exp(-x * (r - r_e))

    def d3rhoii(self, r, r_e, f_e, x):
        return -f_e * x ** 3 * np.exp(-x * (r - r_e))

    def d4rhoii(self, r, r_e, f_e, x):
        return f_e * x ** 4 * np.exp(-x * (r - r_e))

    def d5rhoii(self, r, r_e, f_e, x):
        return -f_e * x ** 5 * np.exp(-x * (r - r_e))

    def d6rhoii(self, r, r_e, f_e, x):
        return f_e * x ** 6 * np.exp(-x * (r - r_e))
    #
    def F_i(self, rho_i, F0, F1, rho_e, n):
        return -F0 * (1 - np.log((rho_i / rho_e) ** n)) * (rho_i / rho_e) ** n + F1 * (rho_i / rho_e)
    #
    def dF_i(self, rho_i, F0, F1, rho_e, n):
        return (F0 * (rho_i / rho_e) ** n * np.log((rho_i / rho_e) ** n) * n * rho_e + F1 * rho_i) / (rho_i * rho_e)
    #
    def d2F_i(self, rho_i, F0, F1, rho_e, n):
        return n * F0 * (rho_i / rho_e) ** n * ((n - 1) * np.log((rho_i / rho_e) ** n) + n) / rho_i ** 2
    #
    def d3F_i(self, rho_i, F0, F1, rho_e, n):
        return ((n ** 2 - 3 * n + 2) * np.log((rho_i / rho_e) ** n) + 2 * n ** 2 - 3 * n) * n * F0 * (
                    rho_i / rho_e) ** n / rho_i ** 3

    def d4F_i(self, rho_i, F0, F1, rho_e, n):
        return n * F0 * (rho_i / rho_e) ** n * ((n ** 3 - 6 * n ** 2 + 11 * n - 6) * np.log(
            (rho_i / rho_e) ** n) + 3 * n ** 3 - 12 * n ** 2 + 11 * n) / rho_i ** 4

    def d5F_i(self, rho_i, F0, F1, rho_e, n):
        return n * F0 * (rho_i / rho_e) ** n * ((n ** 4 - 10 * n ** 3 + 35 * n ** 2 - 50 * n + 24) * np.log(
            (rho_i / rho_e) ** n) + 4 * n ** 4 - 30 * n ** 3 + 70 * n ** 2 - 50 * n) / rho_i ** 5

    def d6F_i(self, rho_i, F0, F1, rho_e, n):
        return n * F0 * (rho_i / rho_e) ** n * (
                    (n ** 5 - 15 * n ** 4 + 85 * n ** 3 - 225 * n ** 2 + 274 * n - 120) * np.log(
                (rho_i / rho_e) ** n) + 5 * n ** 5 - 60 * n ** 4 + 255 * n ** 3 - 450 * n ** 2 + 274 * n) / rho_i ** 6
    #
    def ab(self, a, b):
    #     # ## pr0nt(a*b)
        return a * b
    #
    def params_elmt_type(self, pEOS):
        self.pEOS_et = pEOS
    #
    def ntypes_A(self):
    #     # # pr0nt('ntypes_A')
        ix = 0
        types_list = re.findall('[A-Z][^A-Z]*', self.formula)
    #
        types_keys = {}
        types_dict = {}
        types_new = []
        for i in range(len(types_list)):
            if i == 0:
                pass
            else:
                if types_list[i] != types_list[i - 1]:
                    ix = max(types_keys.values()) + 1
            try:
                types_keys[types_list[i]]  #### pr0nt(types_list[i],types_keys[types_list[i]])
            except:
                types_keys[types_list[i]] = ix
            types_dict[chr(65 + i)] = str(ix)
            types_new.append(str(ix))
    #
        self.types_new = types_new
    #
        types = list(set(types_dict.values()))

        self.ntypes = len(types)
        types.sort()
        combs_types = list(it.combinations_with_replacement(types, r=2))
        self.comb_types = combs_types
        original_pairs = [A[0] + '-' + A[1] for A in combs_types]
        types_ABCD = list(set(types_dict.keys()))
        types_ABCD.sort()
        combs_types_ABCD = list(it.combinations_with_replacement(types_ABCD, r=2))
        self.new_pairs = [A[0] + '-' + A[1] for A in combs_types_ABCD]
    #
        B_dict = {}
        for A in types_dict.keys():
            B_dict[A] = []
            for AA in self.new_pairs:
                B_dict[A].append(AA.split('-').count(A) * self.nats / 2)
    #
        A_dict = {}
        for A in types_dict.keys():
    #         # ## pr0nt('JJJJJJJJJJJJ',self.npair, self.new_pairs)
            A_dict[A] = 1 * self.ab(np.array([B_dict[A] for _ in self.npair]), self.npair)
    #
        self.A = [A_dict[A] for A in types_ABCD]
        self.types_dict = types_dict
        self.original_pairs = original_pairs
    #
    def params_pair_type(self, pEOS):
        # # pr0nt('params_pair_type')
        p2 = []
        for i in range(len(self.new_pairs)):
            split_types = self.new_pairs[i].split('-')
            p_key = self.types_dict[split_types[0]] + '-' + self.types_dict[split_types[1]]
            p2.append(pEOS[:, self.original_pairs.index(p_key)])

        self.pEOS_pt_ABCD = np.array(p2).T
    #

    def E0(self, V):
        """
        Internal energy.

        :param float V: Volume.

        :return float: Energy.
        """
        if type(V) == np.ndarray:
            return np.array([self.E0(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS_pt = self.pEOS_pt_ABCD.T

        factor_r = (V / self.Vstar) ** (1 / 3)

        r = self.ndist * factor_r
        phi_arr_funct = lambda alpha, beta, r_alpha: -alpha * (1 + beta * (r / r_alpha - 1)) * np.exp(-beta * (r / r_alpha - 1))
        self.phi_arr = np.array([phi_arr_funct(pEOS_pt[:,0],pEOS_pt[:,1],pEOS_pt[:,2])])

        rho_arr_funct = lambda r_e, f_e, x: f_e * np.exp(-x * (r - r_e))
        self.rho_arr = np.array([rho_arr_funct(pEOS_pt[:,3],pEOS_pt[:,4],pEOS_pt[:,5]) ])

        self.rho_is = [np.sum(self.ab(self.rho_arr, Ai)) for Ai in self.A]

        F_is = []
        for i, rho_i in zip(self.types_new, self.rho_is):
            F0, F1, rho_e, n = self.pEOS_et[:, int(i)]
            # ## pr0nt('F0, F1, rho_e, n',F0, F1, rho_e, n)
            F_is.append(self.F_i(rho_i, F0, F1, rho_e, n))
        self.F_is = F_is
        self.Fs = np.sum(self.F_is)
        self.Phis = np.sum(self.ab(self.phi_arr, self.npair)) * self.nats / 2

        return (self.Fs + self.Phis) * (self.mult_E)
    #
    def paramos_raw_2_pt_et(self, params_raw):
        # # pr0nt('paramos_raw_2_pt_et')

        pEOS_pt = np.reshape(params_raw[:-self.ntypes * nparams_F], (-1, nparams_rhophi)).T
        pEOS_et = np.reshape(params_raw[-self.ntypes * nparams_F:], (-1, nparams_F)).T

        # ## pr0nt('pEOS_pt, pEOS_et',pEOS_pt, pEOS_et)
        return pEOS_pt, pEOS_et
    #
    def E04min(self, V: float, pEOS: np.ndarray) -> float:
        """
        Energy for minimization.

        :param V: Volume.
        :type V: float
        :param pEOS: parameters.
        :type pEOS: np.ndarray
        :return: E0.
        :rtype: float
        """

        if type(V)==np.ndarray:
            return np.array([self.E04min(Vi,pEOS) for Vi in V])

        pEOS_pt, pEOS_et = self.paramos_raw_2_pt_et(pEOS)
        self.params_pair_type(pEOS_pt)
        self.params_elmt_type(pEOS_et)
        # if min(pEOS_et)<0:return 1


        return self.E0(V)

    def dE0dV_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: dE0dV_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.dE0dV_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS_pt = self.pEOS_pt_ABCD.T

        r = self.ndist * (V / self.Vstar) ** (1 / 3)
        dr = self.ndist * (V / self.Vstar) ** (-2 / 3) / 3 / self.Vstar

        dphi_arr_funct = lambda a,b,c: self.dphiii(r, a, b, c) * dr
        dphi_arr = np.array([dphi_arr_funct(pEOS_pt[:,0],pEOS_pt[:,1],pEOS_pt[:,2])])

        drho_arr_funct = lambda a, b, c: self.drhoii(r, a, b, c) * dr
        drho_arr = np.array([drho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])

        rho_arr_funct = lambda a, b, c: self.rhoii(r, a, b, c)
        rho_arr = np.array([rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])

        self.rho_is = [np.sum(self.ab(rho_arr, Ai)) for Ai in self.A]
        self.drho_is = [np.sum(self.ab(drho_arr, Ai)) for Ai in self.A]
        dF_is = []
        for i, rho_i, drho_i in zip(self.types_new, self.rho_is, self.drho_is):
            F0, F1, rho_e, n = self.pEOS_et[:, int(i)]
            dF_is.append(self.dF_i(rho_i, F0, F1, rho_e, n) * drho_i)


        dFdV = np.sum(dF_is)
        dPhidV = np.sum(self.ab(dphi_arr, self.npair)) * self.nats / 2

        return (dFdV + dPhidV) * (self.mult_E) / (self.mult_V)
    #
    def d2E0dV2_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy second volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d2E0dV2_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d2E0dV2_T(Vi) for Vi in V])

        V = V / self.mult_V
        pEOS_pt = self.pEOS_pt_ABCD.T

        r = self.ndist * (V / self.Vstar) ** (1 / 3)
        dr = self.ndist * (V / self.Vstar) ** (-2 / 3) / 3 / self.Vstar
        d2r = -2 * self.ndist * (V / self.Vstar) ** (-5 / 3) / 9 / self.Vstar ** 2

        rho_arr_funct = lambda a, b, c: self.rhoii(r, a, b, c)
        drho_arr_funct = lambda a, b, c: self.drhoii(r, a, b, c) * dr
        d2rho_arr_funct = lambda  a, b, c: self.d2rhoii(r, a, b, c) * dr ** 2 + self.drhoii(r, a, b, c) * d2r
        d2phi_arr_funct = lambda a, b, c: self.d2phiii(r, a, b, c) * dr ** 2 + self.dphiii(r, a, b, c) * d2r
        rho_arr = np.array([rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        drho_arr = np.array([drho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        d2rho_arr = np.array([d2rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        d2phi_arr = np.array([d2phi_arr_funct(pEOS_pt[:,0], pEOS_pt[:,1], pEOS_pt[:,2])])

        self.rho_is = [np.sum(self.ab(rho_arr, Ai)) for Ai in self.A]
        self.drho_is = [np.sum(self.ab(drho_arr, Ai)) for Ai in self.A]
        self.d2rho_is = [np.sum(self.ab(d2rho_arr, Ai)) for Ai in self.A]

        d2F_is = []

        for i, rho_i, drho_i, d2rho_i in zip(self.types_new, self.rho_is, self.drho_is, self.d2rho_is):
            F0, F1, rho_e, n = self.pEOS_et[:, int(i)]
            d2F_is.append(
                self.d2F_i(rho_i, F0, F1, rho_e, n) * drho_i ** 2 + self.dF_i(rho_i, F0, F1, rho_e, n) * d2rho_i)

        d2FdV2 = np.sum(d2F_is)

        d2PhidV2 = np.sum(self.ab(d2phi_arr, self.npair)) * self.nats / 2

        return (d2FdV2 + d2PhidV2) * (self.mult_E) / (self.mult_V) ** 2
    #
    def d3E0dV3_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy third volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d3E0dV3_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d3E0dV3_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS_pt = self.pEOS_pt_ABCD.T

        r = self.ndist * (V / self.Vstar) ** (1 / 3)
        dr = self.ndist * (V / self.Vstar) ** (-2 / 3) / 3 / self.Vstar
        d2r = -2 * self.ndist * (V / self.Vstar) ** (-5 / 3) / 9 / self.Vstar ** 2
        d3r = 10 * self.ndist * (V / self.Vstar) ** (-8 / 3) / 27 / self.Vstar ** 3

        rho_arr_funct = lambda a, b, c: self.rhoii(r, a, b, c)
        drho_arr_funct = lambda a, b, c: self.drhoii(r, a, b, c) * dr
        d2rho_arr_funct = lambda a, b, c: self.d2rhoii(r, a, b, c) * dr ** 2 + self.drhoii(r, a, b, c) * d2r
        d3rho_arr_funct = lambda a, b, c: self.d3rhoii(r, a, b, c) * dr ** 3 + 3 * self.d2rhoii(r, a, b, c) * dr * d2r + self.drhoii(r, a, b, c) * d3r
        d3phi_arr_funct = lambda a, b, c: self.d3phiii(r, a, b, c) * dr ** 3 + 3 * self.d2phiii(r, a, b, c) * dr * d2r + self.dphiii(r, a, b, c) * d3r
        rho_arr = np.array([rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        drho_arr = np.array([drho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        d2rho_arr = np.array([d2rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        d3rho_arr = np.array([d3rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        d3phi_arr = np.array([d3phi_arr_funct(pEOS_pt[:,0], pEOS_pt[:,1], pEOS_pt[:,2])])

        self.rho_is = [np.sum(self.ab(rho_arr, Ai)) for Ai in self.A]
        self.drho_is = [np.sum(self.ab(drho_arr, Ai)) for Ai in self.A]
        self.d2rho_is = [np.sum(self.ab(d2rho_arr, Ai)) for Ai in self.A]
        self.d3rho_is = [np.sum(self.ab(d3rho_arr, Ai)) for Ai in self.A]
        d3F_is = []
        for i, rho_i, drho_i, d2rho_i, d3rho_i in zip(self.types_new, self.rho_is, self.drho_is, self.d2rho_is,
                                                      self.d3rho_is):
            F0, F1, rho_e, n = self.pEOS_et[:, int(i)]
            d3F_is.append(self.d3F_i(rho_i, F0, F1, rho_e, n) * drho_i ** 3 + 3 * self.d2F_i(rho_i, F0, F1, rho_e,
                                                                                             n) * drho_i * d2rho_i + self.dF_i(
                rho_i, F0, F1, rho_e, n) * d3rho_i)

        d3FdV3 = np.sum(d3F_is)

        d3PhidV3 = np.sum(self.ab(d3phi_arr, self.npair)) * self.nats / 2

        return (d3FdV3 + d3PhidV3) * (self.mult_E) / (self.mult_V) ** 3

    def d4E0dV4_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fourth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d4E0dV4_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d4E0dV4_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS_pt = self.pEOS_pt_ABCD.T

        r = self.ndist * (V / self.Vstar) ** (1 / 3)
        dr = self.ndist * (V / self.Vstar) ** (-2 / 3) / 3 / self.Vstar
        d2r = -2 * self.ndist * (V / self.Vstar) ** (-5 / 3) / 9 / self.Vstar ** 2
        d3r = 10 * self.ndist * (V / self.Vstar) ** (-8 / 3) / 27 / self.Vstar ** 3
        d4r = -80 * self.ndist * (V / self.Vstar) ** (-11 / 3) / 81 / self.Vstar ** 4

        rho_arr_funct = lambda a, b, c: self.rhoii(r, a, b, c)
        drho_arr_funct = lambda a, b, c: self.drhoii(r, a, b, c) * dr
        d2rho_arr_funct = lambda a, b, c: self.d2rhoii(r, a, b, c) * dr ** 2 + self.drhoii(r, a, b, c) * d2r
        d3rho_arr_funct= lambda a, b, c: self.d3rhoii(r, a, b, c) * dr ** 3 + 3 * self.d2rhoii(r, a, b, c) * dr * d2r + self.drhoii(r, a, b, c) * d3r
        d4rho_arr_funct = lambda a, b, c: self.d4rhoii(r, a, b, c) * dr ** 4 + 6 * self.d3rhoii(r, a, b, c) * dr ** 2 * d2r + 3 * self.d2rhoii(r, a, b, c) * d2r ** 2 + 4 * self.d2rhoii(r, a, b, c) * dr * d3r + self.drhoii(r, a, b, c) * d4r

        d4phi_arr_funct = lambda a, b, c: self.d4phiii(r, a, b, c) * dr ** 4 + 6 * self.d3phiii(r, a, b, c) * dr ** 2 * d2r + 3 * self.d2phiii(r, a, b, c) * d2r ** 2 + 4 * self.d2phiii(r, a, b, c) * dr * d3r + self.dphiii(r, a, b, c) * d4r

        rho_arr = np.array([rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        drho_arr = np.array([drho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        d2rho_arr = np.array([d2rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        d3rho_arr = np.array([d3rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        d4rho_arr = np.array([d4rho_arr_funct(pEOS_pt[:,3], pEOS_pt[:,4], pEOS_pt[:,5])])
        d4phi_arr = np.array([d4phi_arr_funct(pEOS_pt[:,0], pEOS_pt[:,1], pEOS_pt[:,2])])

        self.rho_is = [np.sum(self.ab(rho_arr, Ai)) for Ai in self.A]
        self.drho_is = [np.sum(self.ab(drho_arr, Ai)) for Ai in self.A]
        self.d2rho_is = [np.sum(self.ab(d2rho_arr, Ai)) for Ai in self.A]
        self.d3rho_is = [np.sum(self.ab(d3rho_arr, Ai)) for Ai in self.A]
        self.d4rho_is = [np.sum(self.ab(d4rho_arr, Ai)) for Ai in self.A]
        d4F_is = []
        for i, rho_i, drho_i, d2rho_i, d3rho_i, d4rho_i in zip(self.types_new, self.rho_is, self.drho_is, self.d2rho_is,
                                                               self.d3rho_is, self.d4rho_is):
            F0, F1, rho_e, n = self.pEOS_et[:, int(i)]
            d4F_is.append(self.d4F_i(rho_i, F0, F1, rho_e, n) * drho_i ** 4 + 6 * self.d3F_i(rho_i, F0, F1, rho_e,
                                                                                             n) * drho_i ** 2 * d2rho_i + 3 * self.d2F_i(
                rho_i, F0, F1, rho_e, n) * d2rho_i ** 2 + 4 * self.d2F_i(rho_i, F0, F1, rho_e,
                                                                         n) * drho_i * d3rho_i + self.dF_i(rho_i, F0,
                                                                                                           F1, rho_e,
                                                                                                           n) * d4rho_i)

        d4FdV4 = np.sum(d4F_is)

        d4PhidV4 = np.sum(self.ab(d4phi_arr, self.npair)) * self.nats / 2

        return (d4FdV4 + d4PhidV4) * (self.mult_E) / (self.mult_V) ** 4

    def d5E0dV5_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy fifth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d5E0dV5_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d5E0dV5_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS_pt = self.pEOS_pt_ABCD.T

        r = self.ndist * (V / self.Vstar) ** (1 / 3)
        dr = self.ndist * (V / self.Vstar) ** (-2 / 3) / 3 / self.Vstar
        d2r = -2 * self.ndist * (V / self.Vstar) ** (-5 / 3) / 9 / self.Vstar ** 2
        d3r = 10 * self.ndist * (V / self.Vstar) ** (-8 / 3) / 27 / self.Vstar ** 3
        d4r = -80 * self.ndist * (V / self.Vstar) ** (-11 / 3) / 81 / self.Vstar ** 4
        d5r = 880 * self.ndist * (V / self.Vstar) ** (-14 / 3) / 243 / self.Vstar ** 5

        rho_arr_funct = lambda a, b, c: self.rhoii(r, a, b, c)
        drho_arr_funct = lambda a, b, c: self.drhoii(r, a, b, c) * dr
        d2rho_arr_funct = lambda a, b, c: self.d2rhoii(r, a, b, c) * dr ** 2 + self.drhoii(r, a, b, c) * d2r
        d3rho_arr_funct = lambda a, b, c: self.d3rhoii(r, a, b, c) * dr ** 3 + 3 * self.d2rhoii(r, a, b,c) * dr * d2r + self.drhoii(r, a, b, c) * d3r
        d4rho_arr_funct = lambda a, b, c: self.d4rhoii(r, a, b, c) * dr ** 4 + 6 * self.d3rhoii(r, a, b,c) * dr ** 2 * d2r + 3 * self.d2rhoii(r, a, b, c) * d2r ** 2 + 4 * self.d2rhoii(r, a, b, c) * dr * d3r + self.drhoii(r, a, b, c) * d4r
        d5rho_arr_funct = lambda a, b, c: self.d5rhoii(r, a, b, c) * dr ** 5 + 10 * self.d4rhoii(r, a, b, c) * dr ** 3 * d2r + 15 * self.d3rhoii(r, a, b, c) * dr * d2r ** 2 + 10 * self.d3rhoii(r, a, b, c) * dr ** 2 * d3r + 10 * self.d2rhoii(r, a, b, c) * d2r * d3r + 5 * self.d2rhoii(r,a, b, c) * dr * d4r + self.drhoii(r, a, b, c) * d5r
        d5phi_arr_funct = lambda a, b, c: self.d5phiii(r, a, b, c) * dr ** 5 + 10 * self.d4phiii(r, a, b, c) * dr ** 3 * d2r + 15 * self.d3phiii(r, a, b, c) * dr * d2r ** 2 + 10 * self.d3phiii(r,a, b, c) * dr ** 2 * d3r + 10 * self.d2phiii(r, a, b, c) * d2r * d3r + 5 * self.d2phiii(r, a, b, c) * dr * d4r + self.dphiii(r, a, b, c) * d5r

        rho_arr = np.array([rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        drho_arr = np.array([drho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d2rho_arr = np.array([d2rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d3rho_arr = np.array([d3rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d4rho_arr = np.array([d4rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d5rho_arr = np.array([d5rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d5phi_arr = np.array([d5phi_arr_funct(pEOS_pt[:, 0], pEOS_pt[:, 1], pEOS_pt[:, 2])])  # pair parameters (were the density ones, finding 3.7)

        self.rho_is = [np.sum(self.ab(rho_arr, Ai)) for Ai in self.A]
        self.drho_is = [np.sum(self.ab(drho_arr, Ai)) for Ai in self.A]
        self.d2rho_is = [np.sum(self.ab(d2rho_arr, Ai)) for Ai in self.A]
        self.d3rho_is = [np.sum(self.ab(d3rho_arr, Ai)) for Ai in self.A]
        self.d4rho_is = [np.sum(self.ab(d4rho_arr, Ai)) for Ai in self.A]
        self.d5rho_is = [np.sum(self.ab(d5rho_arr, Ai)) for Ai in self.A]
        d5F_is = []
        for i, rho_i, drho_i, d2rho_i, d3rho_i, d4rho_i, d5rho_i in zip(self.types_new, self.rho_is, self.drho_is,
                                                                        self.d2rho_is, self.d3rho_is, self.d4rho_is,
                                                                        self.d5rho_is):
            F0, F1, rho_e, n = self.pEOS_et[:, int(i)]
            d5F_is.append(self.d5F_i(rho_i, F0, F1, rho_e, n) * drho_i ** 5 + 10 * self.d4F_i(rho_i, F0, F1, rho_e,
                                                                                              n) * drho_i ** 3 * d2rho_i + 15 * self.d3F_i(
                rho_i, F0, F1, rho_e, n) * drho_i * d2rho_i ** 2 + 10 * self.d3F_i(rho_i, F0, F1, rho_e,
                                                                                   n) * drho_i ** 2 * d3rho_i + 10 * self.d2F_i(
                rho_i, F0, F1, rho_e, n) * d2rho_i * d3rho_i + 5 * self.d2F_i(rho_i, F0, F1, rho_e,
                                                                              n) * drho_i * d4rho_i + self.dF_i(rho_i,
                                                                                                                F0, F1,
                                                                                                                rho_e,
                                                                                                                n) * d5rho_i)

        d5FdV5 = np.sum(d5F_is)

        d5PhidV5 = np.sum(self.ab(d5phi_arr, self.npair)) * self.nats / 2

        return (d5FdV5 + d5PhidV5) * (self.mult_E) / (self.mult_V) ** 5

    def d6E0dV6_T(self, V: float|np.ndarray) -> float|np.ndarray:
        """
        Internal energy sixth volume derivative.

        :param V: Volume.
        :type V: float|np.ndarray
        :return: d6E0dV6_T(V)
        :rtype: float|np.ndarray
        """
        if type(V) == np.ndarray:
            return np.array([self.d6E0dV6_T(Vi) for Vi in V])
        V = V / self.mult_V
        pEOS_pt = self.pEOS_pt_ABCD.T

        r = self.ndist * (V / self.Vstar) ** (1 / 3)
        dr = self.ndist * (V / self.Vstar) ** (-2 / 3) / 3 / self.Vstar
        d2r = -2 * self.ndist * (V / self.Vstar) ** (-5 / 3) / 9 / self.Vstar ** 2
        d3r = 10 * self.ndist * (V / self.Vstar) ** (-8 / 3) / 27 / self.Vstar ** 3
        d4r = -80 * self.ndist * (V / self.Vstar) ** (-11 / 3) / 81 / self.Vstar ** 4
        d5r = 880 * self.ndist * (V / self.Vstar) ** (-14 / 3) / 243 / self.Vstar ** 5
        d6r = -12320 * self.ndist * (V / self.Vstar) ** (-17 / 3) / 729 / self.Vstar ** 6

        rho_arr_funct = lambda a, b, c: self.rhoii(r, a, b, c)
        drho_arr_funct = lambda a, b, c: self.drhoii(r, a, b, c) * dr
        d2rho_arr_funct = lambda a, b, c: self.d2rhoii(r, a, b, c) * dr ** 2 + self.drhoii(r, a, b, c) * d2r
        d3rho_arr_funct = lambda a, b, c: self.d3rhoii(r, a, b, c) * dr ** 3 + 3 * self.d2rhoii(r, a, b,
                                                                                                c) * dr * d2r + self.drhoii(
            r, a, b, c) * d3r
        d4rho_arr_funct = lambda a, b, c: self.d4rhoii(r, a, b, c) * dr ** 4 + 6 * self.d3rhoii(r, a, b,
                                                                                                c) * dr ** 2 * d2r + 3 * self.d2rhoii(
            r, a, b, c) * d2r ** 2 + 4 * self.d2rhoii(r, a, b, c) * dr * d3r + self.drhoii(r, a, b, c) * d4r
        d5rho_arr_funct = lambda a, b, c: self.d5rhoii(r, a, b, c) * dr ** 5 + 10 * self.d4rhoii(r, a, b,
                                                                                                 c) * dr ** 3 * d2r + 15 * self.d3rhoii(
            r, a, b, c) * dr * d2r ** 2 + 10 * self.d3rhoii(r, a, b, c) * dr ** 2 * d3r + 10 * self.d2rhoii(r, a, b,
                                                                                                            c) * d2r * d3r + 5 * self.d2rhoii(
            r, a, b, c) * dr * d4r + self.drhoii(r, a, b, c) * d5r

        d6rho_arr_funct = lambda a, b, c: 1 * self.d6rhoii(r, a, b, c) * dr ** 6 + 15 * self.d5rhoii(r, a, b, c) * dr ** 4 * d2r +45 * self.d4rhoii(r, a, b, c) * dr ** 2 * d2r ** 2 +20 * self.d4rhoii(r, a, b, c) * dr ** 3 * d3r +15 * self.d3rhoii(r, a, b, c) * d2r ** 3 +60 * self.d3rhoii(r, a, b, c) * dr * d2r * d3r +15 * self.d3rhoii(r, a, b, c) * dr ** 2 * d4r +10 * self.d2rhoii(r, a, b, c) * d3r ** 2 +15 * self.d2rhoii(r, a, b, c) * d2r * d4r +6 * self.d2rhoii(r, a, b, c) * dr * d5r +1 * self.drhoii(r, a, b, c) * d6r

        d6phi_arr_funct = lambda a, b, c: self.d6phiii(r, a, b, c) * dr ** 6 + 15 * self.d5phiii(r, a, b, c) * dr ** 4 * d2r + 45 * self.d4phiii(r, a, b, c) * dr ** 2 * d2r ** 2 + 20 * self.d4phiii(r, a, b, c) * dr ** 3 * d3r + 15 * self.d3phiii(r, a, b, c) * d2r ** 3 + 60 * self.d3phiii(r, a, b, c) * dr * d2r * d3r + 15 * self.d3phiii(r,a, b, c) * dr ** 2 * d4r + 10 * self.d2phiii(r, a, b, c) * d3r ** 2 + 15 * self.d2phiii(r, a, b, c) * d2r * d4r + 6 * self.d2phiii(r, a, b, c) * dr * d5r + self.dphiii(r, a, b, c) * d6r
        rho_arr = np.array([rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        drho_arr = np.array([drho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d2rho_arr = np.array([d2rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d3rho_arr = np.array([d3rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d4rho_arr = np.array([d4rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d5rho_arr = np.array([d5rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d6rho_arr = np.array([d6rho_arr_funct(pEOS_pt[:, 3], pEOS_pt[:, 4], pEOS_pt[:, 5])])
        d6phi_arr = np.array([d6phi_arr_funct(pEOS_pt[:, 0], pEOS_pt[:, 1], pEOS_pt[:, 2])])



        self.rho_is = [np.sum(self.ab(rho_arr, Ai)) for Ai in self.A]
        self.drho_is = [np.sum(self.ab(drho_arr, Ai)) for Ai in self.A]
        self.d2rho_is = [np.sum(self.ab(d2rho_arr, Ai)) for Ai in self.A]
        self.d3rho_is = [np.sum(self.ab(d3rho_arr, Ai)) for Ai in self.A]
        self.d4rho_is = [np.sum(self.ab(d4rho_arr, Ai)) for Ai in self.A]
        self.d5rho_is = [np.sum(self.ab(d5rho_arr, Ai)) for Ai in self.A]
        self.d6rho_is = [np.sum(self.ab(d6rho_arr, Ai)) for Ai in self.A]
        d6F_is = []
        for i, rho_i, drho_i, d2rho_i, d3rho_i, d4rho_i, d5rho_i, d6rho_i in zip(self.types_new, self.rho_is, self.drho_is,
                                                                        self.d2rho_is, self.d3rho_is, self.d4rho_is,
                                                                        self.d5rho_is, self.d6rho_is):
            F0, F1, rho_e, n = self.pEOS_et[:, int(i)]
            # last term: F'(rho) * d6rho/dV6 (was F'(rho) * d6r/dV6, finding 3.7)
            d6F_is.append(self.d6F_i(rho_i, F0, F1, rho_e, n) * drho_i ** 6 + 15 * self.d5F_i(rho_i, F0, F1, rho_e,
                                                                                              n) * drho_i ** 4 * d2rho_i + 45 * self.d4F_i(
                rho_i, F0, F1, rho_e, n) * drho_i ** 2 * d2rho_i ** 2 + 20 * self.d4F_i(rho_i, F0, F1, rho_e,
                                                                                        n) * drho_i ** 3 * d3rho_i + 15 * self.d3F_i(
                rho_i, F0, F1, rho_e, n) * d2rho_i ** 3 + 60 * self.d3F_i(rho_i, F0, F1, rho_e,
                                                                          n) * drho_i * d2rho_i * d3rho_i + 15 * self.d3F_i(
                rho_i, F0, F1, rho_e, n) * drho_i ** 2 * d4rho_i + 10 * self.d2F_i(rho_i, F0, F1, rho_e,
                                                                                   n) * d3rho_i ** 2 + 15 * self.d2F_i(
                rho_i, F0, F1, rho_e, n) * d2rho_i * d4rho_i + 6 * self.d2F_i(rho_i, F0, F1, rho_e,
                                                                              n) * drho_i * d5rho_i + self.dF_i(rho_i,
                                                                                                                F0, F1,
                                                                                                                rho_e,
                                                                                                                n) * d6rho_i)

        d6FdV6 = np.sum(d6F_is)
        d6PhidV6 = np.sum(self.ab(d6phi_arr, self.npair)) * self.nats / 2
        return (d6FdV6 + d6PhidV6) * (self.mult_E) / (self.mult_V) ** 6
    #
    def error2min(self, P: np.ndarray, Vdata: np.ndarray, Edata: np.ndarray) -> np.ndarray:
        """
        Error for minimization.

        :param P: E0 parameters.
        :type P: np.ndarray
        :param Vdata: Volume data.
        :type Vdata: np.ndarray
        :param Edata: Energy data.
        :type Edata: np.ndarray
        :return: Error.
        :rtype: np.ndarray
        """
        Ecalc = [self.E04min(Vi, P) for Vi in Vdata]
        return np.asarray(Ecalc) - np.asarray(Edata)  # residuals; least_squares squares them (review finding 3.5)


def EVBBp_to_TBparams(pEOS):
    E0, V0, B0, Bp0 = pEOS
    Y_y = abs(Bp0 ** 2 * E0 ** 2 + 4 * B0 * E0 * V0 - 2 * Bp0 * E0 ** 2 + E0 ** 2)
    X_x = 3 * Bp0 * E0 - 3 * E0 + 3 * np.sqrt(Y_y)
    _P0 = -(X_x) * np.exp(3 * Bp0 - 3 - (X_x) / (2 * E0)) / (2 * (3 * Bp0 - 3 - (X_x) / E0))
    _P1 = E0 * (3 * Bp0 - 3 - (X_x) / (2 * E0)) * np.exp((X_x) / (2 * E0)) / (3 * Bp0 - 3 - (X_x) / E0)
    _P2 = (3 * Bp0 - 3 - (X_x) / (2 * E0)) / V0 ** (1 / 3)
    _P3 = (X_x) / (2 * E0 * V0 ** (1 / 3))
    return _P0, _P1, _P2, _P3


def EVBBp_to_BMparams(pEOS):
    E0, V0, B0, Bp0 = pEOS
    P_0 = -9 * V0 * B0 * Bp0 * (1 / 16) + 27 * V0 * B0 * (1 / 8) + E0
    P_1 = 27 * V0 ** (5 / 3) * B0 * Bp0 * (1 / 16) - 9 * V0 ** (5 / 3) * B0
    P_2 = -27 * V0 ** (7 / 3) * B0 * Bp0 * (1 / 16) + 63 * V0 ** (7 / 3) * B0 * (1 / 8)
    P_3 = (9 / 16) * V0 ** 3 * B0 * Bp0 - (9 / 4) * V0 ** 3 * B0

    return P_0, P_1, P_2, P_3
