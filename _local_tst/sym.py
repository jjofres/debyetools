print('start')
from sympy import *

hbar, wE, kB, Na, T, b = symbols('hbar, wE, Na, kB, T, b')

# f = Function('f')
f = (b/T)**2*exp(b/T)

g = (exp(b/T)-1)**2
print(diff(f,T))
print(diff(g,T))
print(simplify(diff(f,T)/diff(g,T)))
print()
f = b*(2*T + b)
g = (2*T**2*(exp(b/T) - 1))
print(simplify(diff(f,T)/diff(g,T)))

print()
f = b
g = (-2*T*(1 - exp(b/T)) - b*exp(b/T))
print(diff(g,T))

print('end')
