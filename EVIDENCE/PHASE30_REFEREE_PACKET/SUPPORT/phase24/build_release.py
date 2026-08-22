#!/usr/bin/env python3
"""Build the deterministic local Phase-24 release directory and ZIP."""

from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/release"
TREE = OUT / "Jensen_Two_Thirds_Phase24"
ZIP_PATH = OUT / "Jensen_Two_Thirds_Phase24.zip"
PDF = ROOT / "output/pdf/JENSEN_TWO_THIRDS_UNIFIED.pdf"
LEAN_ROOT = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
PHASES = (9, 11, 14, 15, 16, 17, 18, 20, 21, 23, 24)
SOURCE_COMMIT = "d71b3d683e67296fd15e41d013a444df5fe2ec5f"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def allowed(path: Path) -> bool:
    parts = set(path.parts)
    if parts & {"__pycache__", ".lake", ".venv", ".git", "tmp"}:
        return False
    return path.is_file() and path.suffix != ".pyc" and path.name != ".DS_Store"


def collect() -> list[tuple[Path, Path]]:
    rows: list[tuple[Path, Path]] = []
    for phase in PHASES:
        base = ROOT / f"ground_zero_work/phase{phase}"
        for path in sorted(base.rglob("*")):
            if allowed(path):
                rows.append((path, path.relative_to(ROOT)))
    symbolic = ROOT / "ground_zero_work/c48_jensen"
    if symbolic.is_dir():
        for path in sorted(symbolic.rglob("*")):
            if allowed(path):
                rows.append((path, path.relative_to(ROOT)))
    for path in sorted((LEAN_ROOT / "Zeta23").rglob("*.lean")):
        rows.append((path, path.relative_to(ROOT)))
    for name in ("lakefile.lean", "lake-manifest.json", "lean-toolchain", "README.md"):
        path = LEAN_ROOT / name
        if path.is_file():
            rows.append((path, path.relative_to(ROOT)))
    for pattern in ("requirements*.txt", "requirements*.lock", "pyproject.toml", "uv.lock"):
        for path in sorted(ROOT.glob(pattern)):
            if path.is_file():
                rows.append((path, path.relative_to(ROOT)))
    rows.append((PDF, Path("manuscript/JENSEN_TWO_THIRDS_UNIFIED.pdf")))
    tex = ROOT / "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex"
    rows.append((tex, Path("manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex")))
    unique: dict[str, tuple[Path, Path]] = {}
    for source, relative in rows:
        unique[relative.as_posix()] = (source, relative)
    return [unique[key] for key in sorted(unique)]


def write_zip() -> None:
    if not PDF.is_file():
        raise SystemExit("missing rendered manuscript PDF")
    if TREE.exists():
        shutil.rmtree(TREE)
    TREE.mkdir(parents=True)
    for source, relative in collect():
        target = TREE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    metadata = {
        "artifact": "Jensen Two-Thirds Phase 24 Mathematica-verified candidate",
        "date": "2026-08-17",
        "source_commit": SOURCE_COMMIT,
        "review_status": (
            "separated analytic and algebraic AI pre-review completed; "
            "user-executed Mathematica M1-M4 exact matches; "
            "not human or peer review"
        ),
        "publication_status": (
            "confidential artifact in a private repository; not publicly published"
        ),
        "required_checkpoint": "5f79158f9c6276dd09142edeea279e35b0d58406",
    }
    (TREE / "RELEASE_METADATA.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    manifest = []
    for path in sorted(TREE.rglob("*")):
        if path.is_file() and path.name != "RELEASE_MANIFEST.sha256":
            manifest.append(f"{sha256(path)}  {path.relative_to(TREE).as_posix()}")
    (TREE / "RELEASE_MANIFEST.sha256").write_text(
        "\n".join(manifest) + "\n", encoding="utf-8"
    )

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(TREE.rglob("*")):
            if not path.is_file():
                continue
            arcname = (Path(TREE.name) / path.relative_to(TREE)).as_posix()
            info = zipfile.ZipInfo(arcname, date_time=(2026, 8, 17, 12, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            zf.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

    external_manifest = OUT / "RELEASE_MANIFEST.sha256"
    shutil.copyfile(TREE / "RELEASE_MANIFEST.sha256", external_manifest)
    checksums = {
        ZIP_PATH.name: sha256(ZIP_PATH),
        PDF.name: sha256(PDF),
        "RELEASE_MANIFEST.sha256": sha256(external_manifest),
    }
    (OUT / "SHA256SUMS.json").write_text(
        json.dumps(checksums, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    shutil.rmtree(TREE)
    print(f"PASS built {ZIP_PATH.relative_to(ROOT)} with {len(manifest)} manifest entries")


if __name__ == "__main__":
    write_zip()
