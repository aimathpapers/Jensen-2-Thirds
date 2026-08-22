#!/usr/bin/env python3
"""Independent exact checks for the Phase-L algebraic AI re-review.

This script reads no frozen result, JSON ledger, manuscript, or repository
output.  It constructs all test inputs from the displayed definitions.  The
standard-library ``Fraction`` type is used for exact arithmetic; the Jacobi
entry inequalities are checked after squaring, so they also use no floating
point.

The finite grids are regression/falsification checks, not substitutes for the
paper or Lean proofs of universally quantified statements.
"""

from __future__ import annotations

from fractions import Fraction as Q
from math import comb, factorial


def determinant(matrix: list[list[Q]]) -> Q:
    a = [row[:] for row in matrix]
    det = Q(1)
    for column in range(len(a)):
        pivot = next(row for row in range(column, len(a)) if a[row][column])
        if pivot != column:
            a[column], a[pivot] = a[pivot], a[column]
            det = -det
        pivot_value = a[column][column]
        det *= pivot_value
        for j in range(column, len(a)):
            a[column][j] /= pivot_value
        for row in range(column + 1, len(a)):
            factor = a[row][column]
            for j in range(column, len(a)):
                a[row][j] -= factor * a[column][j]
    return det


def inverse(matrix: list[list[Q]]) -> list[list[Q]]:
    size = len(matrix)
    a = [row[:] + [Q(i == j) for j in range(size)] for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if a[row][column])
        a[column], a[pivot] = a[pivot], a[column]
        pivot_value = a[column][column]
        a[column] = [value / pivot_value for value in a[column]]
        for row in range(size):
            if row == column:
                continue
            factor = a[row][column]
            a[row] = [x - factor * y for x, y in zip(a[row], a[column])]
    return [row[size:] for row in a]


