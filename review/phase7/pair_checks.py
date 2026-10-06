"""Phase 7b: pair_analysis vs brute-force neighbour shells (counts per atom), several cells and cutoffs."""
import sys, os, warnings
import numpy as np
warnings.filterwarnings("ignore")
sys.path.insert(0, os.getcwd())
from debyetools.pairanalysis import pair_analysis

def brute(basis_frac, cell, cutoff, prec=6):
    B = basis_frac @ cell; n = 6
    imgs = np.array([[i, j, k] for i in range(-n, n + 1) for j in range(-n, n + 1) for k in range(-n, n + 1)]) @ cell
    d = []
    for a in B:
        for b in B:
            r = np.linalg.norm(b + imgs - a, axis=1)
            d += list(r[(r > 1e-8) & (r <= cutoff + 1e-9)])
    d = np.round(d, prec)
    u, c = np.unique(d, return_counts=True)
    return u, c / len(B)

a = 4.04; ah, ch = 2.95, 4.68
cases = {
    "fcc conventional, cutoff 5.0": (np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0]]), np.eye(3) * a, 5.0),
    "fcc conventional, cutoff 3.0": (np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0]]), np.eye(3) * a, 3.0),
    "fcc primitive, cutoff 5.0": (np.array([[0, 0, 0]]), np.array([[0, .5, .5], [.5, 0, .5], [.5, .5, 0]]) * a, 5.0),
    "bcc primitive, cutoff 4.5": (np.array([[0, 0, 0]]), np.array([[-.5, .5, .5], [.5, -.5, .5], [.5, .5, -.5]]) * 3.3, 4.5),
    "hcp, cutoff 5.0": (np.array([[1 / 3, 2 / 3, .25], [2 / 3, 1 / 3, .75]]), np.array([[ah, 0, 0], [-ah / 2, ah * np.sqrt(3) / 2, 0], [0, 0, ch]]), 5.0),
    "hcp, cutoff 4.0 (< c)": (np.array([[1 / 3, 2 / 3, .25], [2 / 3, 1 / 3, .75]]), np.array([[ah, 0, 0], [-ah / 2, ah * np.sqrt(3) / 2, 0], [0, 0, ch]]), 4.0),
}
for name, (basis, cell, cut) in cases.items():
    types = "A" * len(basis)
    try:
        d, n, ct = pair_analysis(types, cut, basis, cell)
        code = dict(zip(np.round(d, 6), np.round(n[:, 0], 6)))
    except Exception as e:
        code = {"error": str(e)}
    u, c = brute(basis, cell, cut)
    ref = dict(zip(u, np.round(c, 6)))
    ok = code == ref
    print("== %-30s %s" % (name, "OK" if ok else "MISMATCH"))
    if not ok:
        print("   brute  :", {float(k): float(v) for k, v in ref.items()})
        print("   code   :", {(float(k) if not isinstance(k, str) else k): (float(v) if not isinstance(v, str) else v) for k, v in code.items()})
