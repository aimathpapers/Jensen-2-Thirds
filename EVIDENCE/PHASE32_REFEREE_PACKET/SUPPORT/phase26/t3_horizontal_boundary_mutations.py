#!/usr/bin/env python3
"""Fail-closed source mutations for the horizontal boundary estimates."""

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
    / "LeadingHorizontalBoundary.lean"
)


class ContractError(RuntimeError):
    """A required boundary connection is absent."""


def require(text: str, needle: str, label: str, count: int = 1) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count}, found {actual}")


def validate(text: str) -> None:
    checks = {
        "curvature-radius scale": ("125 ≤ ‖leadingCurvature", 1),
        "radius exponent": ("Kabs ^ (3 / 5 : ℝ)", 3),
        "phase gap theorem": (
            "theorem quantitativeSaddleBranch_horizontal_boundary_phase_gap\n",
            1,
        ),
        "phase gap constant": ("Kabs * ρ ^ 2 / 20", 1),
        "local expansion producer": (
            "quantitativeSaddleBranch_localExpansion_exact hs hrle",
            1,
        ),
        "cubic producer": (
            "quantitativeSaddleBranch_cubicCoefficient_norm_le hs",
            1,
        ),
        "quartic producer": (
            "quantitativeSaddleBranch_localRemainder_norm_le hs hrle",
            1,
        ),
        "quadratic curvature producer": (
            "quantitativeSaddleBranch_curvature_strong_bounds hs",
            1,
        ),
        "both endpoint theorem": (
            "theorem quantitativeSaddleBranch_horizontal_boundary_phase_gaps\n",
            1,
        ),
        "derivative sign theorem": (
            "theorem quantitativeSaddleBranch_horizontal_boundary_derivative_signs\n",
            1,
        ),
        "strict concavity producer": (
            "quantitativeSaddleBranch_horizontal_strictConcaveOn hs",
            1,
        ),
        "right derivative constant": (
            "deriv (leadingHorizontalRealLog s L) ρ < -(‖K‖ * ρ / 20)",
            1,
        ),
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
        print(f"PASS horizontal-boundary mutation rejected: {label}")
        return
    raise AssertionError(f"horizontal-boundary mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 horizontal-boundary source contract")
    cases = {
        "curvature-radius scale weakened": mutate(
            source, "125 ≤ ‖leadingCurvature", "12 ≤ ‖leadingCurvature"
        ),
        "radius exponent changed": mutate(
            source, "Kabs ^ (3 / 5 : ℝ)", "Kabs ^ (1 / 2 : ℝ)"
        ),
        "phase gap theorem removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_boundary_phase_gap\n",
            "theorem horizontal_boundary_phase_gap_unchecked\n",
        ),
        "phase drop weakened": mutate(
            source, "Kabs * ρ ^ 2 / 20", "Kabs * ρ ^ 2 / 21"
        ),
        "local expansion disconnected": mutate(
            source,
            "quantitativeSaddleBranch_localExpansion_exact hs hrle",
            "localExpansion_exact_unchecked hs hrle",
        ),
        "cubic bound disconnected": mutate(
            source,
            "quantitativeSaddleBranch_cubicCoefficient_norm_le hs",
            "cubicCoefficient_norm_le_unchecked hs",
        ),
        "quartic bound disconnected": mutate(
            source,
            "quantitativeSaddleBranch_localRemainder_norm_le hs hrle",
            "localRemainder_norm_le_unchecked hs hrle",
        ),
        "curvature comparison disconnected": mutate(
            source,
            "quantitativeSaddleBranch_curvature_strong_bounds hs",
            "curvature_strong_bounds_unchecked hs",
        ),
        "signed endpoint pair removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_boundary_phase_gaps\n",
            "theorem horizontal_boundary_phase_gaps_unchecked\n",
        ),
        "derivative signs removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_boundary_derivative_signs\n",
            "theorem horizontal_boundary_derivative_signs_unchecked\n",
        ),
        "concavity producer disconnected": mutate(
            source,
            "quantitativeSaddleBranch_horizontal_strictConcaveOn hs",
            "horizontal_strictConcaveOn_unchecked hs",
        ),
        "right derivative scale weakened": mutate(
            source,
            "deriv (leadingHorizontalRealLog s L) ρ < -(‖K‖ * ρ / 20)",
            "deriv (leadingHorizontalRealLog s L) ρ < 0",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)


if __name__ == "__main__":
    main()
