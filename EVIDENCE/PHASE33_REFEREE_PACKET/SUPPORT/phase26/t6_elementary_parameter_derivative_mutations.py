#!/usr/bin/env python3
"""Fail closed on semantic mutations of elementary parameter derivatives."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ElementaryParameterDerivatives.lean"
)


class ContractError(RuntimeError):
    """The parameter-derivative source contract changed."""


REQUIRED = {
    "remote term": ("def elementaryRemoteTerm", 1),
    "remote scale": ("e ^ (q - 1) * elementaryPhi q alpha (x * e)", 1),
    "paired term": ("def elementaryPairedTerm", 1),
    "gamma boundary": ("def elementaryGammaBoundaryTerm", 1),
    "component decomposition": (
        "theorem exactElementaryParameterComponent_eq_boundaryTerms", 1
    ),
    "alpha producer": ("theorem hasDerivAt_elementaryRemoteTerm_alpha", 1),
    "alpha error": ("theorem elementaryRemoteTerm_alpha_q1_error", 1),
    "alpha constant": ("2 * x * e * alpha₀⁻¹ ^ 3", 1),
    "second average": ("theorem elementaryPhiD2_average_base_error", 1),
    "w producer": ("theorem hasDerivAt_elementaryPairedTerm_w", 1),
    "w sign": ("(-elementaryPhiD1 q (t + w * e) x) w", 1),
    "t producer": ("theorem hasDerivAt_elementaryPairedTerm_t", 1),
    "t sign": ("(-(q : ℝ) * (q + 1) * w * t⁻¹ ^ (q + 2))", 2),
    "delta producer": (
        "theorem hasDerivAt_elementaryGammaBoundaryTerm_delta", 1
    ),
    "delta error": ("theorem elementaryGammaBoundaryTerm_delta_error", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary parameter-derivative source contract")
    mutations = {
        "remote scale weakened": ("e ^ (q - 1)", "e ^ q"),
        "component decomposition disconnected": (
            "theorem exactElementaryParameterComponent_eq_boundaryTerms",
            "theorem uncheckedComponentDecomposition",
        ),
        "alpha producer disconnected": (
            "theorem hasDerivAt_elementaryRemoteTerm_alpha",
            "theorem uncheckedRemoteDerivative",
        ),
        "alpha constant changed": (
            "2 * x * e * alpha₀⁻¹ ^ 3",
            "x * e * alpha₀⁻¹ ^ 3",
        ),
        "second average disconnected": (
            "theorem elementaryPhiD2_average_base_error",
            "theorem uncheckedSecondAverage",
        ),
        "w sign reversed": (
            "(-elementaryPhiD1 q (t + w * e) x) w",
            "(elementaryPhiD1 q (t + w * e) x) w",
        ),
        "t order weakened": (
            "(-(q : ℝ) * (q + 1) * w * t⁻¹ ^ (q + 2))",
            "(-(q : ℝ) * (q + 1) * w * t⁻¹ ^ (q + 1))",
        ),
        "delta producer disconnected": (
            "theorem hasDerivAt_elementaryGammaBoundaryTerm_delta",
            "theorem uncheckedGammaDerivative",
        ),
    }
    for label, (old, new) in mutations.items():
        if source.count(old) < 1:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS elementary parameter-derivative mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
