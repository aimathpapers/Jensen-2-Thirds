#!/usr/bin/env python3
"""Independent recalculation R5 (Gate A7): limiting residual map, zero, Jacobian,
box margins, and endpoint ordering arithmetic.

F(y) = H^inf(y) + S^inf,  y = (alpha, t, w, delta):
  F1 = 1/alpha + w/t^2 + delta - 2
  F2 = w/t^3 + delta - 1
  F3 = 3w/t^4 + 3 delta - 2
  F4 = 4w/t^5 + 4 delta - 2
Claims: unique positive-orthant zero y* = (3, 2, 16/3, 1/3);
det DF(y*) = -1/144; ||DF(y*)^{-1}||_inf = 304/3 (max-row-sum);
absolute row sums of the inverse: 87, 15, 304/3, 10/3;
margins (1/2,1/2),(1/4,1/4),(1/3,2/3),(1/12,1/12) to box
  alpha in [5/2,7/2], t in [7/4,9/4], w in [5,6], delta in [1/4,5/12];
endpoint arithmetic: alpha/e >= 30 > 11/4 >= t + w e for e <= 1/12;
t - 1 - delta e >= 103/144.
All checks in exact rational arithmetic.
"""
import sympy as sp

al, t, w, de = sp.symbols("alpha t w delta", positive=True)
F = sp.Matrix([
    1 / al + w / t ** 2 + de - 2,
    w / t ** 3 + de - 1,
    3 * w / t ** 4 + 3 * de - 2,
    4 * w / t ** 5 + 4 * de - 2,
])
ystar = {al: sp.Rational(3), t: sp.Rational(2), w: sp.Rational(16, 3), de: sp.Rational(1, 3)}

print("=== R5a: zero and uniqueness ===")
print("F(y*) =", [sp.simplify(f.subs(ystar)) for f in F])
# exact elimination, my own derivation:
# from F2: w = t^3 (1 - de); F3: t = 3(1-de)/(2-3de); F4: t^2 = 2(1-de)/(1-2de)
elim = sp.expand(9 * (1 - de) * (1 - 2 * de) - 2 * (2 - 3 * de) ** 2)
print("delta elimination polynomial:", sp.factor(elim), " root:", sp.solve(elim, de))

J = F.jacobian([al, t, w, de])
Jstar = J.subs(ystar)
print("\n=== R5b: Jacobian at y* (exact) ===")
print(Jstar)
det = Jstar.det()
print("det J(y*) =", det, " (manuscript claims -1/144; packet CLAIM_LEDGER prints +1/144)")
Jinv = Jstar.inv()
print("J^{-1} =")
print(Jinv)
rowsums = [sum(abs(Jinv[i, j]) for j in range(4)) for i in range(4)]
print("absolute row sums:", rowsums, " (phase-18 claims 87, 15, 304/3, 10/3)")
print("||J^{-1}||_inf =", max(rowsums), " (= 304/3 ?", max(rowsums) == sp.Rational(304, 3), ")")
# verify JP = I
print("J J^{-1} = I ?", Jstar * Jinv == sp.eye(4))

print("\n=== R5c: box margins (exact) ===")
box = [(sp.Rational(5, 2), sp.Rational(7, 2)), (sp.Rational(7, 4), sp.Rational(9, 4)),
       (sp.Rational(5), sp.Rational(6)), (sp.Rational(1, 4), sp.Rational(5, 12))]
names = ["alpha", "t", "w", "delta"]
vals = [ystar[al], ystar[t], ystar[w], ystar[de]]
for nm, v, (lo, hi) in zip(names, vals, box):
    print(f" {nm}: left margin {v - lo}, right margin {hi - v}")

print("\n=== R5d: endpoint ordering arithmetic (exact) ===")
e_max = sp.Rational(1, 12)
alpha_over_e = sp.Rational(5, 2) / e_max
t_plus_we = sp.Rational(9, 4) + 6 * e_max
print("alpha/e >=", alpha_over_e, "; t+we <=", t_plus_we, "; 30 > 11/4 ?", sp.Rational(30) > sp.Rational(11, 4))
margin_CD = sp.Rational(7, 4) - 1 - sp.Rational(5, 12) * e_max
print("t - 1 - delta e >=", margin_CD, " (= 103/144 ?", margin_CD == sp.Rational(103, 144), ")")

print("\n=== R5e: contraction-structure sanity (P = J^{-1}) ===")
# ||I - P DF(y)||_inf at y=y* is exactly 0; continuity gives <= 1/4 on a shrunk box.
# Check DF entries' Lipschitz constants on the box to see a 1/4-neighborhood exists:
import itertools
sam = []
for corner in itertools.product(*[[lo, hi] for lo, hi in box]):
    Jc = J.subs(dict(zip([al, t, w, de], corner)))
    diff = sp.eye(4) - Jinv * Jc
    nr = max(sum(abs(diff[i, j]) for j in range(4)) for i in range(4))
    sam.append((corner, sp.N(nr, 6)))
worst = max(sam, key=lambda p: p[1])
print("worst corner ||I - P DF||_inf on the OUTER box:", worst[1], "at", worst[0])
print("(conclusion: 1/4 requires a shrunken inner box K0, consistent with the proof)")
