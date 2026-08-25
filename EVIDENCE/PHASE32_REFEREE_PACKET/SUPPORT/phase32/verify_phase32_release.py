#!/usr/bin/env python3
"""Verify Phase-32 release checksums, contents, and audit reassembly."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output/reviewer_packages_phase32"
ROW = re.compile(r"^(?P<digest>[0-9a-f]{64})  (?P<name>.+)$")


def main() -> None:
    names: list[str] = []
    for line in (OUTPUT / "SHA256SUMS.txt").read_text(encoding="utf-8").splitlines():
        match = ROW.fullmatch(line)
        if match is None:
            raise AssertionError(f"malformed checksum row: {line!r}")
        path = OUTPUT / match.group("name")
        if not path.is_file():
            raise AssertionError(f"missing release file: {path.name}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != match.group("digest"):
            raise AssertionError(f"checksum mismatch: {path.name}")
        names.append(path.name)
    if len(names) < 2 or len(names) != len(set(names)):
        raise AssertionError("incomplete or duplicate checksum inventory")

    referee = OUTPUT / "Jensen_Two_Thirds_Phase32_Referee_Packet.zip"
    with zipfile.ZipFile(referee) as archive:
        stripped = {name.split("/", 1)[1] for name in archive.namelist()}
        required = {
            "PAPER/JENSEN_TWO_THIRDS_MAIN.pdf",
            "PAPER/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf",
            "PAPER/JENSEN_TWO_THIRDS_UNIFIED.pdf",
            "FORMAL/Phase32Axioms.lean",
            "FORMAL/PHASE32_AXIOM_AUDIT.txt",
            "FORMAL/THEOREM_MAP.md",
            "FORMAL/evidence/PHASE32_STATUS.md",
            "FORMAL/evidence/MMP_SPECIALIZATION_SOURCE_AUDIT.md",
            "FORMAL/evidence/phase32_mmp_checks.py",
            "FORMAL/lean-project/Zeta23/Research/JensenWedge/FiniteFreeAdapters.lean",
            "FORMAL/lean-project/Zeta23/Research/JensenWedge/XiNaturalFiniteFreeSpecialization.lean",
            "COMPUTATION/mathematica/C48_Mathematica_CleanRoom_2.nb",
            "DISCLOSURE/TRUST_BOUNDARY.md",
            "START_HERE.md",
            "VERIFY_BUNDLE.py",
            "VERIFY_ANCESTRY.py",
            "REPRODUCE/VERIFY_ARCHIVE.sh",
        }
        missing = required - stripped
        if missing:
            raise AssertionError(f"referee packet missing: {sorted(missing)}")
        prefix = archive.namelist()[0].split("/", 1)[0]
        bibliography = archive.read(f"{prefix}/PAPER/source/references.bib")
        if b"Holland, Jonathan" not in bibliography or b"Holland, Jensen" in bibliography:
            raise AssertionError("Holland attribution correction absent from packet")
        adapter = archive.read(
            f"{prefix}/FORMAL/lean-project/Zeta23/Research/JensenWedge/FiniteFreeAdapters.lean"
        )
        if b"structure MMPFiniteFreeLogMeshInput" not in adapter:
            raise AssertionError("factor-level MMP interface absent from packet")
        if b"structure MMPLogMeshInput" in adapter:
            raise AssertionError("obsolete final-comparison MMP interface in packet")
        with tempfile.TemporaryDirectory(prefix="phase32-referee-") as temp:
            archive.extractall(temp)
            roots = [path for path in Path(temp).iterdir() if path.is_dir()]
            if len(roots) != 1:
                raise AssertionError("unexpected referee archive root layout")
            subprocess.run(["python3", str(roots[0] / "VERIFY_BUNDLE.py")], check=True)
            metadata = json.loads((roots[0] / "RELEASE_METADATA.json").read_text())
            if metadata["typed_external_inputs"] != ["Jacobi", "MMP", "MSS"]:
                raise AssertionError("release metadata literature boundary drift")

    reassembly = json.loads((OUTPUT / "FULL_AUDIT_REASSEMBLY.json").read_text())
    payload = b"".join((OUTPUT / part["name"]).read_bytes() for part in reassembly["parts"])
    if len(payload) != reassembly["bytes"]:
        raise AssertionError("reassembled byte count mismatch")
    if hashlib.sha256(payload).hexdigest() != reassembly["sha256"]:
        raise AssertionError("reassembled archive digest mismatch")
    print("PASS Phase-32 release checksums, contents, manifest, and audit reassembly")


if __name__ == "__main__":
    main()
