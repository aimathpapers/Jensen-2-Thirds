#!/usr/bin/env python3
"""Check machine-readable theorem locations against the manuscript structure.

Expected locations are selected by matching each claim's mathematical subject
to the manuscript's own section titles.  No frozen verifier result or prior
review report is used as expected data.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


SUBJECT_SECTION_TITLES = {
    "T2": "Quantitative sectorial saddle",
    "T3": "Contour deformation and leading mode",
    "T4": "Higher theta modes and coefficient theorem",
    "T5": "Higher theta modes and coefficient theorem",
    "T6": "Logarithmic derivatives through order six",
    "T7": "Six matches and quotient coordinates",
    "T8": "Elementary cube calculus",
    "T9": "Quantitative positive branch",
    "T10": "Jacobi factors and finite-free convolution",
    "T11": "Jacobi factors and finite-free convolution",
    "T12": "Jacobi factors and finite-free convolution",
    "T13": "Terminating hypergeometric ODE",
    "T14": "Critical-point derivative radius",
    "T15": "Complex Hermite--Genocchi residual",
    "T16": "Multiplier stability and final assembly",
    "T17": "Multiplier stability and final assembly",
}


def normalize_tex(value: str) -> str:
    return value.replace("--", "--").strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet_root", type=Path)
    args = parser.parse_args()
    root = args.packet_root.resolve()
    tex = (root / "manuscript/source/JENSEN_TWO_THIRDS_MAIN.tex").read_text(
        encoding="utf-8"
    )
    numbered_tex = tex.split(r"\appendix", 1)[0]
    section_titles = [
        normalize_tex(title)
        for title in re.findall(r"\\section\{([^}]*)\}", numbered_tex)
    ]
    section_numbers = {title: index + 1 for index, title in enumerate(section_titles)}
    matrix = json.loads(
        (
            root
            / "evidence/ground_zero_work/phase25/THEOREM_ASSURANCE_MATRIX.json"
        ).read_text(encoding="utf-8")
    )
    claims = {claim["id"]: claim for claim in matrix["claims"]}
    mismatches = []
    for claim_id, title in SUBJECT_SECTION_TITLES.items():
        expected = section_numbers.get(title)
        if expected is None:
            raise AssertionError(f"manuscript lacks expected subject section: {title}")
        source = claims[claim_id]["paper_source"]
        numbers = [int(value) for value in re.findall(r"(?:Section|Lemma|Theorem) (\d+)", source)]
        if expected not in numbers:
            mismatches.append((claim_id, expected, source))

    t18_source = claims["T18"]["paper_source"]
    t18_numbers = [int(value) for value in re.findall(r"\d+", t18_source)]
    if any(number in {10, 11, 12} for number in t18_numbers):
        mismatches.append(("T18", "Theorem 1.1 and final assembly Sections 15--19", t18_source))

    empty_lean = [
        claim["id"]
        for claim in matrix["claims"]
        if "lean_kernel" in claim["channels"] and not claim["lean_declarations"]
    ]
    print("Manuscript sections:")
    for number, title in enumerate(section_titles, 1):
        print(f"  {number}: {title}")
    print("Crosswalk mismatches:")
    for claim_id, expected, recorded in mismatches:
        print(f"  {claim_id}: expected {expected}; recorded {recorded}")
    print(f"lean_kernel channel with no declarations: {empty_lean}")
    if not mismatches:
        raise AssertionError("adversarial check expected stale crosswalks but found none")


if __name__ == "__main__":
    main()
