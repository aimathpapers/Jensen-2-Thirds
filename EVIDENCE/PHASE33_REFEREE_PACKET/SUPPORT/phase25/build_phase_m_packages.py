#!/usr/bin/env python3
"""Build deterministic Phase-M referee, audit, and fresh-review packages."""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output" / "reviewer_packages_phase25"
CHECKPOINT = "5f79158f9c6276dd09142edeea279e35b0d58406"
FIXED_TIMESTAMP = (2026, 8, 18, 12, 0, 0)
SOURCE_DATE_EPOCH = "1786968000"
LEAN_ROOT = "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
MATERIALS = "ground_zero_work/phase25/package_materials"


PAPER_FILES = (
    "paper/JENSEN_TWO_THIRDS_MAIN.tex",
    "paper/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex",
    "paper/c48_common.tex",
    "paper/c48_detailed_appendices.tex",
    "paper/references.bib",
    "paper/README.md",
    "paper/THEOREM_EVIDENCE_CROSS_REFERENCE.md",
)
PDF_FILES = (
    "output/pdf/JENSEN_TWO_THIRDS_MAIN.pdf",
    "output/pdf/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf",
)
DISCLOSURE_FILES = (
    f"{MATERIALS}/TRUST_BOUNDARY.md",
    f"{MATERIALS}/KNOWN_LIMITATIONS.md",
    f"{MATERIALS}/AI_ASSISTANCE.md",
    f"{MATERIALS}/SOURCE_INDEX.md",
)
ASSURANCE_FILES = (
    "ground_zero_work/phase25/THEOREM_ASSURANCE_MATRIX.json",
    "ground_zero_work/phase25/THEOREM_ASSURANCE_MATRIX.md",
    "ground_zero_work/phase25/PROOF_DEPENDENCY_GRAPH.json",
    "ground_zero_work/phase25/PROOF_DEPENDENCY_GRAPH.md",
    "ground_zero_work/phase25/NOTATION_NORMALIZATION_CROSSWALK.md",
    "ground_zero_work/phase25/ASYMPTOTIC_LANGUAGE_LEDGER.json",
    "ground_zero_work/phase25/EFFECTIVITY_LEDGER.json",
    "ground_zero_work/phase25/EFFECTIVITY_LEDGER.md",
)
PHASE_N_VALIDATION_FILES = (
    "ground_zero_work/phase25/PHASE_N_FINAL_HANDOFF.md",
    "ground_zero_work/phase25/PHASE25_STATUS.md",
    "ground_zero_work/phase25/phase_n_logs/REPO_VERIFY_ALL_FULL.log",
    "ground_zero_work/phase25/phase_n_logs/PHASE24_SERIAL.log",
    "ground_zero_work/phase25/phase_n_logs/AUDIT_ARCHIVE_FULL_INITIAL_FAILURE.log",
    "ground_zero_work/phase25/phase_n_logs/AUDIT_ARCHIVE_FULL.log",
)
PRIMARY_SOURCE_FILES = (
    "ground_zero_work/phase24/PRIMARY_SOURCE_AUDIT.md",
    "ground_zero_work/phase24/SOURCE_HASHES.sha256",
    "ground_zero_work/phase20/GORTTW_PRIMARY_INPUT.md",
    "ground_zero_work/phase20/HOLLAND_DEPENDENCY_FIREWALL.md",
)
FORMAL_INDEX_FILES = (
    "ground_zero_work/phase25/Phase25Axioms.lean",
    "ground_zero_work/phase25/PHASE25_AXIOM_AUDIT.txt",
    "ground_zero_work/phase25/verify_phase25_axioms.py",
    "ground_zero_work/phase24/PAPER_THEOREM_INVENTORY.md",
    "ground_zero_work/phase24/FORMALIZATION_LEDGER.md",
)
MATHEMATICA_PREFIX = "ground_zero_work/phase24/mathematica_verification/"
SYMPY_PREFIX = "ground_zero_work/c48_jensen/"


