#!/usr/bin/env python3
"""Fail-closed mutations for the one-constant sixth-residual rate."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/SixthResidualRate.lean"
)


class ContractError(RuntimeError):
    """The residual-rate source contract changed."""


REQUIRED = {
    "Cauchy half bound": "theorem manuscriptCauchyEpsilon_le_half",
    "quarter anchor": "theorem manuscriptQuarterAnchor_ge_twelfth",
    "quarter value": "(n : ℝ) / 12 ≤ (((n / 4 - 1 : ℕ) : ℝ))",
    "far anchor": "theorem manuscriptFarAnchor_ge_quarter_log",
    "far value":
        "(n : ℝ) * Real.log (n : ℝ) / 4 ≤",
    "reciprocal-log premise": "e ≤ 2 / Real.log (n : ℝ)",
    "Cauchy constant":
        "def manuscriptSixthResidualCauchyConstant : ℝ := 540 * 2000 ^ 6",
    "BC constant":
        "def manuscriptSixthResidualBCConstant : ℝ := 1440 * 12 ^ 6",
    "D constant":
        "def manuscriptSixthResidualDConstant : ℝ := 160 * 12 ^ 6",
    "A constant":
        "def manuscriptSixthResidualAConstant : ℝ := 24 * 4 ^ 5",
    "combined constant": "def manuscriptSixthResidualRateConstant",
    "Cauchy rate": "theorem manuscriptSixthResidual_cauchy_term_le",
    "BC rate": "theorem manuscriptSixthResidual_BC_term_le",
    "D rate": "theorem manuscriptSixthResidual_D_term_le",
    "A rate": "theorem manuscriptSixthResidual_A_term_le",
    "final rate": "theorem manuscriptSixthResidual_outerBox_rate",
    "ledger producer": "manuscriptSixthResidual_outerBox_farA_norm_le",
}

COUNTS = {
    "e ≤ 2 / Real.log (n : ℝ)": 5,
}


def validate(text: str) -> None:
    for label, needle in REQUIRED.items():
        if text.count(needle) != COUNTS.get(needle, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T6 one-constant residual-rate source contract")
    mutations = {
        "Cauchy half removed": (
            "theorem manuscriptCauchyEpsilon_le_half",
            "theorem uncheckedCauchyHalf",
        ),
        "quarter anchor weakened": (
            "(n : ℝ) / 12 ≤ (((n / 4 - 1 : ℕ) : ℝ))",
            "(n : ℝ) / 16 ≤ (((n / 4 - 1 : ℕ) : ℝ))",
        ),
        "far logarithm dropped": (
            "(n : ℝ) * Real.log (n : ℝ) / 4 ≤",
            "(n : ℝ) / 4 ≤",
        ),
        "scale premise weakened": (
            "e ≤ 2 / Real.log (n : ℝ)",
            "e ≤ 3 / Real.log (n : ℝ)",
        ),
        "Cauchy constant reduced": (
            "540 * 2000 ^ 6", "500 * 2000 ^ 6"),
        "BC constant reduced": (
            "1440 * 12 ^ 6", "1400 * 12 ^ 6"),
        "D constant reduced": (
            "160 * 12 ^ 6", "150 * 12 ^ 6"),
        "A constant reduced": (
            "24 * 4 ^ 5", "20 * 4 ^ 5"),
        "Cauchy rate removed": (
            "theorem manuscriptSixthResidual_cauchy_term_le",
            "theorem uncheckedCauchyRate",
        ),
        "BC rate removed": (
            "theorem manuscriptSixthResidual_BC_term_le",
            "theorem uncheckedBCRate",
        ),
        "D rate removed": (
            "theorem manuscriptSixthResidual_D_term_le",
            "theorem uncheckedDRate",
        ),
        "A rate removed": (
            "theorem manuscriptSixthResidual_A_term_le",
            "theorem uncheckedARate",
        ),
        "ledger producer disconnected": (
            "manuscriptSixthResidual_outerBox_farA_norm_le",
            "uncheckedFarALedger",
        ),
        "final theorem removed": (
            "theorem manuscriptSixthResidual_outerBox_rate",
            "theorem uncheckedResidualRate",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 residual-rate mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
