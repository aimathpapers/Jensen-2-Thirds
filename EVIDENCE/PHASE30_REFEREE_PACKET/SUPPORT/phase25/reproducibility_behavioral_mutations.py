#!/usr/bin/env python3
"""Behavioral mutations for release-critical mathematical interfaces.

Each case changes a mathematical object and requires a derived invariant to
fail. These are deliberately not source-string replacement tests.
"""

from __future__ import annotations

from fractions import Fraction as Q
from math import factorial, isclose


def rejected(name: str, invariant: bool) -> None:
    if invariant:
        raise AssertionError(f"behavioral mutation survived: {name}")
    print(f"PASS behavioral mutation rejected: {name}")


def recurrence_residual(
    k: int, m: int, d: int, a: Q, b: Q, c: Q, dp: Q, ck: Q, ck1: Q
) -> Q:
    return (
        a * c * (k + 1) * (k + b + m) * (k + dp + m) * ck1
        - dp * (k + m - d) * (k + a + m) * (k + c + m) * ck
    )


def main() -> None:
    # Inner sector must be strictly contained in the outer sector.
    theta_inner = Q(1, 400)
    theta_outer_mutated = Q(1, 500)
    rejected("sector nesting", theta_inner < theta_outer_mutated)

    # The six-simplex mass is the product of the six FTC weights.
    simplex_mass = Q(1)
    for denominator in range(2, 7):
        simplex_mass /= denominator
    rejected("simplex mass 1/120", simplex_mass == Q(1, 120))

    # The corrected xi coefficient multiplier is n!, not 2^(2n).
    n = 3
    correct_multiplier = Q(8 * factorial(n), factorial(2 * n))
    mutated_multiplier = Q(8 * 2 ** (2 * n), factorial(2 * n))
    rejected("factor-eight factorial", mutated_multiplier == correct_multiplier)

    # Exact positive branch point and coordinate order.
    alpha, t, w, delta = Q(3), Q(2), Q(16, 3), Q(1, 3)
    mutated = (t, alpha, w, delta)
    equations = (
        Q(1, mutated[0]) + mutated[2] / mutated[1] ** 2 + mutated[3] == 2,
        mutated[2] / mutated[1] ** 3 + mutated[3] == 1,
        3 * mutated[2] / mutated[1] ** 4 + 3 * mutated[3] == 2,
        4 * mutated[2] / mutated[1] ** 5 + 4 * mutated[3] == 2,
    )
    rejected("branch coordinate permutation", all(equations))

    # A center residual is not a whole-box derivative certificate.
    center_derivative = Q(0)
    edge_derivative = Q(3, 4)
    rejected(
        "center-only contraction certificate",
        max(center_derivative, edge_derivative) <= Q(1, 2),
    )

    # The recurrence sign is checked on a genuine adjacent coefficient pair.
    d = 5
    m = 2
    k = 1
    a, b, c, dp = Q(12), Q(9), Q(7), Q(3)
    ck = Q(1)
    ck1 = (
        dp * (k + m - d) * (k + a + m) * (k + c + m) * ck
        / (a * c * (k + 1) * (k + b + m) * (k + dp + m))
    )
    mutated_ck1 = -ck1
    rejected(
        "hypergeometric recurrence sign",
        recurrence_residual(k, m, d, a, b, c, dp, ck, mutated_ck1) == 0,
    )

    # Squaring the positive-endpoint condition gives the exact threshold
    # K_pre > 8^2. The stale value 32 fails it.
    k_pre_mutated = Q(32)
    rejected("Jacobi squared threshold", k_pre_mutated > 64)

    # The wedge is created by six localization factors, not five.
    localization_degree = 5
    rejected("fifth-for-sixth wedge exponent", localization_degree == 6)

    # A purported review claim must remain qualified by an explicit negation.
    mutated_review = "This work has peer review."
    qualified = "not peer review" in mutated_review.lower()
    rejected("review overclaim", qualified)

    # Enlarging the inner box past the exact outer alpha margin must fail.
    alpha_center = Q(3)
    mutated_radius = Q(3, 4)
    outer_low, outer_high = Q(5, 2), Q(7, 2)
    rejected(
        "branch interval endpoint",
        outer_low <= alpha_center - mutated_radius
        and alpha_center + mutated_radius <= outer_high,
    )

    # The saddle has Phi''(L)=-K.  A real horizontal displacement is
    # Gaussian descent, whereas the stale imaginary displacement is ascent.
    kappa = Q(17)
    horizontal_quadratic = -kappa * Q(1, 100) ** 2 / 2
    vertical_quadratic = -kappa * (Q(0, 1) + 1j * 0.01) ** 2 / 2
    rejected(
        "vertical contour Gaussian sign",
        isclose(vertical_quadratic.real, float(horizontal_quadratic)),
    )

    # Defining h=log(gamma) and also retaining the explicit half-shift
    # polygamma term double-counts it.  At order six the missing correction
    # is nonzero already in the one-term positive polygamma series.
    n_shift = Q(9, 2)
    psi5_first_term = Q(120) / n_shift**6
    rejected("log-gamma versus log-M bridge", psi5_first_term == 0)

    # The stale elimination identity is not a polynomial identity.  This
    # legal positive point falsifies it, while the two corrected residual
    # combinations are identities and are source-checked separately.
    alpha, t, w, delta = Q(3), Q(2), Q(5), Q(1, 4)
    f2 = w / t**3 + delta - 1
    f3 = 3 * w / t**4 + 3 * delta - 2
    rejected(
        "stale limiting-system elimination",
        3 * t * f2 - f3 == 3 * w * (t - 1) - t**4,
    )

    # A lower-index first-failure hypothesis does not bound the higher
    # neighbor.  This exact recurrence-level model has T_0 bounded, T_1=0,
    # T_2 the first failure, and T_3 cancelling the recurrence.
    t0, t1, t2, t3 = Q(1), Q(0), Q(2), Q(-2)
    recurrence_holds = t3 + t2 + t1 + t0 == 1
    lower_indices_bounded = abs(t0) <= 1 and abs(t1) <= 1
    higher_neighbor_bounded = abs(t3) <= 1
    rejected(
        "first-failure higher-neighbor inference",
        recurrence_holds and lower_indices_bounded and higher_neighbor_bounded,
    )

    print("PASS all Phase-K behavioral mutations fail for mathematical reasons")


if __name__ == "__main__":
    main()
