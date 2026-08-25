#!/usr/bin/env python3
"""Clean-room numerical checks of normalization and the sectorial contour.

Only Python's standard library is used.  All functions and inputs are built
from the displayed definitions; no packet JSON or frozen expected result is
read.  The numerical integrations are regression tests, not uniform proofs.
"""

from __future__ import annotations

import cmath
import math


PI = math.pi


def gamma_lanczos(z: complex) -> complex:
    coefficients = (
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.6150291621406,
        12.507343278686905,
        -0.13857109526572012,
        9.984369578019572e-6,
        1.5056327351493116e-7,
    )
    if z.real < 0.5:
        return PI / (cmath.sin(PI * z) * gamma_lanczos(1 - z))
    shifted = z - 1
    value = coefficients[0]
    for index, coefficient in enumerate(coefficients[1:], 1):
        value += coefficient / (shifted + index)
    t = shifted + 7.5
    return cmath.sqrt(2 * PI) * t ** (shifted + 0.5) * cmath.exp(-t) * value


def zeta_hasse(s: complex, terms: int = 90) -> complex:
    """Hasse/Euler transform of eta, valid at the center points used here."""

    eta = 0j
    for n in range(terms):
        inner = 0j
        for k in range(n + 1):
            inner += (-1 if k & 1 else 1) * math.comb(n, k) * (k + 1) ** (-s)
        eta += inner / (2 ** (n + 1))
    return eta / (1 - 2 ** (1 - s))


def xi(s: complex) -> complex:
    return 0.5 * s * (s - 1) * PI ** (-s / 2) * gamma_lanczos(s / 2) * zeta_hasse(s)


def simpson(function, left: float, right: float, panels: int) -> complex:
    if panels % 2:
        panels += 1
    step = (right - left) / panels
    total = function(left) + function(right)
    total += 4 * sum(function(left + step * j) for j in range(1, panels, 2))
    total += 2 * sum(function(left + step * j) for j in range(2, panels, 2))
    return total * step / 3


def omega_weight(u: float, theta_terms: int = 8) -> float:
    t = math.exp(2 * u)
    total = 0.0
    for k in range(1, theta_terms + 1):
        total += (
            PI**2 * k**4 * t**2 - 1.5 * PI * k**2 * t
        ) * math.exp(-PI * k**2 * t)
    return math.exp(u / 2) * total


def xi_kernel(w: complex) -> complex:
    return 8 * simpson(
        lambda u: omega_weight(u) * cmath.cosh(w * u),
        0.0,
        4.0,
        40_000,
    )


def saddle(s: complex) -> complex:
    value = cmath.log(s) - cmath.log(cmath.log(s)) - math.log(PI)
    for _ in range(30):
        exponential = cmath.exp(value)
        residual = value * (PI * exponential + 0.75) - s
        derivative = PI * exponential * (value + 1) + 0.75
        step = residual / derivative
        value -= step
        if abs(step) < 1e-14 * max(1.0, abs(value)):
            break
    return value


def moment_ratio(s: complex, modes: int, first_mode: int = 1) -> complex:
    ell = saddle(s)
    curvature = s * (1 / ell + 1 / ell**2) - 0.75
    h_saddle = s * cmath.log(ell) + ell / 4 - PI * cmath.exp(ell)
    log_main = h_saddle + 0.5 * cmath.log(2 * PI / curvature)

    def normalized_integrand(u: float) -> complex:
        if u == 0:
            return 0j
        theta = sum(
            math.exp(-PI * k * k * math.exp(u))
            for k in range(first_mode, modes + 1)
        )
        return cmath.exp(s * math.log(u) + u / 4 - log_main) * theta

    # The first saddle lies well inside this interval for the test inputs.
    return simpson(normalized_integrand, 0.0, 10.0, 120_000)


def rouche_envelope(ell: float, theta: float) -> float:
    m_theta = ell + 2 + math.log(ell + 1) + theta / ell + math.log(PI)
    return (
        2 * (math.log(ell + 1) + theta / ell + math.log(PI) + 1) / ell
        + 3 * m_theta / (2 * math.exp(ell))
    )


def main() -> None:
    print("factor-eight kernel versus direct completed zeta")
    for w in (0j, 0.2 + 0j, 0.15j):
        direct = xi(0.5 + w)
        integral = xi_kernel(w)
        relative = abs(integral - direct) / abs(direct)
        print(
            f"w={w!s:>8}: xi={direct:.12g}, kernel={integral:.12g}, "
            f"relative difference={relative:.3e}"
        )

    print("\nRouche whole-boundary analytic envelope")
    for ell in (12.0, 16.0, 24.0):
        print(f"ell={ell:4.0f}: envelope={rouche_envelope(ell, 0.01):.12f}")

    print("\nleading and full-theta Mellin ratios to the constructed saddle main term")
    for s in (80 + 0j, 120 * cmath.exp(0.002j)):
        leading = moment_ratio(s, 1)
        full = moment_ratio(s, 5)
        second = moment_ratio(s, 2, first_mode=2)
        print(
            f"s={s:.8g}: I1/A={leading:.12g}, F_5/A={full:.12g}, "
            f"I2/A={second:.3e}, summed-difference={abs(full-leading):.3e}"
        )

    print("\nelementary two-step prefactor correction")
    for n_value in (40, 100, 400, 1600):
        log_r = (
            2
            + math.log1p(1 / n_value)
            - (n_value + 1.5) * math.log1p(2 / n_value)
        )
        print(f"N={n_value:4d}: N^2 log(R_N)={n_value*n_value*log_r:.12f}")


if __name__ == "__main__":
    main()
