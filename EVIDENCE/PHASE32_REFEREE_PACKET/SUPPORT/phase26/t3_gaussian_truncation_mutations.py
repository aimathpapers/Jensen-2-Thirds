#!/usr/bin/env python3
"""Fail-closed mutations for the T3 cubic-Gaussian truncation seam."""

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
    / "LeadingGaussianTruncation.lean"
)


class ContractError(RuntimeError):
    """A load-bearing Gaussian-truncation connection is absent."""


def require_count(text: str, needle: str, count: int, label: str) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count} occurrences, found {actual}")


def validate(text: str) -> None:
    checks = {
        "generic tail theorem": (
            "theorem leadingGaussian_tail_moment_le_higher\n",
            1,
        ),
        "higher-moment scale": (
            "(ρ ^ m)⁻¹ *\n        (\u222b r : ℝ, ‖(r : ℂ) ^ (k + m) * leadingGaussian K r‖)",
            2,
        ),
        "exact signed cubic correction": (
            "(1 + c * (3 / K ^ 2 + 1 / K ^ 3)) := by",
            1,
        ),
        "zeroth-to-tenth tail": (
            "leadingGaussian_tail_moment_le_higher hK hρ 0 10",
            1,
        ),
        "cubic-to-eighth tail": (
            "leadingGaussian_tail_moment_le_higher hK hρ 3 5",
            1,
        ),
        "tenth moment output": (
            "(r : ℂ) ^ 10 * leadingGaussian K r",
            4,
        ),
        "eighth moment output": (
            "(r : ℂ) ^ 8 * leadingGaussian K r",
            4,
        ),
        "complement decomposition": (
            "integral_add_compl measurableSet_Icc hF",
            1,
        ),
        "truncation theorem": (
            "theorem leadingCubicGaussianApproximation_truncation_error_le\n",
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
        print(f"PASS Gaussian-truncation mutation rejected: {label}")
        return
    raise AssertionError(f"Gaussian-truncation mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 cubic-Gaussian truncation source contract")
    cases = {
        "generic tail producer disconnected": mutate(
            source,
            "theorem leadingGaussian_tail_moment_le_higher\n",
            "theorem leadingGaussian_tail_moment_le_higher_unchecked\n",
        ),
        "moment scale disconnected": mutate(
            source,
            "(ρ ^ m)⁻¹ *\n        (\u222b r : ℝ, ‖(r : ℂ) ^ (k + m) * leadingGaussian K r‖)",
            "(ρ ^ (m + 1))⁻¹ *\n        (\u222b r : ℝ, ‖(r : ℂ) ^ (k + m) * leadingGaussian K r‖)",
            count=2,
        ),
        "signed correction changed": mutate(
            source,
            "(1 + c * (3 / K ^ 2 + 1 / K ^ 3)) := by",
            "(1 + c * (3 / K ^ 2)) := by",
        ),
        "zeroth tail order weakened": mutate(
            source,
            "leadingGaussian_tail_moment_le_higher hK hρ 0 10",
            "leadingGaussian_tail_moment_le_higher hK hρ 0 9",
        ),
        "cubic tail order weakened": mutate(
            source,
            "leadingGaussian_tail_moment_le_higher hK hρ 3 5",
            "leadingGaussian_tail_moment_le_higher hK hρ 3 4",
        ),
        "complement seam disconnected": mutate(
            source,
            "integral_add_compl measurableSet_Icc hF",
            "integral_add_compl_unchecked measurableSet_Icc hF",
        ),
        "truncation conclusion disconnected": mutate(
            source,
            "theorem leadingCubicGaussianApproximation_truncation_error_le\n",
            "theorem leadingCubicGaussianApproximation_truncation_error_le_unchecked\n",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print(f"PASS Gaussian-truncation semantic mutations: {len(cases)} rejected")


if __name__ == "__main__":
    main()
