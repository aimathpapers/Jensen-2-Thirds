#!/usr/bin/env python3
"""Independent recalculation R8: assembly algebra for gates A3, A7, A10 and the
localization/recurrence chain (manuscript sections finitefree/recurrence/assembly).

 1. Geometric tails: sum_{k>=5} 2^{-k} = 1/16, sum_{k>=6} = 1/32.
 2. |e^w - 1| <= 2|w| on |w| <= 1/2 (max ratio scan).
 3. A3 nesting: arcsin(dC/(1-dC)) < 1/800 with dC=1/1000; arctan(eta/(1-eta)) < 1/800.
 4. C_loc product arithmetic: 8 sqrt(Bd) + 8 B sqrt(d/D) + 64 sqrt(Bd) sqrt(d/D)
    <= (12 + 8 sqrt6) sqrt(Bd) given B/D <= 6, d/D <= 1/256;  C_loc < 32; K_0 = 262144.
 5. (Q3),(Q1),(Q0) normalized neighbor coefficients (symbolic).
 6. Recurrence: expand theta(theta+B+m-1)(theta+D+m-1) g = lambda y (theta+m-d)(theta+A+m)(theta+C+m) g
    with theta = y d/dy; read off (H3) coefficients; verify P_3 = 1 - lambda y,
    P_0 = D y (A+m)(C+m)(d-m)/(AC); verify the claimed decompositions
    P_2 = b_{m+1} + (D+m) a + eps_p (y/A)(A - d + 3 + 3m),
    P_1 = c_{m+1} + (D+m) b_m + eps_p (y/A) beta_m
    with b_m = B+m-y+(d-1-2m) y/A, a = 1 - y/A, eps_p = (C-D)/C,
    c_m = (d-m)(1 + m/A) y, beta_m = A(2m+1-d) - d(2m+1) + 3m^2+3m+1.
 7. Ratio-free Jacobi lemma (J): direct root computation of q_{U,V}(y) =
    2F1(-d, U; V; y/U) at boundary and random (U, V, d); check roots in
    [V - 8 sqrt(Vd), V + 8 sqrt(Vd)]; cross-check transported Jacobi matrix
    eigenvalues against polynomial roots.
 8. Note's diagonal identity: U(H(V+2k)+2k(k+1))/((H+2k)(H+2k+2)) - V
    =?= [2k(k+H+1)(U-2V) + V H (d-1)] / ((H+2k)(H+2k+2)), H = U-d-1.
"""
import sympy as sp
import mpmath as mp

mp.mp.dps = 40

print("=== R8.1-3: tails, exp bound, nesting ===")
print("sum_{k>=5} 2^-k =", sp.Rational(1, 16) == sp.summation(sp.Rational(1, 2) ** sp.symbols('k'), (sp.symbols('k'), 5, sp.oo)))
print("sum_{k>=6} 2^-k = 1/32:", sp.summation(sp.Rational(1, 2) ** sp.symbols('k'), (sp.symbols('k'), 6, sp.oo)) == sp.Rational(1, 32))
worst = max(abs(mp.e ** (mp.mpf('0.5') * mp.e ** (1j * th)) - 1) / mp.mpf('0.5') for th in mp.linspace(0, 2 * mp.pi, 2000))
print("max |e^w-1|/|w| on |w|=1/2:", mp.nstr(worst, 8), " < 2 ?", worst < 2)
dC = mp.mpf(1) / 1000
ang = mp.asin(dC / (1 - dC))
print("arcsin(dC/(1-dC)) =", mp.nstr(ang, 12), " < 1/800 =", mp.nstr(mp.mpf(1) / 800, 12), ":", ang < mp.mpf(1) / 800,
      " (also < 1/1000 + 1e-5:", ang < mp.mpf('0.001') + mp.mpf('1e-5'), ")")
