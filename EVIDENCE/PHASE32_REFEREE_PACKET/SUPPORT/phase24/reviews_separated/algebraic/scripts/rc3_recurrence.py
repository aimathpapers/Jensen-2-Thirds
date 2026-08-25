#!/usr/bin/env python3
"""RC-3: Independent recalculation of Gate B7 (shifted _3F_2 ODE + recurrence).

All formulas re-entered from definitions:
  p_F(y) = _3F_2(-d, A, C; B, D; lambda*y),  lambda = D/(A*C).
  g_m(y) = _3F_2(m-d, A+m, C+m; B+m, D+m; lambda*y) ~ p_F^(m).
  Generic _3F_2(a1,a2,a3; b1,b2; z) ODE:
     [theta (theta+b1-1)(theta+b2-1) - z (theta+a1)(theta+a2)(theta+a3)] g = 0.

Part 1: verify the generic ODE from the series definition (coefficient level).
Part 2: expand Euler operators (Stirling numbers) -> four P_{i,m}; compare with
        closed forms transcribed from DirectRecurrence.lean.
Part 3: exact polynomial-identity verification of the recurrence
        sum_i P_{i,m} T_{m+i} == 0 on genuine _3F_2 polynomials, multiple
        degrees and parameter tuples, full index range 0 <= m <= d.
Part 3b: derivative identity p_F^(m) == prefactor * g_m.
"""
import sympy as sp

A, B, C, D, y = sp.symbols("A B C D y")
d, m = sp.symbols("d m")
lam = D / (A * C)

# ---------------------------------------------------------------- Part 1
a1, a2, a3, b1, b2 = sp.symbols("a1 a2 a3 b1 b2")
k = sp.symbols("k", integer=True, positive=True)
ck = sp.rf(a1, k) * sp.rf(a2, k) * sp.rf(a3, k) / (sp.rf(b1, k) * sp.rf(b2, k) * sp.factorial(k))
ratio_cprev_over_ck = sp.simplify(ck.subs(k, k - 1) / ck)
ode_res = sp.simplify(k * (k + b1 - 1) * (k + b2 - 1)
                      - (k - 1 + a1) * (k - 1 + a2) * (k - 1 + a3) * ratio_cprev_over_ck)
print("Part1: generic _3F_2 ODE coeff residual =", ode_res)
assert ode_res == 0

# ---------------------------------------------------------------- Part 2
# Euler-operator expansion: theta^j g = sum_i S(j,i) y^i g^(i)
S = [[sp.Integer(0)] * 4 for _ in range(4)]
S[0][0] = 1
for j in range(1, 4):
    for i in range(1, j + 1):
        S[j][i] = S[j - 1][i - 1] + i * S[j - 1][i]

aa1, aa2, aa3 = m - d, A + m, C + m
bb1, bb2 = B + m, D + m
s1 = sp.expand(aa1 + aa2 + aa3)
s2 = sp.expand(aa1 * aa2 + aa1 * aa3 + aa2 * aa3)
s3 = sp.expand(aa1 * aa2 * aa3)

# LHS theta(theta + B+m-1)(theta + D+m-1): coefficients of theta^1, theta^2, theta^3
u1, u2 = B + m - 1, D + m - 1
lhs_coeffs = {1: sp.expand(u1 * u2), 2: sp.expand(u1 + u2), 3: sp.Integer(1)}
# RHS factor (theta+a1)(theta+a2)(theta+a3): coefficients of theta^0..3
rhs_coeffs = {0: s3, 1: s2, 2: s1, 3: sp.Integer(1)}

P = {}
for i in range(4):  # coefficient of T_{m+i}
    lhs_ci = sum(c * S[j][i] for j, c in lhs_coeffs.items())
    rhs_ci = sum(c * S[j][i] for j, c in rhs_coeffs.items())
    P[i] = sp.expand(lhs_ci - lam * y * rhs_ci)
P3, P2, P1, P0 = P[3], P[2], P[1], P[0]

# Closed forms transcribed from DirectRecurrence.lean:
lean_P3 = (A * C - D * y) / (A * C)
lean_P2 = (A * C * (B + D + 2 * m + 1) - A * D * y - C * D * y
           + D * d * y - 3 * D * m * y - 3 * D * y) / (A * C)
