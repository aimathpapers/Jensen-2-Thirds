#!/usr/bin/env python3
"""Independent exact recalculation of the order-six HG normalization.

This script reads no packet or repository result.  It constructs all inputs
from the recursive mass and six-node product definitions.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import factorial


@lru_cache(maxsize=None)
def triangle_mass(i: int, r: int) -> Fraction:
    if i == 0:
        return Fraction(1, r + 1)
    return triangle_mass(i - 1, r + 1) / Fraction(r + 1)


def multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    result = [Fraction(0)] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def derivative(coefficients: list[Fraction]) -> list[Fraction]:
    return [Fraction(i) * coefficients[i] for i in range(1, len(coefficients))]


def evaluate(coefficients: list[Fraction], x: Fraction) -> Fraction:
    value = Fraction(0)
    for coefficient in reversed(coefficients):
        value = value * x + coefficient
    return value


def main() -> None:
    for n in range(1, 10):
        assert triangle_mass(n - 1, 0) == Fraction(1, factorial(n))

    stick_breaking_mass = Fraction(1)
    for exponent in (5, 4, 3, 2, 1, 0):
        stick_breaking_mass *= Fraction(1, exponent + 1)
    assert stick_breaking_mass == Fraction(1, 720)
    assert triangle_mass(5, 0) == stick_breaking_mass

    product = [Fraction(1)]
    for node in range(6):
        product = multiply(product, [Fraction(-node), Fraction(1)])
    constant = Fraction(-17, 13)
    polynomial = [constant * coefficient for coefficient in product]
    sixth = polynomial
    for _ in range(6):
        sixth = derivative(sixth)
    assert sixth == [Fraction(720) * constant]
    for node in range(6):
        assert evaluate(polynomial, Fraction(node)) == 0

    z = Fraction(13, 2)
    newton_product = evaluate(product, z)
    assert evaluate(polynomial, z) == newton_product * sixth[0] * stick_breaking_mass
    radius = max(abs(z - node) for node in range(6))
    assert abs(evaluate(polynomial, z)) <= abs(sixth[0]) * radius**6 / 720

    print("PASS independent exact HG recalculation")
    print(f"  triangle_mass(5,0) = {triangle_mass(5, 0)}")
    print(f"  stick-breaking mass = {stick_breaking_mass}")
    print("  six-node degree-six Newton/HG identity and M*rho^6/720 bound pass")
    print("  frozen expected results read: none")


if __name__ == "__main__":
    main()
