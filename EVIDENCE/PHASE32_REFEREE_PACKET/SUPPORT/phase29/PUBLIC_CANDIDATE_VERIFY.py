#!/usr/bin/env python3
"""Fail-closed source, manifest, and mutation audit for the public candidate."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


EXPECTED_NAMES = [
    "centered_xi_continuation_agrees_at_positive_integers",
    "sectorial_centered_xi_coefficient_asymptotic",
    "sectorial_centered_xi_error_derivatives_through_six",
]

EXACT_FRAGMENTS = {
    "theta normalization": "(HurwitzZeta.evenKernel 0 t - 1) / 2",
    "quarter exponent": "Real.exp (u / 4) * thetaTail (Real.exp u)",
    "Gamma quotient": "Gamma (M + 1) / Gamma (2 * M + 1)",
    "dyadic sign": "exp (-(2 * M + 2) * log 2)",
    "two-shift parameter": "2 * M - 2",
    "actual centered xi": "s * (s - 1) / 2 * completedRiemannZeta₀ s + 1 / 2",
    "actual coefficient": "iteratedDeriv (2 * n) centeredRiemannXi 0",
    "saddle equation": "L * ((Real.pi : ℂ) * exp L + 3 / 4) - s",
    "curvature": "((1 + L) * s - (3 / 4) * L ^ 2) / L ^ 2",
    "proof sector": "|s.arg| < 1 / 100",
    "outer sector": "|M.arg| < 1 / 200",
    "closed inner sector": "|M.arg| ≤ 1 / 400",
    "Cauchy radius": "def cauchyRadius (x : ℝ) : ℝ := x / 1000",
}

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


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise ValueError(f"missing {label}: {needle!r}")


def validate(root: Path, *, check_manifest: bool) -> None:
    challenge_path = root / "comparator/Challenge/TheoremSevenOne.lean"
    solution_path = root / "comparator/Solution/TheoremSevenOne.lean"
    challenge = challenge_path.read_text(encoding="utf-8")
    solution = solution_path.read_text(encoding="utf-8")
    config = json.loads((root / "comparator/config-theorem-seven-one.json").read_text(encoding="utf-8"))
    metadata = (root / "comparator/formalization-theorem-seven-one.yaml").read_text(encoding="utf-8")

    if len(challenge.encode()) > 32 * 1024 or len(challenge.splitlines()) > 300:
        raise ValueError("Challenge exceeds Palomar's preferred review surface")
    imports = [line.strip() for line in challenge.splitlines() if line.startswith("import ")]
    if imports != ["import Mathlib"]:
        raise ValueError(f"trusted imports are not exactly Mathlib: {imports}")

    begin = "/- BEGIN PALOMAR TRUSTED DEFINITIONS -/"
    end = "/- END PALOMAR TRUSTED DEFINITIONS -/"
    if challenge.count(begin) != 1 or challenge.count(end) != 1:
        raise ValueError("Challenge definition markers are malformed")
    if solution.count(begin) != 1 or solution.count(end) != 1:
        raise ValueError("Solution definition markers are malformed")
    challenge_defs = challenge.split(begin, 1)[1].split(end, 1)[0]
    solution_defs = solution.split(begin, 1)[1].split(end, 1)[0]
    if challenge_defs != solution_defs:
        raise ValueError("trusted definitions differ between Challenge and Solution")

    for label, fragment in EXACT_FRAGMENTS.items():
        require(challenge, fragment, label)
    for fragment in (
        "theorem centered_xi_continuation_agrees_at_positive_integers",
        "theorem sectorial_centered_xi_coefficient_asymptotic",
        "theorem sectorial_centered_xi_error_derivatives_through_six",
        "E M = xiCoefficientMoment M / xiCoefficientMain L M - 1",
        "‖E M‖ ≤ C * Real.log ‖M‖ / ‖M‖",
        "∀ j ≤ 6",
        "D * Real.log (3 * x) / x",
    ):
        require(challenge, fragment, "theorem surface")
    if challenge.count("E M = xiCoefficientMoment M / xiCoefficientMain L M - 1") != 2:
        raise ValueError("quotient identity does not occur in both statements")
    if challenge.count("DifferentiableOn ℂ E (outerSectorAt R)") != 2:
        raise ValueError("both analytic statements must expose outer holomorphy")
    if challenge.count("∀ s ∈ proofSectorAt R, saddleEquation s (L s) = 0") != 2:
        raise ValueError("both analytic statements must expose the saddle branch")
    if challenge.count("sorry") != 3:
        # Exactly the three deliberate proof holes.
        raise ValueError("Challenge sorry surface changed")
    for token in ("sorry", "admit", "sorryAx", "Lean.ofReduceBool", "unsafe"):
        if token in solution:
            raise ValueError(f"proof escape token in Solution: {token}")

    expected_config = {
        "challenge_module": "Challenge.TheoremSevenOne",
        "solution_module": "Solution.TheoremSevenOne",
        "theorem_names": EXPECTED_NAMES,
        "permitted_axioms": ["propext", "Quot.sound", "Classical.choice"],
        "enable_nanoda": True,
    }
    if config != expected_config:
        raise ValueError("Comparator configuration differs from policy")
    for fragment in (
        'version: "v0.4"',
        'license: "Apache-2.0"',
        'status: "agent-reviewed"',
        "No human expert or peer review has occurred and none is claimed.",
        'project_path: ""',
        "enable_nanoda: true",
    ):
        require(metadata, fragment, "metadata disclosure")
    if 'status: "peer-reviewed"' in metadata or 'status: "author-verified"' in metadata:
        raise ValueError("unsupported review status")

    if check_manifest:
        verify_manifest(root)


def verify_manifest(root: Path) -> None:
    manifest_path = root / "SHA256SUMS"
    entries: dict[str, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        digest, rel = line.split("  ", 1)
        if rel in entries:
            raise ValueError(f"duplicate manifest entry: {rel}")
        entries[rel] = digest
    actual = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path != manifest_path and ".lake" not in path.parts
    }
    if set(entries) != actual:
        raise ValueError("SHA256SUMS file set differs from candidate file set")
    for rel, expected in entries.items():
        digest = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        if digest != expected:
            raise ValueError(f"SHA-256 mismatch: {rel}")


def run_mutations(root: Path) -> None:
    rels = [
        Path("comparator/Challenge/TheoremSevenOne.lean"),
        Path("comparator/Solution/TheoremSevenOne.lean"),
        Path("comparator/config-theorem-seven-one.json"),
        Path("comparator/formalization-theorem-seven-one.yaml"),
    ]
    for label, old, new in MUTATIONS:
        with tempfile.TemporaryDirectory(prefix="t5-public-mutation-") as tmp:
            tmp_root = Path(tmp)
            for rel in rels:
                target = tmp_root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(root / rel, target)
            changed = False
            for rel in rels:
                path = tmp_root / rel
                text = path.read_text(encoding="utf-8")
                if not changed and old in text:
                    path.write_text(text.replace(old, new, 1), encoding="utf-8")
                    changed = True
            if not changed:
                raise ValueError(f"mutation fixture not found: {label}")
            try:
                validate(tmp_root, check_manifest=False)
            except (OSError, ValueError, json.JSONDecodeError):
                print(f"PASS rejected mutation: {label}")
            else:
                raise ValueError(f"mutation survived: {label}")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    try:
        validate(root, check_manifest=True)
        run_mutations(root)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"FAIL {exc}") from exc
    print(f"PASS public candidate source audit and {len(MUTATIONS)} mutations")


if __name__ == "__main__":
    main()
