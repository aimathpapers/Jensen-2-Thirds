#!/usr/bin/env python3
"""Fail-closed semantic mutations for the Phase-G Arb/ACB suite."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path(__file__).with_name("arb_acb_verification.py")


class ContractError(RuntimeError):
    pass


def validate(text: str) -> None:
    required = {
        "omega one-half": "arb(3) / 2 * pi * k**2 * t",
        "factor eight": "* 8 * factorial(n) / factorial(2 * n)",
        "analytic k tail": "exp(2u)>=1+2u",
        "analytic u tail": "For u=U+v",
        "Rouche quadratic remainder": "second_derivative_bound * disc_radius**2 / 2",
        "Rouche strict inclusion": "if not lhs < rhs:",
        "Q nonvanishing": "if not q_value.abs_lower() > 0:",
        "connector gate": "connector_relative < arb(\"1e-35\")",
        "theta modes": "for mode in (2, 3):",
        "implicit ACB series": "method\": \"ACB implicit local power series",
        "root separation": "if root.overlaps(earlier):",
        "no uniform overclaim": "Finite contour/root grids are",
        "review honesty": "No human or peer review is claimed.",
    }
    for label, needle in required.items():
        if needle not in text:
            raise ContractError(f"missing {label}")


def reject(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS Arb/ACB mutation rejected: {label}")
        return
    raise AssertionError(f"Arb/ACB mutation survived: {label}")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    validate(text)
    print("PASS Arb/ACB source contract")
    mutations = {
        "omega factor transposed": ("arb(3) / 2", "arb(3)"),
        "factor eight dropped": ("* 8 * factorial(n)", "* 4 * factorial(n)"),
        "k tail deleted": ("exp(2u)>=1+2u", "sample k tail"),
        "Rouche remainder deleted": (
            "second_derivative_bound * disc_radius**2 / 2",
            "arb(0)",
        ),
        "Rouche strictness weakened": ("if not lhs < rhs:", "if not lhs <= rhs:"),
        "Q check deleted": ("if not q_value.abs_lower() > 0:", "if False:"),
        "connector loosened": (
            "connector_relative < arb(\"1e-35\")",
            "connector_relative < arb(\"1\")",
        ),
        "higher modes deleted": ("for mode in (2, 3):", "for mode in ():"),
        "root separation deleted": ("if root.overlaps(earlier):", "if False:"),
        "uniformity overclaimed": (
            "Finite contour/root grids are",
            "Finite contour/root grids prove uniform asymptotics and are",
        ),
        "human review overclaimed": (
            "No human or peer review is claimed.",
            "Human peer review is complete.",
        ),
    }
    for label, (old, new) in mutations.items():
        if old not in text:
            raise ContractError(f"missing mutation target {label}")
        reject(label, text.replace(old, new))
    print("PASS all Arb/ACB semantic mutations")


if __name__ == "__main__":
    main()
