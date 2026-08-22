#!/usr/bin/env python3
"""Fail closed on semantic mutations of the fixed-box elementary C1 bounds."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/ElementaryC1Box.lean"

REQUIRED = {
    "scale producer": ("theorem elementaryScale_comparisons", 1),
    "scale conclusion": ("x * e ≤ x ∧ x ≤ x / e ∧ e ^ 2 ≤ e ∧ e ^ 3 ≤ e", 1),
    "value producer": ("theorem exactElementaryParameterMap_outerBox_value_error", 1),
    "value source": ("elementaryCoordinateComponent_value_error", 1),
    "value envelope": ("10000 * (e + x / e)", 1),
    "Jacobian producer": ("theorem exactElementaryJacobian_outerBox_entry_error", 1),
    "Jacobian source": ("exactElementaryJacobian_entry_error", 1),
    "Jacobian envelope": ("10000 * (e + x)", 1),
    "outer box": ("(hy : InOuterParameterBox y)", 2),
    "weight-square bound": ("y 2 * y 2 * e ≤ 36 * e", 2),
    "delta-square bound": ("y 3 * y 3 * e ≤ (25 / 144 : ℝ) * e", 2),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary C1 fixed-box source contract")
    mutations = {
        "scale producer disconnected":
            ("theorem elementaryScale_comparisons", "theorem uncheckedScaleComparisons"),
        "x/e value scale deleted": ("10000 * (e + x / e)", "10000 * (e + x)"),
        "value producer disconnected":
            ("elementaryCoordinateComponent_value_error", "uncheckedComponentValueError"),
        "Jacobian producer disconnected":
            ("exactElementaryJacobian_entry_error", "uncheckedJacobianEntryError"),
        "Jacobian constant weakened": ("10000 * (e + x)", "9999 * (e + x)"),
        "weight square weakened":
            ("y 2 * y 2 * e ≤ 36 * e", "y 2 * y 2 * e ≤ 35 * e"),
        "delta square weakened":
            ("y 3 * y 3 * e ≤ (25 / 144 : ℝ) * e",
             "y 3 * y 3 * e ≤ (1 / 6 : ℝ) * e"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS elementary C1 mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
