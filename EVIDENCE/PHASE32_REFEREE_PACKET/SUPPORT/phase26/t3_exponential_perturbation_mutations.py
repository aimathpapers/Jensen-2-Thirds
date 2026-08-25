#!/usr/bin/env python3
"""Fail-closed mutations for the exponentiated T3 local perturbation."""

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
    / "LeadingExponentialPerturbation.lean"
)


class ContractError(RuntimeError):
    """A load-bearing exponential-perturbation connection is absent."""


def require_count(text: str, needle: str, count: int, label: str) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count} occurrences, found {actual}")


def validate(text: str) -> None:
    checks = {
        "cubic coefficient theorem": (
            "theorem quantitativeSaddleBranch_cubicCoefficient_norm_le\n",
            1,
        ),
        "cubic coefficient curvature bound": (
            "‖leadingCubicCoefficient s (quantitativeSaddleBranch s)‖ ≤\n"
            "      ‖leadingCurvature s (quantitativeSaddleBranch s)‖ := by",
            1,
        ),
        "exact factorization": (
            "theorem quantitativeSaddleBranch_localFactorization\n",
            1,
        ),
        "complex exponential remainder": (
            "Complex.norm_exp_sub_one_sub_id_le hzOne",
            1,
        ),
        "central smallness guard": (
            "‖leadingCurvature s (quantitativeSaddleBranch s)‖ * |r| ^ 3 ≤ 1 / 2",
            2,
        ),
        "quartic and squared-cubic error": (
            "6 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ * |r| ^ 4 +\n"
            "        4 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ ^ 2 * |r| ^ 6",
            1,
        ),
        "pointwise integrand comparison": (
            "theorem quantitativeSaddleBranch_integrand_sub_cubicGaussian_norm_le\n",
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
        print(f"PASS exponential-perturbation mutation rejected: {label}")
        return
    raise AssertionError(f"exponential-perturbation mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS exponentiated T3 perturbation source contract")
    cases = {
        "cubic curvature bound weakened": mutate(
            source,
            "‖leadingCubicCoefficient s (quantitativeSaddleBranch s)‖ ≤\n"
            "      ‖leadingCurvature s (quantitativeSaddleBranch s)‖ := by",
            "‖leadingCubicCoefficient s (quantitativeSaddleBranch s)‖ ≤\n"
            "      2 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ := by",
        ),
        "factorization disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_localFactorization\n",
            "theorem quantitativeSaddleBranch_localFactorization_unchecked\n",
        ),
        "exponential remainder disconnected": mutate(
            source,
            "Complex.norm_exp_sub_one_sub_id_le hzOne",
            "Complex.norm_exp_sub_one_sub_id_unchecked hzOne",
        ),
        "central smallness weakened": mutate(
            source,
            "‖leadingCurvature s (quantitativeSaddleBranch s)‖ * |r| ^ 3 ≤ 1 / 2",
            "‖leadingCurvature s (quantitativeSaddleBranch s)‖ * |r| ^ 3 ≤ 1",
            count=2,
        ),
        "quartic order weakened": mutate(
            source,
            "6 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ * |r| ^ 4 +\n"
            "        4 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ ^ 2 * |r| ^ 6",
            "6 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ * |r| ^ 3 +\n"
            "        4 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ ^ 2 * |r| ^ 6",
        ),
        "pointwise comparison disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_integrand_sub_cubicGaussian_norm_le\n",
            "theorem quantitativeSaddleBranch_integrand_sub_cubicGaussian_norm_le_unchecked\n",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print(f"PASS exponential-perturbation semantic mutations: {len(cases)} rejected")


if __name__ == "__main__":
    main()
