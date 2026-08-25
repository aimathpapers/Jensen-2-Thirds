#!/usr/bin/env python3
"""Fail closed on mutations of the auxiliary-moment integer log bridge."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/XiAuxiliaryLogBridge.lean"

REQUIRED = {
    "real factorial ratio": ("def xiFactorialRatioReal", 1),
    "real factorial ratio orientation":
        ("(m.factorial : ℝ) / ((2 * m).factorial : ℝ)", 1),
    "factorial ratio positivity": ("theorem xiFactorialRatioReal_pos", 1),
    "complex ratio bridge":
        ("theorem complexFactorialRatio_nat_eq_ofReal", 1),
    "real auxiliary moment": ("def riemannXiAuxiliaryMomentReal", 1),
    "auxiliary positivity":
        ("theorem riemannXiAuxiliaryMomentReal_pos", 1),
    "complex auxiliary bridge":
        ("theorem complexXiAuxiliaryMoment_nat_eq_ofReal", 1),
    "principal log": ("Complex.ofReal_log", 1),
    "coefficient product log":
        ("theorem exactXiCoefficientLog_eq_factorial_add_auxiliary", 1),
    "factorial recurrence": ("theorem xiFactorialRatioReal_succ", 1),
    "recurrence denominator": ("2 * (2 * (m : ℝ) + 1)", 5),
    "half-shift cancellation":
        ("theorem secondDiff_log_xiFactorialRatioReal", 1),
    "negative half-shift": ("-exactXiHalfShiftLog m 0", 1),
    "corrected coordinate bridge":
        ("theorem ofReal_exactXiAuxiliarySecondDiff\n", 1),
    "four forward bridges":
        ("theorem ofReal_exactXiAuxiliarySecondDiff_forwardDiffs", 1),
    "third forward coefficient": ("complexNatForwardDiff3", 2),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS xi auxiliary log bridge source contract")
    mutations = {
        "factorial ratio inverted":
            ("(m.factorial : ℝ) / ((2 * m).factorial : ℝ)",
             "((2 * m).factorial : ℝ) / (m.factorial : ℝ)"),
        "auxiliary positivity disconnected":
            ("theorem riemannXiAuxiliaryMomentReal_pos",
             "theorem uncheckedAuxiliaryMomentPos"),
        "complex auxiliary bridge disconnected":
            ("theorem complexXiAuxiliaryMoment_nat_eq_ofReal",
             "theorem uncheckedAuxiliaryMomentAtInteger"),
        "principal log disconnected":
            ("Complex.ofReal_log", "uncheckedPrincipalLog"),
        "coefficient product log disconnected":
            ("theorem exactXiCoefficientLog_eq_factorial_add_auxiliary",
             "theorem uncheckedCoefficientAuxiliaryLog"),
        "factorial recurrence changed":
            ("2 * (2 * (m : ℝ) + 1)", "2 * (2 * (m : ℝ) + 3)"),
        "half-shift sign reversed":
            ("-exactXiHalfShiftLog m 0", "exactXiHalfShiftLog m 0"),
        "corrected coordinate disconnected":
            ("theorem ofReal_exactXiAuxiliarySecondDiff\n",
             "theorem uncheckedAuxiliarySecondDiff\n"),
        "forward bridges disconnected":
            ("theorem ofReal_exactXiAuxiliarySecondDiff_forwardDiffs",
             "theorem uncheckedAuxiliaryForwardDiffs"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS xi auxiliary log bridge mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
