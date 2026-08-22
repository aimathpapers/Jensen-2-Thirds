#!/usr/bin/env python3
"""Fail-closed source mutations for the exact Phase-26 T3 contour layer."""

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
    / "LeadingSaddleContour.lean"
)


class ContractError(RuntimeError):
    """A load-bearing T3 source connection is absent or ambiguous."""


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise ContractError(f"{label}: expected exactly one occurrence, found {count}")


def validate(text: str) -> None:
    checks = {
        "published phase": (
            "def leadingPhase (s u : ℂ) : ℂ :=\n"
            "  s * log u - (3 / 4) * u - (Real.pi : ℂ) * exp u"
        ),
        "Jacobian factor": (
            "def leadingIntegrand (s u : ℂ) : ℂ :=\n"
            "  exp u * exp (leadingPhase s u)"
        ),
        "full logarithmic integrand": (
            "def leadingLogIntegrand (s u : ℂ) : ℂ :=\n"
            "  s * log u + u / 4 - (Real.pi : ℂ) * exp u"
        ),
        "horizontal coordinate": (
            "def leadingHorizontalPoint (L : ℂ) (r : ℝ) : ℂ := L + r\n\n"
        ),
        "top-to-horizontal seam": (
            "theorem leadingTopPoint_eq_horizontal (L : ℂ) (r : ℝ) :"
        ),
        "right half-plane domain": (
            "def leadingLogDomain : Set ℂ := {u | 0 < u.re}"
        ),
        "endpoint connector": (
            "def leadingConnectorPoint (y : ℝ) : ℂ := 1 + y * I\n\n"
        ),
        "curvature normalization": (
            "def leadingCurvature (s L : ℂ) : ℂ :=\n"
            "  sectorialSaddleCurvature s L / L ^ 2"
        ),
        "Jacobian linear derivative": (
            "theorem leadingLogD1_at_saddle\n"
        ),
        "quadratic descent sign": (
            "leadingLogD2 s L = -leadingCurvature s L"
        ),
        "Gaussian with linear term": (
            "def leadingGaussian (K : ℂ) (r : ℝ) : ℂ :=\n"
            "  exp ((r : ℂ) - K * (r : ℂ) ^ 2 / 2)"
        ),
        "Gaussian exact integral": (
            "      ((2 * Real.pi : ℂ) / K) ^ (1 / 2 : ℂ) * "
            "exp (1 / (2 * K)) := by"
        ),
        "Cauchy rectangle producer": (
            "Complex.integral_boundary_rect_eq_zero_of_differentiableOn"
        ),
        "four named sides": (
            "leadingBottomSegment s X - leadingTopSegment s b X +\n"
            "        leadingRightSegment s b X - leadingLeftSegment s b = 0"
        ),
        "branch-safe rectangle": (
            "(leadingIntegrand_differentiableOn_domain s).mono\n"
            "      (leadingRectangle_subset_domain hX)"
        ),
        "positive concrete curvature": (
            "theorem quantitativeSaddleBranch_curvature_re_pos\n"
        ),
        "strong concrete curvature": (
            "theorem quantitativeSaddleBranch_curvature_strong_bounds\n"
        ),
        "curvature norm comparability": (
            "        2 * (leadingCurvature s (quantitativeSaddleBranch s)).re := by"
        ),
        "far-side exponential majorant": (
            "‖leadingIntegrand s (X + y * I)‖ ≤ Real.exp (-X) := by"
        ),
        "far vertical side vanishes": (
            "theorem tendsto_leadingRightSegment_zero\n"
        ),
        "translated-ray integrability": (
            "theorem integrableOn_leadingHorizontalRay\n"
        ),
        "infinite contour conclusion": (
            "leadingBottomRay s = leadingTopRay s b + leadingLeftSegment s b := by"
        ),
        "finite-to-infinite limit seam": (
            "have heq := tendsto_nhds_unique hbottom (hrhs.congr' hreverse)"
        ),
    }
    for label, needle in checks.items():
        require_once(text, needle, label)


