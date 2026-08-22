#!/usr/bin/env python3
"""Fail closed on natural-log certificate decomposition mutations."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge/XiNaturalLogCertificateDecomposition.lean"
)

REQUIRED = {
    "single cutoff domain": "theorem nat_mem_leanXiCoefficientSector",
    "six samples": "theorem nat_six_samples_mem_leanXiCoefficientSector",
    "proportional disc producer":
        "manuscriptCauchy_closedBall_subset_sector hm",
    "forward-difference linearity": "theorem complexForwardDiff_add",
    "second-difference identification":
        "theorem complexXiNaturalAuxiliarySecondDiff_eq_forwardDiff",
    "exact four-coordinate decomposition":
        "theorem ofReal_exactXiAuxiliarySecondDiff_forwardDiffs_decomposition",
    "integer-log bridge consumer":
        "ofReal_exactXiAuxiliarySecondDiff_forwardDiffs_natural hnpos",
    "main term order five":
        "complexForwardDiff 5 complexXiNaturalAuxiliaryLogMain",
    "error term order five":
        "complexForwardDiff 5 complexXiNaturalAuxiliaryLogError",
    "four Cauchy bounds":
        "theorem complexXiNaturalAuxiliaryLogError_certificate_bounds",
    "localized error producer":
        "complexXiNaturalAuxiliaryLogError_forwardDiff_bound hn",
}


def validate(text: str) -> None:
    for label, needle in REQUIRED.items():
        if text.count(needle) < 1:
            raise RuntimeError(label)
    if text.count("complexXiNaturalAuxiliaryLogError_forwardDiff_bound hn") != 4:
        raise RuntimeError("all four localized error bounds")
    if text.count("complexForwardDiff 5 complexXiNaturalAuxiliaryLogError") != 2:
        raise RuntimeError("both order-five error surfaces")


def main() -> None:
    text = SOURCE.read_text()
    validate(text)
    print("PASS xi natural certificate decomposition source contract")
    mutations = {
        "six-node domain disconnected": (
            "theorem nat_six_samples_mem_leanXiCoefficientSector",
            "theorem uncheckedSixSampleDomain",
        ),
        "proportional disc disconnected": (
            "manuscriptCauchy_closedBall_subset_sector hm",
            "uncheckedClosedBallSector hm",
        ),
        "linearity disconnected": (
            "theorem complexForwardDiff_add",
            "theorem uncheckedForwardDiffAdd",
        ),
        "second difference disconnected": (
            "theorem complexXiNaturalAuxiliarySecondDiff_eq_forwardDiff",
            "theorem uncheckedNaturalSecondDiff",
        ),
        "integer bridge disconnected": (
            "ofReal_exactXiAuxiliarySecondDiff_forwardDiffs_natural hnpos",
            "uncheckedIntegerBridge hnpos",
        ),
        "order-five main removed": (
            "complexForwardDiff 5 complexXiNaturalAuxiliaryLogMain",
            "complexForwardDiff 4 complexXiNaturalAuxiliaryLogMain",
        ),
        "order-five error removed": (
            "complexForwardDiff 5 complexXiNaturalAuxiliaryLogError",
            "complexForwardDiff 4 complexXiNaturalAuxiliaryLogError",
        ),
        "one error bound removed": (
            "complexXiNaturalAuxiliaryLogError_forwardDiff_bound hn",
            "uncheckedNaturalLogErrorForwardBound hn",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = text.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS xi natural decomposition mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
