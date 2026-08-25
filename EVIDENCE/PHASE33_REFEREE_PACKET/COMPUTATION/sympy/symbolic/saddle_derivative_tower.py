#!/usr/bin/env python3
"""Exact regression for Holland's saddle derivative coefficients 2 through 6."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import sympy as sp


def build_report() -> dict:
    n_var, ell = sp.symbols("N L", positive=True)
    r, sigma = sp.symbols("r sigma", positive=True)
    q_var = (1 + ell) * n_var - sp.Rational(3, 4) * ell**2
    main = (
        (n_var + 1) * sp.log(ell)
        + ell / 4
        - n_var / ell
        - sp.log(q_var) / 2
    )

    def total_derivative(expression):
        return sp.cancel(
            sp.diff(expression, n_var)
            + ell / q_var * sp.diff(expression, ell)
        )

    rows = []
    derivative = main
    for order in range(1, 7):
        derivative = total_derivative(derivative)
        if order < 2:
            continue
        normalized = sp.cancel(derivative * n_var ** (order - 1) * ell)
        two_scale = sp.cancel(
            normalized.subs({ell: 1 / r, n_var: 1 / (r * sigma)})
        )
        sigma_limit = sp.factor(sp.limit(two_scale, sigma, 0))
        saddle_coefficient = sp.limit(sigma_limit, r, 0)
        expected_saddle = (-1) ** order * math.factorial(order - 2)
        h_coefficient = 2 * saddle_coefficient
        expected_h = 2 * expected_saddle
        checks = {
            "saddle_tower_identity": saddle_coefficient == expected_saddle,
            "chain_rule_tower_identity": h_coefficient == expected_h,
        }
        if not all(checks.values()):
            raise AssertionError(f"derivative tower failed at order {order}")
        rows.append(
            {
                "order": order,
                "normalized_saddle_coefficient": str(saddle_coefficient),
                "expected_formula": f"(-1)^{order}*({order}-2)!",
                "h_coefficient_after_N_eq_2x_minus_2": str(h_coefficient),
                "checks": checks,
            }
        )

    return {
        "status": "PASS",
        "sympy_version": sp.__version__,
        "orders": [2, 3, 4, 5, 6],
        "saddle_tower": [row["normalized_saddle_coefficient"] for row in rows],
        "h_tower": [row["h_coefficient_after_N_eq_2x_minus_2"] for row in rows],
        "rows": rows,
        "scope": (
            "Exact rational/logarithmic differentiation of G0 only. Sectorial "
            "remainder and analytic uniformity are separate paper lemmas."
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
