#!/usr/bin/env python3
"""Independent recalculation R3 (Gate A2): one complex contour point off the real axis.

From definitions:
  I_1(s) = int_1^inf (log t)^s t^{-3/4} e^{-pi t} dt = int_0^inf u^s e^{u/4 - pi e^u} du
  saddle L: s = L (pi e^L + 3/4);  K = s (1/L + 1/L^2) - 3/4
  main term A(s) = sqrt(2 pi / K) L^s exp(L/4 - s/L + 3/4)
Claims tested at s off the real axis (|arg s| = 1/100):
  (i)   |Im L| < 1/20, |arg K| < 1/20, Re K >= cos(1/20) |K|
  (ii)  I_1(s) = A(s) (1 + small) with smallness consistent with O(log|s|/|s|)
  (iii) endpoint connector negligible relative to A(s)
  (iv)  the exact shifted-ray identity: I_1 = E_s + int_{1+ib}^{inf+ib}
Also exact symbolic check of the signed cubic Gaussian moment ratio
  int r^3 e^{r - K r^2/2} / int e^{r - K r^2/2} = 3/K^2 + 1/K^3  (at a=1).
"""
import mpmath as mp

mp.mp.dps = 60
pi = mp.pi

def saddle(N):
    w = mp.log(N)
    L = w - mp.log(w) - mp.log(pi)
    for _ in range(100):
        L = L - (L * (pi * mp.e ** L + mp.mpf("0.75")) - N) / (pi * mp.e ** L * (1 + L) + mp.mpf("0.75"))
    return L

def I1_direct(s):
    # real-ray definition, u = log t variable; split finely for the oscillation
    f = lambda u: mp.e ** (s * mp.log(u) + u / 4 - pi * mp.e ** u)
    pts = [mp.mpf("1e-40")] + [mp.mpf(i) / 4 for i in range(1, 49)] + [mp.mpf(20)]
    return mp.quad(f, pts)

for mag, tag in [(mp.mpf(10) ** 4, "1e4"), (mp.mpf(10) ** 5, "1e5")]:
    s = mag * mp.e ** (1j / 100)
    L = saddle(s)
    K = s * (1 / L + 1 / L ** 2) - mp.mpf("0.75")
    A = mp.sqrt(2 * pi / K) * mp.e ** (s * mp.log(L)) * mp.e ** (L / 4 - s / L + mp.mpf("0.75"))
    print(f"=== s = {tag} e^(i/100) ===")
    print(f" L = {mp.nstr(L, 20)}")
    print(f" |Im L| = {mp.nstr(abs(mp.im(L)), 8)}  (< 1/20 = 0.05 ?)")
    print(f" K = {mp.nstr(K, 15)}")
    print(f" |arg K| = {mp.nstr(abs(mp.arg(K)), 8)}  (< 1/20 ?)   Re K - cos(1/20)|K| = {mp.nstr((K.real - mp.cos(mp.mpf('0.05')) * abs(K)), 5)}")
    I = I1_direct(s)
    rel = I / A - 1
    print(f" I_1(s) = {mp.nstr(I, 25)}")
    print(f" A(s)   = {mp.nstr(A, 25)}")
    print(f" relative error = {mp.nstr(rel, 6)}   |rel| = {mp.nstr(abs(rel), 4)}")
    print(f" comparison scale log|s|/|s| = {mp.nstr(mp.log(abs(s)) / abs(s), 4)}")
    # connector estimate: E_s = int_0^1 g dx + i int_0^b g(1+iy) dy
    b = mp.im(L)
    g = lambda u: mp.e ** (s * mp.log(u) + u / 4 - pi * mp.e ** u)
    E1 = mp.quad(g, [mp.mpf("1e-40"), mp.mpf("0.5"), 1])
    E2 = 1j * mp.quad(lambda y: mp.e ** (s * mp.log(1 + 1j * y) + (1 + 1j * y) / 4 - pi * mp.e ** (1 + 1j * y)),
                      [0, b])
    E = E1 + E2
    print(f" |E_s| / |A(s)| = {mp.nstr(abs(E) / abs(A), 4)}  (connector relative size)")
    # exact contour identity check: direct real-ray value vs connector + shifted ray
    shifted = mp.quad(lambda x: mp.e ** (s * mp.log(x + 1j * b) + (x + 1j * b) / 4 - pi * mp.e ** (x + 1j * b)),
                      [1, mp.mpf(2), mp.mpf(4), mp.mpf(7), mp.mpf(12), mp.mpf(20)])
    id_err = abs((E + shifted) - I) / abs(I)
    print(f" contour identity |E_s + shifted - I_1|/|I_1| = {mp.nstr(id_err, 4)}")
    print()

print("=== R3e: signed cubic Gaussian moment identity (symbolic) ===")
import sympy as sp
r, K, a = sp.symbols("r K a", positive=True)
# I(a) = sqrt(2 pi / K) exp(a^2/(2K)); ratio I'''(a)/I(a) at a=1
Ia = sp.sqrt(2 * sp.pi / K) * sp.exp(a ** 2 / (2 * K))
ratio = sp.simplify(sp.diff(Ia, a, 3) / Ia).subs(a, 1)
print("I'''(1)/I(1) =", sp.factor(ratio), " =?= 3/K^2 + 1/K^3:",
      sp.simplify(ratio - (3 / K ** 2 + 1 / K ** 3)) == 0)
# and the modulus identity e^{1/(2K)} absorption: |e^{1/(2K)} - 1| <= C/|K| for Re K>0
# numeric spot check at K = 80 e^{i/100}
Knum = 80 * mp.e ** (1j / 100)
print("|e^{1/(2K)}-1| at |K|=80:", mp.nstr(abs(mp.e ** (1 / (2 * Knum)) - 1), 5), "vs 1/|K| =", mp.nstr(1 / abs(Knum), 5))
