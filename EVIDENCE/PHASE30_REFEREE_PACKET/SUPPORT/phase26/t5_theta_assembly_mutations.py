#!/usr/bin/env python3
"""Fail-closed source mutations for the exact T5 theta assembly seam."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ThetaMomentAssembly.lean"
)


class ContractError(RuntimeError):
    """The exact theta-moment assembly contract is absent or ambiguous."""


def validate(text: str) -> None:
    required = {
        "theta-tail reconstruction":
            "theorem fullThetaContourIntegrand_eq_thetaTail",
        "pointwise two-scale bridge":
            "theorem fullThetaContourIntegrand_evenNat_two_mul",
        "integral change of variables": "integral_comp_mul_left_Ioi'",
        "exact moment bridge":
            "theorem fullThetaMoment_evenNat_eq_thetaMoment",
        "factor eight producer":
            "eight_mul_integral_pow_omegaLogAmplitude_succ n",
        "T1 coefficient producer": "centeredXiCoefficient_eq_omegaMoment",
        "binomial conversion": "Nat.cast_choose_two",
        "denominator-free assembly":
            "theorem centeredXiCoefficient_succ_thetaMomentAssembly",
        "divided assembly":
            "theorem centeredXiCoefficient_succ_eq_thetaMomentAssembly",
    }
    for label, needle in required.items():
        if text.count(needle) != 1:
            raise ContractError(label)
    coefficient = "32 * (((2 * (n + 1)).choose 2 : ℕ) : ℂ)"
    if text.count(coefficient) != 2:
        raise ContractError("frozen two-shift coefficient")


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 exact theta-assembly source contract")
    mutations = {
        "theta-tail identity removed": (
            "theorem fullThetaContourIntegrand_eq_thetaTail",
            "theorem theta_tail_identity_unchecked",
        ),
        "Jacobian producer removed": (
            "integral_comp_mul_left_Ioi'",
            "integral_change_of_variables_unchecked",
        ),
        "moment bridge removed": (
            "theorem fullThetaMoment_evenNat_eq_thetaMoment",
            "theorem theta_moment_bridge_unchecked",
        ),
        "factor eight disconnected": (
            "eight_mul_integral_pow_omegaLogAmplitude_succ n",
            "factor_eight_unchecked n",
        ),
        "T1 coefficient disconnected": (
            "centeredXiCoefficient_eq_omegaMoment",
            "xi_coefficient_unchecked",
        ),
        "binomial identity disconnected": (
            "Nat.cast_choose_two",
            "binomial_identity_unchecked",
        ),
        "coefficient 32 changed": (
            "32 * (((2 * (n + 1)).choose 2 : ℕ) : ℂ)",
            "31 * (((2 * (n + 1)).choose 2 : ℕ) : ℂ)",
        ),
        "final assembly removed": (
            "theorem centeredXiCoefficient_succ_eq_thetaMomentAssembly",
            "theorem final_theta_assembly_unchecked",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 exact theta-assembly mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
