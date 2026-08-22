#!/usr/bin/env python3
"""Fail closed on mutations of the elementary residual/branch bridge."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/ElementaryResidualBranch.lean"

REQUIRED = {
    "value source": ("exactElementaryParameterMap_outerBox_value_error", 1),
    "limiting zero": ("leadingXiParameterMap_center", 1),
    "elementary constant": ("10000 * (e + x / e)", 5),
    "saddle enclosure":
        ("‖saddle - leadingXiSaddleVector‖ ≤ epsilon", 3),
    "residual threshold": ("(3 / 608) * branchInnerRadius", 2),
    "residual certificate":
        ("theorem exactElementaryAffine_residualIntervalCertificate", 1),
    "jacobian certificate":
        ("exactElementaryAffine_jacobianIntervalCertificate", 1),
    "branch consumer":
        ("PositiveParameterBranch.ofIntervalCertificates", 1),
}


def validate(text: str) -> None:
    for label, (needle, count) in REQUIRED.items():
        if text.count(needle) != count:
            raise RuntimeError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS elementary residual branch source contract")
    mutations = {
        "value source disconnected":
            ("exactElementaryParameterMap_outerBox_value_error",
             "uncheckedElementaryValueError"),
        "limiting zero disconnected":
            ("leadingXiParameterMap_center", "uncheckedLeadingCenter"),
        "elementary constant weakened":
            ("10000 * (e + x / e)", "1000 * (e + x / e)"),
        "saddle sign reversed":
            ("saddle - leadingXiSaddleVector",
             "leadingXiSaddleVector - saddle"),
        "residual threshold weakened":
            ("(3 / 608) * branchInnerRadius",
             "(3 / 600) * branchInnerRadius"),
        "residual certificate disconnected":
            ("theorem exactElementaryAffine_residualIntervalCertificate",
             "theorem uncheckedResidualCertificate"),
        "jacobian certificate disconnected":
            ("exactElementaryAffine_jacobianIntervalCertificate",
             "uncheckedJacobianCertificate"),
        "branch consumer disconnected":
            ("PositiveParameterBranch.ofIntervalCertificates",
             "PositiveParameterBranch.unchecked"),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except RuntimeError:
            print(f"PASS elementary residual branch mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
