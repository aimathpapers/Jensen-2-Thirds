#!/usr/bin/env python3
"""Require the former unguarded MSS call to fail at a positivity argument."""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Kimi_Agent_Riemann Lean Exploration" / "zeta-23-lean"
MUTANT = Path(__file__).with_name("MSS_UNGUARDED_CALL.lean.mutant")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lean-dir", type=Path, default=LEAN)
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="phase33-mss-guard-") as temp:
        attack = Path(temp) / "MSSUnguardedCall.lean"
        attack.write_bytes(MUTANT.read_bytes())
        result = subprocess.run(
            ["lake", "env", "lean", str(attack)],
            cwd=args.lean_dir,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    if result.returncode == 0:
        raise SystemExit("unguarded MSS negative-endpoint attack compiled")
    required = (
        "Application type mismatch",
        "is expected to have type\n  0 < -(P + 1)",
    )
    missing = [needle for needle in required if needle not in result.stdout]
    if missing:
        raise SystemExit(
            "MSS attack failed for an unexpected reason; missing " + repr(missing)
        )
    print("PASS Phase 33 unguarded MSS negative-endpoint attack rejected")


if __name__ == "__main__":
    main()

