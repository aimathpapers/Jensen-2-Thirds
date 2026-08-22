#!/usr/bin/env python3
"""Fail closed on mutations of the inner-box Jacobian variation proof."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/LeadingJacobianVariation.lean"

REQUIRED = {
    "coordinate producer": ("theorem branchInnerBox_coordinate_error", 1),
    "exact inner radius": ("branchInnerRadius", 4),
    "reciprocal producer": ("theorem reciprocalPower_center_error", 1),
    "product producer": ("theorem mul_reciprocalPower_center_error", 1),
    "center identity": ("theorem leadingElementaryJacobian_center", 1),
    "audited center matrix":
        ("leadingElementaryJacobian branchCenter = gaugeJacobianReal", 1),
    "entry consumer":
        ("theorem leadingElementaryJacobian_innerBox_entry_error", 1),
    "entry envelope": ("≤ 1 / 50000", 7),
    "operator consumer":
        ("theorem leadingElementaryJacobian_innerBox_operator_error", 1),
    "operator envelope": ("≤ 1 / 12500", 1),
    "operator source": ("branchMatrixCLM_sub_norm_le_of_entrywise", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(f"{label}: expected {count}, got {text.count(needle)}")


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS leading Jacobian variation source contract")
    mutations = {
        "inner radius disconnected":
            ("branchInnerRadius", "uncheckedInnerRadius"),
        "reciprocal producer disconnected":
            ("reciprocalPower_center_error", "uncheckedReciprocalError"),
        "center matrix disconnected":
            ("leadingElementaryJacobian branchCenter = gaugeJacobianReal",
             "leadingElementaryJacobian branchCenter = uncheckedJacobian"),
        "entry envelope weakened": ("≤ 1 / 50000", "≤ 1 / 60000"),
        "operator source disconnected":
            ("branchMatrixCLM_sub_norm_le_of_entrywise",
             "uncheckedEntrywiseToOperator"),
        "operator envelope weakened": ("≤ 1 / 12500", "≤ 1 / 15000"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS leading Jacobian variation mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
