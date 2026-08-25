#!/usr/bin/env python3
"""Fail-closed source mutations for the concrete Phase-26 T1 chain."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration"
    / "zeta-23-lean"
    / "Zeta23"
    / "Research"
    / "JensenWedge"
)
PATHS = {
    "coeff": LEAN / "XiOmegaCoefficients.lean",
    "theta": LEAN / "ThetaOmega.lean",
    "integral": LEAN / "XiOmegaIntegral.lean",
}


class ContractError(RuntimeError):
    """A load-bearing T1 source connection is absent or ambiguous."""


def require_once(text: str, needle: str, label: str) -> None:
    count = text.count(needle)
    if count != 1:
        raise ContractError(f"{label}: expected exactly one occurrence, found {count}")


def validate(sources: dict[str, str]) -> None:
    coeff = sources["coeff"]
    theta = sources["theta"]
    integral = sources["integral"]
    require_once(
        coeff,
        "theorem iteratedDeriv_centeredXi_eq_eight_omegaMoment (n : ℕ)",
        "concrete factor-eight producer",
    )
    require_once(
        coeff,
        "iteratedDeriv (2 * n) centeredXi 0 =\n"
        "      8 * halfLineMoment (fun u => (omegaLogAmplitude u : ℂ)) n",
        "even derivative and factor eight",
    )
    require_once(
        coeff,
        "theorem centeredXiCoefficient_eq_omegaMoment (n : ℕ)",
        "unconditional coefficient theorem",
    )
    require_once(
        coeff,
        "8 * (n.factorial : ℂ) / ((2 * n).factorial : ℂ) *",
        "factorial normalization",
    )
    require_once(
        coeff,
        "theorem eight_mul_integral_omegaLogAmplitude_zero :",
        "endpoint cancellation theorem",
    )
    require_once(
        theta,
        "def thetaLogAmplitude (u : ℝ) : ℝ :=\n"
        "  Real.exp (u / 2) * riemannThetaTail (Real.exp (2 * u))",
        "theta exponential half-shift",
    )
    require_once(
        integral,
        "def centeredModifiedThetaAmplitude (u : ℝ) : ℂ :=\n"
        "  (Real.exp (u / 2) : ℂ) *\n"
        "    riemannThetaModifiedKernel (Real.exp (2 * u))",
        "centered modified-theta half-shift",
    )


def expect_rejected(label: str, sources: dict[str, str]) -> None:
    try:
        validate(sources)
    except ContractError:
        print(f"PASS T1 mutation rejected: {label}")
        return
    raise AssertionError(f"T1 mutation survived: {label}")


def mutate(
    sources: dict[str, str], key: str, old: str, new: str
) -> dict[str, str]:
    changed = dict(sources)
    if changed[key].count(old) != 1:
        raise AssertionError(f"mutation source is not unique: {key}: {old!r}")
    changed[key] = changed[key].replace(old, new, 1)
    return changed


def main() -> None:
    sources = {key: path.read_text(encoding="utf-8") for key, path in PATHS.items()}
    validate(sources)
    print("PASS concrete T1 source contract")
    cases = {
        "factor eight changed to four": mutate(
            sources,
            "coeff",
            "8 * halfLineMoment (fun u => (omegaLogAmplitude u : ℂ)) n",
            "4 * halfLineMoment (fun u => (omegaLogAmplitude u : ℂ)) n",
        ),
        "even derivative changed to odd": mutate(
            sources,
            "coeff",
            "iteratedDeriv (2 * n) centeredXi 0 =\n",
            "iteratedDeriv (2 * n + 1) centeredXi 0 =\n",
        ),
        "coefficient factorial transposed": mutate(
            sources,
            "coeff",
            "8 * (n.factorial : ℂ) / ((2 * n).factorial : ℂ) *",
            "8 * ((2 * n).factorial : ℂ) / (n.factorial : ℂ) *",
        ),
        "theta exponential half-shift dropped": mutate(
            sources,
            "theta",
            "def thetaLogAmplitude (u : ℝ) : ℝ :=\n"
            "  Real.exp (u / 2) * riemannThetaTail (Real.exp (2 * u))",
            "def thetaLogAmplitude (u : ℝ) : ℝ :=\n"
            "  Real.exp u * riemannThetaTail (Real.exp (2 * u))",
        ),
        "centered kernel half-shift dropped": mutate(
            sources,
            "integral",
            "def centeredModifiedThetaAmplitude (u : ℝ) : ℂ :=\n"
            "  (Real.exp (u / 2) : ℂ) *\n"
            "    riemannThetaModifiedKernel (Real.exp (2 * u))",
            "def centeredModifiedThetaAmplitude (u : ℝ) : ℂ :=\n"
            "  (Real.exp u : ℂ) *\n"
            "    riemannThetaModifiedKernel (Real.exp (2 * u))",
        ),
        "endpoint cancellation disconnected": mutate(
            sources,
            "coeff",
            "theorem eight_mul_integral_omegaLogAmplitude_zero :",
            "theorem eight_mul_integral_omegaLogAmplitude_unchecked :",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)
    print("PASS all concrete T1 semantic mutations")


if __name__ == "__main__":
    main()
