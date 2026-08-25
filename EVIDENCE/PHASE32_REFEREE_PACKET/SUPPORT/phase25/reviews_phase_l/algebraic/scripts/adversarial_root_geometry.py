#!/usr/bin/env python3
"""Definition-first numerical attacks on Phase-L gates B6--B8.

Jacobi and hypergeometric coefficients are generated from their finite product
definitions. Roots are recomputed by recursive derivative interlacing and
bisection; no candidate JSON, expected root list, or frozen result is read.
These are broad finite regressions, not proofs of the imported
Jacobi/MSS/MMP theorems.
"""

from __future__ import annotations

import math
from fractions import Fraction as Q
from math import comb, factorial


def pochhammer(x: Q, k: int) -> Q:
    result = Q(1)
    for j in range(k):
        result *= x + j
    return result


def hypergeometric_coefficients(
    d: int, a: Q, b: Q, c: Q, lower_d: Q, lam: Q
) -> list[Q]:
    return [
        pochhammer(Q(-d), k) * pochhammer(a, k) * pochhammer(c, k) * lam**k
        / (pochhammer(b, k) * pochhammer(lower_d, k) * factorial(k))
        for k in range(d + 1)
    ]


def finite_free_ascending(d: int, p: list[Q], q: list[Q]) -> list[Q]:
    return [Q((-1) ** k) * p[k] * q[k] / comb(d, k) for k in range(d + 1)]


def poly_eval(coefficients: list[complex], z: complex) -> complex:
    value = 0j
    for coefficient in reversed(coefficients):
        value = value * z + coefficient
    return value


def derivative(coefficients: list[Q]) -> list[Q]:
    return [Q(k + 1) * coefficients[k + 1] for k in range(len(coefficients) - 1)]


def real_roots_by_interlacing(coefficients: list[float]) -> list[float]:
    """Isolate all simple real roots recursively from derivative roots."""

    while len(coefficients) > 1 and abs(coefficients[-1]) < 1e-300:
        coefficients.pop()
    degree = len(coefficients) - 1
    if degree == 1:
        return [-coefficients[0] / coefficients[1]]
    derivative_coefficients = [float(k + 1) * coefficients[k + 1] for k in range(degree)]
    critical = real_roots_by_interlacing(derivative_coefficients)
    leading = coefficients[-1]
    root_bound = 1 + max(abs(value / leading) for value in coefficients[:-1])
    endpoints = [-root_bound] + critical + [root_bound]
    roots: list[float] = []
    for left, right in zip(endpoints, endpoints[1:]):
        f_left = poly_eval([complex(value) for value in coefficients], left).real
        f_right = poly_eval([complex(value) for value in coefficients], right).real
        if f_left == 0:
            roots.append(left)
            continue
        if f_right == 0:
            roots.append(right)
            continue
        if f_left * f_right > 0:
            continue
        for _ in range(180):
            midpoint = (left + right) / 2
            f_midpoint = poly_eval([complex(value) for value in coefficients], midpoint).real
            if f_left * f_midpoint <= 0:
                right, f_right = midpoint, f_midpoint
            else:
                left, f_left = midpoint, f_midpoint
        roots.append((left + right) / 2)
    # Adjacent intervals share a critical endpoint; deduplicate defensively.
    unique: list[float] = []
    for root in sorted(roots):
        if not unique or abs(root - unique[-1]) > 1e-9:
            unique.append(root)
    assert len(unique) == degree, (degree, unique)
    return unique


def real_positive_roots(coefficients: list[Q], scale: Q) -> list[float]:
    scaled = [float(coefficient * scale**k) for k, coefficient in enumerate(coefficients)]
    roots = real_roots_by_interlacing(scaled)
    values = [root * float(scale) for root in roots]
    assert min(values) > 0
    return sorted(values)


def jacobi_diagonal(U: float, V: float, d: int, k: int) -> float:
    h = U - d - 1
    return U * (h * (V + 2 * k) + 2 * k * (k + 1)) / ((h + 2 * k) * (h + 2 * k + 2))


def jacobi_off_diagonal(U: float, V: float, d: int, k: int) -> float:
    h = U - d - 1
    radicand = (
        k * (k + V - 1) * (k + U - V - d) * (k + h)
        / ((2 * k + h - 1) * (2 * k + h + 1))
    )
    assert radicand >= 0
    return U / (2 * k + h) * math.sqrt(radicand)


