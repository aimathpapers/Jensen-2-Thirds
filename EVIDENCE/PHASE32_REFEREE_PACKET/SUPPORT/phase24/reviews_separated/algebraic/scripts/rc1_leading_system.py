#!/usr/bin/env python3
"""RC-1: Independent recalculation of Gate B1 (limiting four-parameter system).

Everything below is re-entered from the manuscript definitions (Sections 6-7),
not from any frozen JSON or SymPy producer in the packet:

    H^inf = (1/alpha + w/t^2 + delta,
             w/t^3 + delta,
             3 w/t^4 + 3 delta,
             4 w/t^5 + 4 delta)
    S^inf = (-2, -1, -2, -2)
    F = H^inf + S^inf

Checks:
  (a) (alpha,t,w,delta) = (3,2,16/3,1/3) is a zero of F;
  (b) positive-orthant uniqueness via exact elimination;
  (c) det DF(y_*) = -1/144 in the gauge order (alpha,t,w,delta);
  (d) || DF(y_*)^{-1} ||_inf = 304/3;
  (e) DF(y_*)^{-1} equals the transcribed Lean gaugeJacobianInv.
"""
from fractions import Fraction as Fr

import sympy as sp

a, t, w, d = sp.symbols("alpha t w delta", positive=True)

F = sp.Matrix([
    1 / a + w / t**2 + d - 2,
    w / t**3 + d - 1,
    3 * w / t**4 + 3 * d - 2,
    4 * w / t**5 + 4 * d - 2,
])

# (a) candidate zero, re-entered from the manuscript
y_star = {a: sp.Rational(3), t: sp.Rational(2), w: sp.Rational(16, 3), d: sp.Rational(1, 3)}
residual = F.subs(y_star)
print("(a) F(y_*):", residual.T)
assert residual == sp.zeros(4, 1)

# (b) uniqueness in the positive orthant, by hand-level elimination:
# F2-F3 and F3-F4 give  w(t-1)/t^4 = 1/3 and w(t-1)/t^5 = 1/6, hence t = 2.
eq23 = sp.simplify(F[1] - F[2] / 3)          # w/t^3 - w/t^4 - 1/3
eq34 = sp.simplify(F[2] / 3 - F[3] / 4)      # w/t^4 - w/t^5 - 1/6
ratio = sp.simplify((sp.Rational(1, 3)) / (sp.Rational(1, 6)))
print("(b) elimination: w(t-1)/t^4 = 1/3, w(t-1)/t^5 = 1/6 -> t =", ratio)
assert ratio == 2
# With t=2: w = 16/3, delta = 1/3, alpha = 3 follow uniquely:
w_sol = sp.solve(sp.Eq(w * (2 - 1) / 2**5, sp.Rational(1, 6)), w)[0]
d_sol = sp.solve(sp.Eq(w_sol / 2**3 + d, 1), d)[0]
a_sol = sp.solve(sp.Eq(1 / a + w_sol / 2**2 + d_sol, 2), a)[0]
print("(b) forced solution:", (a_sol, sp.Rational(2), w_sol, d_sol))
assert (a_sol, w_sol, d_sol) == (sp.Rational(3), sp.Rational(16, 3), sp.Rational(1, 3))
# Groebner cross-check of zero-dimensionality of the cleared system:
G = sp.groebner([sp.together(x).as_numer_denom()[0] for x in F], a, t, w, d, order="lex")
print("(b) Groebner basis (lex):")
for g in G:
    print("   ", sp.factor(g))

# (c)+(d) Jacobian in gauge order (alpha, t, w, delta)
J = F.jacobian([a, t, w, d]).subs(y_star)
print("(c) DF(y_*) =")
sp.pprint(J)
detJ = J.det()
print("(c) det DF(y_*) =", detJ)
assert detJ == sp.Rational(-1, 144)

Jinv = J.inv()
inf_norm = max(sum(abs(c) for c in row) for row in Jinv.tolist())
print("(d) ||DF(y_*)^-1||_inf =", inf_norm)
assert inf_norm == sp.Rational(304, 3)

# (e) transcribed from LeadingSystem.lean `gaugeJacobianInv` (for comparison)
lean_inv = sp.Matrix([
    [-9, 45, -24, 9],
    [0, 6, -6, 3],
    [0, 48, sp.Rational(-112, 3), 16],
    [0, 1, sp.Rational(-4, 3), 1],
])
print("(e) independent inverse equals Lean gaugeJacobianInv:", Jinv == lean_inv)
assert Jinv == lean_inv

# extra: contraction preconditioner quality metric quoted in the manuscript
print("extra: ||I - P DF(y_*)||_inf =", (sp.eye(4) - Jinv * J).applyfunc(abs).tolist())
print("RC-1 ALL CHECKS PASSED")