def mutate(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise AssertionError(f"mutation source is not unique: {old!r}")
    return text.replace(old, new, 1)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS T3 mutation rejected: {label}")
        return
    raise AssertionError(f"T3 mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS exact T3 contour source contract")
    cases = {
        "phase three-quarters removed": mutate(
            source, "s * log u - (3 / 4) * u", "s * log u"
        ),
        "Jacobian factor removed": mutate(
            source, "exp u * exp (leadingPhase s u)", "exp (leadingPhase s u)"
        ),
        "full phase uses wrong half shift": mutate(
            source, "s * log u + u / 4", "s * log u + u / 2"
        ),
        "horizontal ray made vertical": mutate(
            source, "L + r", "L + r * I"
        ),
        "top-to-horizontal seam disconnected": mutate(
            source,
            "theorem leadingTopPoint_eq_horizontal (L : ℂ) (r : ℝ) :",
            "theorem leadingTopPoint_eq_horizontal_unchecked (L : ℂ) (r : ℝ) :",
        ),
        "log domain widened across cut": mutate(
            source, "{u | 0 < u.re}", "Set.univ"
        ),
        "connector moved to zero": mutate(
            source,
            "def leadingConnectorPoint (y : ℝ) : ℂ := 1 + y * I",
            "def leadingConnectorPoint (y : ℝ) : ℂ := y * I",
        ),
        "curvature loses square": mutate(
            source,
            "sectorialSaddleCurvature s L / L ^ 2",
            "sectorialSaddleCurvature s L / L",
        ),
        "linear saddle derivative disconnected": mutate(
            source,
            "theorem leadingLogD1_at_saddle\n",
            "theorem leadingLogD1_at_saddle_unchecked\n",
        ),
        "quadratic descent sign reversed": mutate(
            source,
            "leadingLogD2 s L = -leadingCurvature s L",
            "leadingLogD2 s L = leadingCurvature s L",
        ),
        "Gaussian linear term dropped": mutate(
            source,
            "exp ((r : ℂ) - K * (r : ℂ) ^ 2 / 2)",
            "exp (-K * (r : ℂ) ^ 2 / 2)",
        ),
        "Gaussian correction sign changed": mutate(
            source,
            "      ((2 * Real.pi : ℂ) / K) ^ (1 / 2 : ℂ) * "
            "exp (1 / (2 * K)) := by",
            "      ((2 * Real.pi : ℂ) / K) ^ (1 / 2 : ℂ) * "
            "exp (-1 / (2 * K)) := by",
        ),
        "Cauchy theorem disconnected": mutate(
            source,
            "Complex.integral_boundary_rect_eq_zero_of_differentiableOn",
            "Complex.integral_boundary_rect_eq_zero_unchecked",
        ),
        "top orientation sign reversed": mutate(
            source,
            "leadingBottomSegment s X - leadingTopSegment s b X +",
            "leadingBottomSegment s X + leadingTopSegment s b X +",
        ),
        "domain containment disconnected": mutate(
            source,
            "(leadingRectangle_subset_domain hX)",
            "(by simp)",
        ),
        "positive curvature theorem disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_curvature_re_pos\n",
            "theorem quantitativeSaddleBranch_curvature_re_pos_unchecked\n",
        ),
        "strong curvature theorem disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_curvature_strong_bounds\n",
            "theorem quantitativeSaddleBranch_curvature_strong_bounds_unchecked\n",
        ),
        "curvature comparison weakened": mutate(
            source,
            "        2 * (leadingCurvature s (quantitativeSaddleBranch s)).re := by",
            "        3 * (leadingCurvature s (quantitativeSaddleBranch s)).re := by",
        ),
        "far-side exponential sign reversed": mutate(
            source,
            "‖leadingIntegrand s (X + y * I)‖ ≤ Real.exp (-X) := by",
            "‖leadingIntegrand s (X + y * I)‖ ≤ Real.exp X := by",
        ),
        "far-side limit disconnected": mutate(
            source,
            "theorem tendsto_leadingRightSegment_zero\n",
            "theorem tendsto_leadingRightSegment_zero_unchecked\n",
        ),
        "translated-ray integrability disconnected": mutate(
            source,
            "theorem integrableOn_leadingHorizontalRay\n",
            "theorem integrableOn_leadingHorizontalRay_unchecked\n",
        ),
        "connector dropped from infinite contour": mutate(
            source,
            "leadingBottomRay s = leadingTopRay s b + leadingLeftSegment s b := by",
            "leadingBottomRay s = leadingTopRay s b := by",
        ),
        "finite-to-infinite seam disconnected": mutate(
            source,
            "have heq := tendsto_nhds_unique hbottom (hrhs.congr' hreverse)",
            "have heq := tendsto_nhds_unique hbottom hrhs",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print(f"PASS T3 semantic mutations: {len(cases)} rejected")


if __name__ == "__main__":
    main()
