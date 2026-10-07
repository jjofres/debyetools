"""
Debye function D_3(x) = 3/x^3 * int_0^x t^3/(e^t - 1) dt and its first three derivatives.

x < 2 : series D_3 = 1 - 3x/8 + sum_k 3 B_2k x^2k / ((2k+3)(2k)!)  (converges for |x| < 2 pi; 20 terms)
x >= 2: D_3 = pi^4/(5 x^3) - 3/x^3 * sum_k e^(-kx) (x^3/k + 3x^2/k^2 + 6x/k^3 + 6/k^4)
        derivatives from the exact recurrences, written with e^(-x) so that no overflow or clamp is needed.
Both branches are accurate to ~1e-15 relative for any x >= 0. NaN or negative x gives NaN.
All functions accept scalars or arrays (vectorised) and return the same shape.
"""
import numpy as np

_X_SWITCH = 2.0
_C = np.array([
    0.05,
    -0.0005952380952380953,
    1.1022927689594357e-05,
    -2.2546897546897547e-07,
    4.8177131510464845e-09,
    -1.0568380277374986e-10,
    2.3616240936502374e-12,
    -5.352126783667236e-14,
    1.2265802937539779e-15,
    -2.8367852589887764e-17,
    6.610803394032275e-19,
    -1.5504960762013913e-20,
    3.656593489271863e-22,
    -8.664694284229884e-24,
    2.061774956670621e-25,
    -4.924106287604745e-27,
    1.1798695748228635e-28,
    -2.8353807235887003e-30,
    6.831756773484179e-32,
    -1.6500156388609047e-33])                  # c_2k, k = 1..20
_K2 = 2 * np.arange(1, len(_C) + 1)  # exponents 2k


def lncomplex(z: complex) -> complex|float:
    """
    Complex natural logarithm (kept for backward compatibility; no longer used by D_3).

    :param z: a complex number.
    :type z: complex
    :return: complex log of z
    :rtype: complex
    """
    x=np.real(z)
    _y=np.imag(z)
    _r=np.abs(z)
    return complex(np.log(_r),np.arctan2(_y, x))


def _out(x_in, y):
    return float(y[0]) if np.ndim(x_in) == 0 else y


def _series(x, order):
    """order-th derivative of the small-x series at x (array)."""
    x = x[:, None]
    if order == 0:
        poly = 1 - 3 * x[:, 0] / 8
        terms = _C * x ** _K2
    else:
        fall = np.ones_like(_K2, dtype=float)
        for j in range(order):
            fall = fall * (_K2 - j)
        poly = {1: np.full(x.shape[0], -3 / 8), 2: np.zeros(x.shape[0]), 3: np.zeros(x.shape[0])}[order]
        nz = fall != 0                      # drop terms whose order-th derivative vanishes (avoids 0 * x^-1 at x = 0)
        terms = (_C * fall)[nz] * x ** (_K2 - order)[nz]
    return poly + terms.sum(axis=1)


def _large(x):
    """D_3 for x >= 2 (array)."""
    kmax = int(np.ceil(40. / max(np.min(x), _X_SWITCH))) + 1
    k = np.arange(1, kmax + 1)[None, :]
    xx = x[:, None]
    with np.errstate(under='ignore', invalid='ignore'):
        tail = (np.exp(-k * xx) * (xx ** 3 / k + 3 * xx ** 2 / k ** 2 + 6 * xx / k ** 3 + 6 / k ** 4)).sum(axis=1)
        D = np.pi ** 4 / (5 * x ** 3) - 3 * tail / x ** 3
    return np.where(np.isinf(x), 0., D)


def _bose(x):
    """x/(e^x - 1), e^x/(e^x - 1)^2 and e^x/(e^x - 1) written with e^-x (array, x >= 2)."""
    with np.errstate(under='ignore', invalid='ignore'):
        em = np.exp(-x)
        q = em / (1 - em)                   # 1/(e^x - 1)
        xq = np.where(em > 0, x * q, 0.)    # x/(e^x - 1), 0 for x = inf
    e2 = em / (1 - em) ** 2                 # e^x/(e^x - 1)^2
    r = 1 / (1 - em)                        # e^x/(e^x - 1)
    return xq, e2, r


def D_3(x: float|np.ndarray) -> float|np.ndarray:
    """
    Debye function with n=3.

    :param x: theta_D/T (>= 0).
    :type x: float|np.ndarray
    :return: Debye function of x with n=3.
    :rtype: float|np.ndarray
    """
    xa = np.atleast_1d(np.asarray(x, dtype=float))
    y = np.full(xa.shape, np.nan)
    s = (xa >= 0) & (xa < _X_SWITCH)
    l = xa >= _X_SWITCH
    if s.any():
        y[s] = _series(xa[s], 0)
    if l.any():
        y[l] = _large(xa[l])
    return _out(x, y)


