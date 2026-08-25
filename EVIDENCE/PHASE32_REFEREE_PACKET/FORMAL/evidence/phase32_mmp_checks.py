#!/usr/bin/env python3
"""Fail-closed checks for the Holland citation and concrete MMP adapter."""

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


class ContractError(RuntimeError):
    pass


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise ContractError(f"missing {label}: {needle!r}")


def reject(text: str, needle: str, label: str) -> None:
    if needle in text:
        raise ContractError(f"forbidden {label}: {needle!r}")


def validate(
    bibliography: str,
    adapters: str,
    specialization: str,
    conditional: str,
    main: str,
    appendix: str,
) -> None:
    require(bibliography, "author       = {Holland, Jonathan}", "Holland author")
    reject(bibliography, "Holland, Jensen", "incorrect Holland author")

    require(
        adapters,
        "structure MMPFiniteFreeLogMeshInput (p q : ℝ[X]) (d : ℕ)",
        "factor-level MMP structure",
    )
    for needle, label in (
        ("first_factor : HasDistinctPositiveRoots p.eval d", "first factor roots"),
        ("first_degree : p.natDegree ≤ d", "first factor degree"),
        ("second_factor : HasDistinctPositiveRoots q.eval d", "second factor roots"),
        ("second_degree : q.natDegree ≤ d", "second factor degree"),
        (
            "roots_are_zeros : ∀ i, (finiteFreeAscending d p q).eval",
            "convolution roots",
        ),
    ):
        require(adapters, needle, label)
    reject(adapters, "structure MMPLogMeshInput", "obsolete final-function MMP seam")

    require(
        specialization,
        "theorem terminating3F2Polynomial_eq_finiteFree_jacobiFactors",
        "symbolic 3F2 factorization",
    )
    require(
        specialization,
        "mmp : MMPFiniteFreeLogMeshInput",
        "concrete factor-level MMP field",
    )
    require(
        specialization,
        "xiNaturalComparisonPolynomial_eq_finiteFree hn hL hL12 hy d",
        "Lean transport to xi comparison",
    )

    require(
        conditional,
        "theorem not_twoThirdsWedge_finiteCutoffAbsorption",
        "kernel-checked finite absorption",
    )
    require(main, "K_{\\rm finite}=N_0^2(N_0+2)+1", "displayed finite constant")
    require(
        appendix,
        "\\label{app:mmp-specialization}",
        "MMP specialization appendix",
    )
    for needle, label in (
        ("Q_{A,B}^{(1)}\\boxconv Q_{C,D}^{(D)}", "concrete factorization"),
        ("MMP v3 Proposition~2.7(iii)", "MMP positivity citation"),
        ("MMP v3 Definition~2.16 and Proposition~2.17", "MMP mesh citation"),
        ("U-V-d", "Jacobi parameter translation"),
        ("not\\_twoThirdsWedge\\_finiteCutoffAbsorption", "Lean absorption link"),
    ):
        require(appendix, needle, label)


def expect_mutation_rejected(label: str, values: list[str]) -> None:
    try:
        validate(*values)
    except ContractError:
        print(f"PASS Phase 32 mutation rejected: {label}")
        return
    raise AssertionError(f"Phase 32 mutation survived: {label}")


def main() -> None:
    paths = [
        ROOT / "paper" / "references.bib",
        LEAN / "FiniteFreeAdapters.lean",
        LEAN / "XiNaturalFiniteFreeSpecialization.lean",
        LEAN / "ConditionalAssembly.lean",
        ROOT / "paper" / "JENSEN_TWO_THIRDS_MAIN.tex",
        ROOT / "paper" / "c48_detailed_appendices.tex",
    ]
    values = [path.read_text(encoding="utf-8") for path in paths]
    validate(*values)
    print("PASS Phase 32 Holland citation and concrete MMP source contract")

    mutations = {
        "Holland name": (0, "Holland, Jonathan", "Holland, Jensen"),
        "factor-level type": (
            1,
            "structure MMPFiniteFreeLogMeshInput",
            "structure MMPLogMeshInput",
        ),
        "first factor membership": (
            1,
            "first_factor : HasDistinctPositiveRoots p.eval d",
            "first_factor : True",
        ),
        "convolution target": (
            1,
            "(finiteFreeAscending d p q).eval",
            "p.eval",
        ),
        "3F2 transport": (
            2,
            "xiNaturalComparisonPolynomial_eq_finiteFree hn hL hL12 hy d",
            "assumedXiComparisonFactorization",
        ),
        "finite absorption": (
            3,
            "theorem not_twoThirdsWedge_finiteCutoffAbsorption",
            "theorem assumedFiniteCutoffAbsorption",
        ),
        "MMP proposition": (
            5,
            "MMP v3 Proposition~2.7(iii)",
            "MMP proposition",
        ),
    }
    for label, (index, old, new) in mutations.items():
        if old not in values[index]:
            raise ContractError(f"missing mutation target {label}: {old!r}")
        mutated = values.copy()
        mutated[index] = mutated[index].replace(old, new, 1)
        expect_mutation_rejected(label, mutated)

    print("PASS all Phase 32 semantic mutations")


if __name__ == "__main__":
    main()
