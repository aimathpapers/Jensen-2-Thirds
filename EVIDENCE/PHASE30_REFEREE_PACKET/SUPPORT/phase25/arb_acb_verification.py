#!/usr/bin/env python3
"""Directed Arb/ACB verification for the Phase-G Jensen campaign.

The script has five deliberately independent numerical paths:

* completed-zeta Taylor series evaluated directly by Arb;
* the positive Riemann ``omega`` kernel with analytic theta/u tail bounds;
* the Phase-21 Mellin ``F`` combination with separate integrals and tails;
* certified complex saddle boxes and contour integrals;
* direct Arb-polynomial root isolation for small Jensen polynomials.

Point grids are regression evidence, not proofs of uniform asymptotics.  The
kernel tails and each recorded Rouche box are genuine continuum enclosures.
Every inequality is accepted only when interval endpoints establish it.
"""

from __future__ import annotations

import argparse
import json
import random
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path

import mpmath as mp
from flint import acb, acb_series, arb, arb_poly, ctx


PRECISION_DPS = 120
THETA_TERMS = 6
INTEGRAL_CUTOFF = 4
SADDLE_GRID = ((200, "0"), (200, "0.01"), (800, "0.01"))


def arb_text(value: arb, digits: int = 36) -> str:
    return value.str(digits, more=True)


def acb_text(value: acb, digits: int = 30) -> str:
    return f"{arb_text(value.real, digits)} + I*({arb_text(value.imag, digits)})"


def widen(value: arb, error: arb) -> arb:
    """Add a proved nonnegative absolute error to an Arb enclosure."""

    if not error >= 0:
        raise AssertionError("tail error was not proved nonnegative")
    return arb(value.mid(), value.rad() + error.upper())


def direct_xi_coefficients(max_n: int, precision: int = PRECISION_DPS) -> list[arb]:
    """Return gamma(n) from xi(1/2+w), directly via completed zeta."""

    ctx.dps = precision
    ctx.cap = 2 * max_n + 3
    w = acb_series([acb("0.5"), acb(1)])
    pi_series = acb_series([arb.pi()])
    completed = pi_series ** (-w / 2) * (w / 2).gamma() * w.zeta()
    xi = w * (w - 1) * completed / 2
    values = [xi[2 * n].real * factorial(n) for n in range(max_n + 1)]
    if not all(value > 0 for value in values):
        raise AssertionError("direct xi series did not prove coefficient positivity")
    return values


def omega_integrand(u: acb, k: int) -> acb:
    """The k-th term of e^(u/2) omega(e^(2u))."""

    pi = arb.pi()
    t = (2 * u).exp()
    # Theta=sum_{k>=1} exp(-pi k^2 t), so the one-half in omega is essential.
    omega = (pi**2 * k**4 * t**2 - arb(3) / 2 * pi * k**2 * t)
    return omega * (-pi * k**2 * t).exp() * (u / 2).exp()


def mellin_f_integrand(u: acb, k: int, order: int) -> acb:
    """The k-th term of F(order) after t=exp(2u)."""

    t = (2 * u).exp()
    return (
        arb(2) ** (order + 1)
        * u**order
        * (u / 2).exp()
        * (-arb.pi() * k**2 * t).exp()
    )


