#!/usr/bin/env python3
"""Fail-closed mutations for relative horizontal-tail normalization."""

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
    / "LeadingHorizontalRelative.lean"
)


class ContractError(RuntimeError):
    """A required relative-normalization connection is absent."""


def require(text: str, needle: str, label: str, count: int = 1) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count}, found {actual}")


def validate(text: str) -> None:
    checks = {
        "amplitude theorem": (
            "theorem quantitativeSaddleBranch_amplitude_le_gaussianMain_scale\n",
            1,
        ),
        "Gaussian lower producer": (
            "quantitativeSaddleBranch_norm_integral_leadingGaussian_lower hs",
            1,
        ),
        "half-power cancellation": (
            "‖K‖ ^ (1 / 2 : ℝ) * ‖K‖ ^ (-(1 / 2 : ℝ)) = 1",
            1,
        ),
        "relative tail theorem": (
            "theorem quantitativeSaddleBranch_horizontal_tail_relative_bound\n",
            1,
        ),
        "integrated tail producer": (
            "quantitativeSaddleBranch_horizontal_tail_integral_bounds hs",
            1,
        ),
        "amplitude producer": (
            "quantitativeSaddleBranch_amplitude_le_gaussianMain_scale hs",
            1,
        ),
        "explicit relative coefficient": (
            "((L.re + 20 / (‖K‖ * ρ)) *\n          Real.exp (-(‖K‖ * ρ ^ 2 / 20)) * ‖K‖ ^ (1 / 2 : ℝ))",
            1,
        ),
        "exact Gaussian main": ("‖leadingIntegrand s L * M‖", 6),
    }
    for label, (needle, count) in checks.items():
        require(text, needle, label, count)


def mutate(text: str, old: str, new: str) -> str:
    if old not in text:
        raise AssertionError(f"missing mutation source: {old!r}")
    return text.replace(old, new, 1)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS horizontal-relative mutation rejected: {label}")
        return
    raise AssertionError(f"horizontal-relative mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 relative horizontal-tail source contract")
    cases = {
        "amplitude theorem removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_amplitude_le_gaussianMain_scale\n",
            "theorem amplitude_le_gaussianMain_unchecked\n",
        ),
        "Gaussian lower disconnected": mutate(
            source,
            "quantitativeSaddleBranch_norm_integral_leadingGaussian_lower hs",
            "norm_integral_gaussian_lower_unchecked hs",
        ),
        "half-power cancellation changed": mutate(
            source,
            "‖K‖ ^ (1 / 2 : ℝ) * ‖K‖ ^ (-(1 / 2 : ℝ)) = 1",
            "‖K‖ ^ (1 / 2 : ℝ) * ‖K‖ ^ (-(1 / 2 : ℝ)) ≤ 1",
        ),
        "relative theorem removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_tail_relative_bound\n",
            "theorem horizontal_tail_relative_bound_unchecked\n",
        ),
        "integrated tails disconnected": mutate(
            source,
            "quantitativeSaddleBranch_horizontal_tail_integral_bounds hs",
            "horizontal_tail_integral_bounds_unchecked hs",
        ),
        "amplitude producer disconnected": mutate(
            source,
            "quantitativeSaddleBranch_amplitude_le_gaussianMain_scale hs",
            "amplitude_le_gaussianMain_unchecked hs",
        ),
        "relative coefficient altered": mutate(
            source,
            "((L.re + 20 / (‖K‖ * ρ)) *\n          Real.exp (-(‖K‖ * ρ ^ 2 / 20)) * ‖K‖ ^ (1 / 2 : ℝ))",
            "((L.re + 20 / (‖K‖ * ρ)) * ‖K‖ ^ (1 / 2 : ℝ))",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)


if __name__ == "__main__":
    main()
