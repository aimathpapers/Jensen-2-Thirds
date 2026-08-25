#!/usr/bin/env python3
"""Validate complete multiline axiom summaries for Phase 33."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED = (
    "XiNaturalClassicalRootInputs.comparison_root_product_interval",
    "riemannXiJensenPolynomialObject_natDegree",
    "riemannXiJensenPolynomial_exactly_d_negative_roots",
    "riemannXiJensen_twoThirds_headline_exactly",
    "riemannXiJensen_twoThirds_global_headline_exactly",
)
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
SUMMARY = re.compile(
    r"'(?P<declaration>[^']+)' depends on axioms: \[(?P<axioms>.*?)\]",
    re.DOTALL,
)


def parse(text: str) -> list[tuple[str, list[str]]]:
    return [
        (
            match.group("declaration"),
            [
                name.strip()
                for name in match.group("axioms").replace("\n", " ").split(",")
                if name.strip()
            ],
        )
        for match in SUMMARY.finditer(text)
    ]


def validate(rows: list[tuple[str, list[str]]]) -> None:
    if len(rows) != len(REQUIRED):
        raise ValueError(f"expected {len(REQUIRED)} summaries, found {len(rows)}")
    text = "\n".join(declaration for declaration, _ in rows)
    for required in REQUIRED:
        if required not in text:
            raise ValueError(f"missing axiom summary: {required}")
    for declaration, names in rows:
        unexpected = [name for name in names if name not in ALLOWED]
        if unexpected:
            raise ValueError(f"unexpected axioms {unexpected!r} in {declaration}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        validate(parse(args.output.read_text(encoding="utf-8")))
    except ValueError as error:
        raise SystemExit(str(error)) from error

    synthetic = parse("'synthetic' depends on axioms: [propext,\n Evil.hidden]")
    try:
        validate([
            (f"prefix.{name}", ["propext"]) for name in REQUIRED[:-1]
        ] + [(f"prefix.{REQUIRED[-1]}", synthetic[0][1])])
    except ValueError as error:
        if "Evil.hidden" not in str(error):
            raise SystemExit(f"wrong continuation-mutation failure: {error}") from error
    else:
        raise SystemExit("continuation-line custom axiom survived")
    print("PASS Phase 33 multiline axiom audit and continuation mutation")


if __name__ == "__main__":
    main()

