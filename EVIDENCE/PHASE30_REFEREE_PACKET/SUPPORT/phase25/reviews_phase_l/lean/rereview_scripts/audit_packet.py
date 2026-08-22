#!/usr/bin/env python3
"""Static correlated re-review checks for the extracted Phase-L Lean packet.

The script accepts the extracted packet root.  It never consults the working
repository and does not modify candidate evidence.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


EXPECTED_COMMIT = "6ee1db8fc5789a01bc0297f850c817f55b529be4"
PREFIX = "Zeta23.Research.JensenWedge."
ACCEPTED_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
CHANNELS = {
    "paper_proof",
    "primary_source",
    "lean_kernel",
    "exact_cas",
    "arb_acb",
    "high_precision",
    "separated_ai_review",
}
EXPECTED_T15 = {
    PREFIX + "sixNode_newton_identity",
    PREFIX + "hermiteGenocchiSix_newton_identityOn",
    PREFIX + "hermiteGenocchiSix_remainder_bound_of_derivative_tower",
    PREFIX + "hermiteGenocchiSix_remainder_bound_on",
    PREFIX + "norm_hermiteGenocchiCubeSix_le",
    PREFIX + "norm_hermiteGenocchiIntegralSix_le",
    PREFIX + "hermiteGenocchiCubePoint_mem_convex",
    PREFIX + "norm_sixNodeProduct_le",
}
DRIVER_ROW = re.compile(r"^#print axioms (?P<name>\S+)$")
OUTPUT_ROW = re.compile(
    r"'(?P<name>[^']+)' depends on axioms: \[(?P<axioms>.*?)\]",
    re.DOTALL,
)
ESCAPE = re.compile(
    r"\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by)\b"
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def strip_lean_comments_and_strings(text: str) -> str:
    """Replace Lean comments and strings while retaining line structure."""

    out: list[str] = []
    i = 0
    block_depth = 0
    in_string = False
    while i < len(text):
        if block_depth:
            if text.startswith("/-", i):
                block_depth += 1
                out.extend("  ")
                i += 2
            elif text.startswith("-/", i):
                block_depth -= 1
                out.extend("  ")
                i += 2
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif in_string:
            if text[i] == "\\" and i + 1 < len(text):
                out.extend("  ")
                i += 2
            elif text[i] == '"':
                in_string = False
                out.append(" ")
                i += 1
            else:
                out.append("\n" if text[i] == "\n" else " ")
                i += 1
        elif text.startswith("--", i):
            end = text.find("\n", i)
            if end == -1:
                out.extend(" " * (len(text) - i))
                break
            out.extend(" " * (end - i))
            out.append("\n")
            i = end + 1
        elif text.startswith("/-", i):
            block_depth = 1
            out.extend("  ")
            i += 2
        elif text[i] == '"':
            in_string = True
            out.append(" ")
            i += 1
        else:
            out.append(text[i])
            i += 1
    require(block_depth == 0, "unterminated Lean block comment")
    require(not in_string, "unterminated Lean string")
    return "".join(out)


def local_closure(lean_root: Path) -> tuple[list[str], list[tuple[str, str]]]:
    stack = ["Zeta23.Research.JensenWedge"]
    seen: set[str] = set()
    edges: list[tuple[str, str]] = []
    while stack:
        module = stack.pop()
        if module in seen:
            continue
        seen.add(module)
        source = lean_root / (module.replace(".", "/") + ".lean")
        require(source.is_file(), f"missing local import source: {module}")
        stripped = strip_lean_comments_and_strings(source.read_text(encoding="utf-8"))
        for line in stripped.splitlines():
            match = re.match(r"^\s*import\s+(.+?)\s*$", line)
            if match is None:
                continue
            for dependency in match.group(1).split():
                if dependency.startswith("Zeta23."):
                    edges.append((module, dependency))
                    stack.append(dependency)
    return sorted(seen), edges


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle_root", type=Path)
    args = parser.parse_args()
    bundle = args.bundle_root.resolve()
    phase = bundle / "evidence/ground_zero_work/phase25"
    project = bundle / "evidence/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    lean_root = project / "Zeta23"

    require(bundle.is_dir(), "bundle root is not a directory")
    require(
        (bundle / "CANDIDATE_COMMIT.txt").read_text(encoding="utf-8").strip()
        == EXPECTED_COMMIT,
        "candidate commit mismatch",
    )
    metadata = json.loads((bundle / "BUNDLE_METADATA.json").read_text(encoding="utf-8"))
    require(metadata["candidate_commit"] == EXPECTED_COMMIT, "metadata commit mismatch")
    require(metadata["review_class"].startswith("targeted correlated AI re-review"),
            "review class is not correlated AI re-review")

    matrix = json.loads((phase / "THEOREM_ASSURANCE_MATRIX.json").read_text(encoding="utf-8"))
    claims = matrix["claims"]
    require([claim["id"] for claim in claims] == [f"T{i}" for i in range(1, 19)],
            "matrix does not contain T1--T18 exactly in order")
    require(all(claim["critical"] is True for claim in claims), "non-critical matrix row")
    require(Counter(claim["assurance"] for claim in claims) == {"amber": 13, "green": 5},
            "assurance totals differ from 13 amber / 5 green")

    flattened: list[str] = []
    for claim in claims:
        channels = claim["channels"]
        require(len(channels) == len(set(channels)), f"duplicate channel in {claim['id']}")
        require(set(channels) <= CHANNELS, f"unknown channel in {claim['id']}")
        declarations = claim["lean_declarations"]
        require(("lean_kernel" in channels) == bool(declarations),
                f"Lean-channel/declaration mismatch in {claim['id']}")
        flattened.extend(declarations)
    unique_declarations = list(dict.fromkeys(flattened))
    require(len(flattened) == 67, "expected 67 claim-to-declaration incidences")
    require(len(unique_declarations) == 66, "expected 66 unique declarations")
    overlaps = {name: count for name, count in Counter(flattened).items() if count > 1}
    require(overlaps == {PREFIX + "relativeError_derivatives_through_six": 2},
            "unexpected declaration overlap")
    t15 = next(claim for claim in claims if claim["id"] == "T15")
    require(set(t15["lean_declarations"]) == EXPECTED_T15,
            "T15 does not expose the repaired producer surface")

    driver = []
    for line in (phase / "Phase25Axioms.lean").read_text(encoding="utf-8").splitlines():
        match = DRIVER_ROW.fullmatch(line)
        if match:
            driver.append(match.group("name"))
    require(driver == unique_declarations, "Phase25Axioms driver differs from matrix order")
    require(len(driver) == len(set(driver)) == 66, "axiom driver is not 66 unique rows")

    records: dict[str, set[str]] = {}
    audit_text = (phase / "PHASE25_AXIOM_AUDIT.txt").read_text(encoding="utf-8")
    for match in OUTPUT_ROW.finditer(audit_text):
        name = match.group("name")
        require(name not in records, f"duplicate frozen axiom record: {name}")
        records[name] = {
            token.strip()
            for token in match.group("axioms").replace("\n", " ").split(",")
            if token.strip()
        }
    require(list(records) == driver, "frozen axiom output differs from driver order")
    unexpected = {name: sorted(axioms - ACCEPTED_AXIOMS)
                  for name, axioms in records.items() if axioms - ACCEPTED_AXIOMS}
    require(not unexpected, f"unexpected axioms: {unexpected}")

    closure, edges = local_closure(project)
    require("Zeta23.XiPrime.Defs" in closure, "Zeta23.XiPrime.Defs absent from closure")
    require("Zeta23.Defs" in closure, "transitive Zeta23.Defs absent from closure")
    require(len(closure) == 23, f"unexpected local closure size: {len(closure)}")

    closure_texts: dict[str, str] = {}
    for module in closure:
        source = project / (module.replace(".", "/") + ".lean")
        closure_texts[module] = strip_lean_comments_and_strings(
            source.read_text(encoding="utf-8")
        )
    combined = "\n".join(closure_texts.values())
    hits = [(module, match.group(0)) for module, text in closure_texts.items()
            for match in ESCAPE.finditer(text)]
    require(not hits, f"proof escape found in local closure: {hits}")

    for declaration in driver:
        require(declaration.startswith(PREFIX), f"unscoped declaration: {declaration}")
        suffix = declaration.removeprefix(PREFIX)
        pattern = re.compile(
            r"(?m)^\s*(?:theorem|lemma)\s+" + re.escape(suffix) + r"(?:\s|\(|:)"
        )
        require(pattern.search(combined) is not None,
                f"mapped declaration not found in closure source: {declaration}")

    ledger = (bundle / "evidence/ground_zero_work/phase24/FORMALIZATION_LEDGER.md").read_text(
        encoding="utf-8"
    )
    require("Historical snapshot" in ledger and "superseded" in ledger
            and "must not be read as the current formal" in ledger,
            "historical-ledger supersession banner missing")

    analytic = closure_texts["Zeta23.Research.JensenWedge.AnalyticAdapters"]
    quantitative = closure_texts["Zeta23.Research.JensenWedge.QuantitativeBranch"]
    require("hMellin" in analytic and "SectorialSaddleCertificate" in analytic,
            "analytic boundary is not visibly typed")
    require("structure JensenWedgeAnalyticInputs" in quantitative
            and "JensenWedgeAnalyticInputs.target_hasDistinctNegativeRoots" in quantitative,
            "final conditional analytic boundary is not visibly typed")

    graph = json.loads((phase / "PROOF_DEPENDENCY_GRAPH.json").read_text(encoding="utf-8"))
    for claim in claims:
        node = graph["nodes"][claim["id"]]
        require(node["internal"] == claim["dependencies"],
                f"graph internal dependencies differ for {claim['id']}")
        require(node["external"] == claim["external_inputs"],
                f"graph external dependencies differ for {claim['id']}")

    warnings: list[str] = []
    graph_md = (phase / "PROOF_DEPENDENCY_GRAPH.md").read_text(encoding="utf-8")
    if t15["external_inputs"] == ["HG"] and "Interpolation layer:** closed" in graph_md:
        warnings.append(
            "T15 still lists HG as an external input although the graph prose and producer "
            "surface say the interpolation layer is closed"
        )
    supplement = (bundle / "manuscript/source/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex").read_text(
        encoding="utf-8"
    )
    if "The Phase-20 axiom report prints every audited declaration" in supplement:
        warnings.append(
            "supplement points to the 40-row Phase-20 report instead of the 66-row Phase-25 audit"
        )

    print(f"PASS commit and correlated-review metadata: {EXPECTED_COMMIT}")
    print("PASS exact T1--T18 map: 67 incidences, 66 unique declarations")
    print("PASS 66-row driver/frozen output: only propext, Classical.choice, Quot.sound")
    print(f"PASS local source closure: {len(closure)} modules, {len(edges)} local import edges")
    print("PASS proof-escape scan on comment/string-stripped transitive local closure")
    print("PASS historical banner and typed analytic boundaries")
    for warning in warnings:
        print(f"WARN {warning}")


if __name__ == "__main__":
    main()
