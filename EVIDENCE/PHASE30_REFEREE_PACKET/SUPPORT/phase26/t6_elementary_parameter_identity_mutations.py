#!/usr/bin/env python3
"""Fail closed on semantic mutations of the logarithmic-boundary identity."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ElementaryParameterIdentity.lean"
)


class ContractError(RuntimeError):
    """The exact source-identity contract changed."""


REQUIRED = {
    "scaling producer": "theorem elementaryPhi_div_scale",
    "scaling orientation":
        "elementaryPhi q (s / e) z = e ^ q * elementaryPhi q s (z * e)",
    "five-boundary residual": "logRatio (y 0 / (x * e)) k -\n"
        "    logRatio ((y 1 + y 2 * e) / x) k +\n"
        "    logRatio (y 1 / x) k -\n"
        "    logRatio ((1 + y 3 * e) / x) k +\n"
        "    logRatio ((1 + x / 2) / x) k",
    "triangular first":
        "-(1 / (x * e)) * natForwardDiff0 (elementaryQuotientResidual y x e)",
    "triangular second":
        "(1 / (2 * x ^ 2 * e)) * natForwardDiff1 (elementaryQuotientResidual y x e)",
    "triangular third":
        "-(1 / (2 * x ^ 3 * e)) * natForwardDiff2 (elementaryQuotientResidual y x e)",
    "triangular fourth":
        "(1 / (6 * x ^ 4 * e)) * natForwardDiff3 (elementaryQuotientResidual y x e)",
    "forward zero": "theorem elementaryQuotientResidual_forward0",
    "forward one": "theorem elementaryQuotientResidual_forward1",
    "forward two": "theorem elementaryQuotientResidual_forward2",
    "forward three": "theorem elementaryQuotientResidual_forward3",
    "identity consumer":
        "theorem elementaryTriangularParameterMap_eq_exactElementary",
}


def validate(text: str) -> None:
    for label, needle in REQUIRED.items():
        if text.count(needle) != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary parameter-identity source contract")
    mutations = {
        "scaling direction reversed": (
            "elementaryPhi q (s / e) z = e ^ q * elementaryPhi q s (z * e)",
            "elementaryPhi q (s / e) z = e ^ q * elementaryPhi q s (z / e)",
        ),
        "B sign reversed": (
            "logRatio (y 0 / (x * e)) k -\n    logRatio",
            "logRatio (y 0 / (x * e)) k +\n    logRatio",
        ),
        "C sign reversed": (
            ") / x) k +\n    logRatio (y 1 / x) k -",
            ") / x) k -\n    logRatio (y 1 / x) k -",
        ),
        "D sign reversed": (
            "logRatio (y 1 / x) k -\n    logRatio ((1 + y 3 * e) / x) k +",
            "logRatio (y 1 / x) k +\n    logRatio ((1 + y 3 * e) / x) k +",
        ),
        "half shift sign reversed": (
            "logRatio ((1 + y 3 * e) / x) k +\n    logRatio ((1 + x / 2) / x) k",
            "logRatio ((1 + y 3 * e) / x) k -\n    logRatio ((1 + x / 2) / x) k",
        ),
        "first triangular sign reversed": (
            "-(1 / (x * e)) * natForwardDiff0",
            "(1 / (x * e)) * natForwardDiff0",
        ),
        "second triangular factorial removed": (
            "(1 / (2 * x ^ 2 * e)) * natForwardDiff1",
            "(1 / (x ^ 2 * e)) * natForwardDiff1",
        ),
        "third triangular sign reversed": (
            "-(1 / (2 * x ^ 3 * e)) * natForwardDiff2",
            "(1 / (2 * x ^ 3 * e)) * natForwardDiff2",
        ),
        "fourth triangular factorial changed": (
            "(1 / (6 * x ^ 4 * e)) * natForwardDiff3",
            "(1 / (4 * x ^ 4 * e)) * natForwardDiff3",
        ),
        "forward producer removed": (
            "theorem elementaryQuotientResidual_forward2",
            "theorem uncheckedElementaryForward2",
        ),
        "identity consumer removed": (
            "theorem elementaryTriangularParameterMap_eq_exactElementary",
            "theorem uncheckedElementaryParameterIdentity",
        ),
    }
    for label, (old, new) in mutations.items():
        if source.count(old) != 1:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS elementary parameter-identity mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
