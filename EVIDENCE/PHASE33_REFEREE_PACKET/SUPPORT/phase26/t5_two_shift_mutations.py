#!/usr/bin/env python3
"""Fail-closed source mutations for T5 two-shift error assembly."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/TwoShiftCoefficient.lean"
)


class ContractError(RuntimeError):
    """The T5 two-shift assembly contract is absent or ambiguous."""


def validate(text: str) -> None:
    required = {
        "relative error definition": "def twoShiftRelativeError",
        "exact cancellation identity": "theorem twoShiftRelativeError_exact",
        "scaled assembly": "theorem twoShiftAssembly_of_errors",
        "relative factorization":
            "theorem holomorphicRelativeError_factorization",
        "subtraction-to-relative bound":
            "theorem holomorphicRelativeError_norm_le_of_sub_le",
        "concrete saddle main": "def saddleMomentMain",
        "main nonvanishing": "theorem saddleMomentMain_ne_zero",
        "T3--T4 relative producer":
            "quantitativeSaddleBranch_fullThetaMoment_relative_error_le hs",
        "exact full-moment assembly": "theorem fullThetaTwoShiftAssembly",
        "quantitative full-moment assembly":
            "theorem fullThetaTwoShiftRelativeError_norm_le",
        "ratio error interaction":
            "ratioError + upperError + ratioError * upperError",
        "cancellation denominator": "coefficient - saddleScale ^ 2",
    }
    expected_counts = {
        "ratio error interaction": 5,
        "cancellation denominator": 11,
    }
    for label, needle in required.items():
        count = text.count(needle)
        expected = expected_counts.get(label, 1)
        if count != expected:
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T5 two-shift source contract")
    mutations = {
        "relative error definition removed": (
            "def twoShiftRelativeError",
            "def twoShiftErrorUnchecked",
        ),
        "cancellation identity removed": (
            "theorem twoShiftRelativeError_exact",
            "theorem cancellation_identity_unchecked",
        ),
        "relative conversion removed": (
            "theorem holomorphicRelativeError_norm_le_of_sub_le",
            "theorem relative_conversion_unchecked",
        ),
        "main nonvanishing removed": (
            "theorem saddleMomentMain_ne_zero",
            "theorem saddle_main_nonzero_unchecked",
        ),
        "T3--T4 theorem disconnected": (
            "quantitativeSaddleBranch_fullThetaMoment_relative_error_le hs",
            "full_moment_bound_unchecked hs",
        ),
        "ratio cross term dropped": (
            "ratioError + upperError + ratioError * upperError",
            "ratioError + upperError",
        ),
        "cancellation denominator sign changed": (
            "coefficient - saddleScale ^ 2",
            "coefficient + saddleScale ^ 2",
        ),
        "final quantitative theorem removed": (
            "theorem fullThetaTwoShiftRelativeError_norm_le",
            "theorem final_two_shift_bound_unchecked",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T5 two-shift mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
