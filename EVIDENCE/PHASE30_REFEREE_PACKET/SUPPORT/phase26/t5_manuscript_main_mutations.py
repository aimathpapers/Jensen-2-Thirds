#!/usr/bin/env python3
"""Fail-closed source mutations for the exact manuscript-main bridge."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ManuscriptCoefficientMain.lean"
)


class ContractError(RuntimeError):
    """The exact manuscript-main contract changed."""


def validate(text: str) -> None:
    required = {
        "displayed saddle main": "def manuscriptSaddleMain (s : ℂ)",
        "displayed elementary main":
            "def manuscriptCoefficientElementaryMain (M : ℂ)",
        "displayed complete main": "def manuscriptXiCoefficientMain (M : ℂ)",
        "reindex correction": "def coefficientReindexCorrection (N : ℂ)",
        "paper reindex exponent":
            "(N + 1 / 2) * log N - (N + 3 / 2) * log (N + 2)",
        "Gaussian correction": "def coefficientGaussianCorrection (N : ℂ)",
        "Gaussian exponent": "exp (1 / (2 * K))",
        "cancellation correction":
            "def coefficientCancellationCorrection (N : ℂ)",
        "cancellation sign":
            "1 - quantitativeSaddleBranch N ^ 2 / coefficientMomentMultiplier N",
        "combined correction": "def manuscriptMainCorrection (M : ℂ)",
        "saddle exact bridge":
            "theorem saddleMomentMain_eq_manuscriptSaddleMain_mul_correction",
        "elementary exact bridge":
            "theorem complexFactorialMain_mul_dyadic_mul_multiplier_eq_manuscript",
        "factorial producer": "complexFactorialRatioMain M * coefficientDyadicScale M",
        "moment multiplier producer":
            "coefficientMomentMultiplier (coefficientMellinParameter M)",
        "complete exact bridge":
            "theorem complexXiCoefficientMain_eq_manuscript_mul_correction",
        "saddle producer":
            "saddleMomentMain_eq_manuscriptSaddleMain_mul_correction hN",
        "prefactor producer":
            "complexFactorialMain_mul_dyadic_mul_multiplier_eq_manuscript hM",
    }
    counts = {
        "factorial producer": 6,
    }
    for label, needle in required.items():
        if text.count(needle) != counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 exact manuscript-main source contract")
    mutations = {
        "saddle main removed": (
            "def manuscriptSaddleMain (s : ℂ)",
            "def uncheckedSaddleMain (s : ℂ)",
        ),
        "reindex exponent shifted": (
            "(N + 1 / 2) * log N - (N + 3 / 2) * log (N + 2)",
            "(N + 1 / 2) * log N - (N + 1 / 2) * log (N + 2)",
        ),
        "Gaussian correction sign changed": (
            "exp (1 / (2 * K))",
            "exp (-(1 / (2 * K)))",
        ),
        "cancellation sign changed": (
            "1 - quantitativeSaddleBranch N ^ 2 / coefficientMomentMultiplier N",
            "1 + quantitativeSaddleBranch N ^ 2 / coefficientMomentMultiplier N",
        ),
        "combined correction removed": (
            "def manuscriptMainCorrection (M : ℂ)",
            "def uncheckedMainCorrection (M : ℂ)",
        ),
        "saddle bridge removed": (
            "theorem saddleMomentMain_eq_manuscriptSaddleMain_mul_correction",
            "theorem uncheckedSaddleBridge",
        ),
        "elementary bridge removed": (
            "theorem complexFactorialMain_mul_dyadic_mul_multiplier_eq_manuscript",
            "theorem uncheckedElementaryBridge",
        ),
        "factorial source disconnected": (
            "complexFactorialRatioMain M * coefficientDyadicScale M",
            "uncheckedFactorialMain M * coefficientDyadicScale M",
        ),
        "moment multiplier disconnected": (
            "coefficientMomentMultiplier (coefficientMellinParameter M)",
            "uncheckedMomentMultiplier (coefficientMellinParameter M)",
        ),
        "complete bridge removed": (
            "theorem complexXiCoefficientMain_eq_manuscript_mul_correction",
            "theorem uncheckedCompleteBridge",
        ),
        "saddle producer disconnected": (
            "saddleMomentMain_eq_manuscriptSaddleMain_mul_correction hN",
            "uncheckedSaddleBridge hN",
        ),
        "prefactor producer disconnected": (
            "complexFactorialMain_mul_dyadic_mul_multiplier_eq_manuscript hM",
            "uncheckedPrefactorBridge hM",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 manuscript-main mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
