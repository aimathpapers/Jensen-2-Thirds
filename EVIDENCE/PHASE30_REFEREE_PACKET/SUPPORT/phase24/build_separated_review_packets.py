#!/usr/bin/env python3
"""Build deterministic, separated Phase-24 AI pre-review packets."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "output" / "reviewer_packets_phase24"
CANDIDATE_COMMIT = "d71b3d683e67296fd15e41d013a444df5fe2ec5f"
REQUIRED_CHECKPOINT = "5f79158f9c6276dd09142edeea279e35b0d58406"
FIXED_TIMESTAMP = (2026, 8, 17, 12, 0, 0)
LEAN_ROOT = "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"


COMMON_FILES = [
    "ground_zero_work/ASSUMPTION_REGISTRY.md",
    "ground_zero_work/CLAIM_LEDGER.md",
    "ground_zero_work/phase9/C48_SIGNED_FIFTH_SADDLE.md",
    "ground_zero_work/phase9/verify_phase9.sh",
    "ground_zero_work/phase11/C48_SIXTH_RESIDUAL.md",
    "ground_zero_work/phase11/verify_phase11.sh",
    "ground_zero_work/phase14/C48_ELEMENTARY_C1_PROOF.md",
    "ground_zero_work/phase14/Phase14Axioms.lean",
    "ground_zero_work/phase14/verify_phase14.sh",
    "ground_zero_work/phase15/C48_FULL_C1_BRANCH.md",
    "ground_zero_work/phase15/Phase15Axioms.lean",
    "ground_zero_work/phase15/verify_phase15.sh",
    "ground_zero_work/phase16/C48_UNIFORM_RADIUS_PROOF.md",
    "ground_zero_work/phase16/Phase16Axioms.lean",
    "ground_zero_work/phase16/verify_phase16.sh",
    "ground_zero_work/phase17/C48_SIXTH_STABILITY_AND_ASSEMBLY.md",
    "ground_zero_work/phase17/Phase17Axioms.lean",
    "ground_zero_work/phase17/verify_phase17.sh",
    "ground_zero_work/phase18/C48_COMPLEX_SIXTH_SADDLE.md",
    "ground_zero_work/phase18/C48_EFFECTIVITY_AND_MARGIN.md",
    "ground_zero_work/phase18/C48_HOLLAND_DEPENDENCY_AUDIT.md",
    "ground_zero_work/phase18/C48_SECTORIAL_SADDLE_VARIABLE.md",
    "ground_zero_work/phase18/Phase18Axioms.lean",
    "ground_zero_work/phase18/verify_phase18.sh",
    "ground_zero_work/phase20/GORTTW_PRIMARY_INPUT.md",
    "ground_zero_work/phase20/HOLLAND_DEPENDENCY_FIREWALL.md",
    "ground_zero_work/phase20/HOLLAND_MULTIPLIER_REPROOF.md",
    "ground_zero_work/phase20/HOLLAND_PROP41_REPROOF.md",
    "ground_zero_work/phase20/Phase20Axioms.lean",
    "ground_zero_work/phase20/verify_phase20.sh",
    "ground_zero_work/phase21/C48_DOWNSTREAM_DISCHARGE.md",
    "ground_zero_work/phase21/C48_GORTTW_SECTOR_EXECUTION_PLAN.md",
    "ground_zero_work/phase21/C48_GORTTW_SECTOR_MILESTONE1.md",
    "ground_zero_work/phase21/C48_HIGHER_THETA_MODES.md",
    "ground_zero_work/phase21/C48_LEADING_CONTOUR_LOCALIZATION.md",
    "ground_zero_work/phase21/C48_XI_COEFFICIENT_ASSEMBLY.md",
    "ground_zero_work/phase21/GORTTW_MELLIN_SOURCE_RECONSTRUCTION.md",
    "ground_zero_work/phase21/SECTORIAL_CONTOUR_PRIMARY_RESEARCH.md",
    "ground_zero_work/phase21/check_phase21_notes.py",
    "ground_zero_work/phase21/verify_phase21.sh",
    "ground_zero_work/phase21/verify_phase21_leading_contour.sh",
    "ground_zero_work/phase21/verify_phase21_milestone1.sh",
    "ground_zero_work/phase24/DEPENDENCY_MATRIX.md",
    "ground_zero_work/phase24/FORMALIZATION_LEDGER.md",
    "ground_zero_work/phase24/INTERVAL_CERTIFICATES.json",
    "ground_zero_work/phase24/KNOWN_LIMITATIONS.md",
    "ground_zero_work/phase24/MATHEMATICA_FOLLOWUP.md",
    "ground_zero_work/phase24/mathematica_verification/C48_Mathematica_CleanRoom.pdf",
    "ground_zero_work/phase24/mathematica_verification/C48_Mathematica_CleanRoom_2.nb",
    "ground_zero_work/phase24/mathematica_verification/C48_Mathematica_Result_Ledger.txt",
    "ground_zero_work/phase24/mathematica_verification/SHA256SUMS.txt",
    "ground_zero_work/phase24/mathematica_verification/VERIFICATION_RECORD.md",
    "ground_zero_work/phase24/PAPER_THEOREM_INVENTORY.md",
    "ground_zero_work/phase24/PRIMARY_SOURCE_AUDIT.md",
    "ground_zero_work/phase24/REVIEW_SEPARATION.md",
    "ground_zero_work/phase24/SOURCE_HASHES.sha256",
    "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex",
    "ground_zero_work/phase24/manuscript_equation_regression.py",
    "ground_zero_work/phase24/mutation_tests.py",
    "ground_zero_work/phase24/release_checks.py",
    "ground_zero_work/phase24/verify_interval_certificates.py",
    "ground_zero_work/phase24/verify_mathematica_evidence.py",
    "ground_zero_work/phase24/verify_phase24.sh",
    "output/pdf/JENSEN_TWO_THIRDS_UNIFIED.pdf",
    f"{LEAN_ROOT}/README.md",
    f"{LEAN_ROOT}/lake-manifest.json",
    f"{LEAN_ROOT}/lakefile.toml",
    f"{LEAN_ROOT}/lean-toolchain",
    f"{LEAN_ROOT}/Zeta23/Research/JensenWedge.lean",
]


ROLES = {
    "Analytic": {
        "packet": "ground_zero_work/phase24/ANALYTIC_REVIEW_PACKET_PHASE24.md",
        "archive": "Jensen_Two_Thirds_Phase24_Analytic_AI_Review_Packet.zip",
    },
    "Algebraic": {
        "packet": "ground_zero_work/phase24/ALGEBRAIC_REVIEW_PACKET_PHASE24.md",
        "archive": "Jensen_Two_Thirds_Phase24_Algebraic_AI_Review_Packet.zip",
    },
}


BANNED_PATH_PATTERNS = (
    re.compile(r"(^|/)reviews?/", re.IGNORECASE),
    re.compile(r"review.*report", re.IGNORECASE),
    re.compile(r"review.*response", re.IGNORECASE),
    re.compile(r"review.*disposition", re.IGNORECASE),
    re.compile(r"review.*intake", re.IGNORECASE),
    re.compile(r"review.*repair", re.IGNORECASE),
)


VERIFY_BUNDLE = r'''#!/usr/bin/env python3
"""Verify all immutable files in an extracted Phase-24 review packet."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ROW = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<path>.+)$")
rows = []
for line in (ROOT / "EVIDENCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    match = ROW.fullmatch(line)
    if match is None:
        raise SystemExit(f"FAIL malformed manifest row: {line!r}")
    rows.append((match.group("path"), match.group("digest")))
if not rows:
    raise SystemExit("FAIL empty evidence manifest")
for relative, expected in rows:
    source = ROOT / relative
    if not source.is_file():
        raise SystemExit(f"FAIL missing {relative}")
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"FAIL hash mismatch {relative}")
print(f"PASS Phase-24 reviewer bundle manifest ({len(rows)} files)")
'''.encode("utf-8")


def git_output(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def candidate_bytes(relative: str) -> bytes:
    return git_output("show", f"{CANDIDATE_COMMIT}:{relative}")


def tracked_candidate_files() -> set[str]:
    output = git_output("ls-tree", "-r", "--name-only", CANDIDATE_COMMIT)
    return set(output.decode("utf-8").splitlines())


def dynamic_files(tracked: set[str]) -> list[str]:
    paths = []
    for relative in tracked:
        if "__pycache__" in relative or relative.endswith(".pyc"):
            continue
        if relative.startswith("ground_zero_work/c48_jensen/"):
            paths.append(relative)
        elif relative.startswith(f"{LEAN_ROOT}/Zeta23/Research/JensenWedge/"):
            paths.append(relative)
    return sorted(paths)


def start_here(role: str) -> bytes:
    return f"""# Phase 24 {role.lower()} adversarial AI pre-review

Candidate proof-source commit: `{CANDIDATE_COMMIT}`
Required historical checkpoint: `{REQUIRED_CHECKPOINT}`
Review classification: separated AI pre-review, not human or peer review
Embargo: confidential working mathematics; do not publish

Start with `REVIEW_PACKET.md` and `manuscript/JENSEN_TWO_THIRDS_UNIFIED.pdf`.
The `evidence/` tree contains proof notes, exact/numerical verifier sources,
Lean sources, environment locks, source hashes, formalization disclosures,
and the frozen user-executed Mathematica M1--M4 evidence.

This follow-up packet intentionally omits every prior review report, author
response, finding disposition, recalculation output, and the other review
track's instructions. Reconstruct the mandatory high-risk calculations from
the definitions and primary sources before comparing with repository-produced
symbolic artifacts. Identify the reviewer as an AI system and disclose the
model/provider, tools, access to prior work, conflicts, and independence.
The reviewer must also disclose whether the same model or session reviewed an
earlier freeze. If so, classify that work as a correlated re-review; it cannot
count as an additional separated pass.

Run `python3 VERIFY_BUNDLE.py` from this directory to verify all bundled
files. To rerun repository verifiers, place the evidence paths at a repository
root or independently clone the candidate commit; Lean and Python runtimes are
not embedded in this archive.
""".encode("utf-8")


def metadata(role: str) -> bytes:
    payload = {
        "artifact": f"Jensen Two-Thirds Phase 24 {role} AI Review Packet",
        "candidate_commit": CANDIDATE_COMMIT,
        "confidential": True,
        "date": "2026-08-17",
        "prior_reports_included": False,
        "review_class": "AI pre-review; not human or peer review",
        "review_track": role,
        "required_checkpoint": REQUIRED_CHECKPOINT,
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def archive_path(relative: str) -> str:
    if relative == "output/pdf/JENSEN_TWO_THIRDS_UNIFIED.pdf":
        return "manuscript/JENSEN_TWO_THIRDS_UNIFIED.pdf"
    if relative == "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex":
        return "manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex"
    return f"evidence/{relative}"


def add_bytes(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=FIXED_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def manifest(entries: dict[str, bytes]) -> bytes:
    return "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n"
        for name, data in sorted(entries.items())
    ).encode("utf-8")


def check_separation(role: str, entries: dict[str, bytes]) -> None:
    for name in entries:
        if any(pattern.search(name) for pattern in BANNED_PATH_PATTERNS):
            raise ValueError(f"banned review-history path in {role} packet: {name}")
    packet = entries.get("REVIEW_PACKET.md", b"").decode("utf-8")
    if f"Phase 24 {role.lower()} adversarial-review packet" not in packet:
        raise ValueError(f"wrong or missing {role} review packet")
    other = "algebraic" if role == "Analytic" else "analytic"
    if f"Phase 24 {other} adversarial-review packet" in packet:
        raise ValueError(f"other track packet leaked into {role} packet")
    for marker in (
        "ALGEBRAIC_REVIEW_REPORT_R3",
        "ANALYTIC_REVIEW_REPORT_PHASE21",
        "Verdict: R0",
        "Review complete. Deliverables",
    ):
        for name, data in entries.items():
            if name.endswith((".md", ".txt")) and marker.encode("utf-8") in data:
                raise ValueError(f"prior-review marker {marker!r} leaked through {name}")


def build(role: str, spec: dict[str, str], tracked: set[str]) -> Path:
    selected = sorted(set(COMMON_FILES + dynamic_files(tracked)))
    missing = [relative for relative in selected + [spec["packet"]] if relative not in tracked]
    if missing:
        raise FileNotFoundError("candidate commit lacks:\n" + "\n".join(missing))

    entries = {archive_path(relative): candidate_bytes(relative) for relative in selected}
    entries["REVIEW_PACKET.md"] = candidate_bytes(spec["packet"])
    entries["START_HERE.md"] = start_here(role)
    entries["BUNDLE_METADATA.json"] = metadata(role)
    entries["CANDIDATE_COMMIT.txt"] = (CANDIDATE_COMMIT + "\n").encode("ascii")
    entries["VERIFY_BUNDLE.py"] = VERIFY_BUNDLE
    check_separation(role, entries)
    entries["EVIDENCE_MANIFEST.sha256"] = manifest(entries)

    root_name = Path(spec["archive"]).stem
    output = OUTPUT_DIR / spec["archive"]
    with zipfile.ZipFile(output, "w") as archive:
        for name, data in sorted(entries.items()):
            add_bytes(archive, f"{root_name}/{name}", data)
    return output


def verify_archive(path: Path, role: str) -> None:
    root_name = path.stem
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if names != sorted(names) or len(names) != len(set(names)):
            raise ValueError(f"noncanonical archive member order in {path.name}")
        if any(info.date_time != FIXED_TIMESTAMP for info in archive.infolist()):
            raise ValueError(f"noncanonical timestamp in {path.name}")
        prefix = f"{root_name}/"
        stripped = {name.removeprefix(prefix): archive.read(name) for name in names}
        if any(name == full for name, full in zip(stripped, names)):
            raise ValueError(f"archive root missing in {path.name}")
        evidence = stripped.pop("EVIDENCE_MANIFEST.sha256")
        if evidence != manifest(stripped):
            raise ValueError(f"manifest mismatch in {path.name}")
        check_separation(role, stripped)


def check_candidate_history() -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", REQUIRED_CHECKPOINT, CANDIDATE_COMMIT],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise ValueError("required historical checkpoint is not in candidate history")


def main() -> None:
    check_candidate_history()
    tracked = tracked_candidate_files()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    checksum_rows = []
    for role, spec in ROLES.items():
        output = build(role, spec, tracked)
        verify_archive(output, role)
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
        checksum_rows.append(f"{digest}  {output.name}")
        print(f"PASS {role.lower()} separation: {output.relative_to(ROOT)}")
    checksum_path = OUTPUT_DIR / "SHA256SUMS.txt"
    checksum_path.write_text("\n".join(sorted(checksum_rows)) + "\n", encoding="utf-8")
    print(f"PASS external checksums: {checksum_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
