#!/usr/bin/env python3
"""Verify a blob-free cryptographic Git commit-parent ancestry proof."""

from __future__ import annotations

import base64
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
proof = json.loads((ROOT / "ANCESTRY_PROOF.json").read_text(encoding="utf-8"))
algorithm = proof["object_format"]
if algorithm not in {"sha1", "sha256"}:
    raise SystemExit(f"FAIL unsupported Git object format: {algorithm}")
chain = proof["chain"]
if not chain or chain[0]["oid"] != proof["candidate"]:
    raise SystemExit("FAIL candidate is not the first commit")
if chain[-1]["oid"] != proof["checkpoint"]:
    raise SystemExit("FAIL checkpoint is not the last commit")
for index, row in enumerate(chain):
    raw = base64.b64decode(row["commit_base64"], validate=True)
    framed = b"commit " + str(len(raw)).encode("ascii") + b"\0" + raw
    actual = hashlib.new(algorithm, framed).hexdigest()
    if actual != row["oid"]:
        raise SystemExit(f"FAIL commit object hash at chain index {index}")
    parents = [
        line.removeprefix(b"parent ").decode("ascii")
        for line in raw.splitlines()
        if line.startswith(b"parent ")
    ]
    if index + 1 < len(chain) and chain[index + 1]["oid"] not in parents:
        raise SystemExit(f"FAIL broken parent edge at chain index {index}")
print(
    "PASS candidate/checkpoint cryptographic ancestry proof "
    f"({len(chain)} commits)"
)
