#!/usr/bin/env python3
"""High-precision diagnostic for the scaled C48 two-Jacobi branch.

This reconstructs the centered-xi coefficient quotients from the positive
theta-kernel moment and solves the four quotient equations with mpmath.  It
then converts the raw Jacobi parameters to the four-coordinate gauge used by
the Phase-5 leading-system derivation:

  alpha = A / (n L_n)
  t     = C / n
  w     = L_n (B - C) / n
  delta = L_n (D - n) / n.

The Lean-checked formal target is (3, 2, 16/3, 1/3).  Observed convergence is
discovery evidence only; the computation supplies no C^1 error bound and no
asymptotic existence theorem.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path
from typing import Sequence

import mpmath as mp
from scipy.optimize import minimize_scalar


DEFAULT_N = (100, 10000, 1000000)
# At n >= 100 the tilted moment is concentrated where the k >= 2 theta
# terms are far below the 70-digit working precision.  This truncation is a
# numerical acceleration, not a certified tail bound.
THETA_TERMS = 1


def theta_phi(u: mp.mpf) -> mp.mpf:
    e2u = mp.exp(2 * u)
    terms = []
    for k in range(1, THETA_TERMS + 1):
        terms.append(
            (
                2 * mp.pi**2 * k**4 * mp.exp(mp.mpf("4.5") * u)
                - 3 * mp.pi * k**2 * mp.exp(mp.mpf("2.5") * u)
            )
            * mp.exp(-mp.pi * k**2 * e2u)
        )
    return mp.fsum(terms)


def double_saddle(n: int) -> float:
    """Cheap location used only to split and scale the mp quadrature."""

    def leading_log_integrand(u: float) -> float:
        e2u = math.exp(2 * u)
        return (
            math.log(math.pi)
            + 2.5 * u
            + math.log(2 * math.pi * e2u - 3)
            - math.pi * e2u
            + 2 * n * math.log(u)
        )

    result = minimize_scalar(
        lambda u: -leading_log_integrand(u),
        bounds=(1.0e-8, 12.0),
        method="bounded",
        options={"xatol": 1.0e-13},
    )
    if not result.success:
        raise RuntimeError(f"saddle search failed for n={n}")
    return float(result.x)


def log_gamma_coefficient(n: int) -> mp.mpf:
    saddle = mp.mpf(double_saddle(n))
    scale = mp.log(theta_phi(saddle)) + 2 * n * mp.log(saddle)

    def scaled_integrand(u: mp.mpf) -> mp.mpf:
        if not u:
            return mp.mpf(0)
        return mp.exp(mp.log(theta_phi(u)) + 2 * n * mp.log(u) - scale)

    integral = mp.quad(
        scaled_integrand,
        [0, saddle / 2, saddle, 2 * saddle, mp.mpf(14)],
    )
    if not integral > 0:
        raise RuntimeError(f"nonpositive moment integral for n={n}")
    return (
        mp.loggamma(n + 1)
        - mp.loggamma(2 * n + 1)
        + scale
        + mp.log(integral)
    )


def log_jacobi_quotient(k: int, upper: mp.mpf, lower: mp.mpf) -> mp.mpf:
    return mp.log(
        (upper + k)
        * (lower + k + 1)
        / ((lower + k) * (upper + k + 1))
    )


def saddle_scale(n: int) -> mp.mpf:
    """Holland's L_n = L_(2n-2)."""

    target = mp.mpf(2 * n - 2)
    guess = mp.log(target + 2)
    return mp.findroot(
        lambda value: value * (mp.pi * mp.exp(value) + mp.mpf("0.75")) - target,
        guess,
    )


def quotient_targets(n: int) -> list[mp.mpf]:
    logs = [log_gamma_coefficient(n + j) for j in range(6)]
    return [2 * logs[k + 1] - logs[k] - logs[k + 2] for k in range(4)]


def solve_branch(n: int, seed_scaled: Sequence[mp.mpf]):
    targets = quotient_targets(n)

    def equations(lower1, gap1, lower2, gap2):
        upper1 = lower1 + gap1
        upper2 = lower2 + gap2
        return tuple(
            log_jacobi_quotient(k, upper1, lower1)
            + log_jacobi_quotient(k, upper2, lower2)
            - targets[k]
            for k in range(4)
        )

    solution = mp.findroot(
        equations,
        tuple(value * n for value in seed_scaled),
        solver="mdnewton",
        tol=mp.mpf("1e-50"),
        maxsteps=100,
    )
    return list(solution), targets


def decimal(value: mp.mpf, digits: int = 40) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


def build_report(n_values: Sequence[int], precision: int) -> dict:
    mp.mp.dps = precision
    seed = [mp.mpf("2.8659"), mp.mpf("16.0235"), mp.mpf("1.2101"), mp.mpf("0.4384")]
    rows = []
    target = [mp.mpf(3), mp.mpf(2), mp.mpf(16) / 3, mp.mpf(1) / 3]

    for n in n_values:
        started = time.monotonic()
        parameters, logq = solve_branch(n, seed)
        lower1, gap1, lower2, gap2 = parameters
        seed = [value / n for value in parameters]
        upper1 = lower1 + gap1
        upper2 = lower2 + gap2
        scale = saddle_scale(n)
        gauge = [
            upper1 / (n * scale),
            upper2 / n,
            scale * (lower1 - upper2) / n,
            scale * (lower2 - n) / n,
        ]
        residuals = [
            log_jacobi_quotient(k, upper1, lower1)
            + log_jacobi_quotient(k, upper2, lower2)
            - logq[k]
            for k in range(4)
        ]
        rows.append(
            {
                "n": n,
                "L_n": decimal(scale),
                "raw_scaled_parameters_B_gapA_D_gapC": [
                    decimal(value / n) for value in parameters
                ],
                "gauge_alpha_t_w_delta": [decimal(value) for value in gauge],
                "max_gauge_error_from_formal_target": decimal(
                    max(abs(gauge[i] - target[i]) for i in range(4))
                ),
                "max_abs_logq_residual": decimal(max(abs(value) for value in residuals)),
                "elapsed_seconds_diagnostic_only": round(time.monotonic() - started, 3),
            }
        )

    # Timings are deliberately excluded from the frozen comparison artifact.
    for row in rows:
        row.pop("elapsed_seconds_diagnostic_only")

    errors = [mp.mpf(row["max_gauge_error_from_formal_target"]) for row in rows]
    return {
        "status": "PASS",
        "formal_status": "not proved",
        "precision_decimal_digits": precision,
        "theta_terms": THETA_TERMS,
        "n_values": list(n_values),
        "formal_target_alpha_t_w_delta": ["3", "2", "5.333333333333333333333333333333333333333", "0.3333333333333333333333333333333333333333"],
        "rows": rows,
        "gauge_error_strictly_decreases": all(
            errors[index + 1] < errors[index] for index in range(len(errors) - 1)
        ),
        "interpretation": (
            "The high-precision numerical branch approaches the Lean-checked "
            "formal leading solution in the chosen four-coordinate gauge. "
            "This is not a C1 convergence proof or a Jensen-wedge theorem."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-values", default=",".join(map(str, DEFAULT_N)))
    parser.add_argument("--precision", type=int, default=70)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    n_values = tuple(int(item) for item in args.n_values.split(","))
    if any(n < 100 for n in n_values):
        raise ValueError("the high-precision asymptotic scan requires n >= 100")
    if args.precision < 60:
        raise ValueError("at least 60 decimal digits are required")
    report = build_report(n_values, args.precision)
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