def exponential_tail_bound(
    order: int,
    k_max: int,
    cutoff: int,
    exponent_linear: arb,
    k_power: int,
    prefactor: arb,
) -> arb:
    """Bound omitted k and u tails for a positive theta-type integrand.

    Uses exp(2u)>=1+2u for the k tail.  For u=U+v it uses
    exp(2v)>=1+2v, then integrates the resulting polynomial times an
    exponential exactly.  The geometric k-tail ratio is intentionally loose.
    """

    pi = arb.pi()
    first_k = k_max + 1
    decay = 2 * pi * first_k**2 - exponent_linear
    first = (
        prefactor
        * first_k**k_power
        * (-pi * first_k**2).exp()
        * factorial(order)
        / decay ** (order + 1)
    )
    ratio = 16 * (-pi * (2 * k_max + 3)).exp()
    if not ratio < 1:
        raise AssertionError("theta k-tail ratio did not contract")
    k_tail = first / (1 - ratio)

    U = arb(cutoff)
    exp_two_u = (2 * U).exp()
    u_tail = arb(0)
    for k in range(1, k_max + 1):
        local_decay = 2 * pi * k**2 * exp_two_u - exponent_linear
        polynomial_integral = sum(
            (
                arb(comb(order, j))
                * U ** (order - j)
                * factorial(j)
                / local_decay ** (j + 1)
            )
            for j in range(order + 1)
        )
        u_tail += (
            prefactor
            * k**k_power
            * (exponent_linear * U - pi * k**2 * exp_two_u).exp()
            * polynomial_integral
        )
    total = k_tail + u_tail
    if not total > 0:
        raise AssertionError("analytic tail bound was not strictly positive")
    return total


def rigorous_integral(function, order: int) -> arb:
    result = acb.integral(
        lambda u, analytic: sum(
            (function(u, k, order) for k in range(1, THETA_TERMS + 1)),
            acb(0),
        ),
        0,
        INTEGRAL_CUTOFF,
        rel_tol=arb("1e-70"),
        abs_tol=arb("1e-70"),
        eval_limit=100_000,
    )
    if not result.imag.contains(0):
        raise AssertionError("real-axis integral failed to enclose a real value")
    return result.real


def coefficient_normalization_checks() -> dict[str, object]:
    ctx.dps = 90
    direct = direct_xi_coefficients(3, 90)
    rows: list[dict[str, object]] = []
    for n in range(4):
        finite = rigorous_integral(
            lambda u, k, order: omega_integrand(u, k) * u**order,
            2 * n,
        )
        tail = exponential_tail_bound(
            2 * n,
            THETA_TERMS,
            INTEGRAL_CUTOFF,
            arb("4.5"),
            4,
            arb.pi() ** 2,
        )
        kernel_gamma = widen(finite, tail) * 8 * factorial(n) / factorial(2 * n)
        if not kernel_gamma.overlaps(direct[n]):
            raise AssertionError(f"omega/direct coefficient mismatch at n={n}")

        row: dict[str, object] = {
            "n": n,
            "direct_completed_zeta": arb_text(direct[n]),
            "omega_kernel": arb_text(kernel_gamma),
            "omega_absolute_tail_bound": arb_text(tail),
            "direct_omega_overlap": True,
        }
        if n >= 1:
            f_values: list[arb] = []
            for order in (2 * n - 2, 2 * n):
                finite_f = rigorous_integral(mellin_f_integrand, order)
                tail_f = exponential_tail_bound(
                    order,
                    THETA_TERMS,
                    INTEGRAL_CUTOFF,
                    arb("0.5"),
                    0,
                    arb(2) ** (order + 1),
                )
                f_values.append(widen(finite_f, tail_f))
            moment = arb(2) ** (-2 * n - 2) * (
                32 * comb(2 * n, 2) * f_values[0] - f_values[1]
            )
            mellin_gamma = arb(factorial(n)) / factorial(2 * n) * moment
            if not mellin_gamma.overlaps(direct[n]):
                raise AssertionError(f"Mellin/direct coefficient mismatch at n={n}")
            row["mellin_F_combination"] = arb_text(mellin_gamma)
            row["direct_mellin_overlap"] = True
        rows.append(row)
    return {
        "status": "PASS",
        "orders": [0, 1, 2, 3],
        "theta_terms_integrated": THETA_TERMS,
        "u_cutoff": INTEGRAL_CUTOFF,
        "rows": rows,
        "coverage": (
            "The omitted theta and infinite-u tails are bounded analytically "
            "over their complete ranges, not sampled."
        ),
    }


