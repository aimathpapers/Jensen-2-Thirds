#!/usr/bin/env python3
"""Fail-closed mutations for fifth-polygamma derivative identification."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/PolygammaDerivative.lean"
)


class ContractError(RuntimeError):
    """The polygamma derivative-identification contract changed."""


def validate(text: str) -> None:
    required = {
        "term definition": "def inversePowerTerm (p k : ℕ) (z : ℂ)",
        "term derivative": "theorem hasDerivAt_inversePowerTerm",
        "normalized derivative": "theorem inversePowerTermDerivative_eq",
        "normalized exponent": (
            "inversePowerTermDerivative p k z =\n"
            "      -(p : ℂ) * inversePowerTerm (p + 1) k z := by"
        ),
        "series summability": "theorem summable_inversePowerSeries",
        "series derivative": "theorem hasDerivAt_inversePowerSeries",
        "uniform differentiation": "hasDerivAt_tsum_of_isPreconnected",
        "right-half-plane analyticity": "theorem analyticAt_digamma_rightHalfPlane",
        "trigamma extension": "theorem deriv_digamma_eq_inversePowerSeries_two",
        "integer split": "by_cases hmem : z ∈ Complex.integerComplement",
        "noninteger producer": "Zeta23.Stirling.hasSum_trigamma (humem n)",
        "holomorphic left limit": (
            "(analyticAt_digamma_rightHalfPlane hz0).deriv.continuousAt.tendsto.comp hu"
        ),
        "series right limit": (
            "(hasDerivAt_inversePowerSeries (p := 2) (by norm_num) hz).continuousAt.tendsto.comp hu"
        ),
        "tower theorem": "theorem iteratedDeriv_digamma_eq_inversePowerSeries",
        "tower coefficient": (
            "iteratedDeriv (m + 1) Complex.digamma z =\n"
            "      ((-1 : ℂ) ^ m * ((m + 1).factorial : ℂ)) *"
        ),
        "fifth identification": "theorem iteratedDeriv_five_digamma_eq_polygammaFiveSeries",
        "paired derivative theorem": "theorem iteratedDeriv_five_digamma_pair_norm_le",
        "paired producer": "polygammaFiveSeries_pair_norm_le hn hz hw",
    }
    for label, needle in required.items():
        if needle not in text:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS polygamma derivative-identification source contract")
    mutations = {
        "term derivative removed": (
            "theorem hasDerivAt_inversePowerTerm",
            "theorem uncheckedInversePowerTermDerivative",
        ),
        "normalized derivative removed": (
            "theorem inversePowerTermDerivative_eq",
            "theorem uncheckedNormalizedTermDerivative",
        ),
        "derivative exponent changed": (
            "inversePowerTermDerivative p k z =\n"
            "      -(p : ℂ) * inversePowerTerm (p + 1) k z := by",
            "inversePowerTermDerivative p k z =\n"
            "      -(p : ℂ) * inversePowerTerm p k z := by",
        ),
        "summability removed": (
            "theorem summable_inversePowerSeries",
            "theorem uncheckedInversePowerSummability",
        ),
        "series derivative removed": (
            "theorem hasDerivAt_inversePowerSeries",
            "theorem uncheckedInversePowerSeriesDerivative",
        ),
        "uniform differentiation disconnected": (
            "hasDerivAt_tsum_of_isPreconnected",
            "uncheckedTermwiseDifferentiation",
        ),
        "digamma analyticity removed": (
            "theorem analyticAt_digamma_rightHalfPlane",
            "theorem uncheckedDigammaAnalyticity",
        ),
        "trigamma extension removed": (
            "theorem deriv_digamma_eq_inversePowerSeries_two",
            "theorem uncheckedTrigammaExtension",
        ),
        "integer split removed": (
            "by_cases hmem : z ∈ Complex.integerComplement",
            "by_cases hmem : z = 0",
        ),
        "noninteger producer disconnected": (
            "Zeta23.Stirling.hasSum_trigamma (humem n)",
            "uncheckedTrigammaProducer (humem n)",
        ),
        "left continuity disconnected": (
            "(analyticAt_digamma_rightHalfPlane hz0).deriv.continuousAt.tendsto.comp hu",
            "uncheckedDigammaLimit hu",
        ),
        "right continuity disconnected": (
            "(hasDerivAt_inversePowerSeries (p := 2) (by norm_num) hz).continuousAt.tendsto.comp hu",
            "uncheckedSeriesLimit hu",
        ),
        "tower theorem removed": (
            "theorem iteratedDeriv_digamma_eq_inversePowerSeries",
            "theorem uncheckedPolygammaTower",
        ),
        "tower sign changed": (
            "iteratedDeriv (m + 1) Complex.digamma z =\n"
            "      ((-1 : ℂ) ^ m * ((m + 1).factorial : ℂ)) *",
            "iteratedDeriv (m + 1) Complex.digamma z =\n"
            "      ((1 : ℂ) ^ m * ((m + 1).factorial : ℂ)) *",
        ),
        "fifth identification removed": (
            "theorem iteratedDeriv_five_digamma_eq_polygammaFiveSeries",
            "theorem uncheckedFifthPolygamma",
        ),
        "paired theorem removed": (
            "theorem iteratedDeriv_five_digamma_pair_norm_le",
            "theorem uncheckedPairedFifthPolygamma",
        ),
        "paired producer disconnected": (
            "polygammaFiveSeries_pair_norm_le hn hz hw",
            "uncheckedPairingProducer hn hz hw",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS polygamma derivative mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
