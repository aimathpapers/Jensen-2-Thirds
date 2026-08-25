#!/usr/bin/env python3
"""Independent static audit of the frozen Phase-L Lean review packet.

The program derives its inventory from Lean source declarations, the assurance
matrix, and the bundled ``#print axioms`` driver.  It does not read any frozen
PASS log or expected-result file, and it contains no expected declaration
counts or hashes.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DECL_RE = re.compile(
    r"(?m)^\s*(?:private\s+)?(?:noncomputable\s+)?"
    r"(?:theorem|lemma|def|structure|abbrev|opaque|class|instance)\s+"
    r"([A-Za-z_][A-Za-z0-9_'.]*)"
)
PRINT_AXIOMS_RE = re.compile(r"(?m)^\s*#print\s+axioms\s+(\S+)\s*$")
FORBIDDEN_RE = re.compile(
    r"\b(sorry|admit|axiom|unsafe|native_decide|implemented_by)\b"
)
LEAN_NAMESPACE = "Zeta23.Research.JensenWedge."


def strip_comments_and_strings(text: str) -> str:
    """Remove Lean line comments, nested block comments, and string contents."""
    output: list[str] = []
    i = 0
    block_depth = 0
    in_string = False
    while i < len(text):
        if block_depth:
            if text.startswith("/-", i):
                block_depth += 1
                output.extend("  ")
                i += 2
            elif text.startswith("-/", i):
                block_depth -= 1
                output.extend("  ")
                i += 2
            else:
                output.append("\n" if text[i] == "\n" else " ")
                i += 1
            continue
        if in_string:
            if text[i] == "\\" and i + 1 < len(text):
                output.extend("  ")
                i += 2
            elif text[i] == '"':
                in_string = False
                output.append(" ")
                i += 1
            else:
                output.append("\n" if text[i] == "\n" else " ")
                i += 1
            continue
        if text.startswith("--", i):
            newline = text.find("\n", i)
            if newline == -1:
                output.extend(" " * (len(text) - i))
                break
            output.extend(" " * (newline - i))
            i = newline
        elif text.startswith("/-", i):
            block_depth = 1
            output.extend("  ")
            i += 2
        elif text[i] == '"':
            in_string = True
            output.append(" ")
            i += 1
        else:
            output.append(text[i])
            i += 1
    return "".join(output)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "packet_root",
        type=Path,
        help="Extracted Jensen_Two_Thirds_Phase25_Lean_AI_Review_Packet directory",
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    packet_root = args.packet_root.resolve()
    lean_root = (
        packet_root
        / "evidence"
        / "Kimi_Agent_Riemann Lean Exploration"
        / "zeta-23-lean"
        / "Zeta23"
        / "Research"
    )
    source_files = [lean_root / "JensenWedge.lean"]
    source_files.extend(sorted((lean_root / "JensenWedge").glob("*.lean")))

    declarations: dict[str, dict[str, object]] = {}
    escape_hits: list[dict[str, object]] = []
    for source_file in source_files:
        raw = source_file.read_text(encoding="utf-8")
        clean = strip_comments_and_strings(raw)
        for match in DECL_RE.finditer(clean):
            short_name = match.group(1)
            full_name = (
                short_name
                if short_name.startswith("Zeta23.")
                else LEAN_NAMESPACE + short_name
            )
            declarations[full_name] = {
                "file": str(source_file.relative_to(packet_root)),
                "line": line_number(clean, match.start()),
            }
        for match in FORBIDDEN_RE.finditer(clean):
            escape_hits.append(
                {
                    "token": match.group(1),
                    "file": str(source_file.relative_to(packet_root)),
                    "line": line_number(clean, match.start()),
                }
            )

    matrix_path = (
        packet_root
        / "evidence"
        / "ground_zero_work"
        / "phase25"
        / "THEOREM_ASSURANCE_MATRIX.json"
    )
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    mapped_by_claim: dict[str, list[str]] = {
        claim["id"]: claim.get("lean_declarations", [])
        for claim in matrix["claims"]
    }
    mapped = sorted({name for names in mapped_by_claim.values() for name in names})
    mapped_missing_from_source = [name for name in mapped if name not in declarations]

    channel_conflicts: list[dict[str, object]] = []
    for claim in matrix["claims"]:
        channels = set(claim.get("channels", []))
        names = claim.get("lean_declarations", [])
        if "lean_kernel" in channels and not names:
            channel_conflicts.append(
                {
                    "claim": claim["id"],
                    "conflict": "lean_kernel channel but no named Lean declaration",
                }
            )
        if names and "lean_kernel" not in channels:
            channel_conflicts.append(
                {
                    "claim": claim["id"],
                    "conflict": "named Lean declarations but no lean_kernel channel",
                }
            )

    axiom_driver = (
        packet_root
        / "evidence"
        / "ground_zero_work"
        / "phase20"
        / "Phase20Axioms.lean"
    )
    audited_axioms = set(
        PRINT_AXIOMS_RE.findall(axiom_driver.read_text(encoding="utf-8"))
    )
    mapped_without_axiom_print = [name for name in mapped if name not in audited_axioms]

    result = {
        "packet_root": str(packet_root),
        "lean_source_files": len(source_files),
        "source_declarations": len(declarations),
        "forbidden_token_hits": escape_hits,
        "matrix_mapped_declarations": len(mapped),
        "matrix_mapped_missing_from_source": mapped_missing_from_source,
        "matrix_channel_conflicts": channel_conflicts,
        "axiom_print_declarations": len(audited_axioms),
        "matrix_mapped_with_axiom_print": len(set(mapped) & audited_axioms),
        "matrix_mapped_without_axiom_print": mapped_without_axiom_print,
    }

    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"Lean source files: {result['lean_source_files']}")
        print(f"Source declarations: {result['source_declarations']}")
        print(f"Forbidden-token hits: {len(escape_hits)}")
        print(f"Unique matrix-mapped declarations: {len(mapped)}")
        print(f"Mapped names missing from source: {len(mapped_missing_from_source)}")
        print("Matrix/channel conflicts:")
        for conflict in channel_conflicts:
            print(f"  {conflict['claim']}: {conflict['conflict']}")
        print(
            "Mapped declarations covered by bundled #print axioms driver: "
            f"{result['matrix_mapped_with_axiom_print']}/{len(mapped)}"
        )
        print("Mapped declarations without bundled #print axioms coverage:")
        for name in mapped_without_axiom_print:
            print(f"  {name}")

    return 1 if escape_hits or mapped_missing_from_source else 0


if __name__ == "__main__":
    raise SystemExit(main())
