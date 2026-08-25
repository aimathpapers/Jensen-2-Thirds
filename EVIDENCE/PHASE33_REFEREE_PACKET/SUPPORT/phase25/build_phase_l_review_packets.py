#!/usr/bin/env python3
"""Build deterministic Phase-L targeted correlated AI re-review packets."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "output" / "reviewer_packets_phase25_ai_repaired"
CANDIDATE_COMMIT = "6ee1db8fc5789a01bc0297f850c817f55b529be4"
REQUIRED_CHECKPOINT = "5f79158f9c6276dd09142edeea279e35b0d58406"
FIXED_TIMESTAMP = (2026, 8, 17, 12, 0, 0)
LEAN_ROOT = "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"


COMMON_FILES = [
    "paper/JENSEN_TWO_THIRDS_MAIN.tex",
    "paper/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex",
    "paper/THEOREM_EVIDENCE_CROSS_REFERENCE.md",
    "paper/c48_common.tex",
    "paper/c48_detailed_appendices.tex",
    "paper/references.bib",
    "output/pdf/JENSEN_TWO_THIRDS_MAIN.pdf",
    "output/pdf/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf",
    "ground_zero_work/phase20/HOLLAND_DEPENDENCY_FIREWALL.md",
    "ground_zero_work/phase20/HOLLAND_MULTIPLIER_REPROOF.md",
    "ground_zero_work/phase20/HOLLAND_PROP41_REPROOF.md",
    "ground_zero_work/phase20/Phase20Axioms.lean",
    "ground_zero_work/phase20/GORTTW_PRIMARY_INPUT.md",
    "ground_zero_work/phase25/ASYMPTOTIC_LANGUAGE_LEDGER.json",
    "ground_zero_work/phase25/EFFECTIVITY_LEDGER.json",
    "ground_zero_work/phase25/EFFECTIVITY_LEDGER.md",
    "ground_zero_work/phase25/NOTATION_NORMALIZATION_CROSSWALK.md",
    "ground_zero_work/phase25/PHASE25_AXIOM_AUDIT.txt",
    "ground_zero_work/phase25/Phase25Axioms.lean",
    "ground_zero_work/phase25/PHASE_I_ANALYTIC_LEAN_FEASIBILITY.md",
    "ground_zero_work/phase25/PROOF_DEPENDENCY_GRAPH.json",
    "ground_zero_work/phase25/PROOF_DEPENDENCY_GRAPH.md",
    "ground_zero_work/phase25/THEOREM_ASSURANCE_MATRIX.json",
    "ground_zero_work/phase25/THEOREM_ASSURANCE_MATRIX.md",
    "ground_zero_work/phase25/verify_phase25_axioms.py",
    "requirements-c48.lock",
    "reproduce/README.md",
    "reproduce/BUILD_MANUSCRIPTS.sh",
    f"{LEAN_ROOT}/lake-manifest.json",
    f"{LEAN_ROOT}/lakefile.toml",
    f"{LEAN_ROOT}/lean-toolchain",
    f"{LEAN_ROOT}/Zeta23/Research/JensenWedge.lean",
]


ANALYTIC_FILES = [
    "ground_zero_work/phase9/C48_SIGNED_FIFTH_SADDLE.md",
    "ground_zero_work/phase11/C48_SIXTH_RESIDUAL.md",
    "ground_zero_work/phase14/C48_ELEMENTARY_C1_PROOF.md",
    "ground_zero_work/phase15/C48_FULL_C1_BRANCH.md",
    "ground_zero_work/phase18/C48_COMPLEX_SIXTH_SADDLE.md",
    "ground_zero_work/phase18/C48_EFFECTIVITY_AND_MARGIN.md",
    "ground_zero_work/phase18/C48_SECTORIAL_SADDLE_VARIABLE.md",
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
    "ground_zero_work/phase25/ARB_ACB_METHOD.md",
    "ground_zero_work/phase25/ARB_ACB_RESULTS.json",
    "ground_zero_work/phase25/arb_acb_verification.py",
    "ground_zero_work/phase25/branch_interval_certificates.py",
    "ground_zero_work/phase25/effectivity_ledger.py",
]


ALGEBRAIC_FILES = [
    "ground_zero_work/phase14/C48_ELEMENTARY_C1_PROOF.md",
    "ground_zero_work/phase15/C48_FULL_C1_BRANCH.md",
    "ground_zero_work/phase16/C48_UNIFORM_RADIUS_PROOF.md",
    "ground_zero_work/phase17/C48_SIXTH_STABILITY_AND_ASSEMBLY.md",
    "ground_zero_work/phase18/C48_COMPLEX_SIXTH_SADDLE.md",
    "ground_zero_work/phase24/PRIMARY_SOURCE_AUDIT.md",
    "ground_zero_work/phase24/SOURCE_HASHES.sha256",
    "ground_zero_work/phase25/branch_interval_certificates.py",
    "ground_zero_work/phase25/finite_free_property_tests.py",
    "ground_zero_work/phase25/hypergeometric_property_tests.py",
]


LEAN_FILES = [
    "ground_zero_work/phase24/FORMALIZATION_LEDGER.md",
    "ground_zero_work/phase25/verify_phase25.sh",
    "ground_zero_work/phase21/verify_phase21.sh",
    "ground_zero_work/phase20/verify_phase20.sh",
    "ground_zero_work/phase25/verify_phase25_axioms.py",
]


REPRO_FILES = [
    ".github/workflows/c48-linux-verification.yml",
    "ground_zero_work/phase24/INTERVAL_CERTIFICATES.json",
    "ground_zero_work/phase24/PAPER_THEOREM_INVENTORY.md",
    "ground_zero_work/phase24/PRIMARY_SOURCE_AUDIT.md",
    "ground_zero_work/phase24/SOURCE_HASHES.sha256",
    "ground_zero_work/phase24/manuscript_equation_regression.py",
    "ground_zero_work/phase24/release_checks.py",
    "ground_zero_work/phase24/verify_interval_certificates.py",
    "ground_zero_work/phase24/verify_mathematica_evidence.py",
    "ground_zero_work/phase25/ENVIRONMENT_INVENTORY.json",
    "ground_zero_work/phase25/PHASE_K_REPRODUCIBILITY.md",
    "ground_zero_work/phase25/ARB_ACB_RESULTS.json",
    "ground_zero_work/phase25/arb_acb_verification.py",
    "ground_zero_work/phase25/branch_interval_certificates.py",
    "ground_zero_work/phase25/manuscript_release_checks.py",
    "ground_zero_work/phase25/manuscript_semantic_mutations.py",
    "ground_zero_work/phase25/phase25_semantic_mutations.py",
    "ground_zero_work/phase25/reproducibility_behavioral_mutations.py",
    "ground_zero_work/phase25/verify_phase25_metadata.py",
    "ground_zero_work/phase25/verify_git_bundle.py",
    "ground_zero_work/phase25/verify_reproducibility_inventory.py",
    "reproduce/BUILD_MANUSCRIPTS.sh",
]


MATHEMATICA_FILES = [
    "ground_zero_work/phase24/mathematica_verification/C48_Mathematica_CleanRoom.pdf",
    "ground_zero_work/phase24/mathematica_verification/C48_Mathematica_CleanRoom_2.nb",
    "ground_zero_work/phase24/mathematica_verification/C48_Mathematica_Result_Ledger.txt",
    "ground_zero_work/phase24/mathematica_verification/SHA256SUMS.txt",
    "ground_zero_work/phase24/mathematica_verification/VERIFICATION_RECORD.md",
]


ROLES = {
    "analytic": {
        "title": "Complex analysis and asymptotics",
        "files": ANALYTIC_FILES + MATHEMATICA_FILES,
        "dynamic": ("ground_zero_work/c48_jensen/",),
        "gates": (
            "A0 completed-xi, Mellin, and factor-eight normalization",
            "A1 sectorial saddle existence, uniqueness, branches, and Q nonvanishing",
            "A2 contour deformation, connector control, theta-mode tails, and uniformity",
            "A3 implicit derivative tower through order six and chain constants",
            "A4 H6 denominator, 82-term numerator, box majorant, and sixth derivative bound",
            "A5 paired polygamma and elementary cube-integral estimates",
            "A6 four-parameter C1 branch and all quantified box hypotheses",
            "A7 coefficient asymptotic and transfer to Jensen coefficients",
            "A8 sixth-order interpolation remainder and theorem-sector uniformity",
            "A9 effectivity ledger and finite-range absorption",
            "A10 final theorem quantifiers and dependence on imported results",
        ),
    },
    "algebraic": {
        "title": "Special functions, finite-free algebra, and root geometry",
        "files": ALGEBRAIC_FILES + MATHEMATICA_FILES,
        "dynamic": (
            "ground_zero_work/c48_jensen/",
            f"{LEAN_ROOT}/Zeta23/Research/JensenWedge/",
        ),
        "gates": (
            "B1 leading system, positive solution, Jacobian, inverse, and norm",
            "B2 quotient-to-six-coefficient adapter and normalizations",
            "B3 terminating 3F2 producer and shifted differential recurrence",
            "B4 recurrence coefficients and exact property tests",
            "B5 finite-free coefficient conventions, reflection, and reciprocal roots",
            "B6 transported Jacobi matrix, Gershgorin interval, and constant eight",
            "B7 MSS product-root bounds in original and reciprocal orientations",
            "B8 MMP logarithmic mesh adapter and distinctness transfer",
            "B9 first-failure/Newton radius with y powers and localization constant",
            "B10 complex Hermite-Genocchi remainder and simplex mass 1/720",
            "B11 sign transfer, sixth-match gain, and final algebraic assembly",
        ),
    },
    "lean": {
        "title": "Lean statement-strength and proof-surface audit",
        "files": LEAN_FILES,
        "dynamic": (f"{LEAN_ROOT}/Zeta23/",),
        "gates": (
            "L0 every paper-facing formal claim maps to the named Lean theorem",
            "L1 theorem hypotheses are neither omitted nor weakened in prose",
            "L2 complex Hermite-Genocchi and quotient adapter are honestly scoped",
            "L3 elementary cube calculus and terminating recurrence are producer proofs",
            "L4 quantitative branch certificates quantify the whole box",
            "L5 finite-free/Jacobi/MSS/MMP inputs are visibly typed assumptions",
            "L6 analytic adapters do not claim the unformalized contour theorem",
            "L7 no sorry, admit, custom axiom, unsafe, native_decide, or implemented_by escape",
            "L8 #print axioms surface uses only standard foundational axioms",
            "L9 imported-paper trust boundary and conditional headline are explicit",
        ),
    },
    "reproducibility": {
        "title": "Reproducibility, source fidelity, and package audit",
        "files": REPRO_FILES + MATHEMATICA_FILES,
        "dynamic": (
            "ground_zero_work/c48_jensen/",
            f"{LEAN_ROOT}/Zeta23/",
        ),
        "gates": (
            "R0 immutable commit, checkpoint ancestry, and manifest integrity",
            "R1 pinned Lean/Mathlib/Python environments and clean-clone procedure",
            "R2 deterministic verifier outputs and behavioral mutation coverage",
            "R3 Mathematica notebook, PDF, ledger, and checksum provenance",
            "R4 equation regression for factor eight and critical-point radius",
            "R5 exact interval and Arb/ACB source-versus-frozen-result checks",
            "R6 paper/source theorem cross-reference and primary-source fidelity",
            "R7 archive exclusions, confidentiality, licensing, and secret/cache hygiene",
            "R8 disclosed local-versus-hosted kernel-check boundary",
            "R9 commands and expected PASS markers are independently usable",
        ),
    },
    "hostile": {
        "title": "Hostile falsification and counterexample search",
        "files": ANALYTIC_FILES + ALGEBRAIC_FILES + LEAN_FILES + REPRO_FILES + MATHEMATICA_FILES,
        "dynamic": (
            "ground_zero_work/c48_jensen/",
            f"{LEAN_ROOT}/Zeta23/",
        ),
        "gates": (
            "H0 seek a normalization, factorial, sign, or factor-eight counterexample",
            "H1 seek a sector/domain/branch-cut or missing-uniformity counterexample",
            "H2 seek a box point violating positivity, ordering, contraction, or Q nonvanishing",
            "H3 seek a recurrence denominator, termination, or degenerate-parameter failure",
            "H4 seek a finite-free reflection, root-orientation, MSS, or MMP mismatch",
            "H5 seek a radius, localization, exponent, or tail-summation failure",
            "H6 seek an unproved implication hidden by notation or a missing quantifier",
            "H7 seek a threshold/effectivity circularity or uncovered finite range",
            "H8 seek stale artifacts, source mismatch, or verifier false positives",
            "H9 attempt an end-to-end legal parameter counterexample before accepting any gate",
        ),
    },
}


BANNED_PATH_PATTERNS = (
    re.compile(r"(^|/)reviews?(/|_)", re.IGNORECASE),
    re.compile(r"review.*report", re.IGNORECASE),
    re.compile(r"review.*finding", re.IGNORECASE),
    re.compile(r"review.*disposition", re.IGNORECASE),
    re.compile(r"review.*intake", re.IGNORECASE),
)
HISTORY_ROLES = {"reproducibility", "hostile"}


VERIFY_BUNDLE = r'''#!/usr/bin/env python3
"""Verify immutable files in an extracted Phase-L AI review packet."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
ROW = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<path>.+)$")
rows = []
for line in (ROOT / "EVIDENCE_MANIFEST.sha256").read_text(encoding="utf-8").splitlines():
    match = ROW.fullmatch(line)
    if match is None:
        raise SystemExit(f"FAIL malformed manifest row: {line!r}")
    relative = match.group("path")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts or relative == "EVIDENCE_MANIFEST.sha256":
        raise SystemExit(f"FAIL unsafe manifest path: {relative!r}")
    rows.append((relative, match.group("digest")))
