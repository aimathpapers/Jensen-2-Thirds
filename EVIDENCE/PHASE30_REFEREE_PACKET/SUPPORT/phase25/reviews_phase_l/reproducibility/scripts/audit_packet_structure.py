#!/usr/bin/env python3
"""Adversarial structure audit for the Phase-L reviewer packet.

The checks inspect candidate inputs but never use a frozen result ledger as
expected mathematical data.  Verifier-robustness mutations are constructed in
fresh temporary directories and do not modify the candidate packet.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROW = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<path>.+)$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_manifest(root: Path) -> list[tuple[str, str]]:
    rows = []
    for line in (root / "EVIDENCE_MANIFEST.sha256").read_text(
        encoding="utf-8"
    ).splitlines():
        match = ROW.fullmatch(line)
        if match is None:
            raise AssertionError(f"malformed manifest row: {line!r}")
        rows.append((match.group("path"), match.group("digest")))
    return rows


def current_manifest_checks(root: Path) -> None:
    rows = parse_manifest(root)
    paths = [relative for relative, _ in rows]
    if len(paths) != len(set(paths)):
        raise AssertionError("current manifest contains duplicate paths")
    for relative, expected in rows:
        candidate = Path(relative)
        if candidate.is_absolute() or ".." in candidate.parts:
            raise AssertionError(f"unsafe current manifest path: {relative}")
        source = root / candidate
        if not source.is_file() or sha256(source) != expected:
            raise AssertionError(f"current manifest mismatch: {relative}")
    all_files = {
        str(path.relative_to(root)) for path in root.rglob("*") if path.is_file()
    }
    unmanifested = all_files - set(paths)
    if unmanifested != {"EVIDENCE_MANIFEST.sha256"}:
        raise AssertionError(f"unexpected unmanifested files: {sorted(unmanifested)}")
    print(
        f"PASS current manifest rows: {len(rows)} unique, safe paths, exact hashes; "
        "only the manifest itself is unmanifested"
    )


def run_verifier(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "VERIFY_BUNDLE.py"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def verifier_mutations(packet_root: Path) -> None:
    verifier_source = (packet_root / "VERIFY_BUNDLE.py").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="phase-l-manifest-mutation-") as raw:
        root = Path(raw)
        (root / "VERIFY_BUNDLE.py").write_text(verifier_source, encoding="utf-8")
        (root / "alpha.txt").write_text("alpha\n", encoding="utf-8")
        (root / "unmanifested.txt").write_text("not covered\n", encoding="utf-8")
        digest = sha256(root / "alpha.txt")
        (root / "EVIDENCE_MANIFEST.sha256").write_text(
            f"{digest}  alpha.txt\n", encoding="utf-8"
        )
        extra_file_result = run_verifier(root)
        if extra_file_result.returncode != 0:
            raise AssertionError("verifier unexpectedly rejected an unmanifested file")

        # Change the protected file and rewrite the untrusted manifest.  With no
        # signed or externally pinned manifest digest, the verifier still passes.
        (root / "alpha.txt").write_text("changed alpha\n", encoding="utf-8")
        changed_digest = sha256(root / "alpha.txt")
        (root / "EVIDENCE_MANIFEST.sha256").write_text(
            f"{changed_digest}  alpha.txt\n", encoding="utf-8"
        )
        rewritten_result = run_verifier(root)
        if rewritten_result.returncode != 0:
            raise AssertionError("verifier unexpectedly rejected a rewritten manifest")

        # Duplicate rows are counted, not rejected.
        duplicate_row = f"{changed_digest}  alpha.txt\n"
        (root / "EVIDENCE_MANIFEST.sha256").write_text(
            duplicate_row + duplicate_row, encoding="utf-8"
        )
        duplicate_result = run_verifier(root)
        if duplicate_result.returncode != 0:
            raise AssertionError("verifier unexpectedly rejected duplicate rows")
    print(
        "FAIL-CLOSED TEST: packet verifier accepts unmanifested files, a rewritten "
        "self-authenticating manifest, and duplicate rows"
    )


def commit_and_checkpoint_checks(root: Path) -> None:
    metadata = json.loads((root / "BUNDLE_METADATA.json").read_text(encoding="utf-8"))
    candidate = (root / "CANDIDATE_COMMIT.txt").read_text(encoding="utf-8").strip()
    review = (root / "REVIEW_PACKET.md").read_text(encoding="utf-8")
    if candidate != metadata["candidate_commit"] or candidate not in review:
        raise AssertionError("candidate commit identifiers disagree")
    checkpoint = metadata["required_checkpoint"]
    if checkpoint not in review:
        raise AssertionError("required checkpoint identifiers disagree")
    git_metadata = root / ".git"
    print(
        "PASS commit strings agree; "
        f"candidate={candidate}; checkpoint={checkpoint}; "
        f"git_metadata_present={git_metadata.exists()}"
    )


def missing_command_inputs(root: Path) -> None:
    verifier = (root / "evidence/reproduce/VERIFY_ALL.sh").read_text(encoding="utf-8")
    referenced = sorted(
        set(re.findall(r'\$ROOT/([^"\n]+\.(?:py|sh|lean))', verifier))
    )
    missing = [relative for relative in referenced if not (root / "evidence" / relative).is_file()]
    print(
        f"VERIFY_ALL referenced_scripts={len(referenced)} missing={len(missing)}: "
        + ", ".join(missing)
    )


def behavioral_source_mutation(root: Path) -> None:
    """Show that the included behavioral suite is not connected to manuscript input."""

    source_script = (
        root
        / "evidence/ground_zero_work/phase25/reproducibility_behavioral_mutations.py"
    )
    manuscript = root / "manuscript/source/JENSEN_TWO_THIRDS_MAIN.tex"
    with tempfile.TemporaryDirectory(prefix="phase-l-source-mutation-") as raw:
        temporary = Path(raw)
        copied_script = temporary / source_script.name
        copied_manuscript = temporary / manuscript.name
        shutil.copy2(source_script, copied_script)
        text = manuscript.read_text(encoding="utf-8")
        mutated = text.replace(r"\frac{8n!}{(2n)!}", r"\frac{4n!}{(2n)!}", 1)
        if mutated == text:
            raise AssertionError("factor-eight source mutation did not apply")
        copied_manuscript.write_text(mutated, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(copied_script)],
            cwd=temporary,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            raise AssertionError("behavioral suite unexpectedly noticed source mutation")
    print(
        "FAIL-CLOSED TEST: included behavioral suite still passes beside a manuscript "
        "copy mutated from factor eight to factor four"
    )


def source_and_license_inputs(root: Path) -> None:
    source_ledger = root / "evidence/ground_zero_work/phase24/SOURCE_HASHES.sha256"
    source_names = []
    for line in source_ledger.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        match = ROW.fullmatch(line)
        if match is None:
            raise AssertionError(f"malformed source hash row: {line!r}")
        source_names.append(match.group("path"))
    present = [name for name in source_names if any(root.rglob(name))]
    licenses = [
        path
        for path in root.rglob("*")
        if path.is_file() and path.name.lower().startswith(("license", "copying", "notice"))
    ]
    print(
        f"primary_source_artifacts listed={len(source_names)} present={len(present)}; "
        f"license_notice_files={len(licenses)}"
    )


def disclosure_and_hygiene_checks(root: Path) -> None:
    textual_suffixes = {".md", ".tex", ".txt", ".json", ".py", ".sh", ".yml", ".toml", ".nb", ".lean", ".lock"}
    prior_markers = []
    personal_paths = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in textual_suffixes:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"separated .*AI|AI pre-review|review flagged", text, re.IGNORECASE):
            prior_markers.append(str(path.relative_to(root)))
        if "/Users/" in text:
            personal_paths.append(str(path.relative_to(root)))
    cache_hits = [
        str(path.relative_to(root))
        for path in root.rglob("*")
        if path.name in {".lake", ".elan", ".venv", "__pycache__", ".DS_Store"}
        or path.suffix in {".pyc", ".pyo"}
    ]
    lock = (root / "evidence/requirements-c48.lock").read_text(encoding="utf-8")
    hash_pinned = "--hash=" in lock
    print(
        f"prior-review outcome exposure files={len(set(prior_markers))}; "
        f"personal-path files={len(set(personal_paths))}; cache hits={len(cache_hits)}; "
        f"Python wheel hashes pinned={hash_pinned}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet_root", type=Path)
    args = parser.parse_args()
    root = args.packet_root.resolve()
    current_manifest_checks(root)
    verifier_mutations(root)
    commit_and_checkpoint_checks(root)
    missing_command_inputs(root)
    behavioral_source_mutation(root)
    source_and_license_inputs(root)
    disclosure_and_hygiene_checks(root)


if __name__ == "__main__":
    main()
