#!/usr/bin/env python3
"""Fail-closed source mutations for the Phase-I analytic Lean adapters."""

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
    / "AnalyticAdapters.lean"
)


class ContractError(RuntimeError):
    """A load-bearing analytic adapter is absent or ambiguous."""


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise ContractError(f"{label}: expected exactly one occurrence, found {count}")


def require_count(text: str, needle: str, expected: int, label: str) -> None:
    count = text.count(needle)
    if count != expected:
        raise ContractError(f"{label}: expected {expected} occurrences, found {count}")


def validate(text: str) -> None:
    require_once(text, "def centeredXi (w : ℂ) : ℂ := riemannXi (1 / 2 + w)", "centered xi")
    require_once(text, "theorem centeredXi_even", "xi evenness")
    require_count(text, "iteratedDeriv (2 * n) centeredXi 0", 3, "coefficient derivative order")
    require_once(text, "theorem centeredXiCoefficient_eq_factorEightMoment", "factor-eight adapter")
    require_once(text, "8 * halfLineMoment kernel n", "factor eight")
    require_once(text, "theorem complexClosedBall_existsUnique_fixedPoint", "disc contraction")
    require_once(text, "theorem relativeError_iteratedDeriv_le", "Cauchy transport")
    require_count(text, "n.factorial * epsilon / radius ^ n", 2, "Cauchy normalization")
    require_once(text, "∀ n ≤ 6,", "order-six cutoff")
    require_once(text, "structure SectorialSaddleCertificate", "analytic boundary")
    require_once(text, "curvature_ne_zero", "curvature seam")
    if "concrete theta-kernel contour estimates have been\n+formalized" in text:
        raise ContractError("source falsely claims concrete theta-kernel formalization")


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS analytic-adapter mutation rejected: {label}")
        return
    raise AssertionError(f"analytic-adapter mutation survived: {label}")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    validate(text)
    print("PASS analytic-adapter source contract")

    mutations = {
        "center moved from one half": text.replace("riemannXi (1 / 2 + w)", "riemannXi (1 + w)", 1),
        "odd derivative used": text.replace("iteratedDeriv (2 * n) centeredXi 0", "iteratedDeriv (2 * n + 1) centeredXi 0", 1),
        "factor eight dropped": text.replace("8 * halfLineMoment kernel n", "4 * halfLineMoment kernel n", 1),
        "factorial omitted": text.replace("n.factorial * epsilon / radius ^ n", "epsilon / radius ^ n", 1),
        "order five substituted": text.replace("∀ n ≤ 6,", "∀ n ≤ 5,", 1),
        "curvature seam deleted": text.replace("curvature_ne_zero", "curvature_unchecked", 1),
    }
    for label, mutation in mutations.items():
        expect_rejected(label, mutation)
    print("PASS all analytic-adapter semantic mutations")


if __name__ == "__main__":
    main()
