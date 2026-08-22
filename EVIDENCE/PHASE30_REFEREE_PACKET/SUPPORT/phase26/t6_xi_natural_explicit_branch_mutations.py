#!/usr/bin/env python3
"""Fail closed on the explicit lower-xi cutoff and branch instantiation."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge/XiNaturalExplicitBranch.lean"
)

REQUIRED = {
    "displayed logarithmic cutoff":
        "def xiNaturalExplicitLogCutoff : ℝ := 1000000000000000",
    "strict natural cutoff":
        "⌈Real.exp xiNaturalExplicitLogCutoff⌉₊ + 1",
    "fixed elementary power gate":
        "theorem ten_pow_oneSixty_le_exp_explicitLogCutoff",
    "seven-condition constructor":
        "theorem xiNaturalSaddleIntervalConditions_of_explicitCutoff",
    "all seven named fields": "    log_error_rate := ?_",
    "correction endpoint consumer": "_ ≤ xiNaturalCorrectionBudget := by",
    "log-error endpoint consumer": "_ ≤ xiNaturalLogErrorBudget := by",
    "kernel identification interface":
        "def XiNaturalLowerIdentificationCertificate (n : ℕ) : Prop :=",
    "four-equality seam":
        "ManuscriptG0LowerIdentification ((2 * y - 2 : ℝ) : ℂ)",
    "kernel identification producer":
        "exact manuscriptG0LowerIdentification_of_mem_sector",
    "exact interval certificate":
        "theorem exactXiSaddleIntervalCertificate_of_explicitCutoff",
    "fixed branch scales":
        "theorem explicitCutoff_xiNatural_branch_scales",
    "exact positive branch":
        "noncomputable def exactXiPositiveParameterBranch_of_explicitCutoff",
    "branch theorem consumer": "exact exactXi_positiveParameterBranch hnpos hL",
}


def validate(text: str) -> None:
    for label, needle in REQUIRED.items():
        if needle not in text:
            raise RuntimeError(label)
    condition_fields = (
        "coefficient_center_in_remote_sector :=",
        "center_in_remote_sector :=",
        "inverse_rate :=",
        "sigma_rate :=",
        "ratio_rate :=",
        "correction_rate :=",
        "log_error_rate :=",
    )
    source_lines = text.splitlines()
    if any(sum(line.strip().startswith(field.strip()) for line in source_lines) != 1
           for field in condition_fields):
        raise RuntimeError("exactly seven explicit endpoint fields")
    if text.count("XiNaturalLowerIdentificationCertificate") != 2:
        raise RuntimeError("kernel identification interface propagation")
    exact_signature = text.split(
        "theorem exactXiSaddleIntervalCertificate_of_explicitCutoff", 1
    )[1].split(":=", 1)[0]
    if "IdentificationCertificate" in exact_signature:
        raise RuntimeError("external symbolic premise survived")


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS explicit lower-xi cutoff and branch source contract")
    mutations = {
        "logarithmic cutoff reduced": (
            "1000000000000000", "100000000000000"
        ),
        "strict cutoff successor removed": (
            "⌉₊ + 1", "⌉₊ + 0"
        ),
        "elementary power gate disconnected": (
            "theorem ten_pow_oneSixty_le_exp_explicitLogCutoff",
            "theorem uncheckedPowerGate"
        ),
        "condition constructor disconnected": (
            "theorem xiNaturalSaddleIntervalConditions_of_explicitCutoff",
            "theorem uncheckedEndpointConditions"
        ),
        "correction condition renamed": (
            "    correction_rate := ?_", "    unchecked_correction_rate := ?_"
        ),
        "identification interface hidden": (
            "def XiNaturalLowerIdentificationCertificate (n : ℕ) : Prop :=",
            "def UncheckedLowerCertificate (n : ℕ) : Prop :="
        ),
        "kernel producer disconnected": (
            "exact manuscriptG0LowerIdentification_of_mem_sector",
            "exact uncheckedG0Identification"
        ),
        "symbolic identification disconnected": (
            "ManuscriptG0LowerIdentification ((2 * y - 2 : ℝ) : ℂ)",
            "UncheckedG0Identification ((2 * y - 2 : ℝ) : ℂ)"
        ),
        "interval certificate disconnected": (
            "theorem exactXiSaddleIntervalCertificate_of_explicitCutoff",
            "theorem uncheckedExactIntervalCertificate"
        ),
        "branch scales disconnected": (
            "theorem explicitCutoff_xiNatural_branch_scales",
            "theorem uncheckedBranchScales"
        ),
        "positive branch disconnected": (
            "noncomputable def exactXiPositiveParameterBranch_of_explicitCutoff",
            "noncomputable def uncheckedPositiveBranch"
        ),
        "exact branch theorem bypassed": (
            "exact exactXi_positiveParameterBranch hnpos hL",
            "exact uncheckedXiBranch hnpos hL"
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS explicit lower-xi mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
