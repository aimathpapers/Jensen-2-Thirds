#!/usr/bin/env python3
"""Fail closed on the explicit critical-radius coefficient budgets."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge/CriticalRadiusCoefficientBounds.lean"
)


class ContractError(RuntimeError):
    """The coefficient-budget source contract changed."""


REQUIRED = {
    "center constant": "n / 8 ≤ recurrenceP2",
    "cubic constant": "|recurrenceP3 A C D y| ≤ 2",
    "linear constant": "≤ 96 * (n * S + n * d)",
    "constant-term constant": "≤ 48 * n ^ 2 * d",
    "explicit scale threshold": "scale_small : 524288 * S ≤ n",
    "localized center": "localized : |y - B| ≤ 32 * S",
    "decomposed linear coefficient": "simp only [recurrenceP1]",
    "beta cancellation identity": "have hbetaIdentity",
    "three-quarter contraction": "(3 / 4 : ℝ) * recurrenceP2",
    "radius choice": "d (4096 * S) (3 / 4)",
    "box-to-budget constructor": "CriticalRadiusParameterGeometry.coefficientBounds",
    "complete geometry consumer": "theorem terminating3F2_critical_radius_of_geometry",
}


def validate(source: str) -> None:
    for label, needle in REQUIRED.items():
        if needle not in source:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS explicit critical-radius coefficient source contract")
    mutations = {
        "center weakened": ("n / 8 ≤ recurrenceP2", "n / 16 ≤ recurrenceP2"),
        "cubic doubled": ("|recurrenceP3 A C D y| ≤ 2", "|recurrenceP3 A C D y| ≤ 4"),
        "linear doubled": ("≤ 96 * (n * S + n * d)", "≤ 192 * (n * S + n * d)"),
        "constant doubled": ("≤ 48 * n ^ 2 * d", "≤ 96 * n ^ 2 * d"),
        "scale threshold weakened": ("524288 * S ≤ n", "262144 * S ≤ n"),
        "localization weakened": ("|y - B| ≤ 32 * S", "|y - B| ≤ 64 * S"),
        "P1 decomposition hidden": ("simp only [recurrenceP1]", "simp only [recurrenceP1_closed]"),
        "beta cancellation hidden": ("have hbetaIdentity", "have uncheckedBetaIdentity"),
        "contraction weakened": ("(3 / 4 : ℝ) * recurrenceP2", "(7 / 8 : ℝ) * recurrenceP2"),
        "radius doubled": ("d (4096 * S) (3 / 4)", "d (8192 * S) (3 / 4)"),
        "constructor disconnected": (
            "CriticalRadiusParameterGeometry.coefficientBounds",
            "uncheckedCoefficientBounds",
        ),
        "consumer hidden": (
            "theorem terminating3F2_critical_radius_of_geometry",
            "theorem uncheckedCriticalRadiusOfGeometry",
        ),
    }
    for label, (old, new) in mutations.items():
        if old not in source:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS coefficient-budget mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
