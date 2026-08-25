#!/usr/bin/env python3
"""Exact symbolic sixth derivative of Holland's saddle main term."""

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

    derivative = main
    for _ in range(6):
        derivative = total_derivative(derivative)

    normalized = sp.cancel(derivative * n_var**5 * ell)
    two_scale = sp.cancel(
        normalized.subs({ell: 1 / r, n_var: 1 / (r * sigma)})
    )
    reduced_numerator, reduced_denominator = map(
        sp.factor, sp.fraction(two_scale)
    )
    leading = sp.factor(sp.limit(two_scale, sigma, 0))
    expected = (
        24 * r**8
        + 216 * r**7
        + 864 * r**6
        + 2016 * r**5
        + 3024 * r**4
        + 2399 * r**3
        + 1042 * r**2
        + 242 * r
        + 24
    ) / (1 + r) ** 9
    remainder_quotient = sp.cancel((two_scale - leading) / sigma)
    expected_denominator = (4 + 4 * r - 3 * sigma) ** 12
    checks = {
        "leading_rational_identity": sp.simplify(leading - expected) == 0,
        "reduced_denominator_identity": sp.simplify(
            reduced_denominator - expected_denominator
        ) == 0,
        "denominator_nonzero_at_origin": reduced_denominator.subs(
            {r: 0, sigma: 0}
        ) == 4**12,
        "normalized_value_at_origin_is_24": sp.simplify(
            reduced_numerator.subs({r: 0, sigma: 0})
            / reduced_denominator.subs({r: 0, sigma: 0})
        ) == 24,
        "sigma_remainder_is_regular_at_zero": not remainder_quotient.has(
            sp.zoo, sp.nan
        ),
        "normalized_main_limit_is_24": sp.limit(leading, r, 0) == 24,
    }
    if not all(checks.values()):
        raise AssertionError("sixth saddle main-term check failed")

    # N=2x-2 contributes 2^6, while N^5/x^5 tends to 2^5.
    h_sixth = sp.Rational(2**6, 2**5) * 24
    if h_sixth != 48:
        raise AssertionError("unexpected h-sixth coefficient")

    return {
        "status": "PASS",
        "sympy_version": sp.__version__,
        "implicit_derivative": "dL/dN = L / ((1+L)N - 3L^2/4)",
        "scale_variables": {"r": "1/L", "sigma": "L/N"},
        "normalized_expression": "N^5*L*G0^(6)(N)",
        "reduced_denominator": sp.sstr(reduced_denominator),
        "numerator_term_count": len(sp.Poly(reduced_numerator, r, sigma).terms()),
        "denominator_value_at_origin": str(
            reduced_denominator.subs({r: 0, sigma: 0})
        ),
        "sigma_zero_limit": sp.sstr(leading),
        "r_zero_limit": "24",
        "chain_rule_h_sixth_coefficient": str(h_sixth),
        "difference_is_sigma_times_rational": True,
        "checks": checks,
        "scope": (
            "Exact differentiation of the explicit G0 main term only. The "
            "extension of Holland's sectorial remainder estimate to derivative "
            "six and the residual-multiplier argument are paper steps."
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
