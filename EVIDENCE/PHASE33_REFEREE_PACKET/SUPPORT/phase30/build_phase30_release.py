#!/usr/bin/env python3
"""Build deterministic Phase-30 referee and full-audit release packages."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE27_PATH = ROOT / "ground_zero_work/phase27/build_phase27_release.py"
OUTPUT = ROOT / "output/reviewer_packages_phase30"
CHECKPOINT = "5f79158f9c6276dd09142edeea279e35b0d58406"
SOURCE_DATE_EPOCH = "1787313600"
FIXED_TIMESTAMP = (2026, 8, 21, 12, 0, 0)


def load_phase27():
    spec = importlib.util.spec_from_file_location("phase27_builder", PHASE27_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Phase-27 package builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


P27 = load_phase27()
BASE = P27.BASE
BASE.OUTPUT = OUTPUT
BASE.SOURCE_DATE_EPOCH = SOURCE_DATE_EPOCH
BASE.FIXED_TIMESTAMP = FIXED_TIMESTAMP
BASE.BUILD_PACKET_MANUSCRIPTS = BASE.BUILD_PACKET_MANUSCRIPTS.replace(
    b'export SOURCE_DATE_EPOCH="1786968000"',
    f'export SOURCE_DATE_EPOCH="{SOURCE_DATE_EPOCH}"'.encode(),
)

LEAN_ROOT = BASE.LEAN_ROOT
MATHEMATICA_PREFIX = BASE.MATHEMATICA_PREFIX
SYMPY_PREFIX = BASE.SYMPY_PREFIX
PAPER_FILES = BASE.PAPER_FILES + (
    "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex",
)
PDF_FILES = BASE.PDF_FILES + ("output/pdf/JENSEN_TWO_THIRDS_UNIFIED.pdf",)
PRIMARY_SOURCE_FILES = BASE.PRIMARY_SOURCE_FILES
DISCLOSURE_FILES = (
    "ground_zero_work/phase30/TRUST_BOUNDARY.md",
    "ground_zero_work/phase30/package_materials/KNOWN_LIMITATIONS.md",
    "ground_zero_work/phase30/package_materials/AI_ASSISTANCE.md",
    "ground_zero_work/phase30/package_materials/SOURCE_INDEX.md",
)
ASSURANCE_FILES = (
    "ground_zero_work/phase27/THEOREM_ASSURANCE_MATRIX.json",
    "ground_zero_work/phase27/THEOREM_ASSURANCE_MATRIX.md",
    "ground_zero_work/phase30/PHASE30_PLAN.md",
    "ground_zero_work/phase30/PHASE30_STATUS.md",
    "ground_zero_work/phase30/Phase30Axioms.lean",
    "ground_zero_work/phase30/PHASE30_AXIOM_AUDIT.txt",
    "ground_zero_work/phase30/verify_phase30_axioms.py",
    "ground_zero_work/phase30/phase30_semantic_mutations.py",
    "ground_zero_work/phase30/phase30_adversarial_checks.py",
    "ground_zero_work/phase30/verify_phase30.sh",
    "ground_zero_work/phase28/PHASE28_STATUS.md",
    "ground_zero_work/phase29/PHASE29_STATUS.md",
    "ground_zero_work/phase29/PHASE29_RELEASE.md",
    "ground_zero_work/phase29/PUBLIC_CANDIDATE_AUDIT.md",
)
REVIEW_FILES = (
    "ground_zero_work/phase30/PHASE30_AI_ONLY_ADVERSARIAL_REVIEW.md",
    "ground_zero_work/phase29/PHASE29_AI_ONLY_RELEASE_AUDIT.md",
    "ground_zero_work/phase27/FRESH_AI_REVIEW.md",
    "ground_zero_work/phase27/FRESH_AI_REREVIEW.md",
    "ground_zero_work/phase27/AUTHOR_DISPOSITION.md",
)
SUPPORT_PREFIXES = (
    "ground_zero_work/phase9/",
    "ground_zero_work/phase11/",
    "ground_zero_work/phase14/",
    "ground_zero_work/phase15/",
    "ground_zero_work/phase16/",
    "ground_zero_work/phase17/",
    "ground_zero_work/phase18/",
    "ground_zero_work/phase20/",
    "ground_zero_work/phase21/",
    "ground_zero_work/phase24/",
    "ground_zero_work/phase25/",
    "ground_zero_work/phase26/",
    "ground_zero_work/phase28/",
    "ground_zero_work/phase29/",
    "ground_zero_work/phase30/",
)


def metadata(candidate: str, package_class: str, title: str) -> bytes:
    payload = {
        "artifact": title,
        "candidate_commit": candidate,
        "date": "2026-08-21",
        "formal_endpoint": (
            "Phase-30 xi-specific multiplier, concrete interval certificate, "
            "actual transformed Jensen connection, and headline Lean theorem"
        ),
        "package_class": package_class,
        "required_checkpoint": CHECKPOINT,
        "review_status": "correlated AI-only review; no human or peer review",
        "source_date_epoch": int(SOURCE_DATE_EPOCH),
        "typed_external_inputs": ["Jacobi", "MMP", "MSS"],
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


BASE.metadata = metadata


def add_common(candidate: str, tracked: set[str], entries: dict[str, bytes]) -> None:
    for source in PAPER_FILES:
        BASE.add_snapshot(entries, candidate, source, f"PAPER/source/{Path(source).name}")
    for source in PDF_FILES:
        BASE.add_snapshot(entries, candidate, source, f"PAPER/{Path(source).name}")
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md",
        "PUBLIC/JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md",
    )
    BASE.add_prefix(entries, candidate, tracked, f"{LEAN_ROOT}/", "FORMAL/lean-project/")
    BASE.add_snapshot(
        entries,
        candidate,
        "paper/THEOREM_EVIDENCE_CROSS_REFERENCE.md",
        "FORMAL/THEOREM_MAP.md",
    )
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase30/Phase30Axioms.lean",
        "FORMAL/Phase30Axioms.lean",
    )
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase30/PHASE30_AXIOM_AUDIT.txt",
        "FORMAL/PHASE30_AXIOM_AUDIT.txt",
    )
    for source in ASSURANCE_FILES:
        BASE.add_snapshot(entries, candidate, source, f"FORMAL/evidence/{Path(source).name}")

    BASE.add_prefix(entries, candidate, tracked, MATHEMATICA_PREFIX, "COMPUTATION/mathematica/")
    BASE.add_prefix(entries, candidate, tracked, SYMPY_PREFIX, "COMPUTATION/sympy/")
    for source in (
        "ground_zero_work/phase25/ARB_ACB_METHOD.md",
        "ground_zero_work/phase25/ARB_ACB_RESULTS.json",
        "ground_zero_work/phase25/arb_acb_verification.py",
        "ground_zero_work/phase25/arb_acb_semantic_mutations.py",
    ):
        BASE.add_snapshot(entries, candidate, source, f"COMPUTATION/arb_acb/{Path(source).name}")
    for source in (
        "ground_zero_work/phase24/INTERVAL_CERTIFICATES.json",
        "ground_zero_work/phase24/verify_interval_certificates.py",
        "ground_zero_work/phase25/branch_interval_certificates.py",
        "ground_zero_work/phase25/branch_semantic_mutations.py",
    ):
        BASE.add_snapshot(
            entries, candidate, source, f"COMPUTATION/interval_certificates/{Path(source).name}"
        )
    for source in (
        "ground_zero_work/phase25/EFFECTIVITY_LEDGER.json",
        "ground_zero_work/phase25/EFFECTIVITY_LEDGER.md",
        "ground_zero_work/phase25/effectivity_ledger.py",
        "ground_zero_work/phase25/effectivity_semantic_mutations.py",
    ):
        BASE.add_snapshot(entries, candidate, source, f"COMPUTATION/effectivity/{Path(source).name}")

    for prefix in SUPPORT_PREFIXES:
        BASE.add_prefix(entries, candidate, tracked, prefix, f"SUPPORT/{prefix.rstrip('/').split('/')[-1]}/")
    for source in PRIMARY_SOURCE_FILES:
        BASE.add_snapshot(entries, candidate, source, f"SUPPORT/primary_sources/{Path(source).name}")
    for source in DISCLOSURE_FILES:
        BASE.add_snapshot(entries, candidate, source, f"DISCLOSURE/{Path(source).name}")
    for source in REVIEW_FILES:
        BASE.add_snapshot(entries, candidate, source, f"REVIEW/{Path(source).name}")
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase30/package_materials/START_HERE.md",
        "START_HERE.md",
    )
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase30/package_materials/EXPECTED_RESULTS.md",
        "REPRODUCE/EXPECTED_RESULTS.md",
    )
    BASE.add_snapshot(entries, candidate, "requirements-c48.lock", "REPRODUCE/requirements-c48.lock")
    BASE.add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase25/ENVIRONMENT_INVENTORY.json",
        "REPRODUCE/ENVIRONMENT_INVENTORY.json",
    )


def referee_entries(candidate: str, tracked: set[str]) -> dict[str, bytes]:
    entries: dict[str, bytes] = {}
    add_common(candidate, tracked, entries)
    BASE.common_generated(entries, candidate, "P30-R", "Jensen Two-Thirds Phase 30 Referee Packet")
    return entries


def audit_entries(candidate: str, tracked: set[str], bundle: bytes) -> dict[str, bytes]:
    entries = referee_entries(candidate, tracked)
    prefixes = (
        "ground_zero_work/",
        f"{LEAN_ROOT}/",
        "paper/",
        "reproduce/",
        ".github/workflows/",
    )
    for source in sorted(tracked):
        if source == "requirements-c48.lock" or any(source.startswith(prefix) for prefix in prefixes):
            BASE.add_snapshot(entries, candidate, source, f"AUDIT/repository/{source}")
    for source in PDF_FILES:
        BASE.add_snapshot(entries, candidate, source, f"AUDIT/repository/{source}")
    entries["AUDIT/CANDIDATE_HISTORY.bundle"] = bundle
    entries["AUDIT/SNAPSHOT_SCOPE.md"] = (
        "# Audit snapshot scope\n\nThe archive contains every tracked proof, review, "
        "paper, verifier, workflow, lockfile, frozen manuscript, and a complete "
        "offline Git history bundle for the candidate. Build caches, virtual "
        "environments, `.git`, and untracked workstation files are excluded.\n"
    ).encode()
    entries["RELEASE_METADATA.json"] = metadata(
        candidate, "P30-A", "Jensen Two-Thirds Phase 30 Full Audit Archive"
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
    required = list(PAPER_FILES + PDF_FILES + DISCLOSURE_FILES + ASSURANCE_FILES + REVIEW_FILES)
    required.extend(
        [
            "ground_zero_work/phase30/package_materials/START_HERE.md",
            "ground_zero_work/phase30/package_materials/EXPECTED_RESULTS.md",
            "requirements-c48.lock",
        ]
    )
    BASE.ensure_files(tracked, required)
    bundle = BASE.history_bundle(candidate)
    if bundle != BASE.history_bundle(candidate):
        raise ValueError("candidate history bundle is not byte deterministic")

    checksums: list[str] = []
    referee_name = "Jensen_Two_Thirds_Phase30_Referee_Packet.zip"
    _, referee_digest = BASE.deterministic_package(
        referee_name, referee_entries(candidate, tracked), run_quick=False
    )
    checksums.append(f"{referee_digest}  {referee_name}")

    audit_name = "Jensen_Two_Thirds_Phase30_Full_Audit_Archive.zip"
    audit_path, audit_digest = BASE.deterministic_package(
        audit_name, audit_entries(candidate, tracked, bundle), run_quick=True
    )
    checksums.extend(BASE.split_full_audit_archive(audit_path, audit_digest))
    (OUTPUT / "SHA256SUMS.txt").write_text("\n".join(sorted(checksums)) + "\n")
    (OUTPUT / "PACKAGE_INDEX.md").write_text(
        "# Jensen two-thirds Phase 30 reviewer release\n\n"
        f"Candidate: `{candidate}`  \nRequired checkpoint: `{CHECKPOINT}`\n\n"
        "- `Jensen_Two_Thirds_Phase30_Referee_Packet.zip` is the navigable paper, "
        "Lean, Mathematica, exact/numerical calculation, source, and AI-review packet.\n"
        "- `Jensen_Two_Thirds_Phase30_Full_Audit_Archive.zip.part*` reassembles to "
        "the full relevant repository and offline history archive. Run "
        "`python3 REASSEMBLE_FULL_AUDIT.py` to recover it.\n\n"
        f"Reassembled audit SHA-256: `{audit_digest}`. The packages passed deterministic "
        "double-build, fail-closed manifest/ancestry attacks, extraction-local "
        "manuscript replay, and full-audit quick replay. Review is correlated AI-only, "
        "not human or peer review.\n"
    )
    print(f"PASS Phase-30 release packages for {candidate}")


if __name__ == "__main__":
    main()
