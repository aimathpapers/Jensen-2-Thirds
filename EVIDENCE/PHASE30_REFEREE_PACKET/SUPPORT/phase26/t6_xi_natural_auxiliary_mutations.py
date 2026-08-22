#!/usr/bin/env python3
"""Fail closed on mutations of the Gamma-free auxiliary factorization."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/XiNaturalAuxiliaryFactorization.lean"

REQUIRED = {
    "natural main": ("def complexXiNaturalAuxiliaryMain", 1),
    "Gamma-free scale": ("coefficientDyadicScale M * saddleMomentMain N *", 1),
    "two-shift denominator":
        ("coefficientMomentMultiplier N - quantitativeSaddleBranch N ^ 2", 1),
    "quotient error": ("def complexXiNaturalAuxiliaryRelativeError", 1),
    "main nonzero": ("theorem complexXiNaturalAuxiliaryMain_ne_zero", 1),
    "direct factorization":
        ("theorem complexXiAuxiliaryMoment_natural_factorization", 1),
    "two-shift producer": ("fullThetaTwoShiftAssembly", 1),
    "error identification":
        ("theorem complexXiNaturalAuxiliaryRelativeError_eq_momentError", 1),
    "main holomorphy":
        ("theorem differentiableOn_complexXiNaturalAuxiliaryMain", 1),
    "error holomorphy":
        ("theorem differentiableOn_complexXiNaturalAuxiliaryRelativeError", 1),
    "moment-only bound":
        ("theorem complexXiNaturalAuxiliaryRelativeError_norm_le", 1),
    "moment bound producer": ("complexXiMomentRelativeError_norm_le hM", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS xi natural auxiliary factorization source contract")
    mutations = {
        "dyadic scale removed":
            ("coefficientDyadicScale M * saddleMomentMain N *",
             "saddleMomentMain N *"),
        "two-shift sign reversed":
            ("coefficientMomentMultiplier N - quantitativeSaddleBranch N ^ 2",
             "coefficientMomentMultiplier N + quantitativeSaddleBranch N ^ 2"),
        "nonzero proof disconnected":
            ("theorem complexXiNaturalAuxiliaryMain_ne_zero",
             "theorem uncheckedNaturalAuxiliaryMainNeZero"),
        "factorization disconnected":
            ("theorem complexXiAuxiliaryMoment_natural_factorization",
             "theorem uncheckedNaturalAuxiliaryFactorization"),
        "two-shift producer disconnected":
            ("fullThetaTwoShiftAssembly", "uncheckedTwoShiftAssembly"),
        "error identity disconnected":
            ("theorem complexXiNaturalAuxiliaryRelativeError_eq_momentError",
             "theorem uncheckedNaturalAuxiliaryErrorIdentity"),
        "error holomorphy disconnected":
            ("theorem differentiableOn_complexXiNaturalAuxiliaryRelativeError",
             "theorem uncheckedNaturalAuxiliaryErrorHolomorphy"),
        "moment bound disconnected":
            ("complexXiMomentRelativeError_norm_le hM",
             "uncheckedNaturalAuxiliaryBound hM"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS xi natural auxiliary mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
