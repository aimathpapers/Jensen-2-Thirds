#!/usr/bin/env python3
"""Fail closed on unexpected axioms in the Phase-30 terminal surface."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = (
    "xiNaturalConcreteMultiplier_six_nodes",
    "xiNaturalConcreteMultiplier_sub_one_norm_lt_one_on_tube",
    "xiNaturalConcreteRealMultiplier_six_nodes_of_explicitCutoff",
    "xiNaturalActualComparison_relativeError_lt_one_at_critical",
    "multiplierIntervalCertificate_of_complete_roots",
    "MultiplierIntervalCertificate.actual_hasDistinctPositiveRoots",
    "xiNatural_multiplierIntervalCertificate",
    "xiNatural_jensenWedgeCertificate",
    "xiNaturalActualLogPolynomial_eq_comparisonMultiplierTransform_of_explicitCutoff",
    "xiNaturalActualLogPolynomial_roots_to_riemannXi",
    "riemannXiJensen_twoThirds_low_degree",
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
            raise SystemExit(f"missing Phase-30 axiom summary: {declaration}")
    for token in FORBIDDEN:
        if token in text:
            raise SystemExit(f"forbidden Phase-30 axiom token: {token}")
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
    print("PASS Phase 30 terminal axiom audit")


if __name__ == "__main__":
    main()
