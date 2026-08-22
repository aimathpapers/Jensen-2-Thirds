#!/usr/bin/env python3
"""Fail-closed mutations for the signed T3 Gaussian-moment layer."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration"
    / "zeta-23-lean"
    / "Zeta23"
    / "Research"
    / "JensenWedge"
    / "LeadingGaussianMoments.lean"
)


class ContractError(RuntimeError):
    """A load-bearing Gaussian-moment connection is absent or ambiguous."""


def require_count(text: str, needle: str, count: int, label: str) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count} occurrences, found {actual}")


def validate(text: str) -> None:
    checks = {
        "signed moment definition": (
            "∫ r : ℝ, (r : ℂ) ^ n * leadingGaussian K r"
        ),
        "all polynomial moments integrable": (
            "theorem integrable_pow_mul_leadingGaussian\n"
        ),
        "absolute Gaussian moment integrable": (
            "theorem integrable_abs_pow_mul_exp_neg_mul_sq\n"
        ),
        "exact absolute Gaussian moment": (
            "theorem integral_abs_pow_mul_exp_neg_mul_sq\n"
        ),
        "uniform absolute moment bound": (
            "theorem integral_norm_pow_mul_leadingGaussian_le\n"
        ),
        "fourth absolute moment": (
            "theorem integral_norm_fourth_mul_leadingGaussian_le\n"
        ),
        "fourth moment exponent": (
            "(K.re / 4) ^ (-(5 : ℝ) / 2)"
        ),
        "sixth absolute moment": (
            "theorem integral_norm_sixth_mul_leadingGaussian_le\n"
        ),
        "sixth moment exponent": (
            "(K.re / 4) ^ (-(7 : ℝ) / 2)"
        ),
        "whole-line integration by parts": (
            "integral_eq_zero_of_hasDerivAt_of_integrable"
        ),
        "signed cubic formula": (
            "leadingGaussianMoment K 0 * (3 / K ^ 2 + 1 / K ^ 3) := by"
        ),
        "normalized cubic ratio": (
            "(∫ r : ℝ, leadingGaussian K r) = 3 / K ^ 2 + 1 / K ^ 3 := by"
        ),
    }
    for label, needle in checks.items():
        require_count(text, needle, 3 if label == "whole-line integration by parts" else 1, label)


def mutate(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise AssertionError(f"mutation source is not unique: {old!r}")
    return text.replace(old, new, 1)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS Gaussian-moment mutation rejected: {label}")
        return
    raise AssertionError(f"Gaussian-moment mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS signed T3 Gaussian-moment source contract")
    cases = {
        "moment integrability disconnected": mutate(
            source,
            "theorem integrable_pow_mul_leadingGaussian\n",
            "theorem integrable_pow_mul_leadingGaussian_unchecked\n",
        ),
        "absolute-moment formula disconnected": mutate(
            source,
            "theorem integral_abs_pow_mul_exp_neg_mul_sq\n",
            "theorem integral_abs_pow_mul_exp_neg_mul_sq_unchecked\n",
        ),
        "uniform absolute bound disconnected": mutate(
            source,
            "theorem integral_norm_pow_mul_leadingGaussian_le\n",
            "theorem integral_norm_pow_mul_leadingGaussian_le_unchecked\n",
        ),
        "fourth-moment exponent weakened": mutate(
            source,
            "(K.re / 4) ^ (-(5 : ℝ) / 2)",
            "(K.re / 4) ^ (-(3 : ℝ) / 2)",
        ),
        "sixth-moment exponent weakened": mutate(
            source,
            "(K.re / 4) ^ (-(7 : ℝ) / 2)",
            "(K.re / 4) ^ (-(5 : ℝ) / 2)",
        ),
        "cubic coefficient changed": mutate(
            source,
            "leadingGaussianMoment K 0 * (3 / K ^ 2 + 1 / K ^ 3) := by",
            "leadingGaussianMoment K 0 * (1 / K ^ 2 + 1 / K ^ 3) := by",
        ),
        "cubic correction sign reversed": mutate(
            source,
            "(∫ r : ℝ, leadingGaussian K r) = 3 / K ^ 2 + 1 / K ^ 3 := by",
            "(∫ r : ℝ, leadingGaussian K r) = 3 / K ^ 2 - 1 / K ^ 3 := by",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print(f"PASS Gaussian-moment semantic mutations: {len(cases)} rejected")


if __name__ == "__main__":
    main()
