#!/usr/bin/env python3
"""Verify archive safety, manifest coverage, and source fidelity for T5."""

from __future__ import annotations

import argparse
import hashlib
import os
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
PHASE = ROOT / "ground_zero_work/phase29"

EXACT_COPIES = {
    Path(".gitignore"): PROJECT / ".gitignore",
    Path("LICENSE"): PROJECT / "LICENSE",
    Path("NOTICE"): PROJECT / "NOTICE",
    Path("lean-toolchain"): PROJECT / "lean-toolchain",
    Path("lake-manifest.json"): PROJECT / "lake-manifest.json",
    Path("Zeta23.lean"): PROJECT / "Zeta23.lean",
    Path("lakefile.toml"): PHASE / "PUBLIC_CANDIDATE_LAKEFILE.toml",
    Path("README.md"): PHASE / "PUBLIC_CANDIDATE_README.md",
    Path("AUDIT.md"): PHASE / "PUBLIC_CANDIDATE_AUDIT.md",
    Path("AI_ONLY_RELEASE_AUDIT.md"): PHASE / "PHASE29_AI_ONLY_RELEASE_AUDIT.md",
    Path("VERIFY.sh"): PHASE / "PUBLIC_CANDIDATE_VERIFY.sh",
    Path("verification/verify_candidate.py"): PHASE / "PUBLIC_CANDIDATE_VERIFY.py",
    Path("verification/verify_axioms.py"): PHASE / "verify_phase29_axioms.py",
}

for rel in (
    "Challenge/TheoremSevenOne.lean",
    "Solution/TheoremSevenOne.lean",
    "PrintAxioms/TheoremSevenOne.lean",
    "config-theorem-seven-one.json",
    "formalization-theorem-seven-one.yaml",
    "THEOREM_SEVEN_ONE_README.md",
):
    EXACT_COPIES[Path("comparator") / rel] = PROJECT / "comparator" / rel


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(candidate: Path) -> None:
    manifest = candidate / "SHA256SUMS"
    listed: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        expected, rel = line.split("  ", 1)
        if rel in listed:
            raise SystemExit(f"FAIL duplicate manifest entry: {rel}")
        listed[rel] = expected
    actual = {
        path.relative_to(candidate).as_posix()
        for path in candidate.rglob("*")
        if path.is_file() and path != manifest
    }
    if set(listed) != actual:
        missing = sorted(actual - set(listed))
        extra = sorted(set(listed) - actual)
        raise SystemExit(f"FAIL manifest coverage missing={missing} extra={extra}")
    for rel, expected in listed.items():
        if digest(candidate / rel) != expected:
            raise SystemExit(f"FAIL manifest digest: {rel}")


def verify_source_fidelity(candidate: Path) -> None:
    for rel, source in EXACT_COPIES.items():
        target = candidate / rel
        if not target.is_file() or target.read_bytes() != source.read_bytes():
            raise SystemExit(f"FAIL source fidelity: {rel}")
    source_lean = {
        path.relative_to(PROJECT / "Zeta23")
        for path in (PROJECT / "Zeta23").rglob("*.lean")
    }
    candidate_lean = {
        path.relative_to(candidate / "Zeta23")
        for path in (candidate / "Zeta23").rglob("*.lean")
    }
    if source_lean != candidate_lean:
        raise SystemExit("FAIL Zeta23 source file set differs")
    for rel in source_lean:
        if (PROJECT / "Zeta23" / rel).read_bytes() != (candidate / "Zeta23" / rel).read_bytes():
            raise SystemExit(f"FAIL Zeta23 byte fidelity: {rel}")


def verify_no_build_artifacts(candidate: Path) -> None:
    forbidden_parts = {".lake", "__pycache__", ".git"}
    forbidden_suffixes = {".olean", ".ilean", ".o", ".c", ".pyc"}
    for path in candidate.rglob("*"):
        rel = path.relative_to(candidate)
        if any(part in forbidden_parts for part in rel.parts):
            raise SystemExit(f"FAIL forbidden directory: {rel}")
        if path.is_file() and path.suffix in forbidden_suffixes:
            raise SystemExit(f"FAIL forbidden build artifact: {rel}")
        if path.is_symlink():
            raise SystemExit(f"FAIL symlink in candidate: {rel}")


def verify_archive(candidate: Path, archive: Path) -> None:
    disk = {
        (Path(candidate.name) / path.relative_to(candidate)).as_posix(): path.read_bytes()
        for path in candidate.rglob("*") if path.is_file()
    }
    with zipfile.ZipFile(archive) as handle:
        names = handle.namelist()
        if len(names) != len(set(names)):
            raise SystemExit("FAIL duplicate archive members")
        if set(names) != set(disk):
            raise SystemExit("FAIL archive file set differs from candidate")
        for info in handle.infolist():
            pure = PurePosixPath(info.filename)
            if pure.is_absolute() or ".." in pure.parts:
                raise SystemExit(f"FAIL unsafe archive path: {info.filename}")
            if info.date_time != (2026, 1, 1, 0, 0, 0):
                raise SystemExit(f"FAIL nondeterministic archive timestamp: {info.filename}")
            if handle.read(info) != disk[info.filename]:
                raise SystemExit(f"FAIL archive bytes: {info.filename}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    candidate = args.candidate_dir.resolve()
    archive = args.archive.resolve()
    verify_manifest(candidate)
    verify_source_fidelity(candidate)
    verify_no_build_artifacts(candidate)
    verify_archive(candidate, archive)
    commit = (candidate / "SOURCE_COMMIT.txt").read_text(encoding="utf-8").strip()
    if len(commit) != 40 or any(c not in "0123456789abcdef" for c in commit):
        raise SystemExit("FAIL invalid source commit")
    print(f"PASS public candidate source commit {commit}")
    print(f"PASS public candidate files {sum(1 for p in candidate.rglob('*') if p.is_file())}")
    print(f"PASS public candidate archive SHA256 {digest(archive)}")


if __name__ == "__main__":
    main()
