#!/usr/bin/env python3
"""Fail-closed mutations for the complete T3 leading-mode assembly."""

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
    / "LeadingT3Assembly.lean"
)


class ContractError(RuntimeError):
    """A required T3 assembly seam is absent."""


def require(text: str, needle: str, label: str, count: int = 1) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count}, found {actual}")


def validate(text: str) -> None:
    checks = {
        "centered ray": ("theorem leadingTopRay_eq_centered\n", 1),
        "centered integrability": (
            "theorem integrableOn_quantitativeSaddleBranch_centeredRay\n",
            1,
        ),
        "three-piece split": (
            "theorem quantitativeSaddleBranch_centeredRay_integral_split\n",
            1,
        ),
        "top-ray assembly": (
            "theorem quantitativeSaddleBranch_leadingTopRay_relative_error_le\n",
            1,
        ),
        "bottom-ray assembly": (
            "theorem quantitativeSaddleBranch_leadingBottomRay_relative_error_le\n",
            1,
        ),
        "central producer": (
            "quantitativeSaddleBranch_centralGaussian_relative_error_le hs",
            1,
        ),
        "tail producer": (
            "quantitativeSaddleBranch_horizontal_tail_relative_inverse_curvature hs",
            1,
        ),
        "connector producer": (
            "quantitativeSaddleBranch_leftSegment_relative_inverse_curvature hs",
            1,
        ),
        "legal rectangle": ("leading_infinite_rectangle_identity s hb", 1),
        "final constant": (
            "((71000001 + 2 * 20 ^ 15 * (Nat.factorial 15 : ℝ)) / ‖K‖)",
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
        print(f"PASS T3 assembly mutation rejected: {label}")
        return
    raise AssertionError(f"T3 assembly mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 complete-assembly source contract")
    cases = {
        "center translation removed": mutate(
            source, "theorem leadingTopRay_eq_centered\n", "theorem centered_ray_unchecked\n"
        ),
        "partition removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_centeredRay_integral_split\n",
            "theorem ray_partition_unchecked\n",
        ),
        "central estimate disconnected": mutate(
            source,
            "quantitativeSaddleBranch_centralGaussian_relative_error_le hs",
            "central_estimate_unchecked hs",
        ),
        "tails disconnected": mutate(
            source,
            "quantitativeSaddleBranch_horizontal_tail_relative_inverse_curvature hs",
            "tail_estimate_unchecked hs",
        ),
        "connector disconnected": mutate(
            source,
            "quantitativeSaddleBranch_leftSegment_relative_inverse_curvature hs",
            "connector_estimate_unchecked hs",
        ),
        "rectangle disconnected": mutate(
            source,
            "leading_infinite_rectangle_identity s hb",
            "rectangle_identity_unchecked s hb",
        ),
        "connector constant omitted": mutate(
            source,
            "((71000001 + 2 * 20 ^ 15 * (Nat.factorial 15 : ℝ)) / ‖K‖)",
            "((71000000 + 2 * 20 ^ 15 * (Nat.factorial 15 : ℝ)) / ‖K‖)",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)


if __name__ == "__main__":
    main()
