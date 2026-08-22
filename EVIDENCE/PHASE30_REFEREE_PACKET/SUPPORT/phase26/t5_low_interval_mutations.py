#!/usr/bin/env python3
"""Fail-closed source mutations for the T5 low-interval seam."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/FullThetaMoment.lean"
)


class ContractError(RuntimeError):
    """The complete-moment contract is absent or ambiguous."""


def validate(text: str) -> None:
    required = {
        "low pointwise bound":
            "theorem fullThetaContourIntegrand_low_norm_le_six",
        "low integrability":
            "theorem integrableOn_fullThetaContourIntegrand_low",
        "exact interval split": "theorem fullThetaMoment_eq_low_add_bottom",
        "full moment theorem":
            "theorem quantitativeSaddleBranch_fullThetaMoment_relative_error_le",
        "infinite-mode producer": "higherThetaMode_tsum_norm_le",
        "connector normalization":
            "quantitativeSaddleBranch_connector_relative_inverse_curvature_of_norm_le",
        "T4 original-ray producer":
            "quantitativeSaddleBranch_fullThetaBottomRay_relative_error_le hs",
        "frozen coefficient":
            "71000004 + 2 * (2 * 20 ^ 15 * (Nat.factorial 15 : ℝ))",
    }
    for label, needle in required.items():
        if text.count(needle) != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 low-interval source contract")
    mutations = {
        "low bound removed": (
            "theorem fullThetaContourIntegrand_low_norm_le_six",
            "theorem low_interval_unchecked",
        ),
        "higher-mode sum disconnected": (
            "higherThetaMode_tsum_norm_le",
            "higher_mode_sum_unchecked",
        ),
        "low integrability removed": (
            "theorem integrableOn_fullThetaContourIntegrand_low",
            "theorem low_integrability_unchecked",
        ),
        "interval split removed": (
            "theorem fullThetaMoment_eq_low_add_bottom",
            "theorem moment_split_unchecked",
        ),
        "low normalization disconnected": (
            "quantitativeSaddleBranch_connector_relative_inverse_curvature_of_norm_le",
            "low_scale_unchecked",
        ),
        "T4 theorem disconnected": (
            "quantitativeSaddleBranch_fullThetaBottomRay_relative_error_le hs",
            "bottom_ray_unchecked",
        ),
        "low contribution dropped": (
            "71000004 + 2 * (2 * 20 ^ 15 * (Nat.factorial 15 : ℝ))",
            "71000003 + 2 * (2 * 20 ^ 15 * (Nat.factorial 15 : ℝ))",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 low-interval mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
