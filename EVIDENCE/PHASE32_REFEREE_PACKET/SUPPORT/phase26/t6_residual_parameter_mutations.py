#!/usr/bin/env python3
"""Fail-closed mutations for concrete sixth-residual parameter geometry."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge/ResidualParameterGeometry.lean"
)


class ContractError(RuntimeError):
    """The residual parameter-geometry contract changed."""


def validate(text: str) -> None:
    required = {
        "A definition": "def residualParameterA",
        "A scale": "y 0 * n / e",
        "B definition": "def residualParameterB",
        "B scale": "n * (y 1 + y 2 * e)",
        "C definition": "def residualParameterC",
        "C scale": "n * y 1",
        "D definition": "def residualParameterD",
        "D scale": "n * (1 + y 3 * e)",
        "Jacobi bridge": "theorem residualParameters_eq_jacobiParameters",
        "reciprocal scale": "jacobiA y (1 / n) e",
        "certificate type": "structure ResidualParameterCertificate",
        "quarter anchor": "anchor_two : 2 ≤ n / 4",
        "BC displacement": "6 * n * e",
        "D-half displacement": "(5 / 12 : ℝ) * n * e + 1 / 2",
        "outer-box constructor":
            "theorem residualParameterCertificate_of_outerBox",
        "floor-cast source": "Nat.cast_div_le (m := n) (n := 4)",
        "outer box destructuring":
            "rcases hy with ⟨ha0, ha1, ht0, ht1, hw0, hw1, hd0, hd1⟩",
        "final instantiated residual":
            "theorem manuscriptSixthResidual_outerBox_norm_le",
        "translated xi point":
            "manuscriptXiSixthLogDecomposition mainSix ((n : ℂ) + z)",
        "end-to-end source":
            "manuscriptSixthResidualValue_of_xiDecomposition_norm_le",
    }
    expected_counts = {
        "y 0 * n / e": 2,
        "6 * n * e": 3,
        "(5 / 12 : ℝ) * n * e + 1 / 2": 3,
    }
    for label, needle in required.items():
        if text.count(needle) != expected_counts.get(needle, 1):
            raise ContractError(label)


def main() -> None:
    source = SOURCE.read_text()
    validate(source)
    print("PASS T6 residual-parameter source contract")
    mutations = {
        "A definition removed": (
            "def residualParameterA", "def uncheckedResidualParameterA"),
        "A scale changed": ("y 0 * n / e", "y 0 * n * e"),
        "B scale changed": (
            "n * (y 1 + y 2 * e)", "n * (y 1 - y 2 * e)"),
        "C scale changed": ("n * y 1", "n + y 1"),
        "D scale changed": (
            "n * (1 + y 3 * e)", "n * (1 - y 3 * e)"),
        "Jacobi bridge removed": (
            "theorem residualParameters_eq_jacobiParameters",
            "theorem uncheckedJacobiBridge",
        ),
        "reciprocal scale changed": (
            "jacobiA y (1 / n) e", "jacobiA y n e"),
        "certificate removed": (
            "structure ResidualParameterCertificate",
            "structure UncheckedResidualParameterCertificate",
        ),
        "anchor weakened": ("anchor_two : 2 ≤ n / 4", "anchor_two : 1 ≤ n / 4"),
        "BC constant changed": ("6 * n * e", "7 * n * e"),
        "D-half constant changed": (
            "(5 / 12 : ℝ) * n * e + 1 / 2",
            "(1 / 2 : ℝ) * n * e + 1 / 2",
        ),
        "outer constructor removed": (
            "theorem residualParameterCertificate_of_outerBox",
            "theorem uncheckedOuterBoxCertificate",
        ),
        "floor cast disconnected": (
            "Nat.cast_div_le (m := n) (n := 4)",
            "uncheckedFloorCast n",
        ),
        "outer box disconnected": (
            "rcases hy with ⟨ha0, ha1, ht0, ht1, hw0, hw1, hd0, hd1⟩",
            "obtain ⟨ha0, ha1, ht0, ht1, hw0, hw1, hd0, hd1⟩ := uncheckedBox",
        ),
        "final theorem removed": (
            "theorem manuscriptSixthResidual_outerBox_norm_le",
            "theorem uncheckedOuterBoxResidual",
        ),
        "xi translation dropped": (
            "manuscriptXiSixthLogDecomposition mainSix ((n : ℂ) + z)",
            "manuscriptXiSixthLogDecomposition mainSix z",
        ),
        "end-to-end source disconnected": (
            "manuscriptSixthResidualValue_of_xiDecomposition_norm_le",
            "uncheckedResidualAssembly",
        ),
    }
    for label, (old, new) in mutations.items():
        changed = source.replace(old, new, 1)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 residual-parameter mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