ROLE_SPECS: dict[str, dict[str, object]] = {
    "analytic": {
        "title": "complex analysis and asymptotics",
        "files": (
            "ground_zero_work/phase9/C48_SIGNED_FIFTH_SADDLE.md",
            "ground_zero_work/phase11/C48_SIXTH_RESIDUAL.md",
            "ground_zero_work/phase14/C48_ELEMENTARY_C1_PROOF.md",
            "ground_zero_work/phase15/C48_FULL_C1_BRANCH.md",
            "ground_zero_work/phase18/C48_COMPLEX_SIXTH_SADDLE.md",
            "ground_zero_work/phase18/C48_EFFECTIVITY_AND_MARGIN.md",
            "ground_zero_work/phase18/C48_SECTORIAL_SADDLE_VARIABLE.md",
        ),
        "prefixes": ("ground_zero_work/phase21/", SYMPY_PREFIX),
        "gates": (
            "normalization, Mellin identity, and factor eight",
            "saddle existence, uniqueness, branches, and curvature",
            "legal contour, central Gaussian, connectors, and tails",
            "higher theta modes and fixed-sector uniformity",
            "derivative tower through order six and H6 majorant",
            "elementary C1/branch estimates and quantified domains",
            "coefficient assembly, interpolation, and effectivity",
        ),
    },
    "algebraic": {
        "title": "special functions, finite-free algebra, and root geometry",
        "files": (
            "ground_zero_work/phase14/C48_ELEMENTARY_C1_PROOF.md",
            "ground_zero_work/phase15/C48_FULL_C1_BRANCH.md",
            "ground_zero_work/phase16/C48_UNIFORM_RADIUS_PROOF.md",
            "ground_zero_work/phase17/C48_SIXTH_STABILITY_AND_ASSEMBLY.md",
            "ground_zero_work/phase24/PRIMARY_SOURCE_AUDIT.md",
            "ground_zero_work/phase24/SOURCE_HASHES.sha256",
            "ground_zero_work/phase25/finite_free_property_tests.py",
            "ground_zero_work/phase25/hypergeometric_property_tests.py",
            "ground_zero_work/phase25/branch_interval_certificates.py",
        ),
        "prefixes": (SYMPY_PREFIX, f"{LEAN_ROOT}/Zeta23/Research/JensenWedge/"),
        "gates": (
            "leading system, Jacobian, and quotient adapter",
            "terminating 3F2 producer, ODE, and recurrence",
            "finite-free conventions and reciprocal orientation",
            "Jacobi, MSS, and MMP input interfaces",
            "global-maximum radius and exact constants",
            "Hermite--Genocchi remainder and sign transfer",
        ),
    },
    "lean": {
        "title": "Lean statement-strength and proof-surface audit",
        "files": FORMAL_INDEX_FILES + ASSURANCE_FILES,
        "prefixes": (f"{LEAN_ROOT}/",),
        "gates": (
            "T1--T18 claim-to-declaration map",
            "exact theorem hypotheses and conditional boundaries",
            "producer strength for HG, cube calculus, and recurrence",
            "whole-box quantitative certificate types",
            "typed classical/external root-theory inputs",
            "proof-escape and complete axiom-surface audit",
        ),
    },
    "reproducibility": {
        "title": "reproducibility, source fidelity, and package audit",
        "files": (
            "requirements-c48.lock",
            ".github/workflows/c48-linux-verification.yml",
            "reproduce/VERIFY_ALL.sh",
            "reproduce/BUILD_MANUSCRIPTS.sh",
            "ground_zero_work/phase25/ENVIRONMENT_INVENTORY.json",
            "ground_zero_work/phase25/PHASE_K_REPRODUCIBILITY.md",
            "ground_zero_work/phase25/verify_reproducibility_inventory.py",
            "ground_zero_work/phase25/reproducibility_behavioral_mutations.py",
            "ground_zero_work/phase25/verify_git_bundle.py",
            "ground_zero_work/phase24/INTERVAL_CERTIFICATES.json",
            "ground_zero_work/phase24/verify_interval_certificates.py",
            "ground_zero_work/phase24/verify_mathematica_evidence.py",
        ) + PRIMARY_SOURCE_FILES,
        "prefixes": (MATHEMATICA_PREFIX, SYMPY_PREFIX, f"{LEAN_ROOT}/"),
        "gates": (
            "immutable commit and checkpoint ancestry",
            "complete manifest and archive-local commands",
            "pinned environments and clean reconstruction",
            "Mathematica and exact-result provenance",
            "PDF, Lean, interval, Arb/ACB, and mutation replay",
            "source versions, hashes, licensing, and disclosures",
        ),
    },
    "hostile": {
        "title": "hostile falsification and counterexample search",
        "files": ASSURANCE_FILES + PRIMARY_SOURCE_FILES + FORMAL_INDEX_FILES,
        "prefixes": (
            "ground_zero_work/phase20/",
            "ground_zero_work/phase21/",
            SYMPY_PREFIX,
            f"{LEAN_ROOT}/Zeta23/Research/JensenWedge/",
        ),
        "gates": (
            "normalization, sign, factorial, and scale counterexamples",
            "branch-cut, sector, contour, and uniformity counterexamples",
            "parameter-box, recurrence, and denominator failures",
            "finite-free orientation and root-theory interface failures",
            "radius, interpolation, and tail-summation failures",
            "hidden implication, quantifier, threshold, or packaging failures",
        ),
    },
}


VERIFY_BUNDLE = r'''#!/usr/bin/env python3
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
'''.encode("utf-8")


VERIFY_ANCESTRY = r'''#!/usr/bin/env python3
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
'''.encode("utf-8")


