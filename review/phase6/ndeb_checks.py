"""Phase 6: ndeb.py checks. Run from repo root with numpy<2.
A: eval_props vs finite differences of the total F (f2min) and of eval_props itself, plus thermodynamic identities.
B: min_G accuracy (fmin) vs exact root of P(V) = P_target, and its effect on Cp/alpha.
C: min_G at P = 10 GPa.  D: failure modes (PT spinodal, MU2, silent row filter)."""
import sys, os, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
import debyetools.potentials as potentials
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts
from scipy.optimize import brentq

P4 = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
P_EL = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
def eos_(name, p):
    e = getattr(potentials, name)(parameters=list(p)); e.fitEOS(np.linspace(.9, 1.1, 5) * p[1], np.zeros(5), initial_parameters=np.array(p, float), fit=False)
    if name == "MU2": e.pEOS = np.array(p, float)
    return e
def nd_(eos, mode="jjsl", intanh=(-1e-5, 1.5), anh=(1e-4, -5., 2e5), xs=(10., 0.01, 1e-6, 1e-9, 0.1, 1e3), dfc=(8.46, 1.69, 933, 0.1)):
    return nDeb(0.31681, 0.0269815, intanh, eos, P_EL, dfc, anh, mode=mode, xsparams=xs)

def d1(f, x, h):  # 4th-order central first derivative
    return (-f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)) / (12 * h)
def d2(f, x, h):
    return (-f(x + 2 * h) + 16 * f(x + h) - 30 * f(x) + 16 * f(x - h) - f(x - 2 * h)) / (12 * h * h)

eos = eos_("BM", P4); nd = nd_(eos)
F = lambda T, V: float(np.real(nd.f2min(T, V, 0.0)))
def ep(T, V, key):
    return float(nd.eval_props(np.array([T]), np.array([V]), P=0)[key][0])

print("== A1. eval_props vs FD of total F = f2min(T,V,0)  (BM, jjsl, all contributions on)")
print("%6s %6s %10s %10s %10s %10s %10s %10s %10s" % ("T", "V/V0", "P", "S", "Cv", "Cp", "alpha", "Kt", "Evib"))
for T, fv in [(50., 1.0), (300., 1.01), (800., 1.035), (1200., 1.06)]:
    V = fv * eos.V0; hT, hV = 1e-3 * T, 1e-4 * V
    FV = d1(lambda v: F(T, v), V, hV); FT = d1(lambda t: F(t, V), T, hT)
    FVV = d2(lambda v: F(T, v), V, hV); FTT = d2(lambda t: F(t, V), T, hT)
    FVT = d1(lambda t: d1(lambda v: F(t, v), V, hV), T, hT)
    tp = nd.eval_props(np.array([T]), np.array([V]), P=0)
    ref = {"P": -FV, "S": -FT, "Cv": -T * FTT, "Cp": -T * (FTT - FVT ** 2 / FVV), "a": -FVT / (V * FVV), "Kt": V * FVV}
    vb = nd.vib; vb.set_int_anh(T, V); vb.set_theta(T, V)
    Fv = float(vb.F(T, V)); Sv = -float(vb.dFdT_V(T, V)); ref["Evib"] = Fv + T * Sv
    print("%6.0f %6.3f " % (T, fv) + " ".join("%10.1e" % (tp[k][0] / ref[k] - 1) for k in ["P", "S", "Cv", "Cp", "a", "Kt", "Evib"]))
print("   (relative differences; FD floor ~1e-6..1e-5)")

print("\n== A2. Pressure/temperature derivatives from eval_props vs FD of eval_props outputs (fixed T)")
keys = [("Ktp", "Kt"), ("Ktpp", "Ktp"), ("Ksp", "Ks"), ("dCpdP_T", "Cp"), ("dadP_T", "a"), ("dSdP_T", "S")]
for T, fv in [(300., 1.01), (800., 1.035)]:
    V = fv * eos.V0; h = 1e-4 * V
    dP = d1(lambda v: ep(T, v, "P"), V, h)
    row = []
    for k, base in keys:
        num = d1(lambda v: ep(T, v, base), V, h) / dP
        row.append("%s %+.1e" % (k, ep(T, V, k) / num - 1))
    # dKt/dT at constant P = dKt/dT|V + dKt/dV|T * dV/dT|P
    hT = 1e-3 * T
    num = d1(lambda t: ep(t, V, "Kt"), T, hT) + d1(lambda v: ep(T, v, "Kt"), V, h) * ep(T, V, "a") * V
    row.append("dKtdT_P %+.1e" % (ep(T, V, "dKtdT_P") / num - 1))
    # Ksp at constant entropy (conventional definition) for comparison
    print("  T=%4.0f: " % T + " | ".join(row))

