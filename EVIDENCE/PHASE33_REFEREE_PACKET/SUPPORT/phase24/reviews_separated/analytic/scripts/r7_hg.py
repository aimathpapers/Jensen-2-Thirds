#!/usr/bin/env python3
"""R7 v2 (Gate A9): Hermite-Genocchi via independent routes.

Route 1 (exact, Dirichlet moments): for polynomial f, both sides of
  f[x_0..x_m] = int_{simplex} f^{(m)}(sum t_j x_j) dt
are exact rationals.  Simplex moments: int prod t_j^{a_j} dt = prod a_j! / (m+|a|)!.
Route 2 (numerical, cube transform): t_j = u_j prod_{l<j}(1-u_l),
  dt = prod (1-u_j)^{m-j} du; tensor Gauss-Legendre on [0,1]^m; test f = exp
  at node sets including a complex node; compare with recursive divided differences.
Route 3: remainder bound form for a six-zero function.
"""
import mpmath as mp
import sympy as sp

mp.mp.dps = 40

def divdiff(f, xs):
    if len(xs) == 1:
        return f(xs[0])
    return (divdiff(f, xs[1:]) - divdiff(f, xs[:-1])) / (xs[-1] - xs[0])

print("=== R7b (exact polynomial route) ===")
z = sp.symbols("z")

def simplex_monomial_int(alphas, m):
    # int_{simplex_m} prod_{j=0..m} t_j^{a_j} dt = prod a_j! / (m + |a|)!
    import math
    num = 1
    for a in alphas:
        num *= math.factorial(a)
    return sp.Rational(num, math.factorial(m + sum(alphas)))

def hg_poly_monomial(p, m, nodes):
    # f = z^p; f^{(m)} = p!/(p-m)! z^{p-m}; integrate (sum t_j x_j)^{p-m} over simplex
    import math
    coef = sp.Rational(math.factorial(p), math.factorial(p - m))
    q = p - m
    # expand (t_0 x_0 + ... + t_m x_m)^q multinomially
    total = sp.Rational(0)
    from itertools import combinations_with_replacement
    # expand via sympy
    ts = sp.symbols(f"t0:{m + 1}")
    expr = sum(ts[j] * nodes[j] for j in range(m + 1)) ** q
    for term in sp.Poly(sp.expand(expr), *ts).terms():
        powers, c = term
        total += c * simplex_monomial_int(list(powers), m)
    return coef * total

for p, nodes in [(6, list(range(7))), (7, [0, 1, 2, 3, 4, 5, 9]), (8, [0, 1, 2, 3, 4, 5, sp.Rational(11, 2)])]:
    m = len(nodes) - 1
    f = lambda zz: sp.Integer(zz) ** p if isinstance(zz, int) else zz ** p
    dd = divdiff(lambda zz: zz ** p, [sp.Rational(v) for v in nodes])
    hg = hg_poly_monomial(p, m, [sp.Rational(v) for v in nodes])
    print(f" f=z^{p}, nodes={nodes}: recursive dd = {dd},  HG moment value = {hg},  equal: {dd == hg}")

print("\n=== R7b2 (cube-transform Gauss quadrature, f=exp) ===")
def gauss_tensor_simplex_int(g, m, npts=8):
    x, w = mp.polynomial.legendre.gauss_legendre(npts, 1) if hasattr(mp.polynomial.legendre, 'gauss_legendre') else (None, None)
    if x is None:
        # fallback: compute nodes/weights for [0,1] via numpy-free legendre
        from mpmath import legendre as _lg
        # use mp.calculus QuadratureRule instead
        ctx = mp.calculus.quadrature.QuadratureRule(mp)
        x, w = ctx.calc_nodes(10, 1)  # GaussLegendre on its default interval
    return None

