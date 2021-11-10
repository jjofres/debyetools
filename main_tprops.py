import numpy as np
from potentials import BM as BM3
class Anharmonicity:
    def __init__(self,s0,s1,s2):
        self.s0=s0
        self.s1=s1
        self.s2=s2
    def A(self,V):
        return self.s0 + self.s1*V + self.s2*V**2
    def dAdV_T(self,V):
        return 2*V*self.s2+self.s1
    def d2AdV2_T(self,V):
        return 2*self.s2
    def d3AdV3_T(self,V):
        return 0
    def d4AdV4_T(self,V):
        return 0

    def E(self,T,V):
        return 1/2*self.A(V)*T**2
    def S(self,T,V):
        return self.A(V)*T
    def F(self,T,V):
        return -1/2*self.A(V)*T**2
    def d2FdT2_V(self,T,V):
        return -self.A(V)
    def d2FdV2_T(self,T,V):
        return -self.d2AdV2_T(V)*T**2/2
    def d3FdV3_T(self,T,V):
        return -self.d3AdV3_T(V)*T**2/2
    def d4FdV4_T(self,T,V):
        return -self.d4AdV4_T(V)*T**2/2
    def d2FdVdT(self,T,V):
        return -self.dAdV_T(V)*T
    def d3FdV2dT(self,T,V):
        return -self.d2AdV2_T(V)*T
    def d3FdVdT2(self,T,V):
        return -self.dAdV_T(V)
class Defects:
    def __init__(self,Evac00,Svac00,Tm,a,P2,V0):
        self.Evac00 = Evac00
        self.Svac00 = Svac00
        self.Svac0 = Svac00*kB
        self.Evac0 = Evac00*kB*Tm
        self.Tm=Tm
        self.a = a
        self.P2 = P2
        self.V0=V0

    def Svac(self,V):
        return self.Svac0
    def dSvacdV_T(self,V):
        return 0
    def d2SvacdV2_T(self,V):
        return 0
    def d3SvacdV3_T(self,V):
        return 0
    def d4SvacdV4_T(self,V):
        return 0
    def Evac(self,V):
        return self.Evac0 - self.V0*self.a*(V - self.V0)*self.P2/(NAv*V)
    def dEvacdV_T(self,V):
        return -self.V0*self.a*self.P2/(NAv*V)+self.V0*self.a*(V-self.V0)*self.P2/(NAv*V**2)
    def d2EvacdV2_T(self,V):
        return 2*self.V0*self.a*self.P2/(NAv*V**2)-2*self.V0*self.a*(V-self.V0)*self.P2/(NAv*V**3)
    def d3EvacdV3_T(self,V):
        return -6*self.V0*self.a*self.P2/(NAv*V**3)+6*self.V0*self.a*(V-self.V0)*self.P2/(NAv*V**4)
    def d4EvacdV4_T(self,V):
        return 24*self.V0*self.a*self.P2/(NAv*V**4)-24*self.V0*self.a*(V-self.V0)*self.P2/(NAv*V**5)

    def E(self,T,V):
        return self.Evac(V)*NAv*np.exp(self.Svac(V)/kB - self.Evac(V)/(kB*T))
    def S(self,T,V):
        return (T*kB+self.Evac(V))*NAv*np.exp(self.Svac(V)/kB - self.Evac(V)/(kB*T))/T
    def F(self,T,V):
        return -NAv*T*kB*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))
    def d2FdT2_V(self,T,V):
        return -NAv*self.Evac(V)**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T**3*kB)
    def d2FdV2_T(self,T,V):
        return -(-(self.d2EvacdV2_T(V))*T*kB+(self.d2SvacdV2_T(V))*T**2*kB+((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))**2)*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))*NAv/(T*kB)
    def d3FdV3_T(self,T,V):
        return -NAv*(self.d3SvacdV3_T(V)*T-self.d3EvacdV3_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-3*NAv*(self.d2SvacdV2_T(V)*T-self.d2EvacdV2_T(V))*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)-NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))**3*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T**2*kB**2)
    def d4FdV4_T(self,T,V):
        return -NAv*(self.d4SvacdV4_T(V)*T-self.d4EvacdV4_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-4*NAv*(self.d3SvacdV3_T(V)*T-self.d3EvacdV3_T(V))*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)-3*NAv*(self.d2SvacdV2_T(V)*T-self.d2EvacdV2_T(V))**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)

    def d2FdVdT(self,T,V):
        return -np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))*(T*(T*kB+self.Evac(V))*(self.dSvacdV_T(V))-(self.dEvacdV_T(V))*self.Evac(V))*NAv/(T**2*kB)
    def d3FdV2dT(self,T,V):
        return -NAv*(self.d2SvacdV2_T(V))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*((self.d2SvacdV2_T(V))*T-(self.d2EvacdV2_T(V)))*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-2*NAv*((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))*(self.dSvacdV_T(V))/(T*kB)+NAv*((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T**2*kB)-NAv*((self.dSvacdV_T(V))*T-(self.dEvacdV_T(V)))**2*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))/(T*kB)
    def d3FdVdT2(self,T,V):
        return -2*NAv*self.dSvacdV_T(V)*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*(-2*self.Svac(V)/(T**2*kB)+(2*(self.Svac(V)*T-self.Evac(V)))/(T**3*kB))*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))-NAv*(self.dSvacdV_T(V)*T-self.dEvacdV_T(V))*(self.Svac(V)/(T*kB)-(self.Svac(V)*T-self.Evac(V))/(T**2*kB))**2*np.exp((self.Svac(V)*T-self.Evac(V))/(T*kB))