lean_P0 = D * y * (A + m) * (C + m) * (d - m) / (A * C)
lean_P1 = (A * B * C * D + A * B * C * m + A * C * D * m -
           A * C * D * y + A * C * m**2 + A * D * d * y -
           2 * A * D * m * y - A * D * y + C * D * d * y -
           2 * C * D * m * y - C * D * y + 2 * D * d * m * y +
           D * d * y - 3 * D * m**2 * y - 3 * D * m * y - D * y) / (A * C)

for name, mine, theirs in [("P3", P3, lean_P3), ("P2", P2, lean_P2),
                           ("P1", P1, lean_P1), ("P0", P0, lean_P0)]:
    diff = sp.simplify(sp.together(mine - theirs))
    print(f"Part2: {name} matches Lean closed form:", diff == 0)
    assert diff == 0
print("Part2: P3 =", sp.factor(P3))
print("Part2: P2 =", sp.factor(P2))
print("Part2: P1 =", sp.factor(P1))
print("Part2: P0 =", sp.factor(P0))

# ---------------------------------------------------------------- Part 3
def pF_poly(dd, AA, BB, CC, DD, lamv):
    """Exact rational coefficients of _3F_2(-d,A,C;B,D; lamv*y)."""
    coeffs = []
    term = sp.Rational(1)
    for j in range(dd + 1):
        if j > 0:
            term *= (sp.Rational(-dd + j - 1)) * (AA + j - 1) * (CC + j - 1) \
                    / ((BB + j - 1) * (DD + j - 1) * j) * lamv
        coeffs.append(sp.simplify(term))
    return sp.Poly(sum(c * y**j for j, c in enumerate(coeffs)), y, domain="QQ")

def recurrence_holds(dd, AA, BB, CC, DD, mm):
    lamv = DD / (AA * CC)
    p = pF_poly(dd, AA, BB, CC, DD, lamv)
    subs = {A: AA, B: BB, C: CC, D: DD, d: dd, m: mm}
    Pn = [sp.Poly(sp.cancel(P[i].subs(subs)), y, domain="QQ") for i in range(4)]
    derivs = [p]
    for _ in range(mm + 3):
        derivs.append(derivs[-1].diff())
    total = sp.Poly(0, y, domain="QQ")
    for i in range(4):
        Tk_num = derivs[mm + i] * sp.Poly(y ** (mm + i), y, domain="QQ")
        total += Pn[i] * Tk_num
    return total.is_zero

tuples = [
    (6, sp.Rational(40), sp.Rational(12), sp.Rational(11), sp.Rational(6)),
    (8, sp.Rational(120), sp.Rational(16), sp.Rational(15), sp.Rational(8)),
    (10, sp.Rational(300), sp.Rational(20), sp.Rational(19), sp.Rational(10)),
    (5, sp.Rational(7, 2), sp.Rational(3), sp.Rational(5, 2), sp.Rational(3, 2)),
    (7, sp.Rational(50), sp.Rational(9), sp.Rational(17, 2), sp.Rational(4)),
]
ok = True
for (dd, AA, BB, CC, DD) in tuples:
    for mm in range(0, dd + 1):
        good = recurrence_holds(dd, AA, BB, CC, DD, mm)
        ok &= good
        if not good:
            print("FAIL at d,m =", dd, mm)
print("Part3: recurrence identity holds for all (d,m) across", len(tuples), "tuples:", ok)
assert ok

# Part 3b: derivative identity p_F^(m) == (-d)_m(A)_m(C)_m/((B)_m(D)_m) lam^m g_m
dd, AA, BB, CC, DD = 7, sp.Rational(50), sp.Rational(9), sp.Rational(17, 2), sp.Rational(4)
lamv = DD / (AA * CC)
p = pF_poly(dd, AA, BB, CC, DD, lamv)
mm = 3
lhs = p
for _ in range(mm):
    lhs = lhs.diff()
pref = sp.rf(-dd, mm) * sp.rf(AA, mm) * sp.rf(CC, mm) / (sp.rf(BB, mm) * sp.rf(DD, mm)) * lamv**mm
gm = pF_poly(dd - mm, AA + mm, BB + mm, CC + mm, DD + mm, lamv)  # SAME lambda
rhs = gm.mul_ground(sp.simplify(pref))
print("Part3b: p_F^(m) == prefactor * shifted _3F_2 (same lambda):", lhs == rhs)
assert lhs == rhs

print("RC-3 ALL CHECKS PASSED")
