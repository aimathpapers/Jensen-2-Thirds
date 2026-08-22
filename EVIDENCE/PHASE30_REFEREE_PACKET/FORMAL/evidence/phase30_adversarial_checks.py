#!/usr/bin/env python3
"""Independent exact regressions and trust-boundary checks for Phase 30."""

from __future__ import annotations

import json
import math
import re
from fractions import Fraction
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[2]
LEAN = ROOT / "Kimi_Agent_Riemann Lean Exploration/zeta-23-lean/Zeta23/Research/JensenWedge"


def forward_difference(values: list[Fraction], k: int) -> Fraction:
    row = values[: k + 1]
    for _ in range(k):
        row = [b - a for a, b in zip(row, row[1:])]
    return row[0]


def exact_newton_regression() -> None:
    x = sp.symbols("x")
    for degree in range(6, 13):
        p = sp.Poly(sp.prod(x - j for j in range(1, degree + 1)), x, domain=sp.QQ)
        denominator = Fraction(10**14)
        c = [
            Fraction(1) + Fraction(math.prod(j - r for r in range(6)), 1) / denominator
            for j in range(degree + 1)
        ]
        assert c[:6] == [Fraction(1)] * 6
        coefficients = [Fraction(p.nth(j)) for j in range(degree + 1)]
        P = sp.Poly(
            sum(sp.Rational(coefficients[j].numerator, coefficients[j].denominator)
                * sp.Rational(c[j].numerator, c[j].denominator) * x**j
                for j in range(degree + 1)),
            x,
            domain=sp.QQ,
        )
        point = sp.Rational(1, 3)
        lhs = sp.cancel(P.eval(point) / p.eval(point) - 1)
        rhs = -1
        for k in range(degree + 1):
            delta = forward_difference(c, k)
            rhs += (
                sp.Rational(delta.numerator, delta.denominator)
                / sp.factorial(k)
                * point**k
                * sp.diff(p.as_expr(), x, k).subs(x, point)
                / p.eval(point)
            )
        assert sp.cancel(lhs - rhs) == 0

        endpoints = [sp.Rational(0)] + [sp.Rational(2 * j + 1, 2) for j in range(1, degree)]
        endpoints_right = [sp.Rational(2 * j + 1, 2) for j in range(1, degree)] + [sp.Rational(degree + 1)]
        for left, right in zip(endpoints, endpoints_right):
            assert p.eval(left) * p.eval(right) < 0
            assert abs(sp.cancel(P.eval(left) / p.eval(left) - 1)) < 1
            assert abs(sp.cancel(P.eval(right) / p.eval(right) - 1)) < 1
            assert P.eval(left) * P.eval(right) < 0
        roots = sp.nroots(P.as_expr(), n=40, maxsteps=200)
        assert len(roots) == degree
        real_roots = [complex(root) for root in roots]
        assert all(abs(root.imag) < 1e-25 and root.real > 0 for root in real_roots)
        assert len({round(root.real, 20) for root in real_roots}) == degree
    print("PASS Phase 30 independent exact Newton/sign-transfer regressions")


def trust_boundary_check() -> None:
    finite_free = (LEAN / "XiNaturalFiniteFreeSpecialization.lean").read_text(encoding="utf-8")
    match = re.search(
        r"structure XiNaturalClassicalRootInputs.*?where(?P<body>.*?)\n\ntheorem",
        finite_free,
        flags=re.S,
    )
    if match is None:
        raise SystemExit("missing XiNaturalClassicalRootInputs")
    body = match.group("body")
    fields = re.findall(r"^  ([a-z_]+)\s*:", body, flags=re.M)
    if fields != ["first_jacobi", "second_jacobi", "mss", "mmp"]:
        raise SystemExit(f"unexpected classical-root fields: {fields}")
    required_types = (
        "RatioFreeJacobiInput",
        "MSSFiniteFreeIntervalInput",
        "MMPLogMeshInput",
    )
    for required in required_types:
        if required not in body:
            raise SystemExit(f"missing typed literature input: {required}")

    certificate = (LEAN / "XiNaturalMultiplierCertificate.lean").read_text(encoding="utf-8")
    headline = re.search(
        r"theorem riemannXiJensen_twoThirds_headline.*?\nend\n\nend Zeta23",
        certificate,
        flags=re.S,
    )
    if headline is None:
        raise SystemExit("missing terminal headline theorem")
    for required in (
        "XiNaturalClassicalRootInputs",
        "riemannXiJensen_twoThirds_low_degree",
        "xiNatural_jensenWedgeCertificate",
        "HasDistinctNegativeRoots",
    ):
        if required not in headline.group(0):
            raise SystemExit(f"headline disconnected from {required}")

    matrix = json.loads(
        (ROOT / "ground_zero_work/phase27/THEOREM_ASSURANCE_MATRIX.json").read_text(
            encoding="utf-8"
        )
    )
    claims = {claim["id"]: claim for claim in matrix["claims"]}
    if claims["T18"]["assurance"] != "green":
        raise SystemExit("T18 assurance map was not advanced to green")
    if claims["T18"]["external_inputs"] != ["Jacobi", "MMP", "MSS"]:
        raise SystemExit("T18 literature boundary is misstated")

    current_surfaces = (
        ROOT / "paper/JENSEN_TWO_THIRDS_MAIN.tex",
        ROOT / "paper/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex",
        ROOT / "paper/c48_detailed_appendices.tex",
        ROOT / "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex",
        ROOT / "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_PUBLIC_EXPLAINER.md",
    )
    stale = ("stops before the final xi-specific", "does not construct the final xi-specific")
    for path in current_surfaces:
        text = path.read_text(encoding="utf-8")
        for phrase in stale:
            if phrase in text:
                raise SystemExit(f"stale endpoint claim in {path}: {phrase}")
    print("PASS Phase 30 typed-input and reader-surface boundary audit")


def main() -> None:
    exact_newton_regression()
    trust_boundary_check()


if __name__ == "__main__":
    main()
