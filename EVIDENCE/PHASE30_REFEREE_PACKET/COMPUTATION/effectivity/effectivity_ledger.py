#!/usr/bin/env python3
"""Build and validate the Phase-H constant/threshold dependency ledger.

All numerical nodes use integers or ``fractions.Fraction``.  The two inputs
that the paper does not presently quantify are kept as named symbols:
``C_B6`` (the assembled uniform sixth-derivative constant) and
``N_analytic`` (the maximum analytic/branch threshold).  The script never
turns diagnostics into theorem constants.
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
FROZEN = HERE / "EFFECTIVITY_LEDGER.json"


def q(value: Q) -> str:
    return f"{value.numerator}/{value.denominator}"


def ceil_fraction(value: Q) -> int:
    return -(-value.numerator // value.denominator)


def node(
    identifier: str,
    kind: str,
    dependencies: list[str],
    expression: str,
    value: str | None,
    role: str,
    source: str,
) -> dict[str, Any]:
    return {
        "id": identifier,
        "kind": kind,
        "dependencies": dependencies,
        "expression": expression,
        "value": value,
        "role": role,
        "source": source,
    }


def build_ledger() -> dict[str, Any]:
    theta_out = Q(1, 200)
    theta_boundary = Q(1, 400)
    theta_center = Q(1, 800)
    eta = Q(1, 1000)
    cauchy_delta = Q(1, 1000)
    cauchy_sixth_loss = cauchy_delta ** -6

    c_jacobi = Q(8)
    c_loc_upper = Q(32)
    k_pre = Q(256)
    k_zero = k_pre * c_loc_upper**2
    c_zero = Q(48)
    c_one_upper = Q(96)  # max(3*C_loc,66), using C_loc<32.
    k_radius = Q(4096)
    q_constant = 8 * c_one_upper / k_radius + 8 * c_zero / k_radius**2
    q_constant_margin = Q(1, 4) - q_constant

    # Each vanishing neighbor term is assigned at most 1/8.
    x_q3 = Q(1, 3 * (128 * int(k_radius)) ** 2)
    x_q1 = Q(int(k_radius) ** 2, 2 * (64 * int(c_one_upper)) ** 2)
    x_localization = Q(1, 2 * int(k_zero))
    x_domain = eta**2 / (48 * k_radius**2)
    x_linear_domain = eta / 2
    x_admissible = min(x_q3, x_q1, x_localization, x_domain, x_linear_domain)

    # For n>=2, log(n+2)<=n.  Thus the wedge implies
    # (d/n)^3 < 1/K, and this integer K forces d/n<x_admissible.
    k_geometry = ceil_fraction(x_admissible ** -3) + 1

    # Crude explicit threshold implying L_(2n-2)>=12.  We use pi<22/7 and
    # e<3, so 12(pi e^12+3/4) < this rational upper bound.
    saddle_at_12_upper = Q(12) * (Q(22, 7) * 3**12 + Q(3, 4))
    n_l12 = ceil_fraction((saddle_at_12_upper + 2) / 2)
    n_exp12 = ceil_fraction(Q(3**12 + 2, 2))
    n_explicit = max(128, 2, n_l12, n_exp12)

    # On the union of radius-2*rho discs, rho>=d gives |z-j|<=3rho.
    # B<=3n then gives rho^6<=27*K_r^6*n^3*d^3.
    hermite_product = Q(3**6)
    b_cube = Q(3**3)
    simplex_mass = Q(1, 720)
    defect_coefficient_multiplier = (
        hermite_product * b_cube * simplex_mass * k_radius**6
    )
    exponential_multiplier = 2 * defect_coefficient_multiplier

    nodes = [
        node("theta_out", "exact_rational", [], "1/200", q(theta_out),
             "outer saddle sector", "Phase 21 / Phase 18"),
        node("theta_boundary", "exact_rational", ["theta_out"], "1/400",
             q(theta_boundary), "Cauchy boundary sector", "Phase 18"),
        node("theta_center", "exact_rational", ["theta_boundary"], "1/800",
             q(theta_center), "Cauchy center sector", "Phase 18"),
        node("eta", "exact_rational", [], "1/1000", q(eta),
             "complex domain containment", "Phase 18"),
        node("delta_C", "exact_rational", [], "1/1000", q(cauchy_delta),
             "nested-sector Cauchy gap", "Phase 18"),
        node("cauchy_sixth_loss", "exact_integer", ["delta_C"],
             "delta_C^(-6)", str(cauchy_sixth_loss.numerator),
             "raw sixth-derivative Cauchy loss", "Phase 18"),
        node("C_J", "exact_integer", [], "8", "8",
             "single-factor Gershgorin radius", "Phase F Lean"),
        node("C_loc", "algebraic", ["C_J"], "12+8*sqrt(6)", "12+8*sqrt(6)",
             "finite-free product localization", "Phase F Lean / Phase 16"),
        node("C_loc_upper", "exact_integer", ["C_loc"],
             "32, since sqrt(6)<5/2", "32",
             "rational envelope for C_loc", "Phase E Lean"),
        node("K_pre", "exact_integer", ["C_J"], "256", "256",
             "positive factor endpoints", "Phase E Lean"),
        node("K_0", "exact_integer", ["K_pre", "C_loc_upper"],
             "K_pre*C_loc_upper^2", str(k_zero.numerator),
             "strengthened Jacobi parameter box", "Phase E Lean"),
        node("C_0", "exact_integer", [], "48", "48",
             "P0 recurrence coefficient envelope", "Phase 16"),
        node("C_1_upper", "exact_integer", ["C_loc_upper"],
             "max(3*C_loc_upper,66)", str(c_one_upper.numerator),
             "P1 recurrence coefficient envelope", "Phase 16"),
        node("K_r", "exact_integer", ["C_0", "C_1_upper"], "4096", "4096",
             "critical-point derivative radius multiplier", "Phase H"),
        node("q_constant", "exact_rational", ["K_r", "C_0", "C_1_upper"],
             "8*C_1_upper/K_r+8*C_0/K_r^2", q(q_constant),
             "constant Q1+Q0 neighbor contribution", "Phase H"),
        node("q_constant_margin", "exact_rational", ["q_constant"],
             "1/4-q_constant", q(q_constant_margin),
             "strict budget left before vanishing terms", "Phase H"),
        node("x_q3", "exact_rational", ["K_r"],
             "1/(3*(128*K_r)^2)", q(x_q3),
             "forces Q3<=1/8", "Phase H"),
        node("x_q1", "exact_rational", ["K_r", "C_1_upper"],
             "K_r^2/(2*(64*C_1_upper)^2)", q(x_q1),
             "forces vanishing Q1 part<=1/8", "Phase H"),
        node("x_localization", "exact_rational", ["K_0"],
             "1/(2*K_0)", q(x_localization),
             "forces B,D>=K_0*d from B,D>=n/2", "Phase H"),
        node("x_domain", "exact_rational", ["eta", "K_r"],
             "eta^2/(48*K_r^2)", q(x_domain),
             "forces 2*rho<=eta*n/2 using B<=3n", "Phase H"),
        node("x_linear_domain", "exact_rational", ["eta"], "eta/2",
             q(x_linear_domain), "forces d<=eta*n/2", "Phase H"),
        node("x_admissible", "exact_rational",
             ["x_q3", "x_q1", "x_localization", "x_domain", "x_linear_domain"],
             "minimum of five exact d/n caps", q(x_admissible),
             "common geometry/radius/domain cap", "Phase H"),
        node("K_geometry", "exact_integer", ["x_admissible"],
             "ceil(x_admissible^(-3))+1", str(k_geometry),
             "wedge constant forcing d/n<x_admissible for n>=2", "Phase H"),
        node("N_L12", "exact_integer", [],
             "ceil((12*((22/7)*3^12+3/4)+2)/2)", str(n_l12),
             "crude sufficient threshold for L_(2n-2)>=12", "Phase H"),
        node("N_exp12", "exact_integer", [], "ceil((3^12+2)/2)",
             str(n_exp12), "crude sufficient threshold for 2n-2>=e^12", "Phase H"),
        node("N_explicit", "exact_integer", ["N_L12", "N_exp12"],
             "max(128,2,N_L12,N_exp12)", str(n_explicit),
             "maximum fully numerical threshold", "Phase H"),
        node("C_B6", "external_constant", [], "positive absolute constant", None,
             "uniform assembled sixth-derivative bound", "Phase 17 (B6)"),
        node("N_analytic", "external_threshold", [], "positive integer", None,
             "maximum branch/sector/asymptotic threshold", "Phases 15, 18, 21"),
        node("C_defect_factor", "exact_rational", ["K_r"],
             "3^6*3^3*K_r^6/720", q(defect_coefficient_multiplier),
             "converts C_B6 to the multiplier logarithm bound", "Phase H"),
        node("C_multiplier_factor", "exact_rational", ["C_defect_factor"],
             "2*C_defect_factor", q(exponential_multiplier),
             "sufficient K coefficient for |exp(E)-1|<=1", "Phase H"),
        node("N_0", "symbolic", ["N_explicit", "N_analytic"],
             "max(N_explicit,N_analytic)", None,
             "single eventual proof threshold", "Phase H"),
        node("K_finite", "symbolic", ["N_0"], "N_0^2*(N_0+2)+1", None,
             "dominates n^2*log(n+2) for every n<N_0", "Phase H"),
        node("K_final", "symbolic",
             ["K_geometry", "C_multiplier_factor", "C_B6", "K_finite"],
             "max(K_geometry,C_multiplier_factor*C_B6,K_finite)", None,
             "one sufficient existential theorem constant", "Phase H"),
    ]

    return {
        "version": 1,
        "arithmetic": "integers and fractions.Fraction; no binary floating point",
        "policy": (
            "A null value is mandatory for unresolved analytic constants and "
            "thresholds. Diagnostics are excluded from K_final."
        ),
        "nodes": nodes,
        "summary": {
            "fully_numeric_nodes": sum(item["value"] is not None for item in nodes),
            "symbolic_or_external_nodes": sum(item["value"] is None for item in nodes),
            "only_unresolved_constant": "C_B6",
            "only_unresolved_threshold": "N_analytic",
            "explicit_geometry_constant": str(k_geometry),
            "symbolic_final_constant": (
                "max(K_geometry,C_multiplier_factor*C_B6,"
                "N_0^2*(N_0+2)+1)"
            ),
            "effectivity_claim": "effective in principle; no useful numerical K claimed",
        },
    }


def validate_ledger(ledger: dict[str, Any]) -> None:
    if set(ledger) != {"version", "arithmetic", "policy", "nodes", "summary"}:
        raise AssertionError("effectivity ledger top-level keys changed")
    if ledger["version"] != 1 or "no binary floating point" not in ledger["arithmetic"]:
        raise AssertionError("effectivity arithmetic/version changed")
    nodes = ledger["nodes"]
    identifiers = [item["id"] for item in nodes]
    if len(identifiers) != len(set(identifiers)):
        raise AssertionError("duplicate effectivity node")
    known: set[str] = set()
    for item in nodes:
        if set(item) != {"id", "kind", "dependencies", "expression", "value", "role", "source"}:
            raise AssertionError(f"malformed effectivity node {item.get('id')}")
        if not set(item["dependencies"]) <= known:
            raise AssertionError(f"non-acyclic or unknown dependency at {item['id']}")
        known.add(item["id"])
    by_id = {item["id"]: item for item in nodes}
    if by_id["C_B6"]["value"] is not None or by_id["N_analytic"]["value"] is not None:
        raise AssertionError("unproved analytic input was assigned a number")
    if by_id["K_final"]["value"] is not None:
        raise AssertionError("symbolic final K was falsely made numerical")
    if "C_B6" not in by_id["K_final"]["dependencies"]:
        raise AssertionError("final K hides the sixth-derivative constant")
    if "K_finite" not in by_id["K_final"]["dependencies"]:
        raise AssertionError("final K hides the finite-range absorption")
    if ledger["summary"]["only_unresolved_constant"] != "C_B6":
        raise AssertionError("unresolved constant disclosure drifted")
    if ledger["summary"]["only_unresolved_threshold"] != "N_analytic":
        raise AssertionError("unresolved threshold disclosure drifted")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build_ledger()
    validate_ledger(expected)
    if args.check:
        actual = json.loads(FROZEN.read_text(encoding="utf-8"))
        validate_ledger(actual)
        if actual != expected:
            raise AssertionError("EFFECTIVITY_LEDGER.json is stale")
        print(
            "PASS Phase H effectivity ledger: exact DAG, explicit geometry K, "
            "symbolic final K, and honest analytic boundary"
        )
        return
    encoded = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
