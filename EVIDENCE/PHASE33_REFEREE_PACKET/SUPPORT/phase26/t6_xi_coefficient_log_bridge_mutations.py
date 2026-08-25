#!/usr/bin/env python3
"""Fail closed on mutations of the integer/holomorphic log bridge."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/XiCoefficientLogBridge.lean"

REQUIRED = {
    "holomorphic sampled log": ("def complexXiDiscreteCoefficientLog", 1),
    "moment continuation": ("complexXiCoefficientMoment", 2),
    "integer specialization": ("complexXiCoefficientMoment_nat_succ", 1),
    "real coefficient identity": ("ofReal_riemannXiCoefficientReal", 1),
    "positivity source": ("riemannXiCoefficientReal_pos", 1),
    "principal log source": ("Complex.ofReal_log", 1),
    "second difference": ("def complexXiSecondDiff", 1),
    "second difference sign":
        ("complexXiDiscreteCoefficientLog (m + 2) -", 1),
    "forward zero": ("def complexNatForwardDiff0", 1),
    "forward one": ("def complexNatForwardDiff1", 1),
    "forward one sign": (":= f 1 - f 0", 1),
    "forward two": ("def complexNatForwardDiff2", 1),
    "forward two coefficient": ("f 2 - 2 * f 1", 1),
    "forward three": ("def complexNatForwardDiff3", 1),
    "forward three coefficient": ("f 3 - 3 * f 2", 1),
    "final bridge": ("theorem ofReal_exactXi_secondDiff_forwardDiffs", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS xi coefficient log bridge source contract")
    mutations = {
        "integer specialization disconnected":
            ("complexXiCoefficientMoment_nat_succ", "uncheckedMomentAtInteger"),
        "real coefficient identity disconnected":
            ("ofReal_riemannXiCoefficientReal", "uncheckedRealCoefficient"),
        "positivity disconnected":
            ("riemannXiCoefficientReal_pos", "uncheckedCoefficientPositivity"),
        "principal log disconnected":
            ("Complex.ofReal_log", "uncheckedPrincipalLog"),
        "second difference sign changed":
            ("complexXiDiscreteCoefficientLog (m + 2) -",
             "complexXiDiscreteCoefficientLog (m + 2) +"),
        "first forward sign changed": (":= f 1 - f 0", ":= f 1 + f 0"),
        "second forward coefficient changed": ("f 2 - 2 * f 1", "f 2 - 3 * f 1"),
        "third forward coefficient changed": ("f 3 - 3 * f 2", "f 3 - 2 * f 2"),
        "final bridge disconnected":
            ("theorem ofReal_exactXi_secondDiff_forwardDiffs",
             "theorem uncheckedForwardDiffBridge"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS xi coefficient log bridge mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
