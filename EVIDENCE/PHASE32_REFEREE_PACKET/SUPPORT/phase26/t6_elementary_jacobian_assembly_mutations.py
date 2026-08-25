#!/usr/bin/env python3
"""Fail closed on semantic mutations of elementary Jacobian assembly."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/ElementaryJacobianAssembly.lean"

REQUIRED = {
    "exact": ("def exactElementaryJacobian", 1),
    "leading": ("def leadingElementaryJacobian", 1),
    "partials": ("theorem elementaryCoordinateComponent_has_all_partials", 1),
    "alpha column": ("elementaryRemoteDerivativeErrorBound j alpha₀ e x", 1),
    "t column": ("t₀⁻¹ ^ (elementaryComponentOrder j + 3)", 1),
    "w column": ("t₀⁻¹ ^ (elementaryComponentOrder j + 2)", 1),
    "delta column": ("((elementaryComponentOrder j : ℝ) * x + delta * e)", 1),
    "consumer": ("theorem exactElementaryJacobian_entry_error", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary Jacobian-assembly source contract")
    mutations = {
        "exact matrix disconnected": ("def exactElementaryJacobian", "def uncheckedExactJacobian"),
        "leading matrix disconnected": ("def leadingElementaryJacobian", "def uncheckedLeadingJacobian"),
        "partial producer disconnected": ("theorem elementaryCoordinateComponent_has_all_partials", "theorem uncheckedAllPartials"),
        "alpha column disconnected": ("elementaryRemoteDerivativeErrorBound j alpha₀ e x", "uncheckedAlphaBound j alpha₀ e x"),
        "t order weakened": ("t₀⁻¹ ^ (elementaryComponentOrder j + 3)", "t₀⁻¹ ^ (elementaryComponentOrder j + 2)"),
        "consumer disconnected": ("theorem exactElementaryJacobian_entry_error", "theorem uncheckedJacobianError"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS elementary Jacobian mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
