#!/usr/bin/env python3
"""Fail-closed source mutations for the completed T4 all-mode contour."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/HigherThetaContour.lean"
)


class ContractError(RuntimeError):
    """The completed contour contract is absent or ambiguous."""


def validate(text: str) -> None:
    required = {
        "finite mode rectangle":
            "theorem higherThetaMode_finite_rectangle_identity",
        "infinite mode rectangle":
            "theorem higherThetaMode_infinite_rectangle_identity",
        "connector dominated convergence":
            "theorem hasSum_intervalIntegral_higherThetaMode_connector",
        "infinite higher rectangle":
            "theorem higherTheta_infinite_rectangle_identity",
        "full rectangle": "theorem fullTheta_infinite_rectangle_identity",
        "generic connector normalization":
            "theorem quantitativeSaddleBranch_connector_relative_inverse_curvature_of_norm_le",
        "final original-ray theorem":
            "theorem quantitativeSaddleBranch_fullThetaBottomRay_relative_error_le",
        "Cauchy producer":
            "Complex.integral_boundary_rect_eq_zero_of_differentiableOn",
        "sum-integral producer":
            "intervalIntegral.hasSum_integral_of_dominated_convergence",
        "leading rectangle producer": "leading_infinite_rectangle_identity s hb",
        "shifted-ray producer":
            "quantitativeSaddleBranch_fullThetaTopRay_relative_error_le hs",
        "frozen final coefficient":
            "71000003 + 2 * (2 * 20 ^ 15 * (Nat.factorial 15 : ℝ))",
    }
    for label, needle in required.items():
        if text.count(needle) != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T4 full-contour source contract")
    mutations = {
        "finite Cauchy theorem removed": (
            "theorem higherThetaMode_finite_rectangle_identity",
            "theorem higher_mode_rectangle_unchecked",
        ),
        "Cauchy producer disconnected": (
            "Complex.integral_boundary_rect_eq_zero_of_differentiableOn",
            "rectangle_integral_unchecked",
        ),
        "far-side limit disconnected": (
            "theorem higherThetaMode_infinite_rectangle_identity",
            "theorem higher_mode_infinite_unchecked",
        ),
        "connector Fubini disconnected": (
            "intervalIntegral.hasSum_integral_of_dominated_convergence",
            "connector_sum_unchecked",
        ),
        "higher sum rectangle removed": (
            "theorem higherTheta_infinite_rectangle_identity",
            "theorem higher_rectangle_unchecked",
        ),
        "leading rectangle disconnected": (
            "leading_infinite_rectangle_identity s hb",
            "leading_rectangle_unchecked",
        ),
        "connector normalization removed": (
            "theorem quantitativeSaddleBranch_connector_relative_inverse_curvature_of_norm_le",
            "theorem connector_scale_unchecked",
        ),
        "shifted-ray theorem disconnected": (
            "quantitativeSaddleBranch_fullThetaTopRay_relative_error_le hs",
            "full_top_ray_unchecked",
        ),
        "final connector constant dropped": (
            "71000003 + 2 * (2 * 20 ^ 15 * (Nat.factorial 15 : ℝ))",
            "71000001 + 2 * (2 * 20 ^ 15 * (Nat.factorial 15 : ℝ))",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T4 full-contour mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
