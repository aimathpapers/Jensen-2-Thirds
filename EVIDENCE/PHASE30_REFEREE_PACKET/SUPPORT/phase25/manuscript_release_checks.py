#!/usr/bin/env python3
"""Fail-closed source and PDF checks for the expanded manuscript set."""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper"
MAIN = PAPER / "JENSEN_TWO_THIRDS_MAIN.tex"
APPENDICES = PAPER / "c48_detailed_appendices.tex"
SUPPLEMENT = PAPER / "JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex"
BIBLIOGRAPHY = PAPER / "references.bib"


def fail(message: str) -> None:
    raise AssertionError(message)


def labels_and_refs(source: str) -> tuple[list[str], list[str]]:
    labels = re.findall(r"\\label\{([^}]+)\}", source)
    refs = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", source)
    return labels, refs


def citations(source: str) -> set[str]:
    groups = re.findall(r"\\cite(?:\[[^]]*\])?\{([^}]+)\}", source)
    return {key.strip() for group in groups for key in group.split(",")}


def check_references() -> None:
    main_source = MAIN.read_text(encoding="utf-8") + APPENDICES.read_text(
        encoding="utf-8"
    )
    supplement_source = SUPPLEMENT.read_text(encoding="utf-8")
    for name, source in (("main", main_source), ("supplement", supplement_source)):
        labels, refs = labels_and_refs(source)
        duplicate_labels = sorted({label for label in labels if labels.count(label) > 1})
        if duplicate_labels:
            fail(f"{name} has duplicate labels: {duplicate_labels}")
        missing_refs = sorted(set(refs) - set(labels))
        if missing_refs:
            fail(f"{name} has unresolved source references: {missing_refs}")

    bib_keys = set(re.findall(r"@\w+\{([^,]+),", BIBLIOGRAPHY.read_text(encoding="utf-8")))
    missing_citations = sorted(
        (citations(main_source) | citations(supplement_source)) - bib_keys
    )
    if missing_citations:
        fail(f"bibliography lacks citation keys: {missing_citations}")


def check_load_bearing_text(joined: str) -> None:
    """Check semantic manuscript sentinels in an already assembled source."""
    required = (
        r"\frac{n!}{(2n)!}",
        r"8\int_0^\infty\omega(e^{2u})e^{u/2}u^{2n}",
        r"\left|\frac{y_0^kp_F^{(k)}(y_0)}{p_F(y_0)}\right|^{1/k}",
        r"C_{\rm loc}=12+8\sqrt6<32",
        r"K_{\rm pre}=256",
        r"\frac1{720}",
        r"n^2\log(n+2)\ge Kd^3",
        r"u=L_s+r",
        r"r\ge1-\Re L_s",
        r"r\ge1-\Re L_N",
        "full real Gaussian is only a comparison integral",
        r"\Phi_s(u)=s\operatorname{Log}u-\frac34u-\pi e^u",
        r"I_1(s):=F_1(s):=\int_0^\infty g_s(u)\,\dd u",
        r"\Phi_N(u)=N\operatorname{Log}u-\frac34u-\pi e^u",
        r"I_1(N):=F_1(N):=\int_0^\infty g_N(u)\,\dd u",
        r"h(z):=\log M_z",
        r"\mathcal M=\max_{0\le j\le d}",
        r"3F_1-F_2=\frac{3w(t-1)}{t^4}-1",
        r"\frac43F_2-F_3=\frac{4w(t-1)}{t^5}-\frac23",
        r"P_{2,m}&=B+D+2m+1",
        r"N_0=\max\{N_{\rm analytic},N_{\rm explicit}\}",
        r"Phase26Axioms.lean",
        "1,217",
        r"G_0(N)=",
        "subtracting the explicit gamma factors",
        "does not purport to compute",
        "All reviews currently",
        "AI reviews, not human or",
    )
    for needle in required:
        if needle not in joined:
            fail(f"missing load-bearing manuscript text: {needle}")

    forbidden = (
        r"\frac{8\,2^{2n}}{(2n)!}",
        r"\omega(e^{2u})e^u u^{2n}",
        r"\frac{p_F^{(k)}(y)}{k!p_F(y)}",
        r"C_{\rm loc}=8+12\sqrt6",
        r"K_{\rm pre}=32",
        r"u=L_s+iv",
        r"u=L_s+i\,v",
        r"u=L_s+r$ with $r\in\R",
        r"u=L_N+r$, $r\in\R",
        r"\Phi_s(u)=s\operatorname{Log}u+\frac14u-\pi e^u",
        r"\Phi_N(u)=N\operatorname{Log}u+\frac14u-\pi e^u",
        r"h(x)=\log\gamma(x)",
        r"P_{2,m}&=B+D+3m+1",
        r"N_{\rm elementary}",
        "The Phase-20 axiom report prints every audited declaration",
        r"Phase25Axioms.lean",
        r"3tF_2-F_3=3w(t-1)-t^4",
        r"|v|=1",
        "first-failure induction",
    )
    for needle in forbidden:
        if needle in joined:
            fail(f"stale false manuscript text: {needle}")

    bad_command = re.search(r"(?<!\\)\b(?:qq?uad|quad)\b", joined)
    if bad_command:
        fail(f"literal TeX spacing command near offset {bad_command.start()}")


