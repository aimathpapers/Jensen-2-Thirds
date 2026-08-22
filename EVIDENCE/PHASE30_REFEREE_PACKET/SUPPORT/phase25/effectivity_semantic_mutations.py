#!/usr/bin/env python3
"""Fail-closed mutations for the Phase-H effectivity ledger producer."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path(__file__).with_name("effectivity_ledger.py")


class ContractError(RuntimeError):
    pass


def validate(text: str) -> None:
    required = {
        "correct localization constant": "12+8*sqrt(6)",
        "provisional threshold": "k_pre = Q(256)",
        "strengthened threshold": "k_zero = k_pre * c_loc_upper**2",
        "explicit C0": "c_zero = Q(48)",
        "explicit C1": "c_one_upper = Q(96)",
        "radius order": "k_radius = Q(4096)",
        "constant neighbor budget": "q_constant_margin = Q(1, 4) - q_constant",
        "domain containment": "x_domain = eta**2 / (48 * k_radius**2)",
        "geometry wedge": "k_geometry = ceil_fraction(x_admissible ** -3) + 1",
        "sixth constant external": 'node("C_B6", "external_constant"',
        "analytic threshold external": 'node("N_analytic", "external_threshold"',
        "finite range": '"N_0^2*(N_0+2)+1"',
        "final dependency": '"max(K_geometry,C_multiplier_factor*C_B6,K_finite)"',
        "no numeric final K": 'if by_id["K_final"]["value"] is not None:',
        "no diagnostic promotion": "Diagnostics are excluded from K_final.",
    }
    for label, needle in required.items():
        if needle not in text:
            raise ContractError(f"missing {label}")


def reject(label: str, text: str) -> None:
    try:
        validate(text)
    except ContractError:
        print(f"PASS effectivity mutation rejected: {label}")
        return
    raise AssertionError(f"effectivity mutation survived: {label}")


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    validate(text)
    print("PASS effectivity source contract")
    mutations = {
        "C_loc transposed": ("12+8*sqrt(6)", "8+12*sqrt(6)"),
        "K_pre regressed": ("k_pre = Q(256)", "k_pre = Q(32)"),
        "C0 hidden": ("c_zero = Q(48)", "c_zero = Q(1)"),
        "C1 hidden": ("c_one_upper = Q(96)", "c_one_upper = Q(1)"),
        "K_r chosen before bounds": ("k_radius = Q(4096)", "k_radius = Q(32)"),
        "neighbor margin removed": (
            "q_constant_margin = Q(1, 4) - q_constant",
            "q_constant_margin = Q(1)",
        ),
        "domain cap removed": (
            "x_domain = eta**2 / (48 * k_radius**2)",
            "x_domain = Q(1)",
        ),
        "C_B6 fabricated": (
            'node("C_B6", "external_constant"',
            'node("C_B6", "exact_integer"',
        ),
        "analytic threshold fabricated": (
            'node("N_analytic", "external_threshold"',
            'node("N_analytic", "exact_integer"',
        ),
        "finite range omitted": (
            '"N_0^2*(N_0+2)+1"',
            '"1"',
        ),
        "analytic constant omitted from K": (
            '"max(K_geometry,C_multiplier_factor*C_B6,K_finite)"',
            '"max(K_geometry,K_finite)"',
        ),
        "diagnostic promoted": (
            "Diagnostics are excluded from K_final.",
            "The 10.7 diagnostic defines K_final.",
        ),
    }
    for label, (old, new) in mutations.items():
        if old not in text:
            raise ContractError(f"missing mutation target {label}")
        reject(label, text.replace(old, new))
    print("PASS all effectivity semantic mutations")


if __name__ == "__main__":
    main()
