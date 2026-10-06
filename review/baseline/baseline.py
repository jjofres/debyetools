"""
Phase 0 regression baseline for debyetools.

    python review/baseline/baseline.py generate   # writes golden.npz + golden_meta.json
    python review/baseline/baseline.py check      # re-runs and compares against golden.npz

Run from the repository root. Three layers are stored:
  fit/*   : results of fitting (EOS, electronic, Poisson). Optimizer/version dependent -> loose tolerance.
  eval/*  : deterministic evaluations with FIXED parameters (EOS derivatives, eval_props on a T,V grid).
            These should be bit-for-bit stable; any change here is a real change in the formulas.
  pipe/*  : full pipeline (min_G + eval_props) with fixed parameters. Depends on fmin -> medium tolerance.
"""
import sys, os, json, platform, warnings, traceback
import numpy as np

warnings.filterwarnings("ignore")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import scipy
import debyetools.potentials as potentials
from debyetools.ndeb import nDeb
from debyetools.aux_functions import gen_Ts, load_V_E, load_EM, load_doscar, load_cell
from debyetools.electronic import fit_electronic
from debyetools.poisson import poisson_ratio

HERE = os.path.dirname(os.path.abspath(__file__))
GOLD = os.path.join(HERE, "golden.npz")
META = os.path.join(HERE, "golden_meta.json")
TOL = {"fit": dict(rtol=1e-6, atol=1e-12), "eval": dict(rtol=1e-11, atol=1e-14), "pipe": dict(rtol=1e-6, atol=1e-12)}

AL = "tests/inpt_files/Al_fcc"
AL_TAGS = ["%02da" % i for i in range(1, 22)]
STD_TAGS = None  # load_doscar default: -0.10 ... 0.10

# --- fixed reference parameters (Al fcc, from tests/min_F_tests.py) -----------------
NU_AL, M_AL = 0.31681, 0.0269815
P_EL_AL = [3.8027342892e-01, -1.8875015171e-02, 5.3071034596e-04, -7.0100707467e-06]
P_DEF_AL = (8.46, 1.69, 933, 0.1)
P_EOS4 = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
P_EOS5 = P_EOS4 + [-5.0e-11]
P_MP = [3.492281316e-01, 9.977375168e-01, 3.246481751e+00]
P_EAM = [3.647649855e-03, 1.643670214e+00, 1.201433529e-02, 2.110843838e-02, 2.099552421e-01,
         1.110019124e+00, 9.353164553e-01, 2.032247973e-06, 1.432174178e-01, 1.213592440e+00]
A_AL = 4.0396918604
CELL_AL = np.array([[A_AL, 0, 0], [0, A_AL, 0], [0, 0, A_AL]])
BASIS_FCC = np.array([[0, 0, 0], [0, .5, .5], [.5, 0, .5], [.5, .5, 0]])

EOS_4P = ["BM", "RV", "MG", "TB", "MU", "BM3", "PT"]
EOS_5P = ["BM4", "MU2"]
MODES = ["jjsl", "DM", "Sl", "mfv", "VZ", "jjdm", "jjfv"]

out, errors = {}, {}


def put(key, val):
    a = np.atleast_1d(np.asarray(val, dtype=float))
    out[key] = a


def guard(name, fn):
    try:
        fn()
    except Exception as e:  # record, keep going
        errors[name] = "%s: %s" % (type(e).__name__, e)
        traceback.print_exc(limit=2)


def make_eos(name, params, fit_data=None):
    """Instantiate an EOS with fixed parameters (no fitting)."""
    if name in ("MP", "EAM"):
        eos = getattr(potentials, name)("AlAlAlAl", CELL_AL, BASIS_FCC, 5.0, 3, units="J/mol", parameters=np.array(params))
    else:
        eos = getattr(potentials, name)(parameters=list(params))
    Vd = np.linspace(0.9, 1.1, 11) * P_EOS4[1] if fit_data is None else fit_data[0]
    Ed = np.zeros_like(Vd) if fit_data is None else fit_data[1]
    eos.fitEOS(Vd, Ed, initial_parameters=np.array(params, dtype=float), fit=False)
    return eos


def eos_params(name):
    return {"MP": P_MP, "EAM": P_EAM}.get(name, P_EOS5 if name in EOS_5P else P_EOS4)


