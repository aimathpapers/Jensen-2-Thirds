#!/usr/bin/env python3
"""Fail closed on the effective lower-xi interval-budget certificate."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge"
)

SOURCES = {
    "limits": (LEAN / "SaddleLowerOrderLimits.lean").read_text(),
    "correction": (LEAN / "XiNaturalMainCorrectionBounds.lean").read_text(),
    "budgets": (LEAN / "XiNaturalMainIntervalBudgets.lean").read_text(),
}

REQUIRED = {
    "limits": {
        "final radius":
            "def saddleFinalLimitRadius : ℝ := 1 / 100000000000000",
        "final error":
            "def saddleFinalLimitError : ℝ := 1 / 1000000000000",
        "all four final rational bounds":
            "theorem saddleH5_add_six_norm_lt_final",
    },
    "correction": {
        "curvature factorization":
            "theorem manuscriptSaddleQ_eq_curvature_mul_sq",
        "right-half-plane denominator": "theorem manuscriptSaddleQ_re_pos",
        "exact cancellation": "theorem xiNaturalMainSaddleRemainder_eq",
        "Cauchy derivatives":
            "theorem xiNaturalMainSaddleRemainder_derivatives_through_five_on_half_disc",
        "named symbolic seam consumer":
            "theorem xiNaturalMainCorrectionFive_eq_remainder",
    },
    "budgets": {
        "saddle budget":
            "def xiNaturalSaddleBudget : ℝ := 1 / 10000000000",
        "correction budget":
            "def xiNaturalCorrectionBudget : ℝ := 1 / 10000000000",
        "log-error budget":
            "def xiNaturalLogErrorBudget : ℝ := 1 / 10000000000",
        "correct order-five error scale":
            "def xiNaturalLogErrorScale : ℝ := 960000000000000000\n",
        "seven endpoint conditions":
            "structure XiNaturalSaddleIntervalConditions",
        "log-error endpoint condition": "  log_error_rate :",
        "pointwise producer":
            "theorem XiNaturalSaddleIntervalConditions.pointwiseCertificate",
        "four log-error bounds":
            "theorem XiNaturalSaddleIntervalConditions.logError_scaled_bounds",
        "exact real certificate":
            "theorem XiNaturalSaddleIntervalConditions.exactCertificate",
        "exact decomposition consumer":
            "ofReal_exactXiAuxiliarySecondDiff_forwardDiffs_decomposition",
        "disclosed symbolic interface":
            "ManuscriptG0LowerIdentification ((2 * y - 2 : ℝ) : ℂ)",
    },
}


def validate(sources: dict[str, str]) -> None:
    for source_name, requirements in REQUIRED.items():
        text = sources[source_name]
        for label, needle in requirements.items():
            if needle not in text:
                raise RuntimeError(f"{source_name}: {label}")
    limits = sources["limits"]
    if limits.count("_norm_lt_final") != 4:
        raise RuntimeError("limits: all four final bounds")
    budgets = sources["budgets"]
    if budgets.count("xiNaturalLogErrorBudget") < 8:
        raise RuntimeError("budgets: log-error budget propagation")
    if budgets.count(
        "ManuscriptG0LowerIdentification ((2 * y - 2 : ℝ) : ℂ)"
    ) != 3:
        raise RuntimeError("budgets: disclosed symbolic interface propagation")
    if budgets.count("norm_scaled_sum_add_le") != 5:
        raise RuntimeError("budgets: four final triangle consumers")


def main() -> None:
    validate(SOURCES)
    print("PASS effective lower-xi interval-budget source contract")
    mutations = {
        "final radius weakened": (
            "limits", "1 / 100000000000000", "1 / 10000000000000"
        ),
        "final H5 bound disconnected": (
            "limits", "theorem saddleH5_add_six_norm_lt_final",
            "theorem uncheckedFinalH5"
        ),
        "curvature factorization disconnected": (
            "correction", "theorem manuscriptSaddleQ_eq_curvature_mul_sq",
            "theorem uncheckedSaddleQFactorization"
        ),
        "remainder cancellation disconnected": (
            "correction", "theorem xiNaturalMainSaddleRemainder_eq",
            "theorem uncheckedRemainderCancellation"
        ),
        "order-five Cauchy scale multiplied by ten": (
            "budgets",
            "def xiNaturalLogErrorScale : ℝ := 960000000000000000\n",
            "def xiNaturalLogErrorScale : ℝ := 9600000000000000000\n"
        ),
        "log-error endpoint condition removed": (
            "budgets", "  log_error_rate :", "  unchecked_log_error_rate :"
        ),
        "symbolic interface hidden": (
            "budgets", "ManuscriptG0LowerIdentification ((2 * y - 2 : ℝ) : ℂ)",
            "UncheckedLowerIdentification ((2 * y - 2 : ℝ) : ℂ)"
        ),
        "exact decomposition disconnected": (
            "budgets", "ofReal_exactXiAuxiliarySecondDiff_forwardDiffs_decomposition",
            "uncheckedExactXiDecomposition"
        ),
        "final certificate disconnected": (
            "budgets", "theorem XiNaturalSaddleIntervalConditions.exactCertificate",
            "theorem uncheckedExactIntervalCertificate"
        ),
    }
    for label, (source_name, old, new) in mutations.items():
        changed = dict(SOURCES)
        changed[source_name] = changed[source_name].replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS lower-xi interval mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
