#!/usr/bin/env python3
"""Exact algebra regression for the Phase-21 xi-coefficient assembly."""

import sympy as sp


def main() -> None:
    n, m = sp.symbols("n m", positive=True)

    # Exact binomial conversion when n=2m-2.
    assert sp.simplify(32 * sp.binomial(n + 2, 2) - 16 * (n + 2) * (n + 1)) == 0

    # Exact cancellation in the logarithmic derivative of A(s).
    s, ell, kappa, kappa_prime = sp.symbols(
        "s ell kappa kappa_prime", nonzero=True
    )
    ell_prime = 1 / (ell * kappa)
    raw = (
        -kappa_prime / (2 * kappa)
        + sp.log(ell)
        + s * ell_prime / ell
        + ell_prime / 4
        - 1 / ell
        + s * ell_prime / ell**2
    )
    saddle_kappa = s * (1 / ell + 1 / ell**2) - sp.Rational(3, 4)
    reduced = sp.log(ell) + 1 / (ell * kappa) - kappa_prime / (2 * kappa)
    assert sp.simplify((raw - reduced).subs(s, sp.solve(sp.Eq(kappa, saddle_kappa), s)[0])) == 0

    # The elementary Stirling correction has logarithm O(1/n).
    x = sp.symbols("x", positive=True)
    log_r = 2 + sp.log(1 + x) - (1 / x + sp.Rational(3, 2)) * sp.log(1 + 2 * x)
    series = sp.series(log_r, x, 0, 4)
    assert sp.limit(log_r, x, 0, dir="+") == 0
    assert sp.limit(log_r / x, x, 0, dir="+").is_finite

    print("PASS: 32*binom(n+2,2)=16(n+2)(n+1)")
    print("PASS: exact logarithmic-derivative cancellation")
    print(f"PASS: log Stirling correction series {series}")
    print("PASS: Phase 21 xi-coefficient assembly algebra")


if __name__ == "__main__":
    main()