if not rows:
    raise SystemExit("FAIL empty evidence manifest")
paths = [relative for relative, _ in rows]
if len(paths) != len(set(paths)):
    raise SystemExit("FAIL duplicate evidence manifest path")
actual_files = {
    str(path.relative_to(ROOT))
    for path in ROOT.rglob("*")
    if path.is_file() and path.name != "EVIDENCE_MANIFEST.sha256"
}
if actual_files != set(paths):
    missing = sorted(set(paths) - actual_files)
    extra = sorted(actual_files - set(paths))
    raise SystemExit(f"FAIL manifest coverage: missing={missing}, extra={extra}")
for relative, expected in rows:
    source = ROOT / relative
    if not source.is_file() or source.is_symlink():
        raise SystemExit(f"FAIL missing {relative}")
    actual = hashlib.sha256(source.read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"FAIL hash mismatch {relative}")
print(f"PASS Phase-L AI reviewer bundle manifest ({len(rows)} files)")
'''.encode("utf-8")


REVIEW_ONLY_NOTICE = b'''# Confidential review-only notice

The author permits the designated reviewer to inspect these materials, run
the included verification commands, and make private working copies solely to
evaluate the mathematical candidate. Public distribution, republication, or
release is not authorized by this packet. This permission is not a claim that
third-party sources may be redistributed; those sources remain subject to
their own copyrights and licenses. The packet therefore supplies exact source
identifiers, consumed statements, official retrieval locations, and hashes
rather than unlicensed copies of third-party publications.