def mp_saddle(radius: int | str, angle: str) -> mp.mpc:
    """Untrusted high-precision seed; every use is validated by Arb."""

    mp.mp.dps = 140
    s = mp.mpf(radius) * mp.exp(1j * mp.mpf(angle))
    guess = mp.log(s) - mp.log(mp.log(s)) - mp.log(mp.pi)
    return mp.findroot(
        lambda ell: ell * (mp.pi * mp.exp(ell) + mp.mpf(3) / 4) - s,
        guess,
    )


def saddle_point(radius: int, angle: str) -> tuple[acb, acb]:
    seed = mp_saddle(radius, angle)
    ell = acb(str(mp.re(seed)), str(mp.im(seed)))
    s = acb(radius) * acb(0, angle).exp()
    return s, ell


def saddle_box_certificate(radius: int, angle: str) -> dict[str, object]:
    """Uniform Rouche certificate for every s in a small rectangular ball."""

    ctx.dps = 90
    pi = arb.pi()
    s_center, ell = saddle_point(radius, angle)
    parameter_padding = arb("1e-40")
    s_box = acb(
        arb(s_center.real.mid(), s_center.real.rad() + parameter_padding),
        arb(s_center.imag.mid(), s_center.imag.rad() + parameter_padding),
    )
    root_radius = arb("1e-32")
    disc_radius = root_radius * arb(2).sqrt()

    def equation(value: acb) -> acb:
        return value * (pi * value.exp() + arb(3) / 4) - s_box

    derivative_center = pi * ell.exp() * (ell + 1) + arb(3) / 4
    second_derivative_bound = (
        pi
        * (ell.real + disc_radius).exp()
        * ((ell + 2).abs_upper() + disc_radius)
    )
    lhs = equation(ell).abs_upper() + second_derivative_bound * disc_radius**2 / 2
    rhs = derivative_center.abs_lower() * disc_radius
    if not lhs < rhs:
        raise AssertionError("Rouche saddle inclusion failed")
    if not second_derivative_bound * disc_radius < derivative_center.abs_lower():
        raise AssertionError("saddle derivative could vanish in root disc")

    ell_box = acb(
        arb(ell.real.mid(), ell.real.rad() + disc_radius),
        arb(ell.imag.mid(), ell.imag.rad() + disc_radius),
    )
    q_value = (1 + ell_box) * s_box - arb(3) / 4 * ell_box**2
    if not q_value.abs_lower() > 0:
        raise AssertionError("Q failed to exclude zero on saddle box")
    if not ell_box.real.lower() > 1:
        raise AssertionError("saddle real-part margin failed")
    if not ell_box.imag.abs_upper() < arb("0.02"):
        raise AssertionError("saddle imaginary-part box exceeded theorem grid margin")
    return {
        "radius": radius,
        "angle": angle,
        "s_parameter_box": acb_text(s_box),
        "root_center": acb_text(ell),
        "root_disc_radius": arb_text(disc_radius),
        "rouche_lhs": arb_text(lhs),
        "rouche_rhs": arb_text(rhs),
        "Q_abs_lower": arb_text(q_value.abs_lower()),
        "unique_root_and_nonzero_derivative": True,
    }


