#!/usr/bin/env python3
"""Fail-closed source mutations for the fixed-sector saddle-main ratio."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/SaddleMainRatio.lean"
)


class ContractError(RuntimeError):
    """The concrete saddle-main ratio contract is absent or ambiguous."""


def validate(text: str) -> None:
    required = {
        "branch speed": "theorem branchDeriv_mul_parameterNorm_le",
        "curvature logarithmic derivative":
            "theorem saddleCurvatureAlong_logDeriv_mul_parameterNorm_le",
        "complete log-main bound":
            "theorem saddleMomentLogMainD1_sub_log_mul_parameterNorm_le",
        "segment FTC": "theorem norm_sub_le_mul_of_hasDerivAt_le",
        "two-shift admissibility": "def leanTwoShiftAdmissible",
        "fixed outer sector": "def leanCoefficientSector",
        "sector containment": "theorem leanCoefficientSector_admissible",
        "exact log error": "def saddleMainTwoShiftLogError",
        "log error formula":
            "saddleMomentLogMain (s + 2) - saddleMomentLogMain s - 2 *",
        "exact relative error": "def saddleMainTwoShiftRelativeError",
        "exponential error producer": "Complex.norm_exp_sub_one_le hlogSmall",
        "main factorization":
            "theorem saddleMomentMain_fixedSector_twoShift_factorization",
        "uniform ratio estimate":
            "theorem saddleMainTwoShiftRelativeError_fixedSector",
        "ratio constant": "‖saddleMainTwoShiftRelativeError s‖ ≤ 52 / ‖s‖",
        "outer angle": "|s.arg| < saddleOuterAngle",
        "outer-sector branch producer": "hasDerivAt_quantitativeSaddleBranch hs",
        "exact main producer": "saddleMomentMain_eq_exp_logMain hs1",
    }
    expected_counts = {"ratio constant": 1}
    for label, needle in required.items():
        if text.count(needle) != expected_counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 fixed-sector saddle-main ratio source contract")
    mutations = {
        "branch speed removed": (
            "theorem branchDeriv_mul_parameterNorm_le",
            "theorem branch_speed_unchecked",
        ),
        "curvature log derivative removed": (
            "theorem saddleCurvatureAlong_logDeriv_mul_parameterNorm_le",
            "theorem curvature_log_derivative_unchecked",
        ),
        "FTC removed": (
            "theorem norm_sub_le_mul_of_hasDerivAt_le",
            "theorem segment_bound_unchecked",
        ),
        "outer angle widened": (
            "|s.arg| < saddleOuterAngle",
            "|s.arg| < saddleProofAngle",
        ),
        "sector containment removed": (
            "theorem leanCoefficientSector_admissible",
            "theorem sector_containment_unchecked",
        ),
        "log error sign changed": (
            "saddleMomentLogMain (s + 2) - saddleMomentLogMain s - 2 *",
            "saddleMomentLogMain (s + 2) - saddleMomentLogMain s + 2 *",
        ),
        "exponential conversion removed": (
            "Complex.norm_exp_sub_one_le hlogSmall",
            "exponential_bound_unchecked hlogSmall",
        ),
        "main producer disconnected": (
            "saddleMomentMain_eq_exp_logMain hs1",
            "saddle_main_identity_unchecked hs1",
        ),
        "ratio factorization removed": (
            "theorem saddleMomentMain_fixedSector_twoShift_factorization",
            "theorem ratio_factorization_unchecked",
        ),
        "ratio constant weakened": (
            "‖saddleMainTwoShiftRelativeError s‖ ≤ 52 / ‖s‖",
            "‖saddleMainTwoShiftRelativeError s‖ ≤ 104 / ‖s‖",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 saddle-main ratio mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
