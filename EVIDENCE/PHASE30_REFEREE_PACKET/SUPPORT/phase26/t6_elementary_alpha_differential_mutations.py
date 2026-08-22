#!/usr/bin/env python3
"""Fail closed on semantic mutations of the remote alpha differential."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ElementaryAlphaDifferential.lean"
)


class ContractError(RuntimeError):
    """The alpha-differential source contract changed."""


REQUIRED = {
    "leading alpha": ("def leadingElementaryCoordinatePartialAlpha", 1),
    "surviving component": ("if j = 0 then -alpha⁻¹ ^ 2 else 0", 1),
    "error bound": ("def elementaryRemoteDerivativeErrorBound", 1),
    "remote power": ("e ^ (elementaryComponentOrder j - 1)", 1),
    "consumer": ("theorem elementaryCoordinatePartialAlpha_error", 1),
    "q1 producer": ("elementaryRemoteTerm_alpha_q1_error", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary alpha-differential source contract")
    mutations = {
        "surviving component changed": (
            "if j = 0 then -alpha⁻¹ ^ 2 else 0",
            "if j = 1 then -alpha⁻¹ ^ 2 else 0",
        ),
        "inverse order weakened": ("-alpha⁻¹ ^ 2", "-alpha⁻¹"),
        "remote power changed": (
            "e ^ (elementaryComponentOrder j - 1)",
            "e ^ elementaryComponentOrder j",
        ),
        "consumer disconnected": (
            "theorem elementaryCoordinatePartialAlpha_error",
            "theorem uncheckedAlphaColumn",
        ),
    }
    for label, (old, new) in mutations.items():
        if source.count(old) < 1:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS elementary alpha mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
