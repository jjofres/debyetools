"""Phase 7a: Poisson ratio / VRH averages vs an exact general implementation (S = C^-1), and clamped-ion vs relaxed-ion moduli."""
import sys, os, glob, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
from debyetools.aux_functions import load_EM
from debyetools.poisson import poisson_ratio

def vrh(C):
    """Exact Voigt-Reuss-Hill for any symmetry; invariant to the order of the three shear components."""
    S = np.linalg.inv(C)
    BV = (C[0, 0] + C[1, 1] + C[2, 2] + 2 * (C[0, 1] + C[0, 2] + C[1, 2])) / 9
    GV = (C[0, 0] + C[1, 1] + C[2, 2] - (C[0, 1] + C[0, 2] + C[1, 2]) + 3 * (C[3, 3] + C[4, 4] + C[5, 5])) / 15
    BR = 1 / (S[0, 0] + S[1, 1] + S[2, 2] + 2 * (S[0, 1] + S[0, 2] + S[1, 2]))
    GR = 15 / (4 * (S[0, 0] + S[1, 1] + S[2, 2]) - 4 * (S[0, 1] + S[0, 2] + S[1, 2]) + 3 * (S[3, 3] + S[4, 4] + S[5, 5]))
    B, G = (BV + BR) / 2, (GV + GR) / 2
    Y = 9 * B * G / (3 * B + G)
    return BR, BV, B, GR, GV, G, (3 * B - Y) / (6 * B)

def load_block(f, title):
    L = open(f).read().splitlines()
    for i, l in enumerate(L):
        if l.strip().startswith(title):
            return np.array([[float(x) for x in L[j].split()[1:7]] for j in range(i + 3, i + 9)])
    return None

print("== A. nu and VRH moduli: code (poisson_ratio / quiet_pa) vs exact (S = C^-1).  B, G in GPa (input kBar/10)")
print("%-16s %9s %9s %9s | %8s %8s %8s %8s | %s" % ("material", "nu code", "nu quiet", "nu exact", "BR code", "BR ex", "GR code", "GR ex", "max|C_ij-C_ji|, off-diag couplings"))
for f in sorted(glob.glob("tests/inpt_files/*/OUTCAR.eps")):
    try:
        EM = load_EM(f)
    except Exception as e:
        print("%-16s load_EM failed: %s" % (f.split("/")[2], e)); continue
    nu = poisson_ratio(EM); q = poisson_ratio(EM, quiet=True)
    ex = vrh(EM / 10)
    coup = [(i, j, round(EM[i, j], 1)) for i in range(3) for j in range(3, 6) if abs(EM[i, j]) > 1e-3] + \
           [(i, j, round(EM[i, j], 1)) for i in range(3, 6) for j in range(i + 1, 6) if abs(EM[i, j]) > 1e-3]
    flag = "  <--" if abs(nu - ex[6]) > 1e-6 else ""
    print("%-16s %9.5f %9.5f %9.5f | %8.2f %8.2f %8.2f %8.2f | %.1e %s%s" % (
        f.split("/")[2], nu, q[-1], ex[6], q[0], ex[0], q[3], ex[3], np.max(np.abs(EM - EM.T)), coup[:4], flag))

print("\n== B. Clamped-ion ('SYMMETRIZED', used by load_EM) vs relaxed-ion ('TOTAL') elastic moduli")
for f in sorted(glob.glob("tests/inpt_files/*/OUTCAR.eps")):
    Cs, Ct = load_block(f, "SYMMETRIZED ELASTIC MODULI"), load_block(f, "TOTAL ELASTIC MODULI")
    if Cs is None or Ct is None:
        continue
    a, b = vrh(Cs / 10), vrh(Ct / 10)
    print("  %-16s nu clamped=%.4f relaxed=%.4f | B %.1f vs %.1f GPa | G %.1f vs %.1f GPa%s" % (
        f.split("/")[2], a[6], b[6], a[2], b[2], a[5], b[5], "   <-- differs" if abs(a[6] - b[6]) > 1e-3 else ""))
