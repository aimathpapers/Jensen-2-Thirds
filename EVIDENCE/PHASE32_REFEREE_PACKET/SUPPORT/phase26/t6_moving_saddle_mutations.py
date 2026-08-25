#!/usr/bin/env python3
"""Fail-closed mutations for the concrete moving-saddle sixth bound."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/MovingSaddleSixth.lean"
)


class ContractError(RuntimeError):
    """The moving-saddle source contract changed."""


REQUIRED = {
    "inverse coordinate": "1 / quantitativeSaddleBranch N",
    "sigma orientation": "quantitativeSaddleBranch N / N",
    "curvature definition": "def manuscriptSaddleQ",
    "G0 definition": "def manuscriptSaddleG0",
    "G0 first term": "(N + 1) * log (quantitativeSaddleBranch N)",
    "G0 curvature term": "log (manuscriptSaddleQ N) / 2",
    "reduced value": "def manuscriptSaddleMainSix",
    "power five": "N ^ 5 * quantitativeSaddleBranch N",
    "identification record": "structure ManuscriptG0SixthIdentification",
    "exact derivative identity":
        "iteratedDeriv 6 manuscriptSaddleG0 N = manuscriptSaddleMainSix N",
    "coordinate box theorem": "theorem manuscriptSaddle_scaled_coordinates_in_box",
    "lower-bound theorem":
        "theorem quantitativeSaddleBranch_norm_lower_half_realLog",
    "half log": "Real.log ‖N‖ / 2 ≤ ‖quantitativeSaddleBranch N‖",
    "H6 theorem": "theorem manuscriptSaddleH6_norm_lt_tenThousand",
    "H6 source": "saddleH6_norm_lt_tenThousand hr hsigma",
    "main bound theorem": "theorem manuscriptSaddleMainSix_norm_le",
    "main bound": "20000 / (‖N‖ ^ 5 * Real.log ‖N‖)",
    "derivative consumer":
        "theorem iteratedDeriv_six_manuscriptSaddleG0_norm_le",
    "identification use": "rw [I.exact_value]",
}

COUNTS = {
    "1 / quantitativeSaddleBranch N": 1,
    "quantitativeSaddleBranch N / N": 1,
    "N ^ 5 * quantitativeSaddleBranch N": 1,
    "Real.log ‖N‖ / 2 ≤ ‖quantitativeSaddleBranch N‖": 1,
    "20000 / (‖N‖ ^ 5 * Real.log ‖N‖)": 3,
}


def validate(text: str) -> None:
    for label, needle in REQUIRED.items():
        if text.count(needle) != COUNTS.get(needle, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T6 moving-saddle source contract")
    mutations = {
        "inverse coordinate reversed": (
            "1 / quantitativeSaddleBranch N", "quantitativeSaddleBranch N"),
        "sigma coordinate reversed": (
            "quantitativeSaddleBranch N / N", "N / quantitativeSaddleBranch N"),
        "curvature removed": ("def manuscriptSaddleQ", "def uncheckedSaddleQ"),
        "G0 removed": ("def manuscriptSaddleG0", "def uncheckedSaddleG0"),
        "G0 leading shift changed": ("(N + 1) * log", "(N - 1) * log"),
        "G0 curvature sign changed": (
            "log (manuscriptSaddleQ N) / 2",
            "log (manuscriptSaddleQ N) / 3",
        ),
        "reduced value removed": (
            "def manuscriptSaddleMainSix", "def uncheckedSaddleMainSix"),
        "power changed": (
            "N ^ 5 * quantitativeSaddleBranch N",
            "N ^ 6 * quantitativeSaddleBranch N",
        ),
        "identification renamed": (
            "structure ManuscriptG0SixthIdentification",
            "structure UncheckedG0SixthIdentification",
        ),
        "derivative order changed": (
            "iteratedDeriv 6 manuscriptSaddleG0 N",
            "iteratedDeriv 5 manuscriptSaddleG0 N",
        ),
        "box theorem removed": (
            "theorem manuscriptSaddle_scaled_coordinates_in_box",
            "theorem uncheckedCoordinatesInBox",
        ),
        "half log weakened": (
            "Real.log ‖N‖ / 2 ≤ ‖quantitativeSaddleBranch N‖",
            "Real.log ‖N‖ / 3 ≤ ‖quantitativeSaddleBranch N‖",
        ),
        "H6 source disconnected": (
            "saddleH6_norm_lt_tenThousand hr hsigma",
            "uncheckedH6Bound hr hsigma",
        ),
        "constant changed": (
            "20000 / (‖N‖ ^ 5 * Real.log ‖N‖)",
            "21000 / (‖N‖ ^ 5 * Real.log ‖N‖)",
        ),
        "identification disconnected": (
            "rw [I.exact_value]", "rw [uncheckedExactValue]"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 moving-saddle mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
