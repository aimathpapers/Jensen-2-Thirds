#!/usr/bin/env python3
"""Independent recalculation R9 (Gate A3, end-to-end): Theorem 21B main term.

Direct from definitions:
  gamma_H(M) = 8 M!/(2M)! int_0^inf omega(e^{2u}) e^{u/2} u^{2M} du
vs the assembled main term (T1):
  G(M) = e^{M-2} M^{M+1/2} L_N^N / (2^{2M-2} N^{N+1/2})
         * sqrt(2 pi / K_N) * exp(L_N/4 - N/L_N + 3/4),   N = 2M-2,
with L_N from my own Newton solve of N = L(pi e^L + 3/4), K = Q/L^2.

Also: the two-step ratio A(N+2)/A(N) vs L_N^2 (assembly eq. 10), and the
F(N+2)/(16(N+2)(N+1)F(N)) subordination scale (assembly eq. 12), where
A(s) = sqrt(2 pi/K_s) L_s^s exp(L_s/4 - s/L_s + 3/4) and F via direct
quadrature of the full theta kernel.
"""
import mpmath as mp

mp.mp.dps = 50
pi = mp.pi

def saddle(N):
    w = mp.log(N)
    L = w - mp.log(w) - mp.log(pi)
    for _ in range(100):
        L = L - (L * (pi * mp.e ** L + mp.mpf("0.75")) - N) / (pi * mp.e ** L * (1 + L) + mp.mpf("0.75"))
    return L

def omega_terms(u):
    # omega(e^{2u}) e^{u/2}: sum over modes, termwise exact
    t = mp.e ** (2 * u)
    s = mp.mpf(0)
    k = 1
    while True:
        a = pi * k * k
        e = mp.e ** (-a * t)
        w = mp.mpf("0.5") * (2 * t * t * a * a - 3 * t * a) * e
        s += w
        if abs(w) < mp.mpf(10) ** (-45) * max(mp.mpf(1), abs(s)):
            break
        k += 1
    return s * mp.e ** (u / 2)

def gammaH_moment(M):
    f = lambda u: omega_terms(u) * u ** (2 * M)
    # locate peak roughly
    Lu = saddle(2 * M - 2)
    c = Lu.real
    pts = [mp.mpf("1e-6"), c / 2, c, 2 * c, 4 * c, 12 * c]
    return 8 * mp.factorial(M) / mp.factorial(2 * M) * mp.quad(f, pts)

def G_main(M):
    N = mp.mpf(2 * M - 2)
    L = saddle(N)
    Q = (1 + L) * N - mp.mpf("0.75") * L ** 2
    K = Q / L ** 2
    return (mp.e ** (M - 2) * mp.mpf(M) ** (M + mp.mpf("0.5")) * mp.e ** (N * mp.log(L))
            / (2 ** (2 * M - 2) * N ** (N + mp.mpf("0.5")))
            * mp.sqrt(2 * pi / K) * mp.e ** (L / 4 - N / L + mp.mpf("0.75")))

print("=== R9a: gamma_H(M) vs assembled main term G(M) ===")
for M in [120, 500]:
    g = gammaH_moment(M)
    G = G_main(M)
    rel = g / G - 1
    print(f" M={M}: gamma_H={mp.nstr(g, 12)}")
    print(f"        G      ={mp.nstr(G, 12)}")
    print(f"        rel diff = {mp.nstr(rel, 5)}   scale log M / M = {mp.nstr(mp.log(M) / M, 5)}")

print("\n=== R9b: two-step ratio A(N+2)/A(N) vs L_N^2 ===")
def Aterm(s):
    L = saddle(s)
    K = s * (1 / L + 1 / L ** 2) - mp.mpf("0.75")
    return mp.sqrt(2 * pi / K) * mp.e ** (s * mp.log(L)) * mp.e ** (L / 4 - s / L + mp.mpf("0.75"))

for N in [mp.mpf(10) ** 4, mp.mpf(10) ** 6, mp.mpf(10) ** 4 * mp.e ** (1j / 100)]:
    L = saddle(N)
    rat = Aterm(N + 2) / Aterm(N)
    dev = rat / L ** 2 - 1
    print(f" N={mp.nstr(N, 10)}: |A(N+2)/A(N) / L_N^2 - 1| = {mp.nstr(abs(dev), 4)}  (claim O(1/N))")

print("\n=== R9c: F(N+2)/(16(N+2)(N+1)F(N)) scale (full theta kernel, real N) ===")
def F_direct(s):
    # F(s) = int_1^inf (log t)^s t^{-3/4} theta_0(t) dt, u = log t
    def theta0(t):
        total = mp.mpf(0)
        k = 1
        while True:
            term = mp.e ** (-pi * k * k * t)
            total += term
            if term < mp.mpf(10) ** (-45):
                break
            k += 1
        return total
    f = lambda u: mp.e ** (s * mp.log(u)) * mp.e ** (-3 * u / 4) * theta0(mp.e ** u) * mp.e ** u
    L = saddle(s)
    c = L.real
    return mp.quad(f, [mp.mpf("1e-6"), c / 2, c, 2 * c, 4 * c, 12 * c])

for N in [mp.mpf(400)]:
    FN = F_direct(N)
    FN2 = F_direct(N + 2)
    L = saddle(N)
    ratio = FN2 / (16 * (N + 2) * (N + 1) * FN)
    print(f" N={N}: F(N+2)/(16(N+2)(N+1)F(N)) = {mp.nstr(ratio, 8)}")
    print(f"   predicted scale L_N^2/N^2 = {mp.nstr(L ** 2 / N ** 2, 8)};  ratio of the two = {mp.nstr(ratio / (L ** 2 / N ** 2), 6)}")
    print(f"   vs claimed O((log N)^2/N^2) = {mp.nstr(mp.log(N) ** 2 / N ** 2, 8)}")
