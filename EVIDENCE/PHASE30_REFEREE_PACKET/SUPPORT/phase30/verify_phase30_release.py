#!/usr/bin/env python3
"""Verify Phase-30 release checksums, contents, and audit reassembly."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "output/reviewer_packages_phase30"
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

    referee = OUTPUT / "Jensen_Two_Thirds_Phase30_Referee_Packet.zip"
    with zipfile.ZipFile(referee) as archive:
        stripped = {name.split("/", 1)[1] for name in archive.namelist()}
        required = {
            "PAPER/JENSEN_TWO_THIRDS_MAIN.pdf",
            "PAPER/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf",
            "PAPER/JENSEN_TWO_THIRDS_UNIFIED.pdf",
            "FORMAL/Phase30Axioms.lean",
            "FORMAL/PHASE30_AXIOM_AUDIT.txt",
            "FORMAL/THEOREM_MAP.md",
            "FORMAL/evidence/PHASE30_STATUS.md",
            "FORMAL/evidence/phase30_semantic_mutations.py",
            "FORMAL/evidence/phase30_adversarial_checks.py",
            "FORMAL/lean-project/Zeta23/Research/JensenWedge/XiNaturalMultiplierCertificate.lean",
            "COMPUTATION/mathematica/C48_Mathematica_CleanRoom_2.nb",
            "COMPUTATION/mathematica/C48_Mathematica_CleanRoom.pdf",
            "COMPUTATION/mathematica/C48_Mathematica_Result_Ledger.txt",
            "DISCLOSURE/TRUST_BOUNDARY.md",
            "DISCLOSURE/KNOWN_LIMITATIONS.md",
            "REVIEW/PHASE30_AI_ONLY_ADVERSARIAL_REVIEW.md",
            "VERIFY_BUNDLE.py",
            "VERIFY_ANCESTRY.py",
            "REPRODUCE/VERIFY_ARCHIVE.sh",
        }
        missing = required - stripped
        if missing:
            raise AssertionError(f"referee packet missing: {sorted(missing)}")
        with tempfile.TemporaryDirectory(prefix="phase30-referee-") as temp:
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
    print("PASS Phase-30 release checksums, contents, manifest, and audit reassembly")


if __name__ == "__main__":
    main()
