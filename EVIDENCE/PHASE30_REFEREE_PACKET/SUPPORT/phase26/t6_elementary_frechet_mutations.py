#!/usr/bin/env python3
"""Fail closed on semantic mutations of the elementary Fréchet assembly."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/ElementaryFrechet.lean"

REQUIRED = {
    "matrix continuous map": ("def branchMatrixCLM", 1),
    "matrix action": ("ContinuousLinearMap.mk (Matrix.mulVecLin A)", 1),
    "differentiability producer":
        ("theorem exactElementaryParameterMap_differentiableAt", 1),
    "remote producer": ("hasDerivAt_elementaryRemoteTerm_alpha", 1),
    "cube derivative producer": ("hasDerivAt_elementaryPhi", 3),
    "basis consumer": ("theorem exactElementaryParameterMap_fderiv_single", 1),
    "coordinate update": ("hasFDerivAt_update", 1),
    "alpha partial": ("hasDerivAt_elementaryCoordinateComponent_alpha", 1),
    "t partial": ("hasDerivAt_elementaryCoordinateComponent_t", 1),
    "w partial": ("hasDerivAt_elementaryCoordinateComponent_w", 1),
    "delta partial": ("hasDerivAt_elementaryCoordinateComponent_delta", 1),
    "full derivative": ("theorem exactElementaryParameterMap_hasFDerivAt", 1),
    "exact Jacobian": ("branchMatrixCLM (exactElementaryJacobian y e x)", 2),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary Frechet source contract")
    mutations = {
        "matrix action disconnected":
            ("ContinuousLinearMap.mk (Matrix.mulVecLin A)",
             "ContinuousLinearMap.mk (Matrix.vecMulLinear A)"),
        "remote producer disconnected":
            ("hasDerivAt_elementaryRemoteTerm_alpha",
             "uncheckedRemoteDerivative"),
        "coordinate update disconnected":
            ("hasFDerivAt_update", "uncheckedCoordinateUpdate"),
        "alpha partial disconnected":
            ("hasDerivAt_elementaryCoordinateComponent_alpha",
             "uncheckedAlphaPartial"),
        "t partial disconnected":
            ("hasDerivAt_elementaryCoordinateComponent_t",
             "uncheckedTPartial"),
        "w partial disconnected":
            ("hasDerivAt_elementaryCoordinateComponent_w",
             "uncheckedWPartial"),
        "delta partial disconnected":
            ("hasDerivAt_elementaryCoordinateComponent_delta",
             "uncheckedDeltaPartial"),
        "Jacobian consumer disconnected":
            ("branchMatrixCLM (exactElementaryJacobian y e x)",
             "branchMatrixCLM uncheckedJacobian"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS elementary Frechet mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