BUILD_PACKET_MANUSCRIPTS = f'''#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${{BASH_SOURCE[0]}}")/.." && pwd)"
TECTONIC="${{C48_TECTONIC:-$(command -v tectonic || true)}}"
if [[ -z "$TECTONIC" || ! -x "$TECTONIC" ]]; then
  printf '%s\n' 'FAIL: Tectonic is required for manuscript replay' >&2
  exit 2
fi
TMP_DIR="$(mktemp -d -t jensen-phase-m-pdf.XXXXXX)"
trap 'rm -rf "$TMP_DIR"' EXIT
export SOURCE_DATE_EPOCH="{SOURCE_DATE_EPOCH}"
"$TECTONIC" -X compile "$ROOT/PAPER/source/JENSEN_TWO_THIRDS_MAIN.tex" --outdir "$TMP_DIR"
"$TECTONIC" -X compile "$ROOT/PAPER/source/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex" --outdir "$TMP_DIR"
cmp "$TMP_DIR/JENSEN_TWO_THIRDS_MAIN.pdf" "$ROOT/PAPER/JENSEN_TWO_THIRDS_MAIN.pdf"
cmp "$TMP_DIR/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf" "$ROOT/PAPER/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf"
printf '%s\n' 'PASS extraction-local deterministic manuscript replay'
'''.encode("utf-8")


VERIFY_ARCHIVE = r'''#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-packet}"
python3 "$ROOT/VERIFY_BUNDLE.py"
python3 "$ROOT/VERIFY_ANCESTRY.py"
bash "$ROOT/REPRODUCE/BUILD_PACKET_MANUSCRIPTS.sh"

if [[ "$MODE" == packet ]]; then
  printf '%s\n' 'PASS extraction-local packet, ancestry, and manuscript replay'
  exit 0
fi
if [[ "$MODE" != quick && "$MODE" != full ]]; then
  printf '%s\n' 'usage: VERIFY_ARCHIVE.sh [packet|quick|full]' >&2
  exit 2
fi
BUNDLE="$ROOT/AUDIT/CANDIDATE_HISTORY.bundle"
if [[ ! -f "$BUNDLE" ]]; then
  printf '%s\n' "FAIL: $MODE requires the full audit archive history bundle" >&2
  exit 2
fi
PYTHON_BIN="${C48_PYTHON:-}"
if [[ -z "$PYTHON_BIN" || ! -x "$PYTHON_BIN" ]]; then
  printf '%s\n' 'FAIL: set C48_PYTHON to the pinned Python executable' >&2
  exit 2
fi
TMP_DIR="$(mktemp -d -t jensen-phase-m-repo.XXXXXX)"
trap 'rm -rf "$TMP_DIR"' EXIT
git clone --quiet --branch phase-m-candidate "$BUNDLE" "$TMP_DIR/repository"
if [[ "$MODE" == quick ]]; then
  C48_PYTHON="$PYTHON_BIN" C48_TECTONIC="${C48_TECTONIC:-$(command -v tectonic)}" \
    bash "$TMP_DIR/repository/reproduce/VERIFY_ALL.sh" quick
else
  ELAN_ROOT="${C48_ELAN_HOME:-${ELAN_HOME:-$HOME/.elan}}"
  LEAN_PROJECT="$TMP_DIR/repository/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
  (
    cd "$LEAN_PROJECT"
    env ELAN_HOME="$ELAN_ROOT" "$ELAN_ROOT/bin/lake" exe cache get
    env ELAN_HOME="$ELAN_ROOT" "$ELAN_ROOT/bin/lake" build \
      Zeta23.Research.JensenWedge
  )
  C48_PYTHON="$PYTHON_BIN" C48_TECTONIC="${C48_TECTONIC:-$(command -v tectonic)}" \
    C48_ELAN_HOME="$ELAN_ROOT" \
    bash "$TMP_DIR/repository/reproduce/VERIFY_ALL.sh" full
fi
printf '%s\n' "PASS extraction-local audit repository $MODE replay"
'''.encode("utf-8")


def run(*args: str, cwd: Path = ROOT, capture: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        list(args),
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def git_bytes(*args: str) -> bytes:
    return run("git", *args).stdout


def candidate_commit() -> str:
    requested = os.environ.get("C48_PHASE_M_CANDIDATE", "HEAD")
    candidate = git_bytes("rev-parse", f"{requested}^{{commit}}")
    candidate = candidate.decode("ascii").strip()
    head = git_bytes("rev-parse", "HEAD").decode("ascii").strip()
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", candidate, head], cwd=ROOT
    ).returncode != 0:
        raise ValueError("Phase-M candidate must be an ancestor of current HEAD")
    return candidate


def tracked_files(candidate: str) -> set[str]:
    return set(
        git_bytes("ls-tree", "-r", "--name-only", candidate)
        .decode("utf-8")
        .splitlines()
    )


def candidate_bytes(candidate: str, relative: str) -> bytes:
    return git_bytes("show", f"{candidate}:{relative}")


def release_head_bytes(relative: str) -> bytes:
    """Read post-candidate packaging/validation evidence from release HEAD."""
    return git_bytes("show", f"HEAD:{relative}")