def dD_3dx(x: float|np.ndarray, D3: float|np.ndarray) -> float|np.ndarray:
    """
    First derivative of the Debye function, dD_3/dx = 3/x (x/(e^x - 1) - D_3).

    :param x: theta_D/T.
    :type x: float|np.ndarray
    :param D3: D_3(x) (used for x >= 2; the series is used below).
    :type D3: float|np.ndarray
    :return: dD_3/dx
    :rtype: float|np.ndarray
    """
    xa = np.atleast_1d(np.asarray(x, dtype=float))
    D3a = np.broadcast_to(np.atleast_1d(np.asarray(D3, dtype=float)), xa.shape)
    y = np.full(xa.shape, np.nan)
    s = (xa >= 0) & (xa < _X_SWITCH)
    l = xa >= _X_SWITCH
    if s.any():
        y[s] = _series(xa[s], 1)
    if l.any():
        xl = xa[l]
        xq, _, _ = _bose(xl)
        y[l] = 3 / xl * (xq - D3a[l])
    return _out(x, y)


def d2D_3dx2(x: float|np.ndarray, D3: float|np.ndarray, dD3dx: float|np.ndarray) -> float|np.ndarray:
    """
    Second derivative of the Debye function, -3 e^x/(e^x-1)^2 - 3 D_3'/x + 3 D_3/x^2.

    :param x: theta_D/T.
    :type x: float|np.ndarray
    :param D3: D_3(x).
    :type D3: float|np.ndarray
    :param dD3dx: dD_3/dx.
    :type dD3dx: float|np.ndarray
    :return: d2D_3/dx2
    :rtype: float|np.ndarray
    """
    xa = np.atleast_1d(np.asarray(x, dtype=float))
    D3a = np.broadcast_to(np.atleast_1d(np.asarray(D3, dtype=float)), xa.shape)
    d1a = np.broadcast_to(np.atleast_1d(np.asarray(dD3dx, dtype=float)), xa.shape)
    y = np.full(xa.shape, np.nan)
    s = (xa >= 0) & (xa < _X_SWITCH)
    l = xa >= _X_SWITCH
    if s.any():
        y[s] = _series(xa[s], 2)
    if l.any():
        xl = xa[l]
        _, e2, _ = _bose(xl)
        y[l] = -3 * e2 - 3 * d1a[l] / xl + 3 * D3a[l] / xl ** 2
    return _out(x, y)


def d3D_3dx3(x: float|np.ndarray, _D3: float|np.ndarray, _dD3dx: float|np.ndarray, _d2D3dx2: float|np.ndarray) -> float|np.ndarray:
    """
    Third derivative of the Debye function,
    -3 E2 + 6 E2 e^x/(e^x-1) - 3 D_3''/x + 6 D_3'/x^2 - 6 D_3/x^3, E2 = e^x/(e^x-1)^2.

    :param x: theta_D/T.
    :type x: float|np.ndarray
    :param _D3: D_3(x).
    :type _D3: float|np.ndarray
    :param _dD3dx: dD_3/dx.
    :type _dD3dx: float|np.ndarray
    :param _d2D3dx2: d2D_3/dx2.
    :type _d2D3dx2: float|np.ndarray
    :return: d3D_3/dx3
    :rtype: float|np.ndarray
    """
    xa = np.atleast_1d(np.asarray(x, dtype=float))
    D3a = np.broadcast_to(np.atleast_1d(np.asarray(_D3, dtype=float)), xa.shape)
    d1a = np.broadcast_to(np.atleast_1d(np.asarray(_dD3dx, dtype=float)), xa.shape)
    d2a = np.broadcast_to(np.atleast_1d(np.asarray(_d2D3dx2, dtype=float)), xa.shape)
    y = np.full(xa.shape, np.nan)
    s = (xa >= 0) & (xa < _X_SWITCH)
    l = xa >= _X_SWITCH
    if s.any():
        y[s] = _series(xa[s], 3)
    if l.any():
        xl = xa[l]
        _, e2, r = _bose(xl)
        y[l] = -3 * e2 + 6 * e2 * r - 3 * d2a[l] / xl + 6 * d1a[l] / xl ** 2 - 6 * D3a[l] / xl ** 3
    return _out(x, y)
