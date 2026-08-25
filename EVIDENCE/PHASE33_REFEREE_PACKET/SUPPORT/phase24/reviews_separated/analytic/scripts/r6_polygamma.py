#!/usr/bin/env python3
"""R6 v3 (Gate A8): paired polygamma scale, with the proof's own hypothesis
d + 2 rho <= n/1000 (eta = 1/1000) enforced, K_r := 1 for the scale test.
rho = sqrt(B d); z sampled on the rim of Omega = dist(z, [0,d]) <= 2 rho."""
import mpmath as mp

mp.mp.dps = 50

def L_saddle(N):
    w = mp.log(N)
    L = w - mp.log(w) - mp.log(mp.pi)
    for _ in range(80):
        L = L - (L * (mp.pi * mp.e ** L + mp.mpf("0.75")) - N) / (mp.pi * mp.e ** L * (1 + L) + mp.mpf("0.75"))
    return L

print(" n        d    rho/(n/2000) | pairBC*scale | pairDb*scale | Aterm*scale | minSegRe/n")
for n in [10 ** 8, 10 ** 9, 10 ** 10]:
    n = mp.mpf(n)
    x = 1 / n
    L = L_saddle(2 * n - 2)
    e = 1 / L
    al, t, w, de = mp.mpf(3), mp.mpf(2), mp.mpf(16) / 3, mp.mpf(1) / 3
    A = al / (x * e); B = (t + w * e) / x; C = t / x; D = (1 + de * e) / x
    b = n + mp.mpf("0.5")
    # largest d with d + 2 sqrt(B d) <= n/1000
    lo, hi = 1, int(n)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid + 2 * mp.sqrt(B * mid) <= n / 1000:
            lo = mid
        else:
            hi = mid - 1
    d = mp.mpf(lo)
    rho = mp.sqrt(B * d)
    target = 1 / (n ** 5 * L)
    worst = [mp.mpf(0)] * 3
    minre = mp.mpf(10)
    for j in range(40):
        th = 2 * mp.pi * j / 40
        # rim point of stadium Omega: circle around endpoint d and around 0
        z1 = d + 2 * rho * mp.e ** (1j * th)
        z2 = 2 * rho * mp.e ** (1j * th + 1j * mp.pi / 40)
        for z in (z1, z2):
            pBC = abs(mp.polygamma(5, B + z) - mp.polygamma(5, C + z)) / target
            pDb = abs(mp.polygamma(5, D + z) - mp.polygamma(5, b + z)) / target
            pA = abs(mp.polygamma(5, A + z)) / target
            worst[0] = max(worst[0], pBC); worst[1] = max(worst[1], pDb); worst[2] = max(worst[2], pA)
            for lam in [0, mp.mpf("0.31"), mp.mpf("0.77"), 1]:
                minre = min(minre, (C + z + lam * (B - C)).real / n, (b + z + lam * (D - b)).real / n)
    print(f" {mp.nstr(n, 3):>8} {int(d):>6} {mp.nstr(rho / (n / 2000), 4):>8} | {mp.nstr(worst[0], 5):>10} | {mp.nstr(worst[1], 5):>10} | {mp.nstr(worst[2], 6):>10} | {mp.nstr(minre, 5)}")

print("\nUnpaired comparison at n=1e9: |psi^5(B)| / (1/n^5) =",
      mp.nstr(abs(mp.polygamma(5, 2 * mp.mpf(10) ** 9)) * mp.mpf(10) ** 45, 5),
      " (no log gain: would be O(1), vs paired O(1/L))")
