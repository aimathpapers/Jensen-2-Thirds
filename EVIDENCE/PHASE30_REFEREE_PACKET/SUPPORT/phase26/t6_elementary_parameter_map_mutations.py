#!/usr/bin/env python3
"""Fail-closed mutations for the elementary and limiting parameter maps."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ElementaryParameterMap.lean"
)


class ContractError(RuntimeError):
    """The elementary-map source contract changed."""


REQUIRED = {
    "component order": "def elementaryComponentOrder (j : Fin 4) : ℕ := j + 1",
    "audited coefficient": "(elementaryWeight j : ℚ)",
    "remote term": "e ^ q * elementaryPhi q (y 0) (x * e)",
    "B term": "-\n      elementaryPhi q (y 1 + y 2 * e) x",
    "C term": "+\n      elementaryPhi q (y 1) x",
    "D term": "-\n      elementaryPhi q (1 + y 3 * e) x",
    "half shift": "+\n      elementaryPhi q (1 + x / 2) x",
    "normalization": "elementaryComponentCoefficient j / e *",
    "saddle vector": "def leadingXiSaddleVector : BranchPoint := ![-2, -1, -2, -2]",
    "full limit": "leadingElementaryParameterMap y + leadingXiSaddleVector",
    "center theorem": "theorem leadingXiParameterMap_center",
    "leading-system bridge": "theorem leadingXiParameterMap_eq_zero_iff",
    "positive uniqueness": "theorem leadingXiParameterMap_unique_positive",
}


def validate(text: str) -> None:
    for label, needle in REQUIRED.items():
        if text.count(needle) != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary parameter-map source contract")
    mutations = {
        "cube order shifted": ("j + 1", "j + 2"),
        "coefficient source replaced": (
            "(elementaryWeight j : ℚ)", "(boundaryWeight j : ℚ)"),
        "remote e power removed": (
            "e ^ q * elementaryPhi q (y 0) (x * e)",
            "elementaryPhi q (y 0) (x * e)"),
        "B sign reversed": (
            "-\n      elementaryPhi q (y 1 + y 2 * e) x",
            "+\n      elementaryPhi q (y 1 + y 2 * e) x"),
        "C sign reversed": (
            "+\n      elementaryPhi q (y 1) x",
            "-\n      elementaryPhi q (y 1) x"),
        "D sign reversed": (
            "-\n      elementaryPhi q (1 + y 3 * e) x",
            "+\n      elementaryPhi q (1 + y 3 * e) x"),
        "gamma half shift dropped": (
            "+\n      elementaryPhi q (1 + x / 2) x", "+\n      0"),
        "normalization changed": (
            "elementaryComponentCoefficient j / e *",
            "elementaryComponentCoefficient j * e *"),
        "saddle sign changed": (
            "![-2, -1, -2, -2]", "![2, -1, -2, -2]"),
        "limit bridge removed": (
            "theorem leadingXiParameterMap_eq_zero_iff",
            "theorem uncheckedLeadingMapBridge"),
        "uniqueness removed": (
            "theorem leadingXiParameterMap_unique_positive",
            "theorem uncheckedLeadingMapUnique"),
    }
    for label, (old, new) in mutations.items():
        if source.count(old) != 1:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS elementary parameter-map mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
