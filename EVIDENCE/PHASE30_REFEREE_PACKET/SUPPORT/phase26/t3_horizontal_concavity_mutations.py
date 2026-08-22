#!/usr/bin/env python3
"""Fail-closed source mutations for horizontal-ray concavity."""

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
    / "LeadingHorizontalConcavity.lean"
)


class ContractError(RuntimeError):
    """A required horizontal-ray connection is absent."""


def require(text: str, needle: str, label: str, count: int = 1) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count}, found {actual}")


def validate(text: str) -> None:
    checks = {
        "sector angle": ("|s.arg| < 1 / 100", 1),
        "real component": ("(99 / 100 : ℝ) * ‖s‖ < s.re", 1),
        "imaginary quotient": ("|s.im| < s.re / 99", 2),
        "rational curvature": (
            "0 < (s / (quantitativeSaddleBranch s + r) ^ 2).re",
            1,
        ),
        "exponential curvature": (
            "quantitativeSaddleBranch_horizontal_exponential_re_pos",
            2,
        ),
        "negative second derivative": (
            "theorem quantitativeSaddleBranch_horizontalLogD2_re_neg",
            1,
        ),
        "real horizontal coordinate": (
            "def leadingHorizontalRealLog",
            1,
        ),
        "second derivative producer": (
            "leadingHorizontalRealLog_iteratedDeriv_two",
            2,
        ),
        "strict concavity": (
            "theorem quantitativeSaddleBranch_horizontal_strictConcaveOn",
            1,
        ),
        "legal ray": (
            "Ici (1 - (quantitativeSaddleBranch s).re)",
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
        print(f"PASS horizontal-concavity mutation rejected: {label}")
        return
    raise AssertionError(f"horizontal-concavity mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 horizontal-concavity source contract")
    cases = {
        "sector widened": mutate(source, "|s.arg| < 1 / 100", "|s.arg| < 1 / 20"),
        "component bound weakened": mutate(
            source, "(99 / 100 : ℝ) * ‖s‖ < s.re", "(9 / 10 : ℝ) * ‖s‖ < s.re"
        ),
        "rational sign reversed": mutate(
            source,
            "0 < (s / (quantitativeSaddleBranch s + r) ^ 2).re",
            "(s / (quantitativeSaddleBranch s + r) ^ 2).re < 0",
        ),
        "exponential producer disconnected": mutate(
            source,
            "quantitativeSaddleBranch_horizontal_exponential_re_pos",
            "horizontal_exponential_re_pos_unchecked",
        ),
        "second derivative renamed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontalLogD2_re_neg",
            "theorem horizontalLogD2_re_neg_unchecked",
        ),
        "vertical coordinate substituted": mutate(
            source,
            "def leadingHorizontalRealLog",
            "def leadingVerticalRealLog",
        ),
        "derivative producer disconnected": mutate(
            source,
            "leadingHorizontalRealLog_iteratedDeriv_two",
            "horizontalRealLog_iteratedDeriv_two_unchecked",
        ),
        "concavity theorem removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_horizontal_strictConcaveOn",
            "theorem horizontal_strictConcaveOn_unchecked",
        ),
        "legal ray shifted": mutate(
            source,
            "Ici (1 - (quantitativeSaddleBranch s).re)",
            "Ici (-(quantitativeSaddleBranch s).re)",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)


if __name__ == "__main__":
    main()