def paths_with_prefix(tracked: set[str], prefix: str) -> list[str]:
    return sorted(
        path
        for path in tracked
        if path.startswith(prefix)
        and "__pycache__" not in path
        and not path.endswith(".pyc")
    )


def ensure_files(tracked: set[str], paths: tuple[str, ...] | list[str]) -> None:
    missing = sorted(set(paths) - tracked)
    if missing:
        raise FileNotFoundError("candidate lacks required files:\n" + "\n".join(missing))


def ancestry_proof(candidate: str) -> bytes:
    algorithm = git_bytes("rev-parse", "--show-object-format").decode("ascii").strip()
    chain = []
    current = candidate
    seen: set[str] = set()
    while True:
        if current in seen:
            raise ValueError("cycle while constructing ancestry proof")
        seen.add(current)
        raw = git_bytes("cat-file", "commit", current)
        chain.append(
            {
                "commit_base64": base64.b64encode(raw).decode("ascii"),
                "oid": current,
            }
        )
        if current == CHECKPOINT:
            break
        parents = git_bytes("show", "-s", "--format=%P", current).decode("ascii").split()
        next_parent = None
        for parent in parents:
            result = subprocess.run(
                ["git", "merge-base", "--is-ancestor", CHECKPOINT, parent],
                cwd=ROOT,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if result.returncode == 0:
                next_parent = parent
                break
        if next_parent is None:
            raise ValueError("checkpoint is not in candidate history")
        current = next_parent
    payload = {
        "candidate": candidate,
        "chain": chain,
        "checkpoint": CHECKPOINT,
        "object_format": algorithm,
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def history_bundle(candidate: str) -> bytes:
    with tempfile.TemporaryDirectory(prefix="phase-m-history-") as temporary:
        bare = Path(temporary) / "repository.git"
        bundle = Path(temporary) / "CANDIDATE_HISTORY.bundle"
        run("git", "init", "--quiet", "--bare", str(bare))
        run(
            "git",
            "-C",
            str(bare),
            "fetch",
            "--quiet",
            "--no-tags",
            str(ROOT),
            f"{candidate}:refs/heads/phase-m-candidate",
        )
        run(
            "git",
            "-C",
            str(bare),
            "-c",
            "pack.threads=1",
            "repack",
            "-adf",
            "--window=0",
        )
        run(
            "git",
            "-C",
            str(bare),
            "-c",
            "pack.threads=1",
            "bundle",
            "create",
            str(bundle),
            "phase-m-candidate",
        )
        run("git", "bundle", "verify", str(bundle))
        return bundle.read_bytes()


def add_snapshot(
    entries: dict[str, bytes], candidate: str, source: str, destination: str
) -> None:
    if destination in entries:
        if entries[destination] != candidate_bytes(candidate, source):
            raise ValueError(f"conflicting archive destination: {destination}")
        return
    entries[destination] = candidate_bytes(candidate, source)


def add_prefix(
    entries: dict[str, bytes],
    candidate: str,
    tracked: set[str],
    prefix: str,
    destination_prefix: str,
) -> None:
    for source in paths_with_prefix(tracked, prefix):
        relative = source.removeprefix(prefix)
        add_snapshot(entries, candidate, source, f"{destination_prefix}{relative}")


def manifest(entries: dict[str, bytes]) -> bytes:
    return "".join(
        f"{hashlib.sha256(data).hexdigest()}  {name}\n"
        for name, data in sorted(entries.items())
    ).encode("utf-8")


def metadata(candidate: str, package_class: str, title: str) -> bytes:
    payload = {
        "artifact": title,
        "candidate_commit": candidate,
        "date": "2026-08-18",
        "package_class": package_class,
        "required_checkpoint": CHECKPOINT,
        "review_status": "AI review only; no human or peer review",
        "source_date_epoch": int(SOURCE_DATE_EPOCH),
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def common_generated(
    entries: dict[str, bytes], candidate: str, package_class: str, title: str
) -> None:
    entries["VERIFY_BUNDLE.py"] = VERIFY_BUNDLE
    entries["VERIFY_ANCESTRY.py"] = VERIFY_ANCESTRY
    entries["ANCESTRY_PROOF.json"] = ancestry_proof(candidate)
    entries["RELEASE_METADATA.json"] = metadata(candidate, package_class, title)
    entries["REPRODUCE/BUILD_PACKET_MANUSCRIPTS.sh"] = BUILD_PACKET_MANUSCRIPTS
    entries["REPRODUCE/VERIFY_ARCHIVE.sh"] = VERIFY_ARCHIVE


def referee_entries(candidate: str, tracked: set[str]) -> dict[str, bytes]:
    entries: dict[str, bytes] = {}
    for source in PAPER_FILES:
        add_snapshot(entries, candidate, source, f"PAPER/source/{Path(source).name}")
    for source in PDF_FILES:
        add_snapshot(entries, candidate, source, f"PAPER/{Path(source).name}")
    add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md",
        "PUBLIC/JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md",
    )
    add_prefix(entries, candidate, tracked, f"{LEAN_ROOT}/", "FORMAL/lean-project/")
    add_snapshot(
        entries,
        candidate,
        "paper/THEOREM_EVIDENCE_CROSS_REFERENCE.md",
        "FORMAL/THEOREM_MAP.md",
    )
    add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase25/PHASE25_AXIOM_AUDIT.txt",
        "FORMAL/AXIOM_AUDIT.txt",
    )
    add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase25/Phase25Axioms.lean",
        "FORMAL/Phase25Axioms.lean",
    )
    for source in FORMAL_INDEX_FILES + ASSURANCE_FILES:
        add_snapshot(entries, candidate, source, f"FORMAL/evidence/{Path(source).name}")
    add_prefix(entries, candidate, tracked, MATHEMATICA_PREFIX, "COMPUTATION/mathematica/")
    add_prefix(entries, candidate, tracked, SYMPY_PREFIX, "COMPUTATION/sympy/")
    for source in (
        "ground_zero_work/phase25/ARB_ACB_METHOD.md",
        "ground_zero_work/phase25/ARB_ACB_RESULTS.json",
        "ground_zero_work/phase25/arb_acb_verification.py",
        "ground_zero_work/phase25/arb_acb_semantic_mutations.py",
    ):
        add_snapshot(entries, candidate, source, f"COMPUTATION/arb_acb/{Path(source).name}")
    for source in (
        "ground_zero_work/phase24/INTERVAL_CERTIFICATES.json",
        "ground_zero_work/phase24/verify_interval_certificates.py",
        "ground_zero_work/phase25/branch_interval_certificates.py",
        "ground_zero_work/phase25/branch_semantic_mutations.py",
    ):
        add_snapshot(
            entries, candidate, source, f"COMPUTATION/interval_certificates/{Path(source).name}"
        )
    for source in (
        "ground_zero_work/phase25/EFFECTIVITY_LEDGER.json",
        "ground_zero_work/phase25/EFFECTIVITY_LEDGER.md",
        "ground_zero_work/phase25/effectivity_ledger.py",
        "ground_zero_work/phase25/effectivity_semantic_mutations.py",
    ):
        add_snapshot(entries, candidate, source, f"COMPUTATION/effectivity/{Path(source).name}")
    add_prefix(entries, candidate, tracked, "ground_zero_work/phase21/", "SUPPORT/phase21/")
    for source in paths_with_prefix(tracked, "ground_zero_work/phase20/"):
        if source.endswith((".md", ".lean", ".py", ".sh", ".json", ".txt")):
            add_snapshot(entries, candidate, source, f"SUPPORT/phase20/{Path(source).name}")
    for source in ASSURANCE_FILES:
        add_snapshot(entries, candidate, source, f"SUPPORT/assurance/{Path(source).name}")
    for source in PRIMARY_SOURCE_FILES:
        add_snapshot(entries, candidate, source, f"SUPPORT/primary_sources/{Path(source).name}")
    for source in DISCLOSURE_FILES:
        add_snapshot(entries, candidate, source, f"DISCLOSURE/{Path(source).name}")
    add_snapshot(
        entries,
        candidate,
        f"{MATERIALS}/REFEREE_START_HERE.md",
        "START_HERE.md",
    )
    add_snapshot(
        entries,
        candidate,
        f"{MATERIALS}/EXPECTED_RESULTS.md",
        "REPRODUCE/EXPECTED_RESULTS.md",
    )
    add_snapshot(entries, candidate, "requirements-c48.lock", "REPRODUCE/requirements-c48.lock")
    add_snapshot(
        entries,
        candidate,
        "ground_zero_work/phase25/ENVIRONMENT_INVENTORY.json",
        "REPRODUCE/ENVIRONMENT_INVENTORY.json",
    )
    for source in PHASE_N_VALIDATION_FILES:
        entries[f"RELEASE_VALIDATION/{Path(source).name}"] = release_head_bytes(source)
    common_generated(entries, candidate, "M1", "Jensen Two-Thirds Referee Packet")
    return entries