def contour_check(radius: int, angle: str) -> dict[str, object]:
    ctx.dps = 70
    pi = arb.pi()
    s, seed_ell = saddle_point(radius, angle)
    # The preceding Rouché calculation places the exact saddle inside this
    # coordinate box.  Carry that uncertainty through the contour values.
    root_coordinate_radius = arb("2e-32")
    ell = acb(
        arb(seed_ell.real.mid(), seed_ell.real.rad() + root_coordinate_radius),
        arb(seed_ell.imag.mid(), seed_ell.imag.rad() + root_coordinate_radius),
    )
    alpha = ell.real
    beta = ell.imag

    def phase(value: acb, analytic: bool = False, mode: int = 1) -> acb:
        return (
            s * value.log(analytic=analytic)
            + value / 4
            - pi * mode**2 * value.exp()
        )

    center = phase(ell)

    def horizontal(left: arb | int, right: arb | int, mode: int = 1) -> acb:
        return acb.integral(
            lambda value, analytic: (phase(value, analytic, mode) - center).exp(),
            acb(left, beta),
            acb(right, beta),
            rel_tol=arb("1e-45"),
            abs_tol=arb("1e-45"),
            eval_limit=100_000,
        )

    whole = horizontal(1, alpha + 6)
    central = horizontal(alpha - 1, alpha + 1)
    kappa = s * (1 / ell + 1 / ell**2) - arb(3) / 4
    gaussian = (2 * pi / kappa).sqrt()
    ratio = whole / gaussian
    error = (ratio - 1).abs_upper()
    error_gate = arb("0.003") if radius == 200 else arb("0.001")
    if not error < error_gate:
        raise AssertionError("certified contour ratio exceeded regression gate")
    if not (central / whole - 1).abs_upper() < arb("1e-15"):
        raise AssertionError("central-window localization gate failed")

    connector = acb.integral(
        lambda value, analytic: (phase(value, analytic) - center).exp(),
        acb(1),
        acb(1, beta),
        rel_tol=arb("1e-45"),
        abs_tol=arb("1e-45"),
        eval_limit=100_000,
    )
    connector_relative = (connector / gaussian).abs_upper()
    if not connector_relative < arb("1e-35"):
        raise AssertionError("endpoint connector was not negligible")

    modes: dict[str, str] = {}
    for mode in (2, 3):
        relative = (horizontal(1, alpha + 6, mode) / gaussian).abs_upper()
        if not relative < arb("1e-25"):
            raise AssertionError(f"theta mode {mode} suppression failed")
        modes[str(mode)] = arb_text(relative)
    return {
        "radius": radius,
        "angle": angle,
        "main_to_gaussian_ratio": acb_text(ratio),
        "absolute_ratio_error_upper": arb_text(error),
        "central_window_relative_error_upper": arb_text(
            (central / whole - 1).abs_upper()
        ),
        "connector_relative_upper": arb_text(connector_relative),
        "higher_mode_relative_uppers": modes,
        "scope": "Certified values at this grid point; not a uniform sector proof.",
    }


def derivative_tower_check() -> dict[str, object]:
    """ACB implicit power-series check independent of symbolic differentiation."""

    ctx.dps = PRECISION_DPS
    ctx.cap = 8
    pi = arb.pi()
    x_zero = 10**12
    n_zero = 2 * x_zero - 2
    seed = mp_saddle(n_zero, "0")
    x = acb_series([acb(x_zero), acb(1)])
    n_var = 2 * x - 2
    ell = acb_series([acb(str(mp.re(seed)))])
    pi_series = acb_series([pi])
    for _ in range(5):
        equation = ell * (pi_series * ell.exp() + arb(3) / 4) - n_var
        derivative = pi_series * ell.exp() * (ell + 1) + arb(3) / 4
        ell -= equation / derivative
    residual = ell * (pi_series * ell.exp() + arb(3) / 4) - n_var
    if not all(residual[k].abs_upper() < arb("1e-80") for k in range(7)):
        raise AssertionError("implicit ACB series did not close")

    q_var = (1 + ell) * n_var - arb(3) / 4 * ell**2
    main = (n_var + 1) * ell.log() + ell / 4 - n_var / ell - q_var.log() / 2
    expected = {2: 2, 3: -2, 4: 4, 5: -12, 6: 48}
    rows: list[dict[str, object]] = []
    for order, target in expected.items():
        derivative = main[order] * factorial(order)
        normalized = derivative * arb(x_zero) ** (order - 1) * ell[0]
        relative = ((normalized - target) / target).abs_upper()
        if not relative < arb("0.05"):
            raise AssertionError(f"ACB derivative-tower gate failed at order {order}")
        rows.append(
            {
                "order": order,
                "normalized_enclosure": arb_text(normalized.real),
                "expected_asymptotic_constant": target,
                "relative_difference_upper": arb_text(relative),
            }
        )
    return {
        "status": "PASS",
        "x": x_zero,
        "method": "ACB implicit local power series; no symbolic derivative formulas",
        "rows": rows,
        "scope": "Finite-x enclosure corroborating, not proving, the asymptotic limit.",
    }


