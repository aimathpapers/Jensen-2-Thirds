#!/usr/bin/env python3
"""Deterministic statement/typography checks for the repaired Phase-21 notes."""

from pathlib import Path


PHASE_DIR = Path(__file__).resolve().parent
FILES = (
    PHASE_DIR / "C48_LEADING_CONTOUR_LOCALIZATION.md",
    PHASE_DIR / "C48_HIGHER_THETA_MODES.md",
    PHASE_DIR / "C48_XI_COEFFICIENT_ASSEMBLY.md",
)


def require(text: str, needle: str, source: Path) -> None:
    if needle not in text:
        raise SystemExit(f"FAIL: missing {needle!r} in {source.name}")


def main() -> None:
    for source in FILES:
        text = source.read_text(encoding="utf-8")
        if "\x0c" in text:
            raise SystemExit(f"FAIL: form-feed LaTeX corruption in {source.name}")
        if text.count(r"\[") != text.count(r"\]"):
            raise SystemExit(f"FAIL: unbalanced display delimiters in {source.name}")

    leading = FILES[0].read_text(encoding="utf-8")
    assembly = FILES[2].read_text(encoding="utf-8")
    require(leading, "theta_1=1/100", FILES[0])
    require(leading, "|b|<0.012<1/20", FILES[0])
    require(assembly, "theta_0=1/400", FILES[2])
    require(assembly, "theta_1=1/200", FILES[2])
    require(assembly, r"=-\frac1{6N^2}+O(1/N^3)", FILES[2])
    print("PASS: Phase 21 repaired note statements and display delimiters")


if __name__ == "__main__":
    main()
