#!/usr/bin/env python3
"""Fail-closed source mutations for the manuscript-normalized T5 theorem."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ManuscriptCoefficientTheorem.lean"
)


class ContractError(RuntimeError):
    """The manuscript theorem source contract changed."""


def validate(text: str) -> None:
    required = {
        "explicit relative error":
            "def manuscriptXiCoefficientRelativeError (M : ℂ)",
        "cross-term normalization":
            "manuscriptMainCorrection M * (1 + complexXiCoefficientRelativeError M) - 1",
        "explicit error constant":
            "20 + 21 * complexXiCoefficientErrorCoefficient",
        "exact factorization":
            "theorem complexXiCoefficientMoment_manuscript_factorization",
        "factored theorem source":
            "complexXiCoefficientMoment_factorization hM",
        "exact-main bridge source":
            "complexXiCoefficientMain_eq_manuscript_mul_correction hM",
        "displayed main nonzero":
            "theorem manuscriptXiCoefficientMain_ne_zero",
        "relative error bound":
            "theorem manuscriptXiCoefficientRelativeError_norm_le",
        "correction estimate source":
            "manuscriptMainCorrection_sub_one_norm_le hM",
        "factored error estimate source":
            "complexXiCoefficientRelativeError_norm_le hM",
        "pointwise export":
            "theorem complexXiCoefficient_manuscript_sector_asymptotic",
        "reindex holomorphy":
            "theorem differentiableAt_coefficientReindexCorrection",
        "Gaussian holomorphy":
            "theorem differentiableAt_coefficientGaussianCorrection",
        "curvature derivative source":
            "hasDerivAt_saddleCurvatureAlong hN",
        "cancellation holomorphy":
            "theorem differentiableAt_coefficientCancellationCorrection",
        "branch derivative source":
            "hasDerivAt_quantitativeSaddleBranch hN",
        "combined correction holomorphy":
            "theorem differentiableAt_manuscriptMainCorrection",
        "correction nonzero":
            "theorem manuscriptMainCorrection_ne_zero",
        "displayed main holomorphy":
            "theorem differentiableAt_manuscriptXiCoefficientMain",
        "relative error holomorphy":
            "theorem differentiableAt_manuscriptXiCoefficientRelativeError",
        "generic quotient witness":
            "holomorphicRelativeError complexXiCoefficientMoment",
        "holomorphic export":
            "theorem complexXiCoefficient_manuscript_sector_holomorphic_asymptotic",
    }
    counts = {
        "exact-main bridge source": 3,
        "generic quotient witness": 2,
    }
    for label, needle in required.items():
        if text.count(needle) != counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 manuscript-theorem source contract")
    mutations = {
        "relative error removed": (
            "def manuscriptXiCoefficientRelativeError (M : ℂ)",
            "def uncheckedRelativeError (M : ℂ)",
        ),
        "cross term dropped": (
            "manuscriptMainCorrection M * (1 + complexXiCoefficientRelativeError M) - 1",
            "manuscriptMainCorrection M + complexXiCoefficientRelativeError M - 1",
        ),
        "constant weakened": (
            "20 + 21 * complexXiCoefficientErrorCoefficient",
            "20 + 20 * complexXiCoefficientErrorCoefficient",
        ),
        "factorization disconnected": (
            "complexXiCoefficientMoment_factorization hM",
            "uncheckedFactoredTheorem hM",
        ),
        "main bridge disconnected": (
            "complexXiCoefficientMain_eq_manuscript_mul_correction hM",
            "uncheckedMainBridge hM",
        ),
        "correction bound disconnected": (
            "manuscriptMainCorrection_sub_one_norm_le hM",
            "uncheckedCorrectionBound hM",
        ),
        "factored error bound disconnected": (
            "complexXiCoefficientRelativeError_norm_le hM",
            "uncheckedFactoredErrorBound hM",
        ),
        "pointwise export removed": (
            "theorem complexXiCoefficient_manuscript_sector_asymptotic",
            "theorem uncheckedPointwiseExport",
        ),
        "curvature derivative disconnected": (
            "hasDerivAt_saddleCurvatureAlong hN",
            "uncheckedCurvatureDerivative hN",
        ),
        "branch derivative disconnected": (
            "hasDerivAt_quantitativeSaddleBranch hN",
            "uncheckedBranchDerivative hN",
        ),
        "correction holomorphy removed": (
            "theorem differentiableAt_manuscriptMainCorrection",
            "theorem uncheckedCorrectionHolomorphy",
        ),
        "correction nonzero removed": (
            "theorem manuscriptMainCorrection_ne_zero",
            "theorem uncheckedCorrectionNonzero",
        ),
        "displayed main holomorphy removed": (
            "theorem differentiableAt_manuscriptXiCoefficientMain",
            "theorem uncheckedMainHolomorphy",
        ),
        "relative error holomorphy removed": (
            "theorem differentiableAt_manuscriptXiCoefficientRelativeError",
            "theorem uncheckedErrorHolomorphy",
        ),
        "holomorphic export removed": (
            "theorem complexXiCoefficient_manuscript_sector_holomorphic_asymptotic",
            "theorem uncheckedHolomorphicExport",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 manuscript-theorem mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
