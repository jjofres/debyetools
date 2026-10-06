"""Phase 4: vibrational.py checks. Run from repo root with numpy<2.
A: theta_D derivatives vs FD, all modes, intrinsic anharmonicity off/on, r=1/2.
B: F_vib derivatives vs FD.
C: Grueneisen parameter of the non-jj modes vs gamma = B'/2 + a  (Slater -1/6, DM -1/2, free-volume/VZ -5/6).
D: state dependence (V0_DM) and the 653 clamp."""
import sys, os, warnings, itertools
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
import debyetools.potentials as potentials
from debyetools.ndeb import nDeb

P = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
eos = potentials.BM(parameters=P); eos.fitEOS(np.linspace(.9, 1.1, 5) * P[1], np.zeros(5), initial_parameters=np.array(P), fit=False)
NU, M = 0.31681, 0.0269815
MODES = ["jjsl", "jjdm", "jjfv", "Sl", "DM", "VZ", "mfv"]

def make(mode, intanh, r=1):
    nd = nDeb(NU, M, intanh, eos, [0, 0, 0, 0], (8.46, 1.69, 933, 0.0), (0, 0, 0), mode=mode, r=r)
    if "jj" not in mode:
        nd.vib.V0_DM = eos.V0
    return nd.vib

def at(vib, T, V):
    vib.set_int_anh(T, V); vib.set_theta(T, V)
    return vib

def fd1(f, x, h):
    return (f(x + 3 * h) - 9 * f(x + 2 * h) + 45 * f(x + h) - 45 * f(x - h) + 9 * f(x - 2 * h) - f(x - 3 * h)) / (60 * h)

# (name of checked quantity, name of lower quantity, variable)
TD = [("dtDdV_T", "tD", "V"), ("dtDdT_V", "tD", "T"), ("d2tDdV2_T", "dtDdV_T", "V"), ("d2tDdT2_V", "dtDdT_V", "T"),
      ("d2tDdVdT", "dtDdV_T", "T"), ("d3tDdV3_T", "d2tDdV2_T", "V"), ("d3tDdV2dT", "d2tDdV2_T", "T"),
      ("d3tDdVdT2", "d2tDdVdT", "T"), ("d4tDdV4_T", "d3tDdV3_T", "V")]
FV = [("dFdV_T", "F", "V"), ("dFdT_V", "F", "T"), ("d2FdV2_T", "dFdV_T", "V"), ("d2FdT2_V", "dFdT_V", "T"),
      ("d2FdVdT", "dFdV_T", "T"), ("d3FdV3_T", "d2FdV2_T", "V"), ("d3FdV2dT", "d2FdV2_T", "T"),
      ("d3FdVdT2", "d2FdVdT", "T"), ("d4FdV4_T", "d3FdV3_T", "V")]
PTS = [(T, f * eos.V0) for T in (50., 300., 900.) for f in (0.97, 1.02, 1.06)]

def val(vib, name, T, V):
    at(vib, T, V)
    if name.startswith("d") and "tD" in name or name == "tD":
        return float(np.real(getattr(vib, name)))
    return float(np.real(getattr(vib, name)(T, V)))

def check(vib, table):
    out = {}
    for hi, lo, var in table:
        num, ana = [], []
        for T, V in PTS:
            if var == "V":
                num.append(fd1(lambda v: val(vib, lo, T, v), V, 1e-3 * V))
            else:
                num.append(fd1(lambda t: val(vib, lo, t, V), T, 1e-3 * T))
            ana.append(val(vib, hi, T, V))
        num, ana = np.array(num), np.array(ana)
        scale = max(np.max(np.abs(num)), np.max(np.abs(ana)))
        out[hi] = np.max(np.abs(ana - num)) / scale if scale > 0 else 0.0
    return out

for title, table in [("A. theta_D derivatives", TD), ("B. F_vib derivatives", FV)]:
    print("== %s: max|code - FD| / max|FD| (3 T x 3 V points); * = > 1e-6" % title)
    print("%-26s " % "case" + " ".join("%10s" % h[0].replace("_T", "").replace("_V", "")[:10] for h in table))
    for mode, (ia_name, ia), r in itertools.product(MODES, [("no intanh", (0, 1)), ("intanh a0=-2e-5,m0=1.5", (-2e-5, 1.5))], [1, 2]):
        if r == 2 and mode not in ("jjsl", "Sl"):
            continue
        res = check(make(mode, ia, r), table)
        print("%-26s " % ("%s %s r=%d" % (mode, "anh" if ia[0] else "   ", r)) + " ".join(("%10.1e" % res[h[0]]) + ("*" if res[h[0]] > 1e-6 else " ") for h in table))
    print()

print("== C. Grueneisen parameter gamma = -dln(thD)/dlnV at V = V0 (no intanh), vs B0'/2 + a")
lit = {"Sl": -1 / 6, "DM": -1 / 2, "VZ": -5 / 6, "mfv": None, "jjsl": -1 / 6, "jjdm": -1 / 2, "jjfv": -5 / 6}
for mode in MODES:
    v = at(make(mode, (0, 1)), 300., eos.V0)
    g = -v.dtDdV_T * eos.V0 / v.tD
    ref = lit[mode]
    print("  %-5s a_DM=%-8s gamma=%.6f  B'/2 + a(lit) = %s" % (mode, getattr(v, "a_DM", "-"), g, "%.6f" % (P[3] / 2 + ref) if ref is not None else "n/a (no reference for -0.95)"))

print("\n== D1. State dependence: non-jj modes use V0_DM, which min_G overwrites with V(T_first)")
nd = nDeb(NU, M, (0, 1), eos, [0, 0, 0, 0], (8.46, 1.69, 933, 0.0), (0, 0, 0), mode="DM")
T = np.array([300.]); V = np.array([1.01 * eos.V0])
a = nd.eval_props(T.copy(), V.copy(), P=0)["Cp"][0]; v0a = nd.vib.V0_DM
nd.min_G(np.array([0.1, 300.]), eos.V0, P=0)
b = nd.eval_props(T.copy(), V.copy(), P=0)["Cp"][0]; v0b = nd.vib.V0_DM
print("  same (T,V): Cp before min_G = %.6f (V0_DM=%.6e)  after min_G = %.6f (V0_DM=%.6e)  rel diff %.2e" % (a, v0a, b, v0b, b / a - 1))

print("\n== D2. 653 clamp: S_vib = -dF/dT at very low T (jjsl, array input; scalar input raises IndexError when x >= 653)")
vib = make("jjsl", (0, 1)); V0 = eos.V0
for T in [0.3, 0.6, 1.0, 2.0]:
    Ta = np.array([T]); vib.set_int_anh(Ta, V0); vib.set_theta(Ta, V0)
    x = float(np.ravel(vib.tD / Ta)[0])
    s_ar = -float(np.ravel(vib.dFdT_V(Ta, V0))[0]); cv = -T * float(np.ravel(vib.d2FdT2_V(Ta, V0))[0])
    R = 8.314462618
    print("  T=%.1f x=%5.0f  S_vib=%.4e (Debye %.4e)  Cv_vib=%.4e (Debye %.4e)" % (T, x, s_ar, 4 * np.pi**4 / 5 * R / x**3, cv, 12 * np.pi**4 / 5 * R / x**3))
try:
    vib.set_int_anh(0.3, V0); vib.set_theta(0.3, V0); vib.dFdT_V(0.3, V0); print("  scalar T=0.3: OK")
except Exception as e:
    print("  scalar T=0.3 K: %s: %s" % (type(e).__name__, e))
