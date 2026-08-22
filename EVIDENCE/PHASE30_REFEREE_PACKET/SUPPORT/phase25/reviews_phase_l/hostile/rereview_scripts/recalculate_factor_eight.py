#!/usr/bin/env python3
"""Numerically reconstruct the factor-eight xi/Mellin normalization.

The theta kernel, xi function, derivatives, and integrals are constructed from
their definitions.  No frozen expected-result file is read.
"""

import math

import mpmath as mp


def xi(s: mp.mpf) -> mp.mpf:
    return mp.mpf(1) / 2 * s * (s - 1) * mp.power(mp.pi, -s / 2) * mp.gamma(s / 2) * mp.zeta(s)


def omega(t: mp.mpf) -> mp.mpf:
    # Here t=exp(2u)>=1.  Twelve modes leave a tail far below the working
    # precision (already exp(-pi*13^2) at u=0).
    theta_prime = mp.fsum(
        -mp.pi * m**2 * mp.exp(-mp.pi * m**2 * t) for m in range(1, 13)
    )
    theta_second = mp.fsum(
        mp.pi**2 * m**4 * mp.exp(-mp.pi * m**2 * t) for m in range(1, 13)
    )
    return (2 * t**2 * theta_second + 3 * t * theta_prime) / 2


def moment(n: int) -> mp.mpf:
    integrand = lambda u: omega(mp.exp(2 * u)) * mp.exp(u / 2) * u ** (2 * n)
    # Beyond u=4 the kernel is doubly exponentially small.
    return mp.quad(integrand, [0, mp.mpf("0.5"), 1, 2, 3, 4])


def coefficient_from_xi(n: int) -> mp.mpf:
    derivative = mp.diff(lambda w: xi(mp.mpf(1) / 2 + w), 0, 2 * n)
    return mp.factorial(n) * derivative / mp.factorial(2 * n)


def main() -> None:
    mp.mp.dps = 55
    for n in range(3):
        direct = coefficient_from_xi(n)
        mellin = 8 * mp.factorial(n) * moment(n) / mp.factorial(2 * n)
        relative = abs(direct - mellin) / abs(direct)
        assert relative < mp.mpf("1e-35"), (n, direct, mellin, relative)

        duplicated = 8 * mp.sqrt(mp.pi) / (4**n * mp.gamma(n + mp.mpf(1) / 2))
        elementary = 8 * mp.factorial(n) / math.factorial(2 * n)
        assert mp.almosteq(duplicated, elementary)

    print("PASS factor-eight coefficient identity for n=0,1,2")


if __name__ == "__main__":
    main()
