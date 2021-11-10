import numpy as np
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
