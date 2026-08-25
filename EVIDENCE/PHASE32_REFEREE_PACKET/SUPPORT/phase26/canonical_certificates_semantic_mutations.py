#!/usr/bin/env python3
"""Exact property checks and mutations for the concrete finite certificates."""

from __future__ import annotations

import re
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/CanonicalCertificates.lean"
)


def residual(point: tuple[Q, Q, Q, Q]) -> tuple[Q, Q, Q, Q]:
    alpha, t, w, delta = point
    return (
        alpha * w + alpha * delta * t**2 + t**2 - 2 * alpha * t**2,
        w + delta * t**3 - t**3,
        3 * (w + delta * t**4) - 2 * t**4,
        4 * (w + delta * t**5) - 2 * t**5,
    )


def validate(center: tuple[Q, Q, Q, Q], constants: tuple[Q, Q, Q]) -> None:
    if center != (Q(3), Q(2), Q(16, 3), Q(1, 3)):
        raise AssertionError("analytic gauge coordinate order changed")
    if residual(center) != (0, 0, 0, 0):
        raise AssertionError("leading residual is nonzero at the branch center")
    k_r, c0, c1 = constants
    if constants != (Q(4096), Q(48), Q(96)):
        raise AssertionError("canonical radius constants changed")
    if not 8 * c1 / k_r + 8 * c0 / k_r**2 < Q(1, 4):
        raise AssertionError("constant-neighbor radius inequality failed")


def expect_rejected(label: str, center: tuple[Q, Q, Q, Q], constants: tuple[Q, Q, Q]) -> None:
    try:
        validate(center, constants)
    except AssertionError:
        print(f"PASS certificate mutation rejected: {label}")
        return
    raise AssertionError(f"certificate mutation escaped: {label}")


def main() -> None:
    center = (Q(3), Q(2), Q(16, 3), Q(1, 3))
    constants = (Q(4096), Q(48), Q(96))
    validate(center, constants)
    expect_rejected("alpha/t coordinate swap", (center[1], center[0], center[2], center[3]), constants)
    expect_rejected("fifth-order branch value", (Q(3), Q(2), Q(5), Q(1, 3)), constants)
    expect_rejected("radius constant weakened", center, (Q(2048), Q(48), Q(96)))
    expect_rejected("C1 envelope doubled", center, (Q(4096), Q(48), Q(192)))

    text = SOURCE.read_text(encoding="utf-8")
    for snippet in (
        "SaddleFiniteCertificate",
        "leadingGaugeResidual_eq_zero_iff",
        "limitingPositiveParameterBranch",
        "leadingResidualIntervalCertificate",
        "canonicalRadiusThresholdStage",
        "does not construct either xi-dependent interval input",
    ):
        if snippet not in text:
            raise AssertionError(f"missing concrete certificate surface: {snippet}")
    if re.search(r"^\s*(sorry|admit|axiom|unsafe)\b", text, re.MULTILINE):
        raise AssertionError("proof escape in CanonicalCertificates.lean")
    print("PASS concrete limiting-branch, saddle, and radius certificate properties")


if __name__ == "__main__":
    main()
