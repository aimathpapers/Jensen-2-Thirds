#!/usr/bin/env python3
"""Verify Phase-33 release checksums, contents, binding, and audit reassembly."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output/reviewer_packages_phase33"
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

    referee = OUTPUT / "Jensen_Two_Thirds_Phase33_Referee_Packet.zip"
    with zipfile.ZipFile(referee) as archive:
        root = archive.namelist()[0].split("/", 1)[0]
        stripped = {name.split("/", 1)[1] for name in archive.namelist()}
        required = {
            "PAPER/JENSEN_TWO_THIRDS_MAIN.pdf",
            "PAPER/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf",
            "PAPER/JENSEN_TWO_THIRDS_UNIFIED.pdf",
            "FORMAL/Phase33Axioms.lean",
            "FORMAL/PHASE33_AXIOM_AUDIT.txt",
            "FORMAL/THEOREM_MAP.md",
            "FORMAL/evidence/PHASE33_STATUS.md",
            "FORMAL/evidence/MMP_SPECIALIZATION_SOURCE_AUDIT.md",
            "FORMAL/lean-project/Zeta23/Research/JensenWedge/XiNaturalFiniteFreeSpecialization.lean",
            "FORMAL/lean-project/Zeta23/Research/JensenWedge/XiNaturalMultiplierCertificate.lean",
            "COMPUTATION/mathematica/C48_Mathematica_CleanRoom_2.nb",
            "REVIEW/PHASE32_FRESH_AI_REVIEW_FINDINGS.md",
            "REVIEW/PHASE33_REPAIR_DISPOSITION.md",
            "SOURCE_TREE_BINDING.json",
            "VERIFY_SOURCE_BINDING.py",
            "START_HERE.md",
            "VERIFY_BUNDLE.py",
            "VERIFY_ANCESTRY.py",
            "REPRODUCE/VERIFY_ARCHIVE.sh",
            "DISCLOSURE/TRUST_BOUNDARY.md",
            "PUBLIC/JENSEN_TWO_THIRDS_GHOST_POST.md",
        }
        missing = required - stripped
        if missing:
            raise AssertionError(f"referee packet missing: {sorted(missing)}")
        boundary = archive.read(f"{root}/DISCLOSURE/TRUST_BOUNDARY.md")
        for needle in (
            b"# Phase 33 trust boundary",
            b"riemannXiJensen_twoThirds_global_headline_exactly",
            b"strictly positive",
        ):
            if needle not in boundary:
                raise AssertionError(f"current trust boundary absent: {needle!r}")
        ghost = archive.read(f"{root}/PUBLIC/JENSEN_TWO_THIRDS_GHOST_POST.md")
        if b"Jonathan Holland" not in ghost or b"James Holland" in ghost:
            raise AssertionError("packaged magazine source attribution incorrect")
        bibliography = archive.read(f"{root}/PAPER/source/references.bib")
        if b"Holland, Jonathan" not in bibliography or b"Morales, Rafael" not in bibliography:
            raise AssertionError("corrected bibliography absent from packet")
        specialization = archive.read(
            f"{root}/FORMAL/lean-project/Zeta23/Research/JensenWedge/"
            "XiNaturalFiniteFreeSpecialization.lean"
        )
        for guard in (b"0 < uLower", b"0 < vLower", b"exact hBLower", b"exact hDLower"):
            if guard not in specialization:
                raise AssertionError(f"guarded MSS interface absent: {guard!r}")
        certificate = archive.read(
            f"{root}/FORMAL/lean-project/Zeta23/Research/JensenWedge/"
            "XiNaturalMultiplierCertificate.lean"
        )
        if b"riemannXiJensen_twoThirds_global_headline_exactly" not in certificate:
            raise AssertionError("global exact headline absent")
        metadata = json.loads(archive.read(f"{root}/RELEASE_METADATA.json"))
        if metadata["typed_external_inputs"] != ["Jacobi", "MMP", "MSS"]:
            raise AssertionError("release metadata literature boundary drift")
        binding = json.loads(archive.read(f"{root}/SOURCE_TREE_BINDING.json"))
        if binding["candidate_commit"] != metadata["candidate_commit"]:
            raise AssertionError("source binding candidate drift")
        with tempfile.TemporaryDirectory(prefix="phase33-referee-") as temporary:
            archive.extractall(temporary)
            packet = Path(temporary) / root
            subprocess.run(["python3", "VERIFY_BUNDLE.py"], cwd=packet, check=True)
            subprocess.run(["python3", "VERIFY_SOURCE_BINDING.py"], cwd=packet, check=True)

    reassembly = json.loads((OUTPUT / "FULL_AUDIT_REASSEMBLY.json").read_text())
    payload = b"".join((OUTPUT / part["name"]).read_bytes() for part in reassembly["parts"])
    if len(payload) != reassembly["bytes"]:
        raise AssertionError("reassembled byte count mismatch")
    if hashlib.sha256(payload).hexdigest() != reassembly["sha256"]:
        raise AssertionError("reassembled archive digest mismatch")
    print("PASS Phase-33 release checksums, contents, binding, and audit reassembly")


if __name__ == "__main__":
    main()

