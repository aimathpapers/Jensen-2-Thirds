#!/usr/bin/env python3
"""Adversarial structural audit for the repaired Phase-L review packet.

This script tests the packet as evidence. It does not use a frozen mathematical
result as expected data: manifest fixtures are generated from fresh payloads,
the source/commit comparison uses the Git object database as the claimed
immutable source, and theorem locations are checked against the manuscript's
own numbered section/label structure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import zipfile
from pathlib import Path
from pathlib import PurePosixPath


def run(
    arguments: list[str],
    *,
    cwd: Path | None = None,
    check: bool = True,
    text: bool = True,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        arguments,
        cwd=cwd,
        check=check,
        text=text,
        capture_output=True,
    )


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest_rows(root: Path, names: list[str]) -> str:
    return "".join(
        f"{sha256((root / name).read_bytes())}  {name}\n" for name in names
    )


def exercise_manifest_failures(packet: Path) -> None:
    verifier = (packet / "VERIFY_BUNDLE.py").read_bytes()
    cases: list[tuple[str, str]] = [
        ("extra", "FAIL manifest coverage"),
        ("duplicate", "FAIL duplicate evidence manifest path"),
        ("traversal", "FAIL unsafe manifest path"),
        ("manifest_self", "FAIL unsafe manifest path"),
        ("hash", "FAIL hash mismatch payload.txt"),
        ("missing", "FAIL manifest coverage"),
        ("symlink", "FAIL missing payload.txt"),
        ("malformed", "FAIL malformed manifest row"),
        ("empty", "FAIL empty evidence manifest"),
    ]
    with tempfile.TemporaryDirectory(prefix="phase-l-manifest-mutations-") as raw:
        outer = Path(raw)
        outside = outer / "outside.txt"
        outside.write_bytes(b"outside symlink target\n")
        for name, expected in cases:
            fixture = outer / name
            fixture.mkdir()
            (fixture / "VERIFY_BUNDLE.py").write_bytes(verifier)
            (fixture / "payload.txt").write_bytes(b"fresh definition payload\n")
            baseline = manifest_rows(fixture, ["VERIFY_BUNDLE.py", "payload.txt"])
            manifest = fixture / "EVIDENCE_MANIFEST.sha256"
            manifest.write_text(baseline, encoding="utf-8")
            passed = run(["python3", "VERIFY_BUNDLE.py"], cwd=fixture)
            if "PASS Phase-L AI reviewer bundle manifest (2 files)" not in passed.stdout:
                raise AssertionError(f"synthetic baseline did not pass for {name}")

            if name == "extra":
                (fixture / "unmanifested.txt").write_text("extra\n", encoding="utf-8")
            elif name == "duplicate":
                manifest.write_text(
                    baseline + baseline.splitlines(keepends=True)[-1],
                    encoding="utf-8",
                )
            elif name == "traversal":
                manifest.write_text(
                    baseline + f"{'0' * 64}  ../escape\n", encoding="utf-8"
                )
            elif name == "manifest_self":
                manifest.write_text(
                    baseline + f"{'0' * 64}  EVIDENCE_MANIFEST.sha256\n",
                    encoding="utf-8",
                )
            elif name == "hash":
                (fixture / "payload.txt").write_bytes(b"mutated payload\n")
            elif name == "missing":
                (fixture / "payload.txt").unlink()
            elif name == "symlink":
                (fixture / "payload.txt").unlink()
                (fixture / "payload.txt").symlink_to(outside)
            elif name == "malformed":
                manifest.write_text("not a manifest row\n", encoding="utf-8")
            elif name == "empty":
                manifest.write_text("", encoding="utf-8")

            failed = run(
                ["python3", "VERIFY_BUNDLE.py"], cwd=fixture, check=False
            )
            combined = failed.stdout + failed.stderr
            if failed.returncode == 0 or expected not in combined:
                raise AssertionError(
                    f"manifest mutation {name!r} was not rejected as expected: "
                    f"returncode={failed.returncode}, output={combined!r}"
                )
    print(f"PASS manifest fail-closed suite: {len(cases)} generated mutations rejected")


def verify_zip_container(archive: Path, packet: Path) -> None:
    with zipfile.ZipFile(archive) as source:
        rows = source.infolist()
        names = [row.filename for row in rows]
        if len(names) != len(set(names)):
            raise AssertionError("ZIP contains duplicate member names")
        unsafe: list[str] = []
        symlinks: list[str] = []
        roots: set[str] = set()
        file_count = 0
        for row in rows:
            pure = PurePosixPath(row.filename)
            if pure.is_absolute() or ".." in pure.parts:
                unsafe.append(row.filename)
            if pure.parts:
                roots.add(pure.parts[0])
            mode = row.external_attr >> 16
            if stat.S_ISLNK(mode):
                symlinks.append(row.filename)
            if not row.is_dir():
                file_count += 1
        if unsafe or symlinks:
            raise AssertionError(f"unsafe ZIP members: traversal={unsafe}, symlinks={symlinks}")
        if roots != {packet.name}:
            raise AssertionError(f"ZIP top-level roots differ from extracted packet: {roots}")
        extracted_count = sum(1 for path in packet.rglob("*") if path.is_file())
        if file_count != extracted_count:
            raise AssertionError(
                f"ZIP/extraction file count mismatch: {file_count} != {extracted_count}"
            )
    print(
        f"PASS ZIP container safety: {file_count} unique files, one root, "
        "no traversal or symlink members"
    )


def git_bytes(repo: Path, revision: str, relative: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f"{revision}:{relative}"],
        check=True,
        capture_output=True,
    )
    return result.stdout


def verify_commit_connections(packet: Path, metadata: dict[str, object]) -> Path:
    candidate = str(metadata["candidate_commit"])
    checkpoint = str(metadata["required_checkpoint"])
    bundle = packet / "CANDIDATE_HISTORY.bundle"
    temporary = Path(tempfile.mkdtemp(prefix="phase-l-source-map-"))
    repo = temporary / "repository"
    run(["git", "init", "--quiet", str(repo)])
    run(
        [
            "git",
            "-C",
            str(repo),
            "fetch",
            "--quiet",
            str(bundle),
            "refs/heads/phase-l-candidate:refs/heads/phase-l-candidate",
        ]
    )
    actual = run(
        ["git", "-C", str(repo), "rev-parse", "refs/heads/phase-l-candidate"]
    ).stdout.strip()
    if actual != candidate:
        raise AssertionError(f"bundle source head {actual} != metadata {candidate}")
    ancestor = run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", checkpoint, candidate],
        check=False,
    )
    if ancestor.returncode != 0:
        raise AssertionError("required checkpoint is not an ancestor of candidate")

    compared = 0
    evidence = packet / "evidence"
    for path in sorted(item for item in evidence.rglob("*") if item.is_file()):
        relative = path.relative_to(evidence).as_posix()
        if path.read_bytes() != git_bytes(repo, candidate, relative):
            raise AssertionError(f"evidence differs from candidate Git object: {relative}")
        compared += 1

    mappings: list[tuple[Path, str]] = []
    for path in sorted((packet / "manuscript" / "source").iterdir()):
        if path.is_file():
            mappings.append((path, f"paper/{path.name}"))
    for name in (
        "JENSEN_TWO_THIRDS_MAIN.pdf",
        "JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf",
    ):
        mappings.append((packet / "manuscript" / name, f"output/pdf/{name}"))
    for path, relative in mappings:
        if path.read_bytes() != git_bytes(repo, candidate, relative):
            raise AssertionError(f"top-level manuscript differs from candidate: {relative}")
        compared += 1

    print(
        "PASS source-to-history connection: "
        f"{compared} packaged files byte-match candidate {candidate}"
    )
    return temporary


def verify_lean_closure(packet: Path) -> None:
    lean_project = (
        packet
        / "evidence"
        / "Kimi_Agent_Riemann Lean Exploration"
        / "zeta-23-lean"
    )
    lean_root = lean_project / "Zeta23"
    sources = sorted(lean_root.rglob("*.lean"))
    if not sources:
        raise AssertionError("no packaged Lean sources")
    missing: set[str] = set()
    import_count = 0
    for source in sources:
        source_text = source.read_text(encoding="utf-8")
        # Imports occur before declarations; removing block and line comments
        # prevents prose such as "import to Zeta23..." from becoming a module.
        source_text = re.sub(r"/-.*?-/", "", source_text, flags=re.DOTALL)
        for line in source_text.splitlines():
            line = line.split("--", maxsplit=1)[0]
            stripped = line.strip()
            if not stripped.startswith("import "):
                continue
            for module in stripped.removeprefix("import ").split():
                if module == "Zeta23":
                    required = lean_project / "Zeta23.lean"
                elif module.startswith("Zeta23."):
                    required = lean_project / (module.replace(".", "/") + ".lean")
                else:
                    continue
                import_count += 1
                if not required.is_file():
                    missing.add(module)
    if missing:
        raise AssertionError(f"missing packaged Lean import closure: {sorted(missing)}")

    headline = lean_root / "Research" / "JensenWedge.lean"
    if not headline.is_file():
        raise AssertionError("headline JensenWedge module is missing")
    escape = re.compile(r"^\s*(sorry|admit|axiom|unsafe)\b")
    escaped: list[str] = []
    for source in sorted((lean_root / "Research" / "JensenWedge").rglob("*.lean")):
        for number, line in enumerate(
            source.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if escape.search(line):
                escaped.append(f"{source.relative_to(lean_project)}:{number}")
    if escaped:
        raise AssertionError(f"Lean proof escapes found: {escaped}")
    print(
        "PASS Lean source closure: "
        f"{len(sources)} sources, {import_count} internal imports, no proof escapes"
    )


def verify_theorem_map_and_axioms(packet: Path) -> None:
    phase = packet / "evidence" / "ground_zero_work" / "phase25"
    matrix = json.loads((phase / "THEOREM_ASSURANCE_MATRIX.json").read_text())
    claims = matrix["claims"]
    if [claim["id"] for claim in claims] != [f"T{i}" for i in range(1, 19)]:
        raise AssertionError("theorem matrix is not ordered T1--T18")

    main = (
        packet / "manuscript" / "source" / "JENSEN_TWO_THIRDS_MAIN.tex"
    ).read_text(encoding="utf-8")
    section_rows = re.findall(
        r"\\section\{[^}]+\}\\label\{([^}]+)\}", main
    )
    numbered = {label: index for index, label in enumerate(section_rows, start=1)}
    expected_sections = {
        "T1": (4,),
        "T2": (5,),
        "T3": (6,),
        "T4": (7,),
        "T5": (7,),
        "T6": (8,),
        "T7": (9,),
        "T8": (10,),
        "T9": (11,),
        "T10": (12,),
        "T11": (12,),
        "T12": (12,),
        "T13": (13,),
        "T14": (14,),
        "T15": (15,),
        "T16": (16,),
        "T17": (16,),
        "T18": (1, 15, 16, 17),
    }
    label_sections = {
        "T1": ("sec:mellin",),
        "T2": ("sec:saddle",),
        "T3": ("sec:contour",),
        "T4": ("sec:coefficient",),
        "T5": ("sec:coefficient",),
        "T6": ("sec:derivatives",),
        "T7": ("sec:matches",),
        "T8": ("sec:cube",),
        "T9": ("sec:branch",),
        "T10": ("sec:finitefree",),
        "T11": ("sec:finitefree",),
        "T12": ("sec:finitefree",),
        "T13": ("sec:ode",),
        "T14": ("sec:radius",),
        "T15": ("sec:residual",),
        "T16": ("sec:assembly",),
        "T17": ("sec:assembly",),
        "T18": ("sec:introduction", "sec:residual", "sec:assembly", "sec:effectivity"),
    }
    for claim in claims:
        claim_id = claim["id"]
        actual_sections = tuple(numbered[label] for label in label_sections[claim_id])
        if actual_sections != expected_sections[claim_id]:
            raise AssertionError(
                f"{claim_id} source labels resolve to {actual_sections}, "
                f"expected {expected_sections[claim_id]}"
            )
        for section in expected_sections[claim_id]:
            source_description = claim["paper_source"]
            numbered_marker = any(
                marker in source_description
                for marker in (
                    f"Section {section}",
                    f"Lemma {section}.",
                    f"Theorem {section}.",
                )
            )
            if claim_id == "T18" and section in (15, 16, 17):
                numbered_marker = "Sections 15--17" in source_description
            if not numbered_marker:
                raise AssertionError(f"{claim_id} metadata omits mapped Section {section}")

    required_labels = ("lem:saddle", "thm:sector", "lem:sixmatch", "lem:stability", "thm:main")
    for label in required_labels:
        if f"\\label{{{label}}}" not in main:
            raise AssertionError(f"missing manuscript theorem label {label}")

    lean_root = (
        packet
        / "evidence"
        / "Kimi_Agent_Riemann Lean Exploration"
        / "zeta-23-lean"
        / "Zeta23"
    )
    lean_text = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(lean_root.rglob("*.lean"))
    )
    declarations: list[str] = []
    for claim in claims:
        channels = claim["channels"]
        names = claim["lean_declarations"]
        if bool(names) != ("lean_kernel" in channels):
            raise AssertionError(f"Lean channel/declaration mismatch for {claim['id']}")
        for qualified in names:
            prefix = "Zeta23.Research.JensenWedge."
            if not qualified.startswith(prefix):
                raise AssertionError(f"unscoped Lean declaration: {qualified}")
            short = qualified.removeprefix(prefix)
            if re.search(rf"\btheorem\s+{re.escape(short)}\b", lean_text) is None:
                raise AssertionError(f"mapped Lean theorem is absent: {qualified}")
            if qualified not in declarations:
                declarations.append(qualified)

    driver = re.findall(
        r"^#print axioms (\S+)$",
        (phase / "Phase25Axioms.lean").read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if driver != declarations:
        raise AssertionError("axiom driver does not exactly cover mapped declarations")
    output_text = (phase / "PHASE25_AXIOM_AUDIT.txt").read_text(encoding="utf-8")
    records = re.findall(
        r"'([^']+)' depends on axioms: \[(.*?)\]", output_text, re.DOTALL
    )
    if [name for name, _ in records] != declarations:
        raise AssertionError("axiom output does not exactly cover mapped declarations")
    accepted = {"propext", "Classical.choice", "Quot.sound"}
    for name, raw_axioms in records:
        axioms = {
            token.strip()
            for token in raw_axioms.replace("\n", " ").split(",")
            if token.strip()
        }
        if not axioms <= accepted:
            raise AssertionError(f"unexpected axiom for {name}: {sorted(axioms - accepted)}")
    print(
        "PASS theorem/axiom mapping: 18 claims, "
        f"{len(declarations)} declarations, exact accepted-axiom coverage"
    )


def verify_environment_and_disclosures(packet: Path) -> None:
    evidence = packet / "evidence"
    phase = evidence / "ground_zero_work" / "phase25"
    inventory = json.loads((phase / "ENVIRONMENT_INVENTORY.json").read_text())
    lock_rows = {}
    for line in (evidence / "requirements-c48.lock").read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        name, version = line.split("==", maxsplit=1)
        lock_rows[name.replace("-", "_")] = version
    for name in ("sympy", "mpmath", "python_flint"):
        if lock_rows.get(name) != inventory["python"][name]:
            raise AssertionError(f"Python lock/inventory mismatch for {name}")

    lean_project = evidence / "Kimi_Agent_Riemann Lean Exploration" / "zeta-23-lean"
    if (lean_project / "lean-toolchain").read_text().strip() != inventory["lean"]["toolchain"]:
        raise AssertionError("Lean toolchain/inventory mismatch")
    if inventory["lean"]["mathlib_commit"] not in (lean_project / "lakefile.toml").read_text():
        raise AssertionError("Mathlib commit is not pinned in lakefile.toml")

    classification = "targeted correlated AI re-review; not human or peer review"
    metadata = json.loads((packet / "BUNDLE_METADATA.json").read_text())
    if metadata["review_class"] != classification:
        raise AssertionError("top-level review classification drift")
    for relative in ("START_HERE.md", "REVIEW_PACKET.md", "REVIEW_ONLY_NOTICE.md"):
        text = " ".join((packet / relative).read_text(encoding="utf-8").split())
        if "not human or peer review" not in text:
            raise AssertionError(f"review disclosure missing from {relative}")
    notice = (packet / "REVIEW_ONLY_NOTICE.md").read_text(encoding="utf-8")
    for marker in ("review-only", "Public distribution", "third-party sources"):
        if marker not in notice:
            raise AssertionError(f"review-only notice omits {marker!r}")

    absolute_hits: list[str] = []
    for path in sorted(item for item in evidence.rglob("*") if item.is_file()):
        data = path.read_bytes()
        if b"/Users/" in data:
            absolute_hits.append(path.relative_to(evidence).as_posix())
    expected_notebook = (
        "ground_zero_work/phase24/mathematica_verification/"
        "C48_Mathematica_CleanRoom_2.nb"
    )
    if absolute_hits != [expected_notebook]:
        raise AssertionError(f"unexpected workstation-path surface: {absolute_hits}")
    print(
        "PASS environment/disclosures: exact version pins agree; correlated and "
        "review-only labels present; one inert frozen-notebook workstation path"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet", type=Path)
    parser.add_argument("--archive", type=Path)
    arguments = parser.parse_args()
    packet = arguments.packet.resolve()
    metadata = json.loads((packet / "BUNDLE_METADATA.json").read_text())

    if arguments.archive is not None:
        verify_zip_container(arguments.archive.resolve(), packet)

    for verifier in ("VERIFY_BUNDLE.py", "VERIFY_HISTORY.py"):
        completed = run(["python3", verifier], cwd=packet)
        print(completed.stdout.strip())
    exercise_manifest_failures(packet)
    temporary = verify_commit_connections(packet, metadata)
    try:
        verify_lean_closure(packet)
        verify_theorem_map_and_axioms(packet)
        verify_environment_and_disclosures(packet)
    finally:
        shutil.rmtree(temporary)
    print("PASS repaired Phase-L structural adversarial audit")


if __name__ == "__main__":
    main()
