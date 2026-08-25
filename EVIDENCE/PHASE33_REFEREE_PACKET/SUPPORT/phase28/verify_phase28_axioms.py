#!/usr/bin/env python3
"""Audit the Phase-28 terminal declarations for proof escapes."""

from __future__ import annotations

import argparse
from pathlib import Path


REQUIRED = (
    "manuscriptOuterSector_parameter_geometry",
    "manuscriptInnerSector_subset_leanXiCoefficientSector",
    "manuscriptTheoremSevenOne_effective",
    "manuscriptTheoremSevenOne",
    "manuscriptPaperRelativeError_derivatives_through_six",
)
FORBIDDEN = ("sorryAx", "Lean.ofReduceBool", "unsafe")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    text = args.output.read_text(encoding="utf-8")
    for name in REQUIRED:
        if name not in text:
            raise SystemExit(f"missing axiom-audit declaration: {name}")
    for token in FORBIDDEN:
        if token in text:
            raise SystemExit(f"forbidden axiom-audit token: {token}")
    allowed = ("propext", "Classical.choice", "Quot.sound")
    axiom_lines = [line for line in text.splitlines() if "depends on axioms:" in line]
    if len(axiom_lines) != len(REQUIRED):
        raise SystemExit(
            f"expected {len(REQUIRED)} axiom summaries, found {len(axiom_lines)}"
        )
    for line in axiom_lines:
        residual = line.split("depends on axioms:", 1)[1]
        for word in residual.replace("[", " ").replace("]", " ").split(","):
            name = word.strip()
            if name and name not in allowed:
                raise SystemExit(f"unexpected axiom {name!r} in {line}")
    print("PASS Phase 28 terminal axiom audit")


if __name__ == "__main__":
    main()
