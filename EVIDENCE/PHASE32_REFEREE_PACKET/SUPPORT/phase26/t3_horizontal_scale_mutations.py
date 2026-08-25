#!/usr/bin/env python3
"""Fail-closed mutations for the inverse-curvature horizontal-tail scale."""

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
    / "LeadingHorizontalScale.lean"
)


class ContractError(RuntimeError):
    """A required inverse-curvature connection is absent."""


def require(text: str, needle: str, label: str, count: int = 1) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count}, found {actual}")


def validate(text: str) -> None:
    checks = {
        "curvature dominates branch": (
            "theorem quantitativeSaddleBranch_re_lt_curvature_norm\n",
            1,
        ),
        "exact saddle curvature formula": (
            "K = s / L ^ 2 + (Real.pi : ℂ) * exp L",
            1,
        ),
        "radius square scale": (
            "theorem leadingCentralRadius_square_scale\n",
            1,
        ),
        "degree fifteen domination": (
            "theorem pow_fifteen_mul_exp_neg_div_twenty_le",
            1,
        ),
        "coefficient theorem": (
            "theorem quantitativeSaddleBranch_horizontal_tail_coefficient_le\n",
            1,
        ),
        "explicit inverse constant": (
            "(2 * 20 ^ 15 * (Nat.factorial 15 : ℝ)) / ‖K‖",
            3,
        ),
        "relative inverse theorem": (
            "theorem quantitativeSaddleBranch_horizontal_tail_relative_inverse_curvature\n",
            1,
        ),
        "relative producer": (
            "quantitativeSaddleBranch_horizontal_tail_relative_bound hs",
            1,
        ),
        "coefficient producer": (
            "quantitativeSaddleBranch_horizontal_tail_coefficient_le hs",
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
        print(f"PASS horizontal-scale mutation rejected: {label}")
        return
    raise AssertionError(f"horizontal-scale mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 inverse-curvature horizontal-tail source contract")
    cases = {
        "curvature theorem removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_re_lt_curvature_norm\n",
            "theorem branch_re_bound_unchecked\n",
        ),
        "saddle curvature formula altered": mutate(
            source,
            "K = s / L ^ 2 + (Real.pi : ℂ) * exp L",
            "K = s / L + (Real.pi : ℂ) * exp L",
        ),
        "radius exponent changed": mutate(
            source,
            "theorem leadingCentralRadius_square_scale\n",
            "theorem central_radius_scale_unchecked\n",
        ),
        "degree fifteen bound removed": mutate(
            source,
            "theorem pow_fifteen_mul_exp_neg_div_twenty_le",
            "theorem polynomial_exponential_bound_unchecked",
        ),
        "coefficient theorem removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_tail_coefficient_le\n",
            "theorem horizontal_tail_coefficient_unchecked\n",
        ),
        "inverse constant changed": mutate(
            source,
            "(2 * 20 ^ 15 * (Nat.factorial 15 : ℝ)) / ‖K‖",
            "(20 ^ 14 : ℝ) / ‖K‖",
        ),
        "final theorem removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_tail_relative_inverse_curvature\n",
            "theorem horizontal_tail_relative_inverse_unchecked\n",
        ),
        "relative producer disconnected": mutate(
            source,
            "quantitativeSaddleBranch_horizontal_tail_relative_bound hs",
            "horizontal_tail_relative_bound_unchecked hs",
        ),
        "coefficient producer disconnected": mutate(
            source,
            "quantitativeSaddleBranch_horizontal_tail_coefficient_le hs",
            "horizontal_tail_coefficient_unchecked hs",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)


if __name__ == "__main__":
    main()
