#!/usr/bin/env python3
"""Falsify the manuscript's L+i*v Gaussian sign from its definitions.

This script reads no repository artifact and contains no frozen expected
result.  It solves the displayed saddle equation, constructs the displayed
phase, and compares the vertical and horizontal local directions.
"""

from __future__ import annotations

import cmath
import math


def saddle(s: float) -> float:
    """Solve s = L * (pi*exp(L) + 3/4) on the positive real branch."""
    value = math.log(s) - math.log(math.log(s)) - math.log(math.pi)
    for _ in range(30):
        exponential = math.pi * math.exp(value)
        residual = value * (exponential + 0.75) - s
        derivative = exponential * (value + 1.0) + 0.75
        value -= residual / derivative
    return value


def phase(s: float, u: complex) -> complex:
    # Full logarithmic u-integrand after t = exp(u).
    return s * cmath.log(u) + u / 4.0 - math.pi * cmath.exp(u)


def main() -> None:
    s = math.exp(12.0)  # Legal positive-sector input in the stated saddle range.
    ell = saddle(s)
    curvature = s * (1.0 / ell + 1.0 / ell**2) - 0.75

    # These follow algebraically from the saddle equation.
    first = s / ell + 0.25 - math.pi * math.exp(ell)
    second = -s / ell**2 - math.pi * math.exp(ell)
    assert abs(first - 1.0) < 1e-10
    assert abs(second + curvature) < 1e-9
    assert curvature > 0.0

    v = 1e-3
    vertical = (phase(s, ell + 1j * v) - phase(s, ell)).real
    vertical_quadratic = curvature * v * v / 2.0
    horizontal = (phase(s, ell + v) - phase(s, ell)).real
    horizontal_quadratic_with_linear = v - curvature * v * v / 2.0

    # Along L+i*v the quadratic sign is positive, not the manuscript's negative.
    assert vertical > 0.0
    assert abs(vertical / vertical_quadratic - 1.0) < 1e-5
    # Along L+r the correct frozen Phase-21 calculation retains the linear term.
    assert abs(horizontal / horizontal_quadratic_with_linear - 1.0) < 2e-2

    print("FAIL manuscript vertical Gaussian direction")
    print(f"s={s:.15g}")
    print(f"L={ell:.15g}")
    print(f"K={curvature:.15g}")
    print(f"Re(Phi(L+i*v)-Phi(L))={vertical:.15g}")
    print(f"+K*v^2/2={vertical_quadratic:.15g}")
    print("The claimed -K*v^2/2 has the opposite sign.")


if __name__ == "__main__":
    main()
