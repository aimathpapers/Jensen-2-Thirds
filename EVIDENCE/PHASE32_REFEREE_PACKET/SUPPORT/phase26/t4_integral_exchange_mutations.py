#!/usr/bin/env python3
"""Fail-closed mutations for T4 sum/integral exchange."""

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
    / "HigherThetaIntegral.lean"
)


class ContractError(RuntimeError):
    pass


def require(text: str, needle: str, label: str, count: int = 1) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count}, found {actual}")


def validate(text: str) -> None:
    checks = {
        "mode measurability": ("theorem aestronglyMeasurable_higherThetaHorizontalMode", 1),
        "sum measurability": ("theorem aestronglyMeasurable_higherThetaHorizontalSum", 1),
        "fixed geometric bound": ("theorem higherThetaMode_horizontal_geometric_bound", 1),
        "mode integrability": ("theorem integrableOn_higherThetaHorizontalMode", 1),
        "integral norm bound": ("theorem integral_norm_higherThetaHorizontalMode_le", 1),
        "summed integral norms": ("theorem summable_integral_norm_higherThetaHorizontalMode", 1),
        "integral exchange": ("theorem integral_tsum_higherThetaHorizontalMode", 1),
        "full ray split": ("theorem fullThetaTopRay_eq_leading_add_higher", 1),
        "mode-integral sum": ("theorem higherThetaTopRay_eq_tsum_modeIntegrals", 1),
        "Fubini producer": ("integral_tsum_of_summable_integral_norm", 1),
        "legal ray": ("(Ioi 1)", 5),
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
        print(f"PASS T4 integral-exchange mutation rejected: {label}")
        return
    raise AssertionError(f"T4 integral-exchange mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T4 infinite sum/integral source contract")
    cases = {
        "mode measurability removed": mutate(
            source,
            "theorem aestronglyMeasurable_higherThetaHorizontalMode",
            "theorem mode_measurability_unchecked",
        ),
        "geometric domination removed": mutate(
            source,
            "theorem higherThetaMode_horizontal_geometric_bound",
            "theorem mode_domination_unchecked",
        ),
        "mode integrability removed": mutate(
            source,
            "theorem integrableOn_higherThetaHorizontalMode",
            "theorem mode_integrability_unchecked",
        ),
        "summability removed": mutate(
            source,
            "theorem summable_integral_norm_higherThetaHorizontalMode",
            "theorem integral_norm_summability_unchecked",
        ),
        "Fubini producer disconnected": mutate(
            source,
            "integral_tsum_of_summable_integral_norm",
            "integral_tsum_unchecked",
        ),
        "integral exchange removed": mutate(
            source,
            "theorem integral_tsum_higherThetaHorizontalMode",
            "theorem integral_exchange_unchecked",
        ),
        "full ray split removed": mutate(
            source,
            "theorem fullThetaTopRay_eq_leading_add_higher",
            "theorem full_ray_split_unchecked",
        ),
        "mode-integral identity removed": mutate(
            source,
            "theorem higherThetaTopRay_eq_tsum_modeIntegrals",
            "theorem mode_integral_sum_unchecked",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)


if __name__ == "__main__":
    main()
