#!/usr/bin/env python3
"""Independent hostile checks constructed from the printed definitions.

This script uses only the Python standard library.  It reads no manuscript,
JSON, certificate, or frozen expected value.
"""

from __future__ import annotations

import math
from fractions import Fraction as Q


def eta_euler(s: float, terms: int = 50) -> float:
    """Euler-transform the alternating Dirichlet eta series."""
    row = [(k + 1.0) ** (-s) for k in range(terms + 1)]
    total = 0.0
    denominator = 2.0
    for _ in range(terms):
        total += row[0] / denominator
        row = [row[k] - row[k + 1] for k in range(len(row) - 1)]
        denominator *= 2.0
    return total


def xi_half() -> float:
    s = 0.5
    zeta = eta_euler(s) / (1.0 - 2.0 ** (1.0 - s))
    return (
        0.5
        * s
        * (s - 1.0)
        * math.pi ** (-s / 2.0)
        * math.gamma(s / 2.0)
        * zeta
    )


def omega_weight(u: float) -> float:
    t = math.exp(2.0 * u)
    theta_first = 0.0
    theta_second = 0.0
    m = 1
    while True:
        decay = math.exp(-math.pi * m * m * t)
        theta_first -= math.pi * m * m * decay
        term = (math.pi * m * m) ** 2 * decay
        theta_second += term
        if abs(term) < 1e-18:
            break
        m += 1
    omega = (2.0 * t * t * theta_second + 3.0 * t * theta_first) / 2.0
    return omega * math.exp(u / 2.0)


def simpson_integral(upper: float = 8.0, panels: int = 20_000) -> float:
    assert panels % 2 == 0
    step = upper / panels
    total = omega_weight(0.0) + omega_weight(upper)
    for index in range(1, panels):
        total += (4.0 if index % 2 else 2.0) * omega_weight(index * step)
    return total * step / 3.0


def check_factor_eight_at_zero() -> None:
    direct = xi_half()
    moment = 8.0 * simpson_integral()
    relative = abs(moment / direct - 1.0)
    assert relative < 2e-12
    print(f"PASS factor-eight n=0 definition check (relative error {relative:.3g})")


def check_duplication_prefactor() -> None:
    for n in range(21):
        left = 8.0 * math.factorial(n) / math.factorial(2 * n)
        right = 8.0 * math.sqrt(math.pi) / (
            4.0**n * math.gamma(n + 0.5)
        )
        assert abs(left / right - 1.0) < 3e-15
    print("PASS duplication prefactor n=0..20")


def check_box_and_denominator_margins() -> None:
    # Exact endpoint arithmetic from the printed outer box, reconstructed here.
    alpha_min, t_min, t_max = Q(5, 2), Q(7, 4), Q(9, 4)
    w_max, delta_max, e_max = Q(6), Q(5, 12), Q(1, 12)
    assert alpha_min / e_max == 30
    assert t_max + w_max * e_max == Q(11, 4)
    assert t_min - 1 - delta_max * e_max == Q(103, 144)
    assert alpha_min / e_max > t_max + w_max * e_max
    assert t_min - 1 - delta_max * e_max > 0

    radius = Q(7, 50)
    assert 1 - radius - Q(3, 4) * radius == Q(151, 200)
    assert 4 - 4 * radius - 3 * radius == Q(151, 50)
    print("PASS exact ordering and Q/reduced-denominator margins")


def check_terminating_producer() -> None:
    # One legal A>B>C>D>0 tuple; every coefficient is built by the definition.
    degree, a, b, c, d_parameter = 7, Q(40), Q(20), Q(12), Q(5)
    assert a > b > c > d_parameter > 0
    for shift in range(degree + 1):
        coefficient = Q(1)
        for k in range(degree - shift + 1):
            denominator = (
                a
                * c
                * (k + 1)
                * (k + b + shift)
                * (k + d_parameter + shift)
            )
            assert denominator > 0
            numerator = (
                d_parameter
                * (k + shift - degree)
                * (k + a + shift)
                * (k + c + shift)
            )
            next_coefficient = coefficient * numerator / denominator
            if k == degree - shift:
                assert next_coefficient == 0
            coefficient = next_coefficient
    print("PASS legal terminating coefficient producer at every derivative shift")


def main() -> None:
    check_factor_eight_at_zero()
    check_duplication_prefactor()
    check_box_and_denominator_margins()
    check_terminating_producer()


if __name__ == "__main__":
    main()
