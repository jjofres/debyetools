import numpy as np
from scipy.optimize import least_squares

NAv  = 0.6022140857e24
kB   = 0.138064852e-22

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

def fit_electronic(Vs, p_el,E,N,Ef):
    q00,q10,q20,q30 = p_el

    V = Vs
    ix_V0=10
    EfV0 = float(Ef[ix_V0])
    ixs=[i for i,x in enumerate(E[ix_V0]) if x>=Ef[ix_V0]]
    E1 = float(E[ix_V0][ixs[0]-1])
    E2 = float(E[ix_V0][ixs[0]])
    N1 = float(N[ix_V0][ixs[0]-1])
    N2 = float(N[ix_V0][ixs[0]])
    NfV0 = (EfV0 - E1)*(N2 - N1)/(E2 - E1) + N1
    NfV = np.array([NfV0*np.sqrt(ef/EfV0) for ef in Ef][8:-1])
    P2=least_squares(NfV2m,[6e-01,-2e+04,1e7,1e11], args=(V[8:-1], NfV))['x']

    return P2
