#!/usr/bin/env python3
"""Fail closed on mutations of the localized forward-difference adapter."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/LocalForwardDifferenceCalculus.lean"

REQUIRED = {
    "real segment": ("theorem complexSegment_real_add_one", 1),
    "real segment target": ("= ((x + t : ℝ) : ℂ)", 1),
    "localized FTC": ("theorem complexSegment_integral_deriv_of_uIcc", 1),
    "localized derivative hypothesis":
        ("hf : ∀ t ∈ Set.uIcc (0 : ℝ) 1", 1),
    "finite translate derivative":
        ("theorem hasDerivAt_complexForwardDiff_on_real", 1),
    "finite translate condition":
        ("hpoints : ∀ j ≤ q, x + (j : ℝ) ∈ S", 1),
    "local norm adapter":
        ("theorem norm_complexForwardDiff_sub_constant_le_on_real_interval", 1),
    "local interval derivative":
        ("y ∈ Set.Icc x (x + (q : ℝ))", 2),
    "top derivative order": ("derivs (r + q) (y : ℂ) - c", 1),
    "localized FTC consumer":
        ("complexSegment_integral_deriv_of_uIcc g g'", 1),
    "constant subtraction":
        ("g' (complexSegment (x : ℂ) ((x + 1 : ℝ) : ℂ) t) - c", 3),
    "unit interval mass": ("M * |(1 : ℝ) - 0|", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS local forward-difference source contract")
    mutations = {
        "segment target changed":
            ("= ((x + t : ℝ) : ℂ)", "= ((x - t : ℝ) : ℂ)"),
        "FTC localization removed":
            ("hf : ∀ t ∈ Set.uIcc (0 : ℝ) 1", "hf : ∀ t : ℝ"),
        "finite translate condition weakened":
            ("hpoints : ∀ j ≤ q, x + (j : ℝ) ∈ S",
             "hpoints : ∀ j < q, x + (j : ℝ) ∈ S"),
        "interval direction changed":
            ("y ∈ Set.Icc x (x + (q : ℝ))",
             "y ∈ Set.Icc x (x - (q : ℝ))"),
        "top derivative order changed":
            ("derivs (r + q) (y : ℂ) - c", "derivs r (y : ℂ) - c"),
        "localized FTC disconnected":
            ("complexSegment_integral_deriv_of_uIcc g g'",
             "uncheckedLocalSegmentIntegral g g'"),
        "constant subtraction changed":
            ("g' (complexSegment (x : ℂ) ((x + 1 : ℝ) : ℂ) t) - c",
             "g' (complexSegment (x : ℂ) ((x + 1 : ℝ) : ℂ) t) + c"),
        "unit mass changed": ("M * |(1 : ℝ) - 0|", "2 * M"),
        "final adapter renamed":
            ("theorem norm_complexForwardDiff_sub_constant_le_on_real_interval",
             "theorem uncheckedLocalForwardDifferenceBound"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS local forward-difference mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
