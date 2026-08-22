#!/usr/bin/env python3
"""Fail-closed mutations for the concrete real Riemann-xi Jensen target."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/RiemannXiJensen.lean"
)


class ContractError(RuntimeError):
    """The concrete Riemann-xi target contract changed."""


def validate(text: str) -> None:
    required = {
        "real coefficient": "def riemannXiCoefficientReal (n : ℕ) : ℝ",
        "factor eight": "8 * (n.factorial : ℝ) / ((2 * n).factorial : ℝ)",
        "omega integrand": "u ^ (2 * n) * omegaLogAmplitude u",
        "complex identification": "theorem ofReal_riemannXiCoefficientReal",
        "T1 source": "centeredXiCoefficient_eq_omegaMoment",
        "real-integral source": "halfLineMoment_omegaLogAmplitude_eq_ofReal",
        "Taylor normalization":
            "theorem riemannXiCoefficientReal_taylor_normalization",
        "Taylor source": "centeredXiCoefficient_taylor_normalization n",
        "reality theorem": "theorem centeredXiCoefficient_im_eq_zero",
        "auxiliary integer seam":
            "theorem complexFactorialRatio_mul_auxiliary_nat_succ_eq_real",
        "auxiliary source": "complexFactorialRatio_mul_auxiliary_nat_succ",
        "concrete polynomial": "def riemannXiJensenPolynomial (n d : ℕ)",
        "generic polynomial source":
            "jensenPolynomial riemannXiCoefficientReal n d X",
        "sum formula": "theorem riemannXiJensenPolynomial_eq_sum",
        "certificate theorem": "theorem conditionalTwoThirdsWedge_riemannXi",
        "conditional producer": "exact conditionalTwoThirdsWedge",
        "typed-input theorem":
            "theorem conditionalTwoThirdsWedge_riemannXi_of_analyticInputs",
        "typed inputs": "JensenWedgeAnalyticInputs",
        "typed consumer": ".target_hasDistinctNegativeRoots",
    }
    counts = {
        "auxiliary source": 2,
        "certificate theorem": 2,
    }
    for label, needle in required.items():
        if text.count(needle) != counts.get(label, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T6 concrete Riemann-xi target source contract")
    mutations = {
        "factor eight changed": (
            "8 * (n.factorial : ℝ) / ((2 * n).factorial : ℝ)",
            "4 * (n.factorial : ℝ) / ((2 * n).factorial : ℝ)",
        ),
        "even power changed": ("u ^ (2 * n)", "u ^ (2 * n + 1)"),
        "complex identification removed": (
            "theorem ofReal_riemannXiCoefficientReal",
            "theorem uncheckedRealIdentification",
        ),
        "T1 disconnected": (
            "centeredXiCoefficient_eq_omegaMoment",
            "uncheckedT1Coefficient",
        ),
        "Taylor normalization removed": (
            "theorem riemannXiCoefficientReal_taylor_normalization",
            "theorem uncheckedTaylorNormalization",
        ),
        "Taylor source disconnected": (
            "centeredXiCoefficient_taylor_normalization n",
            "uncheckedTaylorSource n",
        ),
        "reality theorem removed": (
            "theorem centeredXiCoefficient_im_eq_zero",
            "theorem uncheckedReality",
        ),
        "auxiliary seam removed": (
            "theorem complexFactorialRatio_mul_auxiliary_nat_succ_eq_real",
            "theorem uncheckedAuxiliaryIntegerSeam",
        ),
        "concrete polynomial removed": (
            "def riemannXiJensenPolynomial (n d : ℕ)",
            "def uncheckedJensenTarget (n d : ℕ)",
        ),
        "sequence disconnected": (
            "jensenPolynomial riemannXiCoefficientReal n d X",
            "jensenPolynomial (fun _ => 0) n d X",
        ),
        "conditional theorem removed": (
            "theorem conditionalTwoThirdsWedge_riemannXi",
            "theorem uncheckedConditionalTarget",
        ),
        "typed interface removed": (
            "JensenWedgeAnalyticInputs",
            "JensenWedgeCertificate",
        ),
        "typed consumer disconnected": (
            ".target_hasDistinctNegativeRoots",
            ".uncheckedTargetRoots",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 Riemann-xi target mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