class intAnharmonicity:
    def __init__(self,a0=0,m0=1,V0=1):
        self.a0 = a0
        self.m0 = m0
        self.V0 = V0
    def an(self,V):
         return self.a0*(V/self.V0)**self.m0
    def Anh(self,T,V):
        self.an_val=self.an(V)
        self.Anh_val = np.exp(1/2*self.an_val*T)
        return self.Anh_val
    def dAnhdT_V(self):
        self.dAnhdT_V_val = (1/2)*self.an_val*self.Anh_val
        return self.dAnhdT_V_val
    def d2AnhdT2_V(self):
        self.d2AnhdT2_V_val = (1/2)*self.an_val*self.dAnhdT_V_val
        return self.d2AnhdT2_V_val
    def d3AnhdT3_V(self):
        self.d3AnhdT3_V_val = (1/2)*self.an_val*self.d2AnhdT2_V_val
        return self.d3AnhdT3_V_val
    def d4AnhdT4_V(self):
        self.d4AnhdT4_V_val = (1/2)*self.an_val*self.d3AnhdT3_V_val
        return self.d4AnhdT4_V_val

    def dAnhdV_T(self,T,V):
        self.dAnhdV_T_val = self.m0*T*self.an_val*self.Anh_val/(2*V)
        return self.dAnhdV_T_val
    def d2AnhdV2_T(self,T,V):
        self.d2AnhdV2_T_val = self.dAnhdV_T_val*(T*self.an_val*self.m0+2*self.m0-2)/(2*V)
        return self.d2AnhdV2_T_val
    def d3AnhdV3_T(self,T,V):
        self.d3AnhdV3_T_val= self.dAnhdV_T_val*(T**2*self.an_val**2*self.m0**2+6*T*self.an_val*self.m0**2-6*T*self.an_val*self.m0+4*self.m0**2-12*self.m0+8)/(4*V**2)
        return self.d3AnhdV3_T_val

    def d4AnhdV4_T(self,T,V):
        self.d4AnhdT4_V_val = self.dAnhdV_T_val*(T**3*self.an_val**3*self.m0**3+12*T**2*self.an_val**2*self.m0**3-12*T**2*self.an_val**2*self.m0**2+28*T*self.an_val*self.m0**3-72*T*self.an_val*self.m0**2+44*T*self.an_val*self.m0+8*self.m0**3-48*self.m0**2+88*self.m0-48)/(8*V**3)
        return self.d4AnhdT4_V_val
    def d2AnhdVdT(self,T):
        self.d2AnhdVdT_val = self.dAnhdV_T_val*(1/T+self.an_val/2)
        return self.d2AnhdVdT_val
    def d3AnhdVdT2(self,T):
        self.d3AnhdVdT2_val = self.dAnhdV_T_val*self.an_val*(1/T+self.an_val/4)
        return self.d3AnhdVdT2_val
    def d3AnhdV2dT(self,T,V):
        self.d3AnhdV2dT_val = self.dAnhdV_T_val/V*(self.m0/T - 1/T + 3/2*self.an_val*self.m0 - self.an_val/2 + self.an_val**2*self.m0*T/4)
        return self.d3AnhdV2dT_val

