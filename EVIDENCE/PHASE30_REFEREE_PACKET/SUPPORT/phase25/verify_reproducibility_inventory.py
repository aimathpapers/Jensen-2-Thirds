#!/usr/bin/env python3
"""Verify pinned tool versions, platform record, and Wolfram artifact hashes."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

import flint
import mpmath
import sympy


ROOT = Path(__file__).resolve().parents[2]
PHASE = ROOT / "ground_zero_work/phase25"
INVENTORY = PHASE / "ENVIRONMENT_INVENTORY.json"
LEAN_ROOT = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
MATHEMATICA = ROOT / "ground_zero_work/phase24/mathematica_verification"
WORKFLOW = ROOT / ".github/workflows/c48-linux-verification.yml"
PYTHON_LOCK = ROOT / "requirements-c48.lock"


def output(args: list[str], cwd: Path = ROOT) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    expected = json.loads(INVENTORY.read_text(encoding="utf-8"))
    actual_python = {
        "python": platform.python_version(),
        "sympy": sympy.__version__,
        "mpmath": mpmath.__version__,
        "python_flint": flint.__version__,
    }
    if actual_python != expected["python"]:
        raise AssertionError(f"Python environment drift: {actual_python}")

    # Use the Elan shim directly: ``lake env lean`` initializes an absent
    # package directory and would make this inventory-only gate require the
    # network in a clean audit-archive extraction.
    lean_version = output(["lean", "--version"], LEAN_ROOT)
    expected_lean_version, expected_lean_commit = expected["lean"]["version"].split()
    if expected_lean_version not in lean_version or expected_lean_commit not in lean_version:
        raise AssertionError(f"Lean version drift: {lean_version}")
    lake_version = output(["lake", "--version"], LEAN_ROOT)
    if expected["lean"]["lake"] not in lake_version:
        raise AssertionError(f"Lake version drift: {lake_version}")
    toolchain = (LEAN_ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
    if toolchain != expected["lean"]["toolchain"]:
        raise AssertionError(f"Lean toolchain drift: {toolchain}")
    lakefile = (LEAN_ROOT / "lakefile.toml").read_text(encoding="utf-8")
    if expected["lean"]["mathlib_commit"] not in lakefile:
        raise AssertionError("pinned Mathlib commit is absent from lakefile.toml")

    tectonic = output([os.environ.get("C48_TECTONIC", "tectonic"), "--version"])
    if expected["tectonic"] not in tectonic:
        raise AssertionError(f"Tectonic version drift: {tectonic}")
    git_version = output(["git", "--version"])
    match = re.search(r"(\d+\.\d+\.\d+)", git_version)
    if match is None or match.group(1) != expected["git"]:
        raise AssertionError(f"Git version drift: {git_version}")

    for name, digest in expected["mathematica"]["artifacts"].items():
        path = MATHEMATICA / name
        if not path.is_file() or sha256(path) != digest:
            raise AssertionError(f"Mathematica artifact drift: {name}")

    workflow = WORKFLOW.read_text(encoding="utf-8")
    hosted = expected["github_actions"]
    if f"runs-on: {hosted['runner']}" not in workflow:
        raise AssertionError("GitHub runner label drift")
    for key in ("checkout_action", "setup_python_action", "lean_action"):
        if f"uses: {hosted[key]}" not in workflow:
            raise AssertionError(f"mutable or drifted GitHub action: {key}")
    lock = PYTHON_LOCK.read_text(encoding="utf-8")
    for package in ("mpmath==1.3.0", "python-flint==0.6.0", "sympy==1.14.0"):
        if package not in lock:
            raise AssertionError(f"missing Python package pin: {package}")
    if lock.count("--hash=sha256:") < 6:
        raise AssertionError("Python artifacts are not hash pinned")

    checkpoint = expected["required_checkpoint"]
    subprocess.run(
        ["git", "merge-base", "--is-ancestor", checkpoint, "HEAD"],
        cwd=ROOT,
        check=True,
    )

    if os.environ.get("C48_ALLOW_DIFFERENT_PLATFORM") != "1":
        local = expected["local_platform"]
        if platform.machine() != local["architecture"]:
            raise AssertionError(f"architecture drift: {platform.machine()}")
        if platform.system() != "Darwin" or platform.release() != "24.4.0":
            raise AssertionError(
                f"kernel drift: {platform.system()} {platform.release()}"
            )

    if sys.version_info[:2] != (3, 11):
        raise AssertionError("verification requires Python 3.11")
    print(
        "PASS reproducibility inventory: platform/toolchain pins, Mathlib commit, "
        "Python artifact hashes, immutable CI actions, checkpoint ancestry, "
        "and Mathematica hashes"
    )


if __name__ == "__main__":
    main()
