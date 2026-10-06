"""Phase 5a: electronic fit. N(E_F) interpolated from each DOSCAR vs the model used by fit_electronic. Run from repo root."""
import sys, os, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
from debyetools.aux_functions import load_doscar, load_V_E
from debyetools.electronic import fit_electronic, NfV_poly_fun
from scipy.optimize import least_squares

def read_total_dos(fname):
    """Independent DOSCAR reader: total DOS block only (NEDOS lines), spin-summed, per atom."""
    L = open(fname).read().splitlines()
    nat = int(L[0].split()[0]); h = L[5].split(); nedos, ef = int(h[2]), float(h[3])
    blk = np.array([[float(x) for x in l.split()] for l in L[6:6 + nedos]])
    ispin = 2 if blk.shape[1] == 5 else 1
    dos = blk[:, 1] + (blk[:, 2] if ispin == 2 else 0)
    return blk[:, 0], dos / nat, ef, ispin, len(L)

P0 = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
for mat, tags in [("Al_fcc", ["%02da" % i for i in range(1, 22)]), ("Cu_fcc", None), ("V_bcc", None), ("Ti_hcp", None), ("Al3Li_D023", None)]:
    d = "tests/inpt_files/" + mat
    V, _ = load_V_E(d + "/SUMMARY.fcc", d + "/CONTCAR.5", units="J/mol")
    E, N, Ef = load_doscar(d + "/DOSCAR.EvV.", list_filetags=tags)
    n = min(len(V), len(Ef))
    tags_ = tags or ['-0.10', '-0.09', '-0.08', '-0.07', '-0.06', '-0.05', '-0.04', '-0.03', '-0.02', '-0.01', '-0.00', '0.01', '0.02', '0.03', '0.04', '0.05', '0.06', '0.07', '0.08', '0.09', '0.10']
    rd = [read_total_dos(d + "/DOSCAR.EvV." + t) for t in tags_[:n]]
    actual = np.array([np.interp(r[2], r[0], r[1]) for r in rd])
    print("   ISPIN=%d, NEDOS=%d, points read by load_doscar=%d (non-monotonic E: %s)" % (rd[0][3], len(rd[0][0]), len(E[0]), not np.all(np.diff(np.array(E[0], float)) > 0)))
    model = actual[4] * np.sqrt(np.array(Ef[:n]) / Ef[4])
    p = fit_electronic(V, P0, E, N, Ef)
    poly = NfV_poly_fun(V[:n], *p)
    # proper least squares of a cubic in reduced volume on the actual N(E_F) at all volumes
    x = V[:n] / V[n // 2] - 1
    c = np.polyfit(x, actual, 3)
    print("== %s  (%d volumes, V in m3/mol: %.3e..%.3e)" % (mat, n, V[0], V[n - 1]))
    print("   E_F from DOSCAR (eV): %s" % np.array2string(np.array(Ef[:n])[[0, 4, n // 2, n - 1]], precision=3))
    print("   N(E_F) interpolated per volume (states/eV/at): min %.4f max %.4f  [index 4 = %.4f]" % (actual.min(), actual.max(), actual[4]))
    print("   fit_electronic target model N4*sqrt(Ef/Ef4): min %.4f max %.4f" % (np.nanmin(model), np.nanmax(model)))
    print("   fitted params: %s  (initial q2,q3 = %.3e, %.3e)" % (np.array2string(p, precision=4), P0[2], P0[3]))
    print("   max |poly(V) - actual N(E_F)| = %.4f  (%.1f %% of mean N)   ; cubic fit to actual: max dev %.4f" % (
        np.nanmax(np.abs(poly - actual)), 100 * np.nanmax(np.abs(poly - actual)) / actual.mean(), np.max(np.abs(np.polyval(c, x) - actual))))
    print("   F_el(1000 K) per mol-at with fitted poly at V[mid]: %.1f J/mol; with actual N: %.1f J/mol" % (
        -(np.pi**2 / 6) * 6.02214076e23 * 1.380649e-23**2 * 1e6 * poly[n // 2] / 1.602176634e-19,
        -(np.pi**2 / 6) * 6.02214076e23 * 1.380649e-23**2 * 1e6 * actual[n // 2] / 1.602176634e-19))
