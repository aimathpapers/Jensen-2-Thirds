#!/usr/bin/env python3
"""Independent recalculation R2 (Gate A1): Lemma S Rouche margin and branch.

Definitions from scratch:
  Psi(L) = L (pi e^L + 3/4);  saddle: N = Psi(L_N)
  w = Log N (principal), L_0 = w - Log w - Log pi
  m(l) = l - log(l+1) - log pi - 1
  M_th(l) = l + 2 + log(l+1) + th/l + log pi
  eta(l) = (log(l+1) + th/l + log pi + 1)/l
  Rouche claim: sup_{|L-L0|=1} |G-H| <= 2 eta(l) + 3 M(l)/(2 e^l) < 1 for l >= 12.

Checks:
 (a) exact rational/high-precision values of the margin at l=12, theta=pi/2 (supremum);
 (b) m(l) >= l/2 for l >= 12 (monotone argument spot-verified);
 (c) |r| <= 1/m(12) < 7/50, |sigma| <= M(12)/e^12 < 7/50, |3L/(4N)| bound < 1e-4;
 (d) 151/200 > 9/16 arithmetic and the reduced denominator 151/50;
 (e) FUNCTIONAL check: Newton-solve Psi(L)=N for random sector points,
     verify |L-L0|<1, L' = L/Q against complex-step difference, |1+r-3 sigma/4| >= 9/16;
 (f) DIRECT Rouche sampling (diagnostic only): max |G-H| on the disc boundary
     at a hard point (l=12, theta=1.57) vs |H|=1.
"""
import mpmath as mp

mp.mp.dps = 50
pi = mp.pi

def m_fn(l):
    return l - mp.log(l + 1) - mp.log(pi) - 1

def M_fn(l, th):
    return l + 2 + mp.log(l + 1) + th / l + mp.log(pi)

def eta_fn(l, th):
    return (mp.log(l + 1) + th / l + mp.log(pi) + 1) / l

print("=== R2a: Rouche margin at l=12, theta=pi/2 (worst case) ===")
l = mp.mpf(12); th = pi / 2
m12 = m_fn(l); M12 = M_fn(l, th); eta12 = eta_fn(l, th)
bound = 2 * eta12 + 3 * M12 / (2 * mp.e ** l)
print(f"m(12)   = {mp.nstr(m12, 20)}   (claim > 7.29, and > l/2 = 6)")
print(f"M(12)   = {mp.nstr(M12, 20)}   (note claims <= 17.841)")
print(f"eta(12) = {mp.nstr(eta12, 20)}  (note claims <= 0.4034)")
print(f"2 eta + 3M/(2 e^l) = {mp.nstr(bound, 20)}  (must be < 1; note claims 0.8068+0.0002)")
print(f"margin to 1: {mp.nstr(1 - bound, 5)}")

print("\n=== R2b: m(l) >= l/2 for l in [12, 10^4] (scan, plus monotonicity of l/2 - log(l+1)) ===")
ok = all(m_fn(mp.mpf(v)) >= mp.mpf(v) / 2 for v in [12, 12.5, 13, 15, 20, 50, 100, 1000, 10000])
print("scan ok:", ok, "; m(12)-6 =", mp.nstr(m12 - 6, 5))

print("\n=== R2c: r, sigma bounds ===")
r_bound = 1 / m12
sig_bound = M12 / mp.e ** l
print(f"|r| <= 1/m(12) = {mp.nstr(r_bound, 10)}  < 7/50 = 0.14 ? {r_bound < mp.mpf('0.14')}")
print(f"|sigma| <= M/e^l = {mp.nstr(sig_bound, 10)} < 7/50 ? {sig_bound < mp.mpf('0.14')}")
print(f"3M/(4 e^l) = {mp.nstr(3 * M12 / (4 * mp.e ** l), 10)}  < 1e-4 ? {3 * M12 / (4 * mp.e ** l) < mp.mpf('1e-4')}")
print(f"151/200 = {mp.mpf(151)/200} > 9/16 = {mp.mpf(9)/16} ? {mp.mpf(151)/200 > mp.mpf(9)/16}")
print(f"4 - 4*(7/50) - 3*(7/50) = {mp.mpf(4) - 7 * mp.mpf(7)/50} =?= 151/50 = {mp.mpf(151)/50}")

