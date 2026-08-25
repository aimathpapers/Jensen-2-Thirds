#!/usr/bin/env python3
"""Build deterministic Phase-32 referee and full-audit release packages."""

from __future__ import annotations

import importlib.util
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE30_PATH = ROOT / "ground_zero_work/phase30/build_phase30_release.py"
OUTPUT = ROOT / "output/reviewer_packages_phase32"
CHECKPOINT = "5f79158f9c6276dd09142edeea279e35b0d58406"
SOURCE_DATE_EPOCH = "1787572800"
FIXED_TIMESTAMP = (2026, 8, 24, 12, 0, 0)


def load_phase30():
    spec = importlib.util.spec_from_file_location("phase30_builder", PHASE30_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Phase-30 package builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P30 = load_phase30()
BASE = P30.BASE
BASE.OUTPUT = OUTPUT
BASE.SOURCE_DATE_EPOCH = SOURCE_DATE_EPOCH
BASE.FIXED_TIMESTAMP = FIXED_TIMESTAMP
BASE.BUILD_PACKET_MANUSCRIPTS = BASE.BUILD_PACKET_MANUSCRIPTS.replace(
    b'export SOURCE_DATE_EPOCH="1787313600"',
    f'export SOURCE_DATE_EPOCH="{SOURCE_DATE_EPOCH}"'.encode(),
)

PHASE32_FILES = (
    "ground_zero_work/phase32/MMP_SPECIALIZATION_SOURCE_AUDIT.md",
    "ground_zero_work/phase32/PHASE32_STATUS.md",
    "ground_zero_work/phase32/Phase32Axioms.lean",
    "ground_zero_work/phase32/PHASE32_AXIOM_AUDIT.txt",
    "ground_zero_work/phase32/phase32_mmp_checks.py",
    "ground_zero_work/phase32/verify_phase32_axioms.py",
    "ground_zero_work/phase32/verify_phase32.sh",
)
P30.ASSURANCE_FILES = P30.ASSURANCE_FILES + PHASE32_FILES
P30.SUPPORT_PREFIXES = P30.SUPPORT_PREFIXES + ("ground_zero_work/phase32/",)


def metadata(candidate: str, package_class: str, title: str) -> bytes:
    payload = {
        "artifact": title,
        "candidate_commit": candidate,
        "date": "2026-08-24",
        "formal_endpoint": (
            "Phase-32 concrete Jacobi-factor MMP specialization, xi comparison "
            "transport, finite-cutoff absorption, and Phase-30 headline theorem"
        ),
        "package_class": package_class,
        "required_checkpoint": CHECKPOINT,
        "review_status": "AI-only review record; no human or peer review",
        "source_date_epoch": int(SOURCE_DATE_EPOCH),
        "typed_external_inputs": ["Jacobi", "MMP", "MSS"],
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


BASE.metadata = metadata


def add_common(candidate: str, tracked: set[str], entries: dict[str, bytes]) -> None:
    P30.add_common(candidate, tracked, entries)
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase32/Phase32Axioms.lean",
        "FORMAL/Phase32Axioms.lean",
    )
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase32/PHASE32_AXIOM_AUDIT.txt",
        "FORMAL/PHASE32_AXIOM_AUDIT.txt",
    )
    # Phase 30 installs historical navigation files at these destinations.
    # Replace those two byte payloads explicitly for the current packet.
    entries["START_HERE.md"] = BASE.candidate_bytes(
        candidate, "ground_zero_work/phase32/package_materials/START_HERE.md"
    )
    entries["REPRODUCE/EXPECTED_RESULTS.md"] = BASE.candidate_bytes(
        candidate, "ground_zero_work/phase32/package_materials/EXPECTED_RESULTS.md"
    )


def referee_entries(candidate: str, tracked: set[str]) -> dict[str, bytes]:
    entries: dict[str, bytes] = {}
    add_common(candidate, tracked, entries)
    BASE.common_generated(
        entries, candidate, "P32-R", "Jensen Two-Thirds Phase 32 Referee Packet"
    )
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
        candidate, "P32-A", "Jensen Two-Thirds Phase 32 Full Audit Archive"
    )
    return entries


def ensure_clean() -> None:
    if subprocess.run(["git", "diff", "--quiet"], cwd=ROOT).returncode:
        raise SystemExit("FAIL package builder requires a clean tracked working tree")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode:
        raise SystemExit("FAIL package builder requires an empty index")


def main() -> None:
    ensure_clean()
    candidate = BASE.candidate_commit()
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", CHECKPOINT, candidate], cwd=ROOT
    ).returncode:
        raise SystemExit("FAIL required checkpoint is absent from candidate history")
    tracked = BASE.tracked_files(candidate)
    required = list(
        P30.PAPER_FILES
        + P30.PDF_FILES
        + P30.DISCLOSURE_FILES
        + P30.ASSURANCE_FILES
        + P30.REVIEW_FILES
        + PHASE32_FILES
    )
    required.extend(
        [
            "ground_zero_work/phase32/package_materials/START_HERE.md",
            "ground_zero_work/phase32/package_materials/EXPECTED_RESULTS.md",
            "requirements-c48.lock",
        ]
    )
    BASE.ensure_files(tracked, required)
    bundle = BASE.history_bundle(candidate)
    if bundle != BASE.history_bundle(candidate):
        raise ValueError("candidate history bundle is not byte deterministic")

    checksums: list[str] = []
    referee_name = "Jensen_Two_Thirds_Phase32_Referee_Packet.zip"
    _, referee_digest = BASE.deterministic_package(
        referee_name, referee_entries(candidate, tracked), run_quick=False
    )
    checksums.append(f"{referee_digest}  {referee_name}")

    audit_name = "Jensen_Two_Thirds_Phase32_Full_Audit_Archive.zip"
    audit_path, audit_digest = BASE.deterministic_package(
        audit_name, audit_entries(candidate, tracked, bundle), run_quick=True
    )
    checksums.extend(BASE.split_full_audit_archive(audit_path, audit_digest))
    (OUTPUT / "SHA256SUMS.txt").write_text("\n".join(sorted(checksums)) + "\n")
    (OUTPUT / "PACKAGE_INDEX.md").write_text(
        "# Jensen two-thirds Phase 32 reviewer release\n\n"
        f"Candidate: `{candidate}`  \nRequired checkpoint: `{CHECKPOINT}`\n\n"
        "- `Jensen_Two_Thirds_Phase32_Referee_Packet.zip` is the navigable paper, "
        "Lean, Mathematica, exact/numerical calculation, source, and AI-review packet.\n"
        "- `Jensen_Two_Thirds_Phase32_Full_Audit_Archive.zip.part*` reassembles to "
        "the full relevant repository and offline history archive. Run "
        "`python3 REASSEMBLE_FULL_AUDIT.py` to recover it.\n\n"
        f"Reassembled audit SHA-256: `{audit_digest}`. The packages passed deterministic "
        "double-build, fail-closed manifest/ancestry attacks, extraction-local "
        "manuscript replay, and full-audit quick replay. All included reviews are "
        "AI-only; no human or peer review is claimed.\n"
    )
    print(f"PASS Phase-32 release packages for {candidate}")


if __name__ == "__main__":
    main()
