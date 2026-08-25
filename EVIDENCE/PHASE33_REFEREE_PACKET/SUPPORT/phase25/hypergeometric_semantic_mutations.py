#!/usr/bin/env python3
"""Fail-closed source mutations for the Lean terminating-3F2 producer."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT / "Kimi_Agent_Riemann Lean Exploration" / "zeta-23-lean" / "Zeta23"
    / "Research" / "JensenWedge" / "TerminatingHypergeometric.lean"
)


class ContractError(RuntimeError):
    pass


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise ContractError(f"{label}: expected once, found {count}")


def validate(text: str) -> None:
    checks = {
        "finite polynomial": "theorem coeff_terminating3F2Polynomial",
        "termination": "theorem terminating3F2Coefficient_eq_zero_of_degree_lt",
        "coefficient ratio": "theorem terminating3F2Coefficient_ratio_cross",
        "Euler ODE": "theorem terminating3F2_euler_ode",
        "shifted ODE": "theorem terminating3F2_shifted_euler_ode",
        "derivative coefficient": "theorem terminating3F2_derivative_shift_coefficient",
        "derivative polynomial": "theorem iterate_derivative_terminating3F2Polynomial",
        "genuine recurrence": "theorem terminating3F2_shifted_fourTerm_recurrence",
        "coefficient match": "theorem hypergeometricOdeCoefficients_match_directRecurrence",
        "lambda scale": "hypergeometricOdeP3 (D / (A * C)) y = recurrenceP3 A C D y := by",
        "shifted degree": "Polynomial.C (terminating3F2DerivativePrefactor d m A B C D lambda) *\n        terminating3F2Polynomial (d - m)",
        "third coefficient": "1 + shifted3F2E1 A C d m + shifted3F2E2 A C d m",
        "zeroth coefficient": "-lambda * y * shifted3F2E3 A C d m",
    }
    for label, needle in checks.items():
        require_once(text, needle, label)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS hypergeometric mutation rejected: {label}")
        return
    raise AssertionError(f"hypergeometric mutation survived: {label}")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    validate(text)
    print("PASS terminating 3F2 source contract")
    mutations = {
        "lambda scale transposed": (
            "hypergeometricOdeP3 (D / (A * C)) y = recurrenceP3 A C D y := by",
            "hypergeometricOdeP3 (A * C / D) y = recurrenceP3 A C D y := by",
        ),
        "derivative degree unshifted": (
            "Polynomial.C (terminating3F2DerivativePrefactor d m A B C D lambda) *\n        terminating3F2Polynomial (d - m)",
            "Polynomial.C (terminating3F2DerivativePrefactor d m A B C D lambda) *\n        terminating3F2Polynomial d",
        ),
        "Euler constant dropped": (
            "1 + shifted3F2E1 A C d m + shifted3F2E2 A C d m",
            "shifted3F2E1 A C d m + shifted3F2E2 A C d m",
        ),
        "zeroth sign flipped": (
            "-lambda * y * shifted3F2E3 A C d m",
            "lambda * y * shifted3F2E3 A C d m",
        ),
        "finite producer disconnected": (
            "theorem terminating3F2_shifted_fourTerm_recurrence",
            "theorem assumed_shifted_fourTerm_recurrence",
        ),
    }
    for label, (old, new) in mutations.items():
        require_once(text, old, f"mutation target {label}")
        expect_rejected(label, text.replace(old, new, 1))
    print("PASS all terminating 3F2 semantic mutations")


if __name__ == "__main__":
    main()