All review available in this package is AI review, not human or peer review.
'''


def git_output(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def candidate_bytes(relative: str) -> bytes:
    return git_output("show", f"{CANDIDATE_COMMIT}:{relative}")


def tracked_candidate_files() -> set[str]:
    output = git_output("ls-tree", "-r", "--name-only", CANDIDATE_COMMIT)
    return set(output.decode("utf-8").splitlines())


def candidate_history_bundle() -> bytes:
    """Create a deterministic complete-history bundle ending at the candidate."""
    with tempfile.TemporaryDirectory(prefix="phase-l-history-") as temporary:
        clone = Path(temporary) / "repository.git"
        bundle = Path(temporary) / "CANDIDATE_HISTORY.bundle"
        subprocess.run(
            ["git", "init", "--quiet", "--bare", str(clone)],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(clone),
                "fetch",
                "--quiet",
                "--no-tags",
                str(ROOT),
                f"{CANDIDATE_COMMIT}:refs/heads/phase-l-candidate",
            ],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(clone),
                "-c",
                "pack.threads=1",
                "repack",
                "-adf",
                "--window=0",
            ],
            check=True,
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(clone),
                "-c",
                "pack.threads=1",
                "bundle",
                "create",
                str(bundle),
                "phase-l-candidate",
            ],
            check=True,
        )
        subprocess.run(
            ["git", "bundle", "verify", str(bundle)], cwd=ROOT, check=True
        )
        return bundle.read_bytes()


def verify_history_script() -> bytes:
    return f'''#!/usr/bin/env python3
