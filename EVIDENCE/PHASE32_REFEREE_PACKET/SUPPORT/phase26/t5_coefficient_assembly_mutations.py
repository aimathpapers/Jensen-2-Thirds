#!/usr/bin/env python3
"""Fail-closed source mutations for the exact complex coefficient assembly."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/CoefficientAssembly.lean"
)


class ContractError(RuntimeError):
    """The coefficient normalization contract changed."""


def validate(text: str) -> None:
    required = {
        "Mellin shift": "def coefficientMellinParameter (M : ℂ)",
        "exact shift formula": "2 * M - 2",
        "moment multiplier": "def coefficientMomentMultiplier (N : ℂ)",
        "multiplier formula": "16 * (N + 2) * (N + 1)",
        "dyadic continuation": "def coefficientDyadicScale (M : ℂ)",
        "dyadic exponent": "exp (-(2 * M + 2) * log 2)",
        "complex coefficient": "def complexXiCoefficientMoment (M : ℂ)",
        "Gamma quotient producer": "complexFactorialRatio M * coefficientDyadicScale M",
        "two-shift moment combination":
            "coefficientMomentMultiplier N * fullThetaMoment N -",
        "integer shift theorem": "theorem coefficientMellinParameter_nat_succ",
        "choose-two theorem": "theorem coefficientMomentMultiplier_evenNat",
        "dyadic theorem": "theorem coefficientDyadicScale_natCast",
        "T1 specialization": "theorem complexXiCoefficientMoment_nat_succ",
        "T1 producer": "centeredXiCoefficient_succ_eq_thetaMomentAssembly n",
        "Gamma anchor producer": "complexFactorialRatio_natCast",
        "logarithmic saddle bound":
            "theorem quantitativeSaddleBranch_norm_le_two_log_norm",
        "curvature decay theorem":
            "theorem quantitativeSaddleBranch_curvature_inv_le_log_div_norm",
        "curvature decay rate": "4 * Real.log ‖s‖ / ‖s‖",
        "coefficient upper theorem": "theorem coefficientMomentMultiplier_norm_le",
        "coefficient upper constant": "‖coefficientMomentMultiplier s‖ ≤ 96 * ‖s‖ ^ 2",
        "denominator floor theorem":
            "theorem coefficientMomentMultiplier_sub_saddle_sq_norm_lower",
        "denominator floor": "8 * ‖s‖ ^ 2 ≤",
        "denominator nonzero":
            "theorem coefficientMomentMultiplier_sub_saddle_sq_ne_zero",
        "paired coefficient sector": "def leanXiCoefficientSector : Set ℂ",
        "moment error definition": "def complexXiMomentRelativeError (M : ℂ)",
        "coefficient main": "def complexXiCoefficientMain (M : ℂ)",
        "combined error": "def complexXiCoefficientRelativeError (M : ℂ)",
        "combined cross term":
            "gammaError + momentError + gammaError * momentError",
        "Gamma exact factorization":
            "theorem complexFactorialRatio_exact_factorization",
        "two-shift assembly producer": "have hmoment := fullThetaTwoShiftAssembly",
        "fixed-sector exact factorization":
            "theorem complexXiCoefficientMoment_factorization\n",
        "shifted curvature theorem":
            "theorem quantitativeSaddleBranch_shift_curvature_inv_le_log_div_norm",
        "moment error theorem": "theorem complexXiMomentRelativeError_norm_le",
        "moment error rate":
            "(100 * fullThetaMomentErrorCoefficient) * Real.log ‖N‖ / ‖N‖",
        "Gamma correction theorem":
            "theorem norm_complexFactorialRatioCorrection_sub_one_fixedSector",
        "combined coefficient": "def complexXiCoefficientErrorCoefficient : ℝ",
        "combined rate theorem":
            "theorem complexXiCoefficientRelativeError_norm_le",
        "main nonzero theorem": "theorem complexXiCoefficientMain_ne_zero",
        "exported T5 theorem": "theorem complexXiCoefficient_sector_asymptotic",
    }
    counts = {
        "exact shift formula": 3,
        "Gamma quotient producer": 5,
        "combined cross term": 4,
        "curvature decay rate": 2,
        "denominator floor": 2,
    }
    for label, needle in required.items():
        if text.count(needle) != counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 exact complex coefficient assembly source contract")
    mutations = {
        "Mellin shift changed": ("2 * M - 2", "2 * M - 3"),
        "moment multiplier changed": (
            "16 * (N + 2) * (N + 1)", "8 * (N + 2) * (N + 1)"
        ),
        "dyadic exponent changed": (
            "exp (-(2 * M + 2) * log 2)", "exp (-(2 * M + 1) * log 2)"
        ),
        "Gamma quotient disconnected": (
            "complexFactorialRatio M * coefficientDyadicScale M",
            "uncheckedFactorialRatio M * coefficientDyadicScale M",
        ),
        "upper moment sign changed": (
            "coefficientMomentMultiplier N * fullThetaMoment N -",
            "coefficientMomentMultiplier N * fullThetaMoment N +",
        ),
        "T1 specialization removed": (
            "theorem complexXiCoefficientMoment_nat_succ",
            "theorem unchecked_complexXiCoefficientMoment_nat_succ",
        ),
        "T1 producer disconnected": (
            "centeredXiCoefficient_succ_eq_thetaMomentAssembly n",
            "unchecked_centeredXiCoefficient_assembly n",
        ),
        "Gamma anchor disconnected": (
            "complexFactorialRatio_natCast", "uncheckedGammaAnchor"
        ),
        "logarithmic saddle theorem removed": (
            "theorem quantitativeSaddleBranch_norm_le_two_log_norm",
            "theorem unchecked_saddle_log_bound",
        ),
        "curvature rate weakened": (
            "4 * Real.log ‖s‖ / ‖s‖", "5 * Real.log ‖s‖ / ‖s‖"
        ),
        "coefficient upper constant weakened": (
            "‖coefficientMomentMultiplier s‖ ≤ 96 * ‖s‖ ^ 2",
            "‖coefficientMomentMultiplier s‖ ≤ 97 * ‖s‖ ^ 2",
        ),
        "denominator floor weakened": (
            "8 * ‖s‖ ^ 2 ≤", "7 * ‖s‖ ^ 2 ≤"
        ),
        "denominator nonzero theorem removed": (
            "theorem coefficientMomentMultiplier_sub_saddle_sq_ne_zero",
            "theorem unchecked_coefficient_denominator_nonzero",
        ),
        "paired sector removed": (
            "def leanXiCoefficientSector : Set ℂ", "def uncheckedCoefficientSector : Set ℂ"
        ),
        "moment error definition removed": (
            "def complexXiMomentRelativeError (M : ℂ)",
            "def uncheckedMomentError (M : ℂ)",
        ),
        "coefficient main removed": (
            "def complexXiCoefficientMain (M : ℂ)",
            "def uncheckedCoefficientMain (M : ℂ)",
        ),
        "combined cross term removed": (
            "gammaError + momentError + gammaError * momentError",
            "gammaError + momentError + 0 * momentError",
        ),
        "two-shift producer disconnected": (
            "have hmoment := fullThetaTwoShiftAssembly",
            "have hmoment := uncheckedTwoShiftAssembly",
        ),
        "exact factorization removed": (
            "theorem complexXiCoefficientMoment_factorization\n",
            "theorem uncheckedCoefficientFactorization\n",
        ),
        "moment rate weakened": (
            "(100 * fullThetaMomentErrorCoefficient) * Real.log ‖N‖ / ‖N‖",
            "(101 * fullThetaMomentErrorCoefficient) * Real.log ‖N‖ / ‖N‖",
        ),
        "Gamma correction bound removed": (
            "theorem norm_complexFactorialRatioCorrection_sub_one_fixedSector",
            "theorem uncheckedGammaCorrectionBound",
        ),
        "combined bound removed": (
            "theorem complexXiCoefficientRelativeError_norm_le",
            "theorem uncheckedCoefficientErrorBound",
        ),
        "nonzero main removed": (
            "theorem complexXiCoefficientMain_ne_zero",
            "theorem uncheckedCoefficientMainNonzero",
        ),
        "exported T5 theorem removed": (
            "theorem complexXiCoefficient_sector_asymptotic",
            "theorem uncheckedCoefficientSectorAsymptotic",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 coefficient-assembly mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