def jensen_root_checks() -> dict[str, object]:
    ctx.dps = 200
    examples = ((5, 3), (10, 4), (20, 5))
    max_index = max(n + d for n, d in examples)
    coefficients = direct_xi_coefficients(max_index, 200)
    rows: list[dict[str, object]] = []
    for n, degree in examples:
        polynomial_coefficients = [
            arb(comb(degree, j)) * coefficients[n + j] for j in range(degree + 1)
        ]
        scale = polynomial_coefficients[-1].mid()
        polynomial = arb_poly([value / scale for value in polynomial_coefficients])
        roots = polynomial.complex_roots()
        if len(roots) != degree:
            raise AssertionError("Arb did not isolate every Jensen root")
        if not all(root.real.upper() < 0 and root.imag.contains(0) for root in roots):
            raise AssertionError("Jensen root box failed negative-real test")
        for i, root in enumerate(roots):
            for earlier in roots[:i]:
                if root.overlaps(earlier):
                    raise AssertionError("Jensen root boxes were not separated")
        rows.append(
            {
                "n": n,
                "d": degree,
                "isolated_pairwise_disjoint_negative_root_boxes": [
                    acb_text(root, 18) for root in roots
                ],
            }
        )
    return {
        "status": "PASS",
        "rows": rows,
        "scope": "Finite examples only; these do not imply the asymptotic wedge.",
    }


def exact_recurrence_trials() -> dict[str, object]:
    """Extra exact coefficient-ratio checks with deterministic fresh tuples."""

    generator = random.Random(0xC48)
    checks = 0
    for _ in range(64):
        degree = generator.randint(3, 18)
        shift = generator.randint(0, degree - 1)
        aa = generator.randint(2, 30)
        bb = generator.randint(2, 30)
        cc = generator.randint(2, 30)
        dd = generator.randint(2, 30)
        lam = Q(dd, aa * cc)

        def pochhammer(value: int, order: int) -> int:
            result = 1
            for index in range(order):
                result *= value + index
            return result

        def coefficient(order: int) -> Q:
            return (
                Q(pochhammer(shift - degree, order))
                * pochhammer(aa + shift, order)
                * pochhammer(cc + shift, order)
                * lam**order
                / (
                    pochhammer(bb + shift, order)
                    * pochhammer(dd + shift, order)
                    * factorial(order)
                )
            )

        for order in range(degree - shift):
            left = coefficient(order + 1) * (
                aa
                * cc
                * (order + 1)
                * (bb + order + shift)
                * (dd + order + shift)
            )
            right = coefficient(order) * (
                dd
                * (order + shift - degree)
                * (aa + order + shift)
                * (cc + order + shift)
            )
            if left != right:
                raise AssertionError("fresh exact recurrence trial failed")
            checks += 1
    return {
        "status": "PASS",
        "seed": "0xC48",
        "tuples": 64,
        "cross_multiplied_exact_identities": checks,
        "arithmetic": "fractions.Fraction",
    }


def build_report() -> dict[str, object]:
    ctx.threads = 1
    report = {
        "status": "PASS",
        "python_flint_version": __import__("flint").__version__,
        "precision_decimal_digits": PRECISION_DPS,
        "coefficient_normalizations": coefficient_normalization_checks(),
        "saddle_box_certificates": [
            saddle_box_certificate(radius, angle) for radius, angle in SADDLE_GRID
        ],
        "contour_grid": [
            contour_check(radius, angle) for radius, angle in SADDLE_GRID
        ],
        "derivative_tower": derivative_tower_check(),
        "finite_jensen_roots": jensen_root_checks(),
        "fresh_exact_recurrence": exact_recurrence_trials(),
        "trust_boundary": (
            "Arb/ACB directed enclosures and explicit analytic tails prove the "
            "individual recorded inequalities. Finite contour/root grids are "
            "regression evidence and do not prove uniform sectorial asymptotics "
            "or the two-thirds theorem. No human or peer review is claimed."
        ),
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(build_report(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
