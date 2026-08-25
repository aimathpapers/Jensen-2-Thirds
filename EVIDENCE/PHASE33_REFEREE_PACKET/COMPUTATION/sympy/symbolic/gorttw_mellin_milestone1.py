#!/usr/bin/env python3
"""Exact symbolic regression for C48-GORTTW-SECTOR Milestone 1.

This script verifies normalization and saddle algebra only.  It does not test
or assume the complex-uniform contour estimates required by the theorem.
"""

import sympy as sp


def main() -> None:
    z, w = sp.symbols("z w")
    Lambda = sp.symbols("Lambda")

    # xi(s) = 1/2*s*(s-1)*Lambda(s), with s=1/2+w.
    xi_direct = sp.Rational(1, 2) * (sp.Rational(1, 2) + w) * (
        -sp.Rational(1, 2) + w
    ) * Lambda
    assert sp.simplify(8 * xi_direct - (4 * w**2 - 1) * Lambda) == 0

    s, L, v = sp.symbols("s L v", positive=True)
    pi = sp.pi
    a = sp.exp(L)
    t = sp.symbols("t", positive=True)

    phi = s * sp.log(sp.log(t)) - sp.Rational(3, 4) * sp.log(t) - pi * t
    saddle_relation = {s: L * (pi * a + sp.Rational(3, 4))}

    first_log_derivative = sp.simplify(t * sp.diff(phi, t)).subs(t, a)
    assert sp.simplify(first_log_derivative.subs(saddle_relation)) == 0

    phi_v = phi.subs(t, a * sp.exp(v))
    curvature = sp.simplify(-sp.diff(phi_v, v, 2).subs(v, 0))
    K = s * (1 / L + 1 / L**2) - sp.Rational(3, 4)
    assert sp.simplify((curvature - K).subs(saddle_relation)) == 0

    Q = (1 + L) * s - sp.Rational(3, 4) * L**2
    assert sp.simplify(Q - L**2 * K) == 0

    # log(a * exp(phi(a))) after pi*a=s/L-3/4.
    saddle_log_amplitude = sp.simplify(L + phi.subs(t, a))
    expected_log_amplitude = (
        s * sp.log(L) + L / 4 - s / L + sp.Rational(3, 4)
    )
    assert (
        sp.simplify(
            (saddle_log_amplitude - expected_log_amplitude).subs(
                pi * a, s / L - sp.Rational(3, 4)
            )
        )
        == 0
    )

    # Direct-xi coefficient moment is the GORZ moment divided by eight.
    F_lo, F_hi = sp.symbols("F_lo F_hi")
    binom = sp.binomial(2 * z, 2)
    g_moment = (32 * binom * F_lo - F_hi) / 2 ** (2 * z - 1)
    h_moment = (32 * binom * F_lo - F_hi) / 2 ** (2 * z + 2)
    assert sp.simplify(g_moment / 8 - h_moment) == 0

    print("PASS: factor-eight normalization")
    print("PASS: saddle equation")
    print("PASS: curvature K and Q=L^2 K")
    print("PASS: saddle leading amplitude")
    print("PASS: Milestone 1 exact symbolic regression")


if __name__ == "__main__":
    main()
