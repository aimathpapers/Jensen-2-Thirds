#!/usr/bin/env python3
"""Fail-closed mutations for the relative T3 central Gaussian theorem."""

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
    / "LeadingCentralRelative.lean"
)


class ContractError(RuntimeError):
    """A relative central-Gaussian connection is absent."""


def require_count(text: str, needle: str, count: int, label: str) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count} occurrences, found {actual}")


def validate(text: str) -> None:
    checks = {
        "local ledger constant": (
            "286720 * ‖K‖ ^ (-(3 / 2 : ℝ))",
            3,
        ),
        "truncation ledger constant": (
            "69206016 * ‖K‖ ^ (-(3 / 2 : ℝ))",
            3,
        ),
        "radius tenth inverse": ("(ρ ^ 10)⁻¹ = ‖K‖ ^ (4 : ℝ)", 1),
        "radius fifth inverse": ("(ρ ^ 5)⁻¹ = ‖K‖ ^ (2 : ℝ)", 1),
        "local producer": (
            "quantitativeSaddleBranch_centralWindow_integral_error_le hs",
            1,
        ),
        "truncation producer": (
            "leadingCubicGaussianApproximation_truncation_error_le",
            1,
        ),
        "signed cubic producer": (
            "quantitativeSaddleBranch_cubicGaussian_relative_error_le hs",
            1,
        ),
        "main lower producer": (
            "quantitativeSaddleBranch_norm_integral_leadingGaussian_lower hs",
            1,
        ),
        "integral subtraction": ("integral_sub hFint hconst", 1),
        "exact three-piece decomposition": (
            "(I - g * AC) + g * (AC - AW) + g * (AW - M)",
            2,
        ),
        "final relative constant": ("(71000000 / ‖K‖) *", 3),
        "final theorem": (
            "theorem quantitativeSaddleBranch_centralGaussian_relative_error_le\n",
            1,
        ),
    }
    for label, (needle, count) in checks.items():
        require_count(text, needle, count, label)


def mutate(text: str, old: str, new: str, count: int = 1) -> str:
    if text.count(old) != count:
        raise AssertionError(f"mutation source count is not {count}: {old!r}")
    return text.replace(old, new, 1)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS central-relative mutation rejected: {label}")
        return
    raise AssertionError(f"central-relative mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 relative central-Gaussian source contract")
    cases = {
        "local ledger constant changed": mutate(
            source,
            "286720 * ‖K‖ ^ (-(3 / 2 : ℝ))",
            "286719 * ‖K‖ ^ (-(3 / 2 : ℝ))",
            count=3,
        ),
        "truncation ledger constant changed": mutate(
            source,
            "69206016 * ‖K‖ ^ (-(3 / 2 : ℝ))",
            "69206015 * ‖K‖ ^ (-(3 / 2 : ℝ))",
            count=3,
        ),
        "tenth radius power changed": mutate(
            source,
            "(ρ ^ 10)⁻¹ = ‖K‖ ^ (4 : ℝ)",
            "(ρ ^ 9)⁻¹ = ‖K‖ ^ (4 : ℝ)",
        ),
        "fifth radius power changed": mutate(
            source,
            "(ρ ^ 5)⁻¹ = ‖K‖ ^ (2 : ℝ)",
            "(ρ ^ 4)⁻¹ = ‖K‖ ^ (2 : ℝ)",
        ),
        "local producer disconnected": mutate(
            source,
            "quantitativeSaddleBranch_centralWindow_integral_error_le hs",
            "quantitativeSaddleBranch_centralWindow_error_unchecked hs",
        ),
        "truncation producer disconnected": mutate(
            source,
            "leadingCubicGaussianApproximation_truncation_error_le",
            "leadingCubicGaussianApproximation_tail_unchecked",
        ),
        "signed cubic producer disconnected": mutate(
            source,
            "quantitativeSaddleBranch_cubicGaussian_relative_error_le hs",
            "quantitativeSaddleBranch_cubic_relative_unchecked hs",
        ),
        "main lower producer disconnected": mutate(
            source,
            "quantitativeSaddleBranch_norm_integral_leadingGaussian_lower hs",
            "quantitativeSaddleBranch_main_lower_unchecked hs",
        ),
        "integral subtraction disconnected": mutate(
            source,
            "integral_sub hFint hconst",
            "integral_sub_unchecked hFint hconst",
        ),
        "three-piece decomposition changed": mutate(
            source,
            "(I - g * AC) + g * (AC - AW) + g * (AW - M)",
            "(I - g * AC) + g * (AC - AW)",
            count=2,
        ),
        "relative constant changed": mutate(
            source,
            "(71000000 / ‖K‖) *",
            "(70000000 / ‖K‖) *",
            count=3,
        ),
        "final theorem disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_centralGaussian_relative_error_le\n",
            "theorem quantitativeSaddleBranch_centralGaussian_relative_error_le_unchecked\n",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print(f"PASS central-relative semantic mutations: {len(cases)} rejected")


if __name__ == "__main__":
    main()
