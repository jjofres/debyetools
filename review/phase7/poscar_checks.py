"""Phase 7c: load_cell / load_V_E with POSCAR variants (scale factor, Cartesian, Selective dynamics)."""
import sys, os, tempfile, warnings
import numpy as np
warnings.filterwarnings("ignore")
sys.path.insert(0, os.getcwd())
from debyetools.aux_functions import load_cell, load_V_E

base = """Al
{scale}
 {a} 0 0
 0 {a} 0
 0 0 {a}
Al
4
{sel}{mode}
{coords}"""
frac = ["0 0 0", "0 0.5 0.5", "0.5 0 0.5", "0.5 0.5 0"]
a = 4.04
variants = {
    "Direct, scale 1": dict(scale=1.0, a=a, sel="", mode="Direct", coords="\n".join(frac)),
    "Direct, scale 4.04 (unit vectors)": dict(scale=a, a=1.0, sel="", mode="Direct", coords="\n".join(frac)),
    "Cartesian": dict(scale=1.0, a=a, sel="", mode="Cartesian", coords="\n".join(" ".join(str(float(x) * a) for x in f.split()) for f in frac)),
    "Selective dynamics": dict(scale=1.0, a=a, sel="Selective dynamics\n", mode="Direct", coords="\n".join(f + " T T T" for f in frac)),
}
d = tempfile.mkdtemp()
summ = os.path.join(d, "SUMMARY"); open(summ, "w").write("0.00 x x -14.9\n0.01 x x -14.8\n")
for name, kw in variants.items():
    p = os.path.join(d, "POSCAR"); open(p, "w").write(base.format(**kw) + "\n")
    try:
        f, cell, basis = load_cell(p)
        Bf = basis
        ok_basis = np.allclose(np.sort(np.round(Bf, 4), axis=0), np.sort(np.array([[float(x) for x in s.split()] for s in frac]), axis=0))
        msg = "formula=%s cell_diag=%s basis_ok(fractional)=%s" % (f, np.round(np.diag(cell), 3), ok_basis)
    except Exception as e:
        msg = "load_cell raises %s: %s" % (type(e).__name__, e)
    try:
        V, E = load_V_E(summ, p, units="eV/atom")
        msg += " | load_V_E V(d=0)=%.4f A^3/at (true %.4f)" % (V[0], a ** 3 / 4)
    except Exception as e:
        msg += " | load_V_E raises %s" % type(e).__name__
    print("%-36s %s" % (name, msg))
