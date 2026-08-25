#!/usr/bin/env python3
"""Fail-closed verification of every file in this extracted package."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "MANIFEST.sha256"
ROW = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<path>.+)$")
rows = []
for line in MANIFEST.read_text(encoding="utf-8").splitlines():
    match = ROW.fullmatch(line)
    if match is None:
        raise SystemExit(f"FAIL malformed manifest row: {line!r}")
    relative = match.group("path")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or relative == "MANIFEST.sha256":
        raise SystemExit(f"FAIL unsafe manifest path: {relative!r}")
    rows.append((relative, match.group("digest")))
if not rows:
    raise SystemExit("FAIL empty manifest")
paths = [relative for relative, _ in rows]
if len(paths) != len(set(paths)):
    raise SystemExit("FAIL duplicate manifest path")
actual = {
    str(path.relative_to(ROOT))
    for path in ROOT.rglob("*")
    if path.is_file() and path.name != "MANIFEST.sha256"
}
if actual != set(paths):
    raise SystemExit(
        f"FAIL manifest coverage: missing={sorted(set(paths)-actual)}, "
        f"extra={sorted(actual-set(paths))}"
    )
for relative, expected in rows:
    path = ROOT / relative
    if not path.is_file() or path.is_symlink():
        raise SystemExit(f"FAIL missing or symbolic-link file: {relative}")
    actual_digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual_digest != expected:
        raise SystemExit(f"FAIL hash mismatch: {relative}")
print(f"PASS package manifest ({len(rows)} files)")
