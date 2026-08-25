#!/usr/bin/env python3
"""Independent recalculation R4 (Gates A4/A5): implicit saddle derivative tower.

G_0(N) = (N+1) log L + L/4 - N/L - (1/2) log Q,   Q = (1+L)N - 3 L^2/4,
with L = L_N defined by N = L (pi e^L + 3/4).

PATH A (my own symbolic run): total derivative D = d/dN + (L/Q) d/dL,
  normalized T_k = N^{k-1} L D^k G_0, two-scale form via L=1/r, N=1/(r sigma),
  limits sigma->0 then r->0.  Compare with claimed (-1)^k (k-2)! and with the
  phase-9/11 displayed polynomials in r.
  Chain rule N=2x-2: h^{(k)} leading constant 2 (-1)^k (k-2)!.

PATH B (fully independent numeric): power-series implicit solve.
  Given N(t) = N0 + t, solve Psi(L(t)) = N(t) as a formal series in t to
  order 8 by my own series-Newton; then G_0(N(t), L(t)) series;
  kth derivative = k! [t^k].  Compare against Path A limits numerically.

PATH C (A5): exact H_6(r, sigma) structure: reduced denominator (4+4r-3s)^12,
  numerator term count and total degree, exact coefficientwise majorant on
  |r|,|sigma| <= 7/50 with denominator margin 151/50; compare with the
  disclosed exact fraction and 10^4 cap; final 20000/(|N|^5 log|N|) bound.
"""
import sympy as sp

N, L = sp.symbols("N L")
r, s = sp.symbols("r s")  # r = 1/L, s = sigma = L/N

Q = (1 + L) * N - sp.Rational(3, 4) * L ** 2
G0 = (N + 1) * sp.log(L) + L / 4 - N / L - sp.log(Q) / 2

def D(expr):
    return sp.cancel(sp.diff(expr, N) + L / Q * sp.diff(expr, L))

print("=== R4A: symbolic tower, my own run ===")
cur = G0
tower = {}
for k in range(1, 7):
    cur = D(cur)
    tower[k] = cur

print(f"G_0'(N) spot form: {sp.factor(tower[1])}")

for k in range(2, 7):
    norm = sp.cancel(tower[k] * N ** (k - 1) * L)
    two = sp.cancel(norm.subs({L: 1 / r, N: 1 / (r * s)}))
    lim_s = sp.factor(sp.limit(two, s, 0))
    const = sp.limit(lim_s, r, 0)
    import math
    expect = (-1) ** k * math.factorial(k - 2)
    print(f" k={k}: sigma->0 rational in r = {sp.sstr(lim_s)[:120]}")
    print(f"      r->0 constant = {const}  expected (-1)^k (k-2)! = {expect}  match: {const == expect}")

# chain rule: h(x) = G_0(2x-2): h^{(k)} = 2^k G^{(k)}(2x-2) ~ 2^k c/( (2x)^{k-1} L ) = 2 c / (x^{k-1} L)
import math
print(" chain-rule h constants k=2..6:", [2 * (-1) ** k * math.factorial(k - 2) for k in range(2, 7)],
      " expected [2, -2, 4, -12, 48]")

print("\n=== R4B: independent power-series numeric check ===")
import mpmath as mp
mp.mp.dps = 60
pim = mp.pi

def series_saddle(N0, order=8):
    # L(t) = sum c_j t^j solving Psi(L(t)) = N0 + t, by Newton on series
    # start: c0 = real solution
    f = lambda Lv: Lv * (pim * mp.e ** Lv + mp.mpf("0.75")) - N0
    L0v = mp.findroot(f, mp.log(N0) - mp.log(mp.log(N0)) - mp.log(pim))
    c = [L0v] + [mp.mpf(0)] * order
    # Newton on the series: residual R(t) = Psi(L(t)) - (N0+t); iterate
    for _ in range(60):
        # compute Psi(L(t)) series via series exp
        # exp series of L: use mpmath taylor? do manual: E(t) = e^{L(t)} = e^{c0} * e^{L-c0}
        d = [c[j] for j in range(len(c))]; d[0] = mp.mpf(0)
        # e^{d(t)} by series exponential
        E = [mp.mpf(1)] + [mp.mpf(0)] * order
        for nn in range(1, order + 1):
            E[nn] = sum(j * d[j] * E[nn - j] for j in range(1, nn + 1)) / nn
        E = [mp.e ** L0v * e for e in E]
        # Psi = L*(pi E + 3/4)
        P = [mp.mpf(0)] * (order + 1)
        for j in range(order + 1):
            P[j] = pim * sum(c[i] * E[j - i] for i in range(j + 1)) + mp.mpf("0.75") * c[j]
        R = [P[0] - N0] + [P[1] - 1] + [P[j] for j in range(2, order + 1)]
        if max(abs(x) for x in R) < mp.mpf(10) ** (-55):
            break
        # Newton correction: solve Psi'(L(t)) delta(t) = -R(t) as series
        # Psi'(L) = pi e^L (1+L) + 3/4 ; series product
        U = [pim * (E[j] + sum(c[i] * E[j - i] for i in range(j + 1))) + (mp.mpf("0.75") if j == 0 else 0)
             for j in range(order + 1)]
        # series division delta = -R / U
        delta = [mp.mpf(0)] * (order + 1)
        for nn in range(order + 1):
            delta[nn] = (-R[nn] - sum(U[j] * delta[nn - j] for j in range(1, nn + 1))) / U[0]
        c = [c[j] + delta[j] for j in range(order + 1)]
    return c

