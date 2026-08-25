#!/usr/bin/env python3
"""Exact clean-room reconstruction of the repaired G0 sixth derivative.

This standard-library sparse calculation starts from the displayed G0 and
implicit saddle derivative.  It reads no frozen expected expression.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F


# (i,j,k) represents N^i L^j Q^(-k).
Terms = dict[tuple[int, int, int], F]
Poly = dict[tuple[int, int], F]


# Q' = RQ/Q along L'=L/Q.
RQ = {
    (1, 0): F(1),
    (1, 1): F(3),
    (1, 2): F(1),
    (0, 2): F(-9, 4),
    (0, 3): F(-3, 4),
}


def add(out, key, value):
    if value:
        out[key] += value
        if not out[key]:
            del out[key]


def derivative(terms: Terms) -> Terms:
    out = defaultdict(F)
    for (i, j, k), coefficient in terms.items():
        if i:
            add(out, (i - 1, j, k), coefficient * i)
        if j:
            add(out, (i, j, k + 1), coefficient * j)
        if k:
            for (di, dj), value in RQ.items():
                add(out, (i + di, j + dj, k + 2), -coefficient * k * value)
    return dict(out)


def multiply(left: Poly, right: Poly) -> Poly:
    out = defaultdict(F)
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            add(out, (a + c, b + d), x * y)
    return dict(out)


def power(base: Poly, exponent: int) -> Poly:
    result = {(0, 0): F(1)}
    factor = base
    while exponent:
        if exponent & 1:
            result = multiply(result, factor)
        factor = multiply(factor, factor)
        exponent //= 2
    return result


def main() -> None:
    # Direct differentiation of
    # G0=(N+1)log L+L/4-N/L-(log Q)/2
    # gives log L plus the following rational part at order one.
    g1 = {
        (0, -1, 0): F(-1),
        (1, 0, 1): F(1),
        (0, 0, 1): F(1, 2),
        (0, 1, 1): F(-1, 4),
        (1, -1, 1): F(1),
        (1, 1, 2): F(-1, 2),
        (0, 2, 2): F(3, 4),
    }
    current = derivative(g1)
    current[(0, 0, 1)] = current.get((0, 0, 1), F()) + 1  # D log L=1/Q
    for _ in range(4):
        current = derivative(current)

    denominator_power = max(k for _, _, k in current)
    q = {(0, 0): F(1), (1, 0): F(1), (0, 1): F(-3, 4)}
    q_powers = {j: power(q, j) for j in range(denominator_power + 1)}
    numerator_q = defaultdict(F)

    # N=1/(r*sigma), L=1/r, Q=q/(r^2*sigma), followed by N^5 L.
    for (i, j, k), coefficient in current.items():
        r_power = 2 * k - i - j - 6
        sigma_power = k - i - 5
        if min(r_power, sigma_power) < 0:
            raise AssertionError("negative normalized monomial power")
        for (a, b), value in q_powers[denominator_power - k].items():
            add(
                numerator_q,
                (r_power + a, sigma_power + b),
                coefficient * value,
            )

    scale = 4**denominator_power
    numerator = {key: value * scale for key, value in numerator_q.items()}
    if any(value.denominator != 1 for value in numerator.values()):
        raise AssertionError("nonintegral reduced numerator")

    box = F(7, 50)
    denominator_floor = F(151, 50)
    majorant = sum(
        abs(value) * box ** (a + b) for (a, b), value in numerator.items()
    ) / denominator_floor**denominator_power
    origin = numerator[(0, 0)] / (4**denominator_power)

    print(f"denominator=(4+4r-3sigma)^{denominator_power}")
    print(f"numerator terms={len(numerator)}")
    print(f"numerator total degree={max(a+b for a,b in numerator)}")
    print(f"H6(0,0)={origin}")
    print(f"post-chain coefficient={2*origin}")
    print(f"box majorant={majorant.numerator}/{majorant.denominator}")
    print(f"box majorant decimal={float(majorant):.12f}")
    print(f"box majorant < 10000: {majorant < 10_000}")


if __name__ == "__main__":
    main()
