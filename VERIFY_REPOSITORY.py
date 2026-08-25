#!/usr/bin/env python3
"""Fail-closed integrity and privacy checks for the curated repository."""

from __future__ import annotations

import hashlib
import re
import stat
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


assert not (FORBIDDEN_TOP_LEVEL & {path.name for path in ROOT.iterdir()}), (
    "author-only top-level material is present"
)
current = repository_files()
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

required = {
    "README.md", "PROVENANCE.md", "CITATION.cff", "VERIFICATION_RECORD.md",
    "PAPERS/JENSEN_TWO_THIRDS_MAIN.pdf",
    "PAPER_SOURCE/JENSEN_TWO_THIRDS_MAIN.tex",
    "EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_ARTICLE.pdf",
    "EVIDENCE/CURRENT_STATUS/TRUST_BOUNDARY.md",
    "EVIDENCE/CURRENT_STATUS/MMP_SPECIALIZATION_SOURCE_AUDIT.md",
    "EVIDENCE/PHASE32_REFEREE_PACKET/FORMAL/lean-project/lean-toolchain",
    "EVIDENCE/PHASE32_REFEREE_PACKET/FORMAL/Phase32Axioms.lean",
    "EVIDENCE/PHASE32_REFEREE_PACKET/COMPUTATION/mathematica/C48_Mathematica_CleanRoom_2.nb",
    "REVIEWER_PACKET/Jensen_Two_Thirds_Reviewer_Packet_v1.0.zip",
}
assert required <= set(current), f"missing required files: {sorted(required-set(current))}"
print(
    f"PASS curated repository: {len(current)} files, complete manifest, "
    "allowed hidden paths only, no credential signature, clean reviewer ZIP"
)
