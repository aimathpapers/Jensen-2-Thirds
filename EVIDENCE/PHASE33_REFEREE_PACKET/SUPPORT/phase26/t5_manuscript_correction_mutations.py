#!/usr/bin/env python3
"""Fail-closed mutations for the manuscript correction estimates."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ManuscriptCorrectionBounds.lean"
)


class ContractError(RuntimeError):
    """The correction-bound source contract changed."""


def validate(text: str) -> None:
    required = {
        "reindex logarithm": "def coefficientReindexLogError (N : ℂ)",
        "exponential character":
            "theorem coefficientReindexCorrection_eq_exp_logError",
        "exact second order expansion":
            "theorem coefficientReindexLogError_eq_rational_eps",
        "first remainder source":
            "Zeta23.StirlingVert.log_one_add_sub_log hNre",
        "second remainder source":
            "Zeta23.StirlingVert.log_one_add_sub_log hN1re",
        "right-half-plane remainder bound":
            "Zeta23.StirlingRight.norm_eps_zero_le_re",
        "sector real-part geometry":
            "theorem leanSaddleSector_norm_le_two_re",
        "cosine source": "Real.one_sub_sq_div_two_le_cos",
        "quadratic log bound":
            "theorem coefficientReindexLogError_norm_le",
        "reindex relative bound":
            "theorem coefficientReindexCorrection_sub_one_norm_le",
        "exponential remainder source": "Complex.norm_exp_sub_one_le hEone",
        "Gaussian relative bound":
            "theorem coefficientGaussianCorrection_sub_one_norm_le",
        "curvature source":
            "quantitativeSaddleBranch_curvature_inv_le_log_div_norm hN",
        "multiplier floor":
            "theorem coefficientMomentMultiplier_norm_lower",
        "cancellation relative bound":
            "theorem coefficientCancellationCorrection_sub_one_norm_le",
        "saddle logarithm source":
            "quantitativeSaddleBranch_norm_le_two_log_norm hN",
        "combined correction bound":
            "theorem manuscriptMainCorrection_sub_one_norm_le",
        "reindex bound consumer":
            "coefficientReindexCorrection_sub_one_norm_le hN",
        "Gaussian bound consumer":
            "coefficientGaussianCorrection_sub_one_norm_le hN",
        "cancellation bound consumer":
            "coefficientCancellationCorrection_sub_one_norm_le hN",
    }
    counts = {
        "right-half-plane remainder bound": 2,
    }
    for label, needle in required.items():
        if text.count(needle) != counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 manuscript-correction source contract")
    mutations = {
        "reindex logarithm removed": (
            "def coefficientReindexLogError (N : ℂ)",
            "def uncheckedReindexLogError (N : ℂ)",
        ),
        "exact expansion removed": (
            "theorem coefficientReindexLogError_eq_rational_eps",
            "theorem uncheckedReindexExpansion",
        ),
        "first logarithm remainder disconnected": (
            "Zeta23.StirlingVert.log_one_add_sub_log hNre",
            "uncheckedLogExpansion hNre",
        ),
        "remainder bound disconnected": (
            "Zeta23.StirlingRight.norm_eps_zero_le_re",
            "uncheckedEpsilonBound",
        ),
        "sector geometry removed": (
            "theorem leanSaddleSector_norm_le_two_re",
            "theorem uncheckedSectorGeometry",
        ),
        "cosine bound disconnected": (
            "Real.one_sub_sq_div_two_le_cos",
            "uncheckedCosineBound",
        ),
        "quadratic bound removed": (
            "theorem coefficientReindexLogError_norm_le",
            "theorem uncheckedReindexLogBound",
        ),
        "reindex estimate removed": (
            "theorem coefficientReindexCorrection_sub_one_norm_le",
            "theorem uncheckedReindexBound",
        ),
        "exponential estimate disconnected": (
            "Complex.norm_exp_sub_one_le hEone",
            "uncheckedExponentialBound hEone",
        ),
        "Gaussian estimate removed": (
            "theorem coefficientGaussianCorrection_sub_one_norm_le",
            "theorem uncheckedGaussianBound",
        ),
        "curvature estimate disconnected": (
            "quantitativeSaddleBranch_curvature_inv_le_log_div_norm hN",
            "uncheckedCurvatureBound hN",
        ),
        "multiplier floor removed": (
            "theorem coefficientMomentMultiplier_norm_lower",
            "theorem uncheckedMultiplierFloor",
        ),
        "cancellation estimate removed": (
            "theorem coefficientCancellationCorrection_sub_one_norm_le",
            "theorem uncheckedCancellationBound",
        ),
        "saddle estimate disconnected": (
            "quantitativeSaddleBranch_norm_le_two_log_norm hN",
            "uncheckedSaddleBound hN",
        ),
        "combined bound removed": (
            "theorem manuscriptMainCorrection_sub_one_norm_le",
            "theorem uncheckedCombinedCorrection",
        ),
        "reindex consumer disconnected": (
            "coefficientReindexCorrection_sub_one_norm_le hN",
            "uncheckedReindexConsumer hN",
        ),
        "Gaussian consumer disconnected": (
            "coefficientGaussianCorrection_sub_one_norm_le hN",
            "uncheckedGaussianConsumer hN",
        ),
        "cancellation consumer disconnected": (
            "coefficientCancellationCorrection_sub_one_norm_le hN",
            "uncheckedCancellationConsumer hN",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 manuscript-correction mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
