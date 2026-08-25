#!/usr/bin/env python3
"""Validate the immutable ordering and honest baseline of Phase 26."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PHASE = ROOT / "ground_zero_work/phase26"
EXPECTED_ORDER = ["A", "B", "C", "D", "E", "F"]
REQUIRED = "5f79158f9c6276dd09142edeea279e35b0d58406"


def main() -> None:
    targets = json.loads((PHASE / "FORMAL_TARGETS.json").read_text())
    if targets["version"] != 1 or targets["order"] != EXPECTED_ORDER:
        raise AssertionError("Phase 26 stage order drifted")
    if targets["required_checkpoint"] != REQUIRED:
        raise AssertionError("required proof checkpoint drifted")
    stages = targets["stages"]
    if [stage["id"] for stage in stages] != EXPECTED_ORDER:
        raise AssertionError("stage records are not in approved order")
    statuses = [stage["status"] for stage in stages]
    if any(status not in {"complete", "in_progress", "pending"} for status in statuses):
        raise AssertionError("unknown Phase 26 stage status")
    if statuses.count("in_progress") > 1:
        raise AssertionError("Phase 26 has more than one active stage")
    if "in_progress" in statuses:
        active = statuses.index("in_progress")
        if any(status != "complete" for status in statuses[:active]):
            raise AssertionError("a stage before the active stage is incomplete")
        if any(status != "pending" for status in statuses[active + 1 :]):
            raise AssertionError("a later analytic stage was prematurely advanced")
    elif any(status != "complete" for status in statuses):
        raise AssertionError("Phase 26 has no active stage but is not complete")
    if any(not stage["closure"].strip() for stage in stages):
        raise AssertionError("a stage lacks a concrete closure condition")
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", REQUIRED, "HEAD"], cwd=ROOT
    )
    if result.returncode:
        raise AssertionError("required proof checkpoint is absent from history")
    status = (PHASE / "PHASE26_STATUS.md").read_text()
    for phrase in (
        "Stage B is complete and T1 is kernel closed",
        "Stage C is complete and T2 is kernel closed",
        "Stage D is complete and T3 is kernel closed",
        "Stage E is complete and T4 is",
        "complete at the approved stronger-middle endpoint",
        "The separate T5 endpoint substage now controls the low",
        "positive-integer factorial quotient is its traditional Holland",
        "complex-sector Gamma quotient used",
        "complex Gamma/Stirling subchain is complete",
        "final holomorphic coefficient assembly",
        "instantiation remains outside Phase 26",
        "No human or peer review is claimed",
    ):
        if phrase not in status:
            raise AssertionError(f"missing baseline disclosure: {phrase}")
    print("PASS Phase 26 plan order, checkpoint ancestry, and baseline disclosures")


if __name__ == "__main__":
    main()
