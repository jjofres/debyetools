"""Phase 3: EOS checks (derivative chain, identities at V0, MU2 design, fit objective). Run from repo root, numpy<2."""
import sys, os, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
import debyetools.potentials as potentials
from debyetools.aux_functions import load_V_E, load_cell
from scipy.optimize import least_squares

P4 = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
BPP = -6.0e-11  # B0'' [1/Pa], typical magnitude ~ -B'/B0
P5 = P4 + [BPP]
P_MP = [3.492281316e-01, 9.977375168e-01, 3.246481751e+00]
P_EAM = [3.647649855e-03, 1.643670214e+00, 1.201433529e-02, 2.110843838e-02, 2.099552421e-01,
         1.110019124e+00, 9.353164553e-01, 2.032247973e-06, 1.432174178e-01, 1.213592440e+00]
A = 4.0396918604; CELL = np.diag([A, A, A]); BAS = np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0]])
DER = ["E0", "dE0dV_T", "d2E0dV2_T", "d3E0dV3_T", "d4E0dV4_T", "d5E0dV5_T", "d6E0dV6_T"]

def build(name, force_positive=True):
    if name in ("MP", "EAM"):
        p = P_MP if name == "MP" else P_EAM
        e = getattr(potentials, name)("AlAlAlAl", CELL, BAS, 5.0, 3, units="J/mol", parameters=np.array(p))
        e.fitEOS(np.linspace(.9, 1.1, 5) * P4[1], np.zeros(5), initial_parameters=np.array(p), fit=False)
        return e
    p = list(P5 if name in ("BM4", "MU2") else P4)
    e = getattr(potentials, name)(parameters=list(p))
    e.fitEOS(np.linspace(.9, 1.1, 5) * P4[1], np.zeros(5), initial_parameters=np.array(p, float), fit=False)
    if force_positive:
        e.pEOS = np.array(p, float)  # undo the sign-flip quirks (see findings) to test the formulas themselves
    return e

def fd(f, V, h):
    # 6th-order central difference for the first derivative
    return (f(V + 3 * h) - 9 * f(V + 2 * h) + 45 * f(V + h) - 45 * f(V - h) + 9 * f(V - 2 * h) - f(V - 3 * h)) / (60 * h)

NAMES = ["BM", "BM3", "BM4", "MU", "MU2", "RV", "MG", "TB", "PT", "MP", "EAM"]
Vg = np.linspace(0.85, 1.2, 8) * P4[1]
print("== A. Derivative chain: max|d^nE(code) - FD[d^(n-1)E(code)]| / max|FD| over V/V0 in [0.85, 1.2]")
print("%5s " % "EOS" + " ".join("%10s" % d.replace("E0dV", "").replace("_T", "") for d in DER[1:]))
for n in NAMES:
    e = build(n)
    row = []
    for k in range(1, 7):
        f_lo, f_hi = getattr(e, DER[k - 1]), getattr(e, DER[k])
        nums = np.array([fd(lambda v: float(np.real(f_lo(v))), V, 2e-3 * V) for V in Vg])
        anas = np.array([float(np.real(f_hi(V))) for V in Vg])
        row.append(np.max(np.abs(anas - nums)) / np.max(np.abs(nums)))  # error relative to the scale of the derivative
    print("%5s " % n + " ".join(("%10.1e" % r) + ("*" if r > 1e-5 else " ") for r in row))
print("   (* = inconsistent: error > 1e-5; FD truncation/round-off floor is ~1e-8)")

print("\n== B. Identities at V = V0 (input parameters E0, V0, B0, B0', B0'')")
print("%5s %12s %12s %12s %12s %12s %14s" % ("EOS", "E(V0)-E0", "E'(V0)/B0", "V0E''/B0-1", "B'-B0'", "B''/B0''-1", "attr V0/V0-1"))
for n in ["BM", "BM3", "BM4", "MU", "MU2", "RV", "MG", "TB", "PT"]:
    e = build(n); V0 = P4[1]
    E = [float(getattr(e, d)(V0)) for d in DER[:5]]
    B = V0 * E[2]; dB = E[2] + V0 * E[3]; d2B = 2 * E[3] + V0 * E[4]
    Bp = -dB / E[2]
    dBp = -(d2B * E[2] - dB * E[3]) / E[2] ** 2
    Bpp = dBp / (-E[2])
    s = "%12.3e" % (Bpp / BPP - 1) if n in ("BM4", "MU2") else "%12s" % "-"
    print("%5s %12.3e %12.3e %12.3e %12.3e %s %14.3e" % (n, E[0] - P4[0], E[1] / P4[2], B / P4[2] - 1, Bp - P4[3], s, e.V0 / V0 - 1))

print("\n== C. MU2: derivatives vs FD of its own E0, and vs 2nd-order Murnaghan pressure [C23 eq.16]")
e = build("MU2"); E0_, V0, B0, Bp, Bpp = P5
G = np.sqrt(Bp ** 2 - 2 * B0 * Bpp)
P_mu2 = lambda V: 2 * B0 / Bp / (G / Bp * ((V0 / V) ** G + 1) / ((V0 / V) ** G - 1) - 1)
e_bm4 = build("BM4")
for V in [0.9 * V0, 0.95 * V0, 1.05 * V0, 1.15 * V0]:
    print("  V/V0=%.2f  -dE0dV(MU2)=%.6e  P_Murnaghan2=%.6e  -FD[E0(MU2)]=%.6e  E0(MU2)-E0(BM4)=%.2e" % (
        V / V0, -e.dE0dV_T(V), P_mu2(V), -fd(e.E0, V, 2e-3 * V), e.E0(V) - e_bm4.E0(V)))

print("\n== D. Sign-convention quirks (as a user would call them)")
for n in ["BM4", "MU2"]:
    p = list(P5)
    e1 = getattr(potentials, n)(parameters=p)
    print("  %s(parameters=P) -> caller's list B0 now %.3e ; E0(V0) = %r" % (n, p[2], e1.E0(V0) if hasattr(e1, 'pEOS') else None))
    e2 = getattr(potentials, n)(); e2.fitEOS(Vg, np.zeros_like(Vg), initial_parameters=np.array(P5), fit=False)
    print("  %s().fitEOS(fit=False, P) -> pEOS[2]=%.3e ; E0(V0)=%r" % (n, e2.pEOS[2], float(e2.E0(V0))))

print("\n== E. Fit objective: code (residuals squared inside least_squares => sum r^4) vs true least squares, Al DFT")
V, E = load_V_E("tests/inpt_files/Al_fcc/SUMMARY.fcc", "tests/inpt_files/Al_fcc/CONTCAR.5", units="J/mol")
for n in ["BM", "RV", "MU", "PT", "BM4"]:
    p0 = np.array(P5 if n == "BM4" else P4, float)
    e = getattr(potentials, n)(); e.fitEOS(V, E, initial_parameters=p0.copy())
    pc = np.array(e.pEOS, float)
    res = lambda p: np.array([e.E04min(v, p) for v in V]) - E
    pl = least_squares(res, pc, x_scale=np.abs(pc))["x"]
    rc, rl = np.sqrt(np.mean(res(pc) ** 2)), np.sqrt(np.mean(res(pl) ** 2))
    print("  %-4s code: V0=%.6e B0=%.4e B'=%.4f rms=%.3f J/mol | L2: V0=%.6e B0=%.4e B'=%.4f rms=%.3f J/mol | dB0=%+.2e dB'=%+.2e" % (
        n, pc[1], pc[2], pc[3], rc, pl[1], pl[2], pl[3], rl, pc[2] / pl[2] - 1, pc[3] - pl[3]))
