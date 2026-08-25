#!/usr/bin/env python3
"""Fail-closed source mutations for the concrete Phase-26 T2 chain."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration"
    / "zeta-23-lean"
    / "Zeta23"
    / "Research"
    / "JensenWedge"
)
PATHS = {
    "adapter": LEAN / "AnalyticAdapters.lean",
    "saddle": LEAN / "SectorialSaddle.lean",
}


class ContractError(RuntimeError):
    """A load-bearing T2 source connection is absent or ambiguous."""


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise ContractError(f"{label}: expected exactly one occurrence, found {count}")


def validate(sources: dict[str, str]) -> None:
    adapter = sources["adapter"]
    saddle = sources["saddle"]
    require_once(
        adapter,
        "admissible : ℂ → Set ℂ\n  branch_mem : ∀ s ∈ domain, branch s ∈ admissible s",
        "distinguished-root neighbourhood",
    )
    require_once(
        adapter,
        "root_unique : ∀ s ∈ domain, ∀ z ∈ admissible s,\n"
        "    equation s z = 0 → z = branch s",
        "local uniqueness quantifier",
    )
    require_once(
        saddle,
        "def saddleOuterAngle : ℝ := 1 / 200",
        "outer sector angle",
    )
    require_once(
        saddle,
        "def saddleProofAngle : ℝ := 1 / 100",
        "proof sector angle",
    )
    require_once(
        saddle,
        "def saddleParameterMap (L : ℂ) : ℂ :=\n"
        "  L * ((Real.pi : ℂ) * exp L + 3 / 4)",
        "exact saddle parameter map",
    )
    require_once(
        saddle,
        "(1 + L) * s - (3 / 4) * L ^ 2",
        "curvature denominator",
    )
    require_once(
        saddle,
        "theorem saddle_derivative_mul_eq_curvature {s L : ℂ}",
        "derivative-curvature seam",
    )
    require_once(
        saddle,
        "theorem sectorialSaddleCurvature_ne_zero_of_box\n",
        "finite-box nonvanishing seam",
    )
    require_once(
        saddle,
        "def saddleNewtonMap (s L : ℂ) : ℂ :=\n"
        "  L - sectorialSaddleEquation s L / s",
        "equation-normalized Newton map",
    )
    require_once(
        saddle,
        "theorem saddleNewtonMap_fixed_iff {s L : ℂ} (hs : s ≠ 0)",
        "fixed-point/root equivalence",
    )
    require_once(
        saddle,
        "structure SaddleContractionFamily (domain : Set ℂ) where",
        "uniform contraction family",
    )
    require_once(
        saddle,
        "theorem SaddleContractionFamily.existsUnique_root_in_disc\n",
        "whole-disc root constructor",
    )
    require_once(
        saddle,
        "theorem contractedSaddleBranch_spec\n",
        "selected branch specification",
    )
    require_once(
        saddle,
        "structure SaddleQuantitativeInput (s : ℂ) : Prop where",
        "quantitative input boundary",
    )
    require_once(
        saddle,
        "logParameter_norm_lower : 1000 ≤ ‖log s‖",
        "log-parameter lower bound",
    )
    require_once(
        saddle,
        "logCorrection_le :\n"
        "    ‖log (log s) + log (Real.pi : ℂ)‖ ≤ ‖log s‖ / 100",
        "log-correction ratio",
    )
    require_once(
        saddle,
        "theorem saddleNewton_derivative_norm_le\n",
        "whole-disc derivative bound",
    )
    require_once(
        saddle,
        "theorem saddleNewton_maps_disc\n",
        "whole-disc self-map",
    )
    require_once(
        saddle,
        "contractionConstant := 1 / 4",
        "concrete contraction constant",
    )
    require_once(
        saddle,
        "radius := fun _ => 1 / 20",
        "concrete disc radius",
    )
    require_once(
        saddle,
        "theorem quantitativeSaddleBranch_curvature_ne_zero\n",
        "quantitative curvature conclusion",
    )
    require_once(
        saddle,
        "def leanSaddleCutoff : ℝ := 1000000",
        "Lean effective cutoff",
    )
    require_once(
        saddle,
        "theorem leanSaddleSector_quantitative\n",
        "sector-to-quantitative bridge",
    )
    require_once(
        saddle,
        "dist (quantitativeSaddleBranch s) (saddleComparisonCenter s) ≤ 11 / 750",
        "sharpened branch distance",
    )
    require_once(
        saddle,
        "theorem hasDerivAt_quantitativeSaddleBranch\n",
        "holomorphic branch derivative",
    )
    require_once(
        saddle,
        "quantitativeSaddleBranch s /\n"
        "        sectorialSaddleCurvature s (quantitativeSaddleBranch s)",
        "implicit derivative L over Q",
    )
    require_once(
        saddle,
        "noncomputable def leanSectorialSaddleCertificate :",
        "concrete T2 certificate",
    )


def mutate(
    sources: dict[str, str], key: str, old: str, new: str
) -> dict[str, str]:
    changed = dict(sources)
    if changed[key].count(old) != 1:
        raise AssertionError(f"mutation source is not unique: {key}: {old!r}")
    changed[key] = changed[key].replace(old, new, 1)
    return changed


def expect_rejected(label: str, sources: dict[str, str]) -> None:
    try:
        validate(sources)
    except ContractError:
        print(f"PASS T2 mutation rejected: {label}")
        return
    raise AssertionError(f"T2 mutation survived: {label}")


def main() -> None:
    sources = {key: path.read_text(encoding="utf-8") for key, path in PATHS.items()}
    validate(sources)
    print("PASS concrete T2 source contract")
    cases = {
        "local uniqueness made global": mutate(
            sources,
            "adapter",
            "∀ z ∈ admissible s,",
            "∀ z,",
        ),
        "branch neighbourhood membership removed": mutate(
            sources,
            "adapter",
            "branch_mem : ∀ s ∈ domain, branch s ∈ admissible s",
            "branch_mem_unchecked : True",
        ),
        "outer angle widened": mutate(
            sources,
            "saddle",
            "def saddleOuterAngle : ℝ := 1 / 200",
            "def saddleOuterAngle : ℝ := 1 / 2",
        ),
        "proof angle widened": mutate(
            sources,
            "saddle",
            "def saddleProofAngle : ℝ := 1 / 100",
            "def saddleProofAngle : ℝ := 1 / 2",
        ),
        "saddle three-quarters dropped": mutate(
            sources,
            "saddle",
            "def saddleParameterMap (L : ℂ) : ℂ :=\n"
            "  L * ((Real.pi : ℂ) * exp L + 3 / 4)",
            "def saddleParameterMap (L : ℂ) : ℂ :=\n"
            "  L * ((Real.pi : ℂ) * exp L)",
        ),
        "curvature sign changed": mutate(
            sources,
            "saddle",
            "(1 + L) * s - (3 / 4) * L ^ 2",
            "(1 + L) * s + (3 / 4) * L ^ 2",
        ),
        "derivative-curvature theorem disconnected": mutate(
            sources,
            "saddle",
            "theorem saddle_derivative_mul_eq_curvature {s L : ℂ}",
            "theorem saddle_derivative_mul_eq_curvature_unchecked {s L : ℂ}",
        ),
        "box nonvanishing theorem disconnected": mutate(
            sources,
            "saddle",
            "theorem sectorialSaddleCurvature_ne_zero_of_box\n",
            "theorem sectorialSaddleCurvature_ne_zero_of_box_unchecked\n",
        ),
        "Newton normalization changed": mutate(
            sources,
            "saddle",
            "def saddleNewtonMap (s L : ℂ) : ℂ :=\n"
            "  L - sectorialSaddleEquation s L / s",
            "def saddleNewtonMap (s L : ℂ) : ℂ :=\n"
            "  L - sectorialSaddleEquation s L",
        ),
        "fixed-point equivalence disconnected": mutate(
            sources,
            "saddle",
            "theorem saddleNewtonMap_fixed_iff {s L : ℂ} (hs : s ≠ 0)",
            "theorem saddleNewtonMap_fixed_iff_unchecked {s L : ℂ} (hs : s ≠ 0)",
        ),
        "contraction family disconnected": mutate(
            sources,
            "saddle",
            "structure SaddleContractionFamily (domain : Set ℂ) where",
            "structure SaddleContractionFamilyUnchecked (domain : Set ℂ) where",
        ),
        "root constructor disconnected": mutate(
            sources,
            "saddle",
            "theorem SaddleContractionFamily.existsUnique_root_in_disc\n",
            "theorem SaddleContractionFamily.existsUnique_root_in_disc_unchecked\n",
        ),
        "selected branch specification disconnected": mutate(
            sources,
            "saddle",
            "theorem contractedSaddleBranch_spec\n",
            "theorem contractedSaddleBranch_spec_unchecked\n",
        ),
        "log lower bound weakened": mutate(
            sources,
            "saddle",
            "logParameter_norm_lower : 1000 ≤ ‖log s‖",
            "logParameter_norm_lower : 10 ≤ ‖log s‖",
        ),
        "log correction enlarged": mutate(
            sources,
            "saddle",
            "logCorrection_le :\n"
            "    ‖log (log s) + log (Real.pi : ℂ)‖ ≤ ‖log s‖ / 100",
            "logCorrection_le :\n"
            "    ‖log (log s) + log (Real.pi : ℂ)‖ ≤ ‖log s‖ / 10",
        ),
        "disc radius enlarged": mutate(
            sources,
            "saddle",
            "radius := fun _ => 1 / 20",
            "radius := fun _ => 1 / 2",
        ),
        "contraction constant weakened": mutate(
            sources,
            "saddle",
            "contractionConstant := 1 / 4",
            "contractionConstant := 3 / 4",
        ),
        "derivative bound disconnected": mutate(
            sources,
            "saddle",
            "theorem saddleNewton_derivative_norm_le\n",
            "theorem saddleNewton_derivative_norm_le_unchecked\n",
        ),
        "self-map theorem disconnected": mutate(
            sources,
            "saddle",
            "theorem saddleNewton_maps_disc\n",
            "theorem saddleNewton_maps_disc_unchecked\n",
        ),
        "curvature conclusion disconnected": mutate(
            sources,
            "saddle",
            "theorem quantitativeSaddleBranch_curvature_ne_zero\n",
            "theorem quantitativeSaddleBranch_curvature_ne_zero_unchecked\n",
        ),
        "Lean cutoff weakened": mutate(
            sources,
            "saddle",
            "def leanSaddleCutoff : ℝ := 1000000",
            "def leanSaddleCutoff : ℝ := 12",
        ),
        "sector input bridge disconnected": mutate(
            sources,
            "saddle",
            "theorem leanSaddleSector_quantitative\n",
            "theorem leanSaddleSector_quantitative_unchecked\n",
        ),
        "sharpened branch distance weakened": mutate(
            sources,
            "saddle",
            "dist (quantitativeSaddleBranch s) (saddleComparisonCenter s) ≤ 11 / 750",
            "dist (quantitativeSaddleBranch s) (saddleComparisonCenter s) ≤ 1 / 20",
        ),
        "branch derivative inverted": mutate(
            sources,
            "saddle",
            "quantitativeSaddleBranch s /\n"
            "        sectorialSaddleCurvature s (quantitativeSaddleBranch s)",
            "sectorialSaddleCurvature s (quantitativeSaddleBranch s) /\n"
            "        quantitativeSaddleBranch s",
        ),
        "holomorphic derivative disconnected": mutate(
            sources,
            "saddle",
            "theorem hasDerivAt_quantitativeSaddleBranch\n",
            "theorem hasDerivAt_quantitativeSaddleBranch_unchecked\n",
        ),
        "concrete T2 certificate disconnected": mutate(
            sources,
            "saddle",
            "noncomputable def leanSectorialSaddleCertificate :",
            "noncomputable def leanSectorialSaddleCertificateUnchecked :",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print("PASS all concrete T2 semantic mutations")


if __name__ == "__main__":
    main()