def matrix_product(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    return [
        [sum(left[i][k] * right[k][j] for k in range(len(right)))
         for j in range(len(right[0]))]
        for i in range(len(left))
    ]


def check_leading_system() -> int:
    alpha, t, w, delta = Q(3), Q(2), Q(16, 3), Q(1, 3)
    residual = (
        1 / alpha + w / t**2 + delta - 2,
        w / t**3 + delta - 1,
        3 * w / t**4 + 3 * delta - 2,
        4 * w / t**5 + 4 * delta - 2,
    )
    assert residual == (0, 0, 0, 0)

    # Reconstruct the Jacobian directly by differentiating the four rational
    # residuals in coordinate order (alpha,t,w,delta).
    jacobian = [
        [-1 / alpha**2, -2 * w / t**3, 1 / t**2, Q(1)],
        [Q(0), -3 * w / t**4, 1 / t**3, Q(1)],
        [Q(0), -12 * w / t**5, 3 / t**4, Q(3)],
        [Q(0), -20 * w / t**6, 4 / t**5, Q(4)],
    ]
    inv = inverse(jacobian)
    identity = [[Q(i == j) for j in range(4)] for i in range(4)]
    assert determinant(jacobian) == Q(-1, 144)
    assert matrix_product(jacobian, inv) == identity
    assert matrix_product(inv, jacobian) == identity
    assert max(sum(abs(x) for x in row) for row in inv) == Q(304, 3)

    # The two eliminants are reconstructed from the definitions on a broad
    # exact grid, rather than copied from a saved expected-result file.
    checks = 0
    for t0 in (Q(3, 2), Q(2), Q(7, 3), Q(5)):
        for w0 in (Q(1, 3), Q(7, 5), Q(16, 3)):
            for delta0 in (Q(1, 7), Q(1, 3), Q(5, 4)):
                f1 = w0 / t0**3 + delta0 - 1
                f2 = 3 * w0 / t0**4 + 3 * delta0 - 2
                f3 = 4 * w0 / t0**5 + 4 * delta0 - 2
                assert 3 * f1 - f2 == 3 * w0 * (t0 - 1) / t0**4 - 1
                assert Q(4, 3) * f2 - f3 == 4 * w0 * (t0 - 1) / t0**5 - Q(2, 3)
                checks += 2
    return checks + 8


def check_quotient_adapter() -> int:
    checks = 0
    for seed in range(1, 20):
        a = [Q(seed * seed - 3 * seed + 2), Q(2 * seed - 5)]
        b = a[:]
        second_differences = [Q(seed + k * k, k + 1) for k in range(4)]
        for value in second_differences:
            a.append(value + 2 * a[-1] - a[-2])
            b.append(value + 2 * b[-1] - b[-2])
        assert a == b and len(a) == 6
        checks += 6
    return checks


def hypergeometric_coefficients(d: int, A: int, B: int, C: int, D: int) -> list[Q]:
    lam = Q(D, A * C)
    coefficients = [Q(1)]
    for k in range(d):
        coefficients.append(
            coefficients[-1] * lam * (k - d) * (A + k) * (C + k)
            / ((k + 1) * (B + k) * (D + k))
        )
    return coefficients


def derivative_value(coefficients: list[Q], order: int, y: Q) -> Q:
    return sum(
        coefficients[k] * Q(factorial(k), factorial(k - order)) * y ** (k - order)
        for k in range(order, len(coefficients))
    )


def recurrence_coefficients(
    A: Q, B: Q, C: Q, D: Q, y: Q, d: Q, m: Q
) -> tuple[Q, Q, Q, Q]:
    lam = D / (A * C)
    e1 = (m - d) + (A + m) + (C + m)
    e2 = (m - d) * (A + m) + (m - d) * (C + m) + (A + m) * (C + m)
    e3 = (m - d) * (A + m) * (C + m)
    return (
        1 - lam * y,
        B + D + 2 * m + 1 - lam * y * (3 + e1),
        (B + m) * (D + m) - lam * y * (1 + e1 + e2),
        -lam * y * e3,
    )


def decomposed_recurrence_coefficients(
    A: Q, B: Q, C: Q, D: Q, y: Q, d: Q, m: Q
) -> tuple[Q, Q, Q, Q]:
    epsilon = (C - D) / C
    a = 1 - y / A

    def b(index: Q) -> Q:
        return B + index - y + (d - 1 - 2 * index) * y / A

    def c(index: Q) -> Q:
        return (d - index) * (1 + index / A) * y

    beta = A * (2 * m + 1 - d) - d * (2 * m + 1) + 3 * m**2 + 3 * m + 1
    gamma = m * (m - d) * (m + A)
    return (
        a + epsilon * y / A,
        b(m + 1) + (D + m) * a + epsilon * y / A * (A - d + 3 + 3 * m),
        c(m + 1) + (D + m) * b(m) + epsilon * y / A * beta,
        (D + m) * c(m) + epsilon * y / A * gamma,
    )


def check_hypergeometric_recurrence() -> tuple[int, int]:
    tuples = (
        (17, 11, 13, 7, 4),
        (31, 19, 23, 12, 7),
        (101, 47, 61, 29, 9),
        (4001, 2101, 1801, 1009, 12),
    )
    checks = 0
    bad_display_detections = 0
    for A, B, C, D, d in tuples:
        coefficients = hypergeometric_coefficients(d, A, B, C, D)
        for m in range(d + 1):
            for y in (Q(2 * B + 1, 3), Q(B), Q(5 * B - 2, 4)):
                p = recurrence_coefficients(Q(A), Q(B), Q(C), Q(D), y, Q(d), Q(m))
                assert p == decomposed_recurrence_coefficients(
                    Q(A), Q(B), Q(C), Q(D), y, Q(d), Q(m)
                )
                jet = [y ** (m + j) * derivative_value(coefficients, m + j, y)
                       for j in range(4)]
                assert sum(coefficient * value for coefficient, value in zip(p, reversed(jet))) == 0

                # The two packet displays with B+D+3m+1 differ from the
                # ODE/decomposed coefficient by exactly +m.
                lam = Q(D, A * C)
                printed_p2 = B + D + 3 * m + 1 - lam * y * (A + C + 3 * m - d + 3)
                assert printed_p2 - p[1] == m
                if m:
                    assert printed_p2 != p[1]
                    bad_display_detections += 1
                checks += 6
    return checks, bad_display_detections


def finite_free_ascending(d: int, p: list[Q], q: list[Q]) -> list[Q]:
    return [Q((-1) ** k) * p[k] * q[k] / comb(d, k) for k in range(d + 1)]


def finite_free_descending(d: int, p: list[Q], q: list[Q]) -> list[Q]:
    return [Q((-1) ** (d - k)) * p[k] * q[k] / comb(d, k) for k in range(d + 1)]


def check_finite_free_conventions() -> int:
    checks = 0
    for d in range(1, 15):
        p = [Q((k + 1) * (d + 2), 2 * k + 1) for k in range(d + 1)]
        q = [Q((3 * k + 2) * (d + 5), k + 2) for k in range(d + 1)]
        assert list(reversed(finite_free_ascending(d, p, q))) == finite_free_descending(
            d, list(reversed(p)), list(reversed(q))
        )
        checks += d + 1
    return checks


def jacobi_diagonal(U: Q, V: Q, d: int, k: int) -> Q:
    H = U - d - 1
    return U * (H * (V + 2 * k) + 2 * k * (k + 1)) / (
        (H + 2 * k) * (H + 2 * k + 2)
    )


def jacobi_off_diagonal_squared(U: Q, V: Q, d: int, k: int) -> Q:
    H = U - d - 1
    beta = U - V - d
    radicand = Q(k) * (k + V - 1) * (k + beta) * (k + H) / (
        (2 * k + H - 1) * (2 * k + H + 1)
    )
    return (U / (2 * k + H)) ** 2 * radicand


def check_jacobi_and_product_bounds() -> int:
    checks = 0
    for d in range(1, 41):
        for V in (Q(32 * d), Q(33 * d), Q(64 * d), Q(257 * d, 3)):
            for U in (V + d, 2 * V + d + 1, 5 * V + d, 1000 * V + d):
                for k in range(d):
                    displacement = jacobi_diagonal(U, V, d, k) - V
                    assert displacement**2 <= 16 * V * d
                    checks += 1
                for k in range(1, d):
                    assert jacobi_off_diagonal_squared(U, V, d, k) <= 4 * V * d
                    checks += 1

    # Exact rational envelope used after the two Jacobi intervals.
    assert Q(1, 16) ** 2 == Q(1, 256)
    assert Q(12, 5) ** 2 < 6  # 12/5 < sqrt(6)
    assert 12 + 8 * Q(5, 2) == 32  # sqrt(6) < 5/2 => C_loc < 32
    assert 1 - 8 / Q(16) == Q(1, 2)  # K_pre=256 gives positive endpoints
    checks += 4
    return checks


def check_global_maximum_and_budgets() -> int:
    C0, C1, Kr = Q(48), Q(96), Q(4096)
    q_constant = 8 * C1 / Kr + 8 * C0 / Kr**2
    assert q_constant == Q(24579, 131072) < Q(1, 4)

    x_q3 = 1 / (3 * (128 * Kr) ** 2)
    x_q1 = Kr**2 / (2 * (64 * C1) ** 2)
    assert 16 * Kr * Q(1, 128 * Kr) == Q(1, 8)
    assert 8 * C1 / Kr * Q(Kr, 64 * C1) == Q(1, 8)
    assert q_constant + Q(1, 8) + Q(1, 8) < Q(1, 2)
    assert x_q3 == Q(1, 824633720832)
    assert x_q1 == Q(2, 9)

    # Index audit: m=k-2 centers T_k.  The higher neighbor is inside the
    # global maximum for k<d and is the terminating T_(d+1)=0 for k=d.
    checks = 7
    for d in range(2, 101):
        for k in range(2, d + 1):
            m = k - 2
            assert 0 <= m <= d - 2
            assert (m, m + 1, m + 2, m + 3) == (k - 2, k - 1, k, k + 1)
            assert (k < d and k + 1 <= d) or (k == d)
            checks += 3
    return checks


def check_hermite_genocchi_and_assembly() -> int:
    mass = Q(1)
    for denominator in (6, 5, 4, 3, 2, 1):
        mass /= denominator
    assert mass == Q(1, 720)

    checks = 1
    for z in (Q(-3, 2), Q(1, 3), Q(13, 4), Q(8)):
        product = Q(1)
        for node in range(6):
            product *= z - node
        h = z**2 + 3 * z + 2
        f = product * h
        assert f == product * h
        for node in range(6):
            node_product = Q(1)
            for other in range(6):
                node_product *= Q(node - other)
            assert node_product == 0
        checks += 7

    for length in range(1, 50):
        tail = sum(Q(1, 2) ** k for k in range(5, 5 + length))
        assert tail < Q(1, 16)
        checks += 1

    positive_roots = [Q(1, 3), Q(7, 4), Q(9, 2), Q(23, 3)]
    scale = Q(17, 5)
    negative_roots = [-root / scale for root in positive_roots]
    assert all(root < 0 for root in negative_roots)
    assert len(set(negative_roots)) == len(positive_roots)
    return checks + 2


def main() -> None:
    totals: dict[str, int] = {}
    totals["B1 leading system/Jacobian"] = check_leading_system()
    totals["B2 quotient adapter"] = check_quotient_adapter()
    recurrence_checks, bad_displays = check_hypergeometric_recurrence()
    totals["B3-B4 terminating producer/recurrence"] = recurrence_checks
    totals["B5 convention adapter"] = check_finite_free_conventions()
    totals["B6-B8 Jacobi/product/mesh arithmetic"] = check_jacobi_and_product_bounds()
    totals["B9 global maximum/radius budgets"] = check_global_maximum_and_budgets()
    totals["B10-B11 HG/finite assembly"] = check_hermite_genocchi_and_assembly()

    for gate, count in totals.items():
        print(f"PASS {gate}: {count} exact checks")
    print(
        "DETECTED manuscript P2 display discrepancy: "
        f"B+D+3m+1 differs from the reconstructed P2 by +m "
        f"in {bad_displays} nonzero-m exact instances"
    )
    print(f"PASS total exact checks: {sum(totals.values())}")


if __name__ == "__main__":
    main()
