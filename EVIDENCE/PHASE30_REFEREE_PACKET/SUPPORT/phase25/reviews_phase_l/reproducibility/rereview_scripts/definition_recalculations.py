#!/usr/bin/env python3
"""Definition-level equation regressions with no frozen expected-result input."""

from __future__ import annotations

import argparse
import math
from fractions import Fraction
from pathlib import Path


def factor_eight_from_series() -> None:
    """Equate the two formal coefficients defined in the manuscript.

    The centered-xi convention gives coefficient gamma(n)/n!, while the
    theta identity and cosh series give 8 I_n/(2n)!. Solving for gamma(n)
    yields 8 n! I_n/(2n)! without importing any stored numerical value.
    """
    for n in range(21):
        xi_coefficient_per_unit_moment = Fraction(8, math.factorial(2 * n))
        derived_gamma_per_unit_moment = (
            math.factorial(n) * xi_coefficient_per_unit_moment
        )
        displayed = Fraction(
            8 * math.factorial(n), math.factorial(2 * n)
        )
        if derived_gamma_per_unit_moment != displayed:
            raise AssertionError(f"factor-eight derivation failed at n={n}")
    n = 2
    correct = Fraction(8 * math.factorial(n), math.factorial(2 * n))
    factor_four = Fraction(4 * math.factorial(n), math.factorial(2 * n))
    stale_power = Fraction(8 * 2 ** (2 * n), math.factorial(2 * n))
    if correct in (factor_four, stale_power):
        raise AssertionError("factor-eight mutations were not distinguished")
    print("PASS factor-eight coefficient derived exactly from both series definitions")


def derivative(coefficients: tuple[Fraction, ...], order: int, y: Fraction) -> Fraction:
    total = Fraction(0)
    for degree in range(order, len(coefficients)):
        falling = math.factorial(degree) // math.factorial(degree - order)
        total += coefficients[degree] * falling * y ** (degree - order)
    return total


def critical_radius_normalization() -> None:
    # p(y)=(y-2)^2+1 has nonzero critical point y0=2 and p(y0)=1.
    coefficients = (Fraction(5), Fraction(-4), Fraction(1))
    y0 = Fraction(2)
    value = sum(coefficient * y0**degree for degree, coefficient in enumerate(coefficients))
    if value != 1 or derivative(coefficients, 1, y0) != 0:
        raise AssertionError("critical-point fixture construction failed")
    correct_second_power = abs(y0**2 * derivative(coefficients, 2, y0) / value)
    stale_second_power = abs(
        derivative(coefficients, 2, y0) / (math.factorial(2) * value)
    )
    if correct_second_power != 8 or stale_second_power != 1:
        raise AssertionError("critical-radius normalization was not distinguished")
    print(
        "PASS critical-radius normalization from a constructed critical-point "
        "polynomial (correct squared term 8; stale squared term 1)"
    )


def check_production_source(packet: Path) -> None:
    main = (packet / "manuscript/source/JENSEN_TWO_THIRDS_MAIN.tex").read_text(
        encoding="utf-8"
    )
    required = (
        r"\frac{8n!}{(2n)!}",
        r"\omega(e^{2u})e^{u/2}u^{2n}",
        r"\max_{1\le k\le d}",
        r"\left|\frac{y_0^kp_F^{(k)}(y_0)}{p_F(y_0)}\right|^{1/k}",
        r"K_r=4096",
    )
    forbidden = (
        r"\frac{8\,2^{2n}}{(2n)!}",
        r"\omega(e^{2u})e^u u^{2n}",
        r"\frac{p_F^{(k)}(y)}{k!p_F(y)}",
    )
    for marker in required:
        if marker not in main:
            raise AssertionError(f"production manuscript omits {marker!r}")
    for marker in forbidden:
        if marker in main:
            raise AssertionError(f"production manuscript retains stale {marker!r}")
    print("PASS production source contains the derived displays and excludes stale forms")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    arguments = parser.parse_args()
    factor_eight_from_series()
    critical_radius_normalization()
    check_production_source(arguments.packet.resolve())
    print("PASS definition-level equation recalculations (no frozen expected result read)")


if __name__ == "__main__":
    main()