"""Verify the offline candidate history and checkpoint ancestry."""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BUNDLE = ROOT / "CANDIDATE_HISTORY.bundle"
CANDIDATE = "{CANDIDATE_COMMIT}"
CHECKPOINT = "{REQUIRED_CHECKPOINT}"
REF = "refs/heads/phase-l-candidate"

heads = subprocess.check_output(["git", "bundle", "list-heads", str(BUNDLE)], text=True)
if heads.strip() != f"{{CANDIDATE}} {{REF}}":
    raise SystemExit(f"FAIL unexpected bundle heads: {{heads!r}}")
with tempfile.TemporaryDirectory(prefix="phase-l-history-check-") as temporary:
    repo = Path(temporary) / "repository"
    subprocess.run(["git", "init", "--quiet", str(repo)], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "bundle", "verify", str(BUNDLE)], check=True
    )
    subprocess.run(
        ["git", "-C", str(repo), "fetch", "--quiet", str(BUNDLE), f"{{REF}}:{{REF}}"],
        check=True,
    )
    actual = subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", REF], text=True
    ).strip()
    if actual != CANDIDATE:
        raise SystemExit(f"FAIL candidate mismatch: {{actual}}")
    result = subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", CHECKPOINT, CANDIDATE]
    )
    if result.returncode != 0:
        raise SystemExit("FAIL required checkpoint is not in candidate history")
