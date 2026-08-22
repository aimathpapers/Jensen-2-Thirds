#!/usr/bin/env python3
"""Fail-closed mutations for T4 curvature-scale suppression."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/HigherThetaScale.lean"


class ContractError(RuntimeError):
    pass


def validate(text: str) -> None:
    required = {
        "saddle scale": "theorem quantitativeSaddleBranch_modeParameter_at_saddle_ge_curvature_div_four",
        "boundary scale": "theorem quantitativeSaddleBranch_modeParameter_beyond_leftBoundary_ge_curvature_div_five",
        "exponential absorption": "theorem two_exp_modeFactor_le_curvature_sq_inv",
        "quarter curvature": "‖leadingCurvature s (quantitativeSaddleBranch s)‖ / 4 ≤",
        "fifth curvature": "‖leadingCurvature s (quantitativeSaddleBranch s)‖ / 5 ≤",
        "inverse square": "2 * Real.exp (-3 * q) ≤ 1 / K ^ 2",
        "branch box": "quantitativeSaddleBranch_scaled_bounds hinput",
        "curvature floor": "quantitativeSaddleBranch_curvature_norm_ge_fourThousand hs",
    }
    for label, needle in required.items():
        if text.count(needle) != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T4 curvature-scale source contract")
    mutations = {
        "saddle scale removed": ("theorem quantitativeSaddleBranch_modeParameter_at_saddle_ge_curvature_div_four", "theorem saddle_scale_unchecked"),
        "boundary scale removed": ("theorem quantitativeSaddleBranch_modeParameter_beyond_leftBoundary_ge_curvature_div_five", "theorem boundary_scale_unchecked"),
        "absorption removed": ("theorem two_exp_modeFactor_le_curvature_sq_inv", "theorem absorption_unchecked"),
        "curvature floor disconnected": ("quantitativeSaddleBranch_curvature_norm_ge_fourThousand hs", "curvature_floor_unchecked hs"),
        "sign reversed": ("2 * Real.exp (-3 * q) ≤ 1 / K ^ 2", "2 * Real.exp (3 * q) ≤ 1 / K ^ 2"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T4 curvature-scale mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
