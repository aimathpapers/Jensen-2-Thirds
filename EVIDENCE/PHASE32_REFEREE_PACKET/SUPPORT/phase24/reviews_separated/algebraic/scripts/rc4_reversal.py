#!/usr/bin/env python3
"""RC-4: Independent reconstruction of Gate B4 (reversal adapter).

Definitions re-entered from MSS/MMP conventions:
  Descending monic: p(x) = sum_k (-1)^k e_k(r) x^{d-k}; MSS multiplicative
  finite-free convolution  (p x_d q) = sum_k (-1)^k e_k(r)e_k(s)/C(d,k) x^{d-k}.
  Reversal p^vee(x) = x^d p(1/x)/p(0).
  Ascending constant-term-one: p(y) = prod(1 - y/r_i).

Checks:
  1. Sanity of the descending formula against expected-characteristic-polynomial
     special cases (d=1,2 with diagonal matrices).
  2. (p x_d q)^vee == p^vee x_d q^vee for generic coefficients (symbolic) and
     for random positive-rooted instances (exact rational).
  3. The manuscript identity (F):
        _3F_2(-d,A,C;B,D; (D/(AC)) y) == q_{A,B}(y) x_d q_{C,D}(D y)
     in ascending constant-term-one normalization, exact rational arithmetic.
  4. Roots reciprocate under reversal and log mesh is preserved.
"""
import itertools
import random

import sympy as sp

x, y = sp.symbols("x y")


def desc_boxtimes(apoly, bpoly):
    """MSS multiplicative finite-free convolution, descending SIGNED
    coefficient list index k = coeff of x^{d-k} (leading first).
    For p_k = (-1)^k e_k the signed output is (-1)^k p_k q_k / C(d,k)."""
    d = len(apoly) - 1
    assert len(bpoly) == d + 1
    out = []
    for k in range(d + 1):
        out.append(sp.simplify((-1) ** k * apoly[k] * bpoly[k] / sp.binomial(d, k)))
    return out


def reverse_desc(coeffs):
    """Descending monic -> ascending constant-term-one coefficients."""
    const = coeffs[-1]
    return [sp.simplify(c / const) for c in reversed(coeffs)]


def roots_to_desc(roots):
    p = sp.Poly(1, x)
    for r in roots:
        p = p * sp.Poly(x - r, x)
    return p.all_coeffs()


def roots_to_asc(roots):
    p = sp.Poly(1, y)
    for r in roots:
        p = p * sp.Poly(1 - y / r, y)
    return [sp.simplify(c) for c in reversed(p.all_coeffs())]


# ---------------------------------------------------------------- 1. sanity
# d=1: (x-a) x_1 (x-b) = x - ab
res = desc_boxtimes([1, -sp.Symbol("a")], [1, -sp.Symbol("b")])
assert res == [1, -sp.Symbol("a") * sp.Symbol("b")], res
# d=2 rank-one test: e_k formula gives x^2 - (a1 b1)/2 x + a2 b2
a1s, a2s, b1s, b2s = sp.symbols("a1 a2 b1 b2")
res = desc_boxtimes([1, -a1s, a2s], [1, -b1s, b2s])
assert res == [1, -a1s * b1s / 2, a2s * b2s], res
print("1. sanity cases (d=1, d=2 diagonal) OK")

# ---------------------------------------------------------------- 2. reversal
d = 4
r = sp.symbols("r1:5")
s = sp.symbols("s1:5")
pr = roots_to_desc(list(r))
qr = roots_to_desc(list(s))
conv = desc_boxtimes(pr, qr)
conv_asc = reverse_desc(conv)           # (p x q)^vee ascending coeffs
pr_asc = reverse_desc(pr)
qr_asc = reverse_desc(qr)
# ascending bivariate formula: c_j = (-1)^j p_j q_j / C(d,j)
conv_from_asc = [sp.simplify((-1) ** j * pr_asc[j] * qr_asc[j] / sp.binomial(d, j))
                 for j in range(d + 1)]
