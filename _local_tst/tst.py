import sympy as sym
import numpy as np
r, m, kv, lam = sym.symbols('r m kv lam')
V = sym.Symbol('V')
E0 = sym.Function('E0')(V)
P0 = sym.Function('P0')(V)

# P0 = -sym.diff(E0,V)
dP0dV = sym.diff(P0,V)
vDPrm = - dP0dV/(r*m)
# lam=0
vDsqrt = sym.sqrt(-1/(r*m)*(dP0dV - 2/3*(lam+1)*P0/V))
vD = kv*V*vDsqrt
dvDdV = sym.diff(vD,V)
d2vDdV2  = sym.diff(dvDdV,V)
d3vDdV3  = sym.diff(d2vDdV2,V)
d4vDdV4  = sym.diff(d3vDdV3,V)
print(sym.simplify(vD))
print(sym.simplify(dvDdV))
print(sym.simplify(d2vDdV2))
print(sym.simplify(d3vDdV3))
print(sym.simplify(d4vDdV4))
