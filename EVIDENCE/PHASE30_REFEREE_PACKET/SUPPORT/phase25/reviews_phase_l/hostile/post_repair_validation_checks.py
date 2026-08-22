#!/usr/bin/env python3
"""Post-repair definition-level validation for the Phase-L hostile track.

The phase, Jacobian, contour geometry, and recurrence coefficient are rebuilt
from definitions.  Current manuscript and effectivity files are artifacts
under test; no frozen calculation is treated as expected data.
"""

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
MAIN = ROOT / "paper/JENSEN_TWO_THIRDS_MAIN.tex"
SUPPLEMENT = ROOT / "paper/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex"
APPENDICES = ROOT / "paper/c48_detailed_appendices.tex"
LEDGER = ROOT / "ground_zero_work/phase25/EFFECTIVITY_LEDGER.md"


def verify_phase_and_jacobian() -> None:
    u = sp.symbols("u", positive=True)
    q = sp.symbols("q")

    phi = q * sp.log(u) - sp.Rational(3, 4) * u - sp.pi * sp.exp(u)
    g = sp.exp(u) * sp.exp(phi)
    original_integrand = sp.exp(
        q * sp.log(u) + sp.Rational(1, 4) * u - sp.pi * sp.exp(u)
    )
    assert sp.simplify(g / original_integrand) == 1

    saddle_substitution = {q: u * (sp.pi * sp.exp(u) + sp.Rational(3, 4))}
    assert sp.simplify(sp.diff(phi, u).subs(saddle_substitution)) == 0
    curvature = -sp.diff(phi, u, 2).subs(saddle_substitution)
    expected_curvature = q / u**2 + sp.pi * sp.exp(u)
    assert sp.simplify(curvature - expected_curvature.subs(saddle_substitution)) == 0


def verify_legal_ray() -> None:
    alpha, b, x = sp.symbols("alpha b x", real=True)
    saddle = alpha + sp.I * b
    r = x - alpha
    u = sp.simplify(saddle + r)

    assert u == x + sp.I * b
    assert sp.re(u) == x
    assert sp.simplify((saddle + (1 - alpha)) - (1 + sp.I * b)) == 0

    # This reproduces why the old full-line range was illegal when b=0.
    assert sp.simplify((saddle - alpha - 1).subs(b, 0)) == -1


def verify_recurrence_coefficient() -> None:
    A, B, C, D, y, m, d = sp.symbols("A B C D y m d")
    lam = D / (A * C)

    numerator_parameters = (m - d, A + m, C + m)
    e1 = sp.expand(sum(numerator_parameters))
    from_ode = B + m + D + m + 1 - lam * y * (3 + e1)
    displayed = B + D + 2 * m + 1 - lam * y * (A + C + 3 * m - d + 3)
    assert sp.simplify(from_ode - displayed) == 0

    a = 1 - y / A
    b_m_plus_1 = B + m + 1 - y + (d - 1 - 2 * (m + 1)) * y / A
    epsilon = (C - D) / C
    decomposed = (
        b_m_plus_1
        + (D + m) * a
        + epsilon * y / A * (A - d + 3 + 3 * m)
    )
    assert sp.simplify(decomposed - displayed) == 0

    stale = B + D + 3 * m + 1 - lam * y * (A + C + 3 * m - d + 3)
    assert sp.simplify(stale - displayed) == m


def verify_current_sources() -> None:
    main = MAIN.read_text(encoding="utf-8")
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    appendices = APPENDICES.read_text(encoding="utf-8")
    joined = "\n".join((main, supplement, appendices))

    main_phase = r"\Phi_s(u)=s\operatorname{Log}u-\frac34u-\pi e^u"
    other_phase = r"\Phi_N(u)=N\operatorname{Log}u-\frac34u-\pi e^u"
    main_alias = r"I_1(s):=F_1(s):=\int_0^\infty g_s(u)\,\dd u"
    other_alias = r"I_1(N):=F_1(N):=\int_0^\infty g_N(u)\,\dd u"

    assert main_phase in main
    assert r"g_s(u)=e^u e^{\Phi_s(u)}" in main
    assert main_alias in main
    for source in (supplement, appendices):
        assert other_phase in source
        assert r"g_N(u)=e^u e^{\Phi_N(u)}" in source
        assert other_alias in source

    assert r"r\ge1-\Re L_s" in main
    assert r"r\ge1-\Re L_N" in supplement
    assert r"r\ge1-\Re L_N" in appendices
    assert r"u=L_s+r$ with $r\in\R" not in joined
    assert r"u=L_N+r$, $r\in\R" not in joined

    assert r"P_{2,m}&=B+D+2m+1" in supplement
    assert r"P_{2,m}&=B+D+2m+1" in appendices
    assert r"P_{2,m}&=B+D+3m+1" not in joined

    assert r"N_0=\max\{N_{\rm analytic},N_{\rm explicit}\}" in main
    assert r"N_{\rm elementary}" not in joined
    assert "N_0 = max(N_explicit, N_analytic)" in LEDGER.read_text(encoding="utf-8")


def main() -> None:
    verify_phase_and_jacobian()
    verify_legal_ray()
    verify_recurrence_coefficient()
    verify_current_sources()
    print(
        "PASS post-repair Phi/g/I_1=F_1, legal ray, recurrence, and effectivity validation"
    )


if __name__ == "__main__":
    main()