def audit_entries(
    candidate: str, tracked: set[str], bundle: bytes
) -> dict[str, bytes]:
    entries = referee_entries(candidate, tracked)
    entries["START_HERE.md"] = candidate_bytes(candidate, f"{MATERIALS}/AUDIT_START_HERE.md")
    snapshot_prefixes = (
        "ground_zero_work/",
        f"{LEAN_ROOT}/",
        "paper/",
        "reproduce/",
        ".github/workflows/",
    )
    snapshot_exact = {"requirements-c48.lock"}
    for source in sorted(tracked):
        if source in snapshot_exact or any(source.startswith(prefix) for prefix in snapshot_prefixes):
            add_snapshot(entries, candidate, source, f"AUDIT/repository/{source}")
    for source in PDF_FILES:
        add_snapshot(entries, candidate, source, f"AUDIT/repository/{source}")
    entries["AUDIT/CANDIDATE_HISTORY.bundle"] = bundle
    entries["AUDIT/SNAPSHOT_SCOPE.md"] = (
        "# Audit snapshot scope\n\n"
        "The browsable snapshot contains all tracked `ground_zero_work`, the complete "
        "pinned Lean project, paper sources, reproduction scripts, workflow, locks, and "
        "frozen manuscript PDFs. The offline Git bundle reconstructs the exact complete "
        "candidate history. Build caches, virtual environments, `.git`, unrelated numerical "
        "experiments, and old release containers are not duplicated in the browsable tree.\n"
    ).encode("utf-8")
    entries["RELEASE_METADATA.json"] = metadata(
        candidate, "M2", "Jensen Two-Thirds Full Audit Archive"
    )
    return entries


