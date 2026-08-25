#!/usr/bin/env python3
"""Fail-closed source-contract checks for the classical finite-free adapters."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKET_LAYOUT = (ROOT / "PAPER" / "source").is_dir()
if PACKET_LAYOUT:
    PAPER = ROOT / "PAPER" / "source"
    LEAN = ROOT / "FORMAL" / "lean-project" / "Zeta23" / "Research" / "JensenWedge"
else:
    PAPER = ROOT / "paper"
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
    require(bibliography, "Morales, Rafael", "MMP author")
    reject(bibliography, "Morales, Ram{\\'o}n", "incorrect MMP author")

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
    for needle, label in (
        ("structure MSSFiniteFreeIntervalInput", "MSS interval structure"),
        ("first_factor : HasDistinctPositiveRoots p.eval d", "MSS first factor"),
        ("second_factor : HasDistinctPositiveRoots q.eval d", "MSS second factor"),
        ("0 < uLower →", "MSS first positive lower endpoint"),
        ("0 < vLower →", "MSS second positive lower endpoint"),
        ("(G : XiNaturalFiniteFreeGeometry", "MSS geometry input"),
        ("exact hBLower", "MSS first endpoint proof"),
        ("exact hDLower", "MSS second endpoint proof"),
    ):
        require(specialization, needle, label)
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
        print(f"PASS Phase 32 source-contract mutation rejected: {label}")
        return
    raise AssertionError(f"Phase 32 mutation survived: {label}")


def main() -> None:
    paths = [
        PAPER / "references.bib",
        LEAN / "FiniteFreeAdapters.lean",
        LEAN / "XiNaturalFiniteFreeSpecialization.lean",
        LEAN / "ConditionalAssembly.lean",
        PAPER / "JENSEN_TWO_THIRDS_MAIN.tex",
        PAPER / "c48_detailed_appendices.tex",
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
        "MSS lower-endpoint positivity": (
            2,
            "0 < uLower →",
            "True →",
        ),
    }
    for label, (index, old, new) in mutations.items():
        if old not in values[index]:
            raise ContractError(f"missing mutation target {label}: {old!r}")
        mutated = values.copy()
        mutated[index] = mutated[index].replace(old, new, 1)
        expect_mutation_rejected(label, mutated)

    print("PASS all Phase 32 source-contract mutations")


if __name__ == "__main__":
    main()
