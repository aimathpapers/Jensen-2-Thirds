#!/usr/bin/env python3
"""Fail closed on xi critical-point localization and radius closure."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge/XiNaturalCriticalRadius.lean"
)


class ContractError(RuntimeError):
    """The xi critical-radius source contract changed."""


REQUIRED = {
    "complete roots": "roots_eq_of_natDegree_le_card_of_ne_zero",
    "degree saturation": "have hnatDegree : p.natDegree = d",
    "log derivative": "eval_derivative_div_eval_of_ne_zero",
    "left sign": "apply Finset.sum_neg",
    "right sign": "apply Finset.sum_pos",
    "critical localization": "theorem XiNaturalClassicalRootInputs.comparison_critical_localization",
    "explicit critical localization": "comparison_critical_localization_of_explicitCutoff",
    "wedge constant": "2 * 824633720832 ^ 3",
    "scale constant": "524288 * Real.sqrt",
    "branch geometry": "criticalRadiusParameterGeometry_of_explicitCutoff",
    "literal normalization": "polynomialDerivativeRatio (xiNaturalComparisonPolynomial",
    "final radius": "theorem xiNaturalComparison_critical_radius_of_explicitCutoff",
}


def validate(source: str) -> None:
    for label, needle in REQUIRED.items():
        if needle not in source:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS xi critical-point localization and radius source contract")
    mutations = {
        "root completeness removed": (
            "roots_eq_of_natDegree_le_card_of_ne_zero",
            "uncheckedRootsEq",
        ),
        "degree saturation hidden": (
            "have hnatDegree : p.natDegree = d",
            "have uncheckedNatDegree : p.natDegree = d",
        ),
        "log derivative disconnected": (
            "eval_derivative_div_eval_of_ne_zero",
            "uncheckedLogDerivative",
        ),
        "left sign weakened": ("apply Finset.sum_neg", "apply Finset.sum_nonpos"),
        "right sign weakened": ("apply Finset.sum_pos", "apply Finset.sum_nonneg"),
        "critical localization hidden": (
            "theorem XiNaturalClassicalRootInputs.comparison_critical_localization",
            "theorem XiNaturalClassicalRootInputs.uncheckedCriticalLocalization",
        ),
        "explicit localization hidden": (
            "comparison_critical_localization_of_explicitCutoff",
            "uncheckedCriticalLocalizationOfCutoff",
        ),
        "wedge constant halved": (
            "2 * 824633720832 ^ 3",
            "824633720832 ^ 3",
        ),
        "scale threshold halved": (
            "524288 * Real.sqrt",
            "262144 * Real.sqrt",
        ),
        "branch geometry hidden": (
            "criticalRadiusParameterGeometry_of_explicitCutoff",
            "uncheckedCriticalRadiusGeometry",
        ),
        "normalization transposed": (
            "polynomialDerivativeRatio (xiNaturalComparisonPolynomial",
            "uncheckedDerivativeRatio (xiNaturalComparisonPolynomial",
        ),
        "final theorem hidden": (
            "theorem xiNaturalComparison_critical_radius_of_explicitCutoff",
            "theorem uncheckedXiCriticalRadius",
        ),
    }
    for label, (old, new) in mutations.items():
        if old not in source:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS xi critical-radius mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
