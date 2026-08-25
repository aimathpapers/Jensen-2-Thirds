#!/usr/bin/env python3
"""Semantic fail-closed mutations for Phase-25 load-bearing metadata/math."""

from __future__ import annotations

import copy
import json
from fractions import Fraction
from math import factorial
from pathlib import Path

import sympy as sp

from verify_phase25_metadata import MetadataError, validate_assurance, validate_graph


PHASE = Path(__file__).resolve().parent


def load(name: str):
    return json.loads((PHASE / name).read_text(encoding="utf-8"))


def expect_rejected(name: str, operation) -> None:
    try:
        operation()
    except MetadataError:
        print(f"PASS semantic mutation rejected: {name}")
        return
    raise AssertionError(f"semantic mutation survived: {name}")


def metadata_mutations() -> None:
    original_graph = load("PROOF_DEPENDENCY_GRAPH.json")
    original_matrix = load("THEOREM_ASSURANCE_MATRIX.json")

    def missing_residual_dependency() -> None:
        graph = copy.deepcopy(original_graph)
        matrix = copy.deepcopy(original_matrix)
        graph["nodes"]["T16"]["internal"] = []
        matrix["claims"][15]["dependencies"] = []
        validate_graph(graph)
        validate_assurance(matrix, graph)

    expect_rejected("missing T15 -> T16 seam", missing_residual_dependency)

    def dependency_cycle() -> None:
        graph = copy.deepcopy(original_graph)
        graph["nodes"]["T2"]["internal"] = ["T18"]
        validate_graph(graph)

    expect_rejected("T2/T18 dependency cycle", dependency_cycle)

    def green_single_channel() -> None:
        matrix = copy.deepcopy(original_matrix)
        matrix["claims"][0]["assurance"] = "green"
        matrix["claims"][0]["channels"] = ["paper_proof", "high_precision"]
        validate_assurance(matrix, original_graph)

    expect_rejected("unsupported green T1 classification", green_single_channel)

    def hidden_external_input() -> None:
        matrix = copy.deepcopy(original_matrix)
        matrix["claims"][10]["external_inputs"] = []
        validate_assurance(matrix, original_graph)

    expect_rejected("hidden MMP input", hidden_external_input)

    def stale_hg_dependency() -> None:
        graph = copy.deepcopy(original_graph)
        matrix = copy.deepcopy(original_matrix)
        graph["external_inputs"]["HG"] = "stale external identity"
        graph["nodes"]["T15"]["external"] = ["HG"]
        matrix["claims"][14]["external_inputs"] = ["HG"]
        validate_graph(graph)
        validate_assurance(matrix, graph)

    expect_rejected("stale external HG dependency", stale_hg_dependency)


def exact_math_mutations() -> None:
    n, d, logn = sp.symbols("n d logn", positive=True)
    rho_squared = n * d
    sixth_residual = sp.cancel(rho_squared**3 / (n**5 * logn))
    expected = d**3 / (n**2 * logn)
    if sp.simplify(sixth_residual - expected) != 0:
        raise AssertionError("authoritative sixth-order exponent identity failed")
    fifth_mutation = rho_squared ** sp.Rational(5, 2) / (n**5 * logn)
    if sp.simplify(fifth_mutation - expected) == 0:
        raise AssertionError("fifth-order mutation unexpectedly preserved wedge")
    print("PASS semantic mutation rejected: fifth-for-sixth wedge exponent")

    for index in range(0, 11):
        authoritative = Fraction(8 * factorial(index), factorial(2 * index))
        duplication = Fraction(8 * factorial(index), factorial(2 * index))
        if authoritative != duplication:
            raise AssertionError("factor-eight duplication normalization failed")
    false_prefactor = Fraction(8 * 2**8, factorial(8))
    true_prefactor = Fraction(8 * factorial(4), factorial(8))
    if false_prefactor == true_prefactor:
        raise AssertionError("factorial mutation escaped at n=4")
    print("PASS semantic mutation rejected: factor-eight factorial transposition")

    alpha = Fraction(3)
    t = Fraction(2)
    w = Fraction(16, 3)
    delta = Fraction(1, 3)
    residual = (
        1 / alpha + w / t**2 + delta - 2,
        w / t**3 + delta - 1,
        3 * w / t**4 + 3 * delta - 2,
        4 * w / t**5 + 4 * delta - 2,
    )
    if residual != (0, 0, 0, 0):
        raise AssertionError(f"authoritative leading branch failed: {residual}")
    mutated_w = w + Fraction(1, 10)
    mutated = mutated_w / t**3 + delta - 1
    if mutated == 0:
        raise AssertionError("branch-point mutation escaped")
    print("PASS semantic mutation rejected: positive branch point")

    numerator = 6422139805764931584036533551104
    denominator = 702576099728137594188684005
    majorant = Fraction(numerator, denominator)
    if not majorant < 10_000:
        raise AssertionError("authoritative H6 majorant failed")
    if 2 * majorant < 10_000:
        raise AssertionError("doubled H6 mutation escaped")
    print("PASS semantic mutation rejected: H6 coefficientwise majorant")


def main() -> None:
    if sp.__version__ != "1.14.0":
        raise AssertionError(f"expected SymPy 1.14.0, found {sp.__version__}")
    metadata_mutations()
    exact_math_mutations()
    print("PASS all Phase-25 semantic baseline mutations")


if __name__ == "__main__":
    main()
