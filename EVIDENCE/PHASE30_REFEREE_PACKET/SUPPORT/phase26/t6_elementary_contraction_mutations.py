#!/usr/bin/env python3
"""Fail closed on mutations of the elementary contraction certificate."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/ElementaryContraction.lean"

REQUIRED = {
    "right inverse": ("theorem gaugeJacobianInvReal_mul_real", 1),
    "right inverse product":
        ("gaugeJacobianInvReal * gaugeJacobianReal = 1", 1),
    "continuous inverse": ("theorem gaugeInverseCLM_comp_center", 1),
    "affine map": ("def exactElementaryAffineMap", 1),
    "full derivative": ("exactElementaryParameterMap_hasFDerivAt", 1),
    "Newton derivative":
        ("theorem fixedInverseNewtonMap_exactElementaryAffine_hasFDerivAt", 1),
    "defect identity": ("theorem fixedInverse_derivative_defect_identity", 1),
    "finite operator source":
        ("exactElementaryJacobian_outerBox_operator_error", 1),
    "variation source":
        ("leadingElementaryJacobian_innerBox_operator_error", 1),
    "inverse source": ("gaugeInverseCLM_norm_le", 1),
    "scale threshold": ("e + x ≤ 1 / 100000000", 1),
    "certificate consumer":
        ("theorem exactElementaryAffine_jacobianIntervalCertificate", 1),
    "contraction target": ("≤ 1 / 2", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary contraction source contract")
    mutations = {
        "inverse order reversed":
            ("gaugeJacobianInvReal * gaugeJacobianReal",
             "gaugeJacobianReal * gaugeJacobianInvReal"),
        "full derivative disconnected":
            ("exactElementaryParameterMap_hasFDerivAt",
             "uncheckedElementaryDerivative"),
        "finite bound disconnected":
            ("exactElementaryJacobian_outerBox_operator_error",
             "uncheckedFiniteOperatorError"),
        "variation disconnected":
            ("leadingElementaryJacobian_innerBox_operator_error",
             "uncheckedVariationError"),
        "inverse norm disconnected":
            ("gaugeInverseCLM_norm_le", "uncheckedInverseNorm"),
        "scale weakened":
            ("e + x ≤ 1 / 100000000", "e + x ≤ 1 / 10000000"),
        "contraction weakened": ("≤ 1 / 2", "≤ 2 / 3"),
        "certificate consumer disconnected":
            ("theorem exactElementaryAffine_jacobianIntervalCertificate",
             "theorem uncheckedJacobianCertificate"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS elementary contraction mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
