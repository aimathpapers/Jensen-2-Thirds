#!/usr/bin/env python3
"""Validate the Phase-25 baseline, assurance matrix, and proof metadata."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import flint
import mpmath
import sympy


ROOT = Path(__file__).resolve().parents[2]
PHASE = ROOT / "ground_zero_work/phase25"
LEAN_ROOT = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23"
EXPECTED_IDS = [f"T{i}" for i in range(1, 19)]
ACCEPTED_CHANNELS = {
    "arb_acb",
    "exact_cas",
    "high_precision",
    "lean_kernel",
    "paper_proof",
    "primary_source",
    "separated_ai_review",
}
CLAIM_KEYS = {
    "id",
    "statement",
    "critical",
    "dependencies",
    "external_inputs",
    "paper_source",
    "lean_declarations",
    "channels",
    "assurance",
    "remaining_boundary",
    "upgrade_phase",
}
EXPECTED_PAPER_SOURCES = {
    "T1": "Expanded main paper Section 4; Phase 21 Mellin reconstruction",
    "T2": "Expanded main paper Lemma 5.1; Phase 21 Lemma S proof",
    "T3": "Expanded main paper Section 6; Phase 21 leading contour localization",
    "T4": "Expanded main paper Section 7; Phase 21 higher-theta-mode proof",
    "T5": "Expanded main paper Theorem 7.1; Phase 21 xi-coefficient assembly",
    "T6": "Expanded main paper Section 8; Phase 18 complex sixth saddle",
    "T7": "Expanded main paper Lemma 9.1",
    "T8": "Expanded main paper Section 10; Phase 14 elementary C1 proof",
    "T9": "Expanded main paper Section 11; Phase 15 full C1 branch",
    "T10": "Expanded main paper Section 12; Szegő Jacobi theory",
    "T11": "Expanded main paper Section 12; MMP v3 Propositions 2.7(iii) and 2.17",
    "T12": "Expanded main paper Section 12; Phase 16 ratio-free localization",
    "T13": "Expanded main paper Section 13; Phase 16 direct recurrence",
    "T14": "Expanded main paper Section 14; Phase 16 uniform radius proof",
    "T15": "Expanded main paper Section 15; Phase 18 sixth residual",
    "T16": "Expanded main paper Lemma 16.1; Phase 20 multiplier reproving",
    "T17": "Expanded main paper Section 16",
    "T18": "Expanded main paper Theorem 1.1 and Sections 15--17",
}


class MetadataError(AssertionError):
    """A Phase-25 metadata invariant failed."""


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def assert_ancestor(older: str, newer: str, label: str) -> None:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", older, newer],
        cwd=ROOT,
        check=False,
    )
    if result.returncode != 0:
        raise MetadataError(f"{label}: {older} is not an ancestor of {newer}")


def validate_graph(graph: dict[str, Any]) -> None:
    if set(graph) != {"version", "external_inputs", "nodes"}:
        raise MetadataError("dependency graph top-level keys changed")
    if graph["version"] != 1:
        raise MetadataError("dependency graph version must be 1")
    nodes = graph["nodes"]
    if list(nodes) != EXPECTED_IDS:
        raise MetadataError("dependency graph must contain ordered T1--T18")
    external = set(graph["external_inputs"])
    if external != {"Jacobi", "MMP", "MSS", "Stirling"}:
        raise MetadataError("external-input inventory contains a stale or missing seam")
    for claim_id, node in nodes.items():
        if set(node) != {"internal", "external"}:
            raise MetadataError(f"malformed graph node {claim_id}")
        if len(node["internal"]) != len(set(node["internal"])):
            raise MetadataError(f"duplicate internal dependency in {claim_id}")
        if len(node["external"]) != len(set(node["external"])):
            raise MetadataError(f"duplicate external dependency in {claim_id}")
        if not set(node["internal"]) <= set(EXPECTED_IDS):
            raise MetadataError(f"unknown internal dependency in {claim_id}")
        if not set(node["external"]) <= external:
            raise MetadataError(f"unknown external dependency in {claim_id}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise MetadataError(f"dependency cycle through {node}")
        if node in visited:
            return
        visiting.add(node)
        for dependency in nodes[node]["internal"]:
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for claim_id in EXPECTED_IDS:
        visit(claim_id)
    required_edges = {
        ("T3", "T2"),
        ("T5", "T1"),
        ("T6", "T5"),
        ("T9", "T8"),
        ("T14", "T12"),
        ("T14", "T13"),
        ("T15", "T6"),
        ("T15", "T7"),
        ("T15", "T9"),
        ("T15", "T14"),
        ("T16", "T15"),
        ("T17", "T16"),
    }
    for consumer, dependency in required_edges:
        if dependency not in nodes[consumer]["internal"]:
            raise MetadataError(f"missing critical edge {dependency} -> {consumer}")
    if nodes["T18"]["internal"] != EXPECTED_IDS[:-1]:
        raise MetadataError("T18 must expose every T1--T17 dependency")
    if nodes["T15"]["external"]:
        raise MetadataError("T15 must derive Hermite--Genocchi internally")


def validate_schema(schema: dict[str, Any]) -> None:
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        raise MetadataError("assurance schema draft changed")
    if set(schema.get("required", [])) != {"version", "date", "policy", "claims"}:
        raise MetadataError("assurance schema top-level requirements changed")
    claim_schema = schema["properties"]["claims"]["items"]
    if set(claim_schema.get("required", [])) != CLAIM_KEYS:
        raise MetadataError("assurance schema claim requirements drifted")
    channel_enum = set(claim_schema["properties"]["channels"]["items"]["enum"])
    if channel_enum != ACCEPTED_CHANNELS:
        raise MetadataError("assurance schema channel enum drifted")


def validate_assurance(matrix: dict[str, Any], graph: dict[str, Any]) -> None:
    if set(matrix) != {"version", "date", "policy", "claims"}:
        raise MetadataError("assurance matrix top-level keys changed")
    if matrix["version"] != 1 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", matrix["date"]):
        raise MetadataError("assurance matrix version/date invalid")
    if not matrix["policy"].strip():
        raise MetadataError("assurance policy is empty")
    claims = matrix["claims"]
    if [claim["id"] for claim in claims] != EXPECTED_IDS:
        raise MetadataError("assurance matrix must contain ordered T1--T18")
    lean_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(LEAN_ROOT.rglob("*.lean"))
    )
    for claim in claims:
        claim_id = claim["id"]
        if set(claim) != CLAIM_KEYS:
            raise MetadataError(f"claim keys changed for {claim_id}")
        if claim["assurance"] not in {"green", "amber", "red"}:
            raise MetadataError(f"invalid assurance color for {claim_id}")
        if not isinstance(claim["critical"], bool):
            raise MetadataError(f"critical flag is not Boolean for {claim_id}")
        if claim["dependencies"] != graph["nodes"][claim_id]["internal"]:
            raise MetadataError(f"internal dependency drift for {claim_id}")
        if claim["external_inputs"] != graph["nodes"][claim_id]["external"]:
            raise MetadataError(f"external dependency drift for {claim_id}")
        channels = claim["channels"]
        if len(channels) < 2 or len(channels) != len(set(channels)):
            raise MetadataError(f"insufficient or duplicate channels for {claim_id}")
        if not set(channels) <= ACCEPTED_CHANNELS:
            raise MetadataError(f"unknown verification channel for {claim_id}")
        if bool(claim["lean_declarations"]) != ("lean_kernel" in channels):
            raise MetadataError(
                f"Lean channel/declaration mismatch for {claim_id}"
            )
        if not claim["paper_source"].strip() or not claim["remaining_boundary"].strip():
            raise MetadataError(f"missing paper source or boundary for {claim_id}")
        if claim["paper_source"] != EXPECTED_PAPER_SOURCES[claim_id]:
            raise MetadataError(f"stale paper source mapping for {claim_id}")
        if not re.fullmatch(r"Phase [A-N]", claim["upgrade_phase"]):
            raise MetadataError(f"invalid upgrade phase for {claim_id}")
        if claim["assurance"] == "green":
            independent_exact = {"exact_cas", "arb_acb", "primary_source"}
            if "lean_kernel" not in channels and not (
                "paper_proof" in channels
                and "separated_ai_review" in channels
                and independent_exact.intersection(channels)
                and len(channels) >= 3
            ):
                raise MetadataError(f"green claim lacks sufficient channels: {claim_id}")
        if claim["assurance"] == "red":
            raise MetadataError(f"baseline assurance matrix contains red claim {claim_id}")
        for declaration in claim["lean_declarations"]:
            prefix = "Zeta23.Research.JensenWedge."
            if not declaration.startswith(prefix):
                raise MetadataError(f"unscoped Lean declaration for {claim_id}")
            short = declaration.removeprefix(prefix)
            if f"theorem {short}" not in lean_text:
                raise MetadataError(f"missing Lean declaration {declaration}")
    t15 = next(claim for claim in claims if claim["id"] == "T15")
    required_t15 = {
        "Zeta23.Research.JensenWedge.sixNode_newton_identity",
        "Zeta23.Research.JensenWedge.hermiteGenocchiSix_newton_identityOn",
        "Zeta23.Research.JensenWedge.hermiteGenocchiSix_remainder_bound_of_derivative_tower",
        "Zeta23.Research.JensenWedge.hermiteGenocchiSix_remainder_bound_on",
    }
    if not required_t15 <= set(t15["lean_declarations"]):
        raise MetadataError("T15 must map the local Newton/HG producer surface")
    if t15["external_inputs"]:
        raise MetadataError("T15 must not retain a stale external HG input")


def validate_baseline(baseline: dict[str, Any]) -> None:
    commits = (
        baseline["implementation_baseline_commit"],
        baseline["mathematical_candidate_commit"],
        baseline["required_checkpoint"],
        baseline["mathlib_commit"],
    )
    if not all(re.fullmatch(r"[0-9a-f]{40}", value) for value in commits):
        raise MetadataError("baseline contains malformed commit hash")
    head = git("rev-parse", "HEAD")
    assert_ancestor(
        baseline["implementation_baseline_commit"],
        head,
        "implementation baseline",
    )
    assert_ancestor(
        baseline["mathematical_candidate_commit"],
        baseline["implementation_baseline_commit"],
        "mathematical candidate",
    )
    assert_ancestor(
        baseline["required_checkpoint"],
        baseline["mathematical_candidate_commit"],
        "required checkpoint",
    )
    lean_project = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    lake_manifest = load_json(lean_project / "lake-manifest.json")
    mathlib_entries = [
        package
        for package in lake_manifest.get("packages", [])
        if package.get("name") == "mathlib"
    ]
    if len(mathlib_entries) != 1:
        raise MetadataError("lake-manifest.json must pin exactly one Mathlib package")
    mathlib_entry = mathlib_entries[0]
    if (
        mathlib_entry.get("type") != "git"
        or mathlib_entry.get("rev") != baseline["mathlib_commit"]
    ):
        raise MetadataError("Mathlib manifest revision differs from baseline")
    mathlib_checkout = lean_project / ".lake/packages/mathlib"
    if mathlib_checkout.is_dir():
        mathlib = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=mathlib_checkout, text=True
        ).strip()
        if mathlib != baseline["mathlib_commit"]:
            raise MetadataError("Mathlib checkout differs from baseline")
    if baseline["serial_order"] != ["phase24", "phase21", "phase20"]:
        raise MetadataError("serial verification order changed")
    expected_tools = baseline["toolchain"]
    actual_python = {
        "python": sys.version.split()[0],
        "sympy": sympy.__version__,
        "mpmath": mpmath.__version__,
        "python_flint": flint.__version__,
    }
    for name, actual in actual_python.items():
        if expected_tools[name] != actual:
            raise MetadataError(f"{name} version differs: {actual}")
    # Calling ``lake env lean`` initializes missing Lake packages, which turns a
    # metadata-only clean-archive check into an unnecessary network operation.
    # The Elan shim reads the pinned lean-toolchain file directly.
    lean_version = subprocess.check_output(
        ["lean", "--version"], cwd=lean_project, text=True
    )
    if expected_tools["lean"].split()[0] not in lean_version or expected_tools[
        "lean"
    ].split()[1] not in lean_version:
        raise MetadataError("Lean version/commit differs from baseline")
    lake_version = subprocess.check_output(
        ["lake", "--version"], cwd=lean_project, text=True
    )
    if expected_tools["lake"] not in lake_version:
        raise MetadataError("Lake version differs from baseline")
    tectonic_version = subprocess.check_output(
        ["tectonic", "--version"], cwd=ROOT, text=True
    )
    if expected_tools["tectonic"] not in tectonic_version:
        raise MetadataError("Tectonic version differs from baseline")
    for relative, marker in baseline["verification_markers"].items():
        source = ROOT / relative
        if not source.is_file() or marker not in source.read_text(encoding="utf-8"):
            raise MetadataError(f"missing baseline verification marker in {relative}")


def validate_asymptotic_ledger(ledger: dict[str, Any]) -> None:
    if set(ledger) != {"version", "source", "patterns", "entries"}:
        raise MetadataError("asymptotic ledger top-level keys changed")
    source = ROOT / ledger["source"]
    lines = source.read_text(encoding="utf-8").splitlines()
    found: dict[int, list[str]] = {}
    for line_number, line in enumerate(lines, start=1):
        matches = [pattern for pattern in ledger["patterns"] if pattern in line]
        if matches:
            found[line_number] = matches
    entries = ledger["entries"]
    if [entry["id"] for entry in entries] != [f"A{i:03d}" for i in range(1, 20)]:
        raise MetadataError("asymptotic ledger IDs are not A001--A019")
    recorded = {entry["line"]: entry["terms"] for entry in entries}
    if recorded != found:
        raise MetadataError(
            f"asymptotic-language inventory drift: recorded={recorded}, found={found}"
        )
    for entry in entries:
        if entry["owner"] not in EXPECTED_IDS:
            raise MetadataError(f"unknown asymptotic owner {entry['owner']}")
        if not re.fullmatch(r"Phase [A-N]", entry["upgrade_phase"]):
            raise MetadataError(f"invalid asymptotic upgrade phase {entry['id']}")
        if entry["text"] not in lines[entry["line"] - 1]:
            raise MetadataError(f"asymptotic source text drift at {entry['id']}")


def validate_companions() -> None:
    crosswalk = (PHASE / "NOTATION_NORMALIZATION_CROSSWALK.md").read_text(
        encoding="utf-8"
    )
    required_crosswalk = (
        "factor-eight identity",
        "n^2 log(n+2) >= K d^3",
        "N=2x-2",
        "(2,-2,4,-12,48)",
        "(4+4r-3sigma)^12",
        "A>B>C>D>0",
        "D/(AC)",
        "lmesh(p)=min lambda_j/lambda_(j+1) >= 1",
        "C_loc=12+8 sqrt(6)<32",
        "1/6!=1/720",
        "y^k p^(k)(y)/p(y)",
        "not human or peer",
    )
    for marker in required_crosswalk:
        if marker not in crosswalk:
            raise MetadataError(f"normalization crosswalk missing {marker!r}")
    graph_markdown = (PHASE / "PROOF_DEPENDENCY_GRAPH.md").read_text(
        encoding="utf-8"
    )
    for claim_id in EXPECTED_IDS:
        if claim_id not in graph_markdown:
            raise MetadataError(f"rendered dependency graph missing {claim_id}")
    assurance_markdown = (PHASE / "THEOREM_ASSURANCE_MATRIX.md").read_text(
        encoding="utf-8"
    )
    for claim_id in EXPECTED_IDS:
        if f"| {claim_id} |" not in assurance_markdown:
            raise MetadataError(f"rendered assurance matrix missing {claim_id}")
    if "AI pre-review, not human or peer review" not in assurance_markdown:
        raise MetadataError("rendered assurance matrix review disclosure missing")


def main() -> None:
    baseline = load_json(PHASE / "PHASE25_BASELINE.json")
    schema = load_json(PHASE / "THEOREM_ASSURANCE_MATRIX.schema.json")
    graph = load_json(PHASE / "PROOF_DEPENDENCY_GRAPH.json")
    matrix = load_json(PHASE / "THEOREM_ASSURANCE_MATRIX.json")
    ledger = load_json(PHASE / "ASYMPTOTIC_LANGUAGE_LEDGER.json")
    validate_schema(schema)
    validate_graph(graph)
    validate_assurance(matrix, graph)
    validate_baseline(baseline)
    validate_asymptotic_ledger(ledger)
    validate_companions()
    print(
        "PASS Phase-25 metadata: baseline ancestry/logs, T1--T18 assurance, "
        "acyclic dependencies, Lean declarations, normalizations, and "
        "asymptotic-language inventory"
    )


if __name__ == "__main__":
    main()
