#!/usr/bin/env python3
"""Fail-closed source mutations for the exact T5 saddle-main differential layer."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/SaddleMainDifferential.lean"
)


class ContractError(RuntimeError):
    """The exact saddle-main differential contract is absent or ambiguous."""


def validate(text: str) -> None:
    required = {
        "curvature restriction": "theorem saddleCurvatureAlong_eq",
        "curvature derivative": "theorem hasDerivAt_saddleCurvatureAlong",
        "stationary log derivative": "theorem hasDerivAt_saddleLeadingLog",
        "stationary producer": "leadingLogD1_at_saddle hLne hroot",
        "exact Gaussian logarithm": "def saddleMomentLogMain (s",
        "main exponential identity": "theorem saddleMomentMain_eq_exp_logMain",
        "complete derivative formula":
            "saddleLeadingLogD1 s - dK / (2 * K) - dK / (2 * K ^ 2)",
        "log-main derivative": "theorem hasDerivAt_saddleMomentLogMain",
        "main derivative": "theorem hasDerivAt_saddleMomentMain",
        "logarithmic derivative":
            "theorem saddleMomentMain_logarithmicDerivative",
        "concrete Gaussian evaluation": "integral_leadingGaussian hKre",
        "concrete sector openness": "isOpen_leanSaddleSector.mem_nhds hs",
    }
    for label, needle in required.items():
        count = text.count(needle)
        if count != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 saddle-main differential source contract")
    mutations = {
        "curvature identity removed": (
            "theorem saddleCurvatureAlong_eq",
            "theorem curvature_identity_unchecked",
        ),
        "curvature derivative removed": (
            "theorem hasDerivAt_saddleCurvatureAlong",
            "theorem curvature_derivative_unchecked",
        ),
        "stationarity removed": (
            "leadingLogD1_at_saddle hLne hroot",
            "stationarity_unchecked hLne hroot",
        ),
        "Gaussian evaluation disconnected": (
            "integral_leadingGaussian hKre",
            "gaussian_integral_unchecked hKre",
        ),
        "determinant derivative sign changed": (
            "saddleLeadingLogD1 s - dK / (2 * K)",
            "saddleLeadingLogD1 s + dK / (2 * K)",
        ),
        "Jacobian derivative sign changed": (
            "- dK / (2 * K ^ 2)",
            "+ dK / (2 * K ^ 2)",
        ),
        "main derivative removed": (
            "theorem hasDerivAt_saddleMomentMain",
            "theorem main_derivative_unchecked",
        ),
        "sector neighborhood disconnected": (
            "isOpen_leanSaddleSector.mem_nhds hs",
            "sector_neighborhood_unchecked hs",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 saddle-main differential mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