eta = mp.mpf(1) / 1000
print("arctan(eta/(1-eta)) =", mp.nstr(mp.atan(eta / (1 - eta)), 12), " < 1/800 ?", mp.atan(eta / (1 - eta)) < mp.mpf(1) / 800)

print("\n=== R8.4: C_loc arithmetic ===")
Bd, rt = sp.symbols("Bd rt", positive=True)
# let u = sqrt(Bd), s = sqrt(d/D) <= 1/16, q = sqrt(B/D) <= sqrt6
u, sq, qq = sp.symbols("u s q", positive=True)
expr = 8 * u + 8 * qq * u * sq / sq * sq  # placeholder no
# directly: 8 sqrt(Bd) + 8 sqrt(Bd) sqrt(B/D) + 64 sqrt(Bd) sqrt(d/D)
tot = 8 * u + 8 * u * qq + 64 * u * sq
bound = (12 + 8 * sp.sqrt(6)) * u
print("worst case at q=sqrt6, s=1/16:", sp.simplify(tot.subs({qq: sp.sqrt(6), sq: sp.Rational(1, 16)}) - bound) == 0)
print("C_loc = 12 + 8 sqrt6 =", mp.nstr(12 + 8 * mp.sqrt(6), 10), " < 32 ?", 12 + 8 * mp.sqrt(6) < 32)
print("256 * 32^2 =", 256 * 32 ** 2)

print("\n=== R8.5: normalized neighbor coefficients (symbolic) ===")
n, B, D, d, Kr, C1, C0 = sp.symbols("n B D d K_r C_1 C_0", positive=True)
P2lo = n / 8
P3up = sp.Integer(2)
rho = Kr * sp.sqrt(B * d)
Q3 = sp.simplify(P3up * rho / P2lo).subs(B, 3 * n)  # B <= 3n
print("Q3 <=", sp.simplify(Q3), " (claimed 16 K_r sqrt(3 d / n))")
P1up = C1 * (n * sp.sqrt(B * d) + n * d)
Q1 = sp.simplify(P1up / (P2lo * rho))
print("Q1 =", Q1, " (claimed (8 C_1/K_r)(1 + sqrt(d/B)))")
P0up = C0 * n ** 2 * d
Q0 = sp.simplify(P0up / (P2lo * rho ** 2))
print("Q0 =", sp.simplify(Q0), " (claimed (8 C_0/K_r^2)(n/B) <= 8 C_0/K_r^2)")

print("\n=== R8.6: recurrence coefficients (symbolic) ===")
y, lam, A, Bb, Cc, Dd, m, d = sp.symbols("y lambda A B C D m d")
g = sp.Function("g")
# theta^j g expansions
T1 = y * g(y).diff(y)
T2 = y ** 2 * g(y).diff(y, 2) + y * g(y).diff(y)
T3 = y ** 3 * g(y).diff(y, 3) + 3 * y ** 2 * g(y).diff(y, 2) + y * g(y).diff(y)
a1, a2, a3 = m - d, A + m, Cc + m
b1, b2 = Bb + m, Dd + m
e1 = a1 + a2 + a3
e2 = a1 * a2 + a1 * a3 + a2 * a3
e3 = a1 * a2 * a3
# theta(theta+b1-1)(theta+b2-1) = theta^3 + (b1+b2-2) theta^2 + (b1-1)(b2-1) theta
lhs = (b1 - 1) * (b2 - 1) * T1 + (b1 + b2 - 2) * T2 + T3
# RHS: lambda y (theta^3 + e1 theta^2 + e2 theta + e3) g
rhs = lam * y * (T3 + e1 * T2 + e2 * T1 + e3 * g(y))
expr = sp.expand(lhs - rhs)
c3 = sp.factor(expr.coeff(g(y).diff(y, 3)))
c2 = sp.factor(expr.coeff(g(y).diff(y, 2)))
c1 = sp.factor(expr.coeff(g(y).diff(y, 1)))
c0 = sp.factor(expr.coeff(g(y)))
print("y^3 g''' coeff:", c3, " (= (1 - lambda y) y^3:", sp.simplify(c3 - (1 - lam * y) * y ** 3) == 0, ")")
print("y^2 g''  coeff:", sp.factor(c2 / y ** 2), " (claimed b1+b2+1 - lambda y (3+e1):",
      sp.simplify(c2 / y ** 2 - (b1 + b2 + 1 - lam * y * (3 + e1))) == 0, ")")