def series_log(a, order):
    # log of series a(t) with a0 > 0
    out = [mp.log(a[0])] + [mp.mpf(0)] * order
    for nn in range(1, order + 1):
        out[nn] = (a[nn] - sum(j * out[j] * a[nn - j] for j in range(1, nn)) / a[0] * 1) / 1
        # standard: a' = a * (log a)' -> n a_n = sum_{j=1}^{n} j (log a)_j a_{n-j}
        out[nn] = (nn * a[nn] - sum(j * out[j] * a[nn - j] for j in range(1, nn))) / (nn * a[0])
    return out

def series_div(a, b, order):
    out = [mp.mpf(0)] * (order + 1)
    for nn in range(order + 1):
        out[nn] = (a[nn] - sum(b[j] * out[nn - j] for j in range(1, nn + 1))) / b[0]
    return out

N0 = mp.e ** 9  # large real N
order = 8
cser = series_saddle(N0, order)
# build G_0(N(t), L(t)) series
Nt = [N0, mp.mpf(1)] + [mp.mpf(0)] * (order - 1)
logL = series_log(cser, order)
# Q(t) = (1+L)N - 3/4 L^2
L2 = [sum(cser[i] * cser[nn - i] for i in range(nn + 1)) for nn in range(order + 1)]
oneplusL = [cser[0] + 1] + cser[1:]
Qt = [sum(oneplusL[i] * Nt[nn - i] for i in range(nn + 1)) - mp.mpf("0.75") * L2[nn] for nn in range(order + 1)]
logQ = series_log(Qt, order)
NL = series_div(Nt, cser, order)  # N/L
# G0 = (N+1) logL + L/4 - N/L - (1/2) log Q
N1 = [Nt[0] + 1] + Nt[1:]
G = [sum(N1[i] * logL[nn - i] for i in range(nn + 1)) + cser[nn] / 4 - NL[nn] - logQ[nn] / 2
     for nn in range(order + 1)]
import math
print(f"N0 = e^9 = {mp.nstr(N0, 8)},  L = {mp.nstr(cser[0], 15)}")
for k in range(2, 7):
    deriv = math.factorial(k) * G[k]
    lead = (-1) ** k * math.factorial(k - 2) / (N0 ** (k - 1) * cser[0])
    print(f" k={k}: series deriv = {mp.nstr(deriv, 12)}   leading = {mp.nstr(lead, 12)}   ratio = {mp.nstr(deriv / lead, 8)}")

print("\n=== R4C: exact H_6 structure and majorant ===")
six = sp.cancel(tower[6] * N ** 5 * L)
two6 = sp.cancel(six.subs({L: 1 / r, N: 1 / (r * s)}))
num, den = sp.fraction(sp.together(two6))
num = sp.expand(num); den = sp.factor(den)
print(" reduced denominator:", den)
print(" denominator == (4+4r-3s)^12 ?", sp.expand(den - (4 + 4 * r - 3 * s) ** 12) == 0)
terms = sp.Poly(num, r, s).terms()
degs = {a + b for (a, b), _ in terms}
print(f" numerator term count = {len(terms)}  (claimed 82);  total degrees present: {sorted(degs)} (claimed max 13)")
# coefficientwise majorant at 7/50, denominator margin (151/50)^12, exact rationals
q = sp.Rational(7, 50)
maj = sum(abs(coef) * q ** (a + b) for (a, b), coef in terms)
den_margin = sp.Rational(151, 50) ** 12
val = maj / den_margin
print(" exact majorant value:", val)
print(" float:", sp.N(val, 12), " < 10^4 ?", val < 10 ** 4)
claimed = sp.Rational(6422139805764931584036533551104, 702576099728137594188684005)
print(" equals disclosed fraction?", sp.simplify(val - claimed) == 0)
# sigma->0 polynomial check against phase-11 display
lead6 = sp.factor(sp.limit(two6, s, 0))
expected6 = (24 * r ** 8 + 216 * r ** 7 + 864 * r ** 6 + 2016 * r ** 5 + 3024 * r ** 4
             + 2399 * r ** 3 + 1042 * r ** 2 + 242 * r + 24) / (1 + r) ** 9
print(" sigma=0 numerator matches phase-11 display:", sp.simplify(lead6 - expected6) == 0)
# fifth-order phase-9 display
two5 = sp.cancel(sp.cancel(tower[5] * N ** 4 * L).subs({L: 1 / r, N: 1 / (r * s)}))
lead5 = sp.factor(sp.limit(two5, s, 0))
expected5 = -(6 * r ** 6 + 42 * r ** 5 + 126 * r ** 4 + 210 * r ** 3 + 146 * r ** 2 + 47 * r + 6) / (1 + r) ** 7
print(" sigma=0 order-5 matches phase-9 display:", sp.simplify(lead5 - expected5) == 0)
# fourth-order display
two4 = sp.cancel(sp.cancel(tower[4] * N ** 3 * L).subs({L: 1 / r, N: 1 / (r * s)}))
lead4 = sp.factor(sp.limit(two4, s, 0))
expected4 = (2 * r ** 4 + 10 * r ** 3 + 20 * r ** 2 + 11 * r + 2) / (1 + r) ** 5
print(" sigma=0 order-4 matches phase-9 display:", sp.simplify(lead4 - expected4) == 0)
