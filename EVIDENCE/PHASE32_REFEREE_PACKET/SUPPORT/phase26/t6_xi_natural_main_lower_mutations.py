#!/usr/bin/env python3
"""Fail closed on the lower natural-main derivative certificate surface."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge"
)

SOURCES = {
    "orders": (LEAN / "SaddleLowerOrders.lean").read_text(),
    "limits": (LEAN / "SaddleLowerOrderLimits.lean").read_text(),
    "moving": (LEAN / "MovingSaddleLowerOrders.lean").read_text(),
    "forward": (LEAN / "XiNaturalMainLowerForwardDifferences.lean").read_text(),
}

REQUIRED = {
    "orders": {
        "four reduced rational functions": "def saddleH5 (r sigma : ℂ) : ℂ :=",
        "order-two central value": "theorem saddleH2_zero_zero : saddleH2 0 0 = 1",
        "order-three central value": "theorem saddleH3_zero_zero : saddleH3 0 0 = -1",
        "order-four central value": "theorem saddleH4_zero_zero : saddleH4 0 0 = 2",
        "order-five central value": "theorem saddleH5_zero_zero : saddleH5 0 0 = -6",
        "order-five whole-bidisc bound":
            "theorem saddleH5_norm_lt_eightHundredFortyThree",
    },
    "limits": {
        "exact H2 error identity": "theorem h2LimitErrorNumerator_identity",
        "exact H5 error identity": "theorem h5LimitErrorNumerator_identity",
        "tiny radius": "def saddleLowerLimitRadius : ℝ := 1 / 10000000",
        "common error": "def saddleLowerLimitError : ℝ := 1 / 500000",
        "H2 tiny-bidisc limit": "theorem saddleH2_sub_one_norm_lt",
        "H3 tiny-bidisc limit": "theorem saddleH3_add_one_norm_lt",
        "H4 tiny-bidisc limit": "theorem saddleH4_sub_two_norm_lt\n",
        "H5 tiny-bidisc limit": "theorem saddleH5_add_six_norm_lt",
    },
    "moving": {
        "named CAS seam": "structure ManuscriptG0LowerIdentification",
        "all four CAS equalities":
            "orderFive : iteratedDeriv 5 manuscriptSaddleG0 N = manuscriptSaddleMainFive N",
        "two scalar coordinate rates":
            "theorem manuscriptSaddle_scaled_coordinates_in_lowerLimitBox",
        "normalized four-order result":
            "theorem iteratedDeriv_manuscriptSaddleG0_lower_normalized_limits",
    },
    "forward": {
        "chain factor four":
            "def xiNaturalMainSaddleTwo (M : ℂ) : ℂ :=\n  4 * manuscriptSaddleMainTwo",
        "chain factor eight":
            "def xiNaturalMainSaddleThree (M : ℂ) : ℂ :=\n  8 * manuscriptSaddleMainThree",
        "chain factor sixteen":
            "def xiNaturalMainSaddleFour (M : ℂ) : ℂ :=\n  16 * manuscriptSaddleMainFour",
        "chain factor thirty-two":
            "def xiNaturalMainSaddleFive (M : ℂ) : ℂ :=\n  32 * manuscriptSaddleMainFive",
        "explicit order-five correction": "def xiNaturalMainCorrectionFive",
        "exact order-five split": "theorem xiNaturalMain_orderFive_decomposition",
        "separate primitive budgets":
            "structure XiNaturalMainLowerPointwiseCertificate",
        "budget addition producer":
            "XiNaturalMainLowerDerivativeBounds n L\n      (saddleError + correctionError)",
        "localized FTC consumer":
            "norm_complexForwardDiff_sub_constant_le_on_real_interval",
        "four forward differences":
            "theorem XiNaturalMainLowerDerivativeBounds.forwardDiff_bounds",
    },
}


def validate(sources: dict[str, str]) -> None:
    for source_name, requirements in REQUIRED.items():
        text = sources[source_name]
        for label, needle in requirements.items():
            if needle not in text:
                raise RuntimeError(f"{source_name}: {label}")
    forward = sources["forward"]
    if forward.count("exact norm_scaled_sum_sub_le") != 4:
        raise RuntimeError("forward: all four triangle consumers")
    if forward.count("B.scaled_forwardDiff") != 4:
        raise RuntimeError("forward: all four localized FTC consumers")


def main() -> None:
    validate(SOURCES)
    print("PASS lower natural-main derivative source contract")
    mutations = {
        "H3 sign flipped": ("orders", "saddleH3 0 0 = -1", "saddleH3 0 0 = 1"),
        "H5 central constant changed":
            ("orders", "saddleH5 0 0 = -6", "saddleH5 0 0 = -5"),
        "tiny radius weakened":
            ("limits", "1 / 10000000", "1 / 1000000"),
        "H4 limit disconnected":
            ("limits", "theorem saddleH4_sub_two_norm_lt\n",
             "theorem uncheckedH4Limit\n"),
        "CAS seam removed":
            ("moving", "structure ManuscriptG0LowerIdentification", "structure UncheckedLowerTower"),
        "order-five CAS equality removed":
            ("moving", "orderFive : iteratedDeriv 5", "uncheckedOrderFive : iteratedDeriv 5"),
        "order-two chain factor changed":
            ("forward", "\n  4 * manuscriptSaddleMainTwo", "\n  2 * manuscriptSaddleMainTwo"),
        "order-five chain factor changed":
            ("forward", "\n  32 * manuscriptSaddleMainFive", "\n  16 * manuscriptSaddleMainFive"),
        "order-five correction removed":
            ("forward", "def xiNaturalMainCorrectionFive", "def uncheckedCorrectionFive"),
        "budget sum disconnected":
            ("forward", "(saddleError + correctionError)", "saddleError"),
        "localized FTC disconnected":
            ("forward", "norm_complexForwardDiff_sub_constant_le_on_real_interval",
             "uncheckedForwardDiffBound"),
    }
    for label, (source_name, old, new) in mutations.items():
        changed = dict(SOURCES)
        changed[source_name] = changed[source_name].replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS lower natural-main mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
