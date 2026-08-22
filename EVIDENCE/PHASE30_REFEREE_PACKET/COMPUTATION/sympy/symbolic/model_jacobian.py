#!/usr/bin/env python3
"""Exact formal parameter-Jacobian audit for the C48 scaled map.

The producer reconstructs the same truncated residual as model_adapter.py,
differentiates the four normalized components in the four gauge variables,
and verifies that every displayed Jacobian error is divisible by x=1/n and
contains no 1/e= L_n contamination.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def derive_components():
    x, e = sp.symbols("x e", nonzero=True)
    alpha, t, w, delta = sp.symbols("alpha t w delta", nonzero=True)
    k, u, v = sp.symbols("k u v")

    def jacobi_log(parameter):
        return sp.log((parameter + k) / (parameter + k + 1))

    upper1 = alpha / (x * e)
    upper2 = t / x
    lower1 = (t + w * e) / x
    lower2 = (1 + delta * e) / x
    model = (
        jacobi_log(upper1)
        - jacobi_log(lower1)
        + jacobi_log(upper2)
        - jacobi_log(lower2)
    )
    model_series = sp.series(
        sp.series(model, e, 0, 2).removeO(), x, 0, 6
    ).removeO()
    baseline = sp.log(1 + x / (1 + (k + sp.Rational(1, 2)) * x))
    saddle = 0
    for power in range(4):
        moment = sp.integrate(
            sp.integrate((k + u + v) ** power, (u, 0, 1)), (v, 0, 1)
        )
        saddle += 2 * e * x * (-x) ** power * moment
    xi_series = sp.series(baseline, x, 0, 6).removeO() - saddle
    residual = sp.expand(model_series - xi_series)
    values = [sp.simplify(residual.subs(k, index)) for index in range(4)]
    differences = [
        values[0],
        values[1] - values[0],
        values[2] - 2 * values[1] + values[0],
        values[3] - 3 * values[2] + 3 * values[1] - values[0],
    ]
    scales = [
        -1 / (x * e),
        1 / (2 * x**2 * e),
        -1 / (2 * x**3 * e),
        1 / (6 * x**4 * e),
    ]
    components = sp.Matrix(
        [sp.simplify(sp.expand(a * b)) for a, b in zip(differences, scales)]
    )
    formal = sp.Matrix(
        [
            delta + w / t**2 + 1 / alpha - 2,
            delta + w / t**3 - 1,
            3 * (delta + w / t**4) - 2,
            4 * (delta + w / t**5) - 2,
        ]
    )
    return x, e, (alpha, t, w, delta), components, formal


def build_report() -> dict:
    x, e, variables, components, formal = derive_components()
    error = sp.simplify(components.jacobian(variables) - formal.jacobian(variables))
    encoded_rows = []
    checks = []
    for row in range(4):
        encoded_row = []
        for column in range(4):
            entry = sp.factor(error[row, column])
            divisible = sp.simplify(entry.subs(x, 0)) == 0
            no_inverse_e = not sp.together(entry).has(1 / e)
            # The alpha column vanishes identically in the displayed error.
            alpha_check = column != 0 or entry == 0
            checks.append(divisible and no_inverse_e and alpha_check)
            encoded_row.append(sp.sstr(sp.collect(sp.expand(entry), x)))
        encoded_rows.append(encoded_row)
    if not all(checks):
        raise AssertionError("parameter-Jacobian formal error check failed")

    return {
        "status": "PASS",
        "sympy_version": sp.__version__,
        "variable_order": [str(value) for value in variables],
        "jacobian_deviation_rows": encoded_rows,
        "all_entries_divisible_by_x": True,
        "all_entries_free_of_inverse_e": True,
        "displayed_alpha_error_column_zero": True,
        "scope": (
            "Exact algebra for the same first-order-in-e, fifth-order-in-x "
            "truncated series as Phase 8. Uniform bounds for omitted terms are "
            "a separate paper argument."
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
