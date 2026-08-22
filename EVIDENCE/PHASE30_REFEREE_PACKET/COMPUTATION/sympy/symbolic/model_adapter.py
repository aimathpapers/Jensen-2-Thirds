#!/usr/bin/env python3
"""Exact formal-series audit for the C48 Phase-8 model-side adapter.

This is a symbolic algebra check, not an asymptotic proof.  It expands the
two-Jacobi log quotient in x=1/n and e=1/L, subtracts the formal first-order
xi saddle model, applies the four forward-difference normalizations, and
checks the limiting rational map used by the Lean leading-system module.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def build_report() -> dict:
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

    gamma_baseline = sp.log(1 + x / (1 + (k + sp.Rational(1, 2)) * x))
    saddle = 0
    for power in range(4):
        moment = sp.integrate(
            sp.integrate((k + u + v) ** power, (u, 0, 1)), (v, 0, 1)
        )
        saddle += 2 * e * x * (-x) ** power * moment
    xi_series = sp.series(gamma_baseline, x, 0, 6).removeO() - saddle
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
    components = [
        sp.simplify(sp.expand(difference * scale))
        for difference, scale in zip(differences, scales)
    ]

    formal = [
        delta + w / t**2 + 1 / alpha - 2,
        delta + w / t**3 - 1,
        3 * (delta + w / t**4) - 2,
        4 * (delta + w / t**5) - 2,
    ]
    expected_deviations = [
        x * (-delta + 2 - w / t**3)
        + x**2 * (delta - sp.Rational(7, 3) + w / t**4)
        + x**3 * (-delta + 3 - w / t**5)
        + x**4 * (delta + w / t**6)
        + (-x / 2 + 3 * x**2 / 4 - x**3 + 21 * x**4 / 16) / e,
        x * (-3 * delta + 3 - 3 * w / t**4)
        + x**2 * (7 * delta - sp.Rational(15, 2) + 7 * w / t**5)
        + x**3 * (-15 * delta - 15 * w / t**6)
        + (-x / 2 + 15 * x**2 / 8 - 21 * x**3 / 4) / e,
        x * (-18 * delta + 12 - 18 * w / t**5)
        + x**2 * (75 * delta + 75 * w / t**6)
        + (-3 * x / 2 + 21 * x**2 / 2) / e,
        x * (-40 * delta - 40 * w / t**6) - 2 * x / e,
    ]
    deviations = [
        sp.simplify(sp.expand(component - limit))
        for component, limit in zip(components, formal)
    ]
    checks = [
        sp.simplify(actual - expected) == 0
        for actual, expected in zip(deviations, expected_deviations)
    ]
    if not all(checks):
        raise AssertionError("formal component decomposition failed")

    def encode(expression) -> str:
        return sp.sstr(sp.collect(sp.expand(expression), [x, e]))

    return {
        "status": "PASS",
        "sympy_version": sp.__version__,
        "coordinates": {
            "x": "1/n",
            "e": "1/L_n",
            "A": "alpha/(x*e)",
            "B": "(t+w*e)/x",
            "C": "t/x",
            "D": "(1+delta*e)/x",
        },
        "normalized_component_limits": [encode(value) for value in formal],
        "displayed_deviations": [encode(value) for value in deviations],
        "exact_decomposition_checks": checks,
        "rate_diagnostic": "displayed terms are O(x/e+x); omitted formal terms are expected O(e+x/e)",
        "scope": (
            "Exact algebra for a series truncated at first order in e and fifth "
            "order in x. This does not bound the omitted terms, prove the xi "
            "saddle expansion, or establish C1 convergence."
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
