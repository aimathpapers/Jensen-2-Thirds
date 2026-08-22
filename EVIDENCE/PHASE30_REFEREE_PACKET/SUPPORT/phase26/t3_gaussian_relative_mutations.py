#!/usr/bin/env python3
"""Fail-closed mutations for the T3 Gaussian relative normalization."""

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
    / "LeadingGaussianRelative.lean"
)


class ContractError(RuntimeError):
    """A load-bearing relative-normalization connection is absent."""


def require_count(text: str, needle: str, count: int, label: str) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count} occurrences, found {actual}")


def validate(text: str) -> None:
    checks = {
        "main lower theorem": (
            "theorem norm_integral_leadingGaussian_lower\n",
            1,
        ),
        "exact Gaussian producer": ("integral_leadingGaussian hK", 1),
        "complex-power norm": ("Complex.norm_cpow_real", 1),
        "main scale": ("‖K‖ ^ (-(1 / 2 : ℝ))", 4),
        "signed cubic formula": ("3 / K ^ 2 + 1 / K ^ 3", 4),
        "relative constant four": ("(4 / ‖K‖) *", 3),
        "cubic coefficient producer": (
            "quantitativeSaddleBranch_cubicCoefficient_norm_le hs",
            1,
        ),
        "curvature threshold producer": (
            "quantitativeSaddleBranch_curvature_norm_ge_fourThousand hs",
            1,
        ),
        "branch relative theorem": (
            "theorem quantitativeSaddleBranch_cubicGaussian_relative_error_le\n",
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
        print(f"PASS Gaussian-relative mutation rejected: {label}")
        return
    raise AssertionError(f"Gaussian-relative mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 Gaussian relative-normalization source contract")
    cases = {
        "main lower theorem disconnected": mutate(
            source,
            "theorem norm_integral_leadingGaussian_lower\n",
            "theorem norm_integral_leadingGaussian_lower_unchecked\n",
        ),
        "exact Gaussian producer disconnected": mutate(
            source,
            "integral_leadingGaussian hK",
            "integral_leadingGaussian_unchecked hK",
        ),
        "complex power norm disconnected": mutate(
            source,
            "Complex.norm_cpow_real",
            "Complex.norm_cpow_branch_unchecked",
        ),
        "signed correction changed": mutate(
            source,
            "3 / K ^ 2 + 1 / K ^ 3",
            "3 / K ^ 2 - 1 / K ^ 3",
            count=4,
        ),
        "relative constant weakened": mutate(
            source,
            "(4 / ‖K‖) *",
            "(5 / ‖K‖) *",
            count=3,
        ),
        "coefficient certificate disconnected": mutate(
            source,
            "quantitativeSaddleBranch_cubicCoefficient_norm_le hs",
            "quantitativeSaddleBranch_cubicCoefficient_norm_le_unchecked hs",
        ),
        "curvature threshold disconnected": mutate(
            source,
            "quantitativeSaddleBranch_curvature_norm_ge_fourThousand hs",
            "quantitativeSaddleBranch_curvature_norm_ge_fourThousand_unchecked hs",
        ),
        "branch theorem disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_cubicGaussian_relative_error_le\n",
            "theorem quantitativeSaddleBranch_cubicGaussian_relative_error_le_unchecked\n",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print(f"PASS Gaussian-relative semantic mutations: {len(cases)} rejected")


if __name__ == "__main__":
    main()
