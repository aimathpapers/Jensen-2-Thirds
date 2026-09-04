#!/usr/bin/env python3
"""Fail-closed integrity and privacy checks for the curated repository."""

from __future__ import annotations

import hashlib
import json
import re
import stat
import sys
import zipfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "REPOSITORY_MANIFEST.sha256"
EXCLUDED = {"REPOSITORY_MANIFEST.sha256"}
FORBIDDEN_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", ".env", ".envrc"}
FORBIDDEN_SUFFIXES = {".key", ".p12", ".pem", ".sqlite", ".pyc"}
FORBIDDEN_TOP_LEVEL = {
    "LAUNCH", "PUBLIC", "PREPUBLIC_CHECKLIST.md", "PUBLICATION_AUDIT.json",
    "PUBLICATION_NOTICE.md", "README_FIRST.md", "SOURCE_ARCHIVE.sha256",
}
SECRET_PATTERNS = {
    "private-key": re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "aws-access-key": re.compile(rb"\bAKIA[0-9A-Z]{16}\b"),
    "openai-key": re.compile(rb"\bsk-[A-Za-z0-9_-]{24,}\b"),
    "slack-token": re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
}
EMAIL_PATTERN = re.compile(rb"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
TEXT_SUFFIXES = {
    "", ".bib", ".cff", ".cfg", ".csv", ".html", ".json", ".lean",
    ".lock", ".md", ".nb", ".py", ".sh", ".tex", ".toml", ".txt",
    ".yaml", ".yml",
}


def sha(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def allowed_hidden(relative: Path) -> bool:
    for index, part in enumerate(relative.parts):
        if not part.startswith("."):
            continue
        if part == ".gitignore":
            continue
        if index == 0 and part == ".github":
            continue
        return False
    return True


def repository_files() -> dict[str, Path]:
    result = {}
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if ".git" in relative.parts or path.is_dir() or relative.as_posix() in EXCLUDED:
            continue
        assert not path.is_symlink(), f"symlink is forbidden: {relative}"
        assert allowed_hidden(relative), f"unexpected hidden path: {relative}"
        assert path.name not in FORBIDDEN_NAMES, f"forbidden file: {relative}"
        assert path.suffix.lower() not in FORBIDDEN_SUFFIXES, f"forbidden type: {relative}"
        result[relative.as_posix()] = path
    return result


def verify_zip(path: Path, reviewer: bool = False) -> None:
    with zipfile.ZipFile(path) as archive:
        names = set()
        for info in archive.infolist():
            member = PurePosixPath(info.filename)
            assert info.filename not in names, f"duplicate ZIP member: {path}:{info.filename}"
            names.add(info.filename)
            assert not member.is_absolute() and ".." not in member.parts
            assert (info.external_attr >> 16) & 0o170000 != stat.S_IFLNK
            if reviewer:
                upper = {part.upper() for part in member.parts}
                assert not ({"SUBMISSION", "LAUNCH", "GHOST"} & upper), (
                    f"author-only reviewer member: {info.filename}"
                )
        if reviewer:
            prefixes = {PurePosixPath(name).parts[0] for name in names}
            assert len(prefixes) == 1, "reviewer ZIP must have one root directory"
            prefix = next(iter(prefixes))
            manifest_name = f"{prefix}/MANIFEST.sha256"
            assert manifest_name in names, "reviewer ZIP lacks internal manifest"
            declared = {}
            for line in archive.read(manifest_name).decode("utf-8").splitlines():
                digest, relative = line.split("  ", 1)
                assert len(digest) == 64 and relative not in declared
                declared[relative] = digest
            actual = {
                "/".join(PurePosixPath(name).parts[1:])
                for name in names
                if name != manifest_name and not name.endswith("/")
            }
            assert actual == set(declared), "reviewer ZIP manifest coverage mismatch"
            for relative, expected in declared.items():
                payload = archive.read(f"{prefix}/{relative}")
                assert hashlib.sha256(payload).hexdigest() == expected, (
                    f"reviewer ZIP digest mismatch: {relative}"
                )
            binding_name = f"{prefix}/SOURCE_TREE_BINDING.json"
            assert binding_name in names, "reviewer ZIP lacks source-tree binding"
            binding = json.loads(archive.read(binding_name))
            metadata = json.loads(archive.read(f"{prefix}/RELEASE_METADATA.json"))
            ancestry = json.loads(archive.read(f"{prefix}/ANCESTRY_PROOF.json"))
            candidate = binding["candidate_commit"]
            assert candidate == metadata["candidate_commit"] == ancestry["candidate"], (
                "reviewer ZIP candidate identity drift"
            )
            rows = binding["packet_entries"]
            row_paths = {row["packet_path"] for row in rows}
            assert len(row_paths) == len(rows), "duplicate source-binding path"
            assert row_paths == actual - {"SOURCE_TREE_BINDING.json"}, (
                "reviewer ZIP source-binding coverage mismatch"
            )
            for row in rows:
                payload = archive.read(f"{prefix}/{row['packet_path']}")
                assert hashlib.sha256(payload).hexdigest() == row["sha256"], (
                    f"reviewer ZIP source-binding digest mismatch: {row['packet_path']}"
                )
            assert not any("PALOMAR_PUBLICATION_AND_SUBMISSION_GUIDE" in name for name in names), (
                "author-facing Palomar guide remains in reviewer ZIP"
            )
            explainer = archive.read(
                f"{prefix}/PUBLIC/JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md"
            )
            assert b"Jonathan Holland" in explainer and b"by James Holland" not in explainer, (
                "reviewer ZIP retains an incorrect Holland attribution"
            )


assert not (FORBIDDEN_TOP_LEVEL & {path.name for path in ROOT.iterdir()}), (
    "author-only top-level material is present"
)
current = repository_files()
if sys.argv[1:]:
    assert sys.argv[1:] == ["--write-manifest"], "unknown verifier option"
    lines = [f"{sha(path)}  {name}\n" for name, path in sorted(current.items())]
    MANIFEST.write_text("".join(lines), encoding="utf-8")
    print(f"WROTE repository manifest for {len(current)} files")
    raise SystemExit(0)

declared = {}
for line in MANIFEST.read_text(encoding="utf-8").splitlines():
    digest, name = line.split("  ", 1)
    assert len(digest) == 64 and name not in declared
    declared[name] = digest
assert set(current) == set(declared), "repository manifest coverage mismatch"

for name, path in current.items():
    assert sha(path) == declared[name], f"digest mismatch: {name}"
    payload = path.read_bytes()
    for label, pattern in SECRET_PATTERNS.items():
        assert not pattern.search(payload), f"{label} pattern in {name}"
    if path.suffix.lower() in TEXT_SUFFIXES:
        assert not EMAIL_PATTERN.search(payload), f"email address in {name}"
    if path.suffix.lower() == ".pdf":
        assert payload.startswith(b"%PDF-"), f"invalid PDF header: {name}"
        assert b"%%EOF" in payload[-2048:], f"invalid PDF terminator: {name}"
    if path.suffix.lower() == ".zip":
        verify_zip(path, reviewer=name.startswith("REVIEWER_PACKET/"))

metadata = json.loads((ROOT / "RELEASE_METADATA.json").read_text())
binding = json.loads((ROOT / "PUBLIC_RELEASE_BINDING.json").read_text())
expected_candidate = "46774668e7d0acbe58030228ee12e2d861370116"
expected_tree = "d3a1e7690c8c2c5bd34be440f936834ea90e7563"
expected_packet = "aa21e34eea6f37490eb7119f9c1f98e8459c06bf3fbd2bc277d2b39ef5f58dfc"
expected_public_zip = "a15d0de579f8a4b0d885c1205e6f9b4834bab767ff664ede673cdcc48bd3dd02"
expected_magazine_v1_0 = "a553cb2a64c259cf77deeebc18cbb4e2dc82031fe4fa69ce240d508d9309dc35"
expected_magazine_v1_1 = "60e31e549f9b00a536300048dfd115f5ef5dec71893359b19849bd937ec94c76"
assert metadata["version"] == "1.1"
assert metadata["primary_ai_assistance"] == "OpenAI GPT-5.6 Sol Pro"
assert binding["public_release_version"] == "1.1"

active_disclosures = (
    "README.md",
    "PROVENANCE.md",
    "CITATION.cff",
    "VERIFICATION_RECORD.md",
    "PAPER_SOURCE/JENSEN_TWO_THIRDS_MAIN.tex",
    "PAPER_SOURCE/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex",
    "PAPER_SOURCE/JENSEN_TWO_THIRDS_UNIFIED.tex",
    "EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_FRONT_MATTER.md",
)
for name in active_disclosures:
    normalized = " ".join((ROOT / name).read_text(encoding="utf-8").split())
    assert "OpenAI GPT-5.6 Sol Pro" in normalized, f"primary AI disclosure absent: {name}"
    assert "OpenRouter" not in normalized and "Oh My Pi" not in normalized, (
        f"removed platform detail remains in active disclosure: {name}"
    )

assert metadata["source_candidate_commit"] == expected_candidate
assert binding["private_source_candidate_commit"] == expected_candidate
assert binding["private_source_candidate_tree"] == expected_tree
assert metadata["original_phase33_referee_packet_sha256"] == expected_packet
assert binding["original_phase33_referee_packet_sha256"] == expected_packet
assert metadata["public_reviewer_packet_sha256"] == expected_public_zip
assert binding["public_reviewer_packet_sha256"] == expected_public_zip
assert sha(ROOT / "REVIEWER_PACKET/Jensen_Two_Thirds_Reviewer_Packet_v1.0.zip") == expected_public_zip
assert sha(ROOT / "EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_ARTICLE_V1.0.pdf") == expected_magazine_v1_0
assert sha(ROOT / "EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_ARTICLE.pdf") == expected_magazine_v1_1
explainer = (
    ROOT
    / "EVIDENCE/PHASE33_REFEREE_PACKET/PUBLIC/JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md"
).read_bytes()
assert b"Jonathan Holland" in explainer and b"by James Holland" not in explainer

required = {
    "README.md", "PROVENANCE.md", "CITATION.cff", "VERIFICATION_RECORD.md",
    "PAPERS/JENSEN_TWO_THIRDS_MAIN.pdf",
    "PAPERS/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf",
    "PAPERS/JENSEN_TWO_THIRDS_READERS_SYNOPSIS.pdf",
    "PAPER_SOURCE/JENSEN_TWO_THIRDS_MAIN.tex",
    "PAPER_SOURCE/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex",
    "PAPER_SOURCE/JENSEN_TWO_THIRDS_UNIFIED.tex",
    "EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_ARTICLE.pdf",
    "EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_ARTICLE_V1.0.pdf",
    "EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_FRONT_MATTER.md",
    "EXPOSITORY/merge_pdf_cover.swift",
    "EVIDENCE/CURRENT_STATUS/TRUST_BOUNDARY.md",
    "EVIDENCE/CURRENT_STATUS/MMP_SPECIALIZATION_SOURCE_AUDIT.md",
    "PUBLIC_RELEASE_BINDING.json",
    "EVIDENCE/CURRENT_STATUS/PHASE33_STATUS.md",
    "EVIDENCE/CURRENT_STATUS/PHASE33_REPAIR_DISPOSITION.md",
    "EVIDENCE/PHASE33_REFEREE_PACKET/SOURCE_TREE_BINDING.json",
    "EVIDENCE/PHASE33_REFEREE_PACKET/FORMAL/lean-project/lean-toolchain",
    "EVIDENCE/PHASE33_REFEREE_PACKET/FORMAL/Phase33Axioms.lean",
    "EVIDENCE/PHASE33_REFEREE_PACKET/COMPUTATION/mathematica/C48_Mathematica_CleanRoom_2.nb",
    "REVIEWER_PACKET/Jensen_Two_Thirds_Reviewer_Packet_v1.0.zip",
}
assert required <= set(current), f"missing required files: {sorted(required-set(current))}"
print(
    f"PASS curated Phase 33 repository: {len(current)} files, complete manifest, "
    "source bindings, allowed hidden paths, no credential signature, clean reviewer ZIP"
)
