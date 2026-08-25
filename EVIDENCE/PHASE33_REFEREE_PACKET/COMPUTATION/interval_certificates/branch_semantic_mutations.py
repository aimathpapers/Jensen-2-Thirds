#!/usr/bin/env python3
"""Fail-closed semantic source mutations for the quantitative branch layer."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT / "Kimi_Agent_Riemann Lean Exploration" / "zeta-23-lean" / "Zeta23"
    / "Research" / "JensenWedge" / "QuantitativeBranch.lean"
)


class ContractError(RuntimeError):
    pass


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise ContractError(f"{label}: expected once, found {count}")


def validate(text: str) -> None:
    checks = {
        "coordinate order": "analytic gauge order `(alpha,t,w,delta)`",
        "inner radius": "branchInnerRadius : ℝ := 1 / 1000000",
        "outer ordering": "theorem outerBox_jacobi_ordering",
        "inverse norm": "∑ j, |gaugeJacobianInvReal i j| ≤ 304 / 3",
        "residual factor": "center_residual : ‖G center‖ ≤ (3 / 608) * radius",
        "whole-box derivative": "derivative_defect : ∀ y ∈ closedBall center radius",
        "half contraction": "noncomputable def halfContraction : NNReal := ⟨1 / 2",
        "Banach theorem": "theorem fourDimensionalBranch_existsUnique",
        "local uniqueness": "locally_unique : ∀ z ∈ branchInnerBox",
        "localization constant": "localizationConstant : ℝ := 12 + 8 * Real.sqrt 6",
        "localization threshold": "localizationThreshold = 262144",
        "radius stage": "structure RadiusThresholdStage",
        "eventual stage": "structure EventualThresholdStage",
        "xi input": "structure XiCoefficientEstimate",
        "comparison input": "structure ComparisonRootCertificate",
        "sixth input": "structure SixthResidualCertificate",
        "typed assembly": "def JensenWedgeAnalyticInputs.toJensenWedgeCertificate",
    }
    for label, needle in checks.items():
        require_once(text, needle, label)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS branch mutation rejected: {label}")
        return
    raise AssertionError(f"branch mutation survived: {label}")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    validate(text)
    print("PASS quantitative branch source contract")
    mutations = {
        "coordinate permutation": (
            "analytic gauge order `(alpha,t,w,delta)`",
            "analytic gauge order `(t,w,delta,alpha)`",
        ),
        "inverse norm weakened": ("≤ 304 / 3", "≤ 304 / 4"),
        "center residual doubled": (
            "center_residual : ‖G center‖ ≤ (3 / 608) * radius",
            "center_residual : ‖G center‖ ≤ (3 / 304) * radius",
        ),
        "center-only Jacobian": (
            "derivative_defect : ∀ y ∈ closedBall center radius",
            "derivative_defect : ∀ y ∈ {center}",
        ),
        "contraction removed": (
            "theorem fourDimensionalBranch_existsUnique",
            "theorem assumed_fourDimensionalBranch_existsUnique",
        ),
        "C_loc transposed": (
            "localizationConstant : ℝ := 12 + 8 * Real.sqrt 6",
            "localizationConstant : ℝ := 8 + 12 * Real.sqrt 6",
        ),
        "threshold regressed": (
            "localizationThreshold = 262144",
            "localizationThreshold = 8192",
        ),
        "typed builder disconnected": (
            "def JensenWedgeAnalyticInputs.toJensenWedgeCertificate",
            "def assumedAnalyticInputs.toJensenWedgeCertificate",
        ),
    }
    for label, (old, new) in mutations.items():
        require_once(text, old, f"mutation target {label}")
        expect_rejected(label, text.replace(old, new, 1))
    print("PASS all quantitative branch semantic mutations")


if __name__ == "__main__":
    main()