# ------------------------------------------------------------------------------------------
def layer_fit():
    V, E = load_V_E(AL + "/SUMMARY.fcc", AL + "/CONTCAR.5", units="J/mol")
    put("fit/Al/V_DFT", V); put("fit/Al/E_DFT", E)
    for name in EOS_4P + EOS_5P:
        def f(name=name):
            eos = getattr(potentials, name)()
            p0 = np.array(eos_params(name), dtype=float)
            eos.fitEOS(V, E, initial_parameters=p0)
            put("fit/Al/EOS_%s/pEOS" % name, eos.pEOS); put("fit/Al/EOS_%s/V0" % name, eos.V0)
        guard("fit/Al/EOS_%s" % name, f)

    def fmp():
        formula, cell, basis = load_cell(AL + "/CONTCAR.5")
        eos = potentials.MP(formula, cell, basis, 5, 3, units="J/mol")
        eos.fitEOS(V, E, initial_parameters=np.array([0.35, 1, 3.5]))
        put("fit/Al/EOS_MP/pEOS", eos.pEOS); put("fit/Al/EOS_MP/V0", eos.V0)
    guard("fit/Al/EOS_MP", fmp)

    def fel():
        Ee, N, Ef = load_doscar(AL + "/DOSCAR.EvV.", list_filetags=AL_TAGS)
        put("fit/Al/Ef", Ef)
        put("fit/Al/p_el", fit_electronic(V, P_EL_AL, Ee, N, Ef))
    guard("fit/Al/el", fel)

    def fnu():
        EM = load_EM(AL + "/OUTCAR.eps"); put("fit/Al/EM", EM); put("fit/Al/nu", poisson_ratio(EM))
    guard("fit/Al/nu", fnu)

    # Other materials (complete DFT sets in tests/inpt_files)
    for mat in ["Cu_fcc", "Mg_hcp", "Ti_hcp", "V_bcc", "Al3Li_D023"]:
        def fm(mat=mat):
            d = "tests/inpt_files/" + mat
            Vm, Em = load_V_E(d + "/SUMMARY.fcc", d + "/CONTCAR.5", units="J/mol")
            put("fit/%s/V_DFT" % mat, Vm); put("fit/%s/E_DFT" % mat, Em)
            eos = potentials.BM()
            p0 = [Em.min(), Vm[np.argmin(Em)], 1e11, 4.5]
            eos.fitEOS(Vm, Em, initial_parameters=np.array(p0))
            put("fit/%s/EOS_BM/pEOS" % mat, eos.pEOS); put("fit/%s/EOS_BM/V0" % mat, eos.V0)
            EM = load_EM(d + "/OUTCAR.eps"); put("fit/%s/nu" % mat, poisson_ratio(EM))
            Ee, N, Ef = load_doscar(d + "/DOSCAR.EvV.")
            put("fit/%s/p_el" % mat, fit_electronic(Vm, P_EL_AL, Ee, N, Ef))
        guard("fit/" + mat, fm)


def layer_eval():
    # (a) EOS energy and derivatives on a fixed V grid
    for name in EOS_4P + EOS_5P + ["MP", "EAM"]:
        def f(name=name):
            eos = make_eos(name, eos_params(name))
            Vg = np.linspace(0.85, 1.15, 13) * P_EOS4[1]
            put("eval/EOS_%s/V" % name, Vg)
            put("eval/EOS_%s/V0" % name, eos.V0)
            for d in ["E0", "dE0dV_T", "d2E0dV2_T", "d3E0dV3_T", "d4E0dV4_T", "d5E0dV5_T", "d6E0dV6_T"]:
                if hasattr(eos, d):
                    put("eval/EOS_%s/%s" % (name, d), [getattr(eos, d)(v) for v in Vg])
        guard("eval/EOS_%s" % name, f)

    # (b) eval_props on fixed (T,V) grid -- no minimisation
    Tg = np.array([1., 10., 50., 100., 298.15, 600., 1000.])

    def props(tag, eos_name, mode="jjsl", p_intanh=(0, 1), p_anh=(0, 0, 0), xs=(0,) * 6, p_def=P_DEF_AL):
        def f():
            eos = make_eos(eos_name, eos_params(eos_name))
            nd = nDeb(NU_AL, M_AL, p_intanh, eos, P_EL_AL, p_def, p_anh, mode=mode, xsparams=xs)
            for j, fv in enumerate([0.98, 1.0, 1.03]):
                V = np.full_like(Tg, fv * eos.V0)
                tp = nd.eval_props(Tg.copy(), V, P=0)
                for k, v in tp.items():
                    try:
                        put("eval/props/%s/V%d/%s" % (tag, j, k), v)
                    except Exception:
                        pass
        guard("eval/props/" + tag, f)

    for name in EOS_4P + EOS_5P + ["MP", "EAM"]:
        props("%s_jjsl" % name, name)
    for mode in MODES:
        props("BM_%s" % mode, "BM", mode=mode)
    props("BM_jjsl_allcontrib", "BM", p_intanh=(-1e-5, 1.5), p_anh=(1e-4, -1e-7, 1e-10),
          xs=(10., 0.01, 1e-6, 1e-9, 0.1, 1e3))


