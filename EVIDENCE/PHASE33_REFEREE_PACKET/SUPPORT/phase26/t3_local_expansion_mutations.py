#!/usr/bin/env python3
"""Fail-closed mutations for the exact T3 local Taylor layer."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration"
    / "zeta-23-lean"
    / "Zeta23"
    / "Research"
    / "JensenWedge"
    / "LeadingLocalExpansion.lean"
)


class ContractError(RuntimeError):
    """A load-bearing local-expansion connection is absent or ambiguous."""


def require_count(text: str, needle: str, count: int, label: str) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count} occurrences, found {actual}")


def validate(text: str) -> None:
    checks = {
        "segment Taylor theorem": ("theorem cubicTaylorIntegralOnSegment\n", 1),
        "Mathlib Taylor producer": (
            "map_add_eq_sum_add_integral_iteratedFDeriv",
            1,
        ),
        "weighted fourth derivative": (
            "(1 / 6 : ℝ) • ∫ t in 0..1, ((1 - t) ^ 3 * y ^ 4) •",
            3,
        ),
        "explicit remainder norm": (
            "‖cubicTaylorRemainder f x y‖ ≤ C * |y| ^ 4 / 6 := by",
            1,
        ),
        "principal-log regularity": ("Complex.contDiffAt_log (Or.inl hr)", 1),
        "named derivative tower": (
            "theorem leadingHorizontalLog_iteratedDeriv_tower\n",
            1,
        ),
        "legal local radius": ("{r : ℝ} (hr : |r| ≤ 1 / 10) :", 4),
        "quadratic descent": (
            "(r : ℂ) - leadingCurvature s L * (r : ℂ) ^ 2 / 2 +",
            1,
        ),
        "exact local producer": ("theorem leadingLocalExpansion_exact\n", 1),
        "remainder-bound consumer": (
            "theorem norm_leadingLocalRemainder_le\n",
            1,
        ),
        "concrete saddle ratio": (
            "theorem quantitativeSaddleBranch_ratio_norm_bounds\n",
            1,
        ),
        "concrete fourth derivative": (
            "theorem quantitativeSaddleBranch_leadingLogD4_norm_le\n",
            1,
        ),
        "concrete exact expansion": (
            "theorem quantitativeSaddleBranch_localExpansion_exact\n",
            1,
        ),
        "concrete remainder": (
            "theorem quantitativeSaddleBranch_localRemainder_norm_le\n",
            1,
        ),
        "fourth derivative factor": (
            "‖leadingLogD4 s (quantitativeSaddleBranch s + r)‖ ≤\n"
            "      32 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ := by",
            1,
        ),
        "concrete remainder factor": (
            "‖leadingLocalRemainder s (quantitativeSaddleBranch s) r‖ ≤\n"
            "      6 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ * |r| ^ 4 := by",
            1,
        ),
    }
    for label, (needle, count) in checks.items():
        require_count(text, needle, count, label)


def mutate(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise AssertionError(f"mutation source is not unique: {old!r}")
    return text.replace(old, new, 1)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS local-expansion mutation rejected: {label}")
        return
    raise AssertionError(f"local-expansion mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS exact T3 local-expansion source contract")
    cases = {
        "Taylor producer disconnected": mutate(
            source,
            "map_add_eq_sum_add_integral_iteratedFDeriv",
            "map_add_eq_sum_add_integral_unchecked",
        ),
        "remainder norm weakened": mutate(
            source,
            "‖cubicTaylorRemainder f x y‖ ≤ C * |y| ^ 4 / 6 := by",
            "‖cubicTaylorRemainder f x y‖ ≤ C * |y| ^ 3 / 6 := by",
        ),
        "principal-log guard disconnected": mutate(
            source,
            "Complex.contDiffAt_log (Or.inl hr)",
            "Complex.contDiffAt_log unchecked",
        ),
        "derivative tower disconnected": mutate(
            source,
            "theorem leadingHorizontalLog_iteratedDeriv_tower\n",
            "theorem leadingHorizontalLog_iteratedDeriv_tower_unchecked\n",
        ),
        "local radius enlarged": mutate(
            source,
            "(hroot : sectorialSaddleEquation s L = 0)\n"
            "    {r : ℝ} (hr : |r| ≤ 1 / 10) :",
            "(hroot : sectorialSaddleEquation s L = 0)\n"
            "    {r : ℝ} (hr : |r| ≤ 1) :",
        ),
        "quadratic sign reversed": mutate(
            source,
            "(r : ℂ) - leadingCurvature s L * (r : ℂ) ^ 2 / 2 +",
            "(r : ℂ) + leadingCurvature s L * (r : ℂ) ^ 2 / 2 +",
        ),
        "local expansion disconnected": mutate(
            source,
            "theorem leadingLocalExpansion_exact\n",
            "theorem leadingLocalExpansion_exact_unchecked\n",
        ),
        "remainder consumer disconnected": mutate(
            source,
            "theorem norm_leadingLocalRemainder_le\n",
            "theorem norm_leadingLocalRemainder_le_unchecked\n",
        ),
        "concrete ratio disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_ratio_norm_bounds\n",
            "theorem quantitativeSaddleBranch_ratio_norm_bounds_unchecked\n",
        ),
        "concrete fourth derivative disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_leadingLogD4_norm_le\n",
            "theorem quantitativeSaddleBranch_leadingLogD4_norm_le_unchecked\n",
        ),
        "concrete expansion disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_localExpansion_exact\n",
            "theorem quantitativeSaddleBranch_localExpansion_exact_unchecked\n",
        ),
        "concrete remainder disconnected": mutate(
            source,
            "theorem quantitativeSaddleBranch_localRemainder_norm_le\n",
            "theorem quantitativeSaddleBranch_localRemainder_norm_le_unchecked\n",
        ),
        "fourth derivative factor weakened": mutate(
            source,
            "‖leadingLogD4 s (quantitativeSaddleBranch s + r)‖ ≤\n"
            "      32 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ := by",
            "‖leadingLogD4 s (quantitativeSaddleBranch s + r)‖ ≤\n"
            "      64 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ := by",
        ),
        "concrete remainder order weakened": mutate(
            source,
            "‖leadingLocalRemainder s (quantitativeSaddleBranch s) r‖ ≤\n"
            "      6 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ * |r| ^ 4 := by",
            "‖leadingLocalRemainder s (quantitativeSaddleBranch s) r‖ ≤\n"
            "      6 * ‖leadingCurvature s (quantitativeSaddleBranch s)‖ * |r| ^ 3 := by",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print(f"PASS local-expansion semantic mutations: {len(cases)} rejected")


if __name__ == "__main__":
    main()
