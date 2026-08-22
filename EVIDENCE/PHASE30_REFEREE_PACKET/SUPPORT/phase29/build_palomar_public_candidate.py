#!/usr/bin/env python3
"""Build a deterministic, cache-free public-repository candidate for T5."""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE = ROOT / "ground_zero_work/phase29"
PROJECT = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
FIXED_ZIP_TIME = (2026, 1, 1, 0, 0, 0)

PROJECT_FILES = [
    ".gitignore",
    "LICENSE",
    "NOTICE",
    "lean-toolchain",
    "lake-manifest.json",
    "Zeta23.lean",
]

COMPARATOR_FILES = [
    "Challenge/TheoremSevenOne.lean",
    "Solution/TheoremSevenOne.lean",
    "PrintAxioms/TheoremSevenOne.lean",
    "config-theorem-seven-one.json",
    "formalization-theorem-seven-one.yaml",
    "THEOREM_SEVEN_ONE_README.md",
]


def copy_file(source: Path, target: Path, *, executable: bool = False) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    os.chmod(target, 0o755 if executable else 0o644)


def source_commit() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    commit = result.stdout.strip()
    if len(commit) != 40:
        raise SystemExit("FAIL source commit is not a full SHA")
    return commit


def write_manifest(candidate: Path) -> None:
    files = sorted(
        path for path in candidate.rglob("*")
        if path.is_file() and path.name != "SHA256SUMS"
    )
    lines = []
    for path in files:
        rel = path.relative_to(candidate).as_posix()
        lines.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {rel}\n")
    (candidate / "SHA256SUMS").write_text("".join(lines), encoding="utf-8")
    os.chmod(candidate / "SHA256SUMS", 0o644)


def assemble(candidate: Path) -> None:
    if candidate.exists():
        raise SystemExit(f"FAIL candidate path already exists: {candidate}")
    candidate.mkdir(parents=True)

    for rel in PROJECT_FILES:
        copy_file(PROJECT / rel, candidate / rel)
    shutil.copytree(
        PROJECT / "Zeta23",
        candidate / "Zeta23",
        ignore=shutil.ignore_patterns(".DS_Store", "*.olean", "*.ilean", "*.c", "*.o"),
    )
    for path in (candidate / "Zeta23").rglob("*"):
        if path.is_file():
            os.chmod(path, 0o644)

    for rel in COMPARATOR_FILES:
        copy_file(PROJECT / "comparator" / rel, candidate / "comparator" / rel)

    copy_file(PHASE / "PUBLIC_CANDIDATE_LAKEFILE.toml", candidate / "lakefile.toml")
    copy_file(PHASE / "PUBLIC_CANDIDATE_README.md", candidate / "README.md")
    copy_file(PHASE / "PUBLIC_CANDIDATE_AUDIT.md", candidate / "AUDIT.md")
    copy_file(PHASE / "PHASE29_AI_ONLY_RELEASE_AUDIT.md", candidate / "AI_ONLY_RELEASE_AUDIT.md")
    copy_file(PHASE / "PUBLIC_CANDIDATE_VERIFY.sh", candidate / "VERIFY.sh", executable=True)
    copy_file(
        PHASE / "PUBLIC_CANDIDATE_VERIFY.py",
        candidate / "verification/verify_candidate.py",
        executable=True,
    )
    copy_file(
        PHASE / "verify_phase29_axioms.py",
        candidate / "verification/verify_axioms.py",
        executable=True,
    )

    (candidate / "SOURCE_COMMIT.txt").write_text(source_commit() + "\n", encoding="utf-8")
    os.chmod(candidate / "SOURCE_COMMIT.txt", 0o644)
    write_manifest(candidate)


def zip_candidate(candidate: Path, archive: Path) -> None:
    if archive.exists():
        raise SystemExit(f"FAIL archive path already exists: {archive}")
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as handle:
        for path in sorted(p for p in candidate.rglob("*") if p.is_file()):
            rel = Path(candidate.name) / path.relative_to(candidate)
            info = zipfile.ZipInfo(rel.as_posix(), FIXED_ZIP_TIME)
            mode = 0o755 if os.access(path, os.X_OK) else 0o644
            info.external_attr = (stat.S_IFREG | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            handle.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-dir", type=Path, required=True)
    parser.add_argument("--archive", type=Path, required=True)
    args = parser.parse_args()
    candidate = args.candidate_dir.resolve()
    archive = args.archive.resolve()
    assemble(candidate)
    zip_candidate(candidate, archive)
    print(f"PASS assembled {candidate}")
    print(f"PASS archive SHA256 {hashlib.sha256(archive.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
