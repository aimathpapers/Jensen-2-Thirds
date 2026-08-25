#!/usr/bin/env python3
"""Fail closed on mutations of the natural auxiliary logarithmic error."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge"
RATE = LEAN / "XiLogError.lean"
SOURCE = LEAN / "XiNaturalLogError.lean"

RATE_REQUIRED = {
    "shared rate theorem": ("theorem manuscriptXiCoefficientErrorRate_le_half", 1),
    "rate cutoff": ("(10 : ℝ) ^ 80 ≤ ‖N‖", 1),
    "rate conclusion": ("2 * C / (10 : ℝ) ^ 40", 1),
}

REQUIRED = {
    "natural error half bound":
        ("theorem complexXiNaturalAuxiliaryRelativeError_norm_le_half", 1),
    "natural-to-manuscript comparison":
        ("100 * C ≤ manuscriptXiCoefficientErrorCoefficient", 1),
    "shared rate consumer": ("manuscriptXiCoefficientErrorRate_le_half hM", 1),
    "nonzero branch":
        ("theorem one_add_complexXiNaturalAuxiliaryRelativeError_ne_zero", 1),
    "right half-plane branch":
        ("theorem one_add_complexXiNaturalAuxiliaryRelativeError_re_pos", 1),
    "logarithmic error": ("def complexXiNaturalAuxiliaryLogError", 1),
    "exponential identity":
        ("theorem exp_complexXiNaturalAuxiliaryLogError", 1),
    "log holomorphy":
        ("theorem differentiableOn_complexXiNaturalAuxiliaryLogError", 1),
    "three-halves log bound": ("Complex.norm_log_one_add_half_le_self", 1),
}


def validate(text: str, required: dict[str, tuple[str, int]]) -> None:
    for label, (needle, count) in required.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    rate = RATE.read_text()
    source = SOURCE.read_text()
    validate(rate, RATE_REQUIRED)
    validate(source, REQUIRED)
    print("PASS xi natural logarithmic error source contract")
    mutations = {
        "shared cutoff disconnected":
            (rate, RATE_REQUIRED,
             "theorem manuscriptXiCoefficientErrorRate_le_half",
             "theorem uncheckedCoefficientErrorRate"),
        "constant comparison reversed":
            (source, REQUIRED,
             "100 * C ≤ manuscriptXiCoefficientErrorCoefficient",
             "manuscriptXiCoefficientErrorCoefficient ≤ 100 * C"),
        "shared rate consumer disconnected":
            (source, REQUIRED,
             "manuscriptXiCoefficientErrorRate_le_half hM",
             "uncheckedCoefficientErrorRate hM"),
        "nonzero branch disconnected":
            (source, REQUIRED,
             "theorem one_add_complexXiNaturalAuxiliaryRelativeError_ne_zero",
             "theorem uncheckedNaturalErrorNeZero"),
        "right-half-plane branch disconnected":
            (source, REQUIRED,
             "theorem one_add_complexXiNaturalAuxiliaryRelativeError_re_pos",
             "theorem uncheckedNaturalErrorRePos"),
        "exponential identity disconnected":
            (source, REQUIRED,
             "theorem exp_complexXiNaturalAuxiliaryLogError",
             "theorem uncheckedNaturalLogExp"),
        "log holomorphy disconnected":
            (source, REQUIRED,
             "theorem differentiableOn_complexXiNaturalAuxiliaryLogError",
             "theorem uncheckedNaturalLogHolomorphy"),
        "log bound producer disconnected":
            (source, REQUIRED,
             "Complex.norm_log_one_add_half_le_self",
             "uncheckedNaturalLogBound"),
    }
    for label, (text, required, old, new) in mutations.items():
        changed = text.replace(old, new, 1)
        try:
            validate(changed, required)
        except RuntimeError:
            print(f"PASS xi natural log mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
