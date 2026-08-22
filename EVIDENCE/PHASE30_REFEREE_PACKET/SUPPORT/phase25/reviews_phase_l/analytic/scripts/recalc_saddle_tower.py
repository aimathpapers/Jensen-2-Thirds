#!/usr/bin/env python3
"""Clean-room exact differentiation of the saddle main term.

This script uses only Python's standard library.  It constructs the implicit
derivative from

    N = L * (pi*exp(L) + 3/4)

and differentiates

    G0 = (N+1) log(L) + L/4 - N/L - log(Q)/2,
    Q  = (1+L)N - 3 L^2/4.

It does not read any candidate JSON, symbolic output, or expected numerator.
The sparse calculation keeps powers of Q symbolic until the final substitution
r=1/L, sigma=L/N.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction as F
from math import factorial


# A term key (i,j,k) denotes N^i * L^j * Q^(-k).
Terms = dict[tuple[int, int, int], F]
Poly = dict[tuple[int, int], F]


def add_term(out: defaultdict[tuple[int, int, int], F], key, value: F) -> None:
    if value:
        out[key] += value
        if not out[key]:
            del out[key]


# Along the implicit saddle branch L' = L/Q.  A short calculation gives
# Q' = RQ/Q, where RQ is the following polynomial in N,L.
RQ: dict[tuple[int, int], F] = {
    (1, 0): F(1),
    (1, 1): F(3),
    (1, 2): F(1),
    (0, 2): F(-9, 4),
    (0, 3): F(-3, 4),
}


def total_derivative(terms: Terms) -> Terms:
    """Apply d/dN + (L/Q)d/dL to a rational term expansion."""

    out: defaultdict[tuple[int, int, int], F] = defaultdict(F)
    for (i, j, k), coefficient in terms.items():
        if i:
            add_term(out, (i - 1, j, k), coefficient * i)
        if j:
            add_term(out, (i, j, k + 1), coefficient * j)
        if k:
            for (di, dj), rq_coefficient in RQ.items():
                add_term(
                    out,
                    (i + di, j + dj, k + 2),
                    -coefficient * k * rq_coefficient,
                )
    return dict(out)


def poly_add(out: defaultdict[tuple[int, int], F], key, value: F) -> None:
    if value:
        out[key] += value
        if not out[key]:
            del out[key]


def poly_mul(left: Poly, right: Poly) -> Poly:
    out: defaultdict[tuple[int, int], F] = defaultdict(F)
    for (a, b), x in left.items():
        for (c, d), y in right.items():
            poly_add(out, (a + c, b + d), x * y)
    return dict(out)


def poly_pow(base: Poly, exponent: int) -> Poly:
    result: Poly = {(0, 0): F(1)}
    factor = base
    power = exponent
    while power:
        if power & 1:
            result = poly_mul(result, factor)
        factor = poly_mul(factor, factor)
        power //= 2
    return result


def build_sixth_normalized_numerator() -> tuple[Poly, int]:
    # First derivative of G0, excluding the sole log(L) term.  Directly
    # differentiating once gives
    # log(L) - 1/L + (N+1/2-L/4)/Q + N/(LQ)
    #          - LN/(2Q^2) + 3L^2/(4Q^2).
    rational_g1: Terms = {
        (0, -1, 0): F(-1),
        (1, 0, 1): F(1),
        (0, 0, 1): F(1, 2),
        (0, 1, 1): F(-1, 4),
        (1, -1, 1): F(1),
        (1, 1, 2): F(-1, 2),
        (0, 2, 2): F(3, 4),
    }

    # G0'' = D(rational part of G0') + D log L, and D log L=1/Q.
    derivative = total_derivative(rational_g1)
    derivative[(0, 0, 1)] = derivative.get((0, 0, 1), F(0)) + 1
    # Four further derivatives produce G0^(6).
    for _ in range(4):
        derivative = total_derivative(derivative)

    max_q_power = max(k for _, _, k in derivative)
    q: Poly = {(0, 0): F(1), (1, 0): F(1), (0, 1): F(-3, 4)}
    q_powers = {p: poly_pow(q, p) for p in range(max_q_power + 1)}
    numerator: defaultdict[tuple[int, int], F] = defaultdict(F)

    # Substitute N=1/(r*sigma), L=1/r, Q=q/(r^2*sigma), then multiply
    # by N^5 L.  Bring every term over the common denominator q^max_q_power.
    for (i, j, k), coefficient in derivative.items():
        r_power = 2 * k - i - j - 6
        sigma_power = k - i - 5
        if r_power < 0 or sigma_power < 0:
            raise AssertionError(
                f"normalization left a negative monomial power: {(i, j, k)}"
            )
        for (a, b), q_coefficient in q_powers[max_q_power - k].items():
            poly_add(
                numerator,
                (r_power + a, sigma_power + b),
                coefficient * q_coefficient,
            )
    return dict(numerator), max_q_power


def main() -> None:
    numerator_q, denominator_power = build_sixth_normalized_numerator()

    # Convert Num/q^12 to P/(4q)^12, the integer-denominator convention used
    # in the paper.  This is a derived normalization, not imported data.
    scale = F(4**denominator_power)
    numerator = {monomial: coefficient * scale for monomial, coefficient in numerator_q.items()}
    if any(value.denominator != 1 for value in numerator.values()):
        raise AssertionError("the reduced numerator did not become integral")

    term_count = len(numerator)
    total_degree = max(a + b for a, b in numerator)
    origin_denominator = 4**denominator_power
    origin_value = numerator.get((0, 0), F(0)) / origin_denominator

    box = F(7, 50)
    denominator_floor = F(151, 50)
    majorant_numerator = sum(
        abs(value) * box ** (a + b) for (a, b), value in numerator.items()
    )
    majorant = majorant_numerator / denominator_floor**denominator_power

    print("clean-room saddle tower")
    print(f"denominator = (4 + 4*r - 3*sigma)^{denominator_power}")
    print(f"numerator term count = {term_count}")
    print(f"numerator total degree = {total_degree}")
    print(f"H6(0,0) = {origin_value}")
    print(f"post-chain leading coefficient = {2 * origin_value}")
    print(f"box majorant = {majorant.numerator}/{majorant.denominator}")
    print(f"box majorant decimal = {float(majorant):.12f}")
    print(f"box majorant < 10000: {majorant < 10_000}")

    # The limiting tower follows by differentiating 1/(N^(m-1)L): the exact
    # calculation above supplies order six; this prints the independently
    # generated factorial pattern for cross-order auditing.
    tower = [2 * ((-1) ** order) * factorial(order - 2) for order in range(2, 7)]
    print(f"post-chain leading tower orders 2..6 = {tower}")


if __name__ == "__main__":
    main()
