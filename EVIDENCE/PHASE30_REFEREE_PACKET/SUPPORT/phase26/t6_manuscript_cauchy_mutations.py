#!/usr/bin/env python3
"""Fail-closed mutations for the instantiated order-six Cauchy transport."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ManuscriptCauchyTransport.lean"
)


class ContractError(RuntimeError):
    """The manuscript Cauchy source contract changed."""


def validate(text: str) -> None:
    required = {
        "paper radius": "def manuscriptCauchyRadius (x : ℝ) : ℝ := x / 1000",
        "uniform epsilon": "def manuscriptCauchyEpsilon (x : ℝ)",
        "outer threshold": "Real.exp (leanSaddleCutoff + 2) < x",
        "paired disc containment":
            "theorem manuscriptCauchy_closedBall_subset_sector",
        "shifted parameter": "let N : ℂ := coefficientMellinParameter z",
        "M-angle bound": "|z.arg| < saddleOuterAngle",
        "N-angle bound": "|N.arg| < saddleOuterAngle",
        "shifted norm bounds": "theorem manuscriptCauchy_shifted_norm_bounds",
        "quotient identification":
            "theorem manuscriptXiCoefficientRelativeError_eq_holomorphicRelativeError",
        "uniform disc error": "theorem manuscriptCauchy_error_norm_le",
        "pointwise coefficient estimate":
            "manuscriptXiCoefficientRelativeError_norm_le hzSector",
        "order-six export":
            "theorem manuscriptXiCoefficientRelativeError_derivatives_through_six",
        "generic Cauchy producer": "relativeError_derivatives_through_six",
        "all six orders": "∀ j ≤ 6",
        "factorial-radius normalization":
            "j.factorial * manuscriptCauchyEpsilon x /",
        "sector holomorphy":
            "differentiableOn_complexXiCoefficientMoment.mono hD",
        "main holomorphy":
            "differentiableOn_manuscriptXiCoefficientMain.mono hD",
        "main nonvanishing":
            "manuscriptXiCoefficientMain_ne_zero (hD hz)",
    }
    counts = {
        "outer threshold": 5,
        "shifted parameter": 3,
    }
    for label, needle in required.items():
        if text.count(needle) != counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T6 manuscript-Cauchy source contract")
    mutations = {
        "radius changed": (
            "def manuscriptCauchyRadius (x : ℝ) : ℝ := x / 1000",
            "def manuscriptCauchyRadius (x : ℝ) : ℝ := x / 999",
        ),
        "disc containment removed": (
            "theorem manuscriptCauchy_closedBall_subset_sector",
            "theorem uncheckedDiscContainment",
        ),
        "shifted parameter disconnected": (
            "let N : ℂ := coefficientMellinParameter z",
            "let N : ℂ := z",
        ),
        "shifted norm bounds removed": (
            "theorem manuscriptCauchy_shifted_norm_bounds",
            "theorem uncheckedShiftedNormBounds",
        ),
        "quotient identification removed": (
            "theorem manuscriptXiCoefficientRelativeError_eq_holomorphicRelativeError",
            "theorem uncheckedQuotientIdentification",
        ),
        "uniform error removed": (
            "theorem manuscriptCauchy_error_norm_le",
            "theorem uncheckedUniformError",
        ),
        "pointwise source disconnected": (
            "manuscriptXiCoefficientRelativeError_norm_le hzSector",
            "uncheckedPointwiseError hzSector",
        ),
        "order six weakened": ("∀ j ≤ 6", "∀ j ≤ 5"),
        "factorial dropped": (
            "j.factorial * manuscriptCauchyEpsilon x /",
            "manuscriptCauchyEpsilon x /",
        ),
        "generic Cauchy disconnected": (
            "have htransport := relativeError_derivatives_through_six",
            "have htransport := uncheckedDerivativeTransport",
        ),
        "actual holomorphy disconnected": (
            "differentiableOn_complexXiCoefficientMoment.mono hD",
            "uncheckedActualHolomorphy hD",
        ),
        "main holomorphy disconnected": (
            "differentiableOn_manuscriptXiCoefficientMain.mono hD",
            "uncheckedMainHolomorphy hD",
        ),
        "nonvanishing disconnected": (
            "manuscriptXiCoefficientMain_ne_zero (hD hz)",
            "uncheckedMainNonzero (hD hz)",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 manuscript-Cauchy mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
