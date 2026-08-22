#!/usr/bin/env python3
"""Fail-closed semantic mutations for the exact xi parameter map."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ExactParameterMap.lean"
)


class ContractError(RuntimeError):
    """The exact-map source contract changed."""


REQUIRED = {
    "true xi coefficient": "Real.log (riemannXiCoefficientReal m)",
    "half shift": "(((n + k : ℕ) : ℝ) + 1 / 2)",
    "Jacobi signs": (
        "  logRatio (residualParameterA y n (1 / L)) k -\n"
        "    logRatio (residualParameterB y n (1 / L)) k +\n"
        "    logRatio (residualParameterC y n) k -\n"
        "    logRatio (residualParameterD y n (1 / L)) k"
    ),
    "xi second difference": "secondDiff exactXiCoefficientLog (n + k)",
    "true quotient residual": (
        "exactJacobiLogQuotient y n L k +\n"
        "    secondDiff exactXiCoefficientLog (n + k)"
    ),
    "first scale": "-((n : ℝ) * L) * natForwardDiff0",
    "second scale": "((n : ℝ) ^ 2 * L / 2) * natForwardDiff1",
    "third scale": "-((n : ℝ) ^ 3 * L / 2) * natForwardDiff2",
    "fourth scale": "((n : ℝ) ^ 4 * L / 6) * natForwardDiff3",
    "four values": "theorem exactXiParameterMap_eq_zero_iff_values",
    "finite hinge": "theorem exactXiParameterMap_eq_zero_iff_fin",
    "six-match consumer": "fourQuotients_twoNormalizations_sixCoefficients",
}


def validate(text: str) -> None:
    for label, needle in REQUIRED.items():
        if text.count(needle) != 1:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS exact xi parameter-map source contract")
    mutations = {
        "xi source replaced": (
            "riemannXiCoefficientReal m", "uncheckedXiCoefficient m"),
        "half shift dropped": (
            "(((n + k : ℕ) : ℝ) + 1 / 2)", "((n + k : ℕ) : ℝ)"),
        "A sign reversed": (
            "logRatio (residualParameterA y n (1 / L)) k -",
            "-logRatio (residualParameterA y n (1 / L)) k -"),
        "B sign reversed": (
            "-\n    logRatio (residualParameterB y n (1 / L)) k +",
            "+\n    logRatio (residualParameterB y n (1 / L)) k +"),
        "C sign reversed": (
            "+\n    logRatio (residualParameterC y n) k -",
            "-\n    logRatio (residualParameterC y n) k -"),
        "D sign reversed": (
            "-\n    logRatio (residualParameterD y n (1 / L)) k",
            "+\n    logRatio (residualParameterD y n (1 / L)) k"),
        "second difference removed": (
            "secondDiff exactXiCoefficientLog (n + k)", "0"),
        "true quotient sign reversed": (
            "exactJacobiLogQuotient y n L k +",
            "exactJacobiLogQuotient y n L k -"),
        "first triangular sign reversed": (
            "-((n : ℝ) * L) * natForwardDiff0",
            "((n : ℝ) * L) * natForwardDiff0"),
        "second divisor removed": (
            "((n : ℝ) ^ 2 * L / 2) * natForwardDiff1",
            "((n : ℝ) ^ 2 * L) * natForwardDiff1"),
        "third triangular sign reversed": (
            "-((n : ℝ) ^ 3 * L / 2) * natForwardDiff2",
            "((n : ℝ) ^ 3 * L / 2) * natForwardDiff2"),
        "fourth divisor changed": (
            "((n : ℝ) ^ 4 * L / 6) * natForwardDiff3",
            "((n : ℝ) ^ 4 * L / 4) * natForwardDiff3"),
        "four-value bridge removed": (
            "theorem exactXiParameterMap_eq_zero_iff_values",
            "theorem uncheckedExactMapValues"),
        "finite hinge removed": (
            "theorem exactXiParameterMap_eq_zero_iff_fin",
            "theorem uncheckedExactMapFin"),
        "six-match adapter disconnected": (
            "fourQuotients_twoNormalizations_sixCoefficients",
            "uncheckedSixMatchAdapter"),
    }
    for label, (old, new) in mutations.items():
        if source.count(old) != 1:
            raise AssertionError(f"mutation target changed: {label}")
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS exact parameter-map mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