print("\n=== R2e: functional saddle branch check (Newton from L0) ===")
import random
random.seed(12345)

def Psi(L):
    return L * (pi * mp.e ** L + mp.mpf("0.75"))

def saddle(N):
    w = mp.log(N)
    L = w - mp.log(w) - mp.log(pi)
    for _ in range(80):
        L = L - (Psi(L) - N) / (pi * mp.e ** L * (1 + L) + mp.mpf("0.75"))
    return L

worst_gap = mp.mpf(0)
worst_q = mp.mpf(10)
worst_der = mp.mpf(0)
for trial in range(60):
    lmag = random.uniform(12, 60)
    arg = random.uniform(-1.55, 1.55)
    N = mp.e ** lmag * mp.e ** (1j * arg)
    w = mp.log(N)
    L0 = w - mp.log(w) - mp.log(pi)
    L = saddle(N)
    assert abs(Psi(L) - N) < mp.mpf(10) ** (-40) * abs(N)
    gap = abs(L - L0)
    r = 1 / L; sig = L / N
    Q = (1 + L) * N - mp.mpf("0.75") * L ** 2
    qfac = abs(1 + r - mp.mpf("0.75") * sig)
    # derivative check: dL/dN via complex step on log N
    h = mp.mpf(10) ** (-25)
    N2 = N * mp.e ** h
    L2 = saddle(N2)
    der_num = (L2 - L) / (N2 - N)
    der_exact = L / Q
    worst_der = max(worst_der, abs(der_num - der_exact) / abs(der_exact))
    worst_gap = max(worst_gap, gap)
    worst_q = min(worst_q, qfac)
    if trial < 3:
        print(f" N=e^{mp.nstr(lmag,4)} e^{{i {mp.nstr(arg,4)}}}: |L-L0|={mp.nstr(gap,4)} |r|={mp.nstr(abs(r),4)} |sig|={mp.nstr(abs(sig),4)} |1+r-3sig/4|={mp.nstr(qfac,6)}")
print(f"max |L-L0| over 60 sector points: {mp.nstr(worst_gap, 5)} (< 1 required)")
print(f"min |1+r-3 sigma/4|: {mp.nstr(worst_q, 5)} (>= 9/16 = {mp.nstr(mp.mpf(9)/16, 5)} required)")
print(f"max rel err of L' vs L/Q (complex step): {mp.nstr(worst_der, 3)}")

print("\n=== R2f: direct Rouche boundary sample at the hardest point (diagnostic) ===")
# l = 12, arg N = theta: scan theta in (0, pi/2); |G-H| on |L-L0|=1 sampled densely
def GminusH(N, L):
    w = mp.log(N)
    # G - H = log L - log w - log(1 - 3L/(4N))   [principal logs]
    return mp.log(L) - mp.log(w) - mp.log(1 - 3 * L / (4 * N))

global_max = mp.mpf(0)
for arg in [mp.mpf("0.01"), mp.mpf("0.5"), mp.mpf("1.0"), mp.mpf("1.4"), pi / 2 - mp.mpf("1e-6")]:
    N = mp.e ** 12 * mp.e ** (1j * arg)
    w = mp.log(N)
    L0 = w - mp.log(w) - mp.log(pi)
    mx = max(abs(GminusH(N, L0 + mp.e ** (1j * phi))) for phi in mp.linspace(0, 2 * pi, 400))
    global_max = max(global_max, mx)
    print(f" arg N = {mp.nstr(arg, 6)}: sampled max |G-H| on |L-L0|=1: {mp.nstr(mx, 8)}")
print(f"sampled global max {mp.nstr(global_max, 8)} vs proved upper bound {mp.nstr(bound, 8)} vs |H|=1")
