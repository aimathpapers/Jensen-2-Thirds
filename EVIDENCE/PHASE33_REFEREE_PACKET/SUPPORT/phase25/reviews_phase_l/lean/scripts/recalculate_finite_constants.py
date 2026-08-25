#!/usr/bin/env python3
"""Recalculate finite constants used by the Phase-L Lean interfaces.

All inputs below are transcribed from the displayed definitions in the Lean
sources/manuscript.  No saved result, PASS log, JSON output, or expected-value
artifact is read.  Exact ``Fraction`` arithmetic is used throughout.
"""

from fractions import Fraction as Q
from math import isqrt


def det(matrix: list[list[Q]]) -> Q:
    work = [row[:] for row in matrix]
    result = Q(1)
    for col in range(len(work)):
        pivot = next(row for row in range(col, len(work)) if work[row][col])
        if pivot != col:
            work[col], work[pivot] = work[pivot], work[col]
            result = -result
        pivot_value = work[col][col]
        result *= pivot_value
        for j in range(col, len(work)):
            work[col][j] /= pivot_value
        for row in range(col + 1, len(work)):
            factor = work[row][col]
            for j in range(col, len(work)):
                work[row][j] -= factor * work[col][j]
    return result


def matmul(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    return [
        [sum((left[i][k] * right[k][j] for k in range(4)), Q(0)) for j in range(4)]
        for i in range(4)
    ]


def main() -> None:
    jacobian = [
        [Q(-1, 9), Q(-4, 3), Q(1, 4), Q(1)],
        [Q(0), Q(-1), Q(1, 8), Q(1)],
        [Q(0), Q(-2), Q(3, 16), Q(3)],
        [Q(0), Q(-5, 3), Q(1, 8), Q(4)],
    ]
    inverse = [
        [Q(-9), Q(45), Q(-24), Q(9)],
        [Q(0), Q(6), Q(-6), Q(3)],
        [Q(0), Q(48), Q(-112, 3), Q(16)],
        [Q(0), Q(1), Q(-4, 3), Q(1)],
    ]
    identity = [[Q(int(i == j)) for j in range(4)] for i in range(4)]
    row_sums = [sum(map(abs, row), Q(0)) for row in inverse]

    radius = Q(1, 1_000_000)
    outer_margins = [Q(1, 2), Q(1, 4), Q(1, 3), Q(1, 12)]
    residual_factor = Q(3, 608)
    inverse_bound = max(row_sums)

    e_max = Q(1, 12)
    alpha_over_e_min = Q(5, 2) / e_max
    t_plus_we_max = Q(9, 4) + Q(6) * e_max
    t_minus_one_minus_delta_e_min = Q(7, 4) - 1 - Q(5, 12) * e_max

    localization_threshold = Q(256) * Q(32) ** 2
    sqrt6_upper = Q(5, 2)
    sqrt6_lt_upper = (
        6 * (sqrt6_upper.denominator ** 2) < sqrt6_upper.numerator ** 2
    )

    print(f"det(J) = {det(jacobian)}")
    print(f"J*P = I: {matmul(jacobian, inverse) == identity}")
    print(f"P*J = I: {matmul(inverse, jacobian) == identity}")
    print("absolute row sums(P) = " + ", ".join(map(str, row_sums)))
    print(f"induced infinity bound = {inverse_bound}")
    print(f"(304/3)*(3/608) = {inverse_bound * residual_factor}")
    print(f"inner radius is below every outer-box margin: {all(radius < m for m in outer_margins)}")
    print(f"min(alpha/e) at displayed endpoints = {alpha_over_e_min}")
    print(f"max(t+w*e) at displayed endpoints = {t_plus_we_max}")
    print(
        "min(t-1-delta*e) at displayed endpoints = "
        f"{t_minus_one_minus_delta_e_min}"
    )
    print(f"localization threshold = {localization_threshold}")
    print(f"12+8*sqrt(6) < 32 from sqrt(6)<5/2: {sqrt6_lt_upper}")
    print(
        "sqrt(6)<5/2 exact square check: "
        f"{sqrt6_lt_upper}"
    )
    print("infinite geometric tail sum_(k>=5) 2^-k = 1/16")
    print(f"integer sqrt sanity for threshold: sqrt({int(localization_threshold)}) = {isqrt(int(localization_threshold))}")


if __name__ == "__main__":
    main()
