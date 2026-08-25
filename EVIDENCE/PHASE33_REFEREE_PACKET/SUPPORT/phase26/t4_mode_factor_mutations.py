#!/usr/bin/env python3
"""Fail-closed mutations for the infinite T4 mode-factor bound."""

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
    / "HigherThetaModes.lean"
)


class ContractError(RuntimeError):
    """A required higher-mode seam is absent."""


def require(text: str, needle: str, label: str, count: int = 1) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count}, found {actual}")


def validate(text: str) -> None:
    checks = {
        "exact mode gap": ("def higherThetaGap (n : ℕ) : ℕ := (n + 2) ^ 2 - 1", 1),
        "gap inequality": ("theorem higherThetaGap_ge_three_mul", 1),
        "factor norm": ("theorem higherThetaComplexFactor_norm", 1),
        "geometric term": ("theorem higherThetaScalarFactor_le_geometric", 1),
        "infinite sum": ("theorem higherThetaScalarFactor_tsum_le_two_exp", 1),
        "full mode identity": ("theorem higherThetaMode_eq_fullMode", 1),
        "complex summability": ("theorem summable_higherThetaMode", 1),
        "sum norm": ("theorem higherThetaMode_tsum_norm_le", 1),
        "strip lower bound": ("theorem thetaStrip_modeParameter_ge_one", 1),
        "full-tail result": (
            "theorem fullThetaContourIntegrand_sub_leading_norm_le",
            1,
        ),
        "three-gap exponent": ("Real.exp (-3 * (Real.pi * (exp u).re))", 3),
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
        print(f"PASS T4 mode-factor mutation rejected: {label}")
        return
    raise AssertionError(f"T4 mode-factor mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T4 infinite mode-factor source contract")
    cases = {
        "quadratic gap changed": mutate(
            source,
            "def higherThetaGap (n : ℕ) : ℕ := (n + 2) ^ 2 - 1",
            "def higherThetaGap (n : ℕ) : ℕ := (n + 2) - 1",
        ),
        "gap theorem removed": mutate(
            source,
            "theorem higherThetaGap_ge_three_mul",
            "theorem mode_gap_unchecked",
        ),
        "factor norm removed": mutate(
            source,
            "theorem higherThetaComplexFactor_norm",
            "theorem factor_norm_unchecked",
        ),
        "geometric sum removed": mutate(
            source,
            "theorem higherThetaScalarFactor_tsum_le_two_exp",
            "theorem infinite_sum_unchecked",
        ),
        "mode identity removed": mutate(
            source,
            "theorem higherThetaMode_eq_fullMode",
            "theorem mode_identity_unchecked",
        ),
        "summability removed": mutate(
            source,
            "theorem summable_higherThetaMode",
            "theorem mode_summability_unchecked",
        ),
        "strip theorem removed": mutate(
            source,
            "theorem thetaStrip_modeParameter_ge_one",
            "theorem strip_bound_unchecked",
        ),
        "full tail removed": mutate(
            source,
            "theorem fullThetaContourIntegrand_sub_leading_norm_le",
            "theorem full_tail_unchecked",
        ),
        "suppression exponent weakened": mutate(
            source,
            "Real.exp (-3 * (Real.pi * (exp u).re))",
            "Real.exp (3 * (Real.pi * (exp u).re))",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)


if __name__ == "__main__":
    main()
