#!/usr/bin/env python3
"""Exact elimination audit for the non-perturbative C48 derivative recurrence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def build_report() -> dict:
    A, B, C, D, y = sp.symbols("A B C D y", positive=True)
    d, m = sp.symbols("d m", nonnegative=True)
    t0, t1, t2, t3 = sp.symbols("T_m T_m1 T_m2 T_m3")
    epsilon = (C - D) / C
    a = 1 - y / A

    def b(index):
        return B + index - y + (d - 1 - 2 * index) * y / A

    def c(index):
        return (d - index) * (1 + index / A) * y

    beta = A * (2 * m + 1 - d) - d * (2 * m + 1) + 3 * m**2 + 3 * m + 1
    gamma = m * (m - d) * (m + A)

    y_u_m = a * t2 + b(m) * t1 + c(m) * t0
    y_u_m1 = a * t3 + b(m + 1) * t2 + c(m + 1) * t1
    y_v_m = y / A * (
        t3 + (A - d + 3 + 3 * m) * t2 + beta * t1 + gamma * t0
    )
    eliminated = sp.expand(y_u_m1 + (D + m) * y_u_m + epsilon * y_v_m)

    coefficients = [
        sp.factor(eliminated.coeff(symbol)) for symbol in (t3, t2, t1, t0)
    ]
    expected = [
        a + epsilon * y / A,
        b(m + 1) + (D + m) * a + epsilon * y / A * (A - d + 3 + 3 * m),
        c(m + 1) + (D + m) * b(m) + epsilon * y / A * beta,
        (D + m) * c(m) + epsilon * y / A * gamma,
    ]
    checks = [
        sp.simplify(actual - target) == 0
        for actual, target in zip(coefficients, expected)
    ]
    if not all(checks):
        raise AssertionError("direct recurrence elimination failed")

    # Independent provenance from the m-shifted generalized hypergeometric
    # differential equation.  If
    #   g_m = 3F2(-(d-m), A+m, C+m; B+m, D+m; lambda*y),
    # then p_F^(m) is a nonzero constant multiple of g_m and
    #   theta(theta+b1-1)(theta+b2-1) g_m
    #     = lambda*y (theta+a1)(theta+a2)(theta+a3) g_m.
    # Expanding theta^j in the basis y^i d^i/dy^i gives the four
    # coefficients below directly, with no auxiliary recurrence hypothesis.
    lam = D / (A * C)
    a1, a2, a3 = m - d, A + m, C + m
    b1, b2 = B + m, D + m
    e1 = a1 + a2 + a3
    e2 = a1 * a2 + a1 * a3 + a2 * a3
    e3 = a1 * a2 * a3
    ode_coefficients = [
        1 - lam * y,
        b1 + b2 + 1 - lam * y * (3 + e1),
        b1 * b2 - lam * y * (1 + e1 + e2),
        -lam * y * e3,
    ]
    ode_checks = [
        sp.simplify(actual - target) == 0
        for actual, target in zip(ode_coefficients, expected)
    ]
    if not all(ode_checks):
        raise AssertionError("shifted 3F2 ODE coefficients do not match")

    def theta(expr):
        return y * sp.diff(expr, y)

    def theta_plus(expr, shift):
        return theta(expr) + shift * expr

    sample_parameters = [
        (37, 11, 7, 3, 5),
        (101, 13, 17, 5, 6),
        (29, 7, 11, 4, 4),
        (4000, 2100, 1800, 1000, 12),
    ]
    sample_checks = 0
    for A0, B0, C0, D0, d0 in sample_parameters:
        lam0 = sp.Rational(D0, A0 * C0)
        polynomial = sp.expand(
            sum(
                sp.rf(-d0, j)
                * sp.rf(A0, j)
                * sp.rf(C0, j)
                / (sp.rf(B0, j) * sp.rf(D0, j) * sp.factorial(j))
                * (lam0 * y) ** j
                for j in range(d0 + 1)
            )
        )
        for m0 in range(d0 + 1):
            derivative = sp.diff(polynomial, y, m0)
            left = theta(
                theta_plus(theta_plus(derivative, D0 + m0 - 1), B0 + m0 - 1)
            )
            right = lam0 * y * theta_plus(
                theta_plus(theta_plus(derivative, C0 + m0), A0 + m0), m0 - d0
            )
            if sp.expand(left - right) != 0:
                raise AssertionError(
                    f"3F2 ODE sample failed at {(A0, B0, C0, D0, d0, m0)}"
                )
            sample_checks += 1

    # Leading branch audit: discard d/n, m/n, (y-B)/n and 1/L corrections.
    n_var, ell, alpha, split = sp.symbols("n L alpha t", positive=True)
    central_leading = expected[1].subs(
        {
            A: alpha * n_var * ell,
            B: split * n_var,
            C: split * n_var,
            D: n_var,
            y: split * n_var,
            d: 0,
            m: 0,
        }
    )
    normalized_central = sp.factor(
        sp.limit(sp.limit(central_leading / n_var, ell, sp.oo), n_var, sp.oo)
    )
    if sp.simplify(normalized_central - split) != 0:
        raise AssertionError("unexpected central recurrence coefficient")

    return {
        "status": "PASS",
        "sympy_version": sp.__version__,
        "epsilon": "(C-D)/C",
        "coefficient_order": ["T_(m+3)", "T_(m+2)", "T_(m+1)", "T_m"],
        "coefficients": [sp.sstr(value) for value in coefficients],
        "elimination_identity_checks": checks,
        "ode_coefficient_checks": ode_checks,
        "ode_coefficients": [sp.sstr(sp.factor(value)) for value in ode_coefficients],
        "ode_polynomial_sample_checks": sample_checks,
        "ode_polynomial_samples": [list(values) for values in sample_parameters],
        "central_coefficient_over_n_limit": sp.sstr(normalized_central),
        "target_split_value": "2",
        "interpretation": (
            "On the target branch the central T_(m+2) coefficient is asymptotic "
            "to 2n. The non-small epsilon term reinforces this coefficient in "
            "the exact direct recurrence instead of being estimated as an error."
        ),
        "scope": (
            "Exact m-shifted 3F2 ODE provenance, algebraic elimination, and "
            "leading-coefficient audit only. "
            "Uniform coefficient inequalities and the maximum argument are paper steps."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(build_report(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
