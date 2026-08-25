#!/usr/bin/env python3
"""Build deterministic Phase-33 referee and full-audit release packages."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE32_PATH = ROOT / "ground_zero_work/phase32/build_phase32_release.py"
OUTPUT = ROOT / "output/reviewer_packages_phase33"
CHECKPOINT = "5f79158f9c6276dd09142edeea279e35b0d58406"
REPAIR_COMMIT = "0e478b0166fafd14eff349988048791f336d5e92"
SOURCE_DATE_EPOCH = "1787659200"
FIXED_TIMESTAMP = (2026, 8, 25, 12, 0, 0)


def load_phase32():
    spec = importlib.util.spec_from_file_location("phase32_builder", PHASE32_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Phase-32 package builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P32 = load_phase32()
BASE = P32.BASE
P30 = P32.P30
BASE.OUTPUT = OUTPUT
BASE.SOURCE_DATE_EPOCH = SOURCE_DATE_EPOCH
BASE.FIXED_TIMESTAMP = FIXED_TIMESTAMP
BASE.BUILD_PACKET_MANUSCRIPTS = BASE.BUILD_PACKET_MANUSCRIPTS.replace(
    b'export SOURCE_DATE_EPOCH="1787572800"',
    f'export SOURCE_DATE_EPOCH="{SOURCE_DATE_EPOCH}"'.encode(),
)
BASE.BUILD_PACKET_MANUSCRIPTS = BASE.BUILD_PACKET_MANUSCRIPTS.replace(
    b'"$TECTONIC" -X compile "$ROOT/PAPER/source/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex" --outdir "$TMP_DIR"\n',
    b'"$TECTONIC" -X compile "$ROOT/PAPER/source/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex" --outdir "$TMP_DIR"\n'
    b'"$TECTONIC" -X compile "$ROOT/PAPER/source/JENSEN_TWO_THIRDS_UNIFIED.tex" --outdir "$TMP_DIR"\n',
)
BASE.BUILD_PACKET_MANUSCRIPTS = BASE.BUILD_PACKET_MANUSCRIPTS.replace(
    b'cmp "$TMP_DIR/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf" "$ROOT/PAPER/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf"\n',
    b'cmp "$TMP_DIR/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf" "$ROOT/PAPER/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf"\n'
    b'cmp "$TMP_DIR/JENSEN_TWO_THIRDS_UNIFIED.pdf" "$ROOT/PAPER/JENSEN_TWO_THIRDS_UNIFIED.pdf"\n',
)
BASE.VERIFY_ARCHIVE = BASE.VERIFY_ARCHIVE.replace(
    b'python3 "$ROOT/VERIFY_ANCESTRY.py"\n',
    b'python3 "$ROOT/VERIFY_ANCESTRY.py"\npython3 "$ROOT/VERIFY_SOURCE_BINDING.py"\n',
)

PHASE33_FILES = (
    "ground_zero_work/phase33/MSS_UNGUARDED_CALL.lean.mutant",
    "ground_zero_work/phase33/PHASE32_FRESH_AI_REVIEW_FINDINGS.md",
    "ground_zero_work/phase33/PHASE33_REPAIR_DISPOSITION.md",
    "ground_zero_work/phase33/PHASE33_STATUS.md",
    "ground_zero_work/phase33/Phase33Axioms.lean",
    "ground_zero_work/phase33/PHASE33_AXIOM_AUDIT.txt",
    "ground_zero_work/phase33/phase33_source_checks.py",
    "ground_zero_work/phase33/verify_mss_guard_regression.py",
    "ground_zero_work/phase33/verify_phase33.sh",
    "ground_zero_work/phase33/verify_phase33_axioms.py",
    "ground_zero_work/phase33/verify_source_tree_binding.py",
    "ground_zero_work/phase33/build_phase33_release.py",
    "ground_zero_work/phase33/verify_phase33_release.py",
)
P30.ASSURANCE_FILES = P30.ASSURANCE_FILES + PHASE33_FILES
P30.SUPPORT_PREFIXES = P30.SUPPORT_PREFIXES + ("ground_zero_work/phase33/",)
# Phase-33 re-review advisory R1: ship the current Phase-33 trust boundary
# instead of the stale Phase-30 text.
P30.DISCLOSURE_FILES = tuple(
    "ground_zero_work/phase33/TRUST_BOUNDARY.md"
    if source.endswith("/TRUST_BOUNDARY.md")
    else source
    for source in P30.DISCLOSURE_FILES
)
# Phase-33 re-review advisory R2: package the magazine-article source so the
# attribution gate is fully replayable from the extracted packet.
GHOST_POST_SOURCE = "ground_zero_work/phase31/blog/JENSEN_TWO_THIRDS_GHOST_POST.md"



def metadata(candidate: str, package_class: str, title: str) -> bytes:
    payload = {
        "artifact": title,
        "candidate_commit": candidate,
        "date": "2026-08-25",
        "formal_endpoint": (
            "Phase-33 guarded MSS specialization, exact degree and root count, "
            "single global cutoff theorem, and concrete xi headline"
        ),
        "package_class": package_class,
        "phase33_source_repair_commit": REPAIR_COMMIT,
        "required_checkpoint": CHECKPOINT,
        "review_status": (
            "fresh Phase-32 AI-only review repaired; fresh Phase-33 AI-only "
            "re-review returned no release-blocking finding, and its two P3 "
            "advisories are repaired in this packet; no human or peer review"
        ),
        "source_date_epoch": int(SOURCE_DATE_EPOCH),
        "typed_external_inputs": ["Jacobi", "MMP", "MSS"],
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


BASE.metadata = metadata


def candidate_blob_index(candidate: str) -> dict[str, list[dict[str, str]]]:
    raw = subprocess.run(
        ["git", "ls-tree", "-r", "-z", candidate],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout
    rows: list[tuple[str, str, str]] = []
    for item in raw.split(b"\0"):
        if not item:
            continue
        header, path_bytes = item.split(b"\t", 1)
        mode, kind, oid = header.decode("ascii").split()
        if kind == "blob":
            rows.append((path_bytes.decode("utf-8"), oid, mode))
    index: dict[str, list[dict[str, str]]] = defaultdict(list)
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    try:
        for source_path, oid, mode in rows:
            process.stdin.write((oid + "\n").encode("ascii"))
            process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split()
            if len(header) != 3 or header[1] != "blob":
                raise RuntimeError(f"cannot read candidate blob: {source_path}")
            size = int(header[2])
            payload = process.stdout.read(size)
            if process.stdout.read(1) != b"\n":
                raise RuntimeError(f"malformed cat-file response: {source_path}")
            digest = hashlib.sha256(payload).hexdigest()
            index[digest].append(
                {"source_path": source_path, "git_blob_oid": oid, "git_mode": mode}
            )
    finally:
        process.stdin.close()
        process.wait()
    if process.returncode:
        raise RuntimeError("git cat-file failed")
    return index


def add_source_binding(candidate: str, entries: dict[str, bytes]) -> None:
    entries.pop("SOURCE_TREE_BINDING.json", None)
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase33/verify_source_tree_binding.py",
        "VERIFY_SOURCE_BINDING.py",
    )
    index = candidate_blob_index(candidate)
    rows = []
    for packet_path, payload in sorted(entries.items()):
        digest = hashlib.sha256(payload).hexdigest()
        rows.append(
            {
                "candidate_matches": index.get(digest, []),
                "packet_path": packet_path,
                "sha256": digest,
            }
        )
    candidate_tree = subprocess.run(
        ["git", "show", "-s", "--format=%T", candidate],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.decode("ascii").strip()
    binding = {
        "candidate_commit": candidate,
        "candidate_tree": candidate_tree,
        "coverage": (
            "All packet files except MANIFEST.sha256 and this self-referential binding; "
            "candidate_matches list every byte-identical blob in the candidate tree."
        ),
        "packet_entries": rows,
        "version": 1,
    }
    entries["SOURCE_TREE_BINDING.json"] = (
        json.dumps(binding, indent=2, sort_keys=True) + "\n"
    ).encode()


def add_phase33_navigation(candidate: str, entries: dict[str, bytes]) -> None:
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase33/Phase33Axioms.lean",
        "FORMAL/Phase33Axioms.lean",
    )
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase33/PHASE33_AXIOM_AUDIT.txt",
        "FORMAL/PHASE33_AXIOM_AUDIT.txt",
    )
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase33/PHASE32_FRESH_AI_REVIEW_FINDINGS.md",
        "REVIEW/PHASE32_FRESH_AI_REVIEW_FINDINGS.md",
    )
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase33/PHASE33_REPAIR_DISPOSITION.md",
        "REVIEW/PHASE33_REPAIR_DISPOSITION.md",
    )
    BASE.add_snapshot(
        entries,
        candidate,
        GHOST_POST_SOURCE,
        "PUBLIC/JENSEN_TWO_THIRDS_GHOST_POST.md",
    )
    entries["START_HERE.md"] = BASE.candidate_bytes(
        candidate, "ground_zero_work/phase33/package_materials/START_HERE.md"
    )
    entries["REPRODUCE/EXPECTED_RESULTS.md"] = BASE.candidate_bytes(
        candidate, "ground_zero_work/phase33/package_materials/EXPECTED_RESULTS.md"
    )


def referee_entries(candidate: str, tracked: set[str]) -> dict[str, bytes]:
    entries = P32.referee_entries(candidate, tracked)
    add_phase33_navigation(candidate, entries)
    entries["RELEASE_METADATA.json"] = metadata(
        candidate, "P33-R", "Jensen Two-Thirds Phase 33 Referee Packet"
    )
    add_source_binding(candidate, entries)
    return entries


def audit_entries(candidate: str, tracked: set[str], bundle: bytes) -> dict[str, bytes]:
    entries = referee_entries(candidate, tracked)
    prefixes = (
        "ground_zero_work/",
        f"{P30.LEAN_ROOT}/",
        "paper/",
        "reproduce/",
        ".github/workflows/",
    )
    for source in sorted(tracked):
        if source == "requirements-c48.lock" or any(
            source.startswith(prefix) for prefix in prefixes
        ):
            BASE.add_snapshot(entries, candidate, source, f"AUDIT/repository/{source}")
    for source in P30.PDF_FILES:
        BASE.add_snapshot(entries, candidate, source, f"AUDIT/repository/{source}")
    entries["AUDIT/CANDIDATE_HISTORY.bundle"] = bundle
    entries["AUDIT/SNAPSHOT_SCOPE.md"] = (
        "# Audit snapshot scope\n\nThe archive contains every tracked proof, review, "
        "paper, verifier, workflow, lockfile, frozen manuscript, and a complete "
        "offline Git history bundle for the candidate. Build caches, virtual "
        "environments, `.git`, and untracked workstation files are excluded.\n"
    ).encode()
    entries["RELEASE_METADATA.json"] = metadata(
        candidate, "P33-A", "Jensen Two-Thirds Phase 33 Full Audit Archive"
    )
    add_source_binding(candidate, entries)
    return entries


def ensure_clean() -> None:
    if subprocess.run(["git", "diff", "--quiet"], cwd=ROOT).returncode:
        raise SystemExit("FAIL package builder requires a clean tracked working tree")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode:
        raise SystemExit("FAIL package builder requires an empty index")


def main() -> None:
    ensure_clean()
    candidate = BASE.candidate_commit()
    for ancestor, label in ((CHECKPOINT, "required checkpoint"), (REPAIR_COMMIT, "repair commit")):
        if subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, candidate], cwd=ROOT
        ).returncode:
            raise SystemExit(f"FAIL {label} is absent from candidate history")
    tracked = BASE.tracked_files(candidate)
    required = list(
        P30.PAPER_FILES
        + P30.PDF_FILES
        + P30.DISCLOSURE_FILES
        + P30.ASSURANCE_FILES
        + P30.REVIEW_FILES
        + PHASE33_FILES
    )
    required.extend(
        [
            "ground_zero_work/phase33/package_materials/START_HERE.md",
            "ground_zero_work/phase33/package_materials/EXPECTED_RESULTS.md",
            "ground_zero_work/phase33/TRUST_BOUNDARY.md",
            GHOST_POST_SOURCE,
            "requirements-c48.lock",
        ]
    )
    BASE.ensure_files(tracked, required)
    bundle = BASE.history_bundle(candidate)
    if bundle != BASE.history_bundle(candidate):
        raise ValueError("candidate history bundle is not byte deterministic")

    checksums: list[str] = []
    referee_name = "Jensen_Two_Thirds_Phase33_Referee_Packet.zip"
    _, referee_digest = BASE.deterministic_package(
        referee_name, referee_entries(candidate, tracked), run_quick=False
    )
    checksums.append(f"{referee_digest}  {referee_name}")

    audit_name = "Jensen_Two_Thirds_Phase33_Full_Audit_Archive.zip"
    audit_path, audit_digest = BASE.deterministic_package(
        audit_name, audit_entries(candidate, tracked, bundle), run_quick=True
    )
    checksums.extend(BASE.split_full_audit_archive(audit_path, audit_digest))
    (OUTPUT / "SHA256SUMS.txt").write_text("\n".join(sorted(checksums)) + "\n")
    (OUTPUT / "PACKAGE_INDEX.md").write_text(
        "# Jensen two-thirds Phase 33 reviewer release\n\n"
        f"Candidate: `{candidate}`  \nRequired checkpoint: `{CHECKPOINT}`  \n"
        f"Phase 33 source repair: `{REPAIR_COMMIT}`\n\n"
        "- `Jensen_Two_Thirds_Phase33_Referee_Packet.zip` is the navigable paper, "
        "Lean, Mathematica, exact/numerical calculation, source, and AI-review packet.\n"
        "- `Jensen_Two_Thirds_Phase33_Full_Audit_Archive.zip.part*` reassembles to "
        "the full relevant repository and offline history archive. Run "
        "`python3 REASSEMBLE_FULL_AUDIT.py` to recover it.\n\n"
        f"Referee packet SHA-256: `{referee_digest}`.  Reassembled audit SHA-256: "
        f"`{audit_digest}`. The packages passed deterministic double-build, manifest, "
        "ancestry, source-tree binding, extraction-local three-PDF replay, and full-audit "
        "quick replay. The included review is AI-only; no human or peer review is claimed.\n"
    )
    print(f"PASS Phase-33 release packages for {candidate}")


if __name__ == "__main__":
    main()

