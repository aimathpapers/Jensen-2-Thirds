#!/usr/bin/env python3
"""Fail closed on semantic mutations of elementary boundary estimates."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ElementaryBoundaryEstimates.lean"
)


class ContractError(RuntimeError):
    """The boundary-estimate source contract changed."""


REQUIRED = {
    "reciprocal power": ("theorem reciprocalPower_add_error", 1),
    "power increment": ("s₀⁻¹ ^ (p + 1)", 1),
    "first derivative": ("theorem elementaryPhiD1_base_error", 1),
    "first sign": ("(-(q : ℝ) * s⁻¹ ^ (q + 1))", 5),
    "second derivative": ("theorem elementaryPhiD2_base_error", 1),
    "second order": ("s₀⁻¹ ^ (q + 3)", 5),
    "averaging": ("theorem abs_integral_Icc_zero_one_sub_const_le", 1),
    "paired producer": ("theorem elementaryPhi_paired_value_error", 1),
    "boundary producer": ("theorem elementaryPhi_boundary_value_error", 1),
    "half-shift source": ("elementaryPhi_halfShift_div_bound (q := q) hx he", 1),
    "x over e": ("(q : ℝ) * (x / e) +", 2),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary boundary-estimate source contract")
    mutations = {
        "power increment weakened": ("s₀⁻¹ ^ (p + 1)", "s₀⁻¹ ^ p"),
        "first derivative sign reversed": (
            "(-(q : ℝ) * s⁻¹ ^ (q + 1))", "((q : ℝ) * s⁻¹ ^ (q + 1))"),
        "second derivative order weakened": ("s₀⁻¹ ^ (q + 3)", "s₀⁻¹ ^ (q + 2)"),
        "averaging disconnected": (
            "theorem abs_integral_Icc_zero_one_sub_const_le",
            "theorem uncheckedIntegralAverage"),
        "paired estimate disconnected": (
            "theorem elementaryPhi_paired_value_error",
            "theorem uncheckedPairedValue"),
        "half-shift bound disconnected": (
            "elementaryPhi_halfShift_div_bound (q := q) hx he",
            "uncheckedHalfShiftBound (q := q) hx he"),
        "x over e removed": ("(q : ℝ) * (x / e) +", "(q : ℝ) * x +"),
    }
    for label, (old, new) in mutations.items():
        if source.count(old) < 1:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS elementary boundary mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
