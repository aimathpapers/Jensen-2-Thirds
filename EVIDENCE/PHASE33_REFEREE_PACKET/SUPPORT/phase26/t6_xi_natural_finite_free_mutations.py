#!/usr/bin/env python3
"""Fail closed on the exact xi finite-free and root-localization bridge."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge/XiNaturalFiniteFreeSpecialization.lean"
)


class ContractError(RuntimeError):
    """The finite-free specialization source contract changed."""


REQUIRED = {
    "exact factor magnitude": "def jacobiFactorMagnitude (U V scale : ℝ)",
    "scaled factor convention": "((U + k) * scale) / (U * (V + k))",
    "finite-free coefficient convolution": "theorem coeff_finiteFree_jacobiFactors",
    "terminating coefficient identity": (
        "theorem terminating3F2Coefficient_eq_jacobiMagnitudes"
    ),
    "exact finite-free identity": (
        "theorem terminating3F2Polynomial_eq_finiteFree_jacobiFactors"
    ),
    "xi comparison identity": (
        "theorem xiNaturalComparisonPolynomial_eq_finiteFree"
    ),
    "narrow MSS input": "structure MSSFiniteFreeIntervalInput",
    "narrow classical boundary": "structure XiNaturalClassicalRootInputs",
    "second-factor D scaling": (
        "(residualParameterD y n (1 / L))\n"
        "      (residualParameterD y n (1 / L))) d"
    ),
    "MMP root producer": "I.mmp.hasDistinctPositiveRoots",
    "MSS product consumer": "I.mss.product_interval",
    "corrected localization constant": (
        "productDeviation_le_localizationConstant"
    ),
    "coarse 256 geometry": "structure XiNaturalFiniteFreeGeometry",
    "wedge constant": "def xiNaturalFiniteFreeWedgeConstant : ℝ := 2 * 256 ^ 3",
    "wedge-to-geometry": "theorem twoThirdsWedge_n_ge_256_mul_degree",
    "explicit cutoff geometry": (
        "theorem xiNaturalFiniteFreeGeometry_of_explicitCutoff"
    ),
    "explicit cutoff localization": (
        "comparison_root_localization_of_explicitCutoff"
    ),
}


def validate(source: str) -> None:
    for label, needle in REQUIRED.items():
        if needle not in source:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS exact xi finite-free specialization source contract")
    mutations = {
        "factor scaling removed": (
            "((U + k) * scale) / (U * (V + k))",
            "(U + k) / (U * (V + k))",
        ),
        "finite-free convolution disconnected": (
            "theorem coeff_finiteFree_jacobiFactors",
            "theorem uncheckedFiniteFreeConvolution",
        ),
        "3F2 factor identity disconnected": (
            "theorem terminating3F2Polynomial_eq_finiteFree_jacobiFactors",
            "theorem uncheckedTerminatingFiniteFreeIdentity",
        ),
        "xi comparison identity disconnected": (
            "theorem xiNaturalComparisonPolynomial_eq_finiteFree",
            "theorem uncheckedXiComparisonFiniteFreeIdentity",
        ),
        "MSS input hidden": (
            "structure MSSFiniteFreeIntervalInput",
            "structure UncheckedFiniteFreeIntervalInput",
        ),
        "classical boundary hidden": (
            "structure XiNaturalClassicalRootInputs",
            "structure UncheckedXiNaturalClassicalRootInputs",
        ),
        "MMP root producer bypassed": (
            "I.mmp.hasDistinctPositiveRoots",
            "uncheckedDistinctPositiveRoots",
        ),
        "MSS product consumer bypassed": (
            "I.mss.product_interval",
            "uncheckedProductInterval",
        ),
        "localization constant consumer bypassed": (
            "productDeviation_le_localizationConstant",
            "uncheckedProductDeviation",
        ),
        "geometry weakened": (
            "structure XiNaturalFiniteFreeGeometry",
            "structure UncheckedXiNaturalFiniteFreeGeometry",
        ),
        "wedge constant changed": (
            "2 * 256 ^ 3",
            "256 ^ 3",
        ),
        "wedge bridge disconnected": (
            "theorem twoThirdsWedge_n_ge_256_mul_degree",
            "theorem uncheckedWedgeDegreeBound",
        ),
        "explicit localization disconnected": (
            "comparison_root_localization_of_explicitCutoff",
            "uncheckedComparisonRootLocalization",
        ),
    }
    for label, (old, new) in mutations.items():
        if old not in source:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS finite-free mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
