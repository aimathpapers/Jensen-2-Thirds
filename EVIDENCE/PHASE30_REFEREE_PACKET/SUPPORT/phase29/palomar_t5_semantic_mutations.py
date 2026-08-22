#!/usr/bin/env python3
"""Show that the Palomar surface gate rejects decisive T5 mutations."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "ground_zero_work/phase29/verify_palomar_t5_surface.py"
PROJECT = Path("Kimi_Agent_Riemann Lean Exploration/zeta-23-lean")

MUTATIONS = [
    ("theta normalization", "(HurwitzZeta.evenKernel 0 t - 1) / 2", "HurwitzZeta.evenKernel 0 t / 2"),
    ("quarter exponent", "Real.exp (u / 4)", "Real.exp (u / 2)"),
    ("Gamma denominator", "Gamma (2 * M + 1)", "Gamma (M + 1)"),
    ("dyadic sign", "exp (-(2 * M + 2) * log 2)", "exp ((2 * M + 2) * log 2)"),
    ("xi quadratic prefactor", "s * (s - 1) / 2", "s * (s + 1) / 2"),
    ("xi derivative parity", "iteratedDeriv (2 * n) centeredRiemannXi 0", "iteratedDeriv (2 * n + 1) centeredRiemannXi 0"),
    ("saddle constant", "+ 3 / 4) - s", "+ 1 / 4) - s"),
    ("curvature sign", "- (3 / 4) * L ^ 2", "+ (3 / 4) * L ^ 2"),
    ("proof angle", "|s.arg| < 1 / 100", "|s.arg| < 1 / 200"),
    ("outer angle", "|M.arg| < 1 / 200", "|M.arg| < 1 / 100"),
    ("closed inner boundary", "|M.arg| ≤ 1 / 400", "|M.arg| < 1 / 400"),
    ("Cauchy radius", "x / 1000", "x / 100"),
    ("quotient identity", "xiCoefficientMoment M / xiCoefficientMain L M - 1", "xiCoefficientMoment M - xiCoefficientMain L M"),
    ("derivative ceiling", "∀ j ≤ 6", "∀ j ≤ 5"),
    ("outer holomorphy", "DifferentiableOn ℂ E (outerSectorAt R)", "True"),
    ("NanoDa disabled", '"enable_nanoda": true', '"enable_nanoda": false'),
    ("trusted local import", "import Mathlib", "import Mathlib\nimport Zeta23"),
]


def run() -> None:
    source_files = [
        PROJECT / "comparator/Challenge/TheoremSevenOne.lean",
        PROJECT / "comparator/Solution/TheoremSevenOne.lean",
        PROJECT / "comparator/config-theorem-seven-one.json",
        PROJECT / "comparator/formalization-theorem-seven-one.yaml",
    ]
    for label, old, new in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix="phase29-mutation-") as tmp:
            tmp_root = Path(tmp)
            for rel in source_files:
                target = tmp_root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, target)
            changed = False
            for rel in source_files:
                path = tmp_root / rel
                text = path.read_text(encoding="utf-8")
                if not changed and old in text:
                    path.write_text(text.replace(old, new, 1), encoding="utf-8")
                    changed = True
            if not changed:
                raise SystemExit(f"FAIL mutation fixture not found: {label}")
            result = subprocess.run(
                [str(ROOT / ".venv/bin/python"), str(CHECKER), "--root", str(tmp_root)],
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode == 0:
                raise SystemExit(f"FAIL mutation survived: {label}")
            print(f"PASS rejected mutation: {label}")
    print(f"PASS all {len(MUTATIONS)} Palomar T5 semantic mutations rejected")


if __name__ == "__main__":
    run()