# simpler: use mp.calculus quadrature rule API with the MPContext
from mpmath import mp as mpctx
from mpmath.calculus.quadrature import GaussLegendre
# my own Gauss-Legendre nodes/weights on [0,1] via Legendre roots
def gauss_legendre_01(n):
    x = sp.symbols("x")
    Pn = sp.expand(sp.legendre(n, x))
    coeffs = [mp.mpf(str(c)) for c in sp.Poly(Pn, x).all_coeffs()]
    dcoeffs = [coeffs[i] * (n - i) for i in range(n)]  # derivative, descending powers
    roots = mp.polyroots(coeffs, maxsteps=200, error=False)
    out = []
    for rt in roots:
        xv = mp.polyval(dcoeffs, rt)
        w = 2 / ((1 - rt ** 2) * xv ** 2)   # weight on [-1,1]
        out.append(((rt + 1) / 2, w / 2))   # map to [0,1]
    return out

_gl = gauss_legendre_01(10)
nodes1d = [p for p, _ in _gl]
weights1d = [w for _, w in _gl]
deg = 10

def simplex_int_cube(g, m):
    from itertools import product as iprod
    total = mp.mpf(0)
    for idxs in iprod(range(deg), repeat=m):
        us = [nodes1d[i] for i in idxs]
        # t_j = u_j prod_{l<j} (1-u_l); j = 1..m ; t_0 = prod (1-u_l)
        t = []
        prodterm = mp.mpf(1)
        for j in range(1, m + 1):
            t.append(us[j - 1] * prodterm)
            prodterm *= (1 - us[j - 1])
        t0 = prodterm
        jac = mp.mpf(1)
        for j in range(1, m + 1):
            jac *= (1 - us[j - 1]) ** (m - j)
        wgt = mp.mpf(1)
        for i in idxs:
            wgt *= weights1d[i]
        total += wgt * jac * g([t0] + t)
    return total

for m, zs in [(1, [mp.mpf(0), mp.mpf(2)]),
              (2, [mp.mpf(0), mp.mpf(1), mp.mpf("1.5")]),
              (6, [mp.mpf(j) for j in range(6)] + [mp.mpf("3.5") + mp.mpf("0.8") * 1j])]:
    f = lambda zz: mp.e ** zz
    g = lambda tt: mp.e ** (sum(a * b for a, b in zip(tt, zs)))  # f^{(m)} = exp
    hg = simplex_int_cube(g, m)
    dd = divdiff(f, zs)
    print(f" m={m}: HG quadrature = {mp.nstr(hg, 18)}")
    print(f"      recursive dd   = {mp.nstr(dd, 18)}   rel diff = {mp.nstr(abs(hg - dd) / abs(dd), 3)}")

print("\n=== R7d: 720 normalization through the integral route ===")
val = simplex_int_cube(lambda tt: mp.mpf(720), 6)  # f = z^6, f^{(6)} = 720
print(" int_simplex 720 dt =", mp.nstr(val, 15), " (must be 1)")

print("\n=== R7c: six-zero remainder bound ===")
f = lambda zz: mp.fprod([zz - j for j in range(6)]) * mp.e ** (zz / 10)
for zv in [mp.mpf("2.5"), mp.mpf("3.5") + mp.mpf("0.8") * 1j, mp.mpf("-1.2"), mp.mpf("7.7")]:
    zs = [mp.mpf(j) for j in range(6)] + [zv]
    dd = divdiff(f, zs)
    prodv = mp.fprod([zv - j for j in range(6)])
    rel = abs(f(zv) - dd * prodv) / abs(f(zv)) if f(zv) != 0 else abs(dd * prodv)
    print(f" z={mp.nstr(zv, 10)}: |f(z) - f[0..5,z]*prod| / |f(z)| = {mp.nstr(rel, 3)}")
# sup-bound form
zv = mp.mpf("3.5") + mp.mpf("0.8") * 1j
supf6 = max(abs(mp.diff(f, mp.mpf(a) + mp.mpf("0.8") * 1j * lam, 6))
            for a in mp.linspace(0, 5, 41) for lam in mp.linspace(0, 1, 11))
bound = supf6 * abs(mp.fprod([zv - j for j in range(6)])) / 720
print(f" |f(3.5+0.8i)| = {mp.nstr(abs(f(zv)), 8)} <= {mp.nstr(bound, 8)}: {abs(f(zv)) <= bound}")
