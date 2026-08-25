#!/usr/bin/env python3
"""Fail closed on the transformed-xi and exact six-match bridge."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
    / "Zeta23/Research/JensenWedge"
)
TRANSFORMED = LEAN / "XiNaturalTransformedPolynomial.lean"
SIX_MATCH = LEAN / "XiNaturalSixCoefficientMatch.lean"


class ContractError(RuntimeError):
    """The exact transformed-polynomial source contract changed."""


REQUIRED_TRANSFORMED = {
    "positive xi ratio": "theorem xiNaturalFirstCoefficientRatio_pos",
    "comparison B": "residualParameterB y n (1 / L)",
    "scale normalization": (
        "xiNaturalComparisonB n L y * xiNaturalFirstCoefficientRatio n"
    ),
    "negative variable transform": (
        "riemannXiJensenPolynomial n d\n"
        "      (-X / xiNaturalJensenScale n L y) /"
    ),
    "exact coefficient record": "def xiNaturalCoefficientEstimate",
    "terminating comparison": "terminating3F2Polynomial d A B C D (D / (A * C))",
}

REQUIRED_SIX_MATCH = {
    "actual log normalization": (
        "Real.log (riemannXiCoefficientReal (n + j)) -\n"
        "    Real.log (riemannXiCoefficientReal n) -"
    ),
    "actual scale subtraction": (
        "    Real.log (riemannXiCoefficientReal n) -\n"
        "    (j : ℝ) * Real.log (xiNaturalJensenScale n L y)"
    ),
    "model signs": (
        "Real.log D - Real.log A - Real.log C +\n"
        "    Real.log (A + k) + Real.log (C + k) -\n"
        "    Real.log (B + k) - Real.log (D + k)"
    ),
    "quotient second-difference identity": (
        "exactXiQuotientResidual_eq_logCoordinate_difference"
    ),
    "two-normalization adapter": "exactXiParameterMap_six_log_coefficients",
    "positive parameter domain": "theorem xiNaturalResidualParameters_pos",
    "exponentiated increment": "theorem exp_xiNaturalModelLogIncrement",
    "alternating binomial step": "theorem alternatingChoose_step",
    "terminating coefficient induction": (
        "theorem terminating3F2Coefficient_eq_xiNaturalModel"
    ),
    "model polynomial identity": (
        "theorem xiNaturalModelLogPolynomial_eq_comparison\n    {n : ℕ}"
    ),
    "actual evaluation identity": "theorem eval_xiNaturalActualLogPolynomial",
    "direct six comparison matches": (
        "theorem xiNaturalSixPolynomialCoefficients_match_comparison\n    {n : ℕ}"
    ),
    "explicit cutoff comparison": (
        "theorem xiNaturalModelLogPolynomial_eq_comparison_of_explicitCutoff"
    ),
    "explicit cutoff six matches": (
        "theorem xiNaturalSixPolynomialCoefficients_match_comparison_of_explicitCutoff"
    ),
}


def validate(transformed: str, six_match: str) -> None:
    for label, needle in REQUIRED_TRANSFORMED.items():
        if needle not in transformed:
            raise ContractError(label)
    for label, needle in REQUIRED_SIX_MATCH.items():
        if needle not in six_match:
            raise ContractError(label)


def main() -> None:
    transformed = TRANSFORMED.read_text()
    six_match = SIX_MATCH.read_text()
    validate(transformed, six_match)
    print("PASS transformed-xi and exact six-match source contract")
    mutations = {
        "scale factor removed": (
            "transformed",
            "xiNaturalComparisonB n L y * xiNaturalFirstCoefficientRatio n",
            "xiNaturalFirstCoefficientRatio n",
        ),
        "variable sign reversed": (
            "transformed",
            "      (-X / xiNaturalJensenScale n L y) /",
            "      (X / xiNaturalJensenScale n L y) /",
        ),
        "hypergeometric lambda changed": (
            "transformed",
            "terminating3F2Polynomial d A B C D (D / (A * C))",
            "terminating3F2Polynomial d A B C D (D / (A + C))",
        ),
        "actual scale sign reversed": (
            "six",
            "    (j : ℝ) * Real.log (xiNaturalJensenScale n L y)",
            "    -(j : ℝ) * Real.log (xiNaturalJensenScale n L y)",
        ),
        "model A sign reversed": (
            "six",
            "Real.log D - Real.log A - Real.log C +",
            "Real.log D + Real.log A - Real.log C +",
        ),
        "quotient adapter disconnected": (
            "six",
            "exactXiParameterMap_six_log_coefficients",
            "uncheckedSixLogCoefficientAdapter",
        ),
        "positive parameter proof disconnected": (
            "six",
            "theorem xiNaturalResidualParameters_pos",
            "theorem uncheckedResidualParametersPos",
        ),
        "exponential ratio disconnected": (
            "six",
            "theorem exp_xiNaturalModelLogIncrement",
            "theorem uncheckedExpModelIncrement",
        ),
        "alternating choose step disconnected": (
            "six",
            "theorem alternatingChoose_step",
            "theorem uncheckedAlternatingChooseStep",
        ),
        "coefficient induction disconnected": (
            "six",
            "theorem terminating3F2Coefficient_eq_xiNaturalModel",
            "theorem uncheckedTerminatingCoefficient",
        ),
        "model polynomial identity disconnected": (
            "six",
            "theorem xiNaturalModelLogPolynomial_eq_comparison\n    {n : ℕ}",
            "theorem uncheckedModelPolynomialIdentity\n    {n : ℕ}",
        ),
        "actual evaluation disconnected": (
            "six",
            "theorem eval_xiNaturalActualLogPolynomial",
            "theorem uncheckedActualEvaluation",
        ),
        "six comparison matches disconnected": (
            "six",
            "theorem xiNaturalSixPolynomialCoefficients_match_comparison\n    {n : ℕ}",
            "theorem uncheckedSixComparisonMatches\n    {n : ℕ}",
        ),
        "explicit cutoff match disconnected": (
            "six",
            "theorem xiNaturalSixPolynomialCoefficients_match_comparison_of_explicitCutoff",
            "theorem uncheckedExplicitSixComparisonMatches",
        ),
    }
    for label, (target, old, new) in mutations.items():
        base = transformed if target == "transformed" else six_match
        if old not in base:
            raise AssertionError(f"mutation target changed: {label}")
        changed = base.replace(old, new, 1)
        try:
            if target == "transformed":
                validate(changed, six_match)
            else:
                validate(transformed, changed)
        except ContractError:
            print(f"PASS six-match mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
