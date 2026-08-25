#!/usr/bin/env python3
"""Fail-closed structural checks for the Phase-24 release source tree."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


DEFAULT_ROOT = Path(__file__).resolve().parents[2]
LEAN_BASE = "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research"
LEAN_MODULES = [
    f"{LEAN_BASE}/JensenWedge/QuotientAdapter.lean",
    f"{LEAN_BASE}/JensenWedge/ComplexHermiteGenocchi.lean",
    f"{LEAN_BASE}/JensenWedge/ElementaryCubeBounds.lean",
    f"{LEAN_BASE}/JensenWedge/SaddleBounds.lean",
    f"{LEAN_BASE}/JensenWedge/JensenPolynomial.lean",
]
TEXT_FILES = [
    *LEAN_MODULES,
    f"{LEAN_BASE}/JensenWedge.lean",
    "ground_zero_work/phase24/PRIMARY_SOURCE_AUDIT.md",
    "ground_zero_work/phase24/DEPENDENCY_MATRIX.md",
    "ground_zero_work/phase24/PAPER_THEOREM_INVENTORY.md",
    "ground_zero_work/phase24/FORMALIZATION_LEDGER.md",
    "ground_zero_work/phase24/MATHEMATICA_FOLLOWUP.md",
    "ground_zero_work/phase24/mathematica_verification/VERIFICATION_RECORD.md",
    "ground_zero_work/phase24/SOURCE_HASHES.sha256",
    "ground_zero_work/phase24/INTERVAL_CERTIFICATES.json",
    "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex",
]


class ReleaseCheckError(RuntimeError):
    """A release invariant failed."""


def load_texts(root: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for relative in TEXT_FILES:
        path = root / relative
        if not path.is_file():
            raise ReleaseCheckError(f"missing required file: {relative}")
        texts[relative] = path.read_text(encoding="utf-8")
    return texts


def require(source: str, needle: str, label: str) -> None:
    if needle not in source:
        raise ReleaseCheckError(f"missing {label}: {needle!r}")


def check_texts(texts: dict[str, str]) -> None:
    for relative in LEAN_MODULES:
        source = texts[relative]
        forbidden = re.search(r"(?m)^\s*(sorry|admit|axiom|unsafe)\b", source)
        if forbidden:
            raise ReleaseCheckError(
                f"proof escape {forbidden.group(1)!r} in {relative}"
            )

    aggregator = texts[f"{LEAN_BASE}/JensenWedge.lean"]
    for module in (
        "QuotientAdapter",
        "ComplexHermiteGenocchi",
        "ElementaryCubeBounds",
        "SaddleBounds",
        "JensenPolynomial",
    ):
        require(
            aggregator,
            f"import Zeta23.Research.JensenWedge.{module}",
            f"headline import {module}",
        )

    manuscript = texts[
        "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex"
    ]
    require(manuscript, r"n^2\log(n+2)\ge Kd^3", "two-thirds theorem")
    require(
        manuscript,
        "AI-assisted evidence, not human or peer review",
        "review disclosure",
    )
    if not re.search(r"six\s+repeated FTC steps, the exact Newton identity", manuscript):
        raise ReleaseCheckError("missing current Hermite--Genocchi Lean scope")
    if not re.search(r"Public\s+posting has been authorized", manuscript):
        raise ReleaseCheckError("missing publication authorization")
    if not re.search(r"corrections should appear as new versions", manuscript):
        raise ReleaseCheckError("missing public versioning policy")
    require(
        manuscript,
        r"\gamma(n)=\frac{8\,n!}{(2n)!}",
        "correct factor-eight prefactor",
    )
    require(
        manuscript,
        r"\omega(e^{2u})e^{u/2}u^{2n}",
        "correct factor-eight kernel weight",
    )
    require(
        manuscript,
        r"\left|\frac{y^kp_F^{(k)}(y)}{p_F(y)}\right|^{1/k}",
        "correct critical-point radius",
    )
    require(
        manuscript,
        r"\begin{lemma}[Finite multiplier stability]",
        "multiplier-stability statement",
    )
    require(
        manuscript,
        r"\ll\frac{d^3}{n^2\log(n+2)}\le\frac{C'}K",
        "two-thirds exponent arithmetic",
    )
    require(
        manuscript,
        "astronomically large sufficient threshold",
        "effectivity disclosure",
    )
    require(
        manuscript,
        r"\frac{\lambda_j}{\lambda_{j+1}}\ge1",
        "MMP logarithmic-mesh convention",
    )
    require(
        manuscript,
        r"P_{1,m}&=c_{m+1}+(D+m)b_m",
        "displayed P1 recurrence coefficient",
    )
    require(
        manuscript,
        "user-executed Mathematica 15.0.1 reconstruction returned exact",
        "completed second-CAS reconstruction",
    )
    require(manuscript, r"|\arg K_s|<1/20", "Gaussian half-plane argument")
    require(
        manuscript,
        r"O(e^{-c|s|\log\log|s|})",
        "endpoint-connector estimate",
    )
    for stale in (
        r"\frac{8\,2^{2n}}{(2n)!}",
        r"\omega(e^{2u})e^u u^{2n}",
        r"\frac{p_F^{(k)}(y)}{k!p_F(y)}",
        r"\max_{0\le k\le d}",
        "Mathematica reconstruction still to be run",
    ):
        if stale in manuscript:
            raise ReleaseCheckError(f"stale false manuscript display: {stale!r}")
    if "human reviewed" in manuscript.lower() or "peer-reviewed" in manuscript.lower():
        raise ReleaseCheckError("manuscript overclaims human or peer review")

    followup = texts["ground_zero_work/phase24/MATHEMATICA_FOLLOWUP.md"]
    require(followup, "Do not import JSON, Python, SymPy", "clean-room CAS rule")
    require(followup, "Status: completed with exact `MATCH` results", "CAS completion")
    require(followup, "M1. Saddle derivative tower", "saddle CAS follow-up")
    require(
        followup,
        "M2. Shifted hypergeometric differential equation",
        "recurrence CAS follow-up",
    )
    require(followup, "| M4 | `MATCH` |", "M4 acceptance")

    mathematica_record = texts[
        "ground_zero_work/phase24/mathematica_verification/VERIFICATION_RECORD.md"
    ]
    require(
        mathematica_record,
        "user-executed exact Mathematica verification",
        "Mathematica provenance",
    )
    require(
        mathematica_record,
        "not human or peer review",
        "Mathematica review boundary",
    )
    require(
        mathematica_record,
        "1faea5fcb35b504b5d0aad9391999a99e530373dce36addb496eabb133fb04cc",
        "Mathematica ledger hash",
    )

    audit = texts["ground_zero_work/phase24/PRIMARY_SOURCE_AUDIT.md"]
    require(audit, "MSS Theorem 1.6", "corrected MSS source seam")
    require(audit, "pins **v3**", "MMP v3 pin")
    require(audit, "Definition 2.16 and Proposition 2.17", "MMP mesh convention pin")
    require(audit, "not human or peer review", "source-audit disclosure")

    ledger = texts["ground_zero_work/phase24/SOURCE_HASHES.sha256"]
    hash_rows = [line for line in ledger.splitlines() if line and not line.startswith("#")]
    if len(hash_rows) != 8:
        raise ReleaseCheckError("source hash ledger must contain exactly eight artifacts")
    for row in hash_rows:
        if not re.fullmatch(r"[0-9a-f]{64}  [A-Za-z0-9_.-]+", row):
            raise ReleaseCheckError(f"malformed source hash row: {row!r}")


def check_git(root: Path) -> None:
    checkpoint = "5f79158f9c6276dd09142edeea279e35b0d58406"
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", checkpoint, "HEAD"],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        raise ReleaseCheckError(f"required checkpoint {checkpoint} is not an ancestor")


def main(argv: list[str]) -> None:
    root = Path(argv[1]).resolve() if len(argv) == 2 else DEFAULT_ROOT
    if len(argv) > 2:
        raise SystemExit(f"usage: {Path(argv[0]).name} [repository-root]")
    check_texts(load_texts(root))
    check_git(root)
    print("PASS phase24 release-source checks")


if __name__ == "__main__":
    try:
        main(sys.argv)
    except ReleaseCheckError as exc:
        raise SystemExit(f"FAIL: {exc}") from exc
