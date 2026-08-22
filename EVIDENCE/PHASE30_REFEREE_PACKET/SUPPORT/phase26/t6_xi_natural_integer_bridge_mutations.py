#!/usr/bin/env python3
"""Fail closed on positive-real and integer-log bridge mutations."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge"
SOURCES = {
    "real": LEAN / "PositiveRealSaddle.lean",
    "integer": LEAN / "XiNaturalLogIntegerBridge.lean",
}

REQUIRED = {
    "real": {
        "real center": "theorem saddleComparisonCenter_ofReal\n",
        "conjugate equation": "theorem sectorialSaddleEquation_conj_ofReal",
        "disc uniqueness": "hspec.2.2 (conj L) hconjmem hconjroot",
        "real saddle": "theorem quantitativeSaddleBranch_ofReal_conj",
        "imaginary part": "theorem quantitativeSaddleBranch_ofReal_im",
    },
    "integer": {
        "real saddle main": "theorem saddleMomentLogMain_ofReal_im",
        "real two shift": "theorem complexXiNaturalTwoShiftLog_ofReal_im",
        "positive natural main":
            "theorem complexXiNaturalAuxiliaryMain_ofReal_re_pos",
        "positive error factor":
            "theorem one_add_complexXiNaturalAuxiliaryRelativeError_nat_re_pos",
        "real error log": "theorem complexXiNaturalAuxiliaryLogError_nat_im",
        "principal integer bridge":
            "theorem complexXiNaturalAuxiliaryLog_nat_eq_discrete",
        "exact exponential source": "exp_complexXiNaturalAuxiliaryLog hM",
        "positive moment source":
            "simpa only [a] using riemannXiAuxiliaryMomentReal_pos m",
        "second difference": "def complexXiNaturalAuxiliarySecondDiff",
        "six-node certificate bridge":
            "theorem ofReal_exactXiAuxiliarySecondDiff_forwardDiffs_natural",
        "six samples": "j ≤ 5 →",
    },
}


def validate(texts: dict[str, str]) -> None:
    for source, contracts in REQUIRED.items():
        for label, needle in contracts.items():
            if texts[source].count(needle) != 1:
                raise RuntimeError(f"{source}: {label}")


def main() -> None:
    texts = {name: path.read_text() for name, path in SOURCES.items()}
    validate(texts)
    print("PASS xi positive-real/integer-log bridge source contract")
    mutations = {
        "conjugate uniqueness disconnected":
            ("real", "hspec.2.2 (conj L) hconjmem hconjroot",
             "uncheckedDiscUniqueness"),
        "real saddle disconnected":
            ("real", "theorem quantitativeSaddleBranch_ofReal_conj",
             "theorem uncheckedRealSaddle"),
        "positive main disconnected":
            ("integer", "theorem complexXiNaturalAuxiliaryMain_ofReal_re_pos",
             "theorem uncheckedNaturalMainPos"),
        "error branch disconnected":
            ("integer", "theorem complexXiNaturalAuxiliaryLogError_nat_im",
             "theorem uncheckedErrorLogReal"),
        "principal bridge disconnected":
            ("integer", "theorem complexXiNaturalAuxiliaryLog_nat_eq_discrete",
             "theorem uncheckedPrincipalBridge"),
        "exact exponential disconnected":
            ("integer", "exp_complexXiNaturalAuxiliaryLog hM",
             "uncheckedExactExponential hM"),
        "positive moment disconnected":
            ("integer",
             "simpa only [a] using riemannXiAuxiliaryMomentReal_pos m",
             "simpa only [a] using uncheckedAuxiliaryMomentPos m"),
        "six-node range narrowed":
            ("integer", "j ≤ 5 →", "j ≤ 4 →"),
        "certificate bridge disconnected":
            ("integer",
             "theorem ofReal_exactXiAuxiliarySecondDiff_forwardDiffs_natural",
             "theorem uncheckedNaturalForwardBridge"),
    }
    for label, (source, old, new) in mutations.items():
        changed = dict(texts)
        changed[source] = changed[source].replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS xi integer-log mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
