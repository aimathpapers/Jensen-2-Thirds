#!/usr/bin/env python3
"""Fail closed on the genuine terminating-polynomial radius adapter."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge/Terminating3F2CriticalRadius.lean"
)


class ContractError(RuntimeError):
    """The terminating critical-radius source contract changed."""


REQUIRED = {
    "literal normalized derivative ratio": (
        "polynomialEulerJet p y k / p.eval y"
    ),
    "derivative shift producer": (
        "iterate_derivative_terminating3F2Polynomial"
    ),
    "Euler ODE recurrence producer": (
        "terminating3F2_shifted_fourTerm_recurrence"
    ),
    "coefficient identification": (
        "hypergeometricOdeCoefficients_match_directRecurrence"
    ),
    "actual normalized recurrence": (
        "theorem terminating3F2_polynomialDerivativeRatio_fourTerm"
    ),
    "finite degree termination": "Polynomial.iterate_derivative_eq_zero",
    "critical first jet": "polynomialDerivativeRatio_one_of_critical",
    "genuine certificate constructor": (
        "noncomputable def terminating3F2CriticalRadiusCertificate"
    ),
    "exact recurrence consumer": (
        "terminating3F2_polynomialDerivativeRatio_fourTerm hm hA hC hB hD"
    ),
    "complete radius consumer": (
        ").derivative_radius"
    ),
}


def validate(source: str) -> None:
    for label, needle in REQUIRED.items():
        if needle not in source:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS genuine terminating critical-radius adapter source contract")
    mutations = {
        "normalizing denominator removed": (
            "polynomialEulerJet p y k / p.eval y",
            "polynomialEulerJet p y k",
        ),
        "derivative shift disconnected": (
            "iterate_derivative_terminating3F2Polynomial",
            "uncheckedDerivativeShift",
        ),
        "ODE recurrence disconnected": (
            "terminating3F2_shifted_fourTerm_recurrence",
            "uncheckedFourTermRecurrence",
        ),
        "coefficient match disconnected": (
            "hypergeometricOdeCoefficients_match_directRecurrence",
            "uncheckedCoefficientMatch",
        ),
        "normalized recurrence hidden": (
            "theorem terminating3F2_polynomialDerivativeRatio_fourTerm",
            "theorem uncheckedNormalizedFourTerm",
        ),
        "termination disconnected": (
            "Polynomial.iterate_derivative_eq_zero",
            "uncheckedDerivativeTermination",
        ),
        "critical base case hidden": (
            "polynomialDerivativeRatio_one_of_critical",
            "uncheckedCriticalFirstJet",
        ),
        "certificate constructor hidden": (
            "noncomputable def terminating3F2CriticalRadiusCertificate",
            "noncomputable def uncheckedCriticalRadiusCertificate",
        ),
        "recurrence consumer bypassed": (
            "terminating3F2_polynomialDerivativeRatio_fourTerm hm hA hC hB hD",
            "uncheckedNormalizedFourTerm hm hA hC hB hD",
        ),
        "radius theorem disconnected": (
            ").derivative_radius",
            ").uncheckedDerivativeRadius",
        ),
    }
    for label, (old, new) in mutations.items():
        if old not in source:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS terminating-radius mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