print("y g'   coeff:", sp.factor(c1 / y), " (claimed b1 b2 - lambda y (1+e1+e2):",
      sp.simplify(c1 / y - (b1 * b2 - lam * y * (1 + e1 + e2))) == 0, ")")
print("g      coeff:", c0, " (claimed -lambda y e3:", sp.simplify(c0 + lam * y * e3) == 0, ")")

# P-polynomials in the note's normalization: multiply (H3) by y^m c_m / p_F; P_3 = 1 - lam y,
# P_2 = b1+b2+1 - lam y (3+e1), P_1 = b1 b2 - lam y (1+e1+e2), P_0 = -lam y e3.
P3 = 1 - lam * y
P2 = b1 + b2 + 1 - lam * y * (3 + e1)
P1 = b1 * b2 - lam * y * (1 + e1 + e2)
P0 = -lam * y * e3
subs = {lam: Dd / (A * Cc)}
P3s = sp.simplify(P3.subs(subs))
print("P_3 =", sp.factor(P3s), " = (AC - Dy)/AC ?", sp.simplify(P3s - (A * Cc - Dd * y) / (A * Cc)) == 0)
P0s = sp.factor(P0.subs(subs))
print("P_0 =", P0s, " = D y (A+m)(C+m)(d-m)/(AC) ?",
      sp.simplify(P0s - Dd * y * (A + m) * (Cc + m) * (d - m) / (A * Cc)) == 0)

# decomposed forms
eps = (Cc - Dd) / Cc
am = 1 - y / A
bm = lambda mm: Bb + mm - y + (d - 1 - 2 * mm) * y / A
cm = lambda mm: (d - mm) * (1 + mm / A) * y
beta = lambda mm: A * (2 * mm + 1 - d) - d * (2 * mm + 1) + 3 * mm ** 2 + 3 * mm + 1
P2_dec = bm(m + 1) + (Dd + m) * am + eps * (y / A) * (A - d + 3 + 3 * m)
P1_dec = cm(m + 1) + (Dd + m) * bm(m) + eps * (y / A) * beta(m)
print("P_2 decomposition exact:", sp.simplify(P2.subs(subs) - P2_dec) == 0)
print("P_1 decomposition exact:", sp.simplify(P1.subs(subs) - P1_dec) == 0)

print("\n=== R8.7: ratio-free Jacobi lemma (J), direct roots ===")
import random
random.seed(7)
def jacobi_roots(dv, Uv, Vv):
    # q_{U,V}(y) = 2F1(-d, U; V; y/U): exact polynomial coefficients
    from math import comb
    coeffs = []
    for k in range(dv + 1):
        c = sp.Rational((-1) ** k * comb(dv, k))
        for j in range(k):
            c *= sp.Rational(Uv + j, 1) / sp.Rational(Vv + j, 1)
        c /= sp.factorial(k) * Uv ** k / sp.factorial(k)  # careful: term is (-d)_k (U)_k/(V)_k k! (y/U)^k
        coeffs.append(c)
    # rebuild cleanly: coeff of y^k = (-d)_k (U)_k / ((V)_k k! U^k)
    # use scaled variable z = y/V for numerical stability
    coeffs = []
    for k in range(dv + 1):
        c = sp.Rational(1)
        for j in range(k):
            c *= sp.Rational(-(dv) + j) * sp.Rational(Uv + j)
        c /= sp.factorial(k)
        for j in range(k):
            c /= sp.Rational(Vv + j)
        c /= Uv ** k
        c *= Vv ** k  # scaled variable
        coeffs.append(c)
    poly = [mp.mpf(str(c)) for c in coeffs]  # ascending in z
    return [Vv * rt for rt in mp.polyroots(poly[::-1], maxsteps=800, error=False)]

