"""Regression check for Lemma S of C48_SECTORIAL_SADDLE_VARIABLE.md.

Confirms, for the saddle variable L_N defined by  N = L_N (pi e^{L_N} + 3/4):

  (c)  |L_N - L_0| < 1  with  L_0 = log N - log log N - log pi,
       and  |L_N - L_0| = O(log l / l),  l = log|N|;
  (d)  |L_N| / l -> 1, hence |L_N| asymp log|N|;
  (e)  |r| = |1/L_N| <= 7/50 and |sigma| = |L_N/N| <= 7/50 for |N| >= e^12;
  (f)  the exact identity  Q_N = N L_N (1 + r - (3/4) sigma).

It also proves a conservative coefficientwise upper bound for `|H_6|` on the
closed bidisc of radius `7/50`.  A separate boundary grid is reported only as
a non-rigorous conditioning diagnostic; it is not called a supremum.

This file is a REGRESSION CHECK ONLY.  The proof is Sections 2-8 of the note.
"""

from mpmath import mp, mpf, mpc, exp, log, pi, findroot, nstr

mp.dps = 40


def L_of(N):
    """The branch of the saddle variable continued from the positive real axis.

    Solved in the well-scaled logarithmic form
        L + log L + log pi - log N - log(1 - 3L/(4N)) = 0,
    started at the comparison point L_0, which Lemma S places within 1 of L_N.
    """
    w = log(N)
    L0 = w - log(w) - log(pi)
    return findroot(lambda L: L + log(L) + log(pi) - log(N)
                    - log(1 - 3 * L / (4 * N)), L0)


def table():
    print("Lemma S (c)-(f): saddle variable on |arg N| <= theta < pi/2\n")
    print("  |N|       theta   l=log|N|   |L-L0|     (|L-L0|)l/log l   |L|/l"
          "      |r|        |sigma|     Q/(N L) exact")
    for mag in ['1e4', '1e8', '1e16', '1e32', '1e80', '1e200', '1e600']:
        for th in [mpf(0), mpf('0.6'), mpf('1.4')]:      # 1.4 < pi/2
            N = mpf(mag) * exp(mpc(0, 1) * th)
            L = L_of(N)
            w = log(N)
            L0 = w - log(w) - log(pi)
            l = log(abs(N))
            eps = abs(L - L0)
            r, sig = 1 / L, L / N
            Q = (1 + L) * N - mpf(3) / 4 * L ** 2
            # (f) is an identity, so this residual must be at working-precision zero
            ident = abs(Q - N * L * (1 + r - mpf(3) / 4 * sig)) / abs(Q)
            assert eps < 1, (mag, th, eps)                       # (c)
            assert ident < mpf(10) ** (-30), (mag, th, ident)    # (f)
            print("  %-9s %5s  %8s  %9s  %13s  %8s  %9s  %10s  %s"
                  % (mag, nstr(th, 2), nstr(l, 6), nstr(eps, 4),
                     nstr(eps * l / log(l), 5), nstr(abs(L) / l, 6),
                     nstr(abs(r), 5), nstr(abs(sig), 4), nstr(ident, 3)))
        print()

    print("Bidisc condition of Lemma S(e), |r| <= 7/50 and |sigma| <= 7/50,"
          " at theta = 1.4:")
    for mag in ['2e5', '1e6', '1e8', '1e16']:
        N = mpf(mag) * exp(mpc(0, 1) * mpf('1.4'))
        L = L_of(N)
        ok = abs(1 / L) <= mpf(7) / 50 and abs(L / N) <= mpf(7) / 50
        print("   |N|=%-6s |r|=%s  |sigma|=%s  both <= 7/50: %s"
              % (mag, nstr(abs(1 / L), 6), nstr(abs(L / N), 6), ok))
    print("\n  (Lemma S is stated for |N| >= e^12 = %s.)" % nstr(exp(mpf(12)), 8))


