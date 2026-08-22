#!/usr/bin/env python3
"""Independent regressions for load-bearing displayed manuscript equations.

These numerical checks are not proof. They are transcription oracles: the
factor-eight identity is compared with the completed zeta function itself,
and the radius display is checked structurally and on a fixed comparison
polynomial. Neither check reads a frozen result JSON.
"""

from __future__ import annotations

import math
from pathlib import Path

import mpmath as mp


ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = ROOT / "ground_zero_work/phase24/manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex"


def check_displayed_sources() -> None:
    source = MANUSCRIPT.read_text(encoding="utf-8")
    required = (
        r"\gamma(n)=\frac{8\,n!}{(2n)!}",
        r"\omega(e^{2u})e^{u/2}u^{2n}",
        r"\max_{1\le k\le d}",
        r"\left|\frac{y^kp_F^{(k)}(y)}{p_F(y)}\right|^{1/k}",
        r"\begin{lemma}[Finite multiplier stability]",
        r"\sup_{z\in\Omega}|E_F(z)|",
        r"\ll\frac{d^3}{n^2\log(n+2)}\le\frac{C'}K",
    )
    for needle in required:
        if needle not in source:
            raise AssertionError(f"missing corrected manuscript display: {needle}")
    forbidden = (
        r"\frac{8\,2^{2n}}{(2n)!}",
        r"\omega(e^{2u})e^u u^{2n}",
        r"\frac{p_F^{(k)}(y)}{k!p_F(y)}",
        r"\max_{0\le k\le d}",
    )
    for needle in forbidden:
        if needle in source:
            raise AssertionError(f"stale false manuscript display: {needle}")


def omega(t: mp.mpf) -> mp.mpf:
    d_theta = mp.nsum(
        lambda m: -mp.pi * m**2 * mp.exp(-mp.pi * m**2 * t),
        [1, mp.inf],
    )
    d2_theta = mp.nsum(
        lambda m: (mp.pi * m**2) ** 2 * mp.exp(-mp.pi * m**2 * t),
        [1, mp.inf],
    )
    return (2 * t**2 * d2_theta + 3 * t * d_theta) / 2


def xi_centered(z: mp.mpc) -> mp.mpc:
    s = mp.mpf("0.5") + z
    return mp.mpf("0.5") * s * (s - 1) * mp.pi ** (-s / 2) * mp.gamma(
        s / 2
    ) * mp.zeta(s)


def check_factor_eight() -> None:
    mp.mp.dps = 42
    n_max = 4
    coefficients = mp.taylor(
        xi_centered,
        0,
        2 * n_max,
        method="quad",
        radius=mp.mpf("0.5"),
    )
    gamma_true = [
        coefficients[2 * n] * mp.factorial(n) for n in range(n_max + 1)
    ]
    nodes = [
        0,
        mp.mpf(1) / 8,
        mp.mpf(1) / 4,
        mp.mpf(1) / 2,
        1,
        2,
        3,
        5,
        8,
        12,
    ]
    errors = []
    for n, expected in enumerate(gamma_true):
        integral = mp.quad(
            lambda u: omega(mp.exp(2 * u)) * mp.exp(u / 2) * u ** (2 * n),
            nodes,
        )
        actual = 8 * mp.factorial(n) / mp.factorial(2 * n) * integral
        errors.append(abs(actual / expected - 1))
    if max(errors) >= mp.mpf("1e-28"):
        raise AssertionError(
            f"factor-eight equation regression failed: max relative error {max(errors)}"
        )
    print(
        "PASS manuscript factor-eight equation regression "
        f"(n=0..{n_max}, max relative error {mp.nstr(max(errors), 5)})"
    )


def check_radius_scale() -> None:
    mp.mp.dps = 60
    a = mp.mpf("103773.4")
    b = mp.mpf("9370.0")
    c = mp.mpf("6664.7")
    d_parameter = mp.mpf("4309.6")
    degree = 16
    scale = d_parameter / (a * c)

    coefficients = [mp.mpf(1)]
    for j in range(degree):
        coefficients.append(
            coefficients[-1]
            * (j - degree)
            * (a + j)
            * (c + j)
            / ((b + j) * (d_parameter + j) * (j + 1))
            * scale
        )

    def polynomial(y: mp.mpf) -> mp.mpf:
        return sum(coefficients[j] * y**j for j in range(degree + 1))

    def derivative(order: int, y: mp.mpf) -> mp.mpf:
        return sum(
            coefficients[j]
            * mp.factorial(j)
            / mp.factorial(j - order)
            * y ** (j - order)
            for j in range(order, degree + 1)
        )

    roots = sorted(
        mp.re(root)
        for root in mp.polyroots(
            [coefficients[degree - j] for j in range(degree + 1)],
            maxsteps=200,
            extraprec=200,
        )
    )
    if not all(root > 0 for root in roots):
        raise AssertionError("radius regression polynomial lost positive roots")
    critical_points = [
        mp.findroot(
            lambda y: derivative(1, y),
            (roots[j] + roots[j + 1]) / 2,
        )
        for j in range(degree - 1)
    ]
    correct = mp.mpf(0)
    stale = mp.mpf(0)
    for y in critical_points:
        value = polynomial(y)
        correct = max(
            correct,
            max(
                abs(y**k * derivative(k, y) / value) ** (mp.mpf(1) / k)
                for k in range(1, degree + 1)
            ),
        )
        stale = max(
            stale,
            max(
                abs(derivative(k, y) / (mp.factorial(k) * value))
                ** (mp.mpf(1) / k)
                for k in range(1, degree + 1)
            ),
        )
    root_scale = mp.sqrt(b * degree)
    if not correct / root_scale < 1 or not correct / stale > 10_000:
        raise AssertionError("critical-point radius scale regression failed")
    if not math.isclose(float(root_scale), 387.195, rel_tol=2e-6):
        raise AssertionError("fixed radius regression fixture changed")
    print(
        "PASS manuscript critical-point radius regression "
        f"(correct K_r={mp.nstr(correct / root_scale, 6)}, "
        f"stale-scale ratio={mp.nstr(correct / stale, 6)})"
    )


def main() -> None:
    if mp.__version__ != "1.3.0":
        raise AssertionError(f"expected mpmath 1.3.0, found {mp.__version__}")
    check_displayed_sources()
    check_factor_eight()
    check_radius_scale()
    print("PASS all Phase-24 manuscript equation regressions")


if __name__ == "__main__":
    main()
