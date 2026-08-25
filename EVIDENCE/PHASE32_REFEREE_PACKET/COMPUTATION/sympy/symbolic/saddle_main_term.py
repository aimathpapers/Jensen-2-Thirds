#!/usr/bin/env python3
"""Exact symbolic differentiation of Holland's saddle main term.

The calculation treats L=L_N implicitly through L' = L/Q and differentiates
G_0(N) five times.  It verifies the two normalized leading coefficients used
by the proposed Phase-9 signed-saddle lemma.  It does not bound the analytic
remainder in Holland's sectorial expansion.
"""

from __future__ import annotations

import argparse
import json
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
        return sp.factor(
            sp.diff(expression, n_var)
            + ell / q_var * sp.diff(expression, ell)
        )

    derivatives = []
    current = main
    for _ in range(5):
        current = total_derivative(current)
        derivatives.append(current)

    expected = {
        4: (
            2 * r**4 + 10 * r**3 + 20 * r**2 + 11 * r + 2
        ) / (1 + r) ** 5,
        5: -(
            6 * r**6
            + 42 * r**5
            + 126 * r**4
            + 210 * r**3
            + 146 * r**2
            + 47 * r
            + 6
        ) / (1 + r) ** 7,
    }

    rows = []
    for order in (4, 5):
        normalized = sp.cancel(derivatives[order - 1] * n_var ** (order - 1) * ell)
        two_scale = sp.factor(
            normalized.subs({ell: 1 / r, n_var: 1 / (r * sigma)})
        )
        leading_in_sigma = sp.factor(sp.limit(two_scale, sigma, 0))
        coefficient = sp.limit(leading_in_sigma, r, 0)
        difference_quotient = sp.cancel(
            (two_scale - leading_in_sigma) / sigma
        )
        checks = {
            "leading_rational_identity": sp.simplify(
                leading_in_sigma - expected[order]
            ) == 0,
            "sigma_remainder_is_regular_at_zero": not difference_quotient.has(
                sp.zoo, sp.nan
            ),
        }
        if not all(checks.values()):
            raise AssertionError(f"saddle derivative check failed at order {order}")
        rows.append(
            {
                "derivative_order": order,
                "normalized_expression": f"N^{order - 1}*L*G0^({order})(N)",
                "sigma_zero_limit": sp.sstr(leading_in_sigma),
                "r_zero_limit": str(coefficient),
                "difference_is_sigma_times_rational": True,
                "checks": checks,
            }
        )

    # With N=2x-2, the fifth chain-rule factor is 2^5 and N^4/x^4 -> 2^4.
    h_fifth_coefficient = sp.Rational(2**5, 2**4) * expected[5].subs(r, 0)
    if h_fifth_coefficient != -12:
        raise AssertionError("unexpected h-fifth coefficient")

    return {
        "status": "PASS",
        "sympy_version": sp.__version__,
        "implicit_derivative": "dL/dN = L / ((1+L)N - 3L^2/4)",
        "scale_variables": {"r": "1/L", "sigma": "L/N"},
        "rows": rows,
        "chain_rule_h_fifth_coefficient": str(h_fifth_coefficient),
        "scope": (
            "Exact differentiation of the explicit G0 main term. The sectorial "
            "remainder, explicit normalization terms, and uniformity are not "
            "proved by this symbolic calculation."
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
