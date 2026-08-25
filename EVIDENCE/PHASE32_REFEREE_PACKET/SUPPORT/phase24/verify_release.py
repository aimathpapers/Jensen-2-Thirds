#!/usr/bin/env python3
"""Verify the external checksums and every member of the Phase-24 ZIP."""

from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/release"
ZIP_PATH = OUT / "Jensen_Two_Thirds_Phase24.zip"
PDF = ROOT / "output/pdf/JENSEN_TWO_THIRDS_UNIFIED.pdf"
CHECKSUMS = OUT / "SHA256SUMS.json"
PREFIX = "Jensen_Two_Thirds_Phase24/"
SOURCE_COMMIT = "d71b3d683e67296fd15e41d013a444df5fe2ec5f"
REVIEW_STATUS = (
    "separated analytic and algebraic AI pre-review completed; "
    "user-executed Mathematica M1-M4 exact matches; "
    "not human or peer review"
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    expected = json.loads(CHECKSUMS.read_text(encoding="utf-8"))
    actual = {
        ZIP_PATH.name: digest(ZIP_PATH.read_bytes()),
        PDF.name: digest(PDF.read_bytes()),
        "RELEASE_MANIFEST.sha256": digest((OUT / "RELEASE_MANIFEST.sha256").read_bytes()),
    }
    if actual != expected:
        raise SystemExit("FAIL external release checksums")

    with zipfile.ZipFile(ZIP_PATH) as archive:
        if archive.testzip() is not None:
            raise SystemExit("FAIL corrupt ZIP member")
        names = archive.namelist()
        forbidden = ("/.lake/", "/.venv/", "/.git/", "/__pycache__/", "/AGENTS.md")
        for name in names:
            if not name.startswith(PREFIX) or any(item in name for item in forbidden):
                raise SystemExit(f"FAIL forbidden or unscoped ZIP member: {name}")

        manifest_name = PREFIX + "RELEASE_MANIFEST.sha256"
        metadata_name = PREFIX + "RELEASE_METADATA.json"
        manifest = archive.read(manifest_name).decode("utf-8")
        metadata = json.loads(archive.read(metadata_name).decode("utf-8"))
        if not re.fullmatch(r"[0-9a-f]{40}", metadata["source_commit"]):
            raise SystemExit("FAIL malformed source commit")
        if metadata["source_commit"] != SOURCE_COMMIT:
            raise SystemExit("FAIL ZIP does not identify the immutable source commit")
        if metadata["review_status"] != REVIEW_STATUS:
            raise SystemExit("FAIL review-status disclosure")

        rows = [line for line in manifest.splitlines() if line]
        for row in rows:
            expected_hash, relative = row.split("  ", 1)
            member = PREFIX + relative
            if digest(archive.read(member)) != expected_hash:
                raise SystemExit(f"FAIL internal manifest mismatch: {relative}")

        required_markers = {
            "ground_zero_work/phase24/verification_logs/phase24.log":
                "PASS Phase 24 formalization, interval, and mutation gates",
            "ground_zero_work/phase24/verification_logs/phase21.log":
                "PASS: Phase 21 complete direct-sector proof-surface checks",
            "ground_zero_work/phase24/verification_logs/phase20.log":
                "Phase 20 verification PASS",
        }
        for relative, marker in required_markers.items():
            text = archive.read(PREFIX + relative).decode("utf-8")
            if marker not in text:
                raise SystemExit(f"FAIL missing serial marker in {relative}")

        pdf = archive.read(PREFIX + "manuscript/JENSEN_TWO_THIRDS_UNIFIED.pdf")
        if not pdf.startswith(b"%PDF-") or len(pdf) < 100_000:
            raise SystemExit("FAIL manuscript PDF sanity check")
        if len(rows) < 500:
            raise SystemExit("FAIL release artifact unexpectedly incomplete")

    print(
        "PASS verified Phase-24 ZIP, external checksums, internal manifest, "
        f"serial logs, and {len(rows)} members"
    )


if __name__ == "__main__":
    main()
