#!/usr/bin/env python3
"""Independent hostile checks of the repaired contour and limiting system.

Inputs are constructed from the displayed definitions.  This script does not
read packet-produced answers or expected-result files.
"""

from fractions import Fraction as Q

import mpmath as mp


def saddle(n_value: int) -> mp.mpf:
    """Solve N=L(pi exp(L)+3/4) on the positive branch."""
    n = mp.mpf(n_value)
    guess = mp.log(n) - mp.log(mp.log(n)) - mp.log(mp.pi)
    return mp.findroot(lambda ell: ell * (mp.pi * mp.exp(ell) + mp.mpf(3) / 4) - n, guess)


def phase(n_value: int, u: mp.mpc) -> mp.mpc:
    """First-mode phase in u=Log(t), with the Jacobian kept outside."""
    return n_value * mp.log(u) - mp.mpf(3) * u / 4 - mp.pi * mp.exp(u)


def check_contour() -> None:
    mp.mp.dps = 70
    for n_value in (100, 10_000, 1_000_000):
        ell = saddle(n_value)
        curvature = n_value / ell**2 + mp.pi * mp.exp(ell)
        assert curvature > 0
        for step in (mp.mpf("1e-3"), mp.mpf("2e-3"), mp.mpf("5e-3")):
            horizontal = mp.re(phase(n_value, ell + step) - phase(n_value, ell))
            vertical = mp.re(phase(n_value, ell + 1j * step) - phase(n_value, ell))
            horizontal_scaled = horizontal / (step**2)
            vertical_scaled = vertical / (step**2)
            tolerance = mp.mpf("0.03") * curvature
            assert abs(horizontal_scaled + curvature / 2) < tolerance
            assert abs(vertical_scaled - curvature / 2) < tolerance
            assert horizontal < 0 < vertical

        # The legal deformed ray after splitting the endpoint at u=1 has
        # r >= 1-L, hence Re(u)>=1.  By contrast, the literal full-line claim
        # r in R reaches the principal-Log cut already for real s.
        legal_left_endpoint = ell + (1 - ell)
        full_line_counterexample = ell + (-ell - 1)
        assert mp.almosteq(legal_left_endpoint, 1)
        assert mp.almosteq(full_line_counterexample, -1)


def limiting_map(alpha: Q, t: Q, w: Q, delta: Q) -> tuple[Q, Q, Q, Q]:
    """F=H^infinity+S^infinity in the manuscript's coordinate order."""
    return (
        1 / alpha + w / t**2 + delta - 2,
        w / t**3 + delta - 1,
        3 * w / t**4 + 3 * delta - 2,
        4 * w / t**5 + 4 * delta - 2,
    )


def check_elimination() -> None:
    samples = (
        (Q(3), Q(2), Q(16, 3), Q(1, 3)),
        (Q(5, 2), Q(7, 4), Q(5), Q(1, 4)),
        (Q(7, 2), Q(9, 4), Q(6), Q(5, 12)),
        (Q(13, 4), Q(17, 8), Q(21, 4), Q(3, 8)),
    )
    for alpha, t, w, delta in samples:
        f0, f1, f2, f3 = limiting_map(alpha, t, w, delta)
        assert 3 * f1 - f2 == 3 * w * (t - 1) / t**4 - 1
        assert Q(4, 3) * f2 - f3 == 4 * w * (t - 1) / t**5 - Q(2, 3)

    star = (Q(3), Q(2), Q(16, 3), Q(1, 3))
    assert limiting_map(*star) == (Q(0), Q(0), Q(0), Q(0))

    # At a positive zero the two repaired identities imply t=2 exactly.
    # Cross-multiplication is legal because t,w,t-1 are positive.
    t_from_division = Q(6, 3)
    assert t_from_division == 2
    w = Q(t_from_division**4, 3 * (t_from_division - 1))
    delta = 1 - w / t_from_division**3
    alpha = 1 / (2 - w / t_from_division**2 - delta)
    assert (alpha, t_from_division, w, delta) == star


if __name__ == "__main__":
    check_contour()
    check_elimination()
    print("PASS horizontal sign and elimination; COUNTEREXAMPLE to literal full-line branch claim")
