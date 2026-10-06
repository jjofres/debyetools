"""Phase 2: Debye function D_3 and derivatives vs 50-digit reference. Run from repo root."""
import sys, os, time, warnings
import numpy as np, mpmath as mp
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
from debyetools.debfunct import D_3, dD_3dx, d2D_3dx2, d3D_3dx3
mp.mp.dps = 50

def ref(x):
    x = mp.mpf(x)
    I = mp.quad(lambda t: t**3 / mp.expm1(t), [0, min(x, 40), x] if x > 40 else [0, x])
    D = 3 * I / x**3
    em1 = mp.expm1(x)
    D1 = 3 / em1 - 3 * D / x
    g2 = mp.exp(x) / em1**2
    D2 = -3 * g2 - 3 * D1 / x + 3 * D / x**2
    D3 = -3 * g2 + 6 * g2 * mp.exp(x) / em1 - 3 * D2 / x + 6 * D1 / x**2 - 6 * D / x**3
    return [float(v) for v in (D, D1, D2, D3)]

xs = sorted(set(np.r_[np.logspace(-4, 3, 57), [0.04, 1, 2, 5, 10, 15, 15.79, 15.79779, 15.7978, 15.8, 16, 20, 30, 50,
                                                 354.8, 354.9, 499.9, 500, 600, 653, 700, 709.7, 709.8, 800]]))
print("%10s %12s | %10s %10s %10s %10s   (relative error of code vs reference)" % ("x", "D3_ref", "D3", "dD3", "d2D3", "d3D3"))
worst = {}
for x in xs:
    r = ref(x)
    c0 = D_3(x); c1 = dD_3dx(x, c0); c2 = d2D_3dx2(x, c0, c1); c3 = d3D_3dx3(x, c0, c1, c2)
    rel = [abs(c / v - 1) if v != 0 else abs(c) for c, v in zip((c0, c1, c2, c3), r)]
    for k, e in zip(("D3", "dD3", "d2D3", "d3D3"), rel):
        if e > worst.get(k, (0, 0))[0]: worst[k] = (e, x)
    mark = "  <--" if max(rel) > 1e-8 else ""
    print("%10.4g %12.5e | %10.2e %10.2e %10.2e %10.2e%s" % (x, r[0], *rel, mark))
print("\nworst relative error:", {k: "%.2e at x=%.4g" % v for k, v in worst.items()})

print("\n== Jump of D3 at the branch switch x=15.79779 (polylog -> asymptotic)")
for x in [15.797789999, 15.79779]:
    print("  x=%.9f  code D3=%.15e  ref=%.15e" % (x, D_3(x), ref(x)[0]))

print("\n== Effect on the Debye heat capacity Cv/3R = 4 D3 - 3x/(e^x-1) (code D3 vs reference)")
for x in [10, 15, 15.79779, 16, 20, 30, 100, 400, 499, 500, 600, 1000]:
    D = D_3(x); Dr = ref(x)[0]; b = 3 * x / np.expm1(x)
    cv, cvr = 4 * D - b, 4 * Dr - b
    print("  x=%7.2f  Cv/3R code=%.6e ref=%.6e rel=%+.2e   (T = thD/x; Al thD~448 K -> T=%.3g K)" % (x, cv, cvr, cv / cvr - 1, 448 / x))

print("\n== Small-x behaviour (high T): D3(x) -> 1 - 3x/8 + x^2/20")
for x in [1e-6, 1e-5, 1e-4, 1e-3, 1e-2]:
    print("  x=%g code=%.15f series=%.15f rel=%.1e" % (x, D_3(x), 1 - 3 * x / 8 + x**2 / 20, D_3(x) / (1 - 3 * x / 8 + x**2 / 20) - 1))

print("\n== Special inputs")
for x in [np.nan, 0.0, -1.0, np.inf]:
    try:
        print("  D_3(%s) = %r" % (x, D_3(x)))
    except Exception as e:
        print("  D_3(%s) raises %s: %s" % (x, type(e).__name__, e))
print("  D_3(np.array(5.)) (0-d array):", end=" ")
try: print(D_3(np.array(5.)))
except Exception as e: print("raises", type(e).__name__, e)

print("\n== Cost")
x = np.linspace(0.5, 15, 2000)
t = time.perf_counter(); D_3(x); t1 = time.perf_counter() - t
print("  D_3 on 2000 points (polylog branch): %.3f s  -> %.0f us/point" % (t1, 1e6 * t1 / 2000))
