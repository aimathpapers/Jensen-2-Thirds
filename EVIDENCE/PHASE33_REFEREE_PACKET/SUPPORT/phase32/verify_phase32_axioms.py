#!/usr/bin/env python3
"""Reject unexpected axioms on the Phase-32 repair surface."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED = (
    "MMPFiniteFreeLogMeshInput.hasDistinctPositiveRoots",
    "terminating3F2Polynomial_eq_finiteFree_jacobiFactors",
    "xiNaturalComparisonPolynomial_eq_finiteFree",
    "XiNaturalClassicalRootInputs.comparison_hasDistinctPositiveRoots",
    "XiNaturalClassicalRootInputs.comparison_root_product_interval",
    "not_twoThirdsWedge_finiteCutoffAbsorption",
    "riemannXiJensenPolynomial_exactly_d_negative_roots",
    "riemannXiJensen_twoThirds_headline",
    "riemannXiJensen_twoThirds_headline_exactly",
    "riemannXiJensen_twoThirds_global_headline_exactly",
)
ALLOWED = ("propext", "Classical.choice", "Quot.sound")
FORBIDDEN = ("sorryAx", "Lean.ofReduceBool", "unsafe")
SUMMARY = re.compile(
    r"'(?P<declaration>[^']+)' depends on axioms: \[(?P<axioms>.*?)\]",
    re.DOTALL,
)


def parse_summaries(text: str) -> list[tuple[str, list[str]]]:
    summaries: list[tuple[str, list[str]]] = []
    for match in SUMMARY.finditer(text):
        names = [
            name.strip()
            for name in match.group("axioms").replace("\n", " ").split(",")
            if name.strip()
        ]
        summaries.append((match.group("declaration"), names))
    return summaries


def reject_unexpected_axioms(summaries: list[tuple[str, list[str]]]) -> None:
    for declaration, names in summaries:
        unexpected = [name for name in names if name not in ALLOWED]
        if unexpected:
            raise SystemExit(
                f"unexpected axioms {unexpected!r} in {declaration}"
            )


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
    summaries = parse_summaries(text)
    if len(summaries) != len(REQUIRED):
        raise SystemExit(
            f"expected {len(REQUIRED)} axiom summaries, found {len(summaries)}"
        )
    reject_unexpected_axioms(summaries)

    synthetic = parse_summaries(
        "'synthetic' depends on axioms: [propext,\n Review.customAxiom]"
    )
    try:
        reject_unexpected_axioms(synthetic)
    except SystemExit:
        pass
    else:
        raise SystemExit("continuation-line custom-axiom mutation survived")
    print("PASS Phase 32 multiline axiom audit and continuation mutation")


if __name__ == "__main__":
    main()
