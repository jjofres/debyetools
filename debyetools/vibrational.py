import numpy as np
from debyetools.debfunct import D_3, dD_3dx, d2D_3dx2, d3D_3dx3

np.seterr(divide='ignore',invalid='ignore')
hbar = 0.1054571800e-33
NAv = 0.6022140857e24
kB = 0.138064852e-22
r = 1


class Vibrational:
    """
    Instantiate the vibrational contribution to the free energy and its derivatives for the calculation of the
    thermodynamic properties.

    :param nu: Poisson's ratio.
    :type nu: float
    :param EOS_obj: Equation of state object.
    :type EOS_obj: potential_instance
    :param float m: Mass in Kg/mol-at.
    :param intAnharmonicity_instance intanh: Intrinsic anharmonicity object.
    """

    def __init__(self, nu: float, EOS_obj: object, m: float, intanh: np.ndarray, mode: str):
        self.d4tDdV4_T = None
        self.d3tDdVdT2 = None
        self.d3tDdV2dT = None
        self.d3tDdV3_T = None
        self.d2tDdVdT = None
        self.d2tDdT2_V = None
        self.d2tDdV2_T = None
        self.dtDdT_V = None
        self.d4AnhdV4_T = None
        self.d3AnhdV3_T = None
        self.d3AnhdVdT2 = None
        self.d3AnhdV2dT = None
        self.d2AnhdT2_V = None
        self.d2AnhdV2_T = None
        self.d2AnhdVdT = None
        self.dAnhdV_T = None
        self.dAnhdT_V = None
        self.Anh = None
        self.EOS = EOS_obj
        self.kv = (2. / 3. * ((2. + 2. * nu) / (3. - 6. * nu)) ** (3. / 2.) + 1. / 3. * (
                    (1. + nu) / (3. - 3. * nu)) ** (3. / 2.)) ** (-1. / 3.)
        self.m = m
        self.intanh = intanh
        self.DM = None
        self.tD = None
        self.dtDdV_T = None

        self.xDcte = hbar * 6 ** (1 / 3.) * (np.pi ** 2 * NAv * r) ** (1 / 3.)

        self.mode = mode
        if mode == 'DM':
            self.V0_DM = EOS_obj.V0
            self.b_DM = 0.5
            self.a_DM = -0.5
            self.lam = -1
        elif mode == 'Sl':
            self.V0_DM = EOS_obj.V0
            self.b_DM = 0.5
            self.a_DM = -1 / 6
            self.lam = -1
        elif mode == 'mfv':
            self.V0_DM = EOS_obj.V0
            self.b_DM = 0.5
            self.a_DM = -0.95
            self.lam = -1
        elif mode == 'VZ':
            self.V0_DM = EOS_obj.V0
            self.b_DM = 0.5
            self.a_DM = -5 / 6
            self.lam = -1
        elif mode == 'jjsl':
            self.V0_DM = 1
            self.b_DM = 0
            self.a_DM = 0
            self.lam = -1
        elif mode == 'jjdm':
            self.V0_DM = 1
            self.b_DM = 0
            self.a_DM = 0
            self.lam = 0
        elif mode == 'jjfv':
            self.V0_DM = 1
            self.b_DM = 0
            self.a_DM = 0
            self.lam = 1

        else:
            hola
            self.V0_DM = ''
            self.b_DM = ''
            self.a_DM = ''
            self.lam = -1

    def set_int_anh(self, T: float, V: float) -> None:
        """
        Calculates intrinsic anharmonicity correction to the Debye temperature and its derivatives.

        :param float T: Temperature.
        :param float V: Volume.
        """
        self.Anh = self.intanh.Anh(T, V)
        self.dAnhdT_V = self.intanh.dAnhdT_V()
        self.dAnhdV_T = self.intanh.dAnhdV_T(T, V)
        self.d2AnhdVdT = self.intanh.d2AnhdVdT(T)
        self.d2AnhdV2_T = self.intanh.d2AnhdV2_T(T, V)
        self.d2AnhdT2_V = self.intanh.d2AnhdT2_V()
        self.d3AnhdV2dT = self.intanh.d3AnhdV2dT(T, V)
        self.d3AnhdVdT2 = self.intanh.d3AnhdVdT2(T)
        self.d3AnhdV3_T = self.intanh.d3AnhdV3_T(T, V)
        self.d4AnhdV4_T = self.intanh.d4AnhdV4_T(T, V)
    def set_int_anh_4minF(self, T: float, V: float) -> None:
        """
        Calculates intrinsic anharmonicity correction to the Debye temperature and its derivatives.

        :param float T: Temperature.
        :param float V: Volume.
        """
        self.Anh = self.intanh.Anh(T, V)
        self.dAnhdT_V = 'X'#self.intanh.dAnhdT_V()
        self.dAnhdV_T = 'X'#self.intanh.dAnhdV_T(T, V)
        self.d2AnhdVdT = 'X'#self.intanh.d2AnhdVdT(T)
        self.d2AnhdV2_T = 'X'#self.intanh.d2AnhdV2_T(T, V)
        self.d2AnhdT2_V = 'X'#self.intanh.d2AnhdT2_V()
        self.d3AnhdV2dT = 'X'#self.intanh.d3AnhdV2dT(T, V)
        self.d3AnhdVdT2 = 'X'#self.intanh.d3AnhdVdT2(T)
        self.d3AnhdV3_T = 'X'#self.intanh.d3AnhdV3_T(T, V)
        self.d4AnhdV4_T = 'X'#self.intanh.d4AnhdV4_T(T, V)


    def set_theta(self, T: float, V: float) -> None:
        """
        Calculates the Debye Temperature and its derivatives.

        :param float T: Temperature.
        :param float V: Volume.
        """
        kv = self.kv
        m = self.m

        b_DM = self.b_DM
        a_DM = self.a_DM
        V0_DM = self.V0_DM
        lam = self.lam

        dE0dV_T = self.EOS.dE0dV_T(V)
        d2E0dV2_T = self.EOS.d2E0dV2_T(V)
        d2E0dV2_T_DM = self.EOS.d2E0dV2_T(V0_DM)
        d3E0dV3_T = self.EOS.d3E0dV3_T(V)
        d4E0dV4_T = self.EOS.d4E0dV4_T(V)
        d5E0dV5_T = self.EOS.d5E0dV5_T(V)
        d6E0dV6_T = self.EOS.d6E0dV6_T(V)

        B0_DM = V0_DM * d2E0dV2_T_DM

        P0 = - dE0dV_T
        dP0dV = - d2E0dV2_T
        dP0dV_DM = - d2E0dV2_T_DM
        d2P0dV2 = - d3E0dV3_T
        d3P0dV3 = - d4E0dV4_T
        d4P0dV4 = - d5E0dV5_T
        d5P0dV5 = - d6E0dV6_T

        vDPrm_DM = - dP0dV_DM/(r*m)
        vDsqrt_DM = np.sqrt(vDPrm_DM)
        vD_DM = kv*V0_DM*vDsqrt_DM
        xD = self.xDcte*(1/V)**(1/3.)/kB
        xD_DM = self.xDcte*(1/V0_DM)**(1/3.)/kB

        B2 = (-V*dP0dV-(2*lam*(1/3)+2/3)*P0)/(V*m*r)
        dB2dV = ((4*lam**2+14*lam+10)*P0-9*V*(-2*m*r*B2*(lam+1)*(1/3)+V*d2P0dV2))/(9*V**2*m*r)
        d2B2dV2 = ((-8*lam**3-60*lam**2-132*lam-80)*P0-27*V*(4*m*r*B2*(lam+4)*(lam+1)*(1/9)+V*(-2*m*r*(lam+1)*dB2dV*(1/3)+V*d3P0dV3)))/(27*V**3*m*r)
        d3B2dV3 = ((16*lam**4+208*lam**3+924*lam**2+1612*lam+880)*P0-81*V*(-8*r*(lam+4)*(lam+1)*(lam+11/2)*m*B2*(1/27)+V*(4*r*(lam+1)*(lam+11/2)*m*dB2dV*(1/9)+(-2*m*r*d2B2dV2*(lam+1)*(1/3)+V*d4P0dV4)*V)))/(81*V**4*m*r)
        d4B2dV4 = ((32*lam**5+256*lam**4-232*lam**3-6016*lam**2-14360*lam-8800)*P0-243*V*(-16*r*(lam-5)*(lam+4)*(lam+1)*(lam+11/2)*m*B2*(1/81)+V*(8*r*(lam-5)*(lam+1)*(lam+11/2)*m*dB2dV*(1/27)+(-4*m*r*(lam+1)*(lam-5)*d2B2dV2*(1/9)+V*(2*m*r*(lam+1)*d3B2dV3*(1/3)+V*d5P0dV5))*V)))/(243*V**5*m*r)

        vD = V*kv*np.sqrt(B2)
        dvDdV = (V**3*kv**2*(dB2dV)+2*vD**2)/(2*V*vD)
        d2vDdV2 = (V**4*kv**2*(d2B2dV2)-2*dvDdV**2*V**2+8*dvDdV*V*vD-6*vD**2)/(2*V**2*vD)
        d3vDdV3 = (V**5*kv**2*(d3B2dV3)-(6*(2*vD+V*(V*d2vDdV2-2*dvDdV)))*(dvDdV*V-2*vD))/(2*vD*V**3)
        d4vDdV4 = ((d4B2dV4)*kv**2*V**6-120*vD**2+(16*V**3*d3vDdV3-72*d2vDdV2*V**2+192*dvDdV*V)*vD-72*dvDdV**2*V**2-8*V**3*(V*d3vDdV3-6*d2vDdV2)*dvDdV-6*d2vDdV2**2*V**4)/(2*V**4*vD)
        dxDdV = -self.xDcte/(3*kB*V**(4/3.))
        d2xDdV2 = 4*self.xDcte/(9*kB*V**(7/3.))
        d3xDdV3 = -28*self.xDcte/(27*V**(10/3)*kB)
        d4xDdV4 = 280*self.xDcte/(81*V**(13/3)*kB)

        DM = (V*d2E0dV2_T/B0_DM)**b_DM/(V/V0_DM)**a_DM
        self.DM = DM
        dDMdV = (V*d2E0dV2_T/B0_DM)**b_DM*b_DM*(d2E0dV2_T/B0_DM+V*(d3E0dV3_T)/B0_DM)*B0_DM/(V*d2E0dV2_T*(V/V0_DM)**a_DM)-(V*d2E0dV2_T/B0_DM)**b_DM*a_DM/((V/V0_DM)**a_DM*V)
        d2DMdV2 = V0_DM**a_DM*B0_DM**(-b_DM)*(-2*(d3E0dV3_T)*b_DM*d2E0dV2_T**(b_DM-1)*(-b_DM+a_DM)*V**(b_DM-1-a_DM)+d2E0dV2_T**b_DM*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-2-a_DM)+V**(b_DM-a_DM)*(d2E0dV2_T**(b_DM-1)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-2)*(b_DM-1))*b_DM)
        d3DMdV3 = -V0_DM**a_DM*B0_DM**(-b_DM)*(d2E0dV2_T**b_DM*(-b_DM+2+a_DM)*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-a_DM-3)-3*b_DM*(-(d2E0dV2_T**(b_DM-1)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-2)*(b_DM-1))*(-b_DM+a_DM)*V**(b_DM-1-a_DM)+(d3E0dV3_T)*d2E0dV2_T**(b_DM-1)*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-2-a_DM)+(1/3)*V**(b_DM-a_DM)*(d2E0dV2_T**(b_DM-1)*(d5E0dV5_T)+(d3E0dV3_T)*(3*d2E0dV2_T**(b_DM-2)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-3)*(b_DM-2))*(b_DM-1))))
        d4DMdV4 = (d2E0dV2_T**b_DM*(-b_DM+a_DM)*(-b_DM+a_DM+3)*(-b_DM+2+a_DM)*(-b_DM+1+a_DM)*V**(b_DM-4-a_DM)+6*b_DM*((d2E0dV2_T**(b_DM-1)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-2)*(b_DM-1))*(-b_DM+a_DM)*(-b_DM+1+a_DM)*V**(b_DM-2-a_DM)-(1/3)*(2*(d2E0dV2_T**(b_DM-1)*(d5E0dV5_T)+(d3E0dV3_T)*(3*d2E0dV2_T**(b_DM-2)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-3)*(b_DM-2))*(b_DM-1)))*(-b_DM+a_DM)*V**(b_DM-1-a_DM)-2*(d3E0dV3_T)*d2E0dV2_T**(b_DM-1)*(-b_DM+2+a_DM)*(-b_DM+1+a_DM)*(- b_DM +a_DM)*V**(b_DM-a_DM-3)*(1/3)+(1/6)*(d2E0dV2_T**(b_DM-1)*(d6E0dV6_T)+(4*(d3E0dV3_T)*d2E0dV2_T**(b_DM-2)*(d5E0dV5_T)+3*d2E0dV2_T**(b_DM-2)*(d4E0dV4_T)**2+(6*d2E0dV2_T**(b_DM-3)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-4)*(b_DM-3))*(b_DM-2)*(d3E0dV3_T)**2)*(b_DM-1))*V**(b_DM-a_DM)))*V0_DM**a_DM*B0_DM**(-b_DM)

        tD_DM = xD_DM * vD_DM
        self.tD = xD*vD*self.Anh if 'jj' in self.mode else tD_DM*self.Anh*DM
        self.dtDdV_T = dxDdV*vD*self.Anh+xD*dvDdV*self.Anh+xD*vD*self.dAnhdV_T if 'jj' in self.mode else tD_DM*self.Anh*dDMdV
        self.dtDdT_V = xD*vD*self.dAnhdT_V if 'jj' in self.mode else 0
        self.d2tDdV2_T =d2xDdV2*vD*self.Anh+2*dxDdV*dvDdV*self.Anh+2*dxDdV*vD*self.dAnhdV_T+xD*d2vDdV2*self.Anh+2*xD*dvDdV*self.dAnhdV_T+xD*vD*self.d2AnhdV2_T if 'jj' in self.mode else tD_DM*self.Anh*d2DMdV2
        self.d2tDdT2_V = xD*vD*self.d2AnhdT2_V if 'jj' in self.mode else 0
        self.d2tDdVdT = dxDdV*vD*self.dAnhdT_V+xD*dvDdV*self.dAnhdT_V+xD*vD*self.d2AnhdVdT if 'jj' in self.mode else 0
        self.d3tDdV3_T = d3xDdV3*vD*self.Anh+3*d2xDdV2*dvDdV*self.Anh+3*d2xDdV2*vD*self.dAnhdV_T+3*dxDdV*d2vDdV2*self.Anh+6*dxDdV*dvDdV*self.dAnhdV_T+3*dxDdV*vD*self.d2AnhdV2_T+xD*d3vDdV3*self.Anh+3*xD*d2vDdV2*self.dAnhdV_T+3*xD*dvDdV*self.d2AnhdV2_T+xD*vD*self.d3AnhdV3_T  if 'jj' in self.mode else tD_DM*self.Anh*d3DMdV3
        self.d3tDdV2dT =d2xDdV2*vD*self.dAnhdT_V+2*dxDdV*dvDdV*self.dAnhdT_V+2*dxDdV*vD*self.d2AnhdVdT+xD*d2vDdV2*self.dAnhdT_V+2*xD*dvDdV*self.d2AnhdVdT+xD*vD*self.d3AnhdV2dT  if 'jj' in self.mode else 0
        self.d3tDdVdT2 = dxDdV*vD*self.d2AnhdT2_V+xD*dvDdV*self.d2AnhdT2_V+xD*vD*self.d3AnhdVdT2  if 'jj' in self.mode else 0
        self.d4tDdV4_T = 6*d2xDdV2*d2vDdV2*self.Anh+12*d2xDdV2*dvDdV*self.dAnhdV_T+6*d2xDdV2*vD*self.d2AnhdV2_T+4*dxDdV*d3vDdV3*self.Anh+12*dxDdV*d2vDdV2*self.dAnhdV_T+12*dxDdV*dvDdV*self.d2AnhdV2_T+4*dxDdV*vD*self.d3AnhdV3_T+xD*d4vDdV4*self.Anh+4*xD*d3vDdV3*self.dAnhdV_T+6*xD*d2vDdV2*self.d2AnhdV2_T+4*xD*dvDdV*self.d3AnhdV3_T+xD*vD*self.d4AnhdV4_T+d4xDdV4*vD*self.Anh+4*d3xDdV3*dvDdV*self.Anh+4*d3xDdV3*vD*self.dAnhdV_T  if 'jj' in self.mode else tD_DM*self.Anh*d4DMdV4

    def set_theta_4minF(self, T: float, V: float) -> None:
        """
        Calculates the Debye Temperature and its derivatives.

        :param float T: Temperature.
        :param float V: Volume.
        """
        kv = self.kv
        m = self.m
        #
        b_DM = self.b_DM
        a_DM = self.a_DM
        V0_DM = self.V0_DM
        lam = self.lam
        #
        dE0dV_T = self.EOS.dE0dV_T(V)
        d2E0dV2_T = self.EOS.d2E0dV2_T(V)
        d2E0dV2_T_DM = self.EOS.d2E0dV2_T(V0_DM)
        # d3E0dV3_T = self.EOS.d3E0dV3_T(V)
        # d4E0dV4_T = self.EOS.d4E0dV4_T(V)
        # d5E0dV5_T = self.EOS.d5E0dV5_T(V)
        # d6E0dV6_T = self.EOS.d6E0dV6_T(V)
        #
        B0_DM = V0_DM * d2E0dV2_T_DM
        #
        P0 = - dE0dV_T
        dP0dV = - d2E0dV2_T
        dP0dV_DM = - d2E0dV2_T_DM
        # d2P0dV2 = - d3E0dV3_T
        # d3P0dV3 = - d4E0dV4_T
        # d4P0dV4 = - d5E0dV5_T
        # d5P0dV5 = - d6E0dV6_T
        #
        vDPrm_DM = - dP0dV_DM/(r*m)
        vDsqrt_DM = np.sqrt(vDPrm_DM)
        vD_DM = kv*V0_DM*vDsqrt_DM
        xD = self.xDcte*(1/V)**(1/3.)/kB
        xD_DM = self.xDcte*(1/V0_DM)**(1/3.)/kB
        #
        B2 = (-V*dP0dV-(2*lam*(1/3)+2/3)*P0)/(V*m*r)
        # dB2dV = ((4*lam**2+14*lam+10)*P0-9*V*(-2*m*r*B2*(lam+1)*(1/3)+V*d2P0dV2))/(9*V**2*m*r)
        # d2B2dV2 = ((-8*lam**3-60*lam**2-132*lam-80)*P0-27*V*(4*m*r*B2*(lam+4)*(lam+1)*(1/9)+V*(-2*m*r*(lam+1)*dB2dV*(1/3)+V*d3P0dV3)))/(27*V**3*m*r)
        # d3B2dV3 = ((16*lam**4+208*lam**3+924*lam**2+1612*lam+880)*P0-81*V*(-8*r*(lam+4)*(lam+1)*(lam+11/2)*m*B2*(1/27)+V*(4*r*(lam+1)*(lam+11/2)*m*dB2dV*(1/9)+(-2*m*r*d2B2dV2*(lam+1)*(1/3)+V*d4P0dV4)*V)))/(81*V**4*m*r)
        # d4B2dV4 = ((32*lam**5+256*lam**4-232*lam**3-6016*lam**2-14360*lam-8800)*P0-243*V*(-16*r*(lam-5)*(lam+4)*(lam+1)*(lam+11/2)*m*B2*(1/81)+V*(8*r*(lam-5)*(lam+1)*(lam+11/2)*m*dB2dV*(1/27)+(-4*m*r*(lam+1)*(lam-5)*d2B2dV2*(1/9)+V*(2*m*r*(lam+1)*d3B2dV3*(1/3)+V*d5P0dV5))*V)))/(243*V**5*m*r)
        #
        vD = V*kv*np.sqrt(B2)
        # dvDdV = (V**3*kv**2*(dB2dV)+2*vD**2)/(2*V*vD)
        # d2vDdV2 = (V**4*kv**2*(d2B2dV2)-2*dvDdV**2*V**2+8*dvDdV*V*vD-6*vD**2)/(2*V**2*vD)
        # d3vDdV3 = (V**5*kv**2*(d3B2dV3)-(6*(2*vD+V*(V*d2vDdV2-2*dvDdV)))*(dvDdV*V-2*vD))/(2*vD*V**3)
        # d4vDdV4 = ((d4B2dV4)*kv**2*V**6-120*vD**2+(16*V**3*d3vDdV3-72*d2vDdV2*V**2+192*dvDdV*V)*vD-72*dvDdV**2*V**2-8*V**3*(V*d3vDdV3-6*d2vDdV2)*dvDdV-6*d2vDdV2**2*V**4)/(2*V**4*vD)
        # dxDdV = -self.xDcte/(3*kB*V**(4/3.))
        # d2xDdV2 = 4*self.xDcte/(9*kB*V**(7/3.))
        # d3xDdV3 = -28*self.xDcte/(27*V**(10/3)*kB)
        # d4xDdV4 = 280*self.xDcte/(81*V**(13/3)*kB)
        #
        DM = (V*d2E0dV2_T/B0_DM)**b_DM/(V/V0_DM)**a_DM
        # self.DM = DM
        # dDMdV = (V*d2E0dV2_T/B0_DM)**b_DM*b_DM*(d2E0dV2_T/B0_DM+V*(d3E0dV3_T)/B0_DM)*B0_DM/(V*d2E0dV2_T*(V/V0_DM)**a_DM)-(V*d2E0dV2_T/B0_DM)**b_DM*a_DM/((V/V0_DM)**a_DM*V)
        # d2DMdV2 = V0_DM**a_DM*B0_DM**(-b_DM)*(-2*(d3E0dV3_T)*b_DM*d2E0dV2_T**(b_DM-1)*(-b_DM+a_DM)*V**(b_DM-1-a_DM)+d2E0dV2_T**b_DM*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-2-a_DM)+V**(b_DM-a_DM)*(d2E0dV2_T**(b_DM-1)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-2)*(b_DM-1))*b_DM)
        # d3DMdV3 = -V0_DM**a_DM*B0_DM**(-b_DM)*(d2E0dV2_T**b_DM*(-b_DM+2+a_DM)*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-a_DM-3)-3*b_DM*(-(d2E0dV2_T**(b_DM-1)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-2)*(b_DM-1))*(-b_DM+a_DM)*V**(b_DM-1-a_DM)+(d3E0dV3_T)*d2E0dV2_T**(b_DM-1)*(-b_DM+1+a_DM)*(-b_DM+a_DM)*V**(b_DM-2-a_DM)+(1/3)*V**(b_DM-a_DM)*(d2E0dV2_T**(b_DM-1)*(d5E0dV5_T)+(d3E0dV3_T)*(3*d2E0dV2_T**(b_DM-2)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-3)*(b_DM-2))*(b_DM-1))))
        # d4DMdV4 = (d2E0dV2_T**b_DM*(-b_DM+a_DM)*(-b_DM+a_DM+3)*(-b_DM+2+a_DM)*(-b_DM+1+a_DM)*V**(b_DM-4-a_DM)+6*b_DM*((d2E0dV2_T**(b_DM-1)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-2)*(b_DM-1))*(-b_DM+a_DM)*(-b_DM+1+a_DM)*V**(b_DM-2-a_DM)-(1/3)*(2*(d2E0dV2_T**(b_DM-1)*(d5E0dV5_T)+(d3E0dV3_T)*(3*d2E0dV2_T**(b_DM-2)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-3)*(b_DM-2))*(b_DM-1)))*(-b_DM+a_DM)*V**(b_DM-1-a_DM)-2*(d3E0dV3_T)*d2E0dV2_T**(b_DM-1)*(-b_DM+2+a_DM)*(-b_DM+1+a_DM)*(- b_DM +a_DM)*V**(b_DM-a_DM-3)*(1/3)+(1/6)*(d2E0dV2_T**(b_DM-1)*(d6E0dV6_T)+(4*(d3E0dV3_T)*d2E0dV2_T**(b_DM-2)*(d5E0dV5_T)+3*d2E0dV2_T**(b_DM-2)*(d4E0dV4_T)**2+(6*d2E0dV2_T**(b_DM-3)*(d4E0dV4_T)+(d3E0dV3_T)**2*d2E0dV2_T**(b_DM-4)*(b_DM-3))*(b_DM-2)*(d3E0dV3_T)**2)*(b_DM-1))*V**(b_DM-a_DM)))*V0_DM**a_DM*B0_DM**(-b_DM)

        tD_DM = xD_DM * vD_DM
        self.tD = xD*vD*self.Anh if 'jj' in self.mode else tD_DM*self.Anh*DM
        # self.dtDdV_T = 'X'#dxDdV*vD*self.Anh+xD*dvDdV*self.Anh+xD*vD*self.dAnhdV_T if 'jj' in self.mode else tD_DM*self.Anh*dDMdV
        # self.dtDdT_V = 'X'#xD*vD*self.dAnhdT_V if 'jj' in self.mode else 0
        # self.d2tDdV2_T ='X'#d2xDdV2*vD*self.Anh+2*dxDdV*dvDdV*self.Anh+2*dxDdV*vD*self.dAnhdV_T+xD*d2vDdV2*self.Anh+2*xD*dvDdV*self.dAnhdV_T+xD*vD*self.d2AnhdV2_T if 'jj' in self.mode else tD_DM*self.Anh*d2DMdV2
        # self.d2tDdT2_V = 'X'#xD*vD*self.d2AnhdT2_V if 'jj' in self.mode else 0
        # self.d2tDdVdT = 'X'#dxDdV*vD*self.dAnhdT_V+xD*dvDdV*self.dAnhdT_V+xD*vD*self.d2AnhdVdT if 'jj' in self.mode else 0
        # self.d3tDdV3_T = 'X'#d3xDdV3*vD*self.Anh+3*d2xDdV2*dvDdV*self.Anh+3*d2xDdV2*vD*self.dAnhdV_T+3*dxDdV*d2vDdV2*self.Anh+6*dxDdV*dvDdV*self.dAnhdV_T+3*dxDdV*vD*self.d2AnhdV2_T+xD*d3vDdV3*self.Anh+3*xD*d2vDdV2*self.dAnhdV_T+3*xD*dvDdV*self.d2AnhdV2_T+xD*vD*self.d3AnhdV3_T  if 'jj' in self.mode else tD_DM*self.Anh*d3DMdV3
        # self.d3tDdV2dT ='X'#d2xDdV2*vD*self.dAnhdT_V+2*dxDdV*dvDdV*self.dAnhdT_V+2*dxDdV*vD*self.d2AnhdVdT+xD*d2vDdV2*self.dAnhdT_V+2*xD*dvDdV*self.d2AnhdVdT+xD*vD*self.d3AnhdV2dT  if 'jj' in self.mode else 0
        # self.d3tDdVdT2 = 'X'#dxDdV*vD*self.d2AnhdT2_V+xD*dvDdV*self.d2AnhdT2_V+xD*vD*self.d3AnhdVdT2  if 'jj' in self.mode else 0
        # self.d4tDdV4_T = 'X'#6*d2xDdV2*d2vDdV2*self.Anh+12*d2xDdV2*dvDdV*self.dAnhdV_T+6*d2xDdV2*vD*self.d2AnhdV2_T+4*dxDdV*d3vDdV3*self.Anh+12*dxDdV*d2vDdV2*self.dAnhdV_T+12*dxDdV*dvDdV*self.d2AnhdV2_T+4*dxDdV*vD*self.d3AnhdV3_T+xD*d4vDdV4*self.Anh+4*xD*d3vDdV3*self.dAnhdV_T+6*xD*d2vDdV2*self.d2AnhdV2_T+4*xD*dvDdV*self.d3AnhdV3_T+xD*vD*self.d4AnhdV4_T+d4xDdV4*vD*self.Anh+4*d3xDdV3*dvDdV*self.Anh+4*d3xDdV3*vD*self.dAnhdV_T  if 'jj' in self.mode else tD_DM*self.Anh*d4DMdV4



    def F(self, T: float, V: float) -> float:
        """
        Vibration Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: F_vib.
        :rtype:  float
        """

        x = self.tD/T
        D3 = D_3(x)
        # print(tD/T, tD, T)
        if type(V) is not np.ndarray:
            if x < 0.04:
                return 1e10
        return 3*r*NAv*kB*(self.tD*3/8+T*np.log(1-np.exp(-x))-D3*T/3)

    def dFdV_T(self, T: float, V: float) -> float:
        """
        Derivative of vibrational Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: dFdV_T.
        :rtype:  float
        """

        x = self.tD/T
        D3 = D_3(x)
        dD3 = dD_3dx(x, D3)
        return 3*r*NAv*kB*(3*(self.dtDdV_T)*(1/8)+(self.dtDdV_T)*np.exp(-x)/(1-np.exp(-x))-(1/3)*dD3*(self.dtDdV_T))

    def dFdT_V(self, T: float, V: float) -> float:
        """
        Derivative of vibrational Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: dFdT_V.
        :rtype:  float
        """

        x = self.tD / T
        ixs = np.where(x >= 653)
        if len(ixs[0]) > 0:
            if min(x[ixs]) >= 653:
                for i in ixs:
                    x[i] = 653
        ex = np.exp(x)
        D3 = D_3(x)
        dD3dx = dD_3dx(x, D3)
        return 9*r*NAv*kB*(self.dtDdT_V)*(1/8) + 3*kB*r*NAv*np.log(1-np.exp(-x)) + 3*r*NAv*kB*(self.dtDdT_V)/(ex*(1-1/ex)) - 3*r*NAv*kB*self.tD/(T*ex*(1-1/ex)) - r*NAv*kB*dD3dx*(self.dtDdT_V) + r*NAv*kB*dD3dx*self.tD/T - r*NAv*kB*D3

    def d2FdT2_V(self, T: float, V: float) -> float:
        """
        Derivative of vibrational Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: d2FdT2_V.
        :rtype:  float
        """

        x = self.tD / T
        ixs = np.where(x >= 653)
        if len(ixs[0]) > 0:
            if min(x[ixs]) >= 653:
                for i in ixs:
                    x[i] = 653
        ex = np.exp(x)
        D3 = D_3(x)
        return 3 * r * NAv * ((ex - 1) * T * (
                    T ** 2 * self.d2tDdT2_V * self.tD - 4 * (self.dtDdT_V * T - self.tD) ** 2) * D3 + 3 * self.tD * (
                             self.d2tDdT2_V * self.tD * ex * T ** 2 - T ** 2 * self.d2tDdT2_V * self.tD + 8 * (
                              self.dtDdT_V * T - self.tD) ** 2) * (1 / 8)) * kB / (
                               self.tD ** 2 * (ex - 1) * T ** 2)

    def d2FdV2_T(self, T: float, V: float) -> float:
        """
        Derivative of vibrational Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: d2FdV2_T.
        :rtype:  float
        """
        x = self.tD / T
        D3 = D_3(x)
        dD3dx = dD_3dx(x, D3)
        return 3 * r * NAv * kB * (
                    8 * self.dtDdV_T ** 2 * self.tD * dD3dx - 8 * self.dtDdV_T ** 2 * D3 * T + 8 * self.d2tDdV2_T * D3 * self.tD * T + 3 * self.d2tDdV2_T * self.tD ** 2) / (
                           8 * self.tD ** 2)

    def d3FdV3_T(self, T: float, V: float) -> float:
        """
        Derivative of vibrational Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: d3FdV3_T.
        :rtype:  float
        """
        x = self.tD / T
        D3 = D_3(x)
        dD3dx = dD_3dx(x, D3)
        d2D3dx2 = d2D_3dx2(x, D3, dD3dx)
        return 3 * r * (T ** 2 * (
                    self.d3tDdV3_T * self.tD ** 2 - 3 * self.dtDdV_T * self.d2tDdV2_T * self.tD + 2 * self.dtDdV_T ** 3) * D3 + (
                                    3 * self.dtDdV_T * self.d2tDdV2_T * T * self.tD ** 2 - 2 * self.dtDdV_T ** 3 * T * self.tD) * dD3dx + d2D3dx2 * self.dtDdV_T ** 3 * self.tD ** 2 + 3 * self.d3tDdV3_T * self.tD ** 3 * T * (
                                    1 / 8)) * kB * NAv / (T * self.tD ** 3)

    def d4FdV4_T(self, T: float, V: float) -> float:
        """
        Derivative of vibrational Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: d4FdV4_T.
        :rtype:  float
        """
        x = self.tD / T
        D3 = D_3(x)
        dD3dx = dD_3dx(x, D3)
        d2D3dx2 = d2D_3dx2(x, D3, dD3dx)
        d3D3dx3 = d3D_3dx3(x, D3, dD3dx, d2D3dx2)

        return -12 * r * (T ** 3 * (-(1 / 4) * self.d4tDdV4_T * self.tD ** 3 + (
                    self.d3tDdV3_T * self.dtDdV_T + 3 * self.d2tDdV2_T ** 2 * (
                        1 / 4)) * self.tD ** 2 - 3 * self.dtDdV_T ** 2 * self.d2tDdV2_T * self.tD + 3 * self.dtDdV_T ** 4 * (
                                                1 / 2)) * D3 - self.tD * (T ** 2 * ((
                                                                                                self.d3tDdV3_T * self.dtDdV_T + 3 * self.d2tDdV2_T ** 2 * (
                                                                                                    1 / 4)) * self.tD ** 2 - 3 * self.dtDdV_T ** 2 * self.d2tDdV2_T * self.tD + 3 * self.dtDdV_T ** 4 * (
                                                                                                1 / 2)) * dD3dx + (
                                                                                      1 / 32) * (3 * ((
                                                                                                                  16 * self.dtDdV_T ** 2 * self.d2tDdV2_T * self.tD * T - 8 * self.dtDdV_T ** 4 * T) * d2D3dx2 + self.tD * (
                                                                                                                  8 * d3D3dx3 * self.dtDdV_T ** 4 * (
                                                                                                                      1 / 3) + self.d4tDdV4_T * self.tD * T ** 2))) * self.tD)) * kB * NAv / (
                           T ** 2 * self.tD ** 4)

    def d2FdVdT(self, T: float, V: float) -> float:
        """
        Derivative of vibrational Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: d2FdVdT.
        :rtype:  float
        """
        x = self.tD / T
        D3 = D_3(x)
        dD3dx = dD_3dx(x, D3)
        return 3 * r * (dD3dx * (self.dtDdT_V / T - self.tD / T ** 2) * T + D3 + 3 * self.dtDdT_V * (
                    1 / 8)) * kB * self.dtDdV_T * NAv / self.tD + 3 * r * (
                           D3 * T + 3 * self.tD * (1 / 8)) * kB * self.d2tDdVdT * NAv / self.tD - 3 * r * (
                           D3 * T + 3 * self.tD * (1 / 8)) * kB * self.dtDdV_T * NAv * self.dtDdT_V / self.tD ** 2

    def d3FdV2dT(self, T: float, V: float) -> float:
        """
        Derivative of vibrational Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: d3FdV2dT.
        :rtype:  float
        """
        x = self.tD / T
        D3 = D_3(x)
        dD3dx = dD_3dx(x, D3)
        d2D3dx2 = d2D_3dx2(x, D3, dD3dx)

        return -3 * r * (T ** 2 * ((-T * self.d3tDdV2dT - self.d2tDdV2_T) * self.tD ** 2 + (
                    T * self.d2tDdV2_T * self.dtDdT_V + 2 * T * self.dtDdV_T * self.d2tDdVdT + self.dtDdV_T ** 2) * self.tD - 2 * T * self.dtDdT_V * self.dtDdV_T ** 2) * D3 - self.tD * (
                                     (-self.d2tDdV2_T * self.tD ** 2 + (
                                                 T * self.d2tDdV2_T * self.dtDdT_V + 2 * T * self.dtDdV_T * self.d2tDdVdT + self.dtDdV_T ** 2) * self.tD - 2 * T * self.dtDdT_V * self.dtDdV_T ** 2) * T * dD3dx + 3 * self.tD * (
                                                 8 * self.dtDdV_T ** 2 * (T * self.dtDdT_V - self.tD) * d2D3dx2 * (
                                                     1 / 3) + self.tD * self.d3tDdV2dT * T ** 2) * (
                                                 1 / 8))) * kB * NAv / (T ** 2 * self.tD ** 3)

    def d3FdVdT2(self, T: float, V: float) -> float:
        """
        Derivative of vibrational Helmholtz free energy.

        :param float T: Temperature.
        :param float V: Volume.
        :return: d3FdVdT2.
        :rtype:  float
        """
        x = self.tD / T
        D3 = D_3(x)
        dD3dx = dD_3dx(x, D3)
        d2D3dx2 = d2D_3dx2(x, D3, dD3dx)

        return -(6 * (T ** 3 * ((-1/2 * self.d3tDdVdT2 * T - self.d2tDdVdT) * self.tD ** 2 + ((1/2 * self.d2tDdT2_V * T + self.dtDdT_V) * self.dtDdV_T + self.dtDdT_V * self.d2tDdVdT * T) * self.tD - self.dtDdT_V ** 2 * self.dtDdV_T * T) * D3 - (
                                  T ** 2 * (-self.tD ** 2 * self.d2tDdVdT + (((
                                                                                          1 / 2) * self.d2tDdT2_V * T + self.dtDdT_V) * self.dtDdV_T + self.dtDdT_V * self.d2tDdVdT * T) * self.tD - self.dtDdT_V ** 2 * self.dtDdV_T * T) * dD3dx + (
                                              1 / 16) * (3 * (
                                      8 * self.dtDdV_T * (T * self.dtDdT_V - self.tD) ** 2 * d2D3dx2 * (
                                          1 / 3) + self.tD * self.d3tDdVdT2 * T ** 3)) * self.tD) * self.tD)) * r * kB * NAv / (
                           T ** 3 * self.tD ** 3)