print("PASS offline candidate commit and required checkpoint ancestry")
'''.encode("utf-8")


def dynamic_files(tracked: set[str], prefixes: tuple[str, ...]) -> list[str]:
    return sorted(
        path
        for path in tracked
        if any(path.startswith(prefix) for prefix in prefixes)
        and "__pycache__" not in path
        and not path.endswith(".pyc")
    )


def archive_path(relative: str) -> str:
    if relative.startswith("output/pdf/"):
        return f"manuscript/{Path(relative).name}"
    if relative.startswith("paper/"):
        return f"manuscript/source/{relative.removeprefix('paper/')}"
    return f"evidence/{relative}"


def review_packet(role: str, spec: dict[str, object]) -> bytes:
    gates = "\n".join(f"- {gate}: PASS / FAIL / UNCHECKED" for gate in spec["gates"])
    return f"""# Phase L {spec['title']} adversarial AI review

Candidate proof-source commit: `{CANDIDATE_COMMIT}`
Required historical checkpoint: `{REQUIRED_CHECKPOINT}`
Classification: targeted correlated AI re-review; not human or peer review

## Re-review rules

This is a targeted re-review of a repaired freeze. You have reviewed the
earlier candidate, so do not call this pass independent or separated. Begin
again from the repaired manuscript, definitions, primary-source records, and
frozen proof/calculation sources in this packet. Verify the disposition of
every earlier P0/P1/P2 in your own track and try to find regressions or new
blockers. Do not consult another track or the author disposition.
Any independent-recalculation program you write must construct its inputs from
the definitions; it must not read a frozen repository result as expected data.
State the AI model/provider, tools, context access, conflicts, and whether you
have reviewed the earlier freeze. Call this a correlated re-review.

## Required method

Try to falsify each gate before accepting it. Check displayed equations and
quantifiers, not just prose. Distinguish exact proof, interval certificate,
finite-grid regression, formal adapter, and imported theorem. A verifier PASS
is evidence about its programmed predicate, not proof that the predicate is
the right theorem. Do not infer a human or peer-review status.

## Gate sheet

{gates}

## Required report format

1. Overall verdict: `R0`, `R1`, `R2`, or `R3`, with explicit release status.
2. Gate-by-gate table with evidence and recalculation method.
3. Numbered findings with severity `P0` (fatal), `P1` (theorem-affecting),
   `P2` (material but repairable/nonfatal), or `P3` (editorial/clarity).
4. Independent-recalculation record, including scripts and whether each reads
   any frozen expected result.
5. Unchecked-claims list; empty only if genuinely empty.
6. Earlier-finding disposition, release recommendation, and exact blockers.
7. Model/provider/tool disclosure and conflict/separation statement.
8. The sentence: `This is AI review, not human or peer review.`

Write one Markdown report and place independent scripts beside it. Do not edit
the candidate evidence. Run `python3 VERIFY_BUNDLE.py` before review.
""".encode("utf-8")


def start_here(role: str, spec: dict[str, object]) -> bytes:
    return f"""# Start here: Phase L {spec['title']} review

This archive freezes repaired candidate commit `{CANDIDATE_COMMIT}` for the
`{role}` targeted correlated re-review. Prior reports, the author disposition,
and every other track's result are not placed in the extracted review evidence.
The reproducibility/hostile history bundle necessarily retains the repository's
committed history and is supplied only to verify the candidate and checkpoint.
Read `REVIEW_PACKET.md`,
`REVIEW_ONLY_NOTICE.md`, and run `python3 VERIFY_BUNDLE.py` before review.
That command verifies the complete archive-local manifest; it does not install
Mathlib, Python, Tectonic, or Wolfram dependencies. Full replay uses the exact
private-repository commit. Reproducibility and hostile packets additionally
contain an offline Git history bundle and `VERIFY_HISTORY.py`. Confidential
working mathematics: do not publish. This is AI review, not human or peer
review.
""".encode("utf-8")


def metadata(role: str, spec: dict[str, object]) -> bytes:
    payload = {
        "artifact": f"Jensen Two-Thirds Phase L {spec['title']} AI Review Packet",
        "candidate_commit": CANDIDATE_COMMIT,
        "confidential": True,
        "date": "2026-08-17",
        "other_track_instructions_included": False,
        "prior_reports_included": False,
        "review_class": "targeted correlated AI re-review; not human or peer review",
        "review_track": role,
        "required_checkpoint": REQUIRED_CHECKPOINT,
    }
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


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
        if name in {"REVIEW_PACKET.md", "REVIEW_ONLY_NOTICE.md"}:
            continue
        if any(pattern.search(name) for pattern in BANNED_PATH_PATTERNS):
            raise ValueError(f"banned review-history path in {role} packet: {name}")
    for marker in (
        b"Review complete. Deliverables",
        b"Verdict: R0",
        b"ALGEBRAIC_REVIEW_REPORT",
        b"ANALYTIC_REVIEW_REPORT",
        b"PHASE24_ANALYTIC_REVIEW_FINDINGS",
    ):
        for name, data in entries.items():
            if name.endswith((".md", ".txt")) and marker in data:
                raise ValueError(f"prior-review marker {marker!r} leaked through {name}")
    packet = entries["REVIEW_PACKET.md"].decode("utf-8")
    if f"Phase L {ROLES[role]['title']} adversarial AI review" not in packet:
        raise ValueError(f"wrong review instructions in {role} packet")


def build_once(
    role: str,
    spec: dict[str, object],
    tracked: set[str],
    output: Path,
    root_name: str,
    history_bundle: bytes,
) -> None:
    selected = sorted(
        set(COMMON_FILES + list(spec["files"]) + dynamic_files(tracked, spec["dynamic"]))
    )
    missing = [relative for relative in selected if relative not in tracked]
    if missing:
        raise FileNotFoundError("candidate commit lacks:\n" + "\n".join(missing))
    entries = {archive_path(relative): candidate_bytes(relative) for relative in selected}
    entries["REVIEW_PACKET.md"] = review_packet(role, spec)
    entries["START_HERE.md"] = start_here(role, spec)
    entries["REVIEW_ONLY_NOTICE.md"] = REVIEW_ONLY_NOTICE
    entries["BUNDLE_METADATA.json"] = metadata(role, spec)
    entries["CANDIDATE_COMMIT.txt"] = (CANDIDATE_COMMIT + "\n").encode("ascii")
    entries["VERIFY_BUNDLE.py"] = VERIFY_BUNDLE
    if role in HISTORY_ROLES:
        entries["CANDIDATE_HISTORY.bundle"] = history_bundle
        entries["VERIFY_HISTORY.py"] = verify_history_script()
    check_separation(role, entries)
    entries["EVIDENCE_MANIFEST.sha256"] = manifest(entries)
    with zipfile.ZipFile(output, "w") as archive:
        for name, data in sorted(entries.items()):
            add_bytes(archive, f"{root_name}/{name}", data)


def verify_archive(path: Path, role: str) -> None:
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if names != sorted(names) or len(names) != len(set(names)):
            raise ValueError(f"noncanonical member order in {path.name}")
        if any(info.date_time != FIXED_TIMESTAMP for info in archive.infolist()):
            raise ValueError(f"noncanonical timestamp in {path.name}")
        prefix = f"{path.stem}/"
        if any(not name.startswith(prefix) for name in names):
            raise ValueError(f"archive root missing in {path.name}")
        stripped = {name.removeprefix(prefix): archive.read(name) for name in names}
        evidence = stripped.pop("EVIDENCE_MANIFEST.sha256")
        if evidence != manifest(stripped):
            raise ValueError(f"manifest mismatch in {path.name}")
        check_separation(role, stripped)
    with tempfile.TemporaryDirectory(prefix="phase-l-packet-") as temporary:
        with zipfile.ZipFile(path) as archive:
            archive.extractall(temporary)
        packet_root = Path(temporary) / path.stem
        subprocess.run(
            ["python3", "VERIFY_BUNDLE.py"],
            cwd=packet_root,
            check=True,
            stdout=subprocess.DEVNULL,
        )
        extra = packet_root / "UNMANIFESTED_EXTRA.txt"
        extra.write_text("manifest coverage mutation\n", encoding="utf-8")
        mutation = subprocess.run(
            ["python3", "VERIFY_BUNDLE.py"],
            cwd=packet_root,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if mutation.returncode == 0:
            raise ValueError(f"manifest verifier accepted an extra file in {path.name}")
        extra.unlink()
        manifest_path = packet_root / "EVIDENCE_MANIFEST.sha256"
        original_manifest = manifest_path.read_bytes()
        first_row = original_manifest.splitlines(keepends=True)[0]
        manifest_path.write_bytes(original_manifest + first_row)
        mutation = subprocess.run(
            ["python3", "VERIFY_BUNDLE.py"],
            cwd=packet_root,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if mutation.returncode == 0:
            raise ValueError(f"manifest verifier accepted a duplicate row in {path.name}")
        manifest_path.write_bytes(original_manifest)
        if role in HISTORY_ROLES:
            subprocess.run(
                ["python3", "VERIFY_HISTORY.py"],
                cwd=packet_root,
                check=True,
                stdout=subprocess.DEVNULL,
            )


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
    history_bundle = candidate_history_bundle()
    if history_bundle != candidate_history_bundle():
        raise ValueError("nondeterministic candidate history bundle")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    checksum_rows = []
    for role, spec in ROLES.items():
        filename = f"Jensen_Two_Thirds_Phase25_Repaired_{role.title()}_AI_Rereview_Packet.zip"
        output = OUTPUT_DIR / filename
        root_name = Path(filename).stem
        with tempfile.TemporaryDirectory(prefix="phase-l-rebuild-") as temporary:
            first = Path(temporary) / "first.zip"
            second = Path(temporary) / "second.zip"
            build_once(role, spec, tracked, first, root_name, history_bundle)
            build_once(role, spec, tracked, second, root_name, history_bundle)
            if first.read_bytes() != second.read_bytes():
                raise ValueError(f"nondeterministic rebuild for {role}")
            shutil.copyfile(first, output)
        verify_archive(output, role)
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
        checksum_rows.append(f"{digest}  {output.name}")
        print(f"PASS {role} targeted correlated deterministic packet: {output.relative_to(ROOT)}")
    checksum_path = OUTPUT_DIR / "SHA256SUMS.txt"
    checksum_path.write_text("\n".join(sorted(checksum_rows)) + "\n", encoding="utf-8")
    print(f"PASS external checksums: {checksum_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
