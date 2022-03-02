import numpy as np
from debyetools.debfunct import D_3, dD_3dx, d2D_3dx2, d3D_3dx3
hbar = 0.1054571800e-33
NAv  = 0.6022140857e24
kB   = 0.138064852e-22
r = 1
class Vibrational:
    """
    Instanceiate the vibrational contribution to the free energy and its derivatives for the calculation of the thermodynamic properties.

    :param float nu: Poisson's ratio.
    :param potential_instance EOS_obj: Equation of state object.
    :param float m: Mass in Kg/mol-at.
    :param intAnharmonicity_instance intanh: Intrinsic anharmonicity object.
    """
    def __init__(self, nu, EOS_obj, m, intanh):
        self.EOS = EOS_obj
        self.kv = (2./3.*((2. + 2.*nu)/(3.-6.*nu))**(3./2.) + 1./3.*((1. + nu)/(3. - 3.*nu))**(3./2.))**(-1./3.)
        self.m = m
        self.intanh = intanh

        self.xDcte = hbar*6**(1/3.)*(np.pi**2*NAv*r)**(1/3.)

    def set_int_anh(self, T, V):
        """
        Calculates intrinsic anharmonicity correction to the Debye temperature and its derivatibes.

        :param float T: Temperature.
        :param float V: Volume.
        """
        self.Anh         = self.intanh.Anh(T,V)
        self.dAnhdT_V    = self.intanh.dAnhdT_V()
        self.dAnhdV_T    = self.intanh.dAnhdV_T(T,V)
        self.d2AnhdVdT   = self.intanh.d2AnhdVdT(T)
        self.d2AnhdV2_T  = self.intanh.d2AnhdV2_T(T,V)
        self.d2AnhdT2_V  = self.intanh.d2AnhdT2_V()
        self.d3AnhdV2dT  = self.intanh.d3AnhdV2dT(T,V)
        self.d3AnhdVdT2  = self.intanh.d3AnhdVdT2(T)
        self.d3AnhdV3_T  = self.intanh.d3AnhdV3_T(T,V)
        self.d4AnhdV4_T  = self.intanh.d4AnhdV4_T(T,V)

    def set_theta(self, T, V, V0_DM, a_DM, b_DM):
        """
        Calculates the Debye Temperature and its derivatives.

        :param float T: Temperature.
        :param float V: Volume.
        """
        kv = self.kv
        m = self.m
        dE0dV_T = self.EOS.dE0dV_T(V)
        d2E0dV2_T = self.EOS.d2E0dV2_T(V)
        d3E0dV3_T = self.EOS.d3E0dV3_T(V)
        d4E0dV4_T = self.EOS.d4E0dV4_T(V)
        d5E0dV5_T = self.EOS.d5E0dV5_T(V)
        d6E0dV6_T = self.EOS.d6E0dV6_T(V)
        P0      = - dE0dV_T
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
        xD      = self.xDcte*(1/V)**(1/3.)/kB
        dxDdV   = - self.xDcte/(3*kB*V**(4/3.))
        d2xDdV2 = 4*self.xDcte/(9*kB*V**(7/3.))
        d3xDdV3 = -28*self.xDcte/(27*V**(10/3)*kB)
        d4xDdV4 = 280*self.xDcte/(81*V**(13/3)*kB)

        B0_DM = V0_DM*self.EOS.d2E0dV2_T(V0_DM)
        DM = 1#(V*d2E0dV2_T/B0_DM)**b_DM/(V/V0_DM)**a_DM
        dDMdV = 0#V0_DM**a_DM*(-d2E0dV2_T**b_DM*(-b_DM+a_DM)*V**(b_DM-1-a_DM)+V**(b_DM-a_DM)*d2E0dV2_T**(b_DM-1)*(d3E0dV3_T)*b_DM)*B0_DM**(-b_DM)
        d2DMdV2 = 0#V0_DM**a_DM*B0_DM**(-b_DM)*(-2*(d3E0dV3_T)*b_DM*d2E0dV2_T**(b_DM-1)*(-b_DM+a_DM)*V**(b_DM-1-a_DM)+d2E0dV2_T**b_DM*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-2-a_DM)+V**(b_DM-a_DM)*(d2E0dV2_T**(b_DM-1)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-2)*(b_DM-1))*b_DM)
        d3DMdV3 = 0#-V0_DM**a_DM*B0_DM**(-b_DM)*(d2E0dV2_T**b_DM*(-b_DM+2+a_DM)*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-a_DM-3)-3*b_DM*(-(d2E0dV2_T**(b_DM-1)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-2)*(b_DM-1))*(-b_DM+a_DM)*V**(b_DM-1-a_DM)+(d3E0dV3_T)*d2E0dV2_T**(b_DM-1)*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-2-a_DM)+(1/3)*V**(b_DM-a_DM)*(d2E0dV2_T**(b_DM-1)*(d5E0dV5_T)+(d3E0dV3_T)*(3*d2E0dV2_T**(b_DM-2)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-3)*(b_DM-2))*(b_DM-1))))
        d4DMdV4 = 0#(d2E0dV2_T**b_DM*(-b_DM+a_DM)*(-b_DM+a_DM+3)*(-b_DM+2+a_DM)*(-b_DM+1+a_DM)*V**(b_DM-4-a_DM)+6*b_DM*((d2E0dV2_T**(b_DM-1)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-2)*(b_DM-1))*(-b_DM+a_DM)*(-b_DM+1+a_DM)*V**(b_DM-2-a_DM)-(1/3)*(2*(d2E0dV2_T**(b_DM-1)*(d5E0dV5_T)+(d3E0dV3_T)*(3*d2E0dV2_T**(b_DM-2)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-3)*(b_DM-2))*(b_DM-1)))*(-b_DM+a_DM)*V**(b_DM-1-a_DM)-2*(d3E0dV3_T)*d2E0dV2_T**(b_DM-1)*(-b_DM+2+a_DM)*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-a_DM-3)*(1/3)+(1/6)*(d2E0dV2_T**(b_DM-1)*(d6E0dV6_T)+(4*(d3E0dV3_T)*d2E0dV2_T**(b_DM-2)*(d5E0dV5_T)+3*d2E0dV2_T**(b_DM-2)*(d4E0dV4_T)**2+(6*d2E0dV2_T**(b_DM-3)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-4)*(b_DM-3))*(b_DM-2)*(d3E0dV3_T)**2)*(b_DM-1))*V**(b_DM-a_DM)))*V0_DM**a_DM*B0_DM**(-b_DM)

        self.tD        = xD*vD*DM*self.Anh

        B0_DM = V0_DM*self.EOS.d2E0dV2_T(V0_DM)
        DM = (V*d2E0dV2_T/B0_DM)**b_DM/(V/V0_DM)**a_DM
        Anh         = self.intanh.Anh(T,V)
        xDcte = self.xDcte
        xD      = xDcte*(1/V)**(1/3.)/kB
        vDPrm  = - dP0dV/(r*m)
        vDsqrt = np.sqrt( vDPrm)
        vD      = kv*V*vDsqrt
        self.tD        = xD*vD*Anh*DM


        self.dtDdV_T   = dxDdV*vD*self.Anh*DM+xD*dvDdV*self.Anh*DM+xD*vD*self.dAnhdV_T*DM+xD*vD*self.Anh*dDMdV
        self.dtDdT_V   = xD*vD*DM*self.dAnhdT_V
        self.d2tDdV2_T = xD*vD*self.d2AnhdV2_T*DM+xD*vD*self.Anh*d2DMdV2+xD*d2vDdV2*self.Anh*DM+d2xDdV2*vD*self.Anh*DM+(2*vD*xD*dDMdV+2*DM*(dxDdV*vD+xD*dvDdV))*self.dAnhdV_T+(2*((dxDdV*vD+xD*dvDdV)*dDMdV+DM*dvDdV*dxDdV))*self.Anh
        self.d2tDdT2_V = xD*vD*DM*self.d2AnhdT2_V
        self.d2tDdVdT  = xD*vD*self.d2AnhdVdT*DM+(vD*xD*dDMdV+DM*(dxDdV*vD+xD*dvDdV))*self.dAnhdT_V
        self.d3tDdV3_T = xD*vD*self.d3AnhdV3_T*DM+xD*vD*self.Anh*d3DMdV3+xD*d3vDdV3*self.Anh*DM+d3xDdV3*vD*self.Anh*DM+(3*vD*xD*dDMdV+3*DM*(dxDdV*vD+xD*dvDdV))*self.d2AnhdV2_T+(3*self.dAnhdV_T*vD*xD+3*self.Anh*(dxDdV*vD+xD*dvDdV))*d2DMdV2+(3*self.dAnhdV_T*DM*xD+3*self.Anh*(DM*dxDdV+xD*dDMdV))*d2vDdV2+(3*self.dAnhdV_T*DM*vD+3*self.Anh*(DM*dvDdV+vD*dDMdV))*d2xDdV2+((6*dxDdV*vD+6*xD*dvDdV)*dDMdV+6*DM*dvDdV*dxDdV)*self.dAnhdV_T+6*dxDdV*dvDdV*self.Anh*dDMdV
        self.d3tDdV2dT = xD*vD*self.d3AnhdV2dT*DM+(2*vD*xD*dDMdV+2*DM*(dxDdV*vD+xD*dvDdV))*self.d2AnhdVdT+(d2DMdV2*vD*xD+d2vDdV2*DM*xD+d2xDdV2*DM*vD+(2*dxDdV*vD+2*xD*dvDdV)*dDMdV+2*DM*dvDdV*dxDdV)*self.dAnhdT_V
        self.d3tDdVdT2 = xD*vD*self.d3AnhdVdT2*DM+(vD*xD*dDMdV+DM*(dxDdV*vD+xD*dvDdV))*self.d2AnhdT2_V
        self.d4tDdV4_T = xD*vD*self.d4AnhdV4_T*DM+xD*vD*self.Anh*d4DMdV4+xD*d4vDdV4*self.Anh*DM+d4xDdV4*vD*self.Anh*DM+(4*vD*xD*dDMdV+4*DM*(dxDdV*vD+xD*dvDdV))*self.d3AnhdV3_T+(4*self.dAnhdV_T*vD*xD+4*self.Anh*(dxDdV*vD+xD*dvDdV))*d3DMdV3+(4*self.dAnhdV_T*DM*xD+4*self.Anh*(DM*dxDdV+xD*dDMdV))*d3vDdV3+(4*self.dAnhdV_T*DM*vD+4*self.Anh*(DM*dvDdV+vD*dDMdV))*d3xDdV3+(6*d2DMdV2*vD*xD+6*d2vDdV2*DM*xD+6*d2xDdV2*DM*vD+(12*dxDdV*vD+12*xD*dvDdV)*dDMdV+12*DM*dvDdV*dxDdV)*self.d2AnhdV2_T+(6*d2vDdV2*xD*self.Anh+ 6*d2xDdV2*vD*self.Anh + (12*dxDdV*vD+12*xD*dvDdV)*self.dAnhdV_T + 12*self.Anh*dvDdV*dxDdV)*d2DMdV2 + (6*d2xDdV2*DM*self.Anh+(12*DM*dxDdV+12*xD*dDMdV)*self.dAnhdV_T+12*self.Anh*dDMdV*dxDdV)*d2vDdV2+((12*DM*dvDdV+12*vD*dDMdV)*self.dAnhdV_T+12*self.Anh*dDMdV*dvDdV)*d2xDdV2+24*dxDdV*dvDdV*self.dAnhdV_T*dDMdV

    def E(self, T, V):
        x = self.tD/T
        D3 = D_3(x)

        return -(3*(self.dtDdT_V*T-self.tD))*r*NAv*kB*(T*D3+3*self.tD*(1/8))/self.tD

    def S(self, T, V):
        x = self.tD/T
        D3 = D_3(x)

        return -3*kB*(np.log(1-np.exp(-self.tD/T))*self.tD+(self.dtDdT_V*T-4*self.tD*(1/3))*D3+3*self.dtDdT_V*self.tD*(1/8))*r*NAv/self.tD
    def Fmin(self, T, V, V0_DM, a_DM, b_DM):
        """
        Vibration Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        """
        d2E0dV2_T_0 = self.EOS.d2E0dV2_T(V0_DM)
        d2E0dV2_T = self.EOS.d2E0dV2_T(V)
        dE0dV_T_0 = self.EOS.dE0dV_T(V0_DM)
        if type(V) == np.ndarray:
            if d2E0dV2_T_0<0:return 1
        kv = self.kv
        m = self.m

        dP0dV_0   = - d2E0dV2_T_0

        B0_DM = V0_DM*self.EOS.d2E0dV2_T(V0_DM)
        DM = (V*d2E0dV2_T/B0_DM)**b_DM/(V/V0_DM)**a_DM
        Anh         = self.intanh.Anh(T,V)
        xDcte = self.xDcte
        xD0      = xDcte*(1/V0_DM)**(1/3.)/kB
        vDPrm0  = - dP0dV_0/(r*m)
        vDsqrt0 = np.sqrt( vDPrm0)
        vD0      = kv*V0_DM*vDsqrt0
        tD0        = xD0*vD0*Anh*DM

        x = tD0/T
        D3 = D_3(x)
        # print(tD/T, tD, T)
        if type(V) is not np.ndarray:
            if x<0.07:return 1
        return 3*r*NAv*kB*(tD0*3/8 + T*np.log(1-np.exp(-x))  - D3*T/3)

    def F(self, T, V, V0_DM, a_DM, b_DM):
        """
        Vibration Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        """
        d2E0dV2_T = self.EOS.d2E0dV2_T(V)
        dE0dV_T = self.EOS.dE0dV_T(V)
        if type(V) == np.ndarray:
            if min(d2E0dV2_T)<0:return 1
        kv = self.kv
        m = self.m

        P0 = - dE0dV_T
        dP0dV   = - d2E0dV2_T

        B0_DM = V0_DM*self.EOS.d2E0dV2_T(V0_DM)
        DM = (V*d2E0dV2_T/B0_DM)**b_DM/(V/V0_DM)**a_DM
        Anh         = self.intanh.Anh(T,V)
        xDcte = self.xDcte
        xD      = xDcte*(1/V)**(1/3.)/kB
        vDPrm  = - dP0dV/(r*m)
        vDsqrt = np.sqrt( vDPrm)
        vD      = kv*V*vDsqrt
        tD        = xD*vD*Anh*DM

        x = tD/T
        D3 = D_3(x)
        # print(tD/T, tD, T)
        if type(V) is not np.ndarray:
            if x<0.07:return 1
        return 3*r*NAv*kB*(tD*3/8 + T*np.log(1-np.exp(-x))  - D3*T/3)

    # def dSdV_T(self, T, V):
    #     _dSvibdV_T =  -3*kB*(_dtDdV_T*np.exp(-_x)*_tD/(_T*(1-np.exp(-_x)))+np.log(1-np.exp(-_x))*_dtDdV_T+(_d2tDdVdT*_T-4*_dtDdV_T*(1/3))*_D3+(_dtDdT_V*_T-4*_tD*(1/3))*_dD3dx*_dtDdV_T/_T+3*_d2tDdVdT*_tD*(1/8)+3*_dtDdT_V*_dtDdV_T*(1/8))*r*NAv/_tD+3*kB*(np.log(1-np.exp(-_x))*_tD+(_dtDdT_V*_T-4*_tD*(1/3))*_D3+3*_dtDdT_V*_tD*(1/8))*r*NAv*_dtDdV_T/_tD**2
    #
    # def dFdV_T(self,T,V):
    #     d2E0dV2_T = self.EOS.d2E0dV2_T
    #     if type(V) == np.ndarray:
    #         if min(d2E0dV2_T)<0:return 1
    #     kv = self.kv
    #     m = self.m
    #
    #     d3E0dV3_T = self.EOS.d3E0dV3_T(V)
    #
    #     dP0dV   = - d2E0dV2_T
    #     d2P0dV2 = - d3E0dV3_T
    #
    #     Anh      = self.intanh.Anh(T,V)
    #     dAnhdV_T = self.intanh.dAnhdV_T(T,V)
    #     xDcte = self.xDcte
    #     xD      = xDcte*(1/V)**(1/3.)/kB
    #     dxDdV   = - self.xDcte/(3*kB*V**(4/3.))
    #     vDPrm  = - dP0dV/(r*m)
    #     vDsqrt = np.sqrt( vDPrm)
    #     vD      = kv*V*vDsqrt
    #     dvDdV   = kv*vDsqrt-kv*V*d2P0dV2/(2*vDsqrt*r*m)
    #     tD        = xD*vD*Anh
    #     dtDdV_T = dxDdV*vD*Anh + xD*dvDdV*Anh + xD*vD*dAnhdV_T
    #
    #     x = tD/T
    #     D3 = D_3(x)
    #     dD3dx   = dD_3dx(x,D3)
    #
    #     return 3*r*NAv*kB*(3*dtDdV_T*(1/8)+dtDdV_T*np.exp(-x)/(1-np.exp(-x))-(1/3)*dD3dx*dtDdV_T)

    def d2FdT2_V(self,T,V):
        """
        (d2F(T,V)/dT2)_V

        :param float T: Temperature.
        :param float V: Volume.
        """
        x = self.tD/T
        ex = np.exp(x)
        D3      = D_3(x)
        return 3*r*NAv*((ex-1)*T*(T**2*self.d2tDdT2_V*self.tD-4*(self.dtDdT_V*T-self.tD)**2)*D3+3*self.tD*(self.d2tDdT2_V*self.tD*ex*T**2-T**2*self.d2tDdT2_V*self.tD+8*(self.dtDdT_V*T-self.tD)**2)*(1/8))*kB/(self.tD**2*(ex-1)*T**2)

    def d2FdV2_T(self,T,V):
        """
        (d2F(T,V)/dV2)_T

        :param float T: Temperature.
        :param float V: Volume.
        """
        x = self.tD/T
        D3      = D_3(x)
        dD3dx   = dD_3dx(x,D3)
        return 3*r*NAv*kB*(8*self.dtDdV_T**2*self.tD*dD3dx-8*self.dtDdV_T**2*D3*T+8*self.d2tDdV2_T*D3*self.tD*T+3*self.d2tDdV2_T*self.tD**2)/(8*self.tD**2)

    def d3FdV3_T(self,T,V):
        """
        (d3F(T,V)/dV3)_T

        :param float T: Temperature.
        :param float V: Volume.
        """
        x = self.tD/T
        D3      = D_3(x)
        dD3dx   = dD_3dx(x,D3)
        d2D3dx2 = d2D_3dx2(x,D3,dD3dx)
        return 3*r*(T**2*(self.d3tDdV3_T*self.tD**2-3*self.dtDdV_T*self.d2tDdV2_T*self.tD+2*self.dtDdV_T**3)*D3+(3*self.dtDdV_T*self.d2tDdV2_T*T*self.tD**2-2*self.dtDdV_T**3*T*self.tD)*dD3dx+d2D3dx2*self.dtDdV_T**3*self.tD**2+3*self.d3tDdV3_T*self.tD**3*T*(1/8))*kB*NAv/(T*self.tD**3)

    def d4FdV4_T(self,T,V):
        """
        (d4F(T,V)/dV4)_T

        :param float T: Temperature.
        :param float V: Volume.
        """
        x = self.tD/T
        D3      = D_3(x)
        dD3dx   = dD_3dx(x,D3)
        d2D3dx2 = d2D_3dx2(x,D3,dD3dx)
        d3D3dx3 = d3D_3dx3(x,D3,dD3dx,d2D3dx2)

        return -12*r*(T**3*(-(1/4)*self.d4tDdV4_T*self.tD**3+(self.d3tDdV3_T*self.dtDdV_T+3*self.d2tDdV2_T**2*(1/4))*self.tD**2-3*self.dtDdV_T**2*self.d2tDdV2_T*self.tD+3*self.dtDdV_T**4*(1/2))*D3-self.tD*(T**2*((self.d3tDdV3_T*self.dtDdV_T+3*self.d2tDdV2_T**2*(1/4))*self.tD**2-3*self.dtDdV_T**2*self.d2tDdV2_T*self.tD+3*self.dtDdV_T**4*(1/2))*dD3dx+(1/32)*(3*((16*self.dtDdV_T**2*self.d2tDdV2_T*self.tD*T-8*self.dtDdV_T**4*T)*d2D3dx2+self.tD*(8*d3D3dx3*self.dtDdV_T**4*(1/3)+self.d4tDdV4_T*self.tD*T**2)))*self.tD))*kB*NAv/(T**2*self.tD**4)

    def d2FdVdT(self,T,V):
        """
        (d2F(T,V)/dVdT)

        :param float T: Temperature.
        :param float V: Volume.
        """
        x = self.tD/T
        D3      = D_3(x)
        dD3dx   = dD_3dx(x,D3)
        return 3*r*(dD3dx*(self.dtDdT_V/T-self.tD/T**2)*T+D3+3*self.dtDdT_V*(1/8))*kB*self.dtDdV_T*NAv/self.tD+3*r*(D3*T+3*self.tD*(1/8))*kB*self.d2tDdVdT*NAv/self.tD-3*r*(D3*T+3*self.tD*(1/8))*kB*self.dtDdV_T*NAv*self.dtDdT_V/self.tD**2

    def d3FdV2dT(self,T,V):
        """
        (d3F(T,V)/dV2dT)

        :param float T: Temperature.
        :param float V: Volume.
        """
        x = self.tD/T
        D3      = D_3(x)
        dD3dx   = dD_3dx(x,D3)
        d2D3dx2 = d2D_3dx2(x,D3,dD3dx)

        return -3*r*(T**2*((-T*self.d3tDdV2dT-self.d2tDdV2_T)*self.tD**2+(T*self.d2tDdV2_T*self.dtDdT_V+2*T*self.dtDdV_T*self.d2tDdVdT+self.dtDdV_T**2)*self.tD-2*T*self.dtDdT_V*self.dtDdV_T**2)*D3-self.tD*((-self.d2tDdV2_T*self.tD**2+(T*self.d2tDdV2_T*self.dtDdT_V+2*T*self.dtDdV_T*self.d2tDdVdT+self.dtDdV_T**2)*self.tD-2*T*self.dtDdT_V*self.dtDdV_T**2)*T*dD3dx+3*self.tD*(8*self.dtDdV_T**2*(T*self.dtDdT_V-self.tD)*d2D3dx2*(1/3)+self.tD*self.d3tDdV2dT*T**2)*(1/8)))*kB*NAv/(T**2*self.tD**3)

    def d3FdVdT2(self,T,V):
        """
        (d3F(T,V)/dVdT2)

        :param float T: Temperature.
        :param float V: Volume.
        """
        x = self.tD/T
        D3      = D_3(x)
        dD3dx   = dD_3dx(x,D3)
        d2D3dx2 = d2D_3dx2(x,D3,dD3dx)

        return -(6*(T**3*((-(1/2)*self.d3tDdVdT2*T-self.d2tDdVdT)*self.tD**2+(((1/2)*self.d2tDdT2_V*T+self.dtDdT_V)*self.dtDdV_T+self.dtDdT_V*self.d2tDdVdT*T)*self.tD-self.dtDdT_V**2*self.dtDdV_T*T)*D3-(T**2*(-self.tD**2*self.d2tDdVdT+(((1/2)*self.d2tDdT2_V*T+self.dtDdT_V)*self.dtDdV_T+self.dtDdT_V*self.d2tDdVdT*T)*self.tD-self.dtDdT_V**2*self.dtDdV_T*T)*dD3dx+(1/16)*(3*(8*self.dtDdV_T*(T*self.dtDdT_V-self.tD)**2*d2D3dx2*(1/3)+self.tD*self.d3tDdVdT2*T**3))*self.tD)*self.tD))*r*kB*NAv/(T**3*self.tD**3)
