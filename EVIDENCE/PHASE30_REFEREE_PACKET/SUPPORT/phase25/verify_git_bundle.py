#!/usr/bin/env python3
"""Create two deterministic Git bundles and verify a clean reconstruction."""

from __future__ import annotations

import hashlib
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT = "5f79158f9c6276dd09142edeea279e35b0d58406"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args: list[str], cwd: Path = ROOT) -> None:
    subprocess.run(args, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> None:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    with tempfile.TemporaryDirectory(prefix="c48-git-bundle-") as raw:
        tmp = Path(raw)
        first = tmp / "c48-first.bundle"
        second = tmp / "c48-second.bundle"
        # Multithreaded delta search may choose different, equally valid pack
        # representations. A single pack thread makes the release container
        # byte reproducible.
        bundle_prefix = ["git", "-c", "pack.threads=1", "bundle", "create"]
        run([*bundle_prefix, str(first), "HEAD"])
        run([*bundle_prefix, str(second), "HEAD"])
        if sha256(first) != sha256(second):
            raise AssertionError("repeated Git bundles are not byte-identical")
        run(["git", "bundle", "verify", str(first)])
        clone = tmp / "clone"
        run(["git", "clone", "--quiet", str(first), str(clone)])
        clone_head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=clone, text=True
        ).strip()
        if clone_head != head:
            raise AssertionError(f"bundle reconstructed {clone_head}, expected {head}")
        run(["git", "merge-base", "--is-ancestor", CHECKPOINT, "HEAD"], clone)
        for forbidden in (".lake", ".venv", "AGENTS.md"):
            if any(path.name == forbidden for path in clone.rglob(forbidden)):
                raise AssertionError(f"bundle clone contains forbidden {forbidden}")
        print(
            "PASS deterministic Git bundle: two byte-identical builds, exact HEAD, "
            "required-checkpoint ancestry, and clean reconstruction"
        )


if __name__ == "__main__":
    main()
