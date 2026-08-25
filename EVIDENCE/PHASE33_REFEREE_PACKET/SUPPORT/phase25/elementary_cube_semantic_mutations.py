#!/usr/bin/env python3
"""Fail-closed source mutations for the elementary cube-calculus chain."""

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
    / "ElementaryCubeCalculus.lean"
)


class ContractError(RuntimeError):
    """A load-bearing elementary-calculus source contract failed."""


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise ContractError(f"{label}: expected exactly one occurrence, found {count}")


def validate(text: str) -> None:
    required = {
        "tail-oriented Fubini": "theorem integral_unitCube_succ_tail",
        "finite-difference recursion": "theorem elementaryCubeIntegral_shift_sub",
        "forward convention": "iteratedForwardDifference n f (s + 1) - iteratedForwardDifference n f s",
        "q1 sign": "iteratedForwardDifference 0 elementaryLogFactor s =\n      -elementaryCubeIntegral 1 1 s 1",
        "q2 sign": "elementaryCubeIntegral 2 2 s 1",
        "q3 coefficient": "-2 * elementaryCubeIntegral 3 3 s 1",
        "q4 coefficient": "iteratedForwardDifference 3 elementaryLogFactor s =\n      6 * elementaryCubeIntegral 4 4 s 1",
        "exact scale": "x ^ p * elementaryCubeIntegral q p s x",
        "first derivative": "theorem hasDerivAt_elementaryPhi\n",
        "second derivative": "theorem hasDerivAt_elementaryPhi_firstDerivative",
        "B-C segment": "theorem elementaryPhi_paired_dividedDifference",
        "w derivative": "theorem hasDerivAt_elementaryPhi_paired_w",
        "t derivative": "theorem hasDerivAt_elementaryPhi_paired_t",
        "delta derivative": "theorem hasDerivAt_elementaryPhi_boundary_delta",
        "first-order error": "theorem elementaryCubeIntegral_firstOrder_error",
        "remote q1": "theorem elementaryPhi_remote_q1_error",
        "remote scale": "elementaryPhi 1 alpha (x * e)",
        "half shift": "elementaryPhi q (1 + x / 2) x",
        "x/e bound": "elementaryPhi q 1 x) / e| ≤\n      (q : ℝ) * (x / e)",
    }
    for label, needle in required.items():
        require_once(text, needle, label)


def expect_rejected(label: str, mutated: str) -> None:
    try:
        validate(mutated)
    except ContractError:
        print(f"PASS elementary mutation rejected: {label}")
        return
    raise AssertionError(f"elementary mutation survived: {label}")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    validate(text)
    print("PASS elementary cube source contract")
    mutations = {
        "reverse forward difference": (
            "iteratedForwardDifference n f (s + 1) - iteratedForwardDifference n f s",
            "iteratedForwardDifference n f s - iteratedForwardDifference n f (s + 1)",
        ),
        "q3 loses factorial": (
            "-2 * elementaryCubeIntegral 3 3 s 1",
            "-elementaryCubeIntegral 3 3 s 1",
        ),
        "q4 sign flip": (
            "iteratedForwardDifference 3 elementaryLogFactor s =\n      6 * elementaryCubeIntegral 4 4 s 1",
            "iteratedForwardDifference 3 elementaryLogFactor s =\n      -6 * elementaryCubeIntegral 4 4 s 1",
        ),
        "scale exponent shift": (
            "x ^ p * elementaryCubeIntegral q p s x",
            "x ^ (p + 1) * elementaryCubeIntegral q p s x",
        ),
        "remote product dropped": (
            "elementaryPhi 1 alpha (x * e)",
            "elementaryPhi 1 alpha x",
        ),
        "half shift doubled": (
            "elementaryPhi q (1 + x / 2) x",
            "elementaryPhi q (1 + x) x",
        ),
        "x/e term inverted": (
            "elementaryPhi q 1 x) / e| ≤\n      (q : ℝ) * (x / e)",
            "elementaryPhi q 1 x) / e| ≤\n      (q : ℝ) * (e / x)",
        ),
    }
    for label, (old, new) in mutations.items():
        require_once(text, old, f"mutation target {label}")
        expect_rejected(label, text.replace(old, new, 1))
    print("PASS all elementary cube semantic mutations")


if __name__ == "__main__":
    main()
