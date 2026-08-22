#!/usr/bin/env python3
"""Fail-closed source mutations for the integrated horizontal tails."""

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
    / "LeadingHorizontalTails.lean"
)


class ContractError(RuntimeError):
    """A required horizontal-tail connection is absent."""


def require(text: str, needle: str, label: str, count: int = 1) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count}, found {actual}")


def validate(text: str) -> None:
    checks = {
        "right tangent lemma": ("theorem concaveOn_right_tangent_bound\n", 1),
        "left tangent lemma": ("theorem concaveOn_left_tangent_bound\n", 1),
        "phase envelopes": (
            "theorem quantitativeSaddleBranch_horizontal_phase_tail_envelopes\n",
            1,
        ),
        "boundary sign producer": (
            "quantitativeSaddleBranch_horizontal_boundary_derivative_signs hs",
            1,
        ),
        "boundary gap producer": (
            "quantitativeSaddleBranch_horizontal_boundary_phase_gaps hs",
            1,
        ),
        "left unit envelope": ("-(‖K‖ * ρ ^ 2 / 20) + (r + ρ)", 1),
        "right slope envelope": (
            "-(‖K‖ * ρ ^ 2 / 20) - (‖K‖ * ρ / 20) * (r - ρ)",
            1,
        ),
        "norm identity": ("theorem norm_leadingIntegrand_horizontal_eq_exp\n", 1),
        "norm envelopes": (
            "theorem quantitativeSaddleBranch_horizontal_norm_tail_envelopes\n",
            1,
        ),
        "exponential integral": ("theorem integral_exp_neg_mul_sub_Ioi\n", 1),
        "tail integral theorem": (
            "theorem quantitativeSaddleBranch_horizontal_tail_integral_bounds\n",
            1,
        ),
        "left interval": ("Icc (1 - L.re) (-ρ)", 2),
        "right interval": ("Ioi ρ", 10),
        "right reciprocal scale": ("20 / (‖K‖ * ρ)", 3),
        "integral monotonicity": ("setIntegral_mono_on htarget hgint", 1),
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
        print(f"PASS horizontal-tail mutation rejected: {label}")
        return
    raise AssertionError(f"horizontal-tail mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 integrated horizontal-tail source contract")
    cases = {
        "right tangent removed": mutate(
            source,
            "theorem concaveOn_right_tangent_bound\n",
            "theorem right_tangent_bound_unchecked\n",
        ),
        "left tangent removed": mutate(
            source,
            "theorem concaveOn_left_tangent_bound\n",
            "theorem left_tangent_bound_unchecked\n",
        ),
        "phase envelopes removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_phase_tail_envelopes\n",
            "theorem horizontal_phase_tail_envelopes_unchecked\n",
        ),
        "derivative signs disconnected": mutate(
            source,
            "quantitativeSaddleBranch_horizontal_boundary_derivative_signs hs",
            "horizontal_boundary_derivative_signs_unchecked hs",
        ),
        "phase gaps disconnected": mutate(
            source,
            "quantitativeSaddleBranch_horizontal_boundary_phase_gaps hs",
            "horizontal_boundary_phase_gaps_unchecked hs",
        ),
        "left envelope sign changed": mutate(
            source,
            "-(‖K‖ * ρ ^ 2 / 20) + (r + ρ)",
            "-(‖K‖ * ρ ^ 2 / 20) - (r + ρ)",
        ),
        "right slope weakened": mutate(
            source,
            "-(‖K‖ * ρ ^ 2 / 20) - (‖K‖ * ρ / 20) * (r - ρ)",
            "-(‖K‖ * ρ ^ 2 / 20)",
        ),
        "norm identity removed": mutate(
            source,
            "theorem norm_leadingIntegrand_horizontal_eq_exp\n",
            "theorem norm_horizontal_eq_exp_unchecked\n",
        ),
        "norm envelopes removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_norm_tail_envelopes\n",
            "theorem horizontal_norm_tail_envelopes_unchecked\n",
        ),
        "exponential integral removed": mutate(
            source,
            "theorem integral_exp_neg_mul_sub_Ioi\n",
            "theorem integral_exp_tail_unchecked\n",
        ),
        "tail theorem removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_tail_integral_bounds\n",
            "theorem horizontal_tail_integral_bounds_unchecked\n",
        ),
        "right reciprocal weakened": mutate(
            source, "20 / (‖K‖ * ρ)", "200 / (‖K‖ * ρ)"
        ),
        "integral comparison disconnected": mutate(
            source, "setIntegral_mono_on htarget hgint", "setIntegral_mono_on_unchecked"
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)


if __name__ == "__main__":
    main()
