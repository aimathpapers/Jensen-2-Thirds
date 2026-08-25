#!/usr/bin/env python3
"""Fail-closed source checks for the Phase-33 review repairs."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKET_LAYOUT = (ROOT / "PAPER" / "source").is_dir()
if PACKET_LAYOUT:
    PAPER = ROOT / "PAPER" / "source"
    LEAN = ROOT / "FORMAL" / "lean-project" / "Zeta23" / "Research" / "JensenWedge"
    PUBLIC_EXPLAINER = ROOT / "PUBLIC" / "JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md"
    GHOST_POST = ROOT / "PUBLIC" / "JENSEN_TWO_THIRDS_GHOST_POST.md"
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
    PUBLIC_EXPLAINER = (
        ROOT
        / "ground_zero_work"
        / "phase24"
        / "manuscript"
        / "JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md"
    )
    GHOST_POST = (
        ROOT
        / "ground_zero_work"
        / "phase31"
        / "blog"
        / "JENSEN_TWO_THIRDS_GHOST_POST.md"
    )


def require(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise SystemExit(f"missing {label}: {needle!r}")


def validate_attributions(
    bibliography: str, public_explainer: str, ghost_post: str
) -> None:
    require(bibliography, "Morales, Rafael", "Rafael Morales attribution")
    require(
        bibliography,
        "Holland, Jonathan",
        "Jonathan Holland bibliography attribution",
    )
    for text, label in (
        (public_explainer, "public explainer"),
        (ghost_post, "magazine article source"),
    ):
        require(text, "Jonathan Holland", f"Jonathan Holland in {label}")
        if "James Holland" in text or "Holland, Jensen" in text:
            raise SystemExit(f"incorrect Holland attribution remains in {label}")


def expect_attribution_mutation_rejected(
    label: str, bibliography: str, public_explainer: str, ghost_post: str
) -> None:
    try:
        validate_attributions(bibliography, public_explainer, ghost_post)
    except SystemExit:
        print(f"PASS Phase 33 attribution source-contract mutation rejected: {label}")
        return
    raise AssertionError(f"Phase 33 attribution mutation survived: {label}")


def main() -> None:
    specialization = (LEAN / "XiNaturalFiniteFreeSpecialization.lean").read_text()
    certificate = (LEAN / "XiNaturalMultiplierCertificate.lean").read_text()
    roots = (LEAN / "MultiplierStability.lean").read_text()
    bibliography = (PAPER / "references.bib").read_text()
    appendix = (PAPER / "c48_detailed_appendices.tex").read_text()
    public_explainer = PUBLIC_EXPLAINER.read_text()
    ghost_post = GHOST_POST.read_text()

    for needle, label in (
        ("structure MSSFiniteFreeIntervalInput", "MSS record"),
        ("0 < uLower →", "first MSS lower guard"),
        ("0 < vLower →", "second MSS lower guard"),
        ("exact hBLower", "first endpoint proof"),
        ("exact hDLower", "second endpoint proof"),
    ):
        require(specialization, needle, label)
    for needle, label in (
        ("riemannXiJensenPolynomialObject_natDegree", "exact degree theorem"),
        ("riemannXiJensen_twoThirds_global_headline", "global cutoff theorem"),
        ("riemannXiJensen_twoThirds_global_headline_exactly", "global exact theorem"),
    ):
        require(certificate, needle, label)
    require(roots, "def HasExactlyDistinctNegativeRoots", "exact root predicate")
    validate_attributions(bibliography, public_explainer, ghost_post)
    require(
        appendix,
        "not\\_twoThirdsWedge\\_finiteCutoffAbsorption",
        "literal finite absorption theorem",
    )
    mutations = (
        (
            "bibliography Holland name",
            bibliography.replace("Holland, Jonathan", "Holland, Jensen", 1),
            public_explainer,
            ghost_post,
        ),
        (
            "public-explainer Holland name",
            bibliography,
            public_explainer.replace("Jonathan Holland", "James Holland", 1),
            ghost_post,
        ),
        (
            "magazine-source Holland name",
            bibliography,
            public_explainer,
            ghost_post.replace("Jonathan Holland", "James Holland", 1),
        ),
    )
    for mutation in mutations:
        expect_attribution_mutation_rejected(*mutation)
    print(
        "PASS Phase 33 guarded MSS, exact-root, global, and attribution source checks"
    )


if __name__ == "__main__":
    main()