def check_load_bearing_sources() -> None:
    main = MAIN.read_text(encoding="utf-8")
    appendices = APPENDICES.read_text(encoding="utf-8")
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    joined = "\n".join((main, appendices, supplement))
    check_load_bearing_text(joined)

    if "\\documentclass[12pt]{article}" not in main:
        fail("main paper is not the expanded 12-point edition")
    if "\\input{c48_detailed_appendices.tex}" not in main:
        fail("main paper does not load its detailed proof appendices")


def check_review_language() -> None:
    files = (
        MAIN,
        APPENDICES,
        SUPPLEMENT,
        PAPER / "README.md",
        PAPER / "THEOREM_EVIDENCE_CROSS_REFERENCE.md",
        ROOT / "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex",
        ROOT / "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md",
    )
    safeguards = (
        "no ",
        "not ",
        "neither ",
        "absence ",
        "without ",
        "limitation",
        "AI ",
        "any claim ",
        "claims of ",
        "rather than ",
    )
    for path in files:
        source = path.read_text(encoding="utf-8")
        for sentence in re.split(r"(?<=[.!?])\s+", source):
            lowered = sentence.lower()
            if "human review" not in lowered and "peer review" not in lowered:
                continue
            if not any(word.lower() in lowered for word in safeguards):
                fail(f"unqualified review claim in {path.relative_to(ROOT)}: {sentence}")


def command_output(args: list[str]) -> str:
    completed = subprocess.run(args, check=True, text=True, capture_output=True)
    return completed.stdout


def pdf_pages(path: Path) -> int:
    info = command_output(["pdfinfo", str(path)])
    match = re.search(r"^Pages:\s+(\d+)\s*$", info, re.MULTILINE)
    if not match:
        fail(f"could not read page count from {path}")
    return int(match.group(1))


def check_compiled_artifacts(pdf_dir: Path) -> None:
    cases = (
        ("JENSEN_TWO_THIRDS_MAIN", 35, 55),
        ("JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT", 8, 25),
    )
    for stem, minimum, maximum in cases:
        pdf = pdf_dir / f"{stem}.pdf"
        log = pdf_dir / f"{stem}.log"
        if not pdf.is_file() or not log.is_file():
            fail(f"missing compiled artifact for {stem}")
        pages = pdf_pages(pdf)
        if not minimum <= pages <= maximum:
            fail(f"{stem} page count {pages} is outside [{minimum}, {maximum}]")
        log_text = log.read_text(encoding="utf-8", errors="replace")
        warnings = re.findall(
            r"(?:LaTeX Warning|Package .* Warning|Overfull \\hbox|Underfull \\hbox|undefined references|multiply defined)",
            log_text,
        )
        if warnings:
            fail(f"{stem} compile log contains layout/reference warnings: {warnings}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-dir", type=Path)
    args = parser.parse_args()

    check_references()
    check_load_bearing_sources()
    check_review_language()
    if args.pdf_dir is not None:
        check_compiled_artifacts(args.pdf_dir.resolve())
    print("PASS expanded manuscript sources, equations, references, review language, and PDFs")


if __name__ == "__main__":
    main()
