#!/usr/bin/env python3
"""Fail-closed semantic source mutations for the xi multiplier endpoint."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge"
PATHS = {
    "multiplier": LEAN / "XiNaturalConcreteMultiplier.lean",
    "bound": LEAN / "XiNaturalConcreteMultiplierSpecialization.lean",
    "endpoint": LEAN / "XiNaturalMultiplierEndpoint.lean",
    "intervals": LEAN / "PolynomialRootIntervals.lean",
    "certificate": LEAN / "XiNaturalMultiplierCertificate.lean",
}


class ContractError(RuntimeError):
    pass


def declaration(text: str, name: str) -> str:
    pattern = re.compile(
        rf"(?ms)^(?:theorem|def) {re.escape(name)}\b.*?(?=^(?:theorem|def|structure|class|end\b)|\Z)"
    )
    match = pattern.search(text)
    if match is None:
        raise ContractError(f"missing declaration {name}")
    return match.group(0)


def require(block: str, needle: str, label: str) -> None:
    if needle not in block:
        raise ContractError(f"{label}: missing {needle!r}")


def validate(sources: dict[str, str]) -> None:
    six = declaration(sources["multiplier"], "xiNaturalConcreteMultiplier_six_nodes")
    require(six, "∀ j : Fin 6", "six-node arity")
    require(six, "= 1", "six-node value")

    tube = declaration(
        sources["bound"], "xiNaturalConcreteMultiplier_sub_one_norm_lt_one_on_tube"
    )
    require(tube, "‖xiNaturalConcreteMultiplier", "concrete multiplier bound")
    require(tube, "- 1‖ < 1", "strict unit bound")
    require(tube, "xiNaturalMultiplierTube_subset_radius", "tube-to-disc proof")

    transform = declaration(
        sources["endpoint"],
        "xiNaturalActualLogPolynomial_eq_comparisonMultiplierTransform_of_explicitCutoff",
    )
    require(transform, "xiNaturalActualLogPolynomial", "actual polynomial")
    require(transform, "coefficientMultiplierTransform", "multiplier transform")

    residual = declaration(
        sources["endpoint"],
        "xiNaturalActualComparison_relativeError_lt_one_at_critical",
    )
    require(residual, "finiteNewtonRelativeError_lt_one", "finite Newton estimate")
    require(residual, "xiNaturalConcreteRealMultiplier_forwardDiff_bound", "residual input")

    constructor = declaration(
        sources["intervals"], "multiplierIntervalCertificate_of_complete_roots"
    )
    require(constructor, "nonnegative_left", "natural left endpoint")
    require(constructor, "polynomialRollePoint", "Rolle endpoints")
    require(constructor, "model_change", "model sign change")

    cert = declaration(sources["certificate"], "xiNatural_multiplierIntervalCertificate")
    require(cert, "MultiplierIntervalCertificate", "certificate type")
    require(cert, "xiNaturalActualComparison_relativeError_lt_one_at_critical", "critical error")
    require(cert, "multiplierIntervalCertificate_of_complete_roots", "complete-root constructor")
    require(cert, "exists_right_relativeError_lt_one", "exterior endpoint")

    assembly = declaration(sources["certificate"], "xiNatural_jensenWedgeCertificate")
    require(assembly, "xiNatural_multiplierIntervalCertificate", "concrete interval consumer")
    require(assembly, "riemannXiJensenPolynomial", "actual Jensen target")

    headline = declaration(sources["certificate"], "riemannXiJensen_twoThirds_headline")
    require(headline, "XiNaturalClassicalRootInputs", "typed literature input")
    require(headline, "riemannXiJensen_twoThirds_low_degree", "low-degree branch")
    require(headline, "xiNatural_jensenWedgeCertificate", "high-degree branch")
    require(headline, "HasDistinctNegativeRoots", "headline conclusion")


def mutate(
    sources: dict[str, str], key: str, old: str, new: str
) -> dict[str, str]:
    changed = dict(sources)
    count = changed[key].count(old)
    if count < 1:
        raise ContractError(f"mutation source {key}: missing {old!r}")
    changed[key] = changed[key].replace(old, new, 1)
    return changed


def main() -> None:
    sources = {key: path.read_text(encoding="utf-8") for key, path in PATHS.items()}
    validate(sources)
    print("PASS Phase 30 xi-multiplier semantic source contract")
    cases = {
        "six nodes weakened to five": mutate(
            sources,
            "multiplier",
            "∀ j : Fin 6, xiNaturalConcreteMultiplier n L y (j : ℂ) = 1 := by",
            "∀ j : Fin 5, xiNaturalConcreteMultiplier n L y (j : ℂ) = 1 := by",
        ),
        "strict unit bound weakened": mutate(
            sources,
            "bound",
            "(exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters z - 1‖ < 1 :=\n  xiNaturalConcreteMultiplier_sub_one_norm_lt_one_of_explicitCutoff",
            "(exactXiPositiveParameterBranch_of_explicitCutoff hn).parameters z - 1‖ ≤ 1 :=\n  xiNaturalConcreteMultiplier_sub_one_norm_lt_one_of_explicitCutoff",
        ),
        "actual transform disconnected": mutate(
            sources,
            "endpoint",
            "theorem xiNaturalActualLogPolynomial_eq_comparisonMultiplierTransform_of_explicitCutoff",
            "theorem unchecked_actual_transform",
        ),
        "finite Newton input disconnected": mutate(
            sources,
            "endpoint",
            "finiteNewtonRelativeError_lt_one",
            "uncheckedFiniteNewtonRelativeError",
        ),
        "Rolle constructor disconnected": mutate(
            sources,
            "intervals",
            "def multiplierIntervalCertificate_of_complete_roots",
            "def uncheckedMultiplierIntervalCertificate",
        ),
        "critical relative error disconnected": mutate(
            sources,
            "certificate",
            "xiNaturalActualComparison_relativeError_lt_one_at_critical",
            "uncheckedCriticalRelativeError",
        ),
        "actual Jensen target disconnected": mutate(
            sources,
            "certificate",
            "riemannXiJensenPolynomial n (k + 2)",
            "uncheckedTarget n (k + 2)",
        ),
        "low-degree branch removed": mutate(
            sources,
            "certificate",
            "riemannXiJensen_twoThirds_low_degree hn hd I",
            "uncheckedLowDegree hn hd I",
        ),
        "headline conclusion weakened": mutate(
            sources,
            "certificate",
            "theorem riemannXiJensen_twoThirds_headline",
            "theorem unchecked_riemannXiJensen_twoThirds_headline",
        ),
    }
    for label, changed in cases.items():
        try:
            validate(changed)
        except ContractError:
            print(f"PASS Phase 30 mutation rejected: {label}")
            continue
        raise SystemExit(f"Phase 30 mutation survived: {label}")


if __name__ == "__main__":
    main()
