"""Phase 5b: electronic, defects, anharmonicity (excess A(V)T^2), Xs: derivative chain vs FD and S=-dF/dT, E=F+TS. Run from repo root."""
import sys, os, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
from debyetools.electronic import Electronic
from debyetools.defects import Defects
from debyetools.anharmonicity import Anharmonicity
from debyetools.XS import Xs

V0, B0 = 9.929931142e-06, 7.618619745e+10
objs = {
    "Electronic": Electronic(4.2285e-01, -1.6277e+04, 3.0e8, -2.0e13),
    "Defects": Defects(8.46, 1.69, 933, 0.1, B0, V0),
    "Anharmonicity": Anharmonicity(1e-4, -5.0, 2.0e5),
    "Xs": Xs(10., 0.01, 1e-6, 1e-9, 0.1, 1e3),
}
FV = [("dFdV_T", "F", "V"), ("dFdT_V", "F", "T"), ("d2FdV2_T", "dFdV_T", "V"), ("d2FdT2_V", "dFdT_V", "T"),
      ("d2FdVdT", "dFdV_T", "T"), ("d3FdV3_T", "d2FdV2_T", "V"), ("d3FdV2dT", "d2FdV2_T", "T"),
      ("d3FdVdT2", "d2FdVdT", "T"), ("d4FdV4_T", "d3FdV3_T", "V")]
PTS = [(T, f * V0) for T in (300., 900., 1500.) for f in (0.97, 1.02, 1.06)]

def fd1(f, x, h):
    return (f(x + 3 * h) - 9 * f(x + 2 * h) + 45 * f(x + h) - 45 * f(x - h) + 9 * f(x - 2 * h) - f(x - 3 * h)) / (60 * h)

print("== derivative chain: max|code - FD| / max(|FD|,|code|);  * > 1e-6")
print("%-14s " % "" + " ".join("%10s" % h[0][:10] for h in FV) + "   S=-dF/dT   E=F+TS")
for name, o in objs.items():
    row = []
    for hi, lo, var in FV:
        f_lo, f_hi = getattr(o, lo), getattr(o, hi)
        num = np.array([fd1(lambda v: f_lo(T, v), V, 1e-3 * V) if var == "V" else fd1(lambda t: f_lo(t, V), T, 1e-3 * T) for T, V in PTS])
        ana = np.array([f_hi(T, V) for T, V in PTS], float)
        sc = max(np.max(np.abs(num)), np.max(np.abs(ana)))
        row.append(np.max(np.abs(ana - num)) / sc if sc > 1e-300 else 0.0)
    s_ok = max(abs(o.S(T, V) + o.dFdT_V(T, V)) / max(abs(o.S(T, V)), 1e-300) for T, V in PTS)
    e_ok = max(abs(o.E(T, V) - o.F(T, V) - T * o.S(T, V)) / max(abs(o.E(T, V)), 1e-300) for T, V in PTS)
    print("%-14s " % name + " ".join(("%10.1e" % r) + ("*" if r > 1e-6 else " ") for r in row) + "  %9.1e  %9.1e" % (s_ok, e_ok))

d = objs["Defects"]
print("\n== Defects vs [C23] eqs.(10)-(11): F = -N_A k_B T exp(-(dH - T dS)/k_B T), dH = E0 - dV(1 - V0/V) B0, dV = a V0/N_A")
kB, NA = 1.38064852e-23, 6.022140857e23
for T, V in PTS[:3]:
    dH = 8.46 * kB * 933 - 0.1 * V0 / NA * (1 - V0 / V) * B0
    Fp = -NA * kB * T * np.exp(-(dH - T * 1.69 * kB) / (kB * T))
    print("  T=%g V/V0=%.2f  code F=%.6e  paper F=%.6e  rel %.1e" % (T, V / V0, d.F(T, V), Fp, d.F(T, V) / Fp - 1))
