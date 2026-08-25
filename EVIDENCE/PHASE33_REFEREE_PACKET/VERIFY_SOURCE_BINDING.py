#!/usr/bin/env python3
"""Verify packet payload hashes and, when present, their bundled Git source."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OID = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
EXCLUDED = {"MANIFEST.sha256", "SOURCE_TREE_BINDING.json"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def packet_files() -> set[str]:
    return {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and path.relative_to(ROOT).as_posix() not in EXCLUDED
    }


def verify_payloads(binding: dict[str, object]) -> None:
    rows = binding["packet_entries"]
    if not isinstance(rows, list):
        raise AssertionError("packet_entries must be a list")
    declared: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise AssertionError("malformed source-binding row")
        packet_path = row["packet_path"]
        if not isinstance(packet_path, str) or packet_path in declared:
            raise AssertionError(f"duplicate or invalid packet path: {packet_path!r}")
        declared.add(packet_path)
        path = ROOT / packet_path
        if not path.is_file() or sha256(path) != row["sha256"]:
            raise AssertionError(f"packet/source binding mismatch: {packet_path}")
        matches = row["candidate_matches"]
        if not isinstance(matches, list):
            raise AssertionError(f"invalid candidate match list: {packet_path}")
        for match in matches:
            if not OID.fullmatch(match["git_blob_oid"]):
                raise AssertionError(f"invalid Git blob id: {packet_path}")
    actual = packet_files()
    if actual != declared:
        missing = sorted(actual - declared)
        extra = sorted(declared - actual)
        raise AssertionError(f"source-binding coverage mismatch missing={missing} extra={extra}")


def verify_history(binding: dict[str, object]) -> bool:
    bundle = ROOT / "AUDIT/CANDIDATE_HISTORY.bundle"
    if not bundle.is_file():
        return False
    candidate = binding["candidate_commit"]
    with tempfile.TemporaryDirectory(prefix="phase33-binding-") as temporary:
        repository = Path(temporary) / "repository"
        environment = os.environ.copy()
        environment["GIT_CONFIG_NOSYSTEM"] = "1"
        subprocess.run(
            [
                "git",
                "clone",
                "--quiet",
                "--branch",
                "phase-m-candidate",
                str(bundle),
                str(repository),
            ],
            check=True,
            env=environment,
        )
        tree = subprocess.run(
            ["git", "show", "-s", "--format=%T", candidate],
            cwd=repository,
            check=True,
            stdout=subprocess.PIPE,
        ).stdout.decode("ascii").strip()
        if tree != binding["candidate_tree"]:
            raise AssertionError("candidate tree id mismatch")
        checked: dict[tuple[str, str], str] = {}
        for row in binding["packet_entries"]:
            for match in row["candidate_matches"]:
                key = (match["source_path"], match["git_blob_oid"])
                if key not in checked:
                    oid = subprocess.run(
                        ["git", "rev-parse", f"{candidate}:{key[0]}"],
                        cwd=repository,
                        check=True,
                        stdout=subprocess.PIPE,
                    ).stdout.decode("ascii").strip()
                    if oid != key[1]:
                        raise AssertionError(f"Git blob mismatch: {key[0]}")
                    payload = subprocess.run(
                        ["git", "show", f"{candidate}:{key[0]}"],
                        cwd=repository,
                        check=True,
                        stdout=subprocess.PIPE,
                    ).stdout
                    checked[key] = hashlib.sha256(payload).hexdigest()
                if checked[key] != row["sha256"]:
                    raise AssertionError(f"Git payload mismatch: {key[0]}")
    return True


def main() -> None:
    binding = json.loads((ROOT / "SOURCE_TREE_BINDING.json").read_text())
    metadata = json.loads((ROOT / "RELEASE_METADATA.json").read_text())
    ancestry = json.loads((ROOT / "ANCESTRY_PROOF.json").read_text())
    candidate = binding["candidate_commit"]
    if candidate != metadata["candidate_commit"] or candidate != ancestry["candidate"]:
        raise AssertionError("candidate identity drift across release records")
    if not OID.fullmatch(candidate) or not OID.fullmatch(binding["candidate_tree"]):
        raise AssertionError("invalid candidate object id")
    verify_payloads(binding)
    history_checked = verify_history(binding)
    suffix = " and bundled Git tree" if history_checked else ""
    print(f"PASS packet payload/source binding{suffix}")


if __name__ == "__main__":
    main()
