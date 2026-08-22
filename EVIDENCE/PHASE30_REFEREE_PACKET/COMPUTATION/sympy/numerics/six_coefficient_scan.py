#!/usr/bin/env python3
"""Numerical Phase-4 gate for a six-coefficient Jensen comparison model.

Holland's two-Jacobi finite-free model (arXiv:2608.08682v1) fixes one of
its four shape parameters and matches R_0,...,R_4.  This script leaves all
four shape parameters free and asks the next exact design question:

    can two positive Jacobi factors match R_0,...,R_5?

The xi coefficients are reconstructed from the positive theta-kernel moment
representation.  We solve the four quotient equations q_0,...,q_3 twice,
using adaptive quadrature and fixed Gauss--Legendre quadrature independently.

This is a non-rigorous discovery computation.  It neither proves existence
of an asymptotic positive parameter branch nor proves a wider hyperbolicity
wedge.  Its purpose is to decide whether that proof campaign survives its
first sign/positivity test.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from scipy.integrate import quad
from scipy.optimize import least_squares, minimize_scalar
from scipy.special import gammaln, logsumexp, roots_legendre


N_VALUES = (20, 30, 50, 80, 100, 150)
THETA_TERMS = 24
INTEGRAL_CUTOFF = 6.0


def log_phi(u: float) -> float:
    """Log of the positive Riemann Xi theta kernel, up to a common factor.

    The omitted common normalization cancels from every coefficient ratio.
    Every summand is positive for u >= 0.
    """

    e2u = math.exp(2.0 * u)
    terms = []
    for k in range(1, THETA_TERMS + 1):
        kk = float(k * k)
        x = math.pi * kk * e2u
        terms.append(
            math.log(math.pi * kk)
            + 2.5 * u
            + math.log(2.0 * math.pi * kk * e2u - 3.0)
            - x
        )
    return float(logsumexp(terms))


def log_gamma_coefficient(n: int, method: str) -> float:
    """Return log gamma(n) in Holland's centered-xi normalization.

    gamma(n) = n! M_n / (2n)!, and M_n is evaluated after subtracting the
    maximum of its log integrand.  The two supported methods have different
    quadrature implementations but share the same positive kernel formula.
    """

    if n < 0:
        raise ValueError("n must be nonnegative")

    def log_integrand(u: float) -> float:
        if u <= 0.0:
            return log_phi(0.0) if n == 0 else -math.inf
        return log_phi(u) + 2.0 * n * math.log(u)

    saddle = minimize_scalar(
        lambda u: -log_integrand(u),
        bounds=(1.0e-10, 5.0),
        method="bounded",
        options={"xatol": 1.0e-13},
    )
    if not saddle.success:
        raise RuntimeError(f"moment saddle search failed for n={n}")
    scale = log_integrand(float(saddle.x))

    if method == "adaptive":
        integral, error = quad(
            lambda u: math.exp(log_integrand(u) - scale),
            0.0,
            INTEGRAL_CUTOFF,
            epsabs=5.0e-14,
            epsrel=5.0e-14,
            limit=500,
        )
        if integral <= 0.0 or error / integral > 2.0e-11:
            raise RuntimeError(f"unreliable adaptive moment for n={n}")
    elif method == "gauss1024":
        nodes, weights = roots_legendre(1024)
        mapped = 0.5 * INTEGRAL_CUTOFF * (nodes + 1.0)
        values = np.exp([log_integrand(float(u)) - scale for u in mapped])
        integral = 0.5 * INTEGRAL_CUTOFF * float(np.dot(weights, values))
    else:
        raise ValueError(f"unknown quadrature method: {method}")

    return (
        float(gammaln(n + 1))
        - float(gammaln(2 * n + 1))
        + scale
        + math.log(integral)
    )


def log_quotients(n: int, method: str) -> np.ndarray:
    logs = np.array(
        [log_gamma_coefficient(n + j, method) for j in range(6)],
        dtype=float,
    )
    return np.array(
        [2.0 * logs[k + 1] - logs[k] - logs[k + 2] for k in range(4)],
        dtype=float,
    )


def log_jacobi_quotient(k: int, upper: float, lower: float) -> float:
    """log q_k(U,V) in Holland equation (49), evaluated stably."""

    if not upper > lower > 0.0:
        raise ValueError("a positive Jacobi factor requires U > V > 0")
    return math.log1p(-1.0 / (upper + k + 1.0)) - math.log1p(
        -1.0 / (lower + k + 1.0)
    )


def residual(log_parameters: np.ndarray, target: np.ndarray) -> np.ndarray:
    lower1, gap1, lower2, gap2 = np.exp(log_parameters)
    upper1 = lower1 + gap1
    upper2 = lower2 + gap2
    model = np.array(
        [
            log_jacobi_quotient(k, upper1, lower1)
            + log_jacobi_quotient(k, upper2, lower2)
            for k in range(4)
        ]
    )
    # The equations become increasingly ill-scaled with n.  This fixed scale
    # affects only the optimizer, not the reported unscaled residual.
    return 1.0e12 * (model - target)


@dataclass
class Solution:
    n: int
    method: str
    lower1: float
    gap1: float
    lower2: float
    gap2: float
    max_abs_logq_residual: float
    jacobian_condition: float

    def to_json(self) -> dict:
        return {
            "n": self.n,
            "method": self.method,
            "lower1_over_n": self.lower1 / self.n,
            "gap1_over_n": self.gap1 / self.n,
            "lower2_over_n": self.lower2 / self.n,
            "gap2_over_n": self.gap2 / self.n,
            "upper1_over_lower1": (self.lower1 + self.gap1) / self.lower1,
            "upper2_over_lower2": (self.lower2 + self.gap2) / self.lower2,
            "max_abs_logq_residual": self.max_abs_logq_residual,
            "jacobian_condition": self.jacobian_condition,
        }


def solve_one(
    n: int,
    method: str,
    initial_scaled: Sequence[float],
) -> Solution:
    target = log_quotients(n, method)
    initial = np.log(np.asarray(initial_scaled, dtype=float) * n)
    fit = least_squares(
        residual,
        initial,
        args=(target,),
        max_nfev=30000,
        xtol=1.0e-14,
        ftol=1.0e-14,
        gtol=1.0e-14,
    )
    parameters = np.exp(fit.x)
    unscaled = residual(fit.x, target) / 1.0e12
    singular_values = np.linalg.svd(fit.jac, compute_uv=False)
    condition = float(singular_values[0] / singular_values[-1])
    if float(np.max(np.abs(unscaled))) > 2.0e-12:
        raise RuntimeError(
            f"six-coefficient fit failed for n={n}, method={method}: "
            f"{np.max(np.abs(unscaled))}"
        )
    return Solution(
        n=n,
        method=method,
        lower1=float(parameters[0]),
        gap1=float(parameters[1]),
        lower2=float(parameters[2]),
        gap2=float(parameters[3]),
        max_abs_logq_residual=float(np.max(np.abs(unscaled))),
        jacobian_condition=condition,
    )


def solve_sequence(method: str, n_values: Iterable[int]) -> list[Solution]:
    # A broad positive start; subsequent n values use continuation.
    scaled = np.array([4.0, 15.0, 1.5, 0.4], dtype=float)
    answers = []
    for n in n_values:
        solution = solve_one(n, method, scaled)
        answers.append(solution)
        scaled = np.array(
            [solution.lower1, solution.gap1, solution.lower2, solution.gap2]
        ) / n
    return answers


def build_report(n_values: Sequence[int]) -> dict:
    adaptive = solve_sequence("adaptive", n_values)
    gauss = solve_sequence("gauss1024", n_values)
    by_key = {(row.n, row.method): row for row in adaptive + gauss}

    comparisons = []
    for n in n_values:
        first = by_key[(n, "adaptive")]
        second = by_key[(n, "gauss1024")]
        p = np.array([first.lower1, first.gap1, first.lower2, first.gap2]) / n
        q = np.array([second.lower1, second.gap1, second.lower2, second.gap2]) / n
        comparisons.append(
            {
                "n": n,
                "max_scaled_parameter_disagreement": float(np.max(np.abs(p - q))),
                "minimum_positive_gap_over_n": float(min(p[1], p[3], q[1], q[3])),
            }
        )

    all_rows = adaptive + gauss
    min_gap = min(min(row.gap1, row.gap2) / row.n for row in all_rows)
    max_residual = max(row.max_abs_logq_residual for row in all_rows)
    max_disagreement = max(
        row["max_scaled_parameter_disagreement"] for row in comparisons
    )
    return {
        "status": "PASS",
        "claim_scope": "non-rigorous positivity/sign gate only",
        "source": "Holland arXiv:2608.08682v1 equations (10), (49), and (52)",
        "matched_coefficients": [0, 1, 2, 3, 4, 5],
        "matched_quotients": [0, 1, 2, 3],
        "methods": ["adaptive", "gauss1024"],
        "n_values": list(n_values),
        "solutions": [row.to_json() for row in all_rows],
        "method_comparisons": comparisons,
        "minimum_positive_gap_over_n": min_gap,
        "maximum_logq_residual": max_residual,
        "maximum_scaled_parameter_disagreement": max_disagreement,
        "formal_status": "not proved",
        "interpretation": (
            "Both independent quadratures find positive two-Jacobi parameters "
            "matching q0..q3 throughout the scan.  This supports, but does not "
            "prove, an R0..R5 comparison model and a sixth-order residual campaign."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n-values",
        default=",".join(map(str, N_VALUES)),
        help="comma-separated positive derivative indices",
    )
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    n_values = tuple(int(value) for value in args.n_values.split(","))
    if not n_values or any(n <= 0 for n in n_values):
        raise ValueError("all n values must be positive")
    report = build_report(n_values)
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
