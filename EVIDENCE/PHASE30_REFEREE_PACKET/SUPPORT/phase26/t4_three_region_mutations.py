#!/usr/bin/env python3
"""Fail-closed source mutations for the T4 three-region assembly."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/HigherThetaSuppression.lean"
)


class ContractError(RuntimeError):
    """The frozen T4 assembly contract is absent or ambiguous."""


def validate(text: str) -> None:
    required = {
        "central leading integral":
            "theorem quantitativeSaddleBranch_central_leading_norm_integral_le_two_amplitude",
        "central inverse square":
            "theorem quantitativeSaddleBranch_central_higherThetaSum_norm_le_curvature_sq_inv_mul_leading",
        "centered integrability":
            "theorem integrableOn_quantitativeSaddleBranch_centeredHigherThetaRay",
        "three-region split":
            "theorem quantitativeSaddleBranch_centeredHigherThetaRay_integral_split",
        "higher ray result":
            "theorem quantitativeSaddleBranch_higherThetaTopRay_relative_le",
        "full ray result":
            "theorem quantitativeSaddleBranch_fullThetaTopRay_relative_error_le",
        "pointwise producer": "higherThetaMode_tsum_norm_le",
        "curvature absorption": "two_exp_modeFactor_le_curvature_sq_inv",
        "amplitude producer":
            "quantitativeSaddleBranch_amplitude_le_gaussianMain_scale",
        "tail producer":
            "quantitativeSaddleBranch_horizontal_tail_relative_inverse_curvature",
        "all-mode identity": "fullThetaTopRay_eq_leading_add_higher",
        "leading T3 producer":
            "quantitativeSaddleBranch_leadingTopRay_relative_error_le",
        "frozen full coefficient":
            "71000001 + 2 * (2 * 20 ^ 15 * (Nat.factorial 15 : ℝ))",
    }
    for label, needle in required.items():
        if text.count(needle) != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T4 three-region source contract")
    mutations = {
        "central theorem removed": (
            "theorem quantitativeSaddleBranch_central_higherThetaSum_norm_le_curvature_sq_inv_mul_leading",
            "theorem central_higher_sum_unchecked",
        ),
        "three-region split removed": (
            "theorem quantitativeSaddleBranch_centeredHigherThetaRay_integral_split",
            "theorem centered_split_unchecked",
        ),
        "pointwise producer disconnected": (
            "higherThetaMode_tsum_norm_le",
            "higher_sum_unchecked",
        ),
        "curvature absorption disconnected": (
            "two_exp_modeFactor_le_curvature_sq_inv",
            "curvature_absorption_unchecked",
        ),
        "tail theorem disconnected": (
            "quantitativeSaddleBranch_horizontal_tail_relative_inverse_curvature",
            "tail_bound_unchecked",
        ),
        "full sum identity disconnected": (
            "fullThetaTopRay_eq_leading_add_higher",
            "full_sum_identity_unchecked",
        ),
        "T3 producer disconnected": (
            "quantitativeSaddleBranch_leadingTopRay_relative_error_le",
            "leading_t3_unchecked",
        ),
        "final constant weakened": (
            "71000001 + 2 * (2 * 20 ^ 15 * (Nat.factorial 15 : ℝ))",
            "71000000 + 2 * (2 * 20 ^ 15 * (Nat.factorial 15 : ℝ))",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T4 three-region mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
