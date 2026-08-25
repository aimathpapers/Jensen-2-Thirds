#!/usr/bin/env python3
"""Fail-closed source mutations for the literal manuscript T5 theorem."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge"
PATHS = {
    "saddle": LEAN / "SectorialSaddle.lean",
    "ratio": LEAN / "SaddleMainRatio.lean",
    "theorem": LEAN / "ManuscriptTheoremSevenOne.lean",
}


class ContractError(RuntimeError):
    pass


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise ContractError(f"{label}: expected one occurrence, found {count}")


def validate(sources: dict[str, str]) -> None:
    saddle = sources["saddle"]
    ratio = sources["ratio"]
    theorem = sources["theorem"]
    checks = (
        (saddle, "def saddleInnerAngle : ℝ := 1 / 400", "inner angle"),
        (saddle, "def saddleOuterAngle : ℝ := 1 / 200", "outer angle"),
        (saddle, "def saddleProofAngle : ℝ := 1 / 100", "proof angle"),
        (saddle, "|s.arg| < saddleProofAngle", "proof-sector consumer"),
        (ratio, "|s.arg| < saddleOuterAngle", "outer coefficient sector"),
        (theorem, "def manuscriptOuterSectorAt", "outer paper sector"),
        (theorem, "def manuscriptInnerSectorAt", "inner paper sector"),
        (theorem, "theorem manuscriptOuterSector_parameter_geometry", "outer geometry"),
        (theorem, "theorem manuscriptInnerSector_subset_leanXiCoefficientSector", "inner geometry"),
        (theorem, "def manuscriptPaperRelativeError", "quotient error"),
        (theorem, "2 * manuscriptXiCoefficientErrorCoefficient", "M-normalized constant"),
        (theorem, "theorem manuscriptTheoremSevenOne_effective", "effective theorem"),
        (theorem, "theorem manuscriptTheoremSevenOne :", "existential theorem"),
        (theorem, "∃ R C : ℝ, 0 < R ∧ 0 < C", "positive witnesses"),
        (theorem, "theorem differentiableOn_manuscriptPaperRelativeError_manuscriptOuter", "outer error holomorphy"),
        (theorem, "∀ M ∈ manuscriptInnerSectorAt R", "closed inner consumer"),
        (theorem, "theorem manuscriptPaperRelativeError_norm_le", "paper rate"),
        (theorem, "theorem manuscriptPaperRelativeError_derivatives_through_six", "six derivatives"),
        (theorem, "∀ j ≤ 6", "order six"),
    )
    for text, needle, label in checks:
        require_once(text, needle, label)


def mutate(sources: dict[str, str], key: str, old: str, new: str) -> dict[str, str]:
    result = dict(sources)
    require_once(result[key], old, f"mutation source {key}")
    result[key] = result[key].replace(old, new, 1)
    return result


def main() -> None:
    sources = {key: path.read_text(encoding="utf-8") for key, path in PATHS.items()}
    validate(sources)
    print("PASS Phase 28 literal-T5 source contract")
    cases = {
        "proof sector collapsed": mutate(
            sources,
            "saddle",
            "def saddleProofAngle : ℝ := 1 / 100",
            "def saddleProofAngle : ℝ := 1 / 200",
        ),
        "outer sector narrowed": mutate(
            sources,
            "saddle",
            "def saddleOuterAngle : ℝ := 1 / 200",
            "def saddleOuterAngle : ℝ := 1 / 400",
        ),
        "inner sector widened": mutate(
            sources,
            "saddle",
            "def saddleInnerAngle : ℝ := 1 / 400",
            "def saddleInnerAngle : ℝ := 1 / 200",
        ),
        "affine geometry disconnected": mutate(
            sources,
            "theorem",
            "theorem manuscriptOuterSector_parameter_geometry",
            "theorem unchecked_manuscriptOuterSector_parameter_geometry",
        ),
        "quotient error disconnected": mutate(
            sources,
            "theorem",
            "def manuscriptPaperRelativeError",
            "def uncheckedManuscriptPaperRelativeError",
        ),
        "error constant halved": mutate(
            sources,
            "theorem",
            "2 * manuscriptXiCoefficientErrorCoefficient",
            "manuscriptXiCoefficientErrorCoefficient",
        ),
        "existential theorem disconnected": mutate(
            sources,
            "theorem",
            "theorem manuscriptTheoremSevenOne :",
            "theorem uncheckedManuscriptTheoremSevenOne :",
        ),
        "inner rate moved to outer": mutate(
            sources,
            "theorem",
            "∀ M ∈ manuscriptInnerSectorAt R",
            "∀ M ∈ manuscriptOuterSectorAt R",
        ),
        "sixth derivative dropped": mutate(sources, "theorem", "∀ j ≤ 6", "∀ j ≤ 5"),
    }
    for label, changed in cases.items():
        try:
            validate(changed)
        except ContractError:
            print(f"PASS Phase 28 mutation rejected: {label}")
            continue
        raise SystemExit(f"Phase 28 mutation survived: {label}")


if __name__ == "__main__":
    main()
