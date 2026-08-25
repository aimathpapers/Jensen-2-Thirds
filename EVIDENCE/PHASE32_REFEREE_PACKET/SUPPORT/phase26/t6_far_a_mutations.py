#!/usr/bin/env python3
"""Fail-closed source mutations for the separate distant-A anchor."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
LEAN = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/"
    "JensenWedge"
)
ASSEMBLY = LEAN / "SixthResidualAssembly.lean"
GEOMETRY = LEAN / "ResidualParameterGeometry.lean"
MOMENT = LEAN / "MomentSaddleResidual.lean"


class ContractError(RuntimeError):
    """The distant-A source contract changed."""


def validate(files: dict[str, str]) -> None:
    required = {
        "assembly": {
            "separate theorem":
                "theorem manuscriptSixthResidualValue_norm_le_separateA",
            "separate anchor": "{n m mA : ℕ}",
            "A right half plane": "(hA : (mA : ℝ) ≤ (A + z).re)",
            "A fifth tail": "24 / (((mA - 1 : ℕ) : ℝ) ^ 5)",
        },
        "geometry": {
            "far anchor theorem":
                "theorem residualParameterA_floor_anchor_of_outerBox",
            "floor anchor": "2 ≤ ⌊(n : ℝ) / e⌋₊",
            "A lower box face":
                "rcases hy with ⟨ha0, _ha1, _ht0, _ht1, _hw0, _hw1, _hd0, _hd1⟩",
            "reciprocal lower bound":
                "12 * (n : ℝ) ≤ (n : ℝ) / e",
            "A scale comparison":
                "(5 / 2 : ℝ) * ((n : ℝ) / e) ≤ residualParameterA y n e",
        },
        "moment": {
            "far residual theorem":
                "theorem manuscriptSixthResidual_outerBox_farA_norm_le",
            "far anchor source":
                "residualParameterA_floor_anchor_of_outerBox hy hn he he12 hzRe",
            "separate assembly source":
                "manuscriptSixthResidualValue_norm_le_separateA",
            "far tail":
                "24 / (((⌊(n : ℝ) / e⌋₊ - 1 : ℕ) : ℝ) ^ 5)",
            "two anchors consumed":
                "C.anchor_two hA.1 hSix C.B_right C.C_right C.D_right C.half_right hA.2",
        },
    }
    for file_label, contracts in required.items():
        for contract_label, needle in contracts.items():
            if needle not in files[file_label]:
                raise ContractError(f"{file_label}: {contract_label}")


def main() -> None:
    files = {
        "assembly": ASSEMBLY.read_text(),
        "geometry": GEOMETRY.read_text(),
        "moment": MOMENT.read_text(),
    }
    validate(files)
    print("PASS T6 distant-A source contract")
    mutations = {
        "separate theorem removed": (
            "assembly",
            "theorem manuscriptSixthResidualValue_norm_le_separateA",
            "theorem uncheckedSeparateAResidual",
        ),
        "far tail exponent changed": (
            "assembly",
            "24 / (((mA - 1 : ℕ) : ℝ) ^ 5)",
            "24 / (((mA - 1 : ℕ) : ℝ) ^ 4)",
        ),
        "floor anchor removed": (
            "geometry",
            "theorem residualParameterA_floor_anchor_of_outerBox",
            "theorem uncheckedFarAAnchor",
        ),
        "reciprocal lower bound weakened": (
            "geometry",
            "12 * (n : ℝ) ≤ (n : ℝ) / e",
            "6 * (n : ℝ) ≤ (n : ℝ) / e",
        ),
        "A box source disconnected": (
            "geometry",
            "rcases hy with ⟨ha0, _ha1, _ht0, _ht1, _hw0, _hw1, _hd0, _hd1⟩",
            "obtain ⟨ha0, _ha1, _ht0, _ht1, _hw0, _hw1, _hd0, _hd1⟩ := uncheckedBox",
        ),
        "far residual removed": (
            "moment",
            "theorem manuscriptSixthResidual_outerBox_farA_norm_le",
            "theorem uncheckedFarAResidual",
        ),
        "far anchor source disconnected": (
            "moment",
            "residualParameterA_floor_anchor_of_outerBox hy hn he he12 hzRe",
            "uncheckedFarAAnchor hy hn he he12 hzRe",
        ),
        "separate assembly disconnected": (
            "moment",
            "manuscriptSixthResidualValue_norm_le_separateA",
            "uncheckedSeparateAAssembly",
        ),
        "final far tail exponent changed": (
            "moment",
            "24 / (((⌊(n : ℝ) / e⌋₊ - 1 : ℕ) : ℝ) ^ 5)",
            "24 / (((⌊(n : ℝ) / e⌋₊ - 1 : ℕ) : ℝ) ^ 4)",
        ),
    }
    for label, (file_label, old, new) in mutations.items():
        changed = dict(files)
        changed[file_label] = changed[file_label].replace(old, new)
        try:
            validate(changed)
        except ContractError:
            print(f"PASS T6 distant-A mutation rejected: {label}")
            continue
        raise AssertionError(f"mutation survived: {label}")


if __name__ == "__main__":
    main()