print("\n== A3. Identities (eval_props outputs only)")
tp = nd.eval_props(np.array([300., 800.]), np.array([1.01, 1.035]) * eos.V0, P=0)
V = tp["V"]; T = tp["T"]
print("  Cp-Cv - T V a^2 Kt :", (tp["Cp"] - tp["Cv"]) / (T * V * tp["a"] ** 2 * tp["Kt"]) - 1)
print("  Ks/Kt - Cp/Cv      :", tp["Ks"] / tp["Kt"] / (tp["Cp"] / tp["Cv"]) - 1)
print("  dS/dP_T + V a      :", tp["dSdP_T"] / (-V * tp["a"]) - 1)
print("  g (theta-based) vs thermodynamic gamma = a Kt V / Cv :", tp["g"], tp["a"] * tp["Kt"] * V / tp["Cv"])
print("  Evib returned vs Fvib + T*Svib:", tp["Evib"], tp["Fvib"] + T * tp["Svib"])

print("\n== B. min_G accuracy (BM, jjsl, all contributions): fmin volume vs root of P(V)=0")
Ts = np.array([0.1, 100., 298.15, 600., 900.])
Tm, Vm = nd.min_G(Ts.copy(), eos.V0, P=0)
for T, V in zip(Tm, Vm):
    Vr = brentq(lambda v: ep(T, v, "P"), 0.95 * V, 1.05 * V, xtol=1e-20, rtol=1e-14)
    a, b = nd.eval_props(np.array([T, T]), np.array([V, Vr]), P=0), None
    print("  T=%7.2f  V_fmin/V_root-1=%+.2e  P(V_fmin)=%+.2e Pa  Cp rel %+.1e  alpha rel %+.1e  Kt rel %+.1e" % (
        T, V / Vr - 1, a["P"][0], a["Cp"][0] / a["Cp"][1] - 1, a["a"][0] / a["a"][1] - 1, a["Kt"][0] / a["Kt"][1] - 1))

print("\n== C. min_G at P = 10 GPa")
Tm, Vm = nd.min_G(np.array([0.1, 300., 800.]), eos.V0, P=1e10)
tp = nd.eval_props(Tm, Vm, P=1e10)
print("  returned P from eval_props:", tp["P"], " G - (F + P V) uses computed P:", tp["G"][-1])

print("\n== D1. PT EOS: min_G vs stability")
ndp = nd_(eos_("PT", P4), intanh=(0, 1), anh=(0, 0, 0), xs=(0,) * 6, dfc=(8.46, 1.69, 933, 0.0))
Ts = np.array([0.1, 800., 900., 950., 1000.])
Tm, Vm = ndp.min_G(Ts.copy(), eos.V0, P=0); tp = ndp.eval_props(Tm, Vm, P=0)
for i in range(len(Tm)):
    print("  T=%6.1f V/V0=%.4f  Kt=%.3e  P=%.3e  tD=%s  Cp=%.4e" % (Tm[i], Vm[i] / P4[1], tp["Kt"][i], tp["P"][i], tp["tD"][i], tp["Cp"][i]))

print("\n== D2. MU2 (sign quirk bypassed): P at the min_G volumes (should be 0)")
ndm = nd_(eos_("MU2", P4 + [-6e-11]), intanh=(0, 1), anh=(0, 0, 0), xs=(0,) * 6, dfc=(8.46, 1.69, 933, 0.0))
Tm, Vm = ndm.min_G(np.array([0.1, 300., 900.]), P4[1], P=0); tp = ndm.eval_props(Tm, Vm, P=0)
print("  P (Pa):", tp["P"], " vs BM same settings:", nd_(eos, intanh=(0, 1), anh=(0, 0, 0), xs=(0,) * 6, dfc=(8.46, 1.69, 933, 0.0)).eval_props(*nd_(eos, intanh=(0, 1), anh=(0, 0, 0), xs=(0,) * 6, dfc=(8.46, 1.69, 933, 0.0)).min_G(np.array([0.1, 300., 900.]), P4[1], P=0), P=0)["P"])

print("\n== D3. Silent row filter in min_G (V > 1.5 V(T_first) dropped)")
Ts = gen_Ts(0.1, 1000.1, 11)
Tm, Vm = ndp.min_G(Ts.copy(), eos.V0, P=0)
print("  input %d temperatures -> returned %d; dropped: %s" % (len(Ts), len(Tm), sorted(set(np.round(Ts, 2)) - set(np.round(Tm, 2)))))
