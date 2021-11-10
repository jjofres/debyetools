import numpy as np

from debyetools.anharmonicity import Anharmonicity, intAnharmonicity
from debyetools.electronic import Electronic
from debyetools.defects import Defects
import debyetools.potentials as pots
from debyetools.debfunct import D_3, dD_3dx, d2D_3dx2, d3D_3dx3
hbar = 0.1054571800e-33
NAv  = 0.6022140857e24
kB   = 0.138064852e-22


class nDeb:
    """
    Instantiate an object that contains all the parameters for the evaluation of
    the thermodynamic properties of a certain element or compound. Also contains
    the method that implements an original Debye formalism for the calculation of
    the thermodynamic properties

    :param float nu: Poisson's ratio.
    :param float m: mass in Kg/mol-at
    :param list_of_floats p_intanh: Intrinsic anharmonicity parameters: a0, m0, V0.
    :param list_of_floats p_EOS: Equation of state parameters.
    :param list_of_floats p_electronic: Electronic contribution parameters.
    :param list_of_floats p_defects: Mono-vacancies defects contribution parameters: Evac00,Svac00,Tm,a,P2,V0.
    :param list_of_floats p_anh: Excess contribution parameters.
    :param string EOS_name: The EOS or potential to use as internal energy description.
    """
    def __init__(self, nu, m, p_intanh, p_EOS, p_electronic, p_defects, p_anh,EOS_name):
        a0, m0, V0_anh = p_intanh
        q0,q1,q2,q3 = p_electronic
        Evac00,Svac00,Tm,a,P2,V0_def = p_defects
        s0,s1,s2 = p_anh

        self.nu, self.r, self.m = nu, 1, m
        self.kv = (2./3.*((2. + 2.*nu)/(3.-6.*nu))**(3./2.) + 1./3.*((1. + nu)/(3. - 3.*nu))**(3./2.))**(-1./3.)

        self.anh = Anharmonicity(s0,s1,s2)
        self.intanh = intAnharmonicity(a0,m0,V0_anh)
        self.el = Electronic(1,q0,q1,q2,q3)
        self.deff = Defects(Evac00,Svac00,Tm,a,P2,V0_def)

        self.EOS = getattr(pots,EOS_name)()
        self.EOS.pEOS = p_EOS

        r=1
        self.xDcte = hbar*6**(1/3.)*(np.pi**2*NAv*r)**(1/3.)

    def eval_props(self, T, V):
        """
        Evaluates the thermodynamic properties of a given compound/element at (T,V).

        :params float T: The temperature in Kelvin.
        :params float V: The volume in "units".

        :return float: The heat capacity for the moment.
        """
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

        return {'Cp':-T*( d2FdT2_V - (d2FdVdT)**2 / d2FdV2_T)}
