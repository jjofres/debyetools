"""Phase 8: optim.ga_fitting behaviour and fs_compound_db.fit_FS accuracy. Run from repo root (numpy<2)."""
import sys, os, io, random, contextlib, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
from debyetools.optim import ga_fitting, eval_error
from debyetools.fs_compound_db import fit_FS, Cp2fit, alpha2fit

print("== A. ga_fitting on y = p0 + p1*x (true p = [2, 3]); initial guess [1.5, 2.5], range (0.8, 1.2)")
X = np.linspace(0, 1, 20); Y = 2 + 3 * X
f = lambda x, p: p[0] + p[1] * x
for seed in [1, 2]:
    for rep in range(2):
        random.seed(seed)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            p = ga_fitting(f, X, Y, [1.5, 2.5], npop=20, ngen=60, verbose=True)
        fits = [float(l.split("Best fitness = ")[1].split(",")[0]) for l in buf.getvalue().splitlines() if l.startswith("Generation")]
        incr = sum(1 for a, b in zip(fits, fits[1:]) if b > a * (1 + 1e-12))
        print("  seed %d run %d: result %s  final mse %.2e  generations %d  times best fitness INCREASED %d (max %.2e)" % (
            seed, rep, np.round(p, 4), fits[-1], len(fits), incr, max(fits)))
random.seed(None)
print("  without seeding, two runs:", [np.round(ga_fitting(f, X, Y, [1.5, 2.5], npop=20, ngen=60, verbose=False), 4) for _ in range(2)] if False else "(see A2)")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    r1 = ga_fitting(f, X, Y, [1.5, 2.5], npop=20, ngen=60, verbose=False); r2 = ga_fitting(f, X, Y, [1.5, 2.5], npop=20, ngen=60, verbose=False)
print("  A2 unseeded runs:", np.round(r1, 5), np.round(r2, 5))

print("\n== B. A parameter whose initial guess is 0 can never change (multiplicative normalisation)")
Y2 = 2 + 3 * X + 0.5 * X ** 2
g = lambda x, p: p[0] + p[1] * x + p[2] * x ** 2
random.seed(3)
with contextlib.redirect_stdout(io.StringIO()):
    p = ga_fitting(g, X, Y2, [2, 3, 0.0], npop=20, ngen=40, verbose=False)
print("  true [2, 3, 0.5], initial [2, 3, 0] -> result", np.round(p, 4))

print("\n== C. fit_FS: Cp model is linear in its 6 coefficients -> compare curve_fit (code) with exact linear least squares")
g_ = np.load("review/baseline/golden.npz")
for case in ["BM_jjsl", "BM_jjsl_allcontrib", "MG_jjsl"]:
    T = g_["pipe/%s/T" % case]; tp = {k: g_["pipe/%s/%s" % (case, k)] for k in ["T", "Cp", "a", "Ks"]}
    tp["Ksp"] = np.ones_like(T)
    m = (T >= 298.15 - 1e-6) & (T <= 1000.1 + 1e-6)
    try:
        r = fit_FS(tp, 298.15, 1000.1)
        pc = r["Cp"]
        A = np.vstack([T[m] ** 0, T[m], T[m] ** -2, T[m] ** 2, T[m] ** -0.5, T[m] ** -3]).T
        pl = np.linalg.lstsq(A, tp["Cp"][m], rcond=None)[0]
        rc = np.sqrt(np.mean((Cp2fit(T[m], *pc) - tp["Cp"][m]) ** 2)); rl = np.sqrt(np.mean((A @ pl - tp["Cp"][m]) ** 2))
        print("  %-20s rms Cp residual: curve_fit %.4f, linear LSQ %.4f J/mol/K | curve_fit last coef (T^-3) = %.6g (initial guess 1)" % (case, rc, rl, pc[5]))
        print("  %-20s n points in window = %d for 6 Cp parameters" % ("", m.sum()))
    except Exception as e:
        print("  %-20s fit_FS raised %s: %s" % (case, type(e).__name__, e))
try:
    fit_FS({"T": np.array([300., 400., 500.]), "Cp": np.ones(3), "a": np.ones(3), "Ks": np.ones(3), "Ksp": np.ones(3)}, 298.15, 500.)
except Exception as e:
    print("  T_from not on the T grid (298.15 absent) -> %s: %s" % (type(e).__name__, e))
