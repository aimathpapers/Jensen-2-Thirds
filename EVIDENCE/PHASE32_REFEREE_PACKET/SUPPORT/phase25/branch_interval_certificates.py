#!/usr/bin/env python3
"""Independent exact-rational checks for the Phase-E finite branch ledger.

This script does not claim the analytic residual or Jacobian enclosures.  It
checks the rational box inclusion margins, inverse row sums, Jacobi ordering
extrema, residual-to-half-radius arithmetic, and non-circular localization
threshold that the Lean theorem consumes.
"""

from fractions import Fraction as Q


def main() -> None:
    center = (Q(3), Q(2), Q(16, 3), Q(1, 3))
    outer = (
        (Q(5, 2), Q(7, 2)),
        (Q(7, 4), Q(9, 4)),
        (Q(5), Q(6)),
        (Q(1, 4), Q(5, 12)),
    )
    margins = tuple((c - lo, hi - c) for c, (lo, hi) in zip(center, outer))
    expected_margins = (
        (Q(1, 2), Q(1, 2)),
        (Q(1, 4), Q(1, 4)),
        (Q(1, 3), Q(2, 3)),
        (Q(1, 12), Q(1, 12)),
    )
    assert margins == expected_margins
    inner_radius = Q(1, 1_000_000)
    assert inner_radius < min(min(pair) for pair in margins)

    inverse = (
        (Q(-9), Q(45), Q(-24), Q(9)),
        (Q(0), Q(6), Q(-6), Q(3)),
        (Q(0), Q(48), Q(-112, 3), Q(16)),
        (Q(0), Q(1), Q(-4, 3), Q(1)),
    )
    row_sums = tuple(sum(abs(entry) for entry in row) for row in inverse)
    assert row_sums == (Q(87), Q(15), Q(304, 3), Q(10, 3))
    assert max(row_sums) == Q(304, 3)
    assert Q(304, 3) * Q(3, 608) == Q(1, 2)

    e_max = Q(1, 12)
    remote_min = outer[0][0] / e_max
    near_max = outer[1][1] + outer[2][1] * e_max
    lower_gap = outer[1][0] - 1 - outer[3][1] * e_max
    assert remote_min == 30
    assert near_max == Q(11, 4)
    assert remote_min > near_max
    assert lower_gap == Q(103, 144) > 0

    k_pre = Q(256)
    c_loc_upper = Q(32)
    k_zero = k_pre * c_loc_upper**2
    assert k_zero == 262_144
    assert k_pre < k_zero
    assert 6 * 4 < 25  # sqrt(6) < 5/2, hence 12+8sqrt(6) < 32.

    print(
        "PASS exact branch intervals: margins, inner inclusion, inverse norm, "
        "ordering extrema, half-radius factor, and K_pre -> C_loc -> K_0"
    )


if __name__ == "__main__":
    main()
