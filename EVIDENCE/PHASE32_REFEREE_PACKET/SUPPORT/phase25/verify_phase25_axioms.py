#!/usr/bin/env python3
"""Verify complete paper-facing #print axioms coverage and output."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE = ROOT / "ground_zero_work" / "phase25"
PREFIX = "Zeta23.Research.JensenWedge."
ACCEPTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
DRIVER_ROW = re.compile(r"^#print axioms (?P<name>\S+)$")
OUTPUT_ROW = re.compile(
    r"'(?P<name>[^']+)' depends on axioms: \[(?P<axioms>.*?)\]",
    re.DOTALL,
)


def expected_declarations() -> list[str]:
    matrix = json.loads(
        (PHASE / "THEOREM_ASSURANCE_MATRIX.json").read_text(encoding="utf-8")
    )
    names: list[str] = []
    for claim in matrix["claims"]:
        for name in claim["lean_declarations"]:
            if name not in names:
                names.append(name)
    return names


def parse_driver() -> list[str]:
    names = []
    for line in (PHASE / "Phase25Axioms.lean").read_text(encoding="utf-8").splitlines():
        match = DRIVER_ROW.fullmatch(line)
        if match is not None:
            names.append(match.group("name"))
    return names


def parse_output(path: Path) -> dict[str, set[str]]:
    records: dict[str, set[str]] = {}
    text = path.read_text(encoding="utf-8")
    for match in OUTPUT_ROW.finditer(text):
        name = match.group("name")
        if name in records:
            raise AssertionError(f"duplicate axiom output for {name}")
        tokens = {
            token.strip()
            for token in match.group("axioms").replace("\n", " ").split(",")
            if token.strip()
        }
        records[name] = tokens
    return records


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=PHASE / "PHASE25_AXIOM_AUDIT.txt",
    )
    arguments = parser.parse_args()

    expected = expected_declarations()
    driver = parse_driver()
    if driver != expected:
        raise AssertionError("Phase25Axioms.lean does not exactly cover matrix declarations")
    if len(driver) != len(set(driver)):
        raise AssertionError("duplicate declaration in Phase25Axioms.lean")
    if any(not name.startswith(PREFIX) for name in driver):
        raise AssertionError("unscoped declaration in Phase25Axioms.lean")

    records = parse_output(arguments.output)
    if list(records) != expected:
        raise AssertionError("axiom output does not exactly cover matrix declarations")
    for name, axioms in records.items():
        unexpected = axioms - ACCEPTED_AXIOMS
        if unexpected:
            raise AssertionError(f"unexpected axiom for {name}: {sorted(unexpected)}")
    print(
        "PASS complete Phase-25 axiom surface: "
        f"{len(expected)} declarations, only accepted foundational axioms"
    )


if __name__ == "__main__":
    main()
