#!/usr/bin/env python3
"""Reject proof escapes or non-foundational axioms in Phase 26 declarations."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE = ROOT / "ground_zero_work/phase26"
ACCEPTED = {"propext", "Classical.choice", "Quot.sound"}
DRIVER_ROW = re.compile(r"^#print axioms (?P<name>\S+)$")
OUTPUT_ROW = re.compile(
    r"'(?P<name>[^']+)' depends on axioms: \[(?P<axioms>.*?)\]", re.DOTALL
)
OUTPUT_EMPTY_ROW = re.compile(
    r"'(?P<name>[^']+)' does not depend on any axioms"
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    driver = [
        match.group("name")
        for line in (PHASE / "Phase26Axioms.lean").read_text().splitlines()
        if (match := DRIVER_ROW.fullmatch(line))
    ]
    if len(driver) != 1217 or len(driver) != len(set(driver)):
        raise AssertionError("Phase 26 axiom driver coverage changed")
    output = args.output.read_text()
    parsed: list[tuple[int, str, set[str]]] = []
    for match in OUTPUT_ROW.finditer(output):
        parsed.append((match.start(), match.group("name"), {
            token.strip()
            for token in match.group("axioms").replace("\n", " ").split(",")
            if token.strip()
        }))
    for match in OUTPUT_EMPTY_ROW.finditer(output):
        parsed.append((match.start(), match.group("name"), set()))
    records = {name: axioms for _, name, axioms in sorted(parsed)}
    if list(records) != driver:
        raise AssertionError("Phase 26 axiom output does not match the driver")
    for name, axioms in records.items():
        if unexpected := axioms - ACCEPTED:
            raise AssertionError(f"unexpected axioms for {name}: {sorted(unexpected)}")
    print("PASS Phase 26 axiom audit: 1217 declarations, foundational axioms only")


if __name__ == "__main__":
    main()
