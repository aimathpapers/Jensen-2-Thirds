#!/usr/bin/env python3
"""Fail-closed mutations for xi auxiliary nonvanishing and log transport."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/XiLogError.lean"
)


class ContractError(RuntimeError):
    """The xi logarithmic-error contract changed."""


def validate(text: str) -> None:
    required = {
        "huge cutoff consequence":
            "private theorem leanSaddleSector_norm_ge_ten_pow_eighty",
        "explicit half bound":
            "theorem manuscriptXiCoefficientRelativeError_norm_le_half",
        "half conclusion":
            "‖manuscriptXiCoefficientRelativeError M‖ ≤ 1 / 2 := by",
        "coefficient bound source":
            "manuscriptXiCoefficientRelativeError_norm_le hM",
        "nonzero correction":
            "theorem one_add_manuscriptXiCoefficientRelativeError_ne_zero",
        "right-half-plane correction":
            "theorem one_add_manuscriptXiCoefficientRelativeError_re_pos",
        "auxiliary nonzero": "theorem complexXiAuxiliaryMoment_ne_zero",
        "auxiliary factorization source":
            "complexXiAuxiliaryMoment_manuscript_factorization hM",
        "logarithmic error": "def manuscriptXiLogRelativeError (M : ℂ)",
        "correct logarithm argument":
            "log (1 + manuscriptXiCoefficientRelativeError M)",
        "exponential identity": "theorem exp_manuscriptXiLogRelativeError",
        "log holomorphy":
            "theorem differentiableAt_manuscriptXiLogRelativeError",
        "slit-plane guard":
            "one_add_manuscriptXiCoefficientRelativeError_re_pos hM",
        "sector holomorphy":
            "theorem differentiableOn_manuscriptXiLogRelativeError",
        "three-halves bound": "Complex.norm_log_one_add_half_le_self",
        "order-six transport":
            "theorem manuscriptXiLogRelativeError_derivatives_through_six\n",
        "paper radius geometry":
            "have hD : D ⊆ leanXiCoefficientSector :=\n"
            "    manuscriptCauchy_closedBall_subset_sector hx",
        "uniform error source": "manuscriptCauchy_error_norm_le hx hzD",
        "interior radius":
            "def manuscriptInteriorCauchyRadius (x : ℝ) : ℝ := x / 2000",
        "nested-disc geometry":
            "theorem manuscriptInterior_closedBall_subset_manuscriptDisc",
        "metric triangle source": "dist_triangle _ _ _",
        "uniform complex transport":
            "theorem manuscriptXiLogRelativeError_derivatives_through_six_on_half_disc",
        "uniform inner denominator":
            "manuscriptInteriorCauchyRadius x ^ j := by",
        "uniform sector containment":
            "hDinner.trans (manuscriptCauchy_closedBall_subset_sector hx)",
    }
    for label, needle in required.items():
        if text.count(needle) != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T6 xi logarithmic-error source contract")
    mutations = {
        "cutoff consequence removed": (
            "private theorem leanSaddleSector_norm_ge_ten_pow_eighty",
            "private theorem uncheckedHugeCutoff",
        ),
        "half bound weakened": (
            "‖manuscriptXiCoefficientRelativeError M‖ ≤ 1 / 2 := by",
            "‖manuscriptXiCoefficientRelativeError M‖ ≤ 3 / 4 := by",
        ),
        "coefficient bound disconnected": (
            "manuscriptXiCoefficientRelativeError_norm_le hM",
            "uncheckedCoefficientBound hM",
        ),
        "nonzero correction removed": (
            "theorem one_add_manuscriptXiCoefficientRelativeError_ne_zero",
            "theorem uncheckedCorrectionNonzero",
        ),
        "right-half-plane guard removed": (
            "theorem one_add_manuscriptXiCoefficientRelativeError_re_pos",
            "theorem uncheckedCorrectionHalfPlane",
        ),
        "auxiliary nonzero removed": (
            "theorem complexXiAuxiliaryMoment_ne_zero",
            "theorem uncheckedAuxiliaryNonzero",
        ),
        "factorization disconnected": (
            "complexXiAuxiliaryMoment_manuscript_factorization hM",
            "uncheckedAuxiliaryFactorization hM",
        ),
        "wrong logarithm": (
            "log (1 + manuscriptXiCoefficientRelativeError M)",
            "log (manuscriptXiCoefficientRelativeError M)",
        ),
        "exponential identity removed": (
            "theorem exp_manuscriptXiLogRelativeError",
            "theorem uncheckedLogExponential",
        ),
        "log holomorphy removed": (
            "theorem differentiableAt_manuscriptXiLogRelativeError",
            "theorem uncheckedLogHolomorphy",
        ),
        "sharp bound disconnected": (
            "Complex.norm_log_one_add_half_le_self",
            "uncheckedLogBound",
        ),
        "interior radius changed": (
            "def manuscriptInteriorCauchyRadius (x : ℝ) : ℝ := x / 2000",
            "def manuscriptInteriorCauchyRadius (x : ℝ) : ℝ := x / 1000",
        ),
        "nested geometry removed": (
            "theorem manuscriptInterior_closedBall_subset_manuscriptDisc",
            "theorem uncheckedNestedDiscGeometry",
        ),
        "metric triangle disconnected": (
            "dist_triangle _ _ _",
            "uncheckedDistTriangle _ _ _",
        ),
        "uniform complex transport removed": (
            "theorem manuscriptXiLogRelativeError_derivatives_through_six_on_half_disc",
            "theorem uncheckedUniformComplexTransport",
        ),
        "uniform denominator weakened": (
            "manuscriptInteriorCauchyRadius x ^ j := by",
            "manuscriptCauchyRadius x ^ j := by",
        ),
        "uniform sector containment disconnected": (
            "hDinner.trans (manuscriptCauchy_closedBall_subset_sector hx)",
            "uncheckedUniformSectorContainment hx",
        ),
        "disc geometry disconnected": (
            "have hD : D ⊆ leanXiCoefficientSector :=\n"
            "    manuscriptCauchy_closedBall_subset_sector hx",
            "have hD : D ⊆ leanXiCoefficientSector :=\n"
            "    uncheckedDiscGeometry hx",
        ),
        "uniform error disconnected": (
            "manuscriptCauchy_error_norm_le hx hzD",
            "uncheckedDiscError hx hzD",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 xi-log mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
