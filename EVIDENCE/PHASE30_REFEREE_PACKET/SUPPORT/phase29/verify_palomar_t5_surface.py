#!/usr/bin/env python3
"""Fail-closed source audit for the Palomar-facing T5 topic."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PROJECT = Path("Kimi_Agent_Riemann Lean Exploration/zeta-23-lean")
CHALLENGE = PROJECT / "comparator/Challenge/TheoremSevenOne.lean"
SOLUTION = PROJECT / "comparator/Solution/TheoremSevenOne.lean"
CONFIG = PROJECT / "comparator/config-theorem-seven-one.json"
METADATA = PROJECT / "comparator/formalization-theorem-seven-one.yaml"


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"FAIL missing {label}: {needle!r}")


def forbid(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise SystemExit(f"FAIL forbidden {label}: {needle!r}")


def validate(root: Path) -> None:
    challenge = (root / CHALLENGE).read_text(encoding="utf-8")
    solution = (root / SOLUTION).read_text(encoding="utf-8")
    config = json.loads((root / CONFIG).read_text(encoding="utf-8"))
    metadata = (root / METADATA).read_text(encoding="utf-8")

    if len(challenge.encode()) > 32 * 1024 or len(challenge.splitlines()) > 300:
        raise SystemExit("FAIL challenge exceeds preferred Palomar review surface")

    require(challenge, "import Mathlib", "Mathlib-only import")
    forbid(challenge, "import Zeta23", "candidate-local challenge import")
    forbid(challenge, "import ChallengeDeps", "candidate-local challenge helper")

    begin = "/- BEGIN PALOMAR TRUSTED DEFINITIONS -/"
    end = "/- END PALOMAR TRUSTED DEFINITIONS -/"
    challenge_defs = challenge.split(begin, 1)[1].split(end, 1)[0]
    solution_defs = solution.split(begin, 1)[1].split(end, 1)[0]
    if challenge_defs != solution_defs:
        raise SystemExit("FAIL trusted definitions differ between Challenge and Solution")

    exact_fragments = {
        "theta-tail normalization": "(HurwitzZeta.evenKernel 0 t - 1) / 2",
        "Mellin quarter exponent": "Real.exp (u / 4) * thetaTail (Real.exp u)",
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
    for label, fragment in exact_fragments.items():
        require(challenge, fragment, label)

    challenge_fragments = {
        "integer normalization seam": "theorem centered_xi_continuation_agrees_at_positive_integers",
        "main theorem": "theorem sectorial_centered_xi_coefficient_asymptotic",
        "derivative theorem": "theorem sectorial_centered_xi_error_derivatives_through_six",
        "quotient identity": "E M = xiCoefficientMoment M / xiCoefficientMain L M - 1",
        "relative rate": "‖E M‖ ≤ C * Real.log ‖M‖ / ‖M‖",
        "six-derivative ceiling": "∀ j ≤ 6",
        "Cauchy rate": "D * Real.log (3 * x) / x",
    }
    for label, fragment in challenge_fragments.items():
        require(challenge, fragment, label)
    quotient = "E M = xiCoefficientMoment M / xiCoefficientMain L M - 1"
    if challenge.count(quotient) != 2:
        raise SystemExit("FAIL quotient identity must occur in both compared statements")
    if challenge.count("DifferentiableOn ℂ E (outerSectorAt R)") != 2:
        raise SystemExit("FAIL both analytic statements must expose outer holomorphy")
    if challenge.count("∀ s ∈ proofSectorAt R, saddleEquation s (L s) = 0") != 2:
        raise SystemExit("FAIL both analytic statements must expose the saddle branch")

    for token in ("sorry", "admit", "sorryAx", "Lean.ofReduceBool", "unsafe"):
        forbid(solution, token, f"solution escape token {token}")

    expected_names = [
        "centered_xi_continuation_agrees_at_positive_integers",
        "sectorial_centered_xi_coefficient_asymptotic",
        "sectorial_centered_xi_error_derivatives_through_six",
    ]
    if config != {
        "challenge_module": "Challenge.TheoremSevenOne",
        "solution_module": "Solution.TheoremSevenOne",
        "theorem_names": expected_names,
        "permitted_axioms": ["propext", "Quot.sound", "Classical.choice"],
        "enable_nanoda": True,
    }:
        raise SystemExit("FAIL Comparator configuration differs from the closed policy")

    for fragment in (
        'version: "v0.4"',
        'license: "Apache-2.0"',
        'status: "agent-reviewed"',
        "No human expert or peer review has occurred and none is claimed.",
        'challenge_module: "Challenge.TheoremSevenOne"',
        'enable_nanoda: true',
    ):
        require(metadata, fragment, "metadata disclosure")
    forbid(metadata, 'status: "peer-reviewed"', "false peer-review status")
    forbid(metadata, 'status: "author-verified"', "unsupported author-verification status")

    print("PASS Palomar T5 trusted-surface audit")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    validate(args.root.resolve())


if __name__ == "__main__":
    main()