assert all(sp.simplify(a - b) == 0 for a, b in zip(conv_asc, conv_from_asc)), \
    "symbolic reversal identity failed"
print("2a. symbolic reversal identity (p x_d q)^vee = p^vee x_d q^vee OK (d=4, generic)")

random.seed(24)
for trial in range(5):
    rr = [sp.Rational(random.randint(1, 40), random.randint(1, 9)) for _ in range(5)]
    ss = [sp.Rational(random.randint(1, 40), random.randint(1, 9)) for _ in range(5)]
    conv = desc_boxtimes(roots_to_desc(rr), roots_to_desc(ss))
    lhs = reverse_desc(conv)
    rhs = [sp.simplify((-1) ** j * roots_to_asc(rr)[j] * roots_to_asc(ss)[j]
                       / sp.binomial(5, j)) for j in range(6)]
    assert all(sp.simplify(a - b) == 0 for a, b in zip(lhs, rhs))
print("2b. numeric reversal identity OK (5 random positive-root instances, d=5)")

# ---------------------------------------------------------------- 3. identity (F)
def jacobi2F1_asc(dd, U, V, arg_scale=1):
    """Ascending coeffs of _2F_1(-d,U;V; arg_scale*y/U) with exact rationals."""
    coeffs = []
    for j in range(dd + 1):
        coeffs.append(sp.simplify(sp.rf(-dd, j) * sp.rf(U, j) / (sp.rf(V, j) * sp.factorial(j))
                                  * sp.Rational(arg_scale, 1) ** j / U ** j))
    return coeffs

def threeF2_asc(dd, AA, BB, CC, DD):
    lamv = DD / (AA * CC)
    coeffs = []
    for j in range(dd + 1):
        coeffs.append(sp.simplify(sp.rf(-dd, j) * sp.rf(AA, j) * sp.rf(CC, j)
                                  / (sp.rf(BB, j) * sp.rf(DD, j) * sp.factorial(j)) * lamv ** j))
    return coeffs

dd, AA, BB, CC, DD = 6, sp.Rational(39), sp.Rational(13), sp.Rational(25, 2), sp.Rational(6)
pA = jacobi2F1_asc(dd, AA, BB, arg_scale=1)            # q_{A,B}(y)
qCD = jacobi2F1_asc(dd, CC, DD, arg_scale=DD)          # q_{C,D}(D*y)
conv = [sp.simplify((-1) ** j * pA[j] * qCD[j] / sp.binomial(dd, j)) for j in range(dd + 1)]
target = threeF2_asc(dd, AA, BB, CC, DD)
match = all(sp.simplify(c - t) == 0 for c, t in zip(conv, target))
print("3. identity (F): q_{A,B} x_d q_{C,D}(D.) == _3F_2(-d,A,C;B,D;Dy/(AC)):", match)
assert match

# ---------------------------------------------------------------- 4. roots under reversal
rr = [sp.Rational(3), sp.Rational(7, 2), sp.Rational(11)]
asc = roots_to_asc(rr)  # p(y) = prod(1 - y/r_i): roots are r_i, constant term 1
p_asc = sp.Poly(sum(c * y**j for j, c in enumerate(asc)), y)
sols = sorted(sp.solve(p_asc.as_expr(), y))
assert sols == sorted(rr), (sols, rr)
# reversal y^d p(1/y) is monic with roots 1/r_i
rev = sp.Poly(sum(c * y ** (len(rr) - j) for j, c in enumerate(asc)), y)
rev_roots = sorted(sp.solve(rev.as_expr(), y))
recip = sorted(sp.Rational(1, 1) / r for r in rr)
assert rev_roots == recip, (rev_roots, recip)
mesh_orig = min(rr[i + 1] / rr[i] for i in range(len(rr) - 1))
mesh_rev = min(recip[i + 1] / recip[i] for i in range(len(recip) - 1))
assert sp.simplify(mesh_rev - mesh_orig) == 0
print("4. reversal reciprocates roots and preserves log mesh OK")

print("RC-4 ALL CHECKS PASSED")
