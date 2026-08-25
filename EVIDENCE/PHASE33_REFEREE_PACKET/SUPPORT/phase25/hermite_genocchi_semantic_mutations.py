#!/usr/bin/env python3
"""Fail-closed source mutations for the order-six Hermite--Genocchi chain."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Kimi_Agent_Riemann Lean Exploration" / "zeta-23-lean" / "Zeta23" / "Research" / "JensenWedge"
CUBE = LEAN / "HermiteGenocchiCube.lean"
FTC = LEAN / "HermiteGenocchiFTC.lean"
ADAPTER = LEAN / "ComplexHermiteGenocchi.lean"


class ContractError(RuntimeError):
    """A load-bearing source contract is absent or ambiguous."""


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise ContractError(f"{label}: expected exactly one occurrence, found {count}")


def require_count(text: str, needle: str, expected: int, label: str) -> None:
    count = text.count(needle)
    if count != expected:
        raise ContractError(f"{label}: expected {expected} occurrences, found {count}")


def validate(cube: str, ftc: str, adapter: str) -> None:
    combined = cube + ftc + adapter
    if "(hHG" in combined or "(hNewton :" in combined:
        raise ContractError("legacy free Hermite--Genocchi/Newton premise remains")
    require_once(cube, "theorem norm_hermiteGenocchiCubeSix_le", "cube norm theorem")
    require_once(cube, "theorem norm_hermiteGenocchiIntegralSix_le", "node norm theorem")
    require_once(cube, "theorem hermiteGenocchiCubePoint_mem_convex", "convex-hull theorem")
    require_once(ftc, "theorem hasDerivAt_complexSegmentWeighted\n", "global differentiation theorem")
    require_once(ftc, "theorem hasDerivAt_complexSegmentWeightedOn", "local differentiation theorem")
    require_once(ftc, "theorem hermiteGenocchiSix_newton_identity\n", "global repeated-FTC identity")
    require_once(ftc, "theorem hermiteGenocchiSix_newton_identityOn", "local repeated-FTC identity")
    require_once(ftc, "hermiteGenocchiTriangleMass 5 0 = 1 / 720", "triangle mass")
    require_count(ftc, "(w - nodes 5) * q 5 w", 2, "sixth Newton factors")
    require_once(adapter, "theorem hermiteGenocchiSix_remainder_bound\n", "modular remainder theorem")
    require_once(
        adapter,
        "theorem hermiteGenocchiSix_remainder_bound_of_derivative_tower",
        "derived remainder theorem",
    )
    require_once(adapter, "theorem hermiteGenocchiSix_remainder_bound_on", "local remainder theorem")
    require_count(adapter, "‖derivs 6 w‖ ≤ M", 2, "sixth derivative bounds")
    require_once(
        adapter,
        "hermiteGenocchiSix_newton_identity derivs hderiv hcont hzero z",
        "derived Newton seam",
    )
    require_once(
        adapter,
        "hermiteGenocchiSix_newton_identityOn u hu hconvU",
        "localized Newton seam",
    )
    require_count(adapter, "≤ M * ρ ^ 6 / 720", 3, "remainder normalization")
    require_count(cube, "≤ M / 720", 2, "cube normalization")
    require_once(cube, "((1 - u₀) ^ 5 : ℂ)", "outer Jacobian exponent 5")
    require_count(cube, "((1 - u₁) ^ 4 : ℂ)", 2, "Jacobian exponent 4")
    require_count(cube, "((1 - u₂) ^ 3 : ℂ)", 2, "Jacobian exponent 3")
    require_count(cube, "((1 - u₃) ^ 2 : ℂ)", 2, "Jacobian exponent 2")
    require_count(cube, "((1 - u₄) : ℂ)", 2, "Jacobian exponent 1")


def expect_rejected(label: str, cube: str, ftc: str, adapter: str) -> None:
    try:
        validate(cube, ftc, adapter)
    except ContractError:
        print(f"PASS Hermite--Genocchi mutation rejected: {label}")
        return
    raise AssertionError(f"Hermite--Genocchi mutation survived: {label}")


def main() -> None:
    cube = CUBE.read_text(encoding="utf-8")
    ftc = FTC.read_text(encoding="utf-8")
    adapter = ADAPTER.read_text(encoding="utf-8")
    validate(cube, ftc, adapter)
    print("PASS Hermite--Genocchi source contract")

    expect_rejected(
        "simplex mass 1/120",
        cube,
        ftc.replace("hermiteGenocchiTriangleMass 5 0 = 1 / 720", "hermiteGenocchiTriangleMass 5 0 = 1 / 120", 1),
        adapter,
    )
    expect_rejected(
        "outer Jacobian exponent 4",
        cube.replace("((1 - u₀) ^ 5 : ℂ)", "((1 - u₀) ^ 4 : ℂ)", 1),
        ftc,
        adapter,
    )
    expect_rejected(
        "fifth derivative substituted",
        cube,
        ftc,
        adapter.replace("‖derivs 6 w‖ ≤ M", "‖derivs 5 w‖ ≤ M"),
    )
    expect_rejected(
        "repeated-FTC identity disconnected",
        cube,
        ftc,
        adapter.replace(
            "hermiteGenocchiSix_newton_identity derivs hderiv hcont hzero z",
            "sixNode_newton_identity (derivs 0) hzero",
            1,
        ),
    )
    expect_rejected(
        "sixth node transposed",
        cube,
        ftc.replace("(w - nodes 5) * q 5 w", "(w - nodes 4) * q 5 w", 1),
        adapter,
    )
    expect_rejected(
        "localized repeated-FTC identity disconnected",
        cube,
        ftc,
        adapter.replace(
            "hermiteGenocchiSix_newton_identityOn u hu hconvU",
            "hermiteGenocchiSix_newton_identity derivs",
            1,
        ),
    )
    expect_rejected(
        "Newton premise restored",
        cube,
        ftc,
        adapter.replace("(hM : 0 ≤ M)", "(hNewton : derivs 0 z = 0) (hM : 0 ≤ M)", 1),
    )
    print("PASS all Hermite--Genocchi semantic mutations")


if __name__ == "__main__":
    main()
