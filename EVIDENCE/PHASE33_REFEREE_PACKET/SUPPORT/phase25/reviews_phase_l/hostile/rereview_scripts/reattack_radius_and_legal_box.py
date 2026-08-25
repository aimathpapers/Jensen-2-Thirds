#!/usr/bin/env python3
"""Independent legal-parameter attack on the repaired radius mechanism.

The script builds parameters and terminating hypergeometric coefficients from
their definitions.  It reads no frozen expected values.
"""

import math

import mpmath as mp


def saddle(n_value: int) -> mp.mpf:
    target = mp.mpf(2 * n_value - 2)
    guess = mp.log(target) - mp.log(mp.log(target)) - mp.log(mp.pi)
    return mp.findroot(
        lambda ell: ell * (mp.pi * mp.exp(ell) + mp.mpf(3) / 4) - target,
        guess,
    )


def parameters(n_value: int) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    ell = saddle(n_value)
    e = 1 / ell
    alpha, t, w, delta = mp.mpf(3), mp.mpf(2), mp.mpf(16) / 3, mp.mpf(1) / 3
    a = alpha * n_value / e
    b = (t + w * e) * n_value
    c = t * n_value
    d_parameter = (1 + delta * e) * n_value
    return ell, a, b, c, d_parameter


def p_coefficients(
    degree: int, a: mp.mpf, b: mp.mpf, c: mp.mpf, d_parameter: mp.mpf
) -> list[mp.mpf]:
    """Ascending coefficients of 3F2(-d,A,C;B,D;(D/AC)y)."""
    coefficients = [mp.mpf(1)]
    for k in range(degree):
        ratio = (
            d_parameter
            * (k - degree)
            * (k + a)
            * (k + c)
            / (a * c * (k + 1) * (k + b) * (k + d_parameter))
        )
        coefficients.append(coefficients[-1] * ratio)
    assert len(coefficients) == degree + 1
    return coefficients


def recurrence_coefficients(
    m: int,
    degree: int,
    y0: mp.mpf,
    a_parameter: mp.mpf,
    b_parameter: mp.mpf,
    c_parameter: mp.mpf,
    d_parameter: mp.mpf,
) -> tuple[mp.mpf, mp.mpf, mp.mpf, mp.mpf]:
    a = 1 - y0 / a_parameter
    b_m = b_parameter + m - y0 + (degree - 1 - 2 * m) * y0 / a_parameter
    c_m = (degree - m) * (1 + m / a_parameter) * y0
    epsilon = (c_parameter - d_parameter) / c_parameter
    beta = (
        a_parameter * (2 * m + 1 - degree)
        - degree * (2 * m + 1)
        + 3 * m**2
        + 3 * m
        + 1
    )
    gamma = m * (m - degree) * (m + a_parameter)
    p3 = a + epsilon * y0 / a_parameter
    p2 = (
        b_parameter
        + m
        + 1
        - y0
        + (degree - 1 - 2 * (m + 1)) * y0 / a_parameter
        + (d_parameter + m) * a
        + epsilon * (y0 / a_parameter) * (a_parameter - degree + 3 + 3 * m)
    )
    p1 = (
        (degree - m - 1) * (1 + (m + 1) / a_parameter) * y0
        + (d_parameter + m) * b_m
        + epsilon * (y0 / a_parameter) * beta
    )
    p0 = (d_parameter + m) * c_m + epsilon * (y0 / a_parameter) * gamma
    p0_closed = (
        d_parameter
        * y0
        * (a_parameter + m)
        * (c_parameter + m)
        * (degree - m)
        / (a_parameter * c_parameter)
    )
    assert mp.almosteq(p0, p0_closed, rel_eps=mp.mpf("1e-60"))
    return p3, p2, p1, p0


def derivative_value(coefficients: list[mp.mpf], order: int, y0: mp.mpf) -> mp.mpf:
    total = mp.mpf(0)
    for exponent in range(order, len(coefficients)):
        falling = math.factorial(exponent) // math.factorial(exponent - order)
        total += coefficients[exponent] * falling * y0 ** (exponent - order)
    return total


def main() -> None:
    # p_F(B) is very small for this legal large-n example, so extra precision
    # is needed before testing cancellation in the exact recurrence.
    mp.mp.dps = 160
    n_value = 10**12
    degree = 8
    ell, a_parameter, b_parameter, c_parameter, d_parameter = parameters(n_value)
    e = 1 / ell

    # Direct legal-box and ordering attack at the limiting branch point.
    assert 0 < e < mp.mpf(1) / 12
    assert a_parameter > b_parameter > c_parameter > d_parameter > 0

    radius = 4096 * mp.sqrt(b_parameter * degree)
    localization = 32 * mp.sqrt(b_parameter * degree)
    worst_budget = mp.mpf(0)
    for y0 in (b_parameter - localization, b_parameter, b_parameter + localization):
        assert y0 > 0
        for m in range(degree - 1):
            p3, p2, p1, p0 = recurrence_coefficients(
                m,
                degree,
                y0,
                a_parameter,
                b_parameter,
                c_parameter,
                d_parameter,
            )
            assert p2 > 0
            # This is exactly the normalized global-maximum neighbor budget.
            budget = abs(p3) * radius / p2 + abs(p1) / (p2 * radius) + abs(p0) / (
                p2 * radius**2
            )
            worst_budget = max(worst_budget, budget)
    assert worst_budget < 1

    # Independently construct the terminating producer and check its recurrence
    # at arbitrary legal y0.  The k=d higher neighbor vanishes by degree.
    coefficients = p_coefficients(
        degree, a_parameter, b_parameter, c_parameter, d_parameter
    )
    y0 = b_parameter
    p_at_y0 = derivative_value(coefficients, 0, y0)
    assert p_at_y0 != 0
    t_values = [
        y0**k * derivative_value(coefficients, k, y0) / p_at_y0
        for k in range(degree + 2)
    ]
    assert t_values[degree + 1] == 0
    for m in range(degree - 1):
        p3, p2, p1, p0 = recurrence_coefficients(
            m,
            degree,
            y0,
            a_parameter,
            b_parameter,
            c_parameter,
            d_parameter,
        )
        residual = p3 * t_values[m + 3] + p2 * t_values[m + 2] + p1 * t_values[m + 1] + p0 * t_values[m]
        scale = max(1, *(abs(term) for term in (
            p3 * t_values[m + 3],
            p2 * t_values[m + 2],
            p1 * t_values[m + 1],
            p0 * t_values[m],
        )))
        assert abs(residual) < mp.mpf("1e-90") * scale

    print(f"PASS legal box, termination, recurrence, and global-neighbor budget={mp.nstr(worst_budget, 12)}")


if __name__ == "__main__":
    main()
