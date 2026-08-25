#!/usr/bin/env python3
"""Fail closed on mutations of the natural auxiliary log main."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/XiNaturalLogMain.lean"

REQUIRED = {
    "two-shift log": ("def complexXiNaturalTwoShiftLog", 1),
    "factor logarithms":
        ("log 16 + log (N + 2) + log (N + 1) +", 1),
    "cancellation half bound":
        ("theorem coefficientCancellationCorrection_norm_sub_one_le_half", 1),
    "shared cutoff source": ("manuscriptXiCoefficientErrorRate_le_half hM", 1),
    "cancellation right half-plane":
        ("theorem coefficientCancellationCorrection_re_pos", 1),
    "denominator exponential": ("theorem exp_complexXiNaturalTwoShiftLog", 1),
    "denominator sign":
        ("coefficientMomentMultiplier (coefficientMellinParameter M) -", 1),
    "cancellation derivative":
        ("theorem differentiableAt_coefficientCancellationCorrection_comp", 1),
    "two-shift log derivative":
        ("theorem differentiableAt_complexXiNaturalTwoShiftLog", 1),
    "natural log main": ("def complexXiNaturalAuxiliaryLogMain", 1),
    "saddle log main":
        ("saddleMomentLogMain (coefficientMellinParameter M)", 1),
    "main exponential":
        ("theorem exp_complexXiNaturalAuxiliaryLogMain", 1),
    "main holomorphy":
        ("theorem differentiableOn_complexXiNaturalAuxiliaryLogMain", 1),
    "exact analytic log": ("def complexXiNaturalAuxiliaryLog (M", 1),
    "exact exponential": ("theorem exp_complexXiNaturalAuxiliaryLog\n", 1),
    "natural factorization source":
        ("complexXiAuxiliaryMoment_natural_factorization hM", 1),
    "exact log holomorphy":
        ("theorem differentiableOn_complexXiNaturalAuxiliaryLog :", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS xi natural auxiliary log-main source contract")
    mutations = {
        "N plus two dropped":
            ("log 16 + log (N + 2) + log (N + 1) +",
             "log 16 + log N + log (N + 1) +"),
        "cutoff source disconnected":
            ("manuscriptXiCoefficientErrorRate_le_half hM",
             "uncheckedErrorRate hM"),
        "right-half-plane branch disconnected":
            ("theorem coefficientCancellationCorrection_re_pos",
             "theorem uncheckedCancellationRePos"),
        "denominator sign reversed":
            ("coefficientMomentMultiplier (coefficientMellinParameter M) -",
             "coefficientMomentMultiplier (coefficientMellinParameter M) +"),
        "cancellation derivative disconnected":
            ("theorem differentiableAt_coefficientCancellationCorrection_comp",
             "theorem uncheckedCancellationDerivative"),
        "saddle log main disconnected":
            ("saddleMomentLogMain (coefficientMellinParameter M)",
             "uncheckedSaddleLogMain (coefficientMellinParameter M)"),
        "main exponential disconnected":
            ("theorem exp_complexXiNaturalAuxiliaryLogMain",
             "theorem uncheckedNaturalMainExponential"),
        "main holomorphy disconnected":
            ("theorem differentiableOn_complexXiNaturalAuxiliaryLogMain",
             "theorem uncheckedNaturalMainHolomorphy"),
        "exact exponential disconnected":
            ("theorem exp_complexXiNaturalAuxiliaryLog\n",
             "theorem uncheckedNaturalExactExponential"),
        "factorization disconnected":
            ("complexXiAuxiliaryMoment_natural_factorization hM",
             "uncheckedNaturalFactorization hM"),
        "exact log holomorphy disconnected":
            ("theorem differentiableOn_complexXiNaturalAuxiliaryLog :",
             "theorem uncheckedNaturalExactLogHolomorphy"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS xi natural log-main mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
