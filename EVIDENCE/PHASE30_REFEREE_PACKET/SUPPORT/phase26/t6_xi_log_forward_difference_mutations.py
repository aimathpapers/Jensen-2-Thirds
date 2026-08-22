#!/usr/bin/env python3
"""Fail closed on mutations of xi log-error forward-difference bounds."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/XiLogErrorForwardDifferences.lean"

REQUIRED = {
    "cutoff lower bound": ("theorem manuscriptCauchy_large_tenThousand", 1),
    "explicit cutoff": ("Real.exp (leanSaddleCutoff + 2)", 4),
    "analytic upgrade":
        ("theorem manuscriptXiLogRelativeError_analyticOnNhd", 1),
    "analytic source":
        ("differentiableOn_manuscriptXiLogRelativeError.analyticOnNhd", 1),
    "iterated derivative tower":
        ("theorem hasDerivAt_iteratedDeriv_manuscriptXiLogRelativeError", 1),
    "tower producer": (".iterated_deriv s", 1),
    "five-node interval":
        ("theorem nat_five_interval_mem_manuscriptInteriorDisc", 1),
    "five endpoint": ("((n : ℝ) + 5)", 2),
    "interior radius": ("manuscriptInteriorCauchyRadius", 8),
    "forward bound":
        ("theorem manuscriptXiLogRelativeError_forwardDiff_bound", 1),
    "order cap": ("hq5 : q ≤ 5", 1),
    "half-disc estimate":
        ("manuscriptXiLogRelativeError_derivatives_through_six_on_half_disc", 1),
    "local FTC adapter":
        ("norm_complexForwardDiff_sub_constant_le_on_real_interval", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS xi log-error forward-difference source contract")
    mutations = {
        "cutoff changed":
            ("Real.exp (leanSaddleCutoff + 2)",
             "Real.exp (leanSaddleCutoff - 2)"),
        "analytic source disconnected":
            ("differentiableOn_manuscriptXiLogRelativeError.analyticOnNhd",
             "uncheckedLogErrorAnalytic"),
        "derivative tower disconnected":
            (".iterated_deriv s", ".uncheckedIteratedDerivative s"),
        "five-node endpoint changed":
            ("((n : ℝ) + 5)", "((n : ℝ) + 4)"),
        "inner radius changed":
            ("manuscriptInteriorCauchyRadius", "uncheckedInteriorRadius"),
        "order cap weakened": ("hq5 : q ≤ 5", "hq5 : q ≤ 6"),
        "half-disc estimate disconnected":
            ("manuscriptXiLogRelativeError_derivatives_through_six_on_half_disc",
             "uncheckedLogErrorDerivativeBound"),
        "local FTC adapter disconnected":
            ("norm_complexForwardDiff_sub_constant_le_on_real_interval",
             "uncheckedLocalForwardDifferenceAdapter"),
        "final theorem renamed":
            ("theorem manuscriptXiLogRelativeError_forwardDiff_bound",
             "theorem uncheckedXiLogErrorForwardDiff"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS xi log-error forward-difference mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
