#!/usr/bin/env python3
"""Fail closed on mutations of repeated-FTC forward-difference calculus."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/ForwardDifferenceCalculus.lean"

REQUIRED = {
    "recursive definition": ("def complexForwardDiff", 1),
    "recursive sign":
        ("complexForwardDiff q f (z + 1) - complexForwardDiff q f z", 1),
    "derivative tower": ("theorem hasDerivAt_complexForwardDiff", 1),
    "tower source": ("hderiv : ∀ r z, HasDerivAt", 3),
    "tower continuity": ("theorem continuous_complexDerivativeTower", 1),
    "quantitative adapter":
        ("theorem norm_complexForwardDiff_sub_constant_le", 1),
    "top derivative": ("derivs (r + q) w - c", 1),
    "complex FTC": ("complexSegment_integral_deriv", 1),
    "constant subtraction":
        ("g' (complexSegment z (z + 1) t) - c", 3),
    "unit interval mass": ("M * |(1 : ℝ) - 0|", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS forward-difference calculus source contract")
    mutations = {
        "recursive sign changed":
            ("complexForwardDiff q f (z + 1) - complexForwardDiff q f z",
             "complexForwardDiff q f (z + 1) + complexForwardDiff q f z"),
        "derivative tower disconnected":
            ("theorem hasDerivAt_complexForwardDiff",
             "theorem uncheckedHasDerivAtForwardDiff"),
        "tower source disconnected":
            ("hderiv : ∀ r z, HasDerivAt", "hderiv : ∀ r z, True → HasDerivAt"),
        "complex FTC disconnected":
            ("complexSegment_integral_deriv", "uncheckedSegmentIntegral"),
        "constant subtraction changed":
            ("g' (complexSegment z (z + 1) t) - c",
             "g' (complexSegment z (z + 1) t) + c"),
        "unit mass changed": ("M * |(1 : ℝ) - 0|", "2 * M"),
        "final adapter renamed":
            ("theorem norm_complexForwardDiff_sub_constant_le",
             "theorem uncheckedForwardDifferenceBound"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS forward-difference calculus mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
