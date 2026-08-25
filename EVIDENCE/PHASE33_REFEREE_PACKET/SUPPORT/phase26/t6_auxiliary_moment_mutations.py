#!/usr/bin/env python3
"""Fail-closed mutations for the exact xi auxiliary-moment bridge."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/XiAuxiliaryMoment.lean"
)


class ContractError(RuntimeError):
    """The auxiliary-moment source contract changed."""


def validate(text: str) -> None:
    required = {
        "auxiliary moment": "def complexXiAuxiliaryMoment (M : ℂ)",
        "exact dyadic factor": "coefficientDyadicScale M *",
        "lower shifted moment": "coefficientMomentMultiplier N * fullThetaMoment N",
        "upper shifted moment": "fullThetaMoment (N + 2)",
        "quotient main": "def manuscriptXiAuxiliaryMain (M : ℂ)",
        "exact gamma removal":
            "manuscriptXiCoefficientMain M / complexFactorialRatio M",
        "right-half-plane nonzero":
            "theorem complexFactorialRatio_ne_zero_of_re_pos",
        "sector nonzero":
            "theorem complexFactorialRatio_ne_zero_of_mem_leanXiCoefficientSector",
        "exact coefficient bridge":
            "theorem complexXiCoefficientMoment_eq_factorialRatio_mul_auxiliary",
        "integer specialization":
            "theorem complexFactorialRatio_mul_auxiliary_nat_succ",
        "T1 source": "complexXiCoefficientMoment_nat_succ",
        "same error factorization":
            "theorem complexXiAuxiliaryMoment_manuscript_factorization",
        "coefficient theorem source":
            "complexXiCoefficientMoment_manuscript_factorization hM",
        "auxiliary main nonzero": "theorem manuscriptXiAuxiliaryMain_ne_zero",
        "actual holomorphy": "theorem differentiableAt_complexXiAuxiliaryMoment",
        "main holomorphy": "theorem differentiableAt_manuscriptXiAuxiliaryMain",
        "sector holomorphic export":
            "theorem complexXiAuxiliaryMoment_manuscript_sector_holomorphic_asymptotic",
        "explicit error bound": "manuscriptXiCoefficientRelativeError_norm_le hM",
        "order-six export":
            "theorem complexXiAuxiliaryMoment_relativeError_derivatives_through_six",
        "all six orders": "∀ j ≤ 6",
        "order-six source":
            "manuscriptXiCoefficientRelativeError_derivatives_through_six hx",
    }
    for label, needle in required.items():
        if text.count(needle) != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T6 auxiliary-moment source contract")
    mutations = {
        "dyadic factor removed": (
            "coefficientDyadicScale M *",
            "1 *",
        ),
        "shift changed": (
            "fullThetaMoment (N + 2)",
            "fullThetaMoment (N + 3)",
        ),
        "gamma divisor changed": (
            "manuscriptXiCoefficientMain M / complexFactorialRatio M",
            "manuscriptXiCoefficientMain M / complexFactorialRatioMain M",
        ),
        "right-half-plane nonzero removed": (
            "theorem complexFactorialRatio_ne_zero_of_re_pos",
            "theorem uncheckedFactorialRatioNonzero",
        ),
        "exact bridge removed": (
            "theorem complexXiCoefficientMoment_eq_factorialRatio_mul_auxiliary",
            "theorem uncheckedCoefficientBridge",
        ),
        "integer seam disconnected": (
            "complexXiCoefficientMoment_nat_succ",
            "uncheckedIntegerCoefficientSeam",
        ),
        "factorization removed": (
            "theorem complexXiAuxiliaryMoment_manuscript_factorization",
            "theorem uncheckedAuxiliaryFactorization",
        ),
        "coefficient theorem disconnected": (
            "complexXiCoefficientMoment_manuscript_factorization hM",
            "uncheckedCoefficientTheorem hM",
        ),
        "main nonzero removed": (
            "theorem manuscriptXiAuxiliaryMain_ne_zero",
            "theorem uncheckedAuxiliaryMainNonzero",
        ),
        "actual holomorphy removed": (
            "theorem differentiableAt_complexXiAuxiliaryMoment",
            "theorem uncheckedAuxiliaryHolomorphy",
        ),
        "main holomorphy removed": (
            "theorem differentiableAt_manuscriptXiAuxiliaryMain",
            "theorem uncheckedAuxiliaryMainHolomorphy",
        ),
        "sector theorem removed": (
            "theorem complexXiAuxiliaryMoment_manuscript_sector_holomorphic_asymptotic",
            "theorem uncheckedAuxiliarySectorTheorem",
        ),
        "error bound disconnected": (
            "manuscriptXiCoefficientRelativeError_norm_le hM",
            "uncheckedAuxiliaryErrorBound hM",
        ),
        "order six weakened": ("∀ j ≤ 6", "∀ j ≤ 5"),
        "Cauchy transport disconnected": (
            "manuscriptXiCoefficientRelativeError_derivatives_through_six hx",
            "uncheckedOrderSixTransport hx",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 auxiliary-moment mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
