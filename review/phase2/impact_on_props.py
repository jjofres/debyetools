"""Phase 2: impact of D_3 inaccuracies on eval_props (monkeypatch exact Debye functions, no package change)."""
import sys, os, warnings
import numpy as np, mpmath as mp
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
import debyetools.vibrational as vib
import debyetools.potentials as potentials
from debyetools.ndeb import nDeb
mp.mp.dps = 40

def _ref(x):
    x = mp.mpf(x)
    D = 3 * mp.quad(lambda t: t**3 / mp.expm1(t), [0, x]) / x**3
    em1 = mp.expm1(x); D1 = 3 / em1 - 3 * D / x; g2 = mp.exp(x) / em1**2
    D2 = -3 * g2 - 3 * D1 / x + 3 * D / x**2
    D3 = -3 * g2 + 6 * g2 * mp.exp(x) / em1 - 3 * D2 / x + 6 * D1 / x**2 - 6 * D / x**3
    return [float(v) for v in (D, D1, D2, D3)]
cache = {}
def R(x):
    k = float(x)
    if k not in cache: cache[k] = _ref(k)
    return cache[k]
vec = lambda f: (lambda x, *a: np.array([f(xi) for xi in x]) if isinstance(x, np.ndarray) and x.ndim else f(float(x)))
exact = dict(D_3=vec(lambda x: R(x)[0]), dD_3dx=vec(lambda x: R(x)[1]), d2D_3dx2=vec(lambda x: R(x)[2]), d3D_3dx3=vec(lambda x: R(x)[3]))
orig = {k: getattr(vib, k) for k in exact}

P = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
cases = {"Al (thD~450K)": (P, 0.0269815), "soft/heavy (thD~95K)": ([P[0], P[1], 1.0e10, P[3]], 0.2072)}
T = np.array([0.1, 0.5, 2., 20., 28., 40., 300., 1000., 2000., 4000.])
keys = ["tD", "Cv", "Cp", "S", "a", "Kt", "Ktp", "Ks", "Ksp", "dKtdT_P", "dadP_T", "dCpdP_T"]
for name, (p, m) in cases.items():
    eos = potentials.BM(parameters=p); eos.fitEOS(np.linspace(.9, 1.1, 5) * p[1], np.zeros(5), initial_parameters=np.array(p), fit=False)
    nd = nDeb(0.3, m, (0, 1), eos, [0, 0, 0, 0], (8.46, 1.69, 933, 0.0), (0, 0, 0), mode="jjsl")
    V = np.full_like(T, eos.V0)
    for k in exact: setattr(vib, k, orig[k])
    a = nd.eval_props(T.copy(), V.copy(), P=0)
    for k in exact: setattr(vib, k, exact[k])
    b = nd.eval_props(T.copy(), V.copy(), P=0)
    for k in exact: setattr(vib, k, orig[k])
    print("\n== %s, V=V0, relative difference (current code vs exact Debye functions)" % name)
    print("%8s %8s " % ("T", "x") + " ".join("%9s" % k for k in keys[1:]))
    for i, t in enumerate(T):
        print("%8.1f %8.3g " % (t, a["tD"][i] / t) + " ".join("%9.1e" % (a[k][i] / b[k][i] - 1 if b[k][i] != 0 else np.nan) for k in keys[1:]))
