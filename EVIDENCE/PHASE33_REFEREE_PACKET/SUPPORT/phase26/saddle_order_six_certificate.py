#!/usr/bin/env python3
"""Independent source-to-Lean check and semantic mutations for the H6 certificate."""

from __future__ import annotations

import re
from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
LEAN = (
    ROOT
    / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/SaddleOrderSix.lean"
)
TERM = re.compile(r"⟨(-?\d+),\s*(\d+),\s*(\d+)⟩")
EXPECTED_MAJORANT = Fraction(
    6422139805764931584036533551104,
    702576099728137594188684005,
)


def reconstruct() -> dict[int, dict[tuple[int, int], int]]:
    """Rebuild H6 from G0 and the implicit saddle differential operator."""
    n, ell, r, sigma = sp.symbols("N L r sigma")
    q = (1 + ell) * n - sp.Rational(3, 4) * ell**2
    main = (
        (n + 1) * sp.log(ell)
        + ell / 4
        - n / ell
        - sp.log(q) / 2
    )

    def derivative(expression: sp.Expr) -> sp.Expr:
        return sp.cancel(
            sp.together(sp.diff(expression, n) + ell / q * sp.diff(expression, ell))
        )

    tower: dict[int, dict[tuple[int, int], int]] = {}
    current = main
    for order in range(1, 7):
        current = derivative(current)
        if order < 2:
            continue
        reduced = sp.cancel(
            sp.together(current * n ** (order - 1) * ell)
        ).subs({ell: 1 / r, n: 1 / (r * sigma)})
        reduced = sp.cancel(sp.together(sp.simplify(reduced)))
        numerator, denominator = sp.fraction(reduced)
        if sp.factor(denominator) != (4 + 4 * r - 3 * sigma) ** (2 * order):
            raise AssertionError(f"independent H{order} denominator reconstruction failed")
        tower[order] = {
            monomial: int(coefficient)
            for monomial, coefficient in sp.Poly(numerator, r, sigma).terms()
        }
    return tower


def parse_terms(text: str, name: str = "h6Terms") -> dict[tuple[int, int], int]:
    matches = TERM.findall(text.split(f"def {name}", 1)[1].split("]", 1)[0])
    terms: dict[tuple[int, int], int] = {}
    for coefficient, r_power, sigma_power in matches:
        key = (int(r_power), int(sigma_power))
        if key in terms:
            raise AssertionError(f"duplicate H6 monomial {key}")
        terms[key] = int(coefficient)
    return terms


def exact_majorant(terms: dict[tuple[int, int], int]) -> Fraction:
    radius = Fraction(7, 50)
    numerator = sum(
        abs(coefficient) * radius ** (r_power + sigma_power)
        for (r_power, sigma_power), coefficient in terms.items()
    )
    denominator = Fraction(151, 50) ** 12
    return numerator / denominator


def validate(terms: dict[tuple[int, int], int], expected: dict[tuple[int, int], int]) -> None:
    if terms != expected:
        raise AssertionError("Lean coefficient table differs from definition-level reconstruction")
    if len(terms) != 82:
        raise AssertionError("H6 term count changed")
    if max(sum(monomial) for monomial in terms) != 13:
        raise AssertionError("H6 total degree changed")
    majorant = exact_majorant(terms)
    if majorant != EXPECTED_MAJORANT or not majorant < 10_000:
        raise AssertionError("H6 exact majorant changed")


def expect_rejected(
    label: str,
    terms: dict[tuple[int, int], int],
    expected: dict[tuple[int, int], int],
) -> None:
    try:
        validate(terms, expected)
    except AssertionError:
        print(f"PASS mutation rejected: {label}")
        return
    raise AssertionError(f"mutation escaped: {label}")


def main() -> None:
    text = LEAN.read_text(encoding="utf-8")
    tower = reconstruct()
    expected = tower[6]
    actual = parse_terms(text)
    validate(actual, expected)
    algebra_text = (
        ROOT
        / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge/SaddleOrderSixAlgebra.lean"
    ).read_text(encoding="utf-8")
    expected_counts = {2: 15, 3: 28, 4: 43, 5: 61}
    for order, count in expected_counts.items():
        lean_terms = parse_terms(algebra_text, f"h{order}Terms")
        if lean_terms != tower[order] or len(lean_terms) != count:
            raise AssertionError(f"Lean H{order} table differs from reconstruction")
    for theorem in (
        "h3DensePolynomial_recurrence",
        "h4DensePolynomial_recurrence",
        "h5DensePolynomial_recurrence",
        "h6GeneratedDensePolynomial_eq_frozen",
    ):
        if theorem not in algebra_text:
            raise AssertionError(f"missing kernel recurrence theorem {theorem}")

    changed_sign = actual.copy()
    changed_sign[(12, 1)] *= -1
    expect_rejected("leading coefficient sign", changed_sign, expected)

    changed_coefficient = actual.copy()
    changed_coefficient[(7, 3)] += 1
    expect_rejected("interior numerator coefficient", changed_coefficient, expected)

    missing_term = actual.copy()
    del missing_term[(0, 0)]
    expect_rejected("missing constant term", missing_term, expected)

    extra_degree = actual.copy()
    extra_degree[(13, 1)] = 1
    expect_rejected("degree-fourteen monomial", extra_degree, expected)

    required_source = (
        "(4 + 4 * r - 3 * sigma) ^ 12",
        "bivariateTermsMajorant h6Terms (7 / 50)",
        "h6Majorant < 10000",
        "saddleH6_norm_lt_tenThousand",
    )
    for snippet in required_source:
        if snippet not in text:
            raise AssertionError(f"missing Lean certificate surface: {snippet}")
    if re.search(r"^\s*(sorry|admit|axiom|unsafe)\b", text, re.MULTILINE):
        raise AssertionError("proof escape in SaddleOrderSix.lean")
    print("PASS independent H6 reconstruction matches 82 Lean coefficients")
    print("PASS independent H2--H5 reconstruction matches 15/28/43/61 Lean coefficients")
    print(f"PASS exact H6 majorant {EXPECTED_MAJORANT} < 10000")


if __name__ == "__main__":
    main()
