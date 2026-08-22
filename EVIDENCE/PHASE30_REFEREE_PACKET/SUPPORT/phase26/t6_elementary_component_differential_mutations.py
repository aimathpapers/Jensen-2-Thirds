#!/usr/bin/env python3
"""Fail closed on semantic mutations of the elementary component differential."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ElementaryComponentDifferential.lean"
)


class ContractError(RuntimeError):
    """The component-differential source contract changed."""


REQUIRED = {
    "component": ("def elementaryCoordinateComponent", 1),
    "exact seam": ("theorem elementaryCoordinateComponent_eq_exact", 1),
    "alpha partial": ("def elementaryCoordinatePartialAlpha", 1),
    "t partial": ("def elementaryCoordinatePartialT", 1),
    "w partial": ("def elementaryCoordinatePartialW", 1),
    "delta partial": ("def elementaryCoordinatePartialDelta", 1),
    "alpha producer": (
        "theorem hasDerivAt_elementaryCoordinateComponent_alpha", 1
    ),
    "t producer": ("theorem hasDerivAt_elementaryCoordinateComponent_t", 1),
    "w producer": ("theorem hasDerivAt_elementaryCoordinateComponent_w", 1),
    "delta producer": (
        "theorem hasDerivAt_elementaryCoordinateComponent_delta", 1
    ),
    "leading t sign": (
        "(-(elementaryComponentOrder j : ℝ) *", 3
    ),
    "t error": ("theorem elementaryCoordinatePartialT_error", 1),
    "w error": ("theorem elementaryCoordinatePartialW_error", 1),
    "delta error": ("theorem elementaryCoordinatePartialDelta_error", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary component-differential source contract")
    mutations = {
        "exact seam disconnected": (
            "theorem elementaryCoordinateComponent_eq_exact",
            "theorem uncheckedCoordinateSeam",
        ),
        "alpha producer disconnected": (
            "theorem hasDerivAt_elementaryCoordinateComponent_alpha",
            "theorem uncheckedAlphaProducer",
        ),
        "t producer disconnected": (
            "theorem hasDerivAt_elementaryCoordinateComponent_t",
            "theorem uncheckedTProducer",
        ),
        "w producer disconnected": (
            "theorem hasDerivAt_elementaryCoordinateComponent_w",
            "theorem uncheckedWProducer",
        ),
        "delta producer disconnected": (
            "theorem hasDerivAt_elementaryCoordinateComponent_delta",
            "theorem uncheckedDeltaProducer",
        ),
        "leading t sign reversed": (
            "(-(elementaryComponentOrder j : ℝ) *",
            "((elementaryComponentOrder j : ℝ) *",
        ),
        "t error disconnected": (
            "theorem elementaryCoordinatePartialT_error",
            "theorem uncheckedTError",
        ),
        "w error disconnected": (
            "theorem elementaryCoordinatePartialW_error",
            "theorem uncheckedWError",
        ),
        "delta error disconnected": (
            "theorem elementaryCoordinatePartialDelta_error",
            "theorem uncheckedDeltaError",
        ),
    }
    for label, (old, new) in mutations.items():
        if source.count(old) < 1:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS elementary component-differential mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
