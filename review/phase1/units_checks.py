"""Phase 1 checks: constants, unit conversions, dimensional/limit checks. Run from repo root."""
import sys, os, glob, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
import debyetools.vibrational as vibm, debyetools.ndeb as ndm, debyetools.electronic as elm, debyetools.defects as dfm
import debyetools.potentials as potentials
from debyetools.ndeb import nDeb

# CODATA 2018 / SI-2019 exact values
C18 = dict(hbar=1.054571817e-34, NA=6.02214076e23, kB=1.380649e-23, eV=1.602176634e-19)
print("== 1. Constants vs CODATA 2018 (relative deviation)")
used = [("vibrational/ndeb hbar", vibm.hbar, C18["hbar"]), ("vibrational/ndeb/electronic/defects NAv", vibm.NAv, C18["NA"]),
        ("vibrational/ndeb/electronic/defects kB", vibm.kB, C18["kB"]),
        ("electronic eV (0.160218e-18)", 0.160218e-18, C18["eV"]),
        ("potentials MP/EAM + aux load_V_E: NA in mult_E (6.02214e23)", 6.02214e23, C18["NA"]),
        ("potentials MP/EAM + aux load_V_E: NA in mult_V (6.02e23)", 6.02e23, C18["NA"]),
        ("potentials/aux eV in mult_E (0.160218e-18)", 0.160218e-18, C18["eV"]),
        ("get_elastic eV/A^3->GPa (160.21766208)", 160.21766208, C18["eV"] * 1e30 / 1e9)]
for n, v, ref in used:
    print("  %-62s %.4e  rel %+.2e" % (n, v, v / ref - 1))
print("  R = NA*kB used: %.6f  vs 8.314462618" % (vibm.NAv * vibm.kB))

print("\n== 2. Cell volume in load_V_E (product of diagonal, no scale factor) vs det(scale*cell)")
for f in sorted(glob.glob("tests/inpt_files/*/CONTCAR.5") + glob.glob("debyetools/examples/*/CONTCAR")):
    L = open(f).read().splitlines()
    s = float(L[1].split()[0]); cell = np.array([[float(x) for x in l.split()[:3]] for l in L[2:5]])
    vdiag = np.prod(np.diag(cell)); vdet = abs(np.linalg.det(cell)) * (s ** 3 if s > 0 else 1)
    flag = "" if abs(vdiag / vdet - 1) < 1e-9 else "   <-- MISMATCH"
    print("  %-48s scale=%-8g Vdiag=%10.4f Vtrue=%10.4f ratio=%.6f%s" % (f, s, vdiag, vdet, vdiag / vdet, flag))

# ---- fixed Al parameters
NU, M = 0.31681, 0.0269815
P_EOS = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
P_EL = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
eos = potentials.BM(parameters=P_EOS); eos.fitEOS(np.linspace(.9, 1.1, 5) * P_EOS[1], np.zeros(5), initial_parameters=np.array(P_EOS), fit=False)
hb, NA, kB = C18["hbar"], C18["NA"], C18["kB"]

def kv(nu):
    return (2 / 3 * (2 / 3 * (1 + nu) / (1 - 2 * nu)) ** 1.5 + 1 / 3 * ((1 + nu) / (3 * (1 - nu))) ** 1.5) ** (-1 / 3)

print("\n== 3. Debye temperature: code vs independent SI evaluation of Calphad-2023 eq.(14)")
for mode, lam in [("jjsl", -1), ("jjdm", 0), ("jjfv", 1)]:
    nd = nDeb(NU, M, (0, 1), eos, P_EL, (8.46, 1.69, 933, 0.1), (0, 0, 0), mode=mode)
    for fv in [0.97, 1.0, 1.04]:
        V = fv * eos.V0; T = np.array([300.])
        tp = nd.eval_props(T, np.array([V]), P=0)
        d1, d2 = eos.dE0dV_T(V), eos.d2E0dV2_T(V)
        th = kv(NU) * hb / kB * (6 * np.pi ** 2 * NA / V) ** (1 / 3) * np.sqrt(V ** 2 / M * (d2 + 2 * (lam + 1) / (3 * V) * d1))
        print("  %s V/V0=%.2f  code tD=%.6f  indep=%.6f  rel=%+.2e" % (mode, fv, tp["tD"][0], th, tp["tD"][0] / th - 1))
print("  kv: code=%.10f  paper eq.(11)=%.10f" % (nd.kv, kv(NU)))

