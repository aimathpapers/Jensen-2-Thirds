#!/usr/bin/env python3
"""Fail-closed mutations for the concrete T3 central window."""

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
    / "LeadingCentralWindow.lean"
)


class ContractError(RuntimeError):
    """A load-bearing central-window connection is absent."""


def require_count(text: str, needle: str, count: int, label: str) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count} occurrences, found {actual}")


def validate(text: str) -> None:
    checks = {
        "paper radius": (
            "def leadingCentralRadius (K : ℂ) : ℝ :=\n  ‖K‖ ^ (-(2 / 5 : ℝ))",
            1,
        ),
        "curvature lower bound": (
            "4000 ≤ ‖leadingCurvature s (quantitativeSaddleBranch s)‖ := by",
            1,
        ),
        "Taylor-radius theorem": (
            "theorem quantitativeSaddleBranch_centralRadius_le_tenth\n",
            1,
        ),
        "cubic smallness theorem": (
            "theorem quantitativeSaddleBranch_curvature_mul_centralRadius_cube_le_half\n",
            1,
        ),
        "pointwise producer": (
            "quantitativeSaddleBranch_centralWindow_pointwise hs habs",
            1,
        ),
        "fourth moment integrability": (
            "integrable_pow_mul_leadingGaussian hKre 4",
            1,
        ),
        "sixth moment integrability": (
            "integrable_pow_mul_leadingGaussian hKre 6",
            1,
        ),
        "restricted-to-whole integral": (
            "setIntegral_le_integral hG (Eventually.of_forall hnonneg)",
            1,
        ),
        "integrated error theorem": (
            "theorem quantitativeSaddleBranch_centralWindow_integral_error_le\n",
            1,
        ),
    }
    for label, (needle, count) in checks.items():
        require_count(text, needle, count, label)


def mutate(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise AssertionError(f"mutation source is not unique: {old!r}")
    return text.replace(old, new, 1)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS central-window mutation rejected: {label}")
        return
    raise AssertionError(f"central-window mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS concrete T3 central-window source contract")
    cases = {
        "radius exponent changed": mutate(
            source,
            "def leadingCentralRadius (K : ℂ) : ℝ :=\n  ‖K‖ ^ (-(2 / 5 : ℝ))",
            "def leadingCentralRadius (K : ℂ) : ℝ :=\n  ‖K‖ ^ (-(1 / 3 : ℝ))",
        ),
        "curvature lower bound weakened": mutate(
            source,
            "4000 ≤ ‖leadingCurvature s (quantitativeSaddleBranch s)‖ := by",
            "1000 ≤ ‖leadingCurvature s (quantitativeSaddleBranch s)‖ := by",
        ),
        "Taylor radius disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_centralRadius_le_tenth\n",
            "theorem quantitativeSaddleBranch_centralRadius_le_tenth_unchecked\n",
        ),
        "cubic smallness disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_curvature_mul_centralRadius_cube_le_half\n",
            "theorem quantitativeSaddleBranch_curvature_mul_centralRadius_cube_le_half_unchecked\n",
        ),
        "pointwise producer disconnected": mutate(
            source,
            "quantitativeSaddleBranch_centralWindow_pointwise hs habs",
            "quantitativeSaddleBranch_centralWindow_pointwise_unchecked hs habs",
        ),
        "fourth moment disconnected": mutate(
            source,
            "integrable_pow_mul_leadingGaussian hKre 4",
            "integrable_pow_mul_leadingGaussian hKre 3",
        ),
        "sixth moment disconnected": mutate(
            source,
            "integrable_pow_mul_leadingGaussian hKre 6",
            "integrable_pow_mul_leadingGaussian hKre 5",
        ),
        "whole-line domination disconnected": mutate(
            source,
            "setIntegral_le_integral hG (Eventually.of_forall hnonneg)",
            "setIntegral_le_integral_unchecked hG (Eventually.of_forall hnonneg)",
        ),
        "integrated error disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_centralWindow_integral_error_le\n",
            "theorem quantitativeSaddleBranch_centralWindow_integral_error_le_unchecked\n",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print(f"PASS central-window semantic mutations: {len(cases)} rejected")


if __name__ == "__main__":
    main()
