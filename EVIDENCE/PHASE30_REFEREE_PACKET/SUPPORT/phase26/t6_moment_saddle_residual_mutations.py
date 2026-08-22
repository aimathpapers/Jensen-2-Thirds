#!/usr/bin/env python3
"""Fail-closed mutations for the moment-chain saddle residual insertion."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/MomentSaddleResidual.lean"
)


class ContractError(RuntimeError):
    """The moment-saddle residual source contract changed."""


REQUIRED = {
    "moment value": "def manuscriptMomentSaddleMainSix",
    "chain factor":
        "64 * manuscriptSaddleMainSix (coefficientMellinParameter M)",
    "sector theorem":
        "theorem coefficientMellinParameter_mem_leanSaddleSector_of_innerDisc",
    "outer-disc source":
        "manuscriptCauchy_closedBall_subset_sector hnLarge hzOuter",
    "saddle extraction":
        "leanTwoShiftAdmissible_base (leanCoefficientSector_admissible hM.2)",
    "radial theorem":
        "theorem coefficientMellinParameter_norm_ge_center_of_innerDisc",
    "radial source": "(manuscriptCauchy_shifted_norm_bounds hnLarge hzOuter).1",
    "moment bound theorem":
        "theorem manuscriptMomentSaddleMainSix_norm_le_on_innerDisc",
    "center bound": "1280000 / ((n : ℝ) ^ 5 * Real.log (n : ℝ))",
    "power comparison": "pow_le_pow_left₀ hnpos.le hNlower 5",
    "log comparison": "Real.log_le_log hnpos hNlower",
    "raw H6 bound": "manuscriptSaddleMainSix_norm_le hNsector",
    "final residual":
        "theorem manuscriptSixthResidual_outerBox_reducedSaddle_norm_le",
    "concrete decomposition":
        "manuscriptXiSixthLogDecomposition\n          (manuscriptMomentSaddleMainSix ((n : ℂ) + z)) ((n : ℂ) + z)",
    "outer residual consumer": "manuscriptSixthResidual_outerBox_norm_le",
}

COUNTS = {
    "1280000 / ((n : ℝ) ^ 5 * Real.log (n : ℝ))": 4,
    "manuscriptXiSixthLogDecomposition\n"
    "          (manuscriptMomentSaddleMainSix ((n : ℂ) + z)) ((n : ℂ) + z)": 2,
}


def validate(text: str) -> None:
    for label, needle in REQUIRED.items():
        if text.count(needle) != COUNTS.get(needle, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T6 moment-saddle residual source contract")
    mutations = {
        "moment value removed": (
            "def manuscriptMomentSaddleMainSix",
            "def uncheckedMomentSaddleMainSix",
        ),
        "chain factor changed": (
            "64 * manuscriptSaddleMainSix (coefficientMellinParameter M)",
            "32 * manuscriptSaddleMainSix (coefficientMellinParameter M)",
        ),
        "sector theorem removed": (
            "theorem coefficientMellinParameter_mem_leanSaddleSector_of_innerDisc",
            "theorem uncheckedShiftedSector",
        ),
        "outer-disc source disconnected": (
            "manuscriptCauchy_closedBall_subset_sector hnLarge hzOuter",
            "uncheckedOuterDisc hnLarge hzOuter",
        ),
        "saddle extraction disconnected": (
            "leanTwoShiftAdmissible_base (leanCoefficientSector_admissible hM.2)",
            "uncheckedSaddleExtraction hM",
        ),
        "radial theorem removed": (
            "theorem coefficientMellinParameter_norm_ge_center_of_innerDisc",
            "theorem uncheckedRadialComparison",
        ),
        "radial source disconnected": (
            "(manuscriptCauchy_shifted_norm_bounds hnLarge hzOuter).1",
            "uncheckedShiftedNorm hnLarge hzOuter",
        ),
        "power changed": (
            "pow_le_pow_left₀ hnpos.le hNlower 5",
            "pow_le_pow_left₀ hnpos.le hNlower 4",
        ),
        "log comparison disconnected": (
            "Real.log_le_log hnpos hNlower",
            "uncheckedLogMonotonicity hnpos hNlower",
        ),
        "raw bound disconnected": (
            "manuscriptSaddleMainSix_norm_le hNsector",
            "uncheckedMainSixBound hNsector",
        ),
        "constant changed": (
            "1280000 / ((n : ℝ) ^ 5 * Real.log (n : ℝ))",
            "640000 / ((n : ℝ) ^ 5 * Real.log (n : ℝ))",
        ),
        "final theorem removed": (
            "theorem manuscriptSixthResidual_outerBox_reducedSaddle_norm_le",
            "theorem uncheckedReducedSaddleResidual",
        ),
        "decomposition disconnected": (
            "manuscriptXiSixthLogDecomposition\n          (manuscriptMomentSaddleMainSix ((n : ℂ) + z)) ((n : ℂ) + z)",
            "uncheckedXiSixthDecomposition",
        ),
        "residual consumer disconnected": (
            "manuscriptSixthResidual_outerBox_norm_le",
            "uncheckedOuterBoxResidual",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 moment-saddle residual mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
