#!/usr/bin/env python3
"""Deterministic exact property tests for the terminating 3F2 recurrence."""

from __future__ import annotations

from fractions import Fraction
from math import factorial
import random


def coefficients(d: int, a: int, b: int, c: int, lower_d: int, lam: Fraction) -> list[Fraction]:
    values = [Fraction(1)]
    for k in range(d):
        values.append(
            values[-1]
            * lam
            * (k - d)
            * (a + k)
            * (c + k)
            / ((b + k) * (lower_d + k) * (k + 1))
        )
    return values


def check_tuple(a: int, b: int, c: int, lower_d: int, d: int) -> int:
    lam = Fraction(lower_d, a * c)
    base = coefficients(d, a, b, c, lower_d, lam)
    checks = 0
    for m in range(d + 1):
        degree = d - m
        shifted = coefficients(degree, a + m, b + m, c + m, lower_d + m, lam)
        prefactor = Fraction(factorial(m)) * base[m]

        for k in range(degree + 1):
            derivative_coefficient = Fraction(factorial(k + m), factorial(k)) * base[k + m]
            assert derivative_coefficient == prefactor * shifted[k]
            checks += 1

        for n in range(degree + 2):
            cn = shifted[n] if n <= degree else Fraction(0)
            previous = shifted[n - 1] if 1 <= n <= degree + 1 else Fraction(0)
            left = n * (n + b + m - 1) * (n + lower_d + m - 1) * cn
            right = (
                lam
                * (n - 1 + m - d)
                * (n - 1 + a + m)
                * (n - 1 + c + m)
                * previous
            ) if n else Fraction(0)
            assert left == right
            checks += 1

        y = Fraction(2 * a + b + c + lower_d + d + m, 7)
        e1 = (m - d) + (a + m) + (c + m)
        e2 = (m - d) * (a + m) + (m - d) * (c + m) + (a + m) * (c + m)
        e3 = (m - d) * (a + m) * (c + m)
        ode = (
            1 - lam * y,
            b + m + lower_d + m + 1 - lam * y * (3 + e1),
            (b + m) * (lower_d + m) - lam * y * (1 + e1 + e2),
            -lam * y * e3,
        )
        epsilon = Fraction(c - lower_d, c)
        rec_a = 1 - Fraction(y, a)

        def rec_b(index: int) -> Fraction:
            return b + index - y + Fraction((d - 1 - 2 * index) * y, a)

        def rec_c(index: int) -> Fraction:
            return (d - index) * (1 + Fraction(index, a)) * y

        beta = a * (2 * m + 1 - d) - d * (2 * m + 1) + 3 * m * m + 3 * m + 1
        gamma = m * (m - d) * (m + a)
        direct = (
            rec_a + epsilon * Fraction(y, a),
            rec_b(m + 1) + (lower_d + m) * rec_a
            + epsilon * Fraction(y, a) * (a - d + 3 + 3 * m),
            rec_c(m + 1) + (lower_d + m) * rec_b(m)
            + epsilon * Fraction(y, a) * beta,
            (lower_d + m) * rec_c(m) + epsilon * Fraction(y, a) * gamma,
        )
        assert ode == direct
        checks += 4
    return checks


def main() -> None:
    rng = random.Random(0xC48)
    samples = [(5, 12, 9, 7, 3), (8, 25, 13, 9, 4), (11, 40, 19, 12, 5)]
    for _ in range(24):
        samples.append(
            (
                rng.randint(2, 60),
                rng.randint(2, 80),
                rng.randint(2, 60),
                rng.randint(2, 50),
                rng.randint(1, 11),
            )
        )
    total = sum(check_tuple(*sample) for sample in samples)
    print(f"PASS exact terminating 3F2 properties: {len(samples)} tuples, {total} identities")


if __name__ == "__main__":
    main()
