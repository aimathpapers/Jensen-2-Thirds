#!/usr/bin/env python3
"""Fail closed on mutations of the elementary operator-norm certificate."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/ElementaryJacobianOperator.lean"

REQUIRED = {
    "entrywise operator producer":
        ("theorem branchMatrixCLM_sub_norm_le_of_entrywise", 1),
    "four row sum": ("≤ 4 * C", 1),
    "fixed inverse": ("def gaugeInverseCLM", 1),
    "audited inverse matrix": ("branchMatrixCLM gaugeJacobianInvReal", 1),
    "inverse application": ("gaugeInverseCLM v = gaugeInverseAction v", 1),
    "inverse norm": ("theorem gaugeInverseCLM_norm_le", 1),
    "exact inverse constant": ("‖gaugeInverseCLM‖ ≤ 304 / 3", 1),
    "box operator consumer":
        ("theorem exactElementaryJacobian_outerBox_operator_error", 1),
    "entry source": ("exactElementaryJacobian_outerBox_entry_error", 1),
    "operator envelope": ("40000 * (e + x)", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary Jacobian operator source contract")
    mutations = {
        "row count weakened": ("≤ 4 * C", "≤ 3 * C"),
        "inverse matrix disconnected":
            ("branchMatrixCLM gaugeJacobianInvReal",
             "branchMatrixCLM uncheckedInverseMatrix"),
        "inverse constant weakened":
            ("‖gaugeInverseCLM‖ ≤ 304 / 3", "‖gaugeInverseCLM‖ ≤ 100"),
        "entry producer disconnected":
            ("exactElementaryJacobian_outerBox_entry_error",
             "uncheckedEntrywiseBound"),
        "operator envelope weakened":
            ("40000 * (e + x)", "30000 * (e + x)"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS elementary Jacobian operator mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