def check_entry_bounds() -> tuple[int, float, float]:
    count = 0
    worst_diagonal = 0.0
    worst_row = 0.0
    for d in range(1, 81):
        for v_factor in (32.0, 32.125, 40.0, 64.0, 137.0):
            V = v_factor * d
            for extra_factor in (0.0, 0.01, 1.0, 9.0, 999.0):
                U = V + d + extra_factor * V
                radius = math.sqrt(V * d)
                diagonal_errors = [abs(jacobi_diagonal(U, V, d, k) - V) for k in range(d)]
                assert max(diagonal_errors) <= 4 * radius * (1 + 2e-12)
                worst_diagonal = max(worst_diagonal, max(diagonal_errors) / radius)
                off = [0.0] + [jacobi_off_diagonal(U, V, d, k) for k in range(1, d)] + [0.0]
                row_sums = [off[k] + off[k + 1] for k in range(d)]
                assert max(row_sums) <= 4 * radius * (1 + 2e-12)
                worst_row = max(worst_row, max(row_sums) / radius)
                count += 2 * d
    return count, worst_diagonal, worst_row


def logarithmic_mesh(roots: list[float]) -> float:
    descending = sorted(roots, reverse=True)
    return min(descending[k] / descending[k + 1] for k in range(len(descending) - 1))


def check_root_geometry() -> tuple[int, float, float]:
    checks = 0
    smallest_mesh_margin = float("inf")
    worst_localization_ratio = 0.0
    for d in range(2, 9):
        B = Q(300 * d)
        D = Q(256 * d)
        A = Q(9) * B
        C = Q(2) * D

        # q_{A,B}(y) and q_{C,D}(D*y), both from the terminating 2F1 definition.
        first = hypergeometric_coefficients(d, A, B, Q(1), Q(1), 1 / A)
        second = hypergeometric_coefficients(d, C, D, Q(1), Q(1), D / C)
        model_from_convolution = finite_free_ascending(d, first, second)
        model_direct = hypergeometric_coefficients(d, A, B, C, D, D / (A * C))
        assert model_from_convolution == model_direct

        first_roots = real_positive_roots(first, B)
        second_roots = real_positive_roots(second, Q(1))
        model_roots = real_positive_roots(model_direct, B)
        critical_roots = real_positive_roots(derivative(model_direct), B)

        first_radius = 8 * math.sqrt(float(B * d))
        second_radius = 8 * math.sqrt(float(Q(d, 1) / D))
        assert all(abs(root - float(B)) <= first_radius * (1 + 2e-8) for root in first_roots)
        assert all(abs(root - 1.0) <= second_radius * (1 + 2e-8) for root in second_roots)

        localization = (12 + 8 * math.sqrt(6)) * math.sqrt(float(B * d))
        assert all(abs(root - float(B)) <= localization * (1 + 2e-8) for root in model_roots)
        assert all(abs(root - float(B)) <= localization * (1 + 2e-8) for root in critical_roots)
        worst_localization_ratio = max(
            worst_localization_ratio,
            max(abs(root - float(B)) for root in model_roots) / math.sqrt(float(B * d)),
        )

        first_mesh = logarithmic_mesh(first_roots)
        model_mesh = logarithmic_mesh(model_roots)
        assert first_mesh > 1 + 1e-9
        assert model_mesh + 2e-8 >= first_mesh
        smallest_mesh_margin = min(smallest_mesh_margin, model_mesh - first_mesh)

        # Directly test the original and reciprocal product endpoints that
        # the MSS adapter would supply in these concrete cases.
        u_lower, u_upper = min(first_roots), max(first_roots)
        v_lower, v_upper = min(second_roots), max(second_roots)
        assert min(model_roots) + 2e-7 >= u_lower * v_lower
        assert max(model_roots) <= u_upper * v_upper + 2e-7
        assert 1 / min(model_roots) <= 1 / (u_lower * v_lower) + 2e-10
        checks += 8 * d
    return checks, smallest_mesh_margin, worst_localization_ratio


def main() -> None:
    entry_checks, worst_diagonal, worst_row = check_entry_bounds()
    root_checks, mesh_margin, localization_ratio = check_root_geometry()
    print(
        f"B6 sampled entry attack: {entry_checks} inequalities; "
        f"worst normalized diagonal={worst_diagonal:.6g}, row={worst_row:.6g}"
    )
    print(
        f"B6--B8 definition-built root attack: {root_checks} checks; "
        f"minimum mesh gain={mesh_margin:.6g}, worst localization ratio={localization_ratio:.6g}"
    )
    print("PASS finite root-geometry regressions (external general theorems remain unchecked)")


if __name__ == "__main__":
    main()