class Electronic:
    def __init__(self,r,q0,q1,q2,q3):
        self.r=r
        self.q0=q0
        self.q1=q1
        self.q2=q2
        self.q3=q3

    def NfV(self,V):
        return self.q0*V**0 + self.q1*V**1 + self.q2*V**2 + self.q3*V**3
    def dNfVdV_T(self,V):
        return 3*V**2*self.q3+2*V*self.q2+self.q1
    def d2NfVdV2_T(self,V):
        return 6*V*self.q3+2*self.q2
    def d3NfVdV3_T(self,V):
        return 6*self.q3
    def d4NfVdV4_T(self,V):
        return 0

    def E(self,T,V):
        return (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.NfV(V)/(0.160218e-18)
    def S(self,T,V):
        return (2/6)*np.pi**2*NAv*self.r*kB**2*T*self.NfV(V)/(0.160218e-18)
    def F(self,T,V):
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.NfV(V)/(0.160218e-18)
    def d2FdT2_V(self,T,V):
        return - 2*np.pi**2*NAv*self.r*kB**2*self.NfV(V)*(1/6)/(0.160218e-18)
    def d2FdV2_T(self,T,V):
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.d2NfVdV2_T(V)/(0.160218e-18)
    def d3FdV3_T(self,T,V):
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.d3NfVdV3_T(V)/(0.160218e-18)
    def d4FdV4_T(self,T,V):
        return - (1/6)*np.pi**2*NAv*self.r*kB**2*T**2*self.d4NfVdV4_T(V)/(0.160218e-18)

    def d2FdVdT(self,T,V):
        return -2*np.pi**2*NAv*self.r*kB**2*T*self.dNfVdV_T(V)*(1/6)/(0.160218e-18)
    def d3FdV2dT(self,T,V):
        return -2*np.pi**2*NAv*self.r*kB**2*T*self.d2NfVdV2_T(V)*(1/6)/(0.160218e-18)
    def d3FdVdT2(self,T,V):
        return -2*np.pi**2*NAv*self.r*kB**2*self.dNfVdV_T(V)*(1/6)/(0.160218e-18)

NAv  = 0.6022140857e24
hbar = 0.1054571800e-33
kB   = 0.138064852e-22

def lncomplex(_z):
    """Complex natural logaritm"""
    x=np.real(_z)
    _y=np.imag(_z)
    _r=np.abs(_z)
    return complex(np.log(_r),np.arctan2(_y, x))

A03 = (np.pi**4)/5
A10 = (8*np.pi**4)/15 -49
A11 = (8*np.pi**4)/5 - 219/2 - 12*A10
A12 = (16*np.pi**4)/5 - 117 - 36*A10 - 8*A11
A13 = (16*np.pi**4)/5 - 39 - 24*A10 - 12*A11 - 4*A12
A20 = (4*np.pi**4)/15 - 1 - A10 - A11 - 1/2*A12 - 1/6*A13
A21 = (2*np.pi**4)/5 - A11 - A12 - 1/2*A13
A22 = (2*np.pi**4)/5 - A12 - A13
A23 = (np.pi**4)/5 - A13
def K_24(x):
    return A03*x**(-3) - (A10 + A11*x**(-1) + A12*x**(-2) + A13*x**(-3))*np.exp(-1*x) - (A20 + A21*x**(-1) + A22*x**(-2) + A23*x**(-3))*np.exp(-2*x)

def dK_24(x):
    return -3*A03/x**4-(-A11/x**2-2*A12/x**3-3*A13/x**4)*np.exp(-x)+(A10+A11/x+A12/x**2+A13/x**3)*np.exp(-x)-(-A21/x**2-2*A22/x**3-3*A23/x**4)*np.exp(-2*x)+(2*(A20+A21/x+A22/x**2+A23/x**3))*np.exp(-2*x)

def D_3(x):
    if type(x)==np.ndarray:
        return np.array([D_3(xi) for xi in x])
    return K_24(x)
    # # if x<=1:
    if x >=499.99999999999966:
        return 1.5585456848144562e-07
    elif x>=1.579779e+01:
        return np.pi**4/(5*x**3)
    ex=np.exp(x)
    if x <=0.1111111111111111:
        return 0.958950526584995
    else:
        d1, d2, d3, d4, d5, d6 = -np.pi**4/(5*x**3), -3*x*(1/4), np.real(+3*lncomplex(-ex+1)),np.real(+9*mp.fp.polylog(2,ex)/x), np.real(-18*mp.fp.polylog(3,ex)/x**2), np.real(+18*mp.fp.polylog(4,ex)/x**3)
        return d1+d2+d3+d4+d5+d6
def dD_3dx(x, D3):
    if type(x)==np.ndarray:
        return np.array([dD_3dx(xi,D3i) for xi,D3i in zip(x,D3)])
    return dK_24(x)

    if x >= 709.782712893384:
        return -2.3027630998995085e-10
    return np.real(3./(np.exp(x)-1.)-3.*D3/x)

def d2D_3dx2(x, D3, dD3dx):
    if type(x)==np.ndarray:
        return np.array([d2D_3dx2(xi,D3i,dD3dxi) for xi,D3i,dD3dxi in zip(x,D3, dD3dx)])
    if x >=354.89135644669:
        exp_exp2=7.458340731215135e-155
    else:
        exp_exp2=(np.exp(x)/(np.exp(x)-1.)**2.)
    return np.real(-3.*exp_exp2+-3.*dD3dx/x+3.*D3/x**2)

def d3D_3dx3(x, _D3, _dD3dx,_d2D3dx2):
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
    return (- 3*exp_exp2 + 6.*exp_exp2*exp_x/(exp_x-1.) - 3.*_d2D3dx2/x+6*_dD3dx/x**2 - 6.*_D3/x**3)


class nDeb:
    def __init__(self, nu, r, m, Tmelting, a0, m0, V0, pEOS, q0,q1,q2,q3,Evac00,Svac00,Tm,a,P2,s0,s1,s2):
        self.nu, self.r, self.m = nu, r, m
        self.kv = (2./3.*((2. + 2.*nu)/(3.-6.*nu))**(3./2.) + 1./3.*((1. + nu)/(3. - 3.*nu))**(3./2.))**(-1./3.)

        self.anh = Anharmonicity(s0,s1,s2)
        self.intanh = intAnharmonicity(a0,m0,V0)
        self.el = Electronic(r,q0,q1,q2,q3)
        self.deff = Defects(Evac00,Svac00,Tm,a,P2,V0)

        self.EOS = BM3()
        self.EOS.pEOS = pEOS

        self.xDcte = hbar*6**(1/3.)*(np.pi**2*NAv*r)**(1/3.)

    def Cp(self, T, V):
        nu, r, m = self.nu,self.r,self.m

        kv = self.kv

        Anh         = self.intanh.Anh(T,V)
        dAnhdT_V    = self.intanh.dAnhdT_V()
        d2AnhdT2_V  = self.intanh.d2AnhdT2_V()
        d3AnhdT3_V  = self.intanh.d3AnhdT3_V()

        dAnhdV_T    = self.intanh.dAnhdV_T(T,V)
        d2AnhdV2_T  = self.intanh.d2AnhdV2_T(T,V)
        d3AnhdV3_T  = self.intanh.d3AnhdV3_T(T,V)
        d4AnhdV4_T  = self.intanh.d4AnhdV4_T(T,V)

        d2AnhdVdT   = self.intanh.d2AnhdVdT(T)
        d3AnhdVdT2  = self.intanh.d3AnhdVdT2(T)
        d3AnhdV2dT  = self.intanh.d3AnhdV2dT(T,V)

        dE0dV_T = self.EOS.dE0dV_T(V)
        d2E0dV2_T = self.EOS.d2E0dV2_T(V)
        d3E0dV3_T = self.EOS.d3E0dV3_T(V)
        d4E0dV4_T = self.EOS.d4E0dV4_T(V)
        d5E0dV5_T = self.EOS.d5E0dV5_T(V)
        d6E0dV6_T = self.EOS.d6E0dV6_T(V)
        d2E0dT2_V = 0
        d2E0dVdT  = 0
        d3E0dV2dT  = 0
        d3E0dVdT2  = 0

        P0   = - dE0dV_T
        dP0dV   = - d2E0dV2_T
        d2P0dV2 = - d3E0dV3_T
        d3P0dV3 = - d4E0dV4_T
        d4P0dV4 = - d5E0dV5_T
        d5P0dV5 = - d6E0dV6_T

        vDPrm  = - dP0dV/(r*m)
        vDsqrt = np.sqrt( vDPrm)
        vD      = kv*V*vDsqrt
        dvDdV   = kv*vDsqrt-kv*V*d2P0dV2/(2*vDsqrt*r*m)
        d2vDdV2 = -kv*d2P0dV2/(vDsqrt*r*m)-kv*V*d2P0dV2**2/(4*(vDPrm)**(3/2)*r**2*m**2)-kv*V*d3P0dV3/(2*vDsqrt*r*m)
        d3vDdV3 = -3*kv*d2P0dV2**2/(4*(vDPrm)**(3/2)*r**2*m**2)-3*kv*d3P0dV3/(2*vDsqrt*r*m)-3*kv*V*d2P0dV2**3/(8*(vDPrm)**(5/2)*r**3*m**3)-3*kv*V*d2P0dV2*d3P0dV3/(4*(vDPrm)**(3/2)*r**2*m**2)-kv*V*d4P0dV4/(2*vDsqrt*r*m)
        d4vDdV4 = -3*kv*(d2P0dV2)**3/(2*(-dP0dV/(r*m))**(5/2)*r**3*m**3)-3*kv*(d2P0dV2)*(d3P0dV3)/((-dP0dV/(r*m))**(3/2)*r**2*m**2)-2*kv*(d4P0dV4)/(np.sqrt(-dP0dV/(r*m))*r*m)-15*kv*V*(d2P0dV2)**4/(16*(-dP0dV/(r*m))**(7/2)*r**4*m**4)-9*kv*V*(d2P0dV2)**2*(d3P0dV3)/(4*(-dP0dV/(r*m))**(5/2)*r**3*m**3)-3*kv*V*(d3P0dV3)**2/(4*(-dP0dV/(r*m))**(3/2)*r**2*m**2)-kv*V*(d2P0dV2)*(d4P0dV4)/((-dP0dV/(r*m))**(3/2)*r**2*m**2)-kv*V*(d5P0dV5)/(2*np.sqrt(-dP0dV/(r*m))*r*m)

        xDcte = self.xDcte
        xD      = xDcte*(1/V)**(1/3.)/kB
        dxDdV   = - xDcte/(3*kB*V**(4/3.))
        d2xDdV2 = 4*xDcte/(9*kB*V**(7/3.))
        d3xDdV3 = -28*xDcte/(27*V**(10/3)*kB)
        d4xDdV4 = 280*xDcte/(81*V**(13/3)*kB)

        tD        = xD*vD*Anh
        dtDdT_V   = xD*vD*dAnhdT_V
        d2tDdT2_V = xD*vD*d2AnhdT2_V
        d3tDdT3_V = xD*vD*d3AnhdT3_V
        dtDdV_T   = dxDdV*vD*Anh+xD*dvDdV*Anh+xD*vD*dAnhdV_T
        d2tDdV2_T = d2xDdV2*vD*Anh+2*dxDdV*dvDdV*Anh+2*dxDdV*vD*dAnhdV_T+xD*d2vDdV2*Anh+2*xD*dvDdV*dAnhdV_T+xD*vD*d2AnhdV2_T
        d3tDdV3_T = d3xDdV3*vD*Anh+3*d2xDdV2*dvDdV*Anh+3*d2xDdV2*vD*dAnhdV_T+3*dxDdV*d2vDdV2*Anh+6*dxDdV*dvDdV*dAnhdV_T+3*dxDdV*vD*d2AnhdV2_T+xD*d3vDdV3*Anh+3*xD*d2vDdV2*dAnhdV_T+3*xD*dvDdV*d2AnhdV2_T+xD*vD*d3AnhdV3_T
        d4tDdV4_T = xD*vD*d4AnhdV4_T+d4xDdV4*vD*Anh+4*d3xDdV3*dvDdV*Anh+4*d3xDdV3*vD*dAnhdV_T+6*d2xDdV2*d2vDdV2*Anh+12*d2xDdV2*dvDdV*dAnhdV_T+6*d2xDdV2*vD*d2AnhdV2_T+4*dxDdV*d3vDdV3*Anh+12*dxDdV*d2vDdV2*dAnhdV_T+12*dxDdV*dvDdV*d2AnhdV2_T+4*dxDdV*vD*d3AnhdV3_T+xD*d4vDdV4*Anh+4*xD*d3vDdV3*dAnhdV_T+6*xD*d2vDdV2*d2AnhdV2_T+4*xD*dvDdV*d3AnhdV3_T
        d2tDdVdT  = dxDdV*vD*dAnhdT_V+xD*dvDdV*dAnhdT_V+xD*vD*d2AnhdVdT
        d3tDdVdT2 = dxDdV*vD*d2AnhdT2_V+xD*dvDdV*d2AnhdT2_V+xD*vD*d3AnhdVdT2
        d3tDdV2dT = d2xDdV2*vD*dAnhdT_V+2*dxDdV*dvDdV*dAnhdT_V+2*dxDdV*vD*d2AnhdVdT+xD*d2vDdV2*dAnhdT_V+2*xD*dvDdV*d2AnhdVdT+xD*vD*d3AnhdV2dT

        x = min(tD/T,650)#np.array([min(tDi/Ti,650) for tDi, Ti in zip(tD,T)])

        D3      = D_3(x)
        dD3dx   = dD_3dx(x,D3)
        d2D3dx2 = d2D_3dx2(x,D3,dD3dx)
        d3D3dx3 = d3D_3dx3(x,D3,dD3dx,d2D3dx2)

        ex = np.exp(x)
        d2FvibdT2_V = 3*r*NAv*((ex-1)*T*(T**2*d2tDdT2_V*tD-4*(dtDdT_V*T-tD)**2)*D3+3*tD*(d2tDdT2_V*tD*ex*T**2-T**2*d2tDdT2_V*tD+8*(dtDdT_V*T-tD)**2)*(1/8))*kB/(tD**2*(ex-1)*T**2)
        d2FvibdV2_T = 3*r*NAv*kB*(8*dtDdV_T**2*tD*dD3dx-8*dtDdV_T**2*D3*T+8*d2tDdV2_T*D3*tD*T+3*d2tDdV2_T*tD**2)/(8*tD**2)
        d3FvibdV3_T = 3*r*(T**2*(d3tDdV3_T*tD**2-3*dtDdV_T*d2tDdV2_T*tD+2*dtDdV_T**3)*D3+(3*dtDdV_T*d2tDdV2_T*T*tD**2-2*dtDdV_T**3*T*tD)*dD3dx+d2D3dx2*dtDdV_T**3*tD**2+3*d3tDdV3_T*tD**3*T*(1/8))*kB*NAv/(T*tD**3)
        d4FvibdV4_T = -12*r*(T**3*(-(1/4)*d4tDdV4_T*tD**3+(d3tDdV3_T*dtDdV_T+3*d2tDdV2_T**2*(1/4))*tD**2-3*dtDdV_T**2*d2tDdV2_T*tD+3*dtDdV_T**4*(1/2))*D3-tD*(T**2*((d3tDdV3_T*dtDdV_T+3*d2tDdV2_T**2*(1/4))*tD**2-3*dtDdV_T**2*d2tDdV2_T*tD+3*dtDdV_T**4*(1/2))*dD3dx+(1/32)*(3*((16*dtDdV_T**2*d2tDdV2_T*tD*T-8*dtDdV_T**4*T)*d2D3dx2+tD*(8*d3D3dx3*dtDdV_T**4*(1/3)+d4tDdV4_T*tD*T**2)))*tD))*kB*NAv/(T**2*tD**4)
        d2FvibdVdT  = 3*r*(dD3dx*(dtDdT_V/T-tD/T**2)*T+D3+3*dtDdT_V*(1/8))*kB*dtDdV_T*NAv/tD+3*r*(D3*T+3*tD*(1/8))*kB*d2tDdVdT*NAv/tD-3*r*(D3*T+3*tD*(1/8))*kB*dtDdV_T*NAv*dtDdT_V/tD**2
        d3FvibdV2dT = -3*r*(T**2*((-T*d3tDdV2dT-d2tDdV2_T)*tD**2+(T*d2tDdV2_T*dtDdT_V+2*T*dtDdV_T*d2tDdVdT+dtDdV_T**2)*tD-2*T*dtDdT_V*dtDdV_T**2)*D3-tD*((-d2tDdV2_T*tD**2+(T*d2tDdV2_T*dtDdT_V+2*T*dtDdV_T*d2tDdVdT+dtDdV_T**2)*tD-2*T*dtDdT_V*dtDdV_T**2)*T*dD3dx+3*tD*(8*dtDdV_T**2*(T*dtDdT_V-tD)*d2D3dx2*(1/3)+tD*d3tDdV2dT*T**2)*(1/8)))*kB*NAv/(T**2*tD**3)
        d3FvibdVdT2 = -(6*(T**3*((-(1/2)*d3tDdVdT2*T-d2tDdVdT)*tD**2+(((1/2)*d2tDdT2_V*T+dtDdT_V)*dtDdV_T+dtDdT_V*d2tDdVdT*T)*tD-dtDdT_V**2*dtDdV_T*T)*D3-(T**2*(-tD**2*d2tDdVdT+(((1/2)*d2tDdT2_V*T+dtDdT_V)*dtDdV_T+dtDdT_V*d2tDdVdT*T)*tD-dtDdT_V**2*dtDdV_T*T)*dD3dx+(1/16)*(3*(8*dtDdV_T*(T*dtDdT_V-tD)**2*d2D3dx2*(1/3)+tD*d3tDdVdT2*T**3))*tD)*tD))*r*kB*NAv/(T**3*tD**3)

        d2FeldT2_V  = self.el.d2FdT2_V(T,V)
        d2FeldV2_T  = self.el.d2FdV2_T(T,V)
        d3FeldV3_T  = self.el.d3FdV3_T(T,V)
        d4FeldV4_T  = self.el.d4FdV4_T(T,V)
        d2FeldVdT   = self.el.d2FdVdT(T,V)
        d3FeldV2dT   = self.el.d3FdV2dT(T,V)
        d3FeldVdT2   = self.el.d3FdVdT2(T,V)

        d2FdefdT2_V = self.deff.d2FdT2_V(T,V)
        d2FdefdV2_T = self.deff.d2FdV2_T(T,V)
        d3FdefdV3_T = self.deff.d3FdV3_T(T,V)
        d4FdefdV4_T = self.deff.d4FdV4_T(T,V)
        d2FdefdVdT  = self.deff.d2FdVdT(T,V)
        d3FdefdV2dT  = self.deff.d3FdV2dT(T,V)
        d3FdefdVdT2  = self.deff.d3FdVdT2(T,V)

        d2FadT2_V   = self.anh.d2FdT2_V(T,V)
        d2FadV2_T   = self.anh.d2FdV2_T(T,V)
        d3FadV3_T   = self.anh.d3FdV3_T(T,V)
        d4FadV4_T   = self.anh.d4FdV4_T(T,V)
        d2FadVdT    = self.anh.d2FdVdT(T,V)
        d3FadV2dT    = self.anh.d3FdV2dT(T,V)
        d3FadVdT2    = self.anh.d3FdVdT2(T,V)

        d2FdT2_V = d2E0dT2_V + d2FvibdT2_V + d2FeldT2_V + d2FdefdT2_V + d2FadT2_V
        d2FdV2_T = d2E0dV2_T + d2FvibdV2_T + d2FeldV2_T + d2FdefdV2_T + d2FadV2_T
        d3FdV3_T = d3E0dV3_T + d3FvibdV3_T + d3FeldV3_T + d3FdefdV3_T + d3FadV3_T
        d4FdV4_T = d4E0dV4_T + d4FvibdV4_T + d4FeldV4_T + d4FdefdV4_T + d4FadV4_T
        d2FdVdT  = d2E0dVdT + d2FvibdVdT + d2FeldVdT + d2FdefdVdT + d2FadVdT
        d3FdV2dT  = d3E0dV2dT + d3FvibdV2dT + d3FeldV2dT + d3FdefdV2dT + d3FadV2dT
        d3FdVdT2  = d3E0dVdT2 + d3FvibdVdT2 + d3FeldVdT2 + d3FdefdVdT2 + d3FadVdT2

        g    = -V/(tD)*dtDdV_T
        dPdV_T = - d2FdV2_T
        d2PdV2_T = - d3FdV3_T
        d3PdV3_T = - d4FdV4_T
        Kt = - V*dPdV_T
        dKtdV_T = - dPdV_T - V*d2PdV2_T
        dKtdP_T = dKtdV_T/dPdV_T
        d2KtdV2_T = -2*d2PdV2_T-V*d3PdV3_T
        d2KtdP2_T = (d2KtdV2_T/dPdV_T-dKtdV_T*d2PdV2_T/dPdV_T**2)/dPdV_T
        Ktp = dKtdP_T
        Ktpp = d2KtdP2_T
        Cv = -T*d2FdT2_V
        dPdT_V = - d2FdVdT
        dVdT_P = - dPdT_V/dPdV_T
        a  = 1/V*dVdT_P

        return -T*( d2FdT2_V - (d2FdVdT)**2 / d2FdV2_T)

nu, r, m = 0.31681, 1, 0.026981500000000002
Tmelting = 933
pEOS = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
a0, m0, V0 = 0, 1, pEOS[1]
q0,q1,q2,q3 = [3.8027e-01, -1.8875e-02, 5.3071e-04, -7.0101e-06]
Evac00,Svac00,a,P2 = 8.46, 1.69,0.1,pEOS[2]
s0,s1,s2 = 0,0,0
ndeb_BM = nDeb(nu, r, m, Tmelting, a0, m0, V0, pEOS, q0,q1,q2,q3, Evac00,Svac00,Tmelting,a,P2,s0,s1,s2)

T,V = 9.3300000000000E+02,1.0779013128600E-05


print(ndeb_BM.Cp(T,V)) #3.3249653530900E+01