def layer_pipe():
    T = gen_Ts(0.1, 1000.1, 21)

    def run(tag, eos_name, mode="jjsl", p_intanh=(0, 1), p_anh=(0, 0, 0), xs=(0,) * 6):
        def f():
            eos = make_eos(eos_name, eos_params(eos_name))
            nd = nDeb(NU_AL, M_AL, p_intanh, eos, P_EL_AL, P_DEF_AL, p_anh, mode=mode, xsparams=xs)
            Tm, Vm = nd.min_G(T.copy(), eos.V0, P=0)
            tp = nd.eval_props(Tm, Vm, P=0)
            for k in ["T", "V", "tD", "g", "Kt", "Ktp", "Cv", "a", "Cp", "Ks", "G", "E", "S", "P"]:
                put("pipe/%s/%s" % (tag, k), tp[k])
        guard("pipe/" + tag, f)

    for name in EOS_4P + EOS_5P + ["MP", "EAM"]:
        run("%s_jjsl" % name, name)
    for mode in MODES:
        run("BM_%s" % mode, "BM", mode=mode)
    run("BM_jjsl_allcontrib", "BM", p_intanh=(-1e-5, 1.5), p_anh=(1e-4, -1e-7, 1e-10),
        xs=(10., 0.01, 1e-6, 1e-9, 0.1, 1e3))


def run_all():
    layer_fit(); layer_eval(); layer_pipe()


def env():
    import subprocess
    try:
        rev = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        rev = "?"
    return {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__,
            "platform": platform.platform(), "git_head": rev}


def compare():
    g = np.load(GOLD)
    meta = json.load(open(META))
    rows, nbad = [], 0
    for k in sorted(set(g.files) | set(out)):
        layer = k.split("/")[0]
        if k not in out:
            rows.append(("MISSING_NOW", k, "")); nbad += 1; continue
        if k not in g.files:
            rows.append(("NEW", k, "")); continue
        a, b = out[k], g[k]
        if a.shape != b.shape:
            rows.append(("SHAPE", k, "%s vs %s" % (a.shape, b.shape))); nbad += 1; continue
        same_nan = np.array_equal(np.isnan(a), np.isnan(b))
        ok = same_nan and np.allclose(a, b, equal_nan=True, **TOL[layer])
        if not ok:
            with np.errstate(all="ignore"):
                rel = np.nanmax(np.abs(a - b) / np.maximum(np.abs(b), 1e-300))
            rows.append(("DIFF", k, "max rel %.3g" % rel)); nbad += 1
    for e in sorted(set(errors) | set(meta["errors"])):
        if errors.get(e) != meta["errors"].get(e):
            rows.append(("ERRCHG", e, "now=%s | gold=%s" % (errors.get(e), meta["errors"].get(e)))); nbad += 1
    for r in rows:
        print("%-12s %s %s" % r)
    print("\n%d keys compared, %d problems. golden env: %s | now: %s" % (len(g.files), nbad, meta["env"], env()))
    return nbad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "check"
    np.seterr(all="ignore")
    run_all()
    if cmd == "generate":
        np.savez_compressed(GOLD, **out)
        nan_keys = [k for k, v in out.items() if not np.all(np.isfinite(v))]
        json.dump({"env": env(), "errors": errors, "n_keys": len(out), "non_finite_keys": nan_keys},
                  open(META, "w"), indent=1)
        print("wrote %d keys, %d errors, %d keys with nan/inf" % (len(out), len(errors), len(nan_keys)))
        for k, v in errors.items():
            print("ERROR", k, v)
    else:
        sys.exit(1 if compare() else 0)
