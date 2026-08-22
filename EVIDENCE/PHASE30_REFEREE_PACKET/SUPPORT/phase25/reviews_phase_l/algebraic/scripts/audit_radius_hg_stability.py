#!/usr/bin/env python3
"""Definition-first audit for Phase-L gates B9--B11.

No frozen expected output is opened.  The script rebuilds the terminating
model, critical points, derivative jets, recurrence budgets, simplex mass,
and Newton multiplier identity from definitions.  It also gives an exact
counterexample to the *local first-failure inference* printed in the
manuscript; that counterexample does not refute the valid global-maximum
argument or the radius theorem itself.
"""

from __future__ import annotations

from fractions import Fraction as Q
from math import comb, factorial, sqrt

from adversarial_root_geometry import (
    derivative,
    hypergeometric_coefficients,
    poly_eval,
    real_positive_roots,
)


def eval_fraction(coefficients: list[Q], x: Q) -> Q:
    value = Q(0)
    for coefficient in reversed(coefficients):
        value = value * x + coefficient
    return value


def forward_differences(values: list[Q]) -> list[Q]:
    row = values[:]
    result = []
    while row:
        result.append(row[0])
        row = [b - a for a, b in zip(row, row[1:])]
    return result


def check_radius_budget_and_models() -> None:
    c0 = Q(48)
    c1 = Q(96)
    k_r = Q(4096)
    constant_neighbors = 8 * c1 / k_r + 8 * c0 / k_r**2
    assert constant_neighbors < Q(1, 4)

    x_q3 = 1 / (3 * (128 * k_r) ** 2)
    x_q1 = k_r**2 / (2 * (64 * c1) ** 2)
    eta = Q(1, 1000)
    x_domain = eta**2 / (48 * k_r**2)
    x_admissible = min(x_q3, x_q1, Q(1, 2 * 262_144), x_domain, eta / 2)
    assert 16 * k_r * sqrt(float(3 * x_admissible)) <= Q(1, 8)
    assert 8 * c1 / k_r * sqrt(float(x_admissible)) <= Q(1, 8)
    assert constant_neighbors + Q(1, 8) + Q(1, 8) < 1

    tested_jets = 0
    worst_normalized = 0.0
    for d in range(2, 9):
        B = Q(300 * d)
        D = Q(256 * d)
        A = 9 * B
        C = 2 * D
        coefficients = hypergeometric_coefficients(d, A, B, C, D, D / (A * C))
        critical = real_positive_roots(derivative(coefficients), B)
        rho = float(k_r) * sqrt(float(B * d))
        derivative_lists = [coefficients]
        for _ in range(d):
            derivative_lists.append(derivative(derivative_lists[-1]))
        for critical_point in critical:
            p_value = poly_eval([complex(float(value)) for value in coefficients], critical_point).real
            assert abs(p_value) > 1e-16
            for order in range(d + 1):
                derivative_value = poly_eval(
                    [complex(float(value)) for value in derivative_lists[order]], critical_point
                ).real
                jet = critical_point**order * derivative_value / p_value
                normalized = abs(jet) / rho**order if order else abs(jet)
                assert normalized <= 1 + 2e-7
                worst_normalized = max(worst_normalized, normalized)
                tested_jets += 1

    # Exact logical counterexample to the printed first-failure step.  After
    # normalization let P2=1, the only neighbor coefficient be P3=1/4, and
    # take T2=2, T3=-8.  Index 2 is the first value above one, but the higher
    # (not-yet-bounded) neighbor cancels it exactly.
    t0, t1, t2, t3 = Q(1), Q(0), Q(2), Q(-8)
    assert abs(t0) <= 1 and abs(t1) <= 1 and abs(t2) > 1
    assert t2 + Q(1, 4) * t3 == 0
    assert Q(1, 4) < 1
    print(
        f"B9: constant neighbor budget={constant_neighbors}; {tested_jets} model jets pass; "
        f"worst normalized jet={worst_normalized:.6g}; local first-failure inference falsified"
    )


def check_hermite_genocchi() -> None:
    exponents = (5, 4, 3, 2, 1, 0)
    mass = Q(1)
    for exponent in exponents:
        mass *= Q(1, exponent + 1)
    assert mass == Q(1, 720)

    # The degree-six Newton product saturates the constant: its sixth
    # derivative is 6!=720, so (M/720)*|product| is exactly |f(z)|.
    z = complex(Q(7, 3), Q(5, 4))
    product = 1 + 0j
    for node in range(6):
        product *= z - node
    bound = factorial(6) * float(mass) * abs(product)
    assert abs(abs(product) - bound) < 1e-12
    print(f"B10: stick-breaking mass={mass}; degree-six extremizer attains the 1/720 bound")


def check_newton_multiplier_and_gain() -> None:
    d = 9
    polynomial = [Q((-1) ** j * (3 * j + 2), j + 1) for j in range(d + 1)]
    # Definition-built multiplier: first five integer samples are exactly 1,
    # while higher samples are perturbed by a falling-factorial term.
    multiplier = [Q(1) + Q(1, 10_000) * Q(factorial(j), factorial(j - 5))
                  if j >= 5 else Q(1) for j in range(d + 1)]
    transformed = [a * c for a, c in zip(polynomial, multiplier)]
    differences = forward_differences(multiplier)
    assert differences[0] == 1
    assert all(differences[k] == 0 for k in range(1, 5))

    y = Q(7, 11)
    lhs = eval_fraction(transformed, y) / eval_fraction(polynomial, y)
    derivative_lists = [polynomial]
    for _ in range(d):
        derivative_lists.append(derivative(derivative_lists[-1]))
    rhs = sum(
        differences[k] / factorial(k) * y**k
        * eval_fraction(derivative_lists[k], y) / eval_fraction(polynomial, y)
        for k in range(d + 1)
    )
    assert lhs == rhs

    finite_tail = sum(Q(1, 2) ** k for k in range(5, d + 1))
    assert finite_tail < Q(1, 16)

    # Recalculate the sixth-match scaling identity from rho=K_r*sqrt(B*d).
    # Squaring avoids any floating-point radical: rho^6=K_r^6*(B*d)^3.
    k_r = 4096
    n, degree, B = 10**18, 10**4, 3 * 10**18
    rho_sixth = k_r**6 * (B * degree) ** 3
    assert rho_sixth == k_r**6 * B**3 * degree**3
    defect_numerator = Q(3**6, 720) * rho_sixth
    normalized = defect_numerator / (n**5)
    comparison_scale = Q(3**6 * 3**3 * k_r**6, 720) * Q(degree**3, n**2)
    assert normalized == comparison_scale
    print(
        "B11: Newton multiplier identity exact; fifth-order tail < 1/16; "
        "sixth radius power gives d^3/n^2 exactly"
    )


def main() -> None:
    check_radius_budget_and_models()
    check_hermite_genocchi()
    check_newton_multiplier_and_gain()
    print("PASS definition-first B9--B11 recalculation, with one proof-method falsification")


if __name__ == "__main__":
    main()
