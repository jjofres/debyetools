"""Phase 4: Cp and alpha from eval_props vs from a finite-difference Hessian of the total F (f2min with P=0)."""
import sys, os, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
import debyetools.potentials as potentials
from debyetools.ndeb import nDeb
P = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
eos = potentials.BM(parameters=P); eos.fitEOS(np.linspace(.9, 1.1, 5) * P[1], np.zeros(5), initial_parameters=np.array(P), fit=False)
for mode, ia in [("jjsl", (-2e-5, 1.5)), ("Sl", (-2e-5, 1.5)), ("DM", (-2e-5, 1.5)), ("Sl", (0, 1))]:
    nd = nDeb(0.31681, 0.0269815, ia, eos, [0, 0, 0, 0], (8.46, 1.69, 933, 0.0), (0, 0, 0), mode=mode)
    nd.vib.V0_DM = eos.V0
    for T, fv in [(300., 1.01), (800., 1.04)]:
        V = fv * eos.V0
        F = lambda t, v: float(np.real(nd.f2min(t, v, 0)))
        hT, hV = 1e-2 * T, 1e-3 * V
        FTT = (F(T + hT, V) - 2 * F(T, V) + F(T - hT, V)) / hT**2
        FVV = (F(T, V + hV) - 2 * F(T, V) + F(T, V - hV)) / hV**2
        FTV = (F(T + hT, V + hV) - F(T + hT, V - hV) - F(T - hT, V + hV) + F(T - hT, V - hV)) / (4 * hT * hV)
        Cp_fd = -T * (FTT - FTV**2 / FVV); a_fd = -FTV / (V * FVV)
        tp = nd.eval_props(np.array([T]), np.array([V]), P=0)
        print("%-4s a0=%-6g T=%4.0f V/V0=%.2f  Cp code=%.5f FD=%.5f (%+.1e)  alpha code=%.5e FD=%.5e (%+.1e)" % (
            mode, ia[0], T, fv, tp["Cp"][0], Cp_fd, tp["Cp"][0] / Cp_fd - 1, tp["a"][0], a_fd, tp["a"][0] / a_fd - 1))
