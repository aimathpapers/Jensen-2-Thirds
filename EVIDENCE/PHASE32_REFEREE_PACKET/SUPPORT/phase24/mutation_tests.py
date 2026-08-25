#!/usr/bin/env python3
"""Mutation tests proving that the new Phase-24 gates fail closed."""

from __future__ import annotations

import copy
import json

import release_checks
import verify_interval_certificates


def expect_rejected(
    name: str,
    original: dict[str, str],
    relative: str,
    old: str,
    new: str,
) -> None:
    mutated = copy.deepcopy(original)
    if old not in mutated[relative]:
        raise AssertionError(f"mutation fixture not found for {name}: {old!r}")
    mutated[relative] = mutated[relative].replace(old, new)
    try:
        release_checks.check_texts(mutated)
    except release_checks.ReleaseCheckError:
        print(f"PASS mutation rejected: {name}")
        return
    raise AssertionError(f"mutation survived release checks: {name}")


def main() -> None:
    texts = release_checks.load_texts(release_checks.DEFAULT_ROOT)
    manuscript = "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex"
    aggregator = f"{release_checks.LEAN_BASE}/JensenWedge.lean"
    quotient = f"{release_checks.LEAN_BASE}/JensenWedge/QuotientAdapter.lean"
    hashes = "ground_zero_work/phase24/SOURCE_HASHES.sha256"
    followup = "ground_zero_work/phase24/MATHEMATICA_FOLLOWUP.md"

    expect_rejected(
        "wedge exponent",
        texts,
        manuscript,
        r"n^2\log(n+2)\ge Kd^3",
        r"n^2\log(n+2)\ge Kd^4",
    )
    expect_rejected(
        "review overclaim",
        texts,
        manuscript,
        "AI-assisted evidence, not human review or peer review",
        "peer-reviewed",
    )
    expect_rejected(
        "factor-eight factorial",
        texts,
        manuscript,
        r"\gamma(n)=\frac{8\,n!}{(2n)!}",
        r"\gamma(n)=\frac{8\,2^{2n}}{(2n)!}",
    )
    expect_rejected(
        "factor-eight kernel weight",
        texts,
        manuscript,
        r"\omega(e^{2u})e^{u/2}u^{2n}",
        r"\omega(e^{2u})e^u u^{2n}",
    )
    expect_rejected(
        "critical-point radius",
        texts,
        manuscript,
        r"\left|\frac{y^kp_F^{(k)}(y)}{p_F(y)}\right|^{1/k}",
        r"\left|\frac{p_F^{(k)}(y)}{k!p_F(y)}\right|^{1/k}",
    )
    expect_rejected(
        "Hermite--Genocchi Lean scope",
        texts,
        manuscript,
        "six repeated FTC steps, the exact Newton identity",
        "a named six-simplex identity assumption",
    )
    expect_rejected(
        "effectivity overclaim",
        texts,
        manuscript,
        "astronomically large sufficient threshold",
        "computationally useful threshold",
    )
    expect_rejected(
        "log-mesh convention reversal",
        texts,
        manuscript,
        r"\frac{\lambda_j}{\lambda_{j+1}}\ge1",
        r"\frac{\lambda_{j+1}}{\lambda_j}\ge1",
    )
    expect_rejected(
        "missing P1 recurrence display",
        texts,
        manuscript,
        r"P_{1,m}&=c_{m+1}+(D+m)b_m",
        r"P_{1,m}&=\text{omitted}",
    )
    expect_rejected(
        "Lean proof escape",
        texts,
        quotient,
        "namespace Zeta23.Research.JensenWedge",
        "namespace Zeta23.Research.JensenWedge\n\nsorry",
    )
    expect_rejected(
        "missing headline import",
        texts,
        aggregator,
        "import Zeta23.Research.JensenWedge.SaddleBounds",
        "-- removed SaddleBounds import",
    )
    first_hash = texts[hashes].splitlines()[2]
    expect_rejected(
        "malformed source hash",
        texts,
        hashes,
        first_hash,
        "0" + first_hash,
    )
    expect_rejected(
        "CAS clean-room rule",
        texts,
        followup,
        "Do not import JSON, Python, SymPy",
        "Import JSON, Python, SymPy",
    )
    expect_rejected(
        "Mathematica M4 completion",
        texts,
        followup,
        "| M4 | `MATCH` |",
        "| M4 | `MISMATCH` |",
    )

    exact = verify_interval_certificates.build_certificate()
    mutated = copy.deepcopy(exact)
    mutated["branch_box"]["point"][0] = "4/1"  # type: ignore[index]
    if json.dumps(mutated, sort_keys=True) == json.dumps(exact, sort_keys=True):
        raise AssertionError("interval mutation was ineffective")
    committed = json.loads(
        verify_interval_certificates.CERTIFICATE.read_text(encoding="utf-8")
    )
    if committed != exact or mutated == exact:
        raise AssertionError("interval oracle setup failed")
    print("PASS mutation rejected: branch-box point")

    mutated_h6 = copy.deepcopy(exact)
    mutated_h6["sixth_derivative_majorant"]["strict_upper"] = "9000/1"  # type: ignore[index]
    if committed != exact or mutated_h6 == exact:
        raise AssertionError("H6 majorant mutation setup failed")
    print("PASS mutation rejected: H6 majorant certificate")
    print("PASS all phase24 mutation tests")


if __name__ == "__main__":
    main()
