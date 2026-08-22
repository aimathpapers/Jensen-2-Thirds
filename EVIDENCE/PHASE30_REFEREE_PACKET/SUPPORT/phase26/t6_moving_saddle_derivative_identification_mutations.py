#!/usr/bin/env python3
"""Fail closed on the kernel derivation of the moving-saddle tower."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge/MovingSaddleDerivativeIdentification.lean"
)

REQUIRED = {
    "term r derivative": "def saddleTermDerivR",
    "term sigma derivative": "def saddleTermDerivSigma",
    "bivariate chain rule": "theorem hasDerivAt_evalBivariateTerms_comp",
    "reduced recurrence": "def movingSaddleNumeratorStep",
    "H2 to H3 table check": "theorem h2Numerator_step",
    "H3 to H4 table check": "theorem h3Numerator_step",
    "H4 to H5 table check": "theorem h4Numerator_step",
    "H5 to H6 table check": "theorem h5Numerator_step",
    "scaled curvature identity": "theorem manuscriptSaddleQ_scaled",
    "inverse-saddle derivative": "theorem hasDerivAt_manuscriptSaddleR",
    "ratio derivative": "theorem hasDerivAt_manuscriptSaddleSigma",
    "generic reduced derivative": "theorem hasDerivAt_saddleReducedMain",
    "base G0 derivative": "theorem hasDerivAt_manuscriptSaddleG0",
    "base second derivative": "theorem hasDerivAt_manuscriptG0FirstDerivative",
    "sixth iterated derivative":
        "theorem iteratedDeriv_six_manuscriptSaddleG0",
    "lower record producer":
        "theorem manuscriptG0LowerIdentification_of_mem_sector",
    "sixth record producer":
        "theorem manuscriptG0SixthIdentification_of_mem_sector",
}


def validate(text: str) -> None:
    for label, needle in REQUIRED.items():
        if needle not in text:
            raise RuntimeError(label)
    forbidden = ("sorry", "admit", "axiom", "unsafe")
    if any(f"\n{word} " in text or f"\n{word}\n" in text for word in forbidden):
        raise RuntimeError("proof escape")
    recurrence = text.split("def movingSaddleNumeratorStep", 1)[1].split(
        "set_option", 1
    )[0]
    for token in ("-4 * (r ^ 2", "Pr * B - 8 * k * P", "3 * sigma - 4",
                  "Ps * B + 6 * k * P"):
        if token not in recurrence:
            raise RuntimeError("exact reduced recurrence")


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS moving-saddle derivative identification source contract")
    mutations = {
        "r derivative disconnected":
            ("def saddleTermDerivR", "def uncheckedTermDerivR"),
        "sigma derivative disconnected":
            ("def saddleTermDerivSigma", "def uncheckedTermDerivSigma"),
        "recurrence sign changed":
            ("-4 * (r ^ 2", "4 * (r ^ 2"),
        "recurrence exponent factor changed":
            ("Pr * B - 8 * k * P", "Pr * B - 6 * k * P"),
        "H2 step disconnected":
            ("theorem h2Numerator_step", "theorem uncheckedH2Step"),
        "H5 step disconnected":
            ("theorem h5Numerator_step", "theorem uncheckedH5Step"),
        "curvature identity disconnected":
            ("theorem manuscriptSaddleQ_scaled", "theorem uncheckedQScaled"),
        "inverse-saddle derivative disconnected": (
            "theorem hasDerivAt_manuscriptSaddleR",
            "theorem uncheckedSaddleRDerivative",
        ),
        "generic derivative disconnected": (
            "theorem hasDerivAt_saddleReducedMain",
            "theorem uncheckedReducedDerivative",
        ),
        "base second derivative disconnected": (
            "theorem hasDerivAt_manuscriptG0FirstDerivative",
            "theorem uncheckedG0SecondDerivative",
        ),
        "sixth derivative disconnected": (
            "theorem iteratedDeriv_six_manuscriptSaddleG0",
            "theorem uncheckedSixthDerivative",
        ),
        "lower producer disconnected": (
            "theorem manuscriptG0LowerIdentification_of_mem_sector",
            "theorem uncheckedLowerIdentification",
        ),
        "sixth producer disconnected": (
            "theorem manuscriptG0SixthIdentification_of_mem_sector",
            "theorem uncheckedSixthIdentification",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS moving-saddle derivative mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