cases = [(8, 264, 256), (8, 256 + 8, 256), (12, 384 + 12, 384), (6, 192 + 6, 192),
         (10, 10 ** 6, 320), (5, 160 + 5, 160), (16, 512 + 16, 512)]
for _ in range(6):
    dv = random.randint(4, 14)
    Vv = 32 * dv + random.randint(0, 50)
    Uv = Vv + dv + random.randint(0, 200)
    cases.append((dv, Uv, Vv))

def jacobi_matrix_roots(dv, Uv, Vv):
    # independent construction: standard monic Jacobi recurrence on t, y = U(1-t)/2
    al = Vv - 1.0
    be = Uv - Vv - dv
    diag, off = [], []
    for k in range(dv):
        s = 2 * k + al + be
        Bk = (be * be - al * al) / (s * (s + 2)) if s * (s + 2) != 0 else 0.0
        diag.append(mp.mpf(Bk))
        if k >= 1:
            Ck = 4 * k * (k + al) * (k + be) * (k + al + be) / (s * s * (s + 1) * (s - 1))
            off.append(mp.sqrt(mp.mpf(Ck)))
    M = mp.matrix(dv)
    for i in range(dv):
        M[i, i] = diag[i]
        if i < dv - 1:
            M[i, i + 1] = off[i]
            M[i + 1, i] = off[i]
    ev = mp.eigsy(M)
    evs = [ev[i] if not isinstance(ev, tuple) else ev[0][i] for i in range(dv)]
    return sorted(mp.mpf(Uv) * (1 - t) / 2 for t in evs)

allok = True
for dv, Uv, Vv in cases:
    try:
        roots = jacobi_roots(dv, Uv, Vv)
        rr = sorted([rt.real for rt in roots])
        real_ok = all(abs(rt.imag) < mp.mpf("1e-18") for rt in roots)
    except Exception:
        rr = None
        real_ok = None
    mr = jacobi_matrix_roots(dv, Uv, Vv)
    half = 8 * mp.sqrt(Vv * dv)
    lo, hi = Vv - half, Vv + half
    if rr is not None:
        # cross-check matrix vs polynomial roots
        xerr = max(abs(a - b) for a, b in zip(rr, mr)) / max(1, abs(mr[-1]))
        ok = real_ok and lo - 1e-6 <= rr[0] and rr[-1] <= hi + 1e-6
        src = f"polyroots min {mp.nstr(rr[0], 8)} max {mp.nstr(rr[-1], 8)} xcheck {mp.nstr(xerr, 3)}"
    else:
        ok = lo - 1e-9 <= mr[0] and mr[-1] <= hi + 1e-9
        src = f"matrix-roots min {mp.nstr(mr[0], 8)} max {mp.nstr(mr[-1], 8)} (polyroots n.c.)"
    okM = lo - 1e-9 <= mr[0] and mr[-1] <= hi + 1e-9
    allok &= bool(ok) and bool(okM)
    print(f" d={dv} U={Uv} V={Vv}: window [{mp.nstr(lo, 9)}, {mp.nstr(hi, 9)}]: {src}  ok={bool(ok and okM)}")
print("all root-inclusion checks:", bool(allok))

print("\n=== R8.8: transported diagonal identity ===")
U, V, d, k = sp.symbols("U V d k", positive=True)
H = U - d - 1
diag = U * (H * (V + 2 * k) + 2 * k * (k + 1)) / ((H + 2 * k) * (H + 2 * k + 2))
claim = (2 * k * (k + H + 1) * (U - 2 * V) + V * H * (d - 1)) / ((H + 2 * k) * (H + 2 * k + 2))
print("diagonal - V == claimed form:", sp.simplify(diag - V - claim) == 0)
