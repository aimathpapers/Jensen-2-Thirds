#!/usr/bin/env python3
"""Fail-closed source mutations for the right-half-plane digamma estimate."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/GammaFacts/"
    "StirlingRight.lean"
)


class ContractError(RuntimeError):
    """The right-half-plane Stirling contract is absent or ambiguous."""


def validate(text: str) -> None:
    required = {
        "real-part denominator": "theorem re_add_le_norm_add",
        "interval remainder": "theorem norm_eps_le_re",
        "rho remainder": "theorem norm_rho_le_re",
        "real telescope": "theorem inv_norm_sq_le_telescope_re",
        "finite sum": "theorem sum_inv_norm_sq_le_re",
        "infinite sum": "theorem tsum_inv_norm_sq_le_re",
        "rho summability": "theorem summable_rho_re",
        "epsilon summability": "theorem summable_eps_re",
        "exact identity": "theorem digamma_eq_re",
        "partial fraction producer":
            "Zeta23.DigammaSeries.hasSum_digamma_series hmem",
        "Euler--Maclaurin producer": "rw [partial_sum_eq hw N]",
        "log increment producer": "have hlog := log_one_add_sub_log hw0",
        "remote hypothesis": "(hw : 1 ≤ w.re)",
        "noninteger disclosure": "(hmem : w ∈ Complex.integerComplement)",
        "series-level theorem": "theorem digamma_stirling_re\n",
        "right-half-plane holomorphicity": "theorem differentiableAt_digamma_re",
        "all-point theorem": "theorem digamma_stirling_re_all ",
        "continuity transfer": "le_of_tendsto_of_tendsto hleft hright",
        "final rate": "2 / w.re ^ 2",
    }
    expected_counts = {
        "interval remainder": 2,
        "rho remainder": 2,
        "noninteger disclosure": 2,
        "remote hypothesis": 2,
        "final rate": 4,
    }
    for label, needle in required.items():
        if text.count(needle) != expected_counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 right-half-plane digamma Stirling source contract")
    mutations = {
        "real-part denominator removed": (
            "theorem re_add_le_norm_add",
            "theorem real_part_denominator_unchecked",
        ),
        "telescoping estimate removed": (
            "theorem inv_norm_sq_le_telescope_re",
            "theorem real_telescope_unchecked",
        ),
        "partial-fraction producer disconnected": (
            "Zeta23.DigammaSeries.hasSum_digamma_series hmem",
            "unchecked_digamma_series hmem",
        ),
        "Euler--Maclaurin identity disconnected": (
            "rw [partial_sum_eq hw N]",
            "rw [unchecked_partial_sum hw N]",
        ),
        "log increment disconnected": (
            "have hlog := log_one_add_sub_log hw0",
            "have hlog := unchecked_log_increment hw0",
        ),
        "remote threshold weakened": (
            "(hw : 1 ≤ w.re)",
            "(hw : 0 ≤ w.re)",
        ),
        "integer-complement guard removed": (
            "(hmem : w ∈ Complex.integerComplement)",
            "(hmem : True)",
        ),
        "final rate weakened": (
            "2 / w.re ^ 2",
            "3 / w.re ^ 2",
        ),
        "series-level theorem removed": (
            "theorem digamma_stirling_re\n",
            "theorem digamma_stirling_unchecked",
        ),
        "holomorphicity producer removed": (
            "theorem differentiableAt_digamma_re",
            "theorem differentiableAt_digamma_unchecked",
        ),
        "all-point extension removed": (
            "theorem digamma_stirling_re_all ",
            "theorem digamma_stirling_re_all_unchecked",
        ),
        "continuity transfer removed": (
            "le_of_tendsto_of_tendsto hleft hright",
            "unchecked_limit_transfer hleft hright",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 right-half-plane Stirling mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