print("\n== 4. Vibrational limits (jjsl, V=V0)")
nd = nDeb(NU, M, (0, 1), eos, P_EL, (8.46, 1.69, 933, 0.1), (0, 0, 0), mode="jjsl")
T = np.array([0.5, 1., 2., 5., 1e4, 5e4]); V = np.full_like(T, eos.V0)
tp = nd.eval_props(T, V, P=0)
th = tp["tD"][0]
print("  Cv_vib(T>>thD) = %s   3R(code)=%.6f  3R(2018)=%.6f" % (tp["Cvvib"][-2:], 3 * vibm.NAv * vibm.kB, 3 * NA * kB))
print("  F_vib(T->0)=%.6f  9/8 R thD=%.6f" % (tp["Fvib"][0], 9 / 8 * vibm.NAv * vibm.kB * th))
lowT = 12 * np.pi ** 4 / 5 * vibm.NAv * vibm.kB * (T[:4] / th) ** 3
print("  Cv_vib low T: code=%s  Debye T^3 law=%s" % (tp["Cvvib"][:4], lowT))

print("\n== 5. Electronic free energy vs Sommerfeld F=-(pi^2/6) NA kB^2 T^2 N(EF) [N in states/eV/atom]")
el = nd.el
for T_, V_ in [(300., eos.V0), (1000., 1.03 * eos.V0)]:
    N = el.NfV(V_)
    som = -(np.pi ** 2 / 6) * NA * kB ** 2 * T_ ** 2 * N / C18["eV"]
    print("  T=%g  code F_el=%.6f  Sommerfeld(2018)=%.6f  rel=%+.2e   [paper eq.(9) uses pi^2/3 -> %.6f]" % (T_, el.F(T_, V_), som, el.F(T_, V_) / som - 1, 2 * som))
print("  Electronic.r =", getattr(el, "r", None))

print("\n== 6. Defects: units (Evac00 in kB*Tm, Svac00 in kB)")
d = nd.deff
print("  Evac0 = %.4f eV (per atom)  Svac0 = %.3f kB   Evac(V0)=%.4f eV  P2=B0=%.4e Pa   a*V0*B0/NA = %.4f eV" % (
    d.Evac0 / C18["eV"], d.Svac0 / kB, d.Evac(eos.V0) / C18["eV"], d.P2, d.a * d.V0 * d.P2 / NA / C18["eV"]))
c = 0.001; Tm = 933.
print("  vacancy fraction at Tm: %.3e" % np.exp(d.Svac0 / dfm.kB - d.Evac(eos.V0) / (dfm.kB * Tm)))

print("\n== 7. Property units at T=300 K, V=V0 (Al): expected Pa, 1/K, J/mol/K")
tp = nd.eval_props(np.array([300.]), np.array([eos.V0]), P=0)
for k, u in [("Kt", "Pa"), ("Ks", "Pa"), ("a", "1/K"), ("Cp", "J/mol/K"), ("Cv", "J/mol/K"), ("S", "J/mol/K"), ("G", "J/mol"), ("P", "Pa"), ("g", "-")]:
    print("  %-4s = %.6e %s" % (k, tp[k][0], u))
B_check = eos.V0 * eos.d2E0dV2_T(eos.V0)
print("  B0 from EOS (V d2E/dV2 at V0) = %.6e Pa (input B0 = %.6e)" % (B_check, P_EOS[2]))

print("\n== 8. MP potential: J/mol mode vs eV/atom mode consistency")
from debyetools.aux_functions import load_cell
f, cell, basis = load_cell("tests/inpt_files/Al_fcc/CONTCAR.5")
pm = np.array([3.492281316e-01, 9.977375168e-01, 3.246481751e+00])
mpJ = potentials.MP(f, cell, basis, 5, 3, units="J/mol", parameters=pm)
mpE = potentials.MP(f, cell, basis, 5, 3, units="eV/atom", parameters=pm)
for va in [15.5, 16.5, 17.5]:  # A^3/atom
    vJ = va * 1e-30 * C18["NA"]
    print("  V=%.1f A^3/at  E_J(V_SI)/eV/NA = %.8f eV   E_eV(V)=%.8f eV  ratio-1=%+.2e" % (
        va, mpJ.E0(vJ) / C18["eV"] / C18["NA"], mpE.E0(va), mpJ.E0(vJ) / C18["eV"] / C18["NA"] / mpE.E0(va) - 1))
