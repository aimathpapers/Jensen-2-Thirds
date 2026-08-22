#!/usr/bin/env python3
"""Fail-closed mutations for the paired fifth-polygamma series estimate."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/PolygammaPairing.lean"
)


class ContractError(RuntimeError):
    """The paired-polygamma proof contract changed."""


def validate(text: str) -> None:
    required = {
        "segment containment": "theorem lineSegment_re_lower",
        "segment interpolation": "z + (t : ℂ) * (w - z)",
        "seventh-tail summability": "theorem shiftedSeventhPowerTail_summable",
        "integral-test tail": "theorem shiftedSeventhPowerTail_le",
        "tail statement": (
            "theorem shiftedSeventhPowerTail_le {n : ℕ} (hn : 2 ≤ n) :\n"
            "    (∑' k : ℕ, 1 / (((n + k : ℕ) : ℝ) ^ 7)) ≤\n"
            "      1 / (6 * (((n - 1 : ℕ) : ℝ) ^ 6)) := by"
        ),
        "power algebra": "theorem norm_pow_six_sub_pow_six_le",
        "reciprocal subtraction": "theorem norm_inv_sub_inv_le",
        "inverse-power gain": "theorem norm_inv_pow_six_sub_inv_pow_six_le",
        "inverse-power conclusion": (
            "‖u⁻¹ ^ 6 - v⁻¹ ^ 6‖ ≤ 6 * ‖u - v‖ / a ^ 7 := by"
        ),
        "series convergence": "theorem summable_invPowSix_rightOfNat",
        "series definition": "def polygammaFiveSeries (z : ℂ)",
        "series normalization": "120 * ∑' k : ℕ, (z + (k : ℂ))⁻¹ ^ 6",
        "paired theorem": "theorem polygammaFiveSeries_pair_norm_le",
        "paired statement": (
            "‖polygammaFiveSeries z - polygammaFiveSeries w‖ ≤\n"
            "      120 * ‖z - w‖ / (((n - 1 : ℕ) : ℝ) ^ 6) := by"
        ),
        "integral test source": "hanti.tsum_comp_add_le_integral",
        "termwise producer": "norm_inv_pow_six_sub_inv_pow_six_le hapos hzlower hwlower",
        "tail producer": "shiftedSeventhPowerTail_le hn",
    }
    for label, needle in required.items():
        if needle not in text:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS paired-polygamma source contract")
    mutations = {
        "segment theorem removed": (
            "theorem lineSegment_re_lower",
            "theorem uncheckedLineSegment",
        ),
        "segment direction reversed": (
            "z + (t : ℂ) * (w - z)",
            "z - (t : ℂ) * (w - z)",
        ),
        "tail statement weakened": (
            "theorem shiftedSeventhPowerTail_le {n : ℕ} (hn : 2 ≤ n) :\n"
            "    (∑' k : ℕ, 1 / (((n + k : ℕ) : ℝ) ^ 7)) ≤\n"
            "      1 / (6 * (((n - 1 : ℕ) : ℝ) ^ 6)) := by",
            "theorem shiftedSeventhPowerTail_le {n : ℕ} (hn : 2 ≤ n) :\n"
            "    (∑' k : ℕ, 1 / (((n + k : ℕ) : ℝ) ^ 6)) ≤\n"
            "      1 / (6 * (((n - 1 : ℕ) : ℝ) ^ 5)) := by",
        ),
        "integral test disconnected": (
            "hanti.tsum_comp_add_le_integral",
            "uncheckedIntegralTest",
        ),
        "power algebra removed": (
            "theorem norm_pow_six_sub_pow_six_le",
            "theorem uncheckedPowerDifference",
        ),
        "reciprocal lemma removed": (
            "theorem norm_inv_sub_inv_le",
            "theorem uncheckedInverseDifference",
        ),
        "inverse exponent weakened": (
            "‖u⁻¹ ^ 6 - v⁻¹ ^ 6‖ ≤ 6 * ‖u - v‖ / a ^ 7 := by",
            "‖u⁻¹ ^ 6 - v⁻¹ ^ 6‖ ≤ 6 * ‖u - v‖ / a ^ 6 := by",
        ),
        "convergence theorem removed": (
            "theorem summable_invPowSix_rightOfNat",
            "theorem uncheckedSeriesConvergence",
        ),
        "series normalization changed": (
            "120 * ∑' k : ℕ, (z + (k : ℂ))⁻¹ ^ 6",
            "720 * ∑' k : ℕ, (z + (k : ℂ))⁻¹ ^ 6",
        ),
        "paired theorem removed": (
            "theorem polygammaFiveSeries_pair_norm_le",
            "theorem uncheckedPolygammaPair",
        ),
        "termwise bound disconnected": (
            "norm_inv_pow_six_sub_inv_pow_six_le hapos hzlower hwlower",
            "uncheckedInversePowerBound hapos hzlower hwlower",
        ),
        "tail bound disconnected": (
            "shiftedSeventhPowerTail_le hn",
            "uncheckedTailBound hn",
        ),
        "paired constant changed": (
            "‖polygammaFiveSeries z - polygammaFiveSeries w‖ ≤\n"
            "      120 * ‖z - w‖ / (((n - 1 : ℕ) : ℝ) ^ 6) := by",
            "‖polygammaFiveSeries z - polygammaFiveSeries w‖ ≤\n"
            "      121 * ‖z - w‖ / (((n - 1 : ℕ) : ℝ) ^ 6) := by",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS paired-polygamma mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