def threshold_boundary():
    """Stress the actual left endpoint, including angles near pi/2.

    These checks are numerical regressions, not substitutes for the uniform
    inequalities in Lemma S.  They are useful guards against accidentally
    strengthening one of the endpoint decimals beyond what the proof gives.
    """
    ell = mpf(12)
    print("\nleft-endpoint regression at |N|=e^12:")
    for th in [mpf(0), mpf('0.6'), mpf('1.4'), pi / 2 - mpf('1e-8')]:
        N = exp(ell) * exp(mpc(0, 1) * th)
        L = L_of(N)
        w = log(N)
        L0 = w - log(w) - log(pi)
        r, sig = 1 / L, L / N
        qfactor = 1 + r - mpf(3) * sig / 4
        assert abs(L - L0) < 1
        assert abs(r) <= mpf(7) / 50
        assert abs(sig) < mpf(1) / 7500
        assert abs(qfactor) >= mpf(9) / 16
        print("   theta=%s  |r|=%s  |sigma|=%s  |Q/(NL)|=%s"
              % (nstr(th, 8), nstr(abs(r), 8), nstr(abs(sig), 8),
                 nstr(abs(qfactor), 8)))
    print("left-endpoint regression PASS")


def h6_bidisc_bounds():
    """Rigorous coefficientwise bound and non-rigorous boundary diagnostics."""
    import sympy as sp
    N, L, rs, ss = sp.symbols('N L r sigma')
    Q = (1 + L) * N - sp.Rational(3, 4) * L ** 2
    G0 = (N + 1) * sp.log(L) + L / 4 - N / L - sp.Rational(1, 2) * sp.log(Q)
    D = lambda e: sp.diff(e, N) + (L / Q) * sp.diff(e, L)
    cur = G0
    for _ in range(6):
        cur = sp.cancel(sp.together(D(cur)))
    H6 = sp.cancel(sp.together(cur * N ** 5 * L)).subs({L: 1 / rs, N: 1 / (rs * ss)})
    H6 = sp.cancel(sp.together(sp.simplify(H6)))
    num, den = sp.fraction(H6)
    assert sp.simplify(sp.factor(den) - (4 * rs - 3 * ss + 4) ** 12) == 0, sp.factor(den)
    print("\nreduced denominator of H_6 confirmed: (4 + 4r - 3 sigma)^12")

    # On |r|,|sigma| <= R, bound the numerator by the sum of the absolute
    # coefficient majorants and the denominator by (4 - 7R)^12.  This is an
    # exact rational proof, unlike sampling the distinguished boundary.
    R_exact = sp.Rational(7, 50)
    numerator_bound = sum(
        abs(coeff) * R_exact ** sum(monomial)
        for monomial, coeff in sp.Poly(num, rs, ss).terms()
    )
    denominator_lower = (4 - 7 * R_exact) ** 12
    rigorous_bound = sp.factor(numerator_bound / denominator_lower)
    assert rigorous_bound < 10000
    print("rigorous coefficientwise bound on |r|,|sigma| <= 7/50:")
    print("   numerator <=", numerator_bound)
    print("   denominator >=", denominator_lower)
    print("   |H_6| <=", rigorous_bound, "< 10000")

    f = sp.lambdify((rs, ss), H6, 'mpmath')
    print("sampled boundary maxima (non-rigorous diagnostics only):")
    # Keep this deliberately small: it is a conditioning diagnostic, not a
    # certificate, and should not dominate the verification runtime.
    M = 36
    for R in ['0.15', '0.25', '0.35', '0.5']:
        R = mpf(R)
        best = 0
        for a in range(M):
            for b in range(M):
                v = abs(f(R * exp(mpc(0, 1) * 2 * pi * a / M),
                          R * exp(mpc(0, 1) * 2 * pi * b / M)))
                best = max(best, v)
        print("   R=%-5s  sampled max |H_6| = %s" % (R, nstr(best, 8)))


if __name__ == '__main__':
    table()
    threshold_boundary()
    h6_bidisc_bounds()
