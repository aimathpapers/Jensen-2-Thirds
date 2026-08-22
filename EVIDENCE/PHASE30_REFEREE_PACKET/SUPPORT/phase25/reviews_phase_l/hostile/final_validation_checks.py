#!/usr/bin/env python3
"""Definition-level checks for the final Phase-L hostile validation.

The algebraic objects below are rebuilt from the defining hypergeometric ODE
and contour geometry.  No frozen calculation result is used as expected data.
"""

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[4]
MAIN = ROOT / "paper/JENSEN_TWO_THIRDS_MAIN.tex"
SUPPLEMENT = ROOT / "paper/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex"
APPENDICES = ROOT / "paper/c48_detailed_appendices.tex"
LEDGER = ROOT / "ground_zero_work/phase25/EFFECTIVITY_LEDGER.md"


def check_contour_geometry() -> None:
    alpha, b, x = sp.symbols("alpha b x", real=True)
    saddle = alpha + sp.I * b
    r = x - alpha
    u = sp.simplify(saddle + r)
    assert u == x + sp.I * b

    # The translated ray starts at x=1, not at r=-infinity.
    r_min = 1 - alpha
    assert sp.simplify(saddle + r_min) == 1 + sp.I * b
    # Every actual ray point has Re(u)=x>=1, hence misses (-infinity,0].
    assert sp.re(u) == x

    # A literal full line would still be illegal at the real saddle b=0.
    r_bad = -alpha - 1
    assert sp.simplify((saddle + r_bad).subs(b, 0)) == -1


def check_p2_from_ode() -> None:
    A, B, C, D, y, m, d = sp.symbols("A B C D y m d")
    lam = D / (A * C)

    # Shifted 3F2 numerator parameters in the Euler ODE.
    a1, a2, a3 = m - d, A + m, C + m
    e1 = sp.expand(a1 + a2 + a3)
    p2_from_ode = B + m + D + m + 1 - lam * y * (3 + e1)
    p2_displayed = B + D + 2 * m + 1 - lam * y * (A + C + 3 * m - d + 3)
    assert sp.simplify(p2_from_ode - p2_displayed) == 0

    # Independently expand the decomposed coefficient used in the main proof.
    a = 1 - y / A
    b_m_plus_1 = B + m + 1 - y + (d - 1 - 2 * (m + 1)) * y / A
    epsilon = (C - D) / C
    p2_decomposed = (
        b_m_plus_1
        + (D + m) * a
        + epsilon * (y / A) * (A - d + 3 + 3 * m)
    )
    assert sp.simplify(p2_decomposed - p2_displayed) == 0

    stale = B + D + 3 * m + 1 - lam * y * (A + C + 3 * m - d + 3)
    assert sp.simplify(stale - p2_displayed) == m


def check_current_surfaces() -> None:
    main = MAIN.read_text(encoding="utf-8")
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    appendices = APPENDICES.read_text(encoding="utf-8")
    joined = "\n".join((main, supplement, appendices))
    main_words = " ".join(main.split())
    supplement_words = " ".join(supplement.split())
    appendices_words = " ".join(appendices.split())

    assert r"r\ge1-\Re L_s" in main
    assert r"r\ge1-\Re L_N" in supplement
    assert r"r\ge1-\Re L_N" in appendices
    assert "full real Gaussian is used only as a comparison integral" in main_words
    assert "full real Gaussian is only a comparison integral" in supplement_words
    assert "full real Gaussian is not the deformed contour" in appendices_words
    assert r"P_{2,m}&=B+D+2m+1" in supplement
    assert r"P_{2,m}&=B+D+2m+1" in appendices
    assert r"P_{2,m}&=B+D+3m+1" not in joined
    assert r"N_0=\max\{N_{\rm analytic},N_{\rm explicit}\}" in main
    assert r"N_{\rm elementary}" not in joined
    assert "N_0 = max(N_explicit, N_analytic)" in LEDGER.read_text(encoding="utf-8")

    # The repaired rectangle display introduces these symbols without a
    # defining line, and the prose later switches from I_1 back to F_1.
    # Preserve this as a fail-loud validation finding rather than silently
    # treating the reader's inferred definitions as part of the source.
    assert main.count("I_1(s)") == 1 and main.count("F_1(s)") == 1
    assert supplement.count("I_1(N)") == 1 and supplement.count("F_1(N)") == 1
    assert main.count("g_s(") == 3
    assert supplement.count("g_N(") == 3
    assert appendices.count("g_N(") == 3
    assert "g_s(u):=" not in main and "g_N(u):=" not in supplement + appendices


def main() -> None:
    check_contour_geometry()
    check_p2_from_ode()
    check_current_surfaces()
    print("PASS legal contour geometry, exact P2 coefficient, and N_explicit consistency")
    print("FOUND P2 manuscript surfaces do not define I_1/g/Phi or identify I_1 with F_1")


if __name__ == "__main__":
    main()
