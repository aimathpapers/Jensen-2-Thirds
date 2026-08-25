#!/usr/bin/env python3
"""Fail-closed source mutations for the effective integer Stirling transport."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/FactorialRatioStirling.lean"
)


class ContractError(RuntimeError):
    """The concrete factorial-ratio Stirling contract is absent or ambiguous."""


def validate(text: str) -> None:
    required = {
        "Robbins producer": "Stirling.log_stirlingSeq_sdiff_le (n + k)",
        "Stirling limit producer": "Stirling.tendsto_stirlingSeq_sqrt_pi.comp",
        "telescoped log rate":
            "theorem log_stirlingSeq_sub_limit_le",
        "log constant": "1 / (12 * (n : ℝ))",
        "normalized correction": "def factorialStirlingCorrection",
        "correction floor": "theorem one_le_factorialStirlingCorrection",
        "correction rate":
            "theorem abs_factorialStirlingCorrection_sub_one_le",
        "single-factor constant": "1 / (6 * (n : ℝ))",
        "ratio correction": "def factorialRatioCorrection",
        "ratio rate": "theorem abs_factorialRatioCorrection_sub_one_le",
        "ratio constant": "1 / (4 * (M : ℝ))",
        "traditional main": "def hollandFactorialRatioMain",
        "traditional main identity":
            "theorem factorialRatioElementaryMain_eq_holland",
        "exact quotient factorization":
            "theorem factorial_ratio_eq_elementaryMain_mul_correction",
        "relative-error producer": "theorem factorial_ratio_relative_error",
        "real factorial scope": "(M.factorial : ℝ) / ((2 * M).factorial : ℝ)",
    }
    expected_counts = {
        "log constant": 6,
        "single-factor constant": 3,
        "ratio constant": 3,
        "real factorial scope": 2,
    }
    for label, needle in required.items():
        if text.count(needle) != expected_counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 effective integer Stirling source contract")
    mutations = {
        "Robbins producer disconnected": (
            "Stirling.log_stirlingSeq_sdiff_le (n + k)",
            "unchecked_robbins_step (n + k)",
        ),
        "Stirling limit disconnected": (
            "Stirling.tendsto_stirlingSeq_sqrt_pi.comp",
            "unchecked_stirling_limit.comp",
        ),
        "log rate weakened": (
            "1 / (12 * (n : ℝ))",
            "1 / (11 * (n : ℝ))",
        ),
        "single correction weakened": (
            "1 / (6 * (n : ℝ))",
            "1 / (5 * (n : ℝ))",
        ),
        "ratio correction weakened": (
            "1 / (4 * (M : ℝ))",
            "1 / (3 * (M : ℝ))",
        ),
        "traditional form removed": (
            "theorem factorialRatioElementaryMain_eq_holland",
            "theorem traditional_form_unchecked",
        ),
        "quotient factorization removed": (
            "theorem factorial_ratio_eq_elementaryMain_mul_correction",
            "theorem factorial_ratio_factorization_unchecked",
        ),
        "integer quotient changed": (
            "(M.factorial : ℝ) / ((2 * M).factorial : ℝ)",
            "(M.factorial : ℝ) / ((2 * M + 1).factorial : ℝ)",
        ),
        "relative error removed": (
            "theorem factorial_ratio_relative_error",
            "theorem factorial_ratio_error_unchecked",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 factorial Stirling mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
