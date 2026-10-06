"""Phase 5: effect of the incomplete Defects.d4FdV4_T on Ktpp (instance override with the complete formula)."""
import sys, os, warnings
import numpy as np
warnings.filterwarnings("ignore"); np.seterr(all="ignore")
sys.path.insert(0, os.getcwd())
import debyetools.potentials as potentials
from debyetools.ndeb import nDeb
from debyetools.defects import kB, NAv
P = [-3.617047894e+05, 9.929931142e-06, 7.618619745e+10, 4.591924487e+00]
eos = potentials.BM(parameters=P); eos.fitEOS(np.linspace(.9, 1.1, 5) * P[1], np.zeros(5), initial_parameters=np.array(P), fit=False)
nd = nDeb(0.31681, 0.0269815, (0, 1), eos, [0, 0, 0, 0], (8.46, 1.69, 933, 0.1), (0, 0, 0), mode="jjsl")
T = np.array([300., 600., 800., 900.]); V = np.array([1.01, 1.025, 1.035, 1.04]) * eos.V0
a = nd.eval_props(T.copy(), V.copy(), P=0)
d = nd.deff
def d4_full(T, V):
    g = lambda k: [(d.Svac(V) * T - d.Evac(V)) / (T * kB), (d.dSvacdV_T(V) * T - d.dEvacdV_T(V)) / (T * kB),
                   (d.d2SvacdV2_T(V) * T - d.d2EvacdV2_T(V)) / (T * kB), (d.d3SvacdV3_T(V) * T - d.d3EvacdV3_T(V)) / (T * kB),
                   (d.d4SvacdV4_T(V) * T - d.d4EvacdV4_T(V)) / (T * kB)][k]
    return -NAv * kB * T * np.exp(g(0)) * (g(4) + 4 * g(3) * g(1) + 3 * g(2) ** 2 + 6 * g(2) * g(1) ** 2 + g(1) ** 4)
print("T, code d4Fdef, complete d4Fdef:", [(t, "%.3e" % d.d4FdV4_T(t, v), "%.3e" % d4_full(t, v)) for t, v in zip(T, V)])
d.d4FdV4_T = d4_full
b = nd.eval_props(T.copy(), V.copy(), P=0)
for k in ["Ktpp", "G^2", "Ktp", "Cp"]:
    print("  %-5s rel. change: %s" % (k, " ".join("%9.2e" % (a[k][i] / b[k][i] - 1) for i in range(len(T)))))
