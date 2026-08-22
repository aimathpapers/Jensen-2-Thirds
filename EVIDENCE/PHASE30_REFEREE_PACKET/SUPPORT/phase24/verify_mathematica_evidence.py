#!/usr/bin/env python3
"""Verify the frozen user-executed Mathematica M1--M4 evidence."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
EVIDENCE = HERE / "mathematica_verification"
EXPECTED_HASHES = {
    "C48_Mathematica_CleanRoom_2.nb":
        "f79359ce48fe5e5015bceb88b5de82b87145da22e235688dfe3989526772dc7a",
    "C48_Mathematica_CleanRoom.pdf":
        "f2e428bdd5d1caf03243b81dbc65794950abc2c8a4c13195395eca415d7a373c",
    "C48_Mathematica_Result_Ledger.txt":
        "1faea5fcb35b504b5d0aad9391999a99e530373dce36addb496eabb133fb04cc",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(source: str, needle: str, label: str) -> None:
    if needle not in source:
        raise RuntimeError(f"missing {label}: {needle!r}")


def main() -> None:
    checksum_path = EVIDENCE / "SHA256SUMS.txt"
    rows = checksum_path.read_text(encoding="utf-8").splitlines()
    parsed: dict[str, str] = {}
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", row)
        if match is None:
            raise RuntimeError(f"malformed Mathematica checksum row: {row!r}")
        parsed[match.group(2)] = match.group(1)
    if parsed != EXPECTED_HASHES:
        raise RuntimeError("Mathematica checksum ledger does not match the freeze")
    for name, expected in EXPECTED_HASHES.items():
        path = EVIDENCE / name
        if not path.is_file() or digest(path) != expected:
            raise RuntimeError(f"Mathematica artifact hash mismatch: {name}")

    ledger = (EVIDENCE / "C48_Mathematica_Result_Ledger.txt").read_text(
        encoding="utf-8"
    )
    for needle, label in (
        ('"Version" -> "15.0.1 for Mac OS X ARM (64-bit) (July 2, 2026)"',
         "Mathematica version"),
        ('"M1" -> "MATCH"', "M1 acceptance"),
        ('"M2" -> "MATCH"', "M2 acceptance"),
        ('"M3" -> "MATCH"', "M3 acceptance"),
        ('"M4" -> "MATCH"', "M4 acceptance"),
        ('"ExactResultsContainNoMachineReals" -> True', "exact arithmetic"),
        ('"ExactCheck" -> 0', "implicit derivative identity"),
        ('"PostChainConstant" -> -12', "fifth derivative constant"),
        ('"PostChainConstant" -> 48', "sixth derivative constant"),
        ('"Reduced6Denominator" -> (4 + 4*rr - 3*ss)^12',
         "sixth denominator"),
        ('"CrossMultipliedCheck" -> 0', "coefficient recurrence"),
        ('"RecurrenceComparisons" -> {0, 0, 0, 0}',
         "four recurrence coefficients"),
        ('"Determinant" -> -1/144', "Jacobian determinant"),
        ('"InfinityNorm" -> 304/3', "Jacobian inverse norm"),
        ('"TermCount" -> 82', "H6 term count"),
        ('"TotalDegree" -> 13', "H6 total degree"),
        ('6422139805764931584036533551104/702576099728137594188684005',
         "exact H6 majorant"),
        ('"StrictlyLessThan10000" -> True', "H6 strict bound"),
    ):
        require(ledger, needle, label)
    if ledger.count('"Pass" -> True') != 3:
        raise RuntimeError("expected three exact polynomial test passes")

    notebook = (EVIDENCE / "C48_Mathematica_CleanRoom_2.nb").read_text(
        encoding="ascii"
    )
    for forbidden in (
        '"Import"', '"Get"', '"OpenRead"', '"ReadString"',
        '"ExternalEvaluate"', '"RunProcess"', '"StartProcess"',
    ):
        if forbidden in notebook:
            raise RuntimeError(f"forbidden external-input operation: {forbidden}")
    for required in (
        'Pochhammer', 'crossMultipliedCheck', 'saddleEquation',
        'gDerivative', 'reduced6', 'numeratorMajorant',
    ):
        require(notebook, required, f"notebook definition {required}")

    pdf = (EVIDENCE / "C48_Mathematica_CleanRoom.pdf").read_bytes()
    if not pdf.startswith(b"%PDF-") or len(pdf) < 80_000:
        raise RuntimeError("Mathematica PDF sanity check failed")

    print(
        "PASS Mathematica M1--M4 evidence: exact hashes, exact ledger, "
        "no external-input operations"
    )


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        raise SystemExit(f"FAIL: {exc}") from exc
