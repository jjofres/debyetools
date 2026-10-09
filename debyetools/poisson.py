import numpy as np
from typing import Tuple


def _vrh(EM: np.ndarray) -> Tuple[float, float, float, float, float, float, float, float]:
    """
    Voigt, Reuss and Hill averages from a 6x6 stiffness matrix (any symmetry).

    Voigt: K_V = [C11+C22+C33 + 2(C12+C13+C23)]/9, G_V = [C11+C22+C33 - (C12+C13+C23) + 3(C44+C55+C66)]/15.
    Reuss from the compliance S = C^-1: K_R = 1/[S11+S22+S33 + 2(S12+S13+S23)],
    G_R = 15/[4(S11+S22+S33) - 4(S12+S13+S23) + 3(S44+S55+S66)].
    These sums are invariant under any reordering of the three shear components, so the VASP order
    (XX YY ZZ XY YZ ZX) and the Voigt order (XX YY ZZ YZ ZX XY) give the same result. The matrix is
    symmetrised, (C + C^T)/2, before inversion.

    :return: K_R, K_V, K_H, G_R, G_V, G_H, A_U, nu (moduli in the units of EM)
    """
    C = np.asarray(EM, dtype=float)
    if C.shape != (6, 6):
        raise ValueError('poisson_ratio: the elastic moduli matrix must be 6x6, got %s' % (C.shape,))
    C = 0.5 * (C + C.T)
    S = np.linalg.inv(C)
    KV = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[0, 2] + C[1, 2])) / 9
    GV = (C[0, 0] + C[1, 1] + C[2, 2] - (C[0, 1] + C[0, 2] + C[1, 2]) + 3 * (C[3, 3] + C[4, 4] + C[5, 5])) / 15
    KR = 1 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
    GR = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2]) - 4 * (S[0, 1] + S[0, 2] + S[1, 2]) + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))
    K = (KR + KV) / 2
    G = (GR + GV) / 2
    Y = (9. * K * G) / (3. * K + G)
    nu = (3. * K - Y) / (6. * K)
    AU = 5 * GV / GR + KV / KR - 6
    return KR, KV, K, GR, GV, G, AU, nu


def poisson_ratio(EM: np.ndarray, quiet: bool = False) -> float|Tuple[float,float,float,float,float,float,float,float]:
    """
    Poisson's ratio from the elastic moduli (stiffness) matrix, Voigt-Reuss-Hill average:
    nu = (3K - Y)/(6K), Y = 9KG/(3K + G), K = (K_V + K_R)/2, G = (G_V + G_R)/2.

    The Reuss bounds are computed from the compliance S = C^-1, which is exact for any crystal symmetry
    (cubic ... triclinic) and independent of the order of the shear components (VASP or Voigt).

    :param EM: 6x6 elastic moduli matrix. nu is unit-free; with quiet=True the input is taken in kBar
               (as returned by aux_functions.load_EM and get_elastic.get_EM) and the moduli are returned in GPa.
    :type EM: np.ndarray
    :param quiet: if True, return all VRH quantities (see quiet_pa) instead of nu only.
    :type quiet: bool
    :return: Poisson's ratio, or (B_R, B_V, B, G_R, G_V, G, A_U, nu) if quiet.
    :rtype: float
    """
    if quiet:
        return quiet_pa(EM)
    return _vrh(EM)[-1]


def quiet_pa(EM: np.ndarray) -> Tuple[float,float,float,float,float,float,float,float]:
    """
    Voigt-Reuss-Hill quantities from the elastic moduli matrix.

    :param EM: 6x6 elastic moduli matrix in kBar (as returned by load_EM / get_EM).
    :type EM: np.ndarray
    :return: B_R, B_V, B, G_R, G_V, G (bulk and shear moduli in GPa), A_U (universal anisotropy index), nu
    :rtype: Tuple[float,float,float,float,float,float,float,float]
    """
    return _vrh(np.asarray(EM, dtype=float) * 1e-1)
