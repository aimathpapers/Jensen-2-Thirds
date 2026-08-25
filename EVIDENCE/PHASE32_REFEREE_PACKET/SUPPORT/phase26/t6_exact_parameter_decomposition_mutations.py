#!/usr/bin/env python3
"""Fail closed on semantic mutations of the exact parameter-map split."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/ExactParameterDecomposition.lean"

REQUIRED = {
    "saddle map": ("def exactXiSaddleParameterMap", 1),
    "auxiliary coordinate": ("def exactXiAuxiliarySecondDiff", 1),
    "gamma duplication bridge":
        ("exactXiHalfShiftLog n k + secondDiff exactXiCoefficientLog (n + k)", 1),
    "first scale": ("-((n : ℝ) * L) *", 1),
    "second scale": ("((n : ℝ) ^ 2 * L / 2) *", 1),
    "third scale": ("-((n : ℝ) ^ 3 * L / 2) *", 1),
    "fourth scale": ("((n : ℝ) ^ 4 * L / 6) *", 1),
    "second difference": ("secondDiff exactXiCoefficientLog", 1),
    "corrected saddle coordinate": ("exactXiAuxiliarySecondDiff", 8),
    "half-shift producer": ("theorem exactXiHalfShiftLog_eq_neg_logRatio", 1),
    "half-shift sign": ("-logRatio (((1 : ℝ) + (1 / (n : ℝ)) / 2)", 1),
    "quotient split": ("theorem exactXiQuotientResidual_eq_elementary_add_saddle", 1),
    "cube source": ("elementaryTriangularParameterMap_eq_exactElementary", 1),
    "map split": ("theorem exactXiParameterMap_eq_elementary_add_saddle", 1),
    "outer box": ("(hy : InOuterParameterBox y)", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS exact parameter-decomposition source contract")
    mutations = {
        "first triangular sign reversed": ("-((n : ℝ) * L) *", "((n : ℝ) * L) *"),
        "third triangular sign reversed":
            ("-((n : ℝ) ^ 3 * L / 2) *", "((n : ℝ) ^ 3 * L / 2) *"),
        "fourth denominator changed":
            ("((n : ℝ) ^ 4 * L / 6) *", "((n : ℝ) ^ 4 * L / 4) *"),
        "half-shift sign removed":
            ("-logRatio (((1 : ℝ) + (1 / (n : ℝ)) / 2)",
             "logRatio (((1 : ℝ) + (1 / (n : ℝ)) / 2)"),
        "second difference renamed":
            ("secondDiff exactXiCoefficientLog", "uncheckedDiff exactXiCoefficientLog"),
        "gamma half-shift dropped from saddle":
            ("exactXiHalfShiftLog n k + secondDiff exactXiCoefficientLog (n + k)",
             "secondDiff exactXiCoefficientLog (n + k)"),
        "corrected coordinate disconnected":
            ("exactXiAuxiliarySecondDiff", "uncheckedXiAuxiliarySecondDiff"),
        "cube source disconnected":
            ("elementaryTriangularParameterMap_eq_exactElementary",
             "uncheckedTriangularParameterMapEq"),
        "final consumer disconnected":
            ("theorem exactXiParameterMap_eq_elementary_add_saddle",
             "theorem uncheckedXiParameterMapSplit"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS exact parameter-decomposition mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
