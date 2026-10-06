"""Phase 3: impact of the wrong d5/d6 derivatives (RV d6, EAM d5/d6) on eval_props. Instance-level override, no package change."""
import sys, os, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
exec(open("review/phase3/eos_checks.py").read().split("NAMES =")[0])
from debyetools.ndeb import nDeb
T = np.array([100., 300., 600., 900.])
for name, fix in [("RV", ["d6E0dV6_T"]), ("EAM", ["d5E0dV5_T", "d6E0dV6_T"])]:
    e = build(name)
    nd = nDeb(0.32, 0.0269815, (0, 1), e, [0, 0, 0, 0], (8.46, 1.69, 933, 0.0), (0, 0, 0), mode="jjsl")
    V = np.full_like(T, e.V0 * 1.02)
    a = nd.eval_props(T.copy(), V.copy(), P=0)
    lower = {"d5E0dV5_T": e.d4E0dV4_T, "d6E0dV6_T": e.d5E0dV5_T}
    for k in fix:  # replace by FD of the (verified) lower derivative
        f = lower[k] if k == "d5E0dV5_T" else (lambda v, e=e: fd(lambda u: float(e.d5E0dV5_T(u)), v, 2e-3 * v))
        g = (lambda v, f=f: fd(lambda u: float(f(u)), v, 2e-3 * v)) if k == "d5E0dV5_T" else f
        setattr(e, k, (lambda v, g=g: np.array([g(x) for x in np.atleast_1d(v)]) if np.ndim(v) else g(v)))
    b = nd.eval_props(T.copy(), V.copy(), P=0)
    print("== %s (fixed: %s) relative change of properties at V=1.02 V0" % (name, ", ".join(fix)))
    for key in ["Kt", "Ktp", "Ktpp", "Ksp", "G^2", "Cp", "a"]:
        print("   %-5s " % key + " ".join("%10.2e" % (a[key][i] / b[key][i] - 1) for i in range(len(T))))