def review_instructions(role: str, spec: dict[str, object], candidate: str) -> bytes:
    gates = "\n".join(f"- {gate}: PASS / FAIL / UNCHECKED" for gate in spec["gates"])
    return f"""# Fresh {spec['title']} review packet

Candidate commit: `{candidate}`
Required checkpoint: `{CHECKPOINT}`

This packet contains no prior review report, verdict, or author disposition.
Try to falsify the candidate from definitions before accepting any gate. A
programmed PASS establishes only its programmed predicate. Distinguish paper
proof, Lean theorem, exact algebra, interval enclosure, finite-grid regression,
and imported mathematics.

## Gates

{gates}

## Required report

Give a gate table, numbered P0--P3 findings, independent-recalculation record,
unchecked-claims list, exact release recommendation, and model/provider/tool
and conflict disclosure. Any new calculation must construct expected values
from definitions rather than read a frozen repository result as its oracle.

Do not describe this as human or peer review. Separation of the packet does
not by itself make an AI review epistemically independent.
""".encode("utf-8")


def review_entries(
    role: str, spec: dict[str, object], candidate: str, tracked: set[str]
) -> dict[str, bytes]:
    entries: dict[str, bytes] = {}
    for source in PAPER_FILES:
        add_snapshot(entries, candidate, source, f"PAPER/source/{Path(source).name}")
    for source in PDF_FILES:
        add_snapshot(entries, candidate, source, f"PAPER/{Path(source).name}")
    for source in DISCLOSURE_FILES:
        add_snapshot(entries, candidate, source, f"DISCLOSURE/{Path(source).name}")
    selected = list(spec["files"])
    ensure_files(tracked, selected)
    for source in selected:
        add_snapshot(entries, candidate, source, f"EVIDENCE/{source}")
    for prefix in spec["prefixes"]:
        for source in paths_with_prefix(tracked, prefix):
            if "/reviews" in source.lower() or "review_" in source.lower():
                continue
            add_snapshot(entries, candidate, source, f"EVIDENCE/{source}")
    add_snapshot(entries, candidate, "requirements-c48.lock", "REPRODUCE/requirements-c48.lock")
    entries["START_HERE.md"] = (
        f"# Start here: fresh {spec['title']} review\n\n"
        "Run `python3 VERIFY_BUNDLE.py`, `python3 VERIFY_ANCESTRY.py`, and "
        "`bash REPRODUCE/VERIFY_ARCHIVE.sh packet`. Then read "
        "`ROLE_REVIEW_PACKET.md`. This is confidential working mathematics. "
        "No prior verdict is included. This packet does not represent human or "
        "peer review.\n"
    ).encode("utf-8")
    entries["ROLE_REVIEW_PACKET.md"] = review_instructions(role, spec, candidate)
    common_generated(
        entries,
        candidate,
        f"M3-{role}",
        f"Jensen Two-Thirds Fresh {spec['title'].title()} Review Packet",
    )
    check_review_separation(entries)
    return entries


def check_review_separation(entries: dict[str, bytes]) -> None:
    banned_paths = re.compile(r"review.*(?:report|finding|disposition)|reviews_phase", re.I)
    for path in entries:
        if path == "ROLE_REVIEW_PACKET.md":
            continue
        if banned_paths.search(path):
            raise ValueError(f"prior-review path leaked into fresh packet: {path}")
    banned_markers = (b"Overall verdict", b"Verdict: R", b"AUTHOR_DISPOSITION")
    for path, data in entries.items():
        if path == "ROLE_REVIEW_PACKET.md" or not path.endswith((".md", ".txt")):
            continue
        if any(marker in data for marker in banned_markers):
            raise ValueError(f"prior-review outcome leaked through {path}")


def write_zip(path: Path, entries: dict[str, bytes], root_name: str) -> None:
    complete = dict(entries)
    complete["MANIFEST.sha256"] = manifest(entries)
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in sorted(complete.items()):
            info = zipfile.ZipInfo(f"{root_name}/{name}", date_time=FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            executable = name.endswith(".sh") or name.startswith("VERIFY_")
            info.external_attr = (0o100755 if executable else 0o100644) << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)


