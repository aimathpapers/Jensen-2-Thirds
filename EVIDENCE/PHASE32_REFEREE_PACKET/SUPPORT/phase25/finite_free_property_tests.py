#!/usr/bin/env python3
"""Independent exact checks for the Phase-F finite-free/Jacobi adapters.

Nothing in this file reads generated proof output.  It evaluates the displayed
definitions directly over ``fractions.Fraction`` and checks convention
reflection, the Jacobi diagonal identity, reciprocal/product endpoints, and
the localization arithmetic on deterministic rational grids.
"""

from fractions import Fraction as Q
from math import comb


def ascending(d: int, p: list[Q], q: list[Q]) -> list[Q]:
    return [Q((-1) ** k) * p[k] * q[k] / comb(d, k) for k in range(d + 1)]


def descending(d: int, p: list[Q], q: list[Q]) -> list[Q]:
    return [
        Q((-1) ** (d - k)) * p[k] * q[k] / comb(d, k)
        for k in range(d + 1)
    ]


def reflect(coefficients: list[Q]) -> list[Q]:
    return list(reversed(coefficients))


def check_reflection() -> int:
    count = 0
    for d in range(1, 10):
        p = [Q((k + 2) * (d + 3), k + 1) for k in range(d + 1)]
        q = [Q((2 * k + 3) * (d + 5), k + 2) for k in range(d + 1)]
        assert reflect(ascending(d, p, q)) == descending(
            d, reflect(p), reflect(q)
        )
        assert reflect(descending(d, p, q)) == ascending(
            d, reflect(p), reflect(q)
        )
        assert ascending(d, p, q)[0] == p[0] * q[0]
        count += 3 * (d + 1)
    return count


def diagonal(U: Q, V: Q, d: int, k: int) -> Q:
    H = U - d - 1
    return U * (H * (V + 2 * k) + 2 * k * (k + 1)) / (
        (H + 2 * k) * (H + 2 * k + 2)
    )


def diagonal_displacement(U: Q, V: Q, d: int, k: int) -> Q:
    H = U - d - 1
    return (
        2 * k * (k + H + 1) * (U - 2 * V) + V * H * (d - 1)
    ) / ((H + 2 * k) * (H + 2 * k + 2))


def check_diagonal_identity() -> int:
    count = 0
    for d in range(1, 13):
        for V in (Q(32 * d), Q(40 * d, 1), Q(97 * d, 2)):
            for U in (V + d, 2 * V + d + 1, 5 * V + d):
                for k in range(d):
                    assert diagonal(U, V, d, k) - V == diagonal_displacement(
                        U, V, d, k
                    )
                    count += 1
    return count


def check_endpoint_adapters() -> int:
    count = 0
    for lower, x, upper in (
        (Q(1, 2), Q(3, 4), Q(5, 2)),
        (Q(7, 5), Q(19, 6), Q(23, 4)),
        (Q(101, 100), Q(37, 9), Q(83, 7)),
    ):
        assert Q(1, upper) <= Q(1, x) <= Q(1, lower)
        count += 2

    product_boxes = (
        (Q(2), Q(3), Q(5), Q(7)),
        (Q(3, 5), Q(4, 3), Q(7, 8), Q(9, 4)),
    )
    for u_lower, u_upper, v_lower, v_upper in product_boxes:
        z_lower = u_lower * v_lower
        z_upper = u_upper * v_upper
        for z in (z_lower, (z_lower + z_upper) / 2, z_upper):
            assert z <= u_upper * v_upper
            assert Q(1, z) <= Q(1, u_lower) * Q(1, v_lower)
            assert u_lower * v_lower <= z <= u_upper * v_upper
            count += 3
    return count


def check_localization_algebra() -> int:
    count = 0
    # Exact rational instances of B*s=r*q and s<=1/16.  We use q<=12/5;
    # since (12/5)^2<6 this is strictly below sqrt(6).
    for B, r, s, q in (
        (Q(24), Q(5), Q(1, 24), Q(5)),
        (Q(40), Q(3), Q(3, 80), Q(1, 2)),
        (Q(64), Q(8), Q(1, 32), Q(1, 4)),
    ):
        # The first tuple intentionally fails q<=sqrt(6), so it is excluded
        # from the theorem-domain loop below.
        if q * q >= 6:
            continue
        assert B * s == r * q
        for u in (-8 * r, Q(0), 8 * r):
            for v in (-8 * s, Q(0), 8 * s):
                deviation = abs((B + u) * (1 + v) - B)
                rational_upper = (Q(12) + Q(8) * Q(5, 2)) * r
                assert deviation <= rational_upper
                count += 1
    # Check the exact decomposition separately on a nontrivial legal tuple.
    B, r, s, q = Q(40), Q(3), Q(3, 80), Q(1, 2)
    assert B * s == r * q
    assert 8 * r + 8 * r * q + 64 * r * s <= Q(12) * r + 8 * r * q
    assert q * q < 6 and s <= Q(1, 16)
    count += 3
    return count


def main() -> None:
    total = (
        check_reflection()
        + check_diagonal_identity()
        + check_endpoint_adapters()
        + check_localization_algebra()
    )
    print(
        f"PASS {total} exact finite-free/Jacobi adapter checks: reflection, "
        "diagonal displacement, reciprocal/product endpoints, and localization"
    )


if __name__ == "__main__":
    main()
