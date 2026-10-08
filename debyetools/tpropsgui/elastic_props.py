import numpy as np
from scipy import optimize
from scipy.optimize import minimize
from itertools import product
"""
This module contains functions to calculate elastic properties from the elastic constants
as in ELATE by Romain Gaillac and François-Xavier Coudert.
"""

def dirVec(theta, phi):
    """Return a unit vector associated with angles theta and phi"""
    return [np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)]
def dirVec2(theta, phi, chi):
    """Return the second unit vector associated with angles (theta, phi, chi)"""
    return [np.cos(theta)*np.cos(phi)*np.cos(chi) - np.sin(phi)*np.sin(chi),
            np.cos(theta)*np.sin(phi)*np.cos(chi) + np.cos(phi)*np.sin(chi),
            - np.sin(theta)*np.cos(chi)]

def SVoigtCoeff(p,q):
            return 1. / ((1+p//3)*(1+q//3))
def calc_Smat(Cs):
    mat = np.array(Cs)
    # Check that is is symmetric, or make it symmetric
    if np.linalg.norm(np.tril(mat, -1)) == 0:
        mat = mat + np.triu(mat, 1).transpose()
    if np.linalg.norm(np.triu(mat, 1)) == 0:
        mat = mat + np.tril(mat, -1).transpose()
    if np.linalg.norm(mat - mat.transpose()) > 1e-3:
        raise ValueError("should be symmetric, or triangular")
    elif np.linalg.norm(mat - mat.transpose()) > 0:
        # It was almost symmetric: symmetrize it completely
        mat = 0.5 * (mat + mat.transpose())

    VoigtMat = [[0, 5, 4], [5, 1, 3], [4, 3, 2]]
    # CVoigt = mat
    SVoigt = np.linalg.inv(Cs)
    return [[[[ SVoigtCoeff(VoigtMat[i][j], VoigtMat[k][l]) * SVoigt[VoigtMat[i][j]][VoigtMat[k][l]]
                         for i in range(3) ] for j in range(3) ] for k in range(3) ] for l in range(3) ]

def Young_tp(x, y, Smat):
    a = dirVec(x, y)
    r = sum([ a[i]*a[j]*a[k]*a[l] * Smat[i][j][k][l]
                for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
    return 1/r

def LinearCompressibility_tp(x, y, Smat):
        a = dirVec(x, y)
        r = sum([ a[i]*a[j] * Smat[i][j][k][k]
                  for i in range(3) for j in range(3) for k in range(3) ])
        return 1000 * r

def shear(x, Smat):
        a = dirVec(x[0], x[1])
        b = dirVec2(x[0], x[1], x[2])
        r = sum([ a[i]*b[j]*a[k]*b[l] * Smat[i][j][k][l]
                  for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
        return 1/(4*r)

def Poisson(x, Smat):
        a = dirVec(x[0], x[1])
        b = dirVec2(x[0], x[1], x[2])
        r1 = sum([ a[i]*a[j]*b[k]*b[l] * Smat[i][j][k][l]
                   for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
        r2 = sum([ a[i]*a[j]*a[k]*a[l] * Smat[i][j][k][l]
                   for i in range(3) for j in range(3) for k in range(3) for l in range(3) ])
        return -r1/r2

import sys
def f1f2(x, Smat, fname):
     funct = getattr(sys.modules[__name__], fname)
     return lambda z: funct([x[0], x[1], z[0]], Smat), lambda z: -funct([x[0], x[1], z[0]], Smat)

def _transverse_extrema(theta, phi, Smat):
    """Exact extrema over the transverse direction chi of the shear modulus and Poisson's ratio for the
    direction(s) (theta, phi) (G19). With n = cos(chi) e1 + sin(chi) e2 (e1, e2 = dirVec2(theta, phi, 0 / pi/2)),
    1/(4G) = n.B.n with B_jl = S_ijkl a_i a_k, and nu = -(n.A.n) / (a.a.S.a.a) with A_kl = S_ijkl a_i a_j:
    the extrema over chi are the eigenvalues of the 2x2 projections of B and A (was: Powell from chi = pi/2,
    which can stop at a local optimum).
    theta, phi: scalars or arrays of the same shape. Returns G_min, G_max, nu_min, nu_max (same shape)."""
    T = np.asarray(Smat, dtype=float)
    theta, phi = np.broadcast_arrays(np.asarray(theta, dtype=float), np.asarray(phi, dtype=float))
    shape = theta.shape
    t, p = theta.ravel(), phi.ravel()
    a = np.stack([np.sin(t) * np.cos(p), np.sin(t) * np.sin(p), np.cos(t)], axis=1)
    e1 = np.stack([np.cos(t) * np.cos(p), np.cos(t) * np.sin(p), -np.sin(t)], axis=1)
    e2 = np.stack([-np.sin(p), np.cos(p), np.zeros_like(p)], axis=1)
    P = np.stack([e1, e2], axis=1)  # (n, 2, 3)
    B = np.einsum('ijkl,ni,nk->njl', T, a, a)
    A = np.einsum('ijkl,ni,nj->nkl', T, a, a)
    s = np.einsum('ijkl,ni,nj,nk,nl->n', T, a, a, a, a)
    lb = np.linalg.eigvalsh(np.einsum('nax,nxy,nby->nab', P, B, P))
    la = np.linalg.eigvalsh(np.einsum('nax,nxy,nby->nab', P, A, P))
    G_min, G_max = 1 / (4 * lb[:, 1]), 1 / (4 * lb[:, 0])
    nu_min, nu_max = -la[:, 1] / s, -la[:, 0] / s
    return tuple(v.reshape(shape) for v in (G_min, G_max, nu_min, nu_max))

def shear2D(x, Smat):
    """Minimum and maximum shear modulus over the transverse directions, for the direction x = (theta, phi)."""
    G_min, G_max, _, _ = _transverse_extrema(x[0], x[1], Smat)
    return float(G_min), float(G_max)

def Poisson2D(x, Smat):
    """Poisson's ratio for the direction x = (theta, phi): (min(0, nu_min), max(0, nu_min), nu_max) as floats –
    the negative part of the minimum, its positive part and the maximum (the three plotted curves)."""
    _, _, nu_min, nu_max = _transverse_extrema(x[0], x[1], Smat)
    return min(0.0, float(nu_min)), max(0.0, float(nu_min)), float(nu_max)

def averages(CVoigt):
    SVoigt = np.linalg.inv(CVoigt)
    A = (CVoigt[0][0] + CVoigt[1][1] + CVoigt[2][2]) / 3
    B = (CVoigt[1][2] + CVoigt[0][2] + CVoigt[0][1]) / 3
    C = (CVoigt[3][3] + CVoigt[4][4] + CVoigt[5][5]) / 3
    a = (SVoigt[0][0] + SVoigt[1][1] + SVoigt[2][2]) / 3
    b = (SVoigt[1][2] + SVoigt[0][2] + SVoigt[0][1]) / 3
    c = (SVoigt[3][3] + SVoigt[4][4] + SVoigt[5][5]) / 3

    KV = (A + 2*B) / 3
    GV = (A - B + 3*C) / 5

    KR = 1 / (3*a + 6*b)
    GR = 5 / (4*a - 4*b + 3*c)

    KH = (KV + KR) / 2
    GH = (GV + GR) / 2

    return [ [KV, 1/(1/(3*GV) + 1/(9*KV)), GV, (1 - 3*GV/(3*KV+GV))/2],
                [KR, 1/(1/(3*GR) + 1/(9*KR)), GR, (1 - 3*GR/(3*KR+GR))/2],
                [KH, 1/(1/(3*GH) + 1/(9*KH)), GH, (1 - 3*GH/(3*KH+GH))/2] ]

# Define Born stability criteria for cubic crystals
def check_born_stability(Cmat):
    c11, c12, c44 = Cmat[0][0], Cmat[0][1], Cmat[3][3]
    stability = f'c11 > 0: {c11 > 0}\nc44 > 0: {c44 > 0}\nc11 - c12 > 0: {c11 - c12 > 0}\nc11 + 2*c12 > 0: {c11 + 2 * c12 > 0}'
    return stability



def _directional(fstr, opt_ix, theta, phi, Smat):
    """Directional quantity on arrays of angles: 'Young_tp', 'LinearCompressibility_tp' (signed, TPa^-1 for C in
    GPa), 'shear2D' (opt_ix 0: min over chi, 1: max over chi), 'Poisson2D' (opt_ix 1: min over chi, signed;
    2: max over chi; 0: min(0, min over chi))."""
    T = np.asarray(Smat, dtype=float)
    t, p = np.asarray(theta, dtype=float), np.asarray(phi, dtype=float)
    a = np.stack([np.sin(t) * np.cos(p), np.sin(t) * np.sin(p), np.cos(t)], axis=-1)
    if fstr == 'Young_tp':
        return 1 / np.einsum('ijkl,...i,...j,...k,...l->...', T, a, a, a, a)
    if fstr == 'LinearCompressibility_tp':
        return 1000 * np.einsum('ijkk,...i,...j->...', T, a, a)
    G_min, G_max, nu_min, nu_max = _transverse_extrema(t, p, Smat)
    if fstr == 'shear2D':
        return [G_min, G_max][opt_ix]
    if fstr == 'Poisson2D':
        return [np.minimum(0, nu_min), nu_min, nu_max][opt_ix]
    raise ValueError(fstr)

def get_min_max_directions(Smat, fstr, opt_ix=0, n_dirs=4000):
    """Minimum and maximum of a directional quantity over all directions, and the directions (G22): every
    quantity is even in the direction, so n_dirs quasi-uniform directions of a hemisphere (Fibonacci) are scanned,
    and the 3 best candidates for the minimum and for the maximum are refined with Nelder-Mead in (theta, phi).
    Signed values (was: |f|, and BFGS started only from symmetric directions, where it does not move).
    Returns min, max, direction of the min, direction of the max."""
    k = np.arange(n_dirs) + 0.5
    theta = np.arccos(1 - k / n_dirs)  # cos(theta) uniform in (0, 1]
    phi = np.pi * (1 + 5 ** 0.5) * k
    vals = _directional(fstr, opt_ix, theta, phi, Smat)
    f = lambda x: float(_directional(fstr, opt_ix, np.array([x[0]]), np.array([x[1]]), Smat)[0])
    out = []
    for sign in (1, -1):
        best = None
        for ix in np.argsort(sign * vals)[:3]:
            r = minimize(lambda x: sign * f(x), [theta[ix], phi[ix]], method='Nelder-Mead',
                         options={'xatol': 1e-7, 'fatol': 1e-10})
            cand = (r.fun, r.x) if r.fun <= sign * vals[ix] else (sign * vals[ix], [theta[ix], phi[ix]])
            if best is None or cand[0] < best[0]:
                best = cand
        out.append((sign * best[0], dirVec(best[1][0], best[1][1])))
    (minf, dir_min), (maxf, dir_max) = out
    return minf, maxf, dir_min, dir_max

def run_script(EM):
    # input
    resdata = {}
    txt2output = ''
    txt2output =txt2output + 'Stiffness matrix: (in GPa)\n'
    for c in EM:
        for ci in c:
            txt2output = txt2output + f'{ci:.3f}' + '\t'
        txt2output = txt2output + '\n'
    txt2output = txt2output + '\n'
    resdata['Cijs'] = EM

    # Check stability
    # stability_results = check_born_stability(EM)
    # txt2output = txt2output + 'Born staibily: \n'+ stability_results + '\n'
    # txt2output = txt2output + '\n'
    # resdata['Born_stability'] = stability_results

    #- Eigenvalues of the stiffness matrix (lambda 1 to 6).
    # Calculate the eigenvalues of the stiffness matrix
    eigenvalues = np.linalg.eigvals(EM)
    # Display the eigenvalues
    txt2output = txt2output + "Eigenvalues of the stiffness matrix (in GPa):" + '\n'

    txt2output = txt2output + '\t'.join([f"λ{i+1}" for i in range(len(eigenvalues))])+ '\n'
    txt2output = txt2output + '\t'.join([f"{eigenvalue.real:.2f}" for eigenvalue in eigenvalues])+ '\n'
    if np.all(eigenvalues > 0):
        txt2output = txt2output + 'The material is mechanically stable' + '\n'
    txt2output = txt2output + '\n'

    resdata['eigenvalues'] = eigenvalues


    #Average properties (Bulk modulus, Young's modulus, Shear modulus, Poisson's ratio) according to Voigt, Reuss, Hill.
    Smat = calc_Smat(EM)

    Voigt, Reuss, Hill = averages(EM)
    # averages() returns [K, E, G, nu] (was unpacked as K, G, E, nu: E and G swapped, A^U and G/K wrong, G21)
    KV, EV, GV, nuV = Voigt
    KR, ER, GR, nuR = Reuss
    KH, EH, GH, nuH = Hill
    resdata['average_properties'] = {'Voigt': Voigt, 'Reuss': Reuss, 'Hill': Hill}

    # Print results
    txt2output = txt2output + "Average properties (Bulk modulus (K), Young's modulus (E), Shear modulus (G), Poisson's ratio (ν)):" + '\n'
    txt2output = txt2output + "Method:    K(GPa)\tE(GPa)\tG(GPa)\tν" + '\n'
    txt2output = txt2output + f'Voigt:    {KV:.3f}\t{EV:.3f}\t{GV:.3f}\t{nuV:.3f}' + '\n'
    txt2output = txt2output + f'Reuss:    {KR:.3f}\t{ER:.3f}\t{GR:.3f}\t{nuR:.3f}' + '\n'
    txt2output = txt2output + f'Hill:     {KH:.3f}\t{EH:.3f}\t{GH:.3f}\t{nuH:.3f}' + '\n'
    txt2output = txt2output + f'Universal anisotropy index (A^U): {KV/KR+5*GV/GR -6:.4f}'+'\n'
    txt2output = txt2output + f'G/K: {GH/KH:.5f}' + '\n'
    txt2output = txt2output + '\n'

    minf_Y, maxf_Y, cd_min_Y, cd_max_Y = get_min_max_directions(Smat,'Young_tp')
    anis_Y = minf_Y/maxf_Y
    minf_LC, maxf_LC, cd_min_LC, cd_max_LC = get_min_max_directions(Smat,'LinearCompressibility_tp')
    anis_LC = minf_LC/maxf_LC
    minf_S0, maxf_S0, cd_min_S0, cd_max_S0 = get_min_max_directions(Smat,'shear2D', 0)
    anis_S0 = minf_S0/maxf_S0
    minf_S1, maxf_S1, cd_min_S1, cd_max_S1 = get_min_max_directions(Smat,'shear2D', 1)
    anis_S1 = minf_S1/maxf_S1
    minf_P1, maxf_P1, cd_min_P1, cd_max_P1 = get_min_max_directions(Smat,'Poisson2D', 1)
    anis_P1 = minf_P1/maxf_P1
    minf_P2, maxf_P2, cd_min_P2, cd_max_P2 = get_min_max_directions(Smat,'Poisson2D', 2)
    anis_P2 = minf_P2/maxf_P2

    resdata['variation_properties'] = {'Young': {'min': minf_Y, 'max': maxf_Y, 'anisotropy': anis_Y, 'min_direction': cd_min_Y, 'max_direction': cd_max_Y},
                                        'LinearCompressibility': {'min': minf_LC, 'max': maxf_LC, 'anisotropy': anis_LC, 'min_direction': cd_min_LC, 'max_direction': cd_max_LC},
                                        'Shear': {'min': minf_S0, 'max': maxf_S0, 'anisotropy': anis_S0, 'min_direction': cd_min_S0, 'max_direction': cd_max_S0},
                                        'Shear2': {'min': minf_S1, 'max': maxf_S1, 'anisotropy': anis_S1, 'min_direction': cd_min_S1, 'max_direction': cd_max_S1},
                                        'Poisson': {'min': minf_P1, 'max': maxf_P1, 'anisotropy': anis_P1, 'min_direction': cd_min_P1, 'max_direction': cd_max_P1},
                                        'Poisson2': {'min': minf_P2, 'max': maxf_P2, 'anisotropy': anis_P2, 'min_direction': cd_min_P2, 'max_direction': cd_max_P2}
                                        }

    txt2output = txt2output +  "Variations of the elastic moduli:" + '\n'
    txt2output = txt2output +  "           Young's mod. | Lin. comp. | Shear mod.| Poisson's ratio" + '\n'
    txt2output = txt2output +  '          --------------|------------|-----------|------------------' + '\n'
    txt2output = txt2output + f'Min:       {minf_Y:.3f}\t|  {minf_LC:.3f}     |\t{minf_S0:.3f}\t |\t{minf_P1:.3f}' + '\n'
    txt2output = txt2output + f'                        |            |\t{minf_S1:.3f}\t |\t{minf_P2:.3f}' + '\n'
    txt2output = txt2output +  '          --------------|------------|-----------|------------------' + '\n'
    txt2output = txt2output + f'Max:       \t{maxf_Y:.3f}\t|  {maxf_LC:.3f}     |\t{maxf_S0:.3f}\t |\t{maxf_P1:.3f}' + '\n'
    txt2output = txt2output + f'            \t\t|            |\t{maxf_S1:.3f}\t |\t{maxf_P2:.3f}' + '\n'
    txt2output = txt2output + '          --------------|------------|-----------|------------------' + '\n'
    txt2output = txt2output + f'Anisotropy:\t{anis_Y:.3f}\t|  {anis_LC:.3f}     |\t{anis_S0:.3f}\t |\t{anis_P1:.3f}'   + '\n'
    txt2output = txt2output + f'            \t\t|            |\t{anis_S1:.3f}\t |\t{anis_P2:.3f}' + '\n'
    txt2output = txt2output + '          --------------|------------|-----------|------------------' + '\n'
    txt2output = txt2output + f'direction (min): {cd_min_Y[0]:.3f}\t|  {cd_min_LC[0]:.3f}     |  {cd_min_S0[0]:.3f}\t |\t{cd_min_P1[0]:.3f}' + '\n'
    txt2output = txt2output + f'                 {cd_min_Y[1]:.3f}\t|  {cd_min_LC[1]:.3f}     |  {cd_min_S0[1]:.3f}\t |\t{cd_min_P1[1]:.3f}' + '\n'
    txt2output = txt2output + f'                 {cd_min_Y[2]:.3f}\t|  {cd_min_LC[2]:.3f}     |  {cd_min_S0[2]:.3f}\t |\t{cd_min_P1[2]:.3f}' + '\n'
    txt2output = txt2output + f'                        |            |  {cd_min_S1[0]:.3f}\t |\t{cd_min_P2[0]:.3f}' + '\n'
    txt2output = txt2output + f'                        |            |  {cd_min_S1[1]:.3f}\t |\t{cd_min_P2[1]:.3f}' + '\n'
    txt2output = txt2output + f'                        |            |  {cd_min_S1[2]:.3f}\t |\t{cd_min_P2[2]:.3f}' + '\n'
    txt2output = txt2output + '          --------------|------------|-----------|------------------' + '\n'
    txt2output = txt2output + f'direction (max): {cd_max_Y[0]:.3f}\t|  {cd_max_LC[0]:.3f}     |  {cd_max_S0[0]:.3f}\t |\t{cd_max_P1[0]:.3f}' + '\n'
    txt2output = txt2output + f'                 {cd_max_Y[1]:.3f}\t|  {cd_max_LC[1]:.3f}     |  {cd_max_S0[1]:.3f}\t |\t{cd_max_P1[1]:.3f}' + '\n'
    txt2output = txt2output + f'                 {cd_max_Y[2]:.3f}\t|  {cd_max_LC[2]:.3f}     |  {cd_max_S0[2]:.3f}\t |\t{cd_max_P1[2]:.3f}' + '\n'
    txt2output = txt2output + f'                        |            |  {cd_max_S1[0]:.3f}\t |\t{cd_max_P2[0]:.3f}' + '\n'
    txt2output = txt2output + f'                        |            |  {cd_max_S1[1]:.3f}\t |\t{cd_max_P2[1]:.3f}' + '\n'
    txt2output = txt2output + f'                        |            |  {cd_max_S1[2]:.3f}\t |\t{cd_max_P2[2]:.3f}' + '\n'
    txt2output = txt2output + '\n'


    return txt2output, resdata


def run_script_plots(axs, EM):
    Smat = calc_Smat(EM)
    axY, axL, axS, axP = axs

    Young_funct = lambda t, p: Young_tp(t, p, Smat)
    LinearCompressibility_funct = lambda t, p: LinearCompressibility_tp(t, p, Smat)
    Shear2D_funct = lambda t, p: shear2D([t, p], Smat)
    Poisson2D_funct = lambda t, p: Poisson2D([t, p], Smat)

    phi = np.linspace(0, 2 * np.pi, 100)
    theta = np.linspace(0, 2*np.pi, 100)

    fY = np.vectorize(Young_funct)
    fL = np.vectorize(LinearCompressibility_funct)
    # explicit float outputs: np.vectorize takes the output type from the first call, and an int 0 there turned
    # every negative Poisson's ratio into 0 (G18)
    fS = np.vectorize(Shear2D_funct, otypes=[float, float])
    fP = np.vectorize(Poisson2D_funct, otypes=[float, float, float])

    r_xyY = fY(np.pi / 2, phi)
    r_xzY = fY(-(theta+np.pi/2), 0)
    r_yzY = fY(-(theta+np.pi/2), np.pi/2)

    r_xyL = fL(np.pi / 2, phi)
    r_xzL = fL(-(theta+np.pi/2), 0)
    r_yzL = fL(-(theta+np.pi/2), np.pi/2)

    r_xyS = fS(np.pi/2, phi)
    r_xzS = fS(theta + np.pi/2, np.pi)
    r_yzS = fS(-(theta + np.pi/2), np.pi/2)

    r_xyP = fP(np.pi/2, phi)
    r_xzP = fP(theta + np.pi/2, np.pi)
    r_yzP = fP(-(theta + np.pi/2), np.pi/2)

    axY[0].plot(phi, r_xyY)
    axY[1].plot(phi, r_xzY)
    axY[2].plot(phi, r_yzY)

    # polar radius = |value|, origin at 0; negative values (negative linear compressibility, negative Poisson's
    # ratio) drawn in green as their magnitude (a negative radius moved the origin of the whole plot)
    for ax, r in zip(axL, [r_xyL, r_xzL, r_yzL]):
        ax.plot(phi, np.where(r >= 0, r, np.nan))
        if np.any(r < 0):
            ax.plot(phi, np.where(r < 0, -r, np.nan), color='g')

    axS[0].plot(phi, r_xyS[0], color='b')
    axS[0].plot(phi, r_xyS[1], color='r')

    axS[1].plot(theta, r_xzS[0], color='b')
    axS[1].plot(theta, r_xzS[1], color='r')

    axS[2].plot(theta, r_yzS[0], color='b')
    axS[2].plot(theta, r_yzS[1], color='r')

    axP[0].plot(phi, -r_xyP[0], color='g')
    axP[0].plot(phi, r_xyP[1], color='r')
    axP[0].plot(phi, r_xyP[2], color='b')

    axP[1].plot(theta, -r_xzP[0], color='g')
    axP[1].plot(theta, r_xzP[1], color='r')
    axP[1].plot(theta, r_xzP[2], color='b')

    axP[2].plot(theta, -r_yzP[0], color='g')
    axP[2].plot(theta, r_yzP[1], color='r')
    axP[2].plot(theta, r_yzP[2], color='b')

    axY[0].text(np.pi*1.1, axY[0].get_rmax() * 2.2, r'$E(\theta, \phi)~[GPa]$', rotation=90)
    axL[0].text(np.pi*1.1, axL[0].get_rmax() * 2.2, r'$\beta(\theta, \phi)~[TPa^{-1}]$', rotation=90)
    axS[0].text(np.pi*1.1, axS[0].get_rmax() * 2.2, r'$G(\theta, \phi, \chi)~[GPa]$', rotation=90)
    axP[0].text(np.pi*1.1, axP[0].get_rmax() * 2.2, r'$\nu(\theta, \phi, \chi)$', rotation=90)

    # axY[0].set_title('x-y plane')
    # axY[1].set_title('x-z plane')
    # axY[2].set_title('y-z plane')

    for ax in [axY, axL, axS, axP]:
        for i in range(3):
            ax[i].set_rmin(0)
            ax[i].tick_params(axis='y', labelsize=8, labelrotation=292.5)
    # plt.show()

    return axs



