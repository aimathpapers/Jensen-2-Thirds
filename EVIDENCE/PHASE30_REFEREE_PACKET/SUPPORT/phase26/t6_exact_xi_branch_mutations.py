#!/usr/bin/env python3
"""Fail closed on mutations of the exact-xi finite branch certificate."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/ExactXiBranch.lean"

REQUIRED = {
    "certificate": ("structure ExactXiSaddleIntervalCertificate", 1),
    "order two sign": ("|-((n : ℝ) * L) *", 1),
    "order three scale": ("|((n : ℝ) ^ 2 * L / 2) *", 1),
    "order four sign": ("|-((n : ℝ) ^ 3 * L / 2) *", 1),
    "order five scale": ("|((n : ℝ) ^ 4 * L / 6) *", 1),
    "corrected auxiliary coordinate": ("exactXiAuxiliarySecondDiff n", 4),
    "saddle definition": ("exactXiSaddleParameterMap n L", 1),
    "limiting saddle": ("leadingXiSaddleVector", 5),
    "norm bridge": ("theorem ExactXiSaddleIntervalCertificate.norm_sub_le", 1),
    "decomposition source": ("exactXiParameterMap_eq_elementary_add_saddle", 2),
    "residual branch source": ("exactElementaryAffine_positiveParameterBranch", 1),
    "exact branch": ("noncomputable def exactXi_positiveParameterBranch", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS exact xi branch source contract")
    mutations = {
        "order two sign reversed": ("|-((n : ℝ) * L) *", "|((n : ℝ) * L) *"),
        "order three factor dropped": ("^ 2 * L / 2", "^ 2 * L"),
        "order four sign reversed": ("|-((n : ℝ) ^ 3", "|((n : ℝ) ^ 3"),
        "order five factor changed": ("^ 4 * L / 6", "^ 4 * L / 5"),
        "auxiliary coordinate disconnected":
            ("exactXiAuxiliarySecondDiff n", "uncheckedXiSaddleCoordinate n"),
        "saddle definition disconnected":
            ("exactXiSaddleParameterMap n L", "uncheckedXiSaddle n L"),
        "limiting saddle disconnected":
            ("leadingXiSaddleVector", "uncheckedLeadingSaddle"),
        "norm bridge disconnected":
            ("theorem ExactXiSaddleIntervalCertificate.norm_sub_le",
             "theorem uncheckedSaddleNorm"),
        "decomposition disconnected":
            ("exactXiParameterMap_eq_elementary_add_saddle",
             "uncheckedXiDecomposition"),
        "residual branch disconnected":
            ("exactElementaryAffine_positiveParameterBranch",
             "uncheckedAffineBranch"),
        "exact branch disconnected":
            ("noncomputable def exactXi_positiveParameterBranch",
             "noncomputable def uncheckedXiBranch"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS exact xi branch mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
