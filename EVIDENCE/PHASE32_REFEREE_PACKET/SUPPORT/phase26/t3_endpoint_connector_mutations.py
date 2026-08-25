#!/usr/bin/env python3
"""Fail-closed mutations for the endpoint-connector Gaussian comparison."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration"
    / "zeta-23-lean"
    / "Zeta23"
    / "Research"
    / "JensenWedge"
    / "LeadingEndpointConnector.lean"
)


class ContractError(RuntimeError):
    """A required connector comparison is absent."""


def require(text: str, needle: str, label: str, count: int = 1) -> None:
    actual = text.count(needle)
    if actual != count:
        raise ContractError(f"{label}: expected {count}, found {actual}")


def validate(text: str) -> None:
    checks = {
        "strengthened branch box": (
            "theorem quantitativeSaddleBranch_re_gt_eightHundredThousand\n",
            1,
        ),
        "curvature upper bound": (
            "theorem quantitativeSaddleBranch_curvature_norm_le_parameter_norm\n",
            1,
        ),
        "saddle logarithm": (
            "theorem quantitativeSaddleBranch_log_re_gt_ten\n",
            1,
        ),
        "saddle phase": (
            "theorem quantitativeSaddleBranch_phase_re_gt_eight_parameter_norm\n",
            1,
        ),
        "connector phase": (
            "theorem leadingConnectorPoint_phase_re_le\n",
            1,
        ),
        "connector segment": (
            "theorem quantitativeSaddleBranch_leftSegment_norm_le\n",
            1,
        ),
        "curvature exponential absorption": (
            "theorem quantitativeSaddleBranch_curvature_threeHalves_le_exp_two_parameterNorm\n",
            1,
        ),
        "relative connector theorem": (
            "theorem quantitativeSaddleBranch_leftSegment_relative_inverse_curvature\n",
            1,
        ),
        "Gaussian lower producer": (
            "quantitativeSaddleBranch_norm_integral_leadingGaussian_lower hs",
            1,
        ),
        "exact connector expression": (
            "‖leadingLeftSegment s L.im‖ ≤\n      (1 / ‖K‖) *",
            1,
        ),
    }
    for label, (needle, count) in checks.items():
        require(text, needle, label, count)


def mutate(text: str, old: str, new: str) -> str:
    if old not in text:
        raise AssertionError(f"missing mutation source: {old!r}")
    return text.replace(old, new, 1)


def expect_rejected(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS endpoint-connector mutation rejected: {label}")
        return
    raise AssertionError(f"endpoint-connector mutation survived: {label}")


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    validate(source)
    print("PASS T3 endpoint-connector source contract")
    cases = {
        "branch box weakened": mutate(
            source,
            "theorem quantitativeSaddleBranch_re_gt_eightHundredThousand\n",
            "theorem branch_re_large_unchecked\n",
        ),
        "curvature upper bound removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_curvature_norm_le_parameter_norm\n",
            "theorem curvature_parameter_bound_unchecked\n",
        ),
        "saddle logarithm removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_log_re_gt_ten\n",
            "theorem saddle_log_bound_unchecked\n",
        ),
        "saddle phase removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_phase_re_gt_eight_parameter_norm\n",
            "theorem saddle_phase_bound_unchecked\n",
        ),
        "connector phase removed": mutate(
            source,
            "theorem leadingConnectorPoint_phase_re_le\n",
            "theorem connector_phase_bound_unchecked\n",
        ),
        "connector segment removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_leftSegment_norm_le\n",
            "theorem connector_segment_bound_unchecked\n",
        ),
        "curvature absorption removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_curvature_threeHalves_le_exp_two_parameterNorm\n",
            "theorem curvature_absorption_unchecked\n",
        ),
        "relative theorem removed": mutate(
            source,
            "theorem quantitativeSaddleBranch_leftSegment_relative_inverse_curvature\n",
            "theorem connector_relative_unchecked\n",
        ),
        "Gaussian lower disconnected": mutate(
            source,
            "quantitativeSaddleBranch_norm_integral_leadingGaussian_lower hs",
            "gaussian_lower_unchecked hs",
        ),
        "inverse curvature dropped": mutate(
            source,
            "‖leadingLeftSegment s L.im‖ ≤\n      (1 / ‖K‖) *",
            "‖leadingLeftSegment s L.im‖ ≤\n      ‖K‖ *",
        ),
    }
    for label, changed in cases.items():
        expect_rejected(label, changed)


if __name__ == "__main__":
    main()
