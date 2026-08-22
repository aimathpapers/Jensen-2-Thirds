#!/usr/bin/env python3
"""Fail-closed semantic source mutations for Phase-F adapters."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT / "Kimi_Agent_Riemann Lean Exploration" / "zeta-23-lean" / "Zeta23"
    / "Research" / "JensenWedge" / "FiniteFreeAdapters.lean"
)


class ContractError(RuntimeError):
    pass


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise ContractError(f"missing {label}")


def validate(text: str) -> None:
    checks = {
        "ascending sign": "((-1 : ℝ) ^ k * p.coeff k * q.coeff k)",
        "descending sign": "((-1 : ℝ) ^ (d - k) * p.coeff k * q.coeff k)",
        "binomial normalization": "/ (Nat.choose d k : ℝ)",
        "reflection theorem": "theorem reflect_finiteFreeAscending",
        "reciprocal endpoint": "theorem reciprocal_mem_interval",
        "Gershgorin eight": "V - 8 * r ≤ μ ∧ μ ≤ V + 8 * r",
        "transported diagonal": "theorem transportedJacobiDiagonal_sub",
        "root eigenvalue seam": "root_is_eigenvalue : ∀ y, q.eval y = 0",
        "reciprocal MSS input": "reciprocal_largest_root : 1 / z ≤",
        "product theorem": "theorem MSSProductRootInput.product_interval",
        "localization theorem": "theorem productDeviation_le_localizationConstant",
        "correct localization constant": "_ = localizationConstant * r",
        "strict mesh": "ratio_gt_one : ∀ i j, i < j → 1 < roots i / roots j",
        "MMP seam": "structure MMPLogMeshInput",
        "positive distinct output": "theorem MMPLogMeshInput.hasDistinctPositiveRoots",
    }
    for label, needle in checks.items():
        require(text, needle, label)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS finite-free mutation rejected: {label}")
        return
    raise AssertionError(f"finite-free mutation survived: {label}")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    validate(text)
    print("PASS finite-free/Jacobi source contract")
    mutations = {
        "ascending sign": ("((-1 : ℝ) ^ k", "((1 : ℝ) ^ k"),
        "descending exponent": ("^ (d - k) * p.coeff", "^ k * p.coeff"),
        "binomial removed": ("/ (Nat.choose d k : ℝ)", "/ 1"),
        "reflection disconnected": (
            "theorem reflect_finiteFreeAscending",
            "theorem assumed_reflect_finiteFreeAscending",
        ),
        "Gershgorin constant": ("V - 8 * r", "V - 7 * r"),
        "root-eigenvalue source hidden": (
            "root_is_eigenvalue : ∀ y, q.eval y = 0",
            "root_is_eigenvalue : True → ∀ y, q.eval y = 0",
        ),
        "reciprocal MSS half removed": (
            "reciprocal_largest_root : 1 / z ≤",
            "reciprocal_largest_root : True → 1 / z ≤",
        ),
        "localization constant disconnected": (
            "_ = localizationConstant * r",
            "_ = (8 + 12 * Real.sqrt 6) * r",
        ),
        "mesh not strict": ("1 < roots i / roots j", "1 ≤ roots i / roots j"),
        "MMP seam hidden": (
            "structure MMPLogMeshInput",
            "structure AssumedMMPLogMeshInput",
        ),
    }
    for label, (old, new) in mutations.items():
        require(text, old, f"mutation target {label}")
        expect_rejected(label, text.replace(old, new))
    print("PASS all finite-free/Jacobi semantic mutations")


if __name__ == "__main__":
    main()
