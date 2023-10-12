import numpy as np
from typing import Tuple


def poisson_ratio(EM: np.ndarray, quiet: bool = False) -> float|Tuple[float,float,float,float,float,float,float,float]:
    """
    Calculation of the Poisson's ratio from elastic moduli matrix.

    :param EM: Elastic moduli matrix.
    :type EM: np.ndarray
    :param quiet: (optional) If verbose.
    :type quiet: bool
    :return: Poisson's ratio.
    :rtype: float
    """
    if quiet:
        return quiet_pa(EM)

    C11, C12, C13 = EM[0,0], EM[0,1], EM[0,2]
    C22, C23 = EM[1,1], EM[1,2]
    C33 = EM[2,2]
    C44 = EM[3,3]
    C55 = EM[4,4]
    C66 = EM[5,5]

    if EM[0,4]**2>0:
        C15 = EM[0,4]
        C25 = EM[1,4]
        C35 = EM[2,4]
        C46 = EM[3,5]
    else:
        C15 = EM[0,5]
        C25 = EM[1,5]
        C35 = EM[2,5]
        C46 = EM[3,4]

    f = C11*(C22*C55-C25**2)-C12*(C12*C55-C15*C25)+C15*(C12*C25-C15*C22)+C25*(C23*C35-C25*C33)
    g = C11*C22*C33-C11*C23**2-C22*C13**2-C33*C12**2+2*C12*C13*C23
    Omega=2*(C15*C25*(C33*C12-C13*C23)+C15*C35*(C22*C13-C12*C23)+C25*C35*(C11*C23-C12*C13)) -(C15**2*(C22*C33-C23**2)+C25**2*(C11*C33-C13**2)+C35**2*(C11*C22-C12**2))+g*C55
    GV = 1/15*(C11+C22+C33+3*(C44+C55+C66)-(C12+C13+C23))
    GR = 15*(4*((C33*C55-C35**2)*(C11+C22+C12) + (C23*C55-C25*C35)*(C11-C12-C23) + (C13*C35-C15*C33)*(C15+C25) + (C13*C55-C15*C35)*(C22-C12-C23-C13) + (C13*C25-C15*C23)*(C15-C25) + f)/Omega+3*(g/Omega+(C44+C66)/(C44*C66-C46**2)))**(-1)
    BV = (C11+C22+C33+2*(C12+C13+C23))/9
    BR = Omega*((C33*C55-C35**2)*(C11+C22-2*C12)+(C23*C55-C25*C35)*(2*C12-2*C11-C23) + (C13*C35-C15*C33)*(C15-2*C25)+(C13*C55-C15*C35)*(2*C12+2*C23-C13-2*C22)+2*(C13*C25-C15*C23)*(C25-C15)+f)**(-1)

    B = (BR+BV)/2
    S = (GR+GV)/2
    Y = (9.*B*S)/(3.*B+S)
    nu = (3.*B-Y)/(6.*B)

    return nu

def quiet_pa(EM: np.ndarray) -> Tuple[float,float,float,float,float,float,float,float]:
    """
    Calculation of the Poisson's ratio from elastic moduli matrix.

    :param EM: Elastic moduli matrix.
    :type EM: np.ndarray
    :return: BR, BV, B, GR, GV, S, AU, nu
    :rtype: Tuple[float,float,float,float,float,float,float,float]
    """
    C11, C12, C13 = EM[0,0]*1e-1, EM[0,1]*1e-1, EM[0,2]*1e-1
    C22, C23 = EM[1,1]*1e-1, EM[1,2]*1e-1
    C33 = EM[2,2]*1e-1
    C44 = EM[3,3]*1e-1
    C55 = EM[4,4]*1e-1
    C66 = EM[5,5]*1e-1

    if EM[0,4]*1e-1>0:
        C15 = EM[0,4]*1e-1
        C25 = EM[1,4]*1e-1
        C35 = EM[2,4]*1e-1
        C46 = EM[3,5]*1e-1
    else:
        C15 = EM[0,5]*1e-1
        C25 = EM[1,5]*1e-1
        C35 = EM[2,5]*1e-1
        C46 = EM[3,4]*1e-1

    f = C11*(C22*C55-C25**2)-C12*(C12*C55-C15*C25)+C15*(C12*C25-C15*C22)+C25*(C23*C35-C25*C33)
    g = C11*C22*C33-C11*C23**2-C22*C13**2-C33*C12**2+2*C12*C13*C23
    Omega=2*(C15*C25*(C33*C12-C13*C23)+C15*C35*(C22*C13-C12*C23)+C25*C35*(C11*C23-C12*C13)) -(C15**2*(C22*C33-C23**2)+C25**2*(C11*C33-C13**2)+C35**2*(C11*C22-C12**2))+g*C55
    GV = 1/15*(C11+C22+C33+3*(C44+C55+C66)-(C12+C13+C23))
    GR = 15*(4*((C33*C55-C35**2)*(C11+C22+C12) + (C23*C55-C25*C35)*(C11-C12-C23) + (C13*C35-C15*C33)*(C15+C25) + (C13*C55-C15*C35)*(C22-C12-C23-C13) + (C13*C25-C15*C23)*(C15-C25) + f)/Omega+3*(g/Omega+(C44+C66)/(C44*C66-C46**2)))**(-1)
    BV = (C11+C22+C33+2*(C12+C13+C23))/9
    BR = Omega*((C33*C55-C35**2)*(C11+C22-2*C12)+(C23*C55-C25*C35)*(2*C12-2*C11-C23) + (C13*C35-C15*C33)*(C15-2*C25)+(C13*C55-C15*C35)*(2*C12+2*C23-C13-2*C22)+2*(C13*C25-C15*C23)*(C25-C15)+f)**(-1)

    Br=BR
    Bv=BV
    Sr=GR
    Sv=GV
    B = (BR+BV)/2
    S = (GR+GV)/2
    Y = (9.*B*S)/(3.*B+S)
    nu = (3.*B-Y)/(6.*B)
    AU = 5*Sv/Sr+Bv/Br-6

    return BR, BV, B, GR, GV, S, AU, nu