def verify_zip(path: Path, run_quick: bool) -> None:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if names != sorted(names) or len(names) != len(set(names)):
            raise ValueError(f"noncanonical member order: {path.name}")
        if any(info.date_time != FIXED_TIMESTAMP for info in archive.infolist()):
            raise ValueError(f"noncanonical timestamp: {path.name}")
        prefix = f"{path.stem}/"
        if any(not name.startswith(prefix) for name in names):
            raise ValueError(f"wrong archive root: {path.name}")
        stripped = {name.removeprefix(prefix): archive.read(name) for name in names}
        declared = stripped.pop("MANIFEST.sha256")
        if declared != manifest(stripped):
            raise ValueError(f"manifest mismatch: {path.name}")
    with tempfile.TemporaryDirectory(prefix="phase-m-extract-") as temporary:
        with zipfile.ZipFile(path) as archive:
            archive.extractall(temporary)
        packet = Path(temporary) / path.stem
        subprocess.run(["python3", "VERIFY_BUNDLE.py"], cwd=packet, check=True)
        subprocess.run(["python3", "VERIFY_ANCESTRY.py"], cwd=packet, check=True)
        environment = os.environ.copy()
        environment["C48_PYTHON"] = str(ROOT / ".venv/bin/python")
        subprocess.run(
            ["bash", "REPRODUCE/VERIFY_ARCHIVE.sh", "packet"],
            cwd=packet,
            check=True,
            env=environment,
        )
        extra = packet / "UNMANIFESTED_EXTRA.txt"
        extra.write_text("manifest coverage attack\n", encoding="utf-8")
        attack = subprocess.run(
            ["python3", "VERIFY_BUNDLE.py"],
            cwd=packet,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if attack.returncode == 0:
            raise ValueError(f"manifest accepted extra file: {path.name}")
        extra.unlink()
        ancestry = packet / "ANCESTRY_PROOF.json"
        original = ancestry.read_bytes()
        mutated = json.loads(original)
        mutated["candidate"] = "0" * len(mutated["candidate"])
        ancestry.write_text(json.dumps(mutated), encoding="utf-8")
        attack = subprocess.run(
            ["python3", "VERIFY_ANCESTRY.py"],
            cwd=packet,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if attack.returncode == 0:
            raise ValueError(f"ancestry verifier accepted mutation: {path.name}")
        ancestry.write_bytes(original)
        if run_quick:
            subprocess.run(
                ["bash", "REPRODUCE/VERIFY_ARCHIVE.sh", "quick"],
                cwd=packet,
                check=True,
                env=environment,
            )


def deterministic_package(
    filename: str, entries: dict[str, bytes], run_quick: bool
) -> tuple[Path, str]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT / filename
    with tempfile.TemporaryDirectory(prefix="phase-m-double-build-") as temporary:
        first = Path(temporary) / "first.zip"
        second = Path(temporary) / "second.zip"
        root_name = Path(filename).stem
        write_zip(first, entries, root_name)
        write_zip(second, entries, root_name)
        if first.read_bytes() != second.read_bytes():
            raise ValueError(f"nondeterministic package: {filename}")
        shutil.copyfile(first, destination)
    verify_zip(destination, run_quick=run_quick)
    digest = hashlib.sha256(destination.read_bytes()).hexdigest()
    print(f"PASS deterministic Phase-M package: {destination.relative_to(ROOT)}")
    return destination, digest


def split_full_audit_archive(path: Path, digest: str) -> list[str]:
    """Split the validated archive below GitHub's 100 MiB object limit."""
    part_size = 90 * 1024 * 1024
    prefix = f"{path.name}.part"
    for stale in OUTPUT.glob(f"{prefix}*"):
        stale.unlink()
    payload = path.read_bytes()
    parts: list[dict[str, object]] = []
    checksums: list[str] = []
    for number, offset in enumerate(range(0, len(payload), part_size), start=1):
        name = f"{prefix}{number:02d}"
        part_payload = payload[offset : offset + part_size]
        (OUTPUT / name).write_bytes(part_payload)
        part_digest = hashlib.sha256(part_payload).hexdigest()
        parts.append({"name": name, "bytes": len(part_payload), "sha256": part_digest})
        checksums.append(f"{part_digest}  {name}")
    metadata = {
        "version": 1,
        "archive": path.name,
        "bytes": len(payload),
        "sha256": digest,
        "parts": parts,
    }
    (OUTPUT / "FULL_AUDIT_REASSEMBLY.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    reassembler = '''#!/usr/bin/env python3
"""Reassemble and verify the split Jensen two-thirds full audit archive."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
METADATA = json.loads((ROOT / "FULL_AUDIT_REASSEMBLY.json").read_text(encoding="utf-8"))


def main() -> None:
    destination = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else ROOT / METADATA["archive"]
    if len(sys.argv) > 2:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [output.zip]")
    payloads = []
    for part in METADATA["parts"]:
        path = ROOT / part["name"]
        payload = path.read_bytes()
        if len(payload) != part["bytes"] or hashlib.sha256(payload).hexdigest() != part["sha256"]:
            raise SystemExit(f"FAIL split-part verification: {path.name}")
        payloads.append(payload)
    archive = b"".join(payloads)
    if len(archive) != METADATA["bytes"] or hashlib.sha256(archive).hexdigest() != METADATA["sha256"]:
        raise SystemExit("FAIL reassembled archive verification")
    destination.write_bytes(archive)
    print(f"PASS reassembled {destination} sha256={METADATA['sha256']}")


if __name__ == "__main__":
    main()
'''
    reassembler_path = OUTPUT / "REASSEMBLE_FULL_AUDIT.py"
    reassembler_path.write_text(reassembler, encoding="utf-8")
    reassembler_path.chmod(0o755)
    with tempfile.TemporaryDirectory(prefix="phase-m-reassembly-") as temporary:
        rebuilt = Path(temporary) / path.name
        subprocess.run(
            [sys.executable, str(reassembler_path), str(rebuilt)],
            cwd=OUTPUT,
            check=True,
        )
        if rebuilt.read_bytes() != payload:
            raise ValueError("split archive did not reassemble byte-for-byte")
    path.unlink()
    print(
        "PASS split full audit archive: "
        f"{len(parts)} sub-100-MiB parts, byte-exact verified reassembly"
    )
    return checksums


def main() -> None:
    if subprocess.run(["git", "diff", "--quiet"], cwd=ROOT).returncode != 0:
        raise SystemExit("FAIL package builder requires a clean tracked working tree")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode != 0:
        raise SystemExit("FAIL package builder requires an empty index")
    candidate = candidate_commit()
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", CHECKPOINT, candidate], cwd=ROOT
    ).returncode != 0:
        raise SystemExit("FAIL required checkpoint is not in candidate history")
    tracked = tracked_files(candidate)
    required = list(PAPER_FILES + PDF_FILES + DISCLOSURE_FILES + ASSURANCE_FILES)
    required.extend(
        [
            f"{MATERIALS}/REFEREE_START_HERE.md",
            f"{MATERIALS}/AUDIT_START_HERE.md",
            f"{MATERIALS}/EXPECTED_RESULTS.md",
            "requirements-c48.lock",
        ]
    )
    ensure_files(tracked, required)
    bundle = history_bundle(candidate)
    if bundle != history_bundle(candidate):
        raise ValueError("candidate history bundle is not byte deterministic")

    checksums: list[str] = []
    _, digest = deterministic_package(
        "Jensen_Two_Thirds_Referee_Packet.zip",
        referee_entries(candidate, tracked),
        run_quick=False,
    )
    checksums.append(f"{digest}  Jensen_Two_Thirds_Referee_Packet.zip")
    audit_path, digest = deterministic_package(
        "Jensen_Two_Thirds_Full_Audit_Archive.zip",
        audit_entries(candidate, tracked, bundle),
        run_quick=True,
    )
    audit_digest = digest
    for role, spec in ROLE_SPECS.items():
        filename = f"Jensen_Two_Thirds_Fresh_{role.title()}_AI_Review_Packet.zip"
        _, digest = deterministic_package(
            filename,
            review_entries(role, spec, candidate, tracked),
            run_quick=False,
        )
        checksums.append(f"{digest}  {filename}")
    checksums.extend(split_full_audit_archive(audit_path, audit_digest))
    checksum_path = OUTPUT / "SHA256SUMS.txt"
    checksum_path.write_text("\n".join(sorted(checksums)) + "\n", encoding="utf-8")
    index = OUTPUT / "PACKAGE_INDEX.md"
    index.write_text(
        "# Jensen two-thirds Phase-M packages\n\n"
        f"Candidate: `{candidate}`  \n"
        f"Required checkpoint: `{CHECKPOINT}`\n\n"
        "- `Jensen_Two_Thirds_Referee_Packet.zip`: navigable paper/formal/computation packet.\n"
        "- `Jensen_Two_Thirds_Full_Audit_Archive.zip.part*`: complete relevant source, "
        "review, and history archive, split below GitHub's object-size limit. Run "
        "`python3 REASSEMBLE_FULL_AUDIT.py` to recover and verify the byte-exact ZIP.\n"
        "- `Jensen_Two_Thirds_Fresh_*_AI_Review_Packet.zip`: prior-verdict-free role packets.\n\n"
        "The referee and full-audit packets include `RELEASE_VALIDATION/` with the final "
        "Phase-N handoff, successful serial logs, and the retained initial clean-replay "
        "failure that led to the umbrella-build repair.\n\n"
        "Every archive passed deterministic double-build, fail-closed manifest and ancestry "
        "mutations, extraction-local manuscript replay, and canonical ZIP checks. The full "
        f"audit archive also passed extraction-local repository quick replay. Its reassembled "
        f"SHA-256 is `{audit_digest}`. All existing "
        "review is AI review, not human or peer review.\n",
        encoding="utf-8",
    )
    print(f"PASS external package checksums: {checksum_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
