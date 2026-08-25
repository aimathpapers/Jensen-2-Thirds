#!/usr/bin/env python3
"""Fail-closed mutations for the exact sixth-residual assembly."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/SixthResidualAssembly.lean"
)


class ContractError(RuntimeError):
    """The sixth-residual source contract changed."""


def validate(text: str) -> None:
    required = {
        "sixth tail summability": "theorem shiftedSixthPowerTail_summable",
        "sixth tail bound": "theorem shiftedSixthPowerTail_le",
        "fifth-power integral constant":
            "1 / (5 * (((n - 1 : ℕ) : ℝ) ^ 5)) := by",
        "single series bound": "theorem polygammaFiveSeries_norm_le",
        "single derivative bound":
            "theorem iteratedDeriv_five_digamma_norm_le",
        "exact single-tail constant":
            ("24 / (((n - 1 : ℕ) : ℝ) ^ 5) := by", 3),
        "displayed residual": "def manuscriptSixthResidualValue",
        "half-shift term":
            ("iteratedDeriv 5 Complex.digamma ((n : ℂ) + 1 / 2 + z)", 8),
        "paired regrouping":
            "theorem manuscriptSixthResidualValue_eq_paired",
        "residual inequality":
            ("theorem manuscriptSixthResidualValue_norm_le", 2),
        "paired derivative source":
            ("iteratedDeriv_five_digamma_pair_norm_le hm hB hC", 2),
        "distant tail source":
            "iteratedDeriv_five_digamma_norm_le hm hA",
        "xi log decomposition": "def manuscriptXiSixthLogDecomposition",
        "actual log error":
            "iteratedDeriv 6 manuscriptXiLogRelativeError z",
        "uniform xi decomposition":
            "theorem manuscriptXiSixthLogDecomposition_norm_le",
        "uniform complex source":
            "manuscriptXiLogRelativeError_derivatives_through_six_on_half_disc",
        "end-to-end residual":
            "theorem manuscriptSixthResidualValue_of_xiDecomposition_norm_le",
        "translated xi-log point":
            "manuscriptXiSixthLogDecomposition mainSix ((n : ℂ) + z)",
        "honest remaining input":
            "Only the moving-saddle\n"
            "sixth derivative remains as the explicit `mainSix` input.",
    }
    for label, contract in required.items():
        if isinstance(contract, tuple):
            needle, expected = contract
        else:
            needle, expected = contract, 1
        if text.count(needle) != expected:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T6 sixth-residual source contract")
    mutations = {
        "sixth tail removed": (
            "theorem shiftedSixthPowerTail_le",
            "theorem uncheckedSixthPowerTail",
        ),
        "integral constant changed": (
            "1 / (5 * (((n - 1 : ℕ) : ℝ) ^ 5)) := by",
            "1 / (6 * (((n - 1 : ℕ) : ℝ) ^ 5)) := by",
        ),
        "single series bound removed": (
            "theorem polygammaFiveSeries_norm_le",
            "theorem uncheckedSingleSeriesBound",
        ),
        "single derivative bound removed": (
            "theorem iteratedDeriv_five_digamma_norm_le",
            "theorem uncheckedSingleDerivativeBound",
        ),
        "single-tail exponent changed": (
            "24 / (((n - 1 : ℕ) : ℝ) ^ 5) := by",
            "24 / (((n - 1 : ℕ) : ℝ) ^ 4) := by",
        ),
        "displayed residual removed": (
            "def manuscriptSixthResidualValue",
            "def uncheckedSixthResidualValue",
        ),
        "half shift dropped": (
            "iteratedDeriv 5 Complex.digamma ((n : ℂ) + 1 / 2 + z)",
            "iteratedDeriv 5 Complex.digamma ((n : ℂ) + z)",
        ),
        "pairing identity removed": (
            "theorem manuscriptSixthResidualValue_eq_paired",
            "theorem uncheckedResidualPairing",
        ),
        "residual inequality removed": (
            "theorem manuscriptSixthResidualValue_norm_le",
            "theorem uncheckedResidualNormBound",
        ),
        "paired source disconnected": (
            "iteratedDeriv_five_digamma_pair_norm_le hm hB hC",
            "uncheckedPairBound hm hB hC",
        ),
        "distant tail disconnected": (
            "iteratedDeriv_five_digamma_norm_le hm hA",
            "uncheckedDistantTail hm hA",
        ),
        "xi decomposition removed": (
            "def manuscriptXiSixthLogDecomposition",
            "def uncheckedXiSixthLogDecomposition",
        ),
        "wrong error order": (
            "iteratedDeriv 6 manuscriptXiLogRelativeError z",
            "iteratedDeriv 5 manuscriptXiLogRelativeError z",
        ),
        "uniform complex source disconnected": (
            "manuscriptXiLogRelativeError_derivatives_through_six_on_half_disc",
            "uncheckedUniformXiLogDerivative",
        ),
        "end-to-end theorem removed": (
            "theorem manuscriptSixthResidualValue_of_xiDecomposition_norm_le",
            "theorem uncheckedEndToEndResidual",
        ),
        "xi-log translation dropped": (
            "manuscriptXiSixthLogDecomposition mainSix ((n : ℂ) + z)",
            "manuscriptXiSixthLogDecomposition mainSix z",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 sixth-residual mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
