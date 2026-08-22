#!/usr/bin/env python3
"""Fail-closed mutations for fixed T3 Gaussian moment scaling."""

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
    / "LeadingMomentScale.lean"
)


class ContractError(RuntimeError):
    """A fixed-moment scaling connection is absent."""


def require_count(text: str, needle: str, count: int, label: str) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count} occurrences, found {actual}")


def validate(text: str) -> None:
    checks = {
        "half-integer Gamma recurrence": ("Real.Gamma_nat_add_half", 4),
        "pi upper bound": ("Real.pi_le_four", 4),
        "exponential upper bound": ("Real.exp_one_lt_three.le", 1),
        "Gamma-form producer": (
            "integral_norm_pow_mul_leadingGaussian_le hKre n",
            1,
        ),
        "curvature comparison": (
            "quantitativeSaddleBranch_curvature_strong_bounds hs",
            4,
        ),
        "fourth constant": ("4096 * ‖K‖ ^ (-(5 / 2 : ℝ))", 3),
        "sixth constant": ("65536 * ‖K‖ ^ (-(7 / 2 : ℝ))", 3),
        "eighth constant": ("2097152 * ‖K‖ ^ (-(9 / 2 : ℝ))", 3),
        "tenth constant": ("67108864 * ‖K‖ ^ (-(11 / 2 : ℝ))", 3),
        "scaled producer": (
            "integral_norm_pow_mul_leadingGaussian_le_scaled",
            5,
        ),
    }
    for label, (needle, count) in checks.items():
        require_count(text, needle, count, label)


def mutate(text: str, old: str, new: str, count: int = 1) -> str:
    if text.count(old) != count:
        raise AssertionError(f"mutation source count is not {count}: {old!r}")
    return text.replace(old, new, 1)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS moment-scale mutation rejected: {label}")
        return
    raise AssertionError(f"moment-scale mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 fixed Gaussian moment-scale source contract")
    cases = {
        "Gamma recurrence disconnected": mutate(
            source,
            "Real.Gamma_nat_add_half",
            "Real.Gamma_half_step_unchecked",
            count=4,
        ),
        "pi bound disconnected": mutate(
            source,
            "Real.pi_le_four",
            "Real.pi_upper_unchecked",
            count=4,
        ),
        "exponential bound disconnected": mutate(
            source,
            "Real.exp_one_lt_three.le",
            "Real.exp_one_upper_unchecked",
        ),
        "Gamma moment producer disconnected": mutate(
            source,
            "integral_norm_pow_mul_leadingGaussian_le hKre n",
            "integral_norm_pow_mul_leadingGaussian_le_unchecked hKre n",
        ),
        "curvature comparison disconnected": mutate(
            source,
            "quantitativeSaddleBranch_curvature_strong_bounds hs",
            "quantitativeSaddleBranch_curvature_bounds_unchecked hs",
            count=4,
        ),
        "fourth constant changed": mutate(
            source,
            "4096 * ‖K‖ ^ (-(5 / 2 : ℝ))",
            "2048 * ‖K‖ ^ (-(5 / 2 : ℝ))",
            count=3,
        ),
        "sixth constant changed": mutate(
            source,
            "65536 * ‖K‖ ^ (-(7 / 2 : ℝ))",
            "32768 * ‖K‖ ^ (-(7 / 2 : ℝ))",
            count=3,
        ),
        "eighth constant changed": mutate(
            source,
            "2097152 * ‖K‖ ^ (-(9 / 2 : ℝ))",
            "1048576 * ‖K‖ ^ (-(9 / 2 : ℝ))",
            count=3,
        ),
        "tenth constant changed": mutate(
            source,
            "67108864 * ‖K‖ ^ (-(11 / 2 : ℝ))",
            "33554432 * ‖K‖ ^ (-(11 / 2 : ℝ))",
            count=3,
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print(f"PASS moment-scale semantic mutations: {len(cases)} rejected")


if __name__ == "__main__":
    main()
