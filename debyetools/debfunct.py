import numpy as np
import mpmath as mp
def lncomplex(z: complex) -> complex|float:
    """
    Complex natural logarithm.
    :param z: a complex number.
    :type z: complex
    :return: complex log of z
    :rtype: complex
    """
    x=np.real(z)
    _y=np.imag(z)
    _r=np.abs(z)
    return complex(np.log(_r),np.arctan2(_y, x))

def D_3(x: float|np.ndarray) -> float|np.ndarray:
    """
    Debye function with n=3.
    :param x:
    :type x: float|np.ndarray
    :return: Debye function of x with n=3.
    :rtype: float|np.ndarray
    """
    if type(x)==np.ndarray:
        return np.array([D_3(xi) for xi in x])
    if np.isnan(x):
        return 0
    if x >=499.99999999999966:
        return 1.5585456848144562e-07
    elif x>=1.579779e+01:
        return np.pi**4/(5*x**3)
    else:
        ex=np.exp(x)
        d1, d2, d3, d4, d5, d6 = -np.pi**4/(5*x**3), -3*x*(1/4), np.real(+3*lncomplex(-ex+1)),np.real(+9*mp.fp.polylog(2,ex)/x), np.real(-18*mp.fp.polylog(3,ex)/x**2), np.real(+18*mp.fp.polylog(4,ex)/x**3)
        return d1+d2+d3+d4+d5+d6
def dD_3dx(x: float|np.ndarray, D3: float|np.ndarray) -> float|np.ndarray:
    """
    Debye function derivative

    :param x:
    :type x: float|np.ndarray
    :param D3:
    :type D3: float|np.ndarray
    :return:
    :rtype: float|np.ndarray
    """
    if type(x)==np.ndarray:
        return np.array([dD_3dx(xi,D3i) for xi,D3i in zip(x,D3)])

    if x >= 709.782712893384:
        return -2.3027630998995085e-10
    return np.real(3/x * (x/(np.exp(x)-1) - D_3(x)) )

def d2D_3dx2(x: float|np.ndarray, D3: float|np.ndarray, dD3dx: float|np.ndarray) -> float|np.ndarray:
    """
    Debye function derivative.

    :param x:
    :type x: float|np.ndarray
    :param D3:
    :type D3: float|np.ndarray
    :param dD3dx:
    :type dD3dx: float|np.ndarray
    :return:
    :rtype: float|np.ndarray
    """
    if type(x)==np.ndarray:
        return np.array([d2D_3dx2(xi,D3i,dD3dxi) for xi,D3i,dD3dxi in zip(x,D3, dD3dx)])
    if x >=354.89135644669:
        exp_exp2=7.458340731215135e-155
    else:
        exp_exp2=(np.exp(x)/(np.exp(x)-1.)**2.)
    return np.real(-3.*exp_exp2+-3.*dD3dx/x+3.*D3/x**2)

def d3D_3dx3(x: float|np.ndarray, _D3: float|np.ndarray, _dD3dx: float|np.ndarray, _d2D3dx2: float|np.ndarray) -> float|np.ndarray:
    """
    Debye function derivative.

    :param x:
    :type x: float|np.ndarray
    :param _D3:
    :type _D3: float|np.ndarray
    :param _dD3dx:
    :type _dD3dx: float|np.ndarray
    :param _d2D3dx2:
    :type _d2D3dx2: float|np.ndarray
    :return:
    :rtype: float|np.ndarray
    """
    if type(x)==np.ndarray:
        return np.array([d3D_3dx3(xi,D3i,dD3dxi,d2D3dx2i) for xi,D3i,dD3dxi,d2D3dx2i in zip(x,_D3, _dD3dx, _d2D3dx2)])
    if x>=709.782712893384:
        exp_x = 1.7976931348622732e+308
    else:
        exp_x=np.exp(x)
    if x>=354.89135644669:
        exp_exp2=7.458340731215135e-155
    else:
        exp_exp2 = exp_x/(exp_x-1.)**2.
    return - 3*exp_exp2 + 6.*exp_exp2*exp_x/(exp_x-1.) - 3.*_d2D3dx2/x+6*_dD3dx/x**2 - 6.*_D3/x**3
