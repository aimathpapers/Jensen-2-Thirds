#!/usr/bin/env python3
"""Fail closed on semantic mutations of the elementary component value proof."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ElementaryComponentValue.lean"
)


class ContractError(RuntimeError):
    """The component-value source contract changed."""


REQUIRED = {
    "remote limit": ("def elementaryRemoteLimit", 1),
    "remote case": ("if j = 0 then alpha⁻¹ else 0", 1),
    "leading seam": ("theorem leadingElementaryCoordinateComponent_eq_map", 1),
    "remote error": ("theorem elementaryRemoteTerm_limit_error", 1),
    "q1 producer": ("elementaryPhi_remote_q1_error halpha₀ halpha hx he", 1),
    "value consumer": ("theorem elementaryCoordinateComponent_value_error", 1),
    "paired producer": ("elementaryPhi_paired_value_error ht₀ ht hw he hx", 1),
    "gamma producer": ("elementaryPhi_boundary_value_error hdelta he hx", 1),
    "half shift": ("(elementaryComponentOrder j : ℝ) * (x / e)", 2),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary component-value source contract")
    mutations = {
        "remote component changed": (
            "if j = 0 then alpha⁻¹ else 0",
            "if j = 1 then alpha⁻¹ else 0",
        ),
        "leading seam disconnected": (
            "theorem leadingElementaryCoordinateComponent_eq_map",
            "theorem uncheckedLeadingComponent",
        ),
        "remote producer disconnected": (
            "elementaryPhi_remote_q1_error halpha₀ halpha hx he",
            "uncheckedRemoteError halpha₀ halpha hx he",
        ),
        "paired producer disconnected": (
            "elementaryPhi_paired_value_error ht₀ ht hw he hx",
            "uncheckedPairedError ht₀ ht hw he hx",
        ),
        "gamma producer disconnected": (
            "elementaryPhi_boundary_value_error hdelta he hx",
            "uncheckedGammaError hdelta he hx",
        ),
        "half-shift scale removed": ("(x / e)", "x"),
        "value consumer disconnected": (
            "theorem elementaryCoordinateComponent_value_error",
            "theorem uncheckedComponentValue",
        ),
    }
    for label, (old, new) in mutations.items():
        if source.count(old) < 1:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS elementary component-value mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
