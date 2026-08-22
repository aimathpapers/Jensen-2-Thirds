#!/usr/bin/env python3
"""Fail-closed source mutations for the normalized complex Gamma quotient."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/GammaRatioStirling.lean"
)


class ContractError(RuntimeError):
    """The complex Gamma-ratio differential contract changed."""


def validate(text: str) -> None:
    required = {
        "exact Gamma quotient": "def complexFactorialRatio (z : ℂ)",
        "Gamma quotient denominator": "Complex.Gamma (2 * z + 1)",
        "elementary log main": "def complexFactorialRatioLogMain (z : ℂ)",
        "multiplicative correction": "def complexFactorialRatioCorrection (z : ℂ)",
        "all-point residual": "def digammaStirlingResidual (z : ℂ)",
        "residual half term": "+ (1 / 2 : ℂ) / z",
        "two-scale error":
            "digammaStirlingResidual z - 2 * digammaStirlingResidual (2 * z)",
        "Gamma producer": "Complex.differentiableAt_Gamma",
        "digamma recurrence": "Complex.digamma_apply_add_one",
        "quotient derivative":
            "theorem hasDerivAt_complexFactorialRatioCorrection",
        "all-point bound first scale": "using digamma_stirling_re_all hz\n",
        "all-point bound doubled scale": "using digamma_stirling_re_all hz2",
        "final bound": "theorem norm_gammaRatioLogDerivError_le",
        "final constant": "‖gammaRatioLogDerivError z‖ ≤ 3 / z.re ^ 2",
        "integer quotient anchor": "theorem complexFactorialRatio_natCast",
        "integer main anchor": "theorem complexFactorialRatioMain_natCast",
        "Robbins correction anchor":
            "theorem complexFactorialRatioCorrection_natCast",
        "Gronwall transport": "norm_le_gronwallBound_of_norm_deriv_right_le",
        "segment derivative bound":
            "theorem norm_gammaRatioAnchorPathD1_le_three_fortieth",
        "floor anchor": "theorem leanCoefficientSector_floor_anchor",
        "sector geometry producer":
            "leanSaddleSector_parameter_component_bounds hsaddle",
        "final sector theorem":
            "theorem complexFactorialRatio_relative_error_fixedSector",
        "final sector rate": "‖error‖ ≤ 1 / ‖z‖",
    }
    counts = {
        "digamma recurrence": 2,
    }
    for label, needle in required.items():
        if text.count(needle) != counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 complex Gamma-ratio differential source contract")
    mutations = {
        "Gamma quotient denominator changed": (
            "Complex.Gamma (2 * z + 1)", "Complex.Gamma (3 * z + 1)"
        ),
        "elementary log main removed": (
            "def complexFactorialRatioLogMain", "def uncheckedFactorialRatioLogMain"
        ),
        "residual half term removed": (
            "+ (1 / 2 : ℂ) / z", "+ (0 : ℂ) / z"
        ),
        "two-scale coefficient changed": (
            "digammaStirlingResidual z - 2 * digammaStirlingResidual (2 * z)",
            "digammaStirlingResidual z - 3 * digammaStirlingResidual (2 * z)",
        ),
        "Gamma producer disconnected": (
            "Complex.differentiableAt_Gamma", "uncheckedDifferentiableAtGamma"
        ),
        "digamma recurrence disconnected": (
            "Complex.digamma_apply_add_one", "uncheckedDigammaRecurrence"
        ),
        "correction derivative removed": (
            "theorem hasDerivAt_complexFactorialRatioCorrection",
            "theorem unchecked_complexFactorialRatioCorrection",
        ),
        "all-point residual bound disconnected": (
            "using digamma_stirling_re_all hz\n", "using unchecked_digamma_bound hz\n"
        ),
        "final constant weakened": (
            "‖gammaRatioLogDerivError z‖ ≤ 3 / z.re ^ 2",
            "‖gammaRatioLogDerivError z‖ ≤ 4 / z.re ^ 2",
        ),
        "integer quotient anchor removed": (
            "theorem complexFactorialRatio_natCast",
            "theorem unchecked_complexFactorialRatio_natCast",
        ),
        "integer main anchor removed": (
            "theorem complexFactorialRatioMain_natCast",
            "theorem unchecked_complexFactorialRatioMain_natCast",
        ),
        "Robbins anchor removed": (
            "theorem complexFactorialRatioCorrection_natCast",
            "theorem unchecked_complexFactorialRatioCorrection_natCast",
        ),
        "Gronwall producer disconnected": (
            "norm_le_gronwallBound_of_norm_deriv_right_le",
            "unchecked_gronwall_transport",
        ),
        "segment derivative constant changed": (
            "theorem norm_gammaRatioAnchorPathD1_le_three_fortieth",
            "theorem unchecked_gammaRatioAnchorPathD1_bound",
        ),
        "floor anchor removed": (
            "theorem leanCoefficientSector_floor_anchor",
            "theorem unchecked_leanCoefficientSector_floor_anchor",
        ),
        "sector geometry disconnected": (
            "leanSaddleSector_parameter_component_bounds hsaddle",
            "unchecked_sector_components hsaddle",
        ),
        "final sector theorem removed": (
            "theorem complexFactorialRatio_relative_error_fixedSector",
            "theorem unchecked_complexFactorialRatio_relative_error_fixedSector",
        ),
        "final sector rate weakened": (
            "‖error‖ ≤ 1 / ‖z‖",
            "‖error‖ ≤ 2 / ‖z‖",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 complex Gamma-ratio mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
