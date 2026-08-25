#!/usr/bin/env python3
"""Independent recalculation R1 (Gate A0): factor-eight Mellin identity.

Reconstructed from definitions ONLY:
  xi(s) = (1/2) s (s-1) pi^{-s/2} Gamma(s/2) zeta(s)
  xi(1/2 + w) = sum_n gamma(n) w^{2n} / n!
  Theta(t) = sum_{m>=1} exp(-pi m^2 t)
  omega(t) = (1/2)(2 t^2 Theta''(t) + 3 t Theta'(t))
  claim: gamma(n) = 8 n!/(2n)! int_0^inf omega(e^{2u}) e^{u/2} u^{2n} du

Path A (independent of the packet): Cauchy transform of xi around w=0.
Path B: direct numerical integration of the claimed moment formula.
Path C: the assembly identity gamma_H(n) = Gamma(n+1)/Gamma(2n+1) 2^{-2n-2}
        (32 binom(2n,2) F(2n-2) - F(2n)), F(s) = int_1^inf (log t)^s t^{-3/4} Theta(t) dt.
Also: pointwise identity xi(1/2+w) = 8 int_0^inf omega(e^{2u}) e^{u/2} cosh(w u) du
at a complex w, and the duplication-form prefactor equivalence.
"""
import mpmath as mp

mp.mp.dps = 60

def xi(s):
    return mp.mpf("0.5") * s * (s - 1) * mp.pi ** (-s / 2) * mp.gamma(s / 2) * mp.zeta(s)

def gamma_via_cauchy(n, rho=mp.mpf("0.5")):
    # gamma(n) = n!/(2n)! * xi^{(2n)}(1/2);
    # xi^{(2n)}(1/2) = (2n)!/rho^{2n} * (1/2pi) int_0^{2pi} xi(1/2+rho e^{i th}) e^{-2ni th} dth
    # use even symmetry: integrate 0..pi, real part, double
    m = 2 * n
    f = lambda th: xi(mp.mpf("0.5") + rho * mp.e ** (1j * th)) * mp.e ** (-m * 1j * th)
    integ = mp.quad(f, [0, mp.pi])
    val = (integ.real * 2) / (2 * mp.pi) / rho ** m
    return mp.factorial(n) * val

def theta(t):
    s = mp.mpf(0)
    k = 1
    while True:
        term = mp.e ** (-mp.pi * k * k * t)
        s += term
        if term < mp.mpf(10) ** (-55):
            break
        k += 1
    return s

def omega(t):
    # omega(t) = (1/2)(2 t^2 Theta'' + 3 t Theta') summed termwise (exact series)
    s = mp.mpf(0)
    k = 1
    while True:
        a = mp.pi * k * k
        e = mp.e ** (-a * t)
        # term of Theta: e^{-a t}; Theta' term: -a e^{-a t}; Theta'': a^2 e^{-a t}
        w = mp.mpf("0.5") * (2 * t * t * a * a - 3 * t * a) * e
        s += w
        if abs(w) < mp.mpf(10) ** (-55):
            break
        k += 1
    return s

def gamma_via_moment(n):
    f = lambda u: omega(mp.e ** (2 * u)) * mp.e ** (u / 2) * u ** (2 * n)
    integ = mp.quad(f, [0, 1, 3, 8, 20])
    return 8 * mp.factorial(n) / mp.factorial(2 * n) * integ

def F(s):
    f = lambda t: (mp.log(t)) ** s * t ** (-mp.mpf("0.75")) * theta(t)
    return mp.quad(f, [1, mp.e, mp.e ** 3, mp.inf])

def gamma_via_assembly(n):
    return (mp.gamma(n + 1) / mp.gamma(2 * n + 1) * 2 ** (-2 * n - 2)
            * (32 * mp.binomial(2 * n, 2) * F(2 * n - 2) - F(2 * n)))

print("=== R1: gamma(n) three independent ways (n=0..4) ===")
for n in range(5):
    gA = gamma_via_cauchy(n)
    gB = gamma_via_moment(n)
    gC = gamma_via_assembly(n) if n >= 1 else None
    rel = abs((gA - gB) / gA)
    line = f"n={n}: cauchy={mp.nstr(gA, 25)}  moment={mp.nstr(gB, 25)}  rel|A-B|={mp.nstr(rel, 3)}"
    if gC is not None:
        line += f"  assembly rel={mp.nstr(abs((gA - gC) / gA), 3)}"
    print(line)

print("\n=== R1b: pointwise identity at complex w ===")
for w in [mp.mpc("0.3", "0.2"), mp.mpc("1.1", "-0.4"), mp.mpc("0", "2.0")]:
    lhs = xi(mp.mpf("0.5") + w)
    rhs = 8 * mp.quad(lambda u: omega(mp.e ** (2 * u)) * mp.e ** (u / 2) * mp.cosh(w * u),
                      [0, 1, 3, 8, 20])
    print(f"w={mp.nstr(w, 8)}: xi={mp.nstr(lhs, 20)}  8*int omega e^{{u/2}} cosh={mp.nstr(rhs, 20)}  rel={mp.nstr(abs((lhs - rhs) / lhs), 3)}")

print("\n=== R1c: prefactor duplication form 8 n!/(2n)! =?= 8 sqrt(pi)/(4^n Gamma(n+1/2)) ===")
for n in [0, 1, 2, 7, 25]:
    a = 8 * mp.factorial(n) / mp.factorial(2 * n)
    b = 8 * mp.sqrt(mp.pi) / (4 ** n * mp.gamma(n + mp.mpf("0.5")))
    print(f"n={n}: rel diff = {mp.nstr(abs((a - b) / a), 3)}")
