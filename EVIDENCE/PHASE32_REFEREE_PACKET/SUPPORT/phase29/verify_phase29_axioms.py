#!/usr/bin/env python3
"""Check exact axiom output for the two Palomar T5 solution declarations."""

from __future__ import annotations

import sys


EXPECTED = {
    "centered_xi_continuation_agrees_at_positive_integers",
    "sectorial_centered_xi_coefficient_asymptotic",
    "sectorial_centered_xi_error_derivatives_through_six",
}
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}


def main() -> None:
    text = sys.stdin.read()
    seen: set[str] = set()
    for name in EXPECTED:
        marker = f"'{name}' depends on axioms: ["
        start = text.find(marker)
        if start < 0:
            raise SystemExit(f"FAIL missing axiom line for {name}")
        end = text.find("]", start)
        if end < 0:
            raise SystemExit(f"FAIL malformed axiom line for {name}")
        body = text[start + len(marker):end]
        axioms = {part.strip() for part in body.split(",") if part.strip()}
        if axioms != ALLOWED:
            raise SystemExit(f"FAIL {name} axioms {sorted(axioms)}")
        seen.add(name)
    if seen != EXPECTED:
        raise SystemExit("FAIL incomplete theorem audit")
    print("PASS Palomar T5 exact terminal axiom audit")


if __name__ == "__main__":
    main()
