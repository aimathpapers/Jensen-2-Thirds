#!/usr/bin/env python3
"""Run Phase 24, 21, and 20 verifiers serially while freezing full logs."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "ground_zero_work/phase24/verification_logs"


def run(name: str, command: list[str], extra_env: dict[str, str] | None = None) -> None:
    env = os.environ.copy()
    env["C48_PYTHON"] = str(ROOT / ".venv/bin/python")
    if extra_env:
        env.update(extra_env)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_path = LOG_DIR / f"{name}.log"
    print(f"START {name}: {' '.join(command)}", flush=True)
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert process.stdout is not None
        for line in process.stdout:
            sys.stdout.write(line)
            log.write(line)
        code = process.wait()
    if code != 0:
        raise SystemExit(f"FAIL {name}: exit {code}; see {log_path}")
    print(f"PASS {name}: log {log_path.relative_to(ROOT)}", flush=True)


def main() -> None:
    run("phase24", ["bash", "ground_zero_work/phase24/verify_phase24.sh"])
    run("phase21", ["bash", "ground_zero_work/phase21/verify_phase21.sh"])
    run(
        "phase20",
        ["bash", "ground_zero_work/phase20/verify_phase20.sh"],
        {"ELAN_HOME": "/Users/jsavva/.elan"},
    )
    print("PASS complete serial Phase 24 -> Phase 21 -> Phase 20 replay")


if __name__ == "__main__":
    main()
