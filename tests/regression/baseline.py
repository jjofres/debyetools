"""
Regression baseline for debyetools (review Phase 0, extended in fix step A3).

    python tests/regression/baseline.py generate   # writes golden.npz + golden_meta.json
    python tests/regression/baseline.py check      # re-runs and compares against golden.npz
    pytest tests/regression                        # same check as a test

Can be run from any directory. Layers (first path component of each key):
  fit/*   : results of fitting (EOS, electronic, Poisson). Optimizer/version dependent -> loose tolerance.
  eval/*  : deterministic evaluations with FIXED parameters (EOS derivatives, eval_props on a T,V grid).
            These should be bit-for-bit stable; any change here is a real change in the formulas.
  pipe/*  : full pipeline (min_G + eval_props) with fixed parameters. Since B12 min_G solves P(V) = P exactly
            (brentq), so V and the properties are deterministic; the residual pressure 'P' (~1e-4 Pa) is compared
            with an absolute tolerance (TOL_SUFFIX).
  io/*    : file readers, elastic constants, pair analysis (deterministic).
Errors are recorded by exception type only, so the golden file does not depend on numpy's message wording.
BM4 and MU2 are placeholders (decisions D2/D3) and are not part of the baseline.
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
TOL = {"fit": dict(rtol=1e-6, atol=1e-12), "eval": dict(rtol=1e-11, atol=1e-14), "pipe": dict(rtol=1e-6, atol=1e-12),
       "io": dict(rtol=1e-11, atol=1e-14)}
# per-key overrides: get_EM uses curve_fit, scipy 1.13 vs 1.15 differ by ~1.3e-6
TOL_PREFIX = {"fit/get_EM/": dict(rtol=1e-5, atol=1e-12),
              # C8: fit_FS is a linear least-squares solve; the 6-term Cp fit (cp_T3=True) is ill-conditioned
              # (scaled condition number ~2e4), so its coefficients get a slightly wider tolerance.
              "pipe/fit_FS_T3/": dict(rtol=1e-5, atol=1e-12)}
# per-suffix overrides: pipe/*/P is the pressure residual of min_G (target 0 Pa, |P| < 1e-3 Pa since B12)
TOL_SUFFIX = {("pipe", "/P"): dict(rtol=0, atol=1.0)}

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
EOS_5P = []  # BM4, MU2: placeholders, excluded from the baseline (decisions D2/D3)
MODES = ["jjsl", "DM", "Sl", "mfv", "VZ", "jjdm", "jjfv"]

out, errors = {}, {}


def put(key, val):
    a = np.atleast_1d(np.asarray(val, dtype=float))
    out[key] = a


def guard(name, fn):
    try:
        fn()
    except Exception as e:  # record, keep going
        errors[name] = type(e).__name__
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


# ------------------------------------------------------------------------------------------
# Extension (fix plan step A3): code paths that the original baseline did not exercise.
# ------------------------------------------------------------------------------------------
def layer_ext():
    from debyetools.debfunct import D_3, dD_3dx, d2D_3dx2, d3D_3dx3
    from debyetools.pairanalysis import pair_analysis
    from debyetools.fs_compound_db import fit_FS
    from debyetools.optim import ga_fitting
    import random, io, contextlib, tempfile

    # (1) Debye function and derivatives on a wide x grid (bands x~16 and x>=500 included)  [2.1, 2.2, 2.3]
    def fdeb():
        xs = np.array([1e-3, 1e-2, 0.1, 0.5, 1., 2., 5., 10., 15., 15.79, 15.8, 16., 20., 24., 30., 50., 100., 400., 499., 500., 600., 653., 700., 709.7, 709.8, 1000.])
        d0 = D_3(xs); d1 = dD_3dx(xs, d0); d2 = d2D_3dx2(xs, d0, d1); d3 = d3D_3dx3(xs, d0, d1, d2)
        put("eval/debfunct/x", xs); put("eval/debfunct/D3", d0); put("eval/debfunct/dD3", d1)
        put("eval/debfunct/d2D3", d2); put("eval/debfunct/d3D3", d3)
    guard("eval/debfunct", fdeb)

    # (2) eval_props at low T and in the x~16 band (array T), and scalar-T vibrational derivatives  [2.1, 2.2, 4.5]
    def flowT():
        eos = make_eos("BM", P_EOS4)
        nd = nDeb(NU_AL, M_AL, (0, 1), eos, P_EL_AL, P_DEF_AL, (0, 0, 0), mode="jjsl")
        T = np.array([0.1, 0.3, 0.6, 1., 2., 20., 24., 28., 32.])
        tp = nd.eval_props(T.copy(), np.full_like(T, eos.V0), P=0)
        for k in ["tD", "Cv", "Cp", "S", "a", "Fvib", "Svib", "Cvvib", "dKtdT_P", "dadP_T", "dCpdP_T"]:
            put("eval/lowT/%s" % k, tp[k])
        v = nd.vib
        for T1 in [0.3, 28.]:
            v.set_int_anh(T1, eos.V0); v.set_theta(T1, eos.V0)
            put("eval/lowT/scalar_T%g/F_dFdT_d2FdT2" % T1, [v.F(T1, eos.V0), v.dFdT_V(T1, eos.V0), v.d2FdT2_V(T1, eos.V0)])
    guard("eval/lowT", flowT)

    # D-5: vib.F for x = theta_D/T < 0.04 with scalar input (used to return 1e10), and f2min
    def fhighT():
        eos = make_eos("BM", P_EOS4)
        nd = nDeb(NU_AL, M_AL, (0, 1), eos, P_EL_AL, P_DEF_AL, (0, 0, 0), mode="jjsl")
        out_ = []
        for T1 in [12000., 20000.]:
            nd.vib.set_int_anh(T1, eos.V0); nd.vib.set_theta(T1, eos.V0)
            out_ += [nd.vib.F(T1, eos.V0), nd.f2min(T1, eos.V0, 0)]
        put("eval/highT/scalar_F_f2min", out_)
    guard("eval/highT", fhighT)

    # (3) non-jj modes with intrinsic anharmonicity, deterministic V0_DM  [4.2, 4.4]
    Tg = np.array([10., 100., 298.15, 600., 1000.])
    for mode in ["Sl", "DM", "VZ", "mfv", "jjsl"]:
        def fna(mode=mode):
            eos = make_eos("BM", P_EOS4)
            nd = nDeb(NU_AL, M_AL, (-2e-5, 1.5), eos, P_EL_AL, P_DEF_AL, (0, 0, 0), mode=mode)
            nd.vib.V0_DM = eos.V0 if "jj" not in mode else nd.vib.V0_DM
            for j, fv in enumerate([0.99, 1.02, 1.05]):
                tp = nd.eval_props(Tg.copy(), np.full_like(Tg, fv * eos.V0), P=0)
                for k in ["tD", "g", "Kt", "Ktp", "Cv", "a", "Cp", "Ks", "S", "G", "dtDdV_T"]:
                    put("eval/intanh/%s/V%d/%s" % (mode, j, k), tp[k])
        guard("eval/intanh/" + mode, fna)

    # (4) eval_Cp vs eval_props with all contributions  [6.6]
    def fcp():
        eos = make_eos("BM", P_EOS4)
        nd = nDeb(NU_AL, M_AL, (-1e-5, 1.5), eos, P_EL_AL, P_DEF_AL, (1e-4, -1e-7, 1e-10), mode="jjsl",
                  xsparams=(10., 0.01, 1e-6, 1e-9, 0.1, 1e3))
        T = np.array([300., 800.]); V = np.array([1.01, 1.035]) * eos.V0
        put("eval/eval_Cp/allcontrib/Cp", nd.eval_Cp(T, V, P=0)["Cp"])
    guard("eval/eval_Cp", fcp)

    # (5) pair analysis and Morse energy with cutoffs shorter than a lattice vector  [7.5]
    ah, ch = 2.95, 4.68
    HCP_CELL = np.array([[ah, 0, 0], [-ah / 2, ah * np.sqrt(3) / 2, 0], [0, 0, ch]])
    HCP_BASIS = np.array([[1 / 3, 2 / 3, .25], [2 / 3, 1 / 3, .75]])
    for tag, (types, basis, cell, cut) in {"fcc_conv_cut3.0": ("AAAA", BASIS_FCC, CELL_AL, 3.0), "fcc_conv_cut5.0": ("AAAA", BASIS_FCC, CELL_AL, 5.0),
                                         "hcp_cut4.0": ("AA", HCP_BASIS, HCP_CELL, 4.0), "hcp_cut5.0": ("AA", HCP_BASIS, HCP_CELL, 5.0)}.items():
        def fpa(types=types, basis=basis, cell=cell, cut=cut, tag=tag):
            d, n, ct = pair_analysis(types, cut, basis, cell)
            put("io/pairs/%s/distances" % tag, d); put("io/pairs/%s/n_per_atom" % tag, n[:, 0])
        guard("io/pairs/" + tag, fpa)
    def fmp3():
        e = potentials.MP("AlAlAlAl", CELL_AL, BASIS_FCC, 3.0, 3, units="J/mol", parameters=np.array(P_MP))
        Vg = np.linspace(0.9, 1.1, 5) * P_EOS4[1]
        put("eval/EOS_MP_cut3.0/E0", [e.E0(v) for v in Vg])
    guard("eval/EOS_MP_cut3.0", fmp3)

    # (6) elastic constants / Poisson ratio for every test OUTCAR.eps, both functions  [7.1, 7.2, 7.3, 1.9]
    import glob
    for f in sorted(glob.glob("tests/inpt_files/*/OUTCAR.eps")):
        mat = f.split("/")[2]
        def fel(f=f, mat=mat):
            EM = load_EM(f)
            put("io/elastic/%s/EM" % mat, EM)
            put("io/elastic/%s/nu" % mat, poisson_ratio(EM))
            put("io/elastic/%s/quiet_pa" % mat, poisson_ratio(EM, quiet=True))
        guard("io/elastic/" + mat, fel)
        def felc(f=f, mat=mat):  # clamped-ion option (B7)
            put("io/elastic_clamped/%s/EM" % mat, load_EM(f, block="clamped"))
        guard("io/elastic_clamped/" + mat, felc)

    # (7) get_EM on the Nb energy-strain example  [7.4]
    def fgem():
        from debyetools.get_elastic import get_EM
        put("fit/get_EM/Nb/EM", get_EM(os.path.join(ROOT, "debyetools", "examples", "Nb", "elastic")))
    guard("fit/get_EM/Nb", fgem)

    # C11: extract_from_DFT on the Nb example (elements_energies.out lives in examples/Nb/calculations)
    def fxd():
        from debyetools.load_data_from_DFT import extract_from_DFT
        nb = os.path.join(ROOT, "debyetools", "examples", "Nb")
        v = extract_from_DFT(nb, energies_file=os.path.join(nb, "calculations", "elements_energies.out"))
        put("fit/extract_from_DFT/Nb/V", v.V); put("fit/extract_from_DFT/Nb/E", v.E)
        put("fit/extract_from_DFT/Nb/E0_Ef_mass", [v.E0, v.Ef, v.mass])
    guard("fit/extract_from_DFT/Nb", fxd)

    # D-2: temperature / pressure grids (cases where the float arange gave extra points past T_final)
    def fgrid():
        from debyetools.aux_functions import gen_Ps
        for Ti, Tf, n in [(0.1, 1000.1, 4), (0.1, 1000.1, 21), (1., 2000., 7), (0.1, 1., 10)]:
            put("io/gen_Ts/%g_%g_%d" % (Ti, Tf, n), gen_Ts(Ti, Tf, n))
        put("io/gen_Ps/1e9_0_3", gen_Ps(1e9, 0., 3))
    guard("io/grids", fgrid)

    # (8) POSCAR variants for load_cell / load_V_E  [1.4, 7.6]
    a = 4.04
    frac = ["0 0 0", "0 0.5 0.5", "0.5 0 0.5", "0.5 0.5 0"]
    tmpl = "Al\n{scale}\n {a} 0 0\n 0 {a} 0\n 0 0 {a}\nAl\n4\n{sel}{mode}\n{coords}\n"
    variants = {"direct_scale1": dict(scale=1.0, a=a, sel="", mode="Direct", coords="\n".join(frac)),
                "direct_scale_a": dict(scale=a, a=1.0, sel="", mode="Direct", coords="\n".join(frac)),
                "cartesian": dict(scale=1.0, a=a, sel="", mode="Cartesian", coords="\n".join(" ".join(str(float(x) * a) for x in s.split()) for s in frac)),
                "selective": dict(scale=1.0, a=a, sel="Selective dynamics\n", mode="Direct", coords="\n".join(s + " T T T" for s in frac))}
    tmpd = tempfile.mkdtemp()
    summ = os.path.join(tmpd, "SUMMARY"); open(summ, "w").write("0.00 x x -14.9\n0.01 x x -14.8\n")
    for tag, kw in variants.items():
        p = os.path.join(tmpd, "POSCAR_" + tag); open(p, "w").write(tmpl.format(**kw))
        def fpc(p=p, tag=tag):
            f, cell, basis = load_cell(p)
            put("io/poscar/%s/cell" % tag, cell); put("io/poscar/%s/basis" % tag, basis)
        def fve(p=p, tag=tag):
            put("io/poscar/%s/V_eV_per_atom" % tag, load_V_E(summ, p, units="eV/atom")[0])
        guard("io/poscar/%s/load_cell" % tag, fpc); guard("io/poscar/%s/load_V_E" % tag, fve)
    # C7: further POSCAR forms (non-triangular cell, negative scale = volume, VASP 4, skewed Cartesian + scale + selective)
    ah, ch = 2.95, 4.68
    Hc = np.array([[ah, 0, 0], [-ah / 2, ah * np.sqrt(3) / 2, 0], [0, 0, ch]]); Hb = np.array([[1 / 3, 2 / 3, .25], [2 / 3, 1 / 3, .75]])
    extra = {"fcc_primitive": "Al\n1.0\n0 2.02 2.02\n2.02 0 2.02\n2.02 2.02 0\nAl\n1\nDirect\n0 0 0\n",
             "negative_scale": "Al\n-65.939264\n1 0 0\n0 1 0\n0 0 1\nAl\n4\nDirect\n" + "\n".join(frac) + "\n",
             "vasp4": "Al3Li\n1.0\n4.0 0 0\n0 4.0 0\n0 0 4.0\n3 1\nDirect\n0 .5 .5\n.5 0 .5\n.5 .5 0\n0 0 0\n",
             "hcp_cart_scale2_sel": "Ti\n2.0\n" + "\n".join(" ".join("%.17g" % (v / 2) for v in r) for r in Hc) + "\nTi\n2\nSelective dynamics\nCartesian\n"
                                    + "\n".join(" ".join("%.17g" % (v / 2) for v in (Hb @ Hc)[k]) + " T T F" for k in range(2)) + "\n"}
    for tag, txt in extra.items():
        p = os.path.join(tmpd, "POSCAR_" + tag); open(p, "w").write(txt)
        def fpc2(p=p, tag=tag):
            f, cell, basis = load_cell(p)
            put("io/poscar/%s/cell" % tag, cell); put("io/poscar/%s/basis" % tag, basis); put("io/poscar/%s/nat" % tag, len(basis))
            put("io/poscar/%s/V_eV_per_atom" % tag, load_V_E(summ, p, units="eV/atom")[0])
        guard("io/poscar/%s/load" % tag, fpc2)

    # (9) FactSage fit on two pipelines  [8.5, 8.6]
    T = gen_Ts(0.1, 1000.1, 21)
    for tag, kw in {"BM_jjsl": {}, "BM_jjsl_allcontrib": dict(p_intanh=(-1e-5, 1.5), p_anh=(1e-4, -1e-7, 1e-10), xs=(10., 0.01, 1e-6, 1e-9, 0.1, 1e3))}.items():
        def ffs(tag=tag, kw=kw):
            eos = make_eos("BM", P_EOS4)
            nd = nDeb(NU_AL, M_AL, kw.get("p_intanh", (0, 1)), eos, P_EL_AL, P_DEF_AL, kw.get("p_anh", (0, 0, 0)), mode="jjsl",
                      xsparams=kw.get("xs", (0,) * 6))
            Tm, Vm = nd.min_G(T.copy(), eos.V0, P=0)
            r = fit_FS(nd.eval_props(Tm, Vm, P=0), 298.15, 1000.1)
            for k in ["Cp", "a", "1/Ks", "Ksp"]:
                put("pipe/fit_FS/%s/%s" % (tag, k.replace("/", "inv")), r[k])
            put("pipe/fit_FS_T3/%s/Cp" % tag, fit_FS(nd.eval_props(Tm, Vm, P=0), 298.15, 1000.1, cp_T3=True)["Cp"])
        guard("pipe/fit_FS/" + tag, ffs)

    # (10) seeded genetic algorithm  [8.1, 8.2, 8.3]
    X = np.linspace(0, 1, 20)
    probs = {"linear": (lambda x, p: p[0] + p[1] * x, 2 + 3 * X, [1.5, 2.5]),
             "quadratic_zero_init": (lambda x, p: p[0] + p[1] * x + p[2] * x ** 2, 2 + 3 * X + 0.5 * X ** 2, [2., 3., 0.])}
    for tag, (fun, Y, p0) in probs.items():
        def fga(tag=tag, fun=fun, Y=Y, p0=p0):
            random.seed(1)
            with contextlib.redirect_stdout(io.StringIO()):
                p = ga_fitting(fun, X, Y, list(p0), npop=20, ngen=40, verbose=False)
            put("fit/ga/%s/params" % tag, p)
        guard("fit/ga/" + tag, fga)
    # B13: zero_scale (parameter with initial guess 0 can move and change sign) and failing / truncated model evaluations
    def fga2():
        g = lambda x, p: p[0] + p[1] * x + p[2] * x ** 2
        with contextlib.redirect_stdout(io.StringIO()):
            put("fit/ga/quadratic_zero_scale/params", ga_fitting(g, X, 2 + 3 * X - 0.5 * X ** 2, [2., 3., 0.], npop=20, ngen=40,
                                                                 verbose=False, seed=3, zero_scale=1.0))
        def bad(x, p):
            if p[0] > 1.8 and p[1] < 2.7: return np.full_like(x, np.nan)
            if p[0] < 1.4: return (p[0] + p[1] * x)[:-3]
            return p[0] + p[1] * x
        with contextlib.redirect_stdout(io.StringIO()):
            put("fit/ga/failing_model/params", ga_fitting(bad, X, 2 + 3 * X, [1.5, 2.5], npop=20, ngen=40, verbose=False, seed=1))
    guard("fit/ga/extra", fga2)


def run_all():
    out.clear(); errors.clear()
    layer_fit(); layer_eval(); layer_pipe(); layer_ext()


def run_check():
    """Run everything and compare with the golden file; returns the number of problems (used by pytest)."""
    np.seterr(all="ignore")
    run_all()
    return compare()


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
        tol = next((v for p_, v in TOL_PREFIX.items() if k.startswith(p_)), TOL[layer])
        tol = next((v for (l_, s_), v in TOL_SUFFIX.items() if layer == l_ and k.endswith(s_)), tol)
        ok = same_nan and np.allclose(a, b, equal_nan=True, **tol)
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
