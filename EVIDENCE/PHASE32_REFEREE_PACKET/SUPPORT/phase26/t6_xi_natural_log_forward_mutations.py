#!/usr/bin/env python3
"""Fail closed on natural-log Cauchy and forward-difference mutations."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/XiNaturalLogErrorForwardDifferences.lean"

REQUIRED = {
    "natural epsilon": ("def naturalXiCauchyEpsilon", 1),
    "moment-only coefficient":
        ("(100 * fullThetaMomentErrorCoefficient) * Real.log (3 * x) / x", 1),
    "disc error bound":
        ("theorem complexXiNaturalAuxiliaryRelativeError_cauchy_norm_le", 1),
    "shifted norm geometry": ("manuscriptCauchy_shifted_norm_bounds hx hz", 1),
    "half-disc derivative transport":
        ("theorem complexXiNaturalAuxiliaryLogError_derivatives_through_six_on_half_disc", 1),
    "nested disc": ("manuscriptInterior_closedBall_subset_manuscriptDisc hz", 1),
    "Cauchy producer":
        ("Complex.norm_iteratedDeriv_le_of_forall_mem_sphere_norm_le", 1),
    "three-halves log source":
        ("complexXiNaturalAuxiliaryLogError_norm_le (hDsector hwD)", 1),
    "analytic tower":
        ("theorem complexXiNaturalAuxiliaryLogError_analyticOnNhd", 1),
    "tower derivative":
        ("theorem hasDerivAt_iteratedDeriv_complexXiNaturalAuxiliaryLogError", 1),
    "forward bound":
        ("theorem complexXiNaturalAuxiliaryLogError_forwardDiff_bound", 1),
    "five-node domain": ("nat_five_interval_mem_manuscriptInteriorDisc hn", 2),
    "localized FTC":
        ("norm_complexForwardDiff_sub_constant_le_on_real_interval", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS xi natural log forward-difference source contract")
    mutations = {
        "epsilon coefficient changed":
            ("(100 * fullThetaMomentErrorCoefficient) * Real.log (3 * x) / x",
             "fullThetaMomentErrorCoefficient * Real.log (3 * x) / x"),
        "shifted geometry disconnected":
            ("manuscriptCauchy_shifted_norm_bounds hx hz",
             "uncheckedShiftedNormBounds hx hz"),
        "half-disc transport disconnected":
            ("theorem complexXiNaturalAuxiliaryLogError_derivatives_through_six_on_half_disc",
             "theorem uncheckedNaturalLogDerivativeTransport"),
        "nested disc disconnected":
            ("manuscriptInterior_closedBall_subset_manuscriptDisc hz",
             "uncheckedNestedDisc hz"),
        "Cauchy producer disconnected":
            ("Complex.norm_iteratedDeriv_le_of_forall_mem_sphere_norm_le",
             "uncheckedCauchyDerivativeBound"),
        "log source disconnected":
            ("complexXiNaturalAuxiliaryLogError_norm_le (hDsector hwD)",
             "uncheckedNaturalLogNorm (hDsector hwD)"),
        "analytic tower disconnected":
            ("theorem complexXiNaturalAuxiliaryLogError_analyticOnNhd",
             "theorem uncheckedNaturalLogAnalytic"),
        "forward bound disconnected":
            ("theorem complexXiNaturalAuxiliaryLogError_forwardDiff_bound",
             "theorem uncheckedNaturalLogForwardBound"),
        "five-node domain disconnected":
            ("nat_five_interval_mem_manuscriptInteriorDisc hn",
             "uncheckedFiveNodeDomain hn"),
        "localized FTC disconnected":
            ("norm_complexForwardDiff_sub_constant_le_on_real_interval",
             "uncheckedLocalForwardFTC"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS xi natural log forward mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
