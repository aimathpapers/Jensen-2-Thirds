#!/usr/bin/env python3
"""Reject unexpected axioms on the Phase-32 repair surface."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = (
    "MMPFiniteFreeLogMeshInput.hasDistinctPositiveRoots",
    "terminating3F2Polynomial_eq_finiteFree_jacobiFactors",
    "xiNaturalComparisonPolynomial_eq_finiteFree",
    "XiNaturalClassicalRootInputs.comparison_hasDistinctPositiveRoots",
    "not_twoThirdsWedge_finiteCutoffAbsorption",
    "riemannXiJensen_twoThirds_headline",
)
ALLOWED = ("propext", "Classical.choice", "Quot.sound")
FORBIDDEN = ("sorryAx", "Lean.ofReduceBool", "unsafe")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    text = args.output.read_text(encoding="utf-8")
    for declaration in REQUIRED:
        if declaration not in text:
            raise SystemExit(f"missing Phase-32 axiom summary: {declaration}")
    for token in FORBIDDEN:
        if token in text:
            raise SystemExit(f"forbidden Phase-32 axiom token: {token}")
    summaries = [line for line in text.splitlines() if "depends on axioms:" in line]
    if len(summaries) != len(REQUIRED):
        raise SystemExit(
            f"expected {len(REQUIRED)} axiom summaries, found {len(summaries)}"
        )
    for line in summaries:
        residual = line.split("depends on axioms:", 1)[1]
        names = [
            item.strip()
            for item in residual.replace("[", " ").replace("]", " ").split(",")
            if item.strip()
        ]
        unexpected = [name for name in names if name not in ALLOWED]
        if unexpected:
            raise SystemExit(f"unexpected axioms {unexpected!r} in {line}")
    print("PASS Phase 32 axiom audit")


if __name__ == "__main__":
    main()
