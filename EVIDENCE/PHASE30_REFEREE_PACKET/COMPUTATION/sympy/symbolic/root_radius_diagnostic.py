#!/usr/bin/env python3
"""High-precision finite-degree diagnostic for the C48 derivative radius."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import mpmath as mp
import sympy as sp


DEGREES = (6, 8, 10)


def build_report(branch_artifact: Path) -> dict:
    mp.mp.dps = 80
    branch = json.loads(branch_artifact.read_text(encoding="utf-8"))
    row = next(item for item in branch["rows"] if item["n"] == 10000)
    n_value = mp.mpf(row["n"])
    lower1, gap1, lower2, gap2 = [
        mp.mpf(value) * n_value
        for value in row["raw_scaled_parameters_B_gapA_D_gapC"]
    ]
    B, A = lower1, lower1 + gap1
    D, C = lower2, lower2 + gap2
    z = sp.symbols("z")
    rows = []

    for degree in DEGREES:
        coefficients = []
        for index in range(degree + 1):
            value = (
                (-1) ** index
                * mp.binomial(degree, index)
                * mp.rf(A, index)
                * mp.rf(C, index)
                * D**index
                / (
                    A**index
                    * C**index
                    * mp.rf(B, index)
                    * mp.rf(D, index)
                )
                * B**index
            )
            coefficients.append(sp.Float(str(value), 80))
        polynomial = sum(
            coefficients[index] * z**index for index in range(degree + 1)
        )
        roots = sp.nroots(polynomial, n=60, maxsteps=500)
        critical = sp.nroots(sp.diff(polynomial, z), n=60, maxsteps=500)
        max_root_imag = max(abs(sp.im(value)) for value in roots)
        max_critical_imag = max(abs(sp.im(value)) for value in critical)
        if max_root_imag > sp.Float("1e-45") or max_critical_imag > sp.Float("1e-45"):
            raise AssertionError("high-precision root solve did not return real roots")

        real_roots = sorted(sp.re(value) for value in roots)
        required_k = mp.mpf(0)
        derivative_polynomials = [sp.diff(polynomial, z, order)
                                  for order in range(degree + 1)]
        for critical_point in critical:
            point = mp.mpf(str(sp.re(critical_point)))
            denominator = mp.mpf(
                str(sp.N(polynomial.subs(z, str(point)), 70))
            )
            for order in range(2, degree + 1):
                derivative_value = mp.mpf(
                    str(sp.N(derivative_polynomials[order].subs(z, str(point)), 70))
                )
                ratio = point**order * derivative_value / denominator
                required_k = max(
                    required_k,
                    abs(ratio) ** (mp.mpf(1) / order) / mp.sqrt(B * degree),
                )
        rows.append(
            {
                "degree": degree,
                "scaled_root_min_y_over_B": mp.nstr(mp.mpf(str(real_roots[0])), 18),
                "scaled_root_max_y_over_B": mp.nstr(mp.mpf(str(real_roots[-1])), 18),
                "max_required_radius_constant_K": mp.nstr(required_k, 18),
                "all_roots_and_critical_points_real_at_45_digits": True,
            }
        )

    if not all(mp.mpf(row["max_required_radius_constant_K"]) < 1 for row in rows):
        raise AssertionError("finite diagnostic exceeded radius constant one")

    return {
        "status": "PASS",
        "formal_status": "not proved",
        "source_branch_n": 10000,
        "degrees": list(DEGREES),
        "parameter_scales_A_B_C_D_over_n": [
            mp.nstr(value / n_value, 30) for value in (A, B, C, D)
        ],
        "rows": rows,
        "interpretation": (
            "At one high-precision finite branch point, the derivative ratios "
            "at every computed critical point satisfy the proposed radius with "
            "K<1 for degrees 6, 8, and 10. This is a mechanism diagnostic, not "
            "a uniform theorem."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    default_branch = Path(__file__).resolve().parents[1] / "high_precision" / "scaled_branch.json"
    parser.add_argument("--branch-artifact", type=Path, default=default_branch)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(build_report(args.branch_artifact), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
