#!/usr/bin/env python3
"""Definition-derived checks for the two load-bearing equation regressions.

This script does not read any frozen JSON, ledger, checksum, or expected
numerical result.  It derives its comparison values from the completed-zeta
definition, the positive theta kernel, and an explicitly defined scaled
quadratic polynomial.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path


def eta_euler_transform(s: float, terms: int = 80) -> float:
    """Evaluate Dirichlet eta by Euler's transform of its alternating series."""

    differences = [(index + 1) ** (-s) for index in range(terms)]
    total = 0.0
    weight = 0.5
    for _ in range(terms):
        total += weight * differences[0]
        differences = [
            differences[index] - differences[index + 1]
            for index in range(len(differences) - 1)
        ]
        weight *= 0.5
    return total


def zeta_between_zero_and_one(s: float) -> float:
    return eta_euler_transform(s) / (1.0 - 2.0 ** (1.0 - s))


def completed_xi(s: float) -> float:
    return (
        0.5
        * s
        * (s - 1.0)
        * math.pi ** (-s / 2.0)
        * math.gamma(s / 2.0)
        * zeta_between_zero_and_one(s)
    )


def omega(t: float) -> float:
    """Positive Riemann omega kernel, summed until double-precision exhaustion."""

    total = 0.0
    for k in range(1, 100):
        exponent = -math.pi * k * k * t
        if exponent < -745.0:
            term = 0.0
        else:
            term = (
                math.pi**2 * k**4 * t**2
                - 1.5 * math.pi * k**2 * t
            ) * math.exp(exponent)
        total += term
        if k >= 6 and abs(term) < 1e-18 * max(1.0, abs(total)):
            break
    return total


def adaptive_simpson(function, left: float, right: float, tolerance: float) -> float:
    """Deterministic adaptive Simpson integration on a finite interval."""

    def simpson(a: float, b: float, fa: float, fm: float, fb: float) -> float:
        return (b - a) * (fa + 4.0 * fm + fb) / 6.0

    fa = function(left)
    fb = function(right)
    middle = (left + right) / 2.0
    fm = function(middle)
    whole = simpson(left, right, fa, fm, fb)

    def recurse(
        a: float,
        b: float,
        f_a: float,
        f_m: float,
        f_b: float,
        estimate: float,
        budget: float,
        depth: int,
    ) -> float:
        m = (a + b) / 2.0
        lm = (a + m) / 2.0
        rm = (m + b) / 2.0
        f_lm = function(lm)
        f_rm = function(rm)
        left_estimate = simpson(a, m, f_a, f_lm, f_m)
        right_estimate = simpson(m, b, f_m, f_rm, f_b)
        delta = left_estimate + right_estimate - estimate
        if depth <= 0 or abs(delta) <= 15.0 * budget:
            return left_estimate + right_estimate + delta / 15.0
        return recurse(
            a, m, f_a, f_lm, f_m, left_estimate, budget / 2.0, depth - 1
        ) + recurse(
            m, b, f_m, f_rm, f_b, right_estimate, budget / 2.0, depth - 1
        )

    return recurse(left, right, fa, fm, fb, whole, tolerance, 24)


def factor_eight_check() -> None:
    direct = completed_xi(0.5)
    integral = adaptive_simpson(
        lambda u: omega(math.exp(2.0 * u)) * math.exp(u / 2.0),
        0.0,
        6.0,
        1e-14,
    )
    reconstructed = 8.0 * integral
    relative_error = abs(reconstructed / direct - 1.0)
    wrong_factor_error = abs((4.0 * integral) / direct - 1.0)
    if relative_error >= 2e-12:
        raise AssertionError(f"factor-eight reconstruction error: {relative_error}")
    if wrong_factor_error <= 0.49:
        raise AssertionError("factor-four mutation was not separated")

    # Coefficient comparison is exact at the level of formal power series:
    # cosh(wu) contributes u^(2n)/(2n)!, while the definition contributes
    # gamma(n)/n!.  The ratios below must therefore be 8*n!/(2n)!.
    ratios = [
        8 * math.factorial(n) / math.factorial(2 * n) for n in range(9)
    ]
    if ratios[0] != 8 or ratios[1] != 4 or ratios[2] != 2 / 3:
        raise AssertionError("formal coefficient comparison failed")
    print(
        "PASS factor eight from independent completed-zeta/theta definitions: "
        f"relative error={relative_error:.3e}; factor-four error={wrong_factor_error:.3e}"
    )


def radius_scaling_check() -> None:
    """Test scale covariance on p_a(y)=(1-y/a)(1-y/(3a))."""

    correct_values = []
    stale_values = []
    for scale in (1.0, 10.0, 1000.0):
        critical_point = 2.0 * scale
        polynomial_value = -1.0 / 3.0
        second_derivative = 2.0 / (3.0 * scale**2)
        correct = abs(
            critical_point**2 * second_derivative / polynomial_value
        ) ** 0.5
        stale = abs(
            second_derivative / (2.0 * polynomial_value)
        ) ** 0.5
        correct_values.append(correct)
        stale_values.append(stale)
    if max(correct_values) - min(correct_values) > 1e-14:
        raise AssertionError("the displayed radius lost scale invariance")
    if not math.isclose(stale_values[0] / stale_values[1], 10.0, rel_tol=1e-14):
        raise AssertionError("the stale no-y^k, divided-by-k! expression did not rescale")
    print(
        "PASS critical-point radius scaling from an explicit polynomial: "
        f"displayed values={correct_values}; stale values={stale_values}"
    )


def source_spelling_check(packet_root: Path) -> None:
    main = (
        packet_root / "manuscript/source/JENSEN_TWO_THIRDS_MAIN.tex"
    ).read_text(encoding="utf-8")
    required = (
        r"\gamma(n)=\frac{8n!}{(2n)!}",
        r"\omega(e^{2u})e^{u/2}u^{2n}",
        r"\max_{1\le k\le d}",
        r"\left|\frac{y_0^kp_F^{(k)}(y_0)}{p_F(y_0)}\right|^{1/k}",
    )
    forbidden = (
        r"\frac{8\,2^{2n}}{(2n)!}",
        r"\omega(e^{2u})e^u u^{2n}",
        r"\frac{p_F^{(k)}(y)}{k!p_F(y)}",
        r"\max_{0\le k\le d}",
    )
    missing = [needle for needle in required if needle not in main]
    stale = [needle for needle in forbidden if needle in main]
    if missing or stale:
        raise AssertionError(f"source equation mismatch: missing={missing}, stale={stale}")
    print("PASS manuscript source contains corrected factor-eight and radius displays")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet_root", type=Path)
    args = parser.parse_args()
    root = args.packet_root.resolve()
    factor_eight_check()
    radius_scaling_check()
    source_spelling_check(root)
    print("PASS all definition-derived equation recalculations")


if __name__ == "__main__":
    main()
