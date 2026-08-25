#!/usr/bin/env python3
"""Verify the Phase-24 branch-box and parameter inequalities exactly.

No floating-point arithmetic is used.  The committed JSON is a readable
certificate ledger; this script reconstructs every entry from Fraction
arithmetic and rejects stale or altered values.
"""

from __future__ import annotations

import json
from fractions import Fraction as Q
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CERTIFICATE = ROOT / "ground_zero_work/phase24/INTERVAL_CERTIFICATES.json"


def q(value: Q) -> str:
    """Canonical exact-rational representation."""
    return f"{value.numerator}/{value.denominator}"


def build_certificate() -> dict[str, object]:
    alpha_lo, alpha_hi = Q(5, 2), Q(7, 2)
    t_lo, t_hi = Q(7, 4), Q(9, 4)
    w_lo, w_hi = Q(5), Q(6)
    delta_lo, delta_hi = Q(1, 4), Q(5, 12)
    e_hi = Q(1, 12)

    remote_numerator_min = alpha_lo / e_hi
    b_numerator_max = t_hi + w_hi * e_hi
    cd_gap_min = t_lo - 1 - delta_hi * e_hi
    d_numerator_min = 1 + delta_lo * Q(0)  # closure value; e > 0 in use

    y_star = (Q(3), Q(2), Q(16, 3), Q(1, 3))
    box = (
        (alpha_lo, alpha_hi),
        (t_lo, t_hi),
        (w_lo, w_hi),
        (delta_lo, delta_hi),
    )
    margins = tuple((point - lo, hi - point) for point, (lo, hi) in zip(y_star, box))

    saddle_small = Q(7, 50)
    saddle_factor_perturbation = saddle_small + Q(3, 4) * saddle_small
    saddle_reduced_perturbation = 4 * saddle_small + 3 * saddle_small

    coarse_b_over_n_upper = Q(3)
    coarse_d_over_n_lower = Q(1, 2)
    coarse_b_over_d_upper = coarse_b_over_n_upper / coarse_d_over_n_lower
    provisional_v_over_degree = Q(256)
    degree_over_d_parameter_upper = 1 / provisional_v_over_degree
    jacobi_radius = Q(8)
    positive_lower_fraction = Q(1, 2)
    required_v_over_degree = (jacobi_radius / positive_lower_fraction) ** 2
    cross_term_upper = 64 * Q(1, 16)

    sqrt6_upper = Q(5, 2)
    c_loc_constant_term = 8 + cross_term_upper
    c_loc_sqrt_coefficient = 8
    c_loc_upper = c_loc_constant_term + c_loc_sqrt_coefficient * sqrt6_upper
    k0_rational = provisional_v_over_degree * c_loc_upper**2

    h6_majorant = Q(
        6422139805764931584036533551104,
        702576099728137594188684005,
    )
    h6_strict_upper = Q(10000)
    g0_sixth_bound_coefficient = 2 * h6_strict_upper

    assert remote_numerator_min == 30
    assert b_numerator_max == Q(11, 4)
    assert remote_numerator_min > b_numerator_max
    assert cd_gap_min == Q(103, 144) > 0
    assert d_numerator_min == 1 > 0
    assert all(left > 0 and right > 0 for left, right in margins)
    assert saddle_factor_perturbation == Q(49, 200)
    assert 1 - saddle_factor_perturbation == Q(151, 200) > Q(9, 16)
    assert saddle_reduced_perturbation == Q(49, 50)
    assert 4 - saddle_reduced_perturbation == Q(151, 50)
    assert coarse_b_over_d_upper == 6
    assert degree_over_d_parameter_upper == Q(1, 256)
    assert required_v_over_degree == 256
    assert provisional_v_over_degree >= required_v_over_degree
    assert cross_term_upper == 4
    assert sqrt6_upper**2 > 6
    assert c_loc_constant_term == 12
    assert c_loc_sqrt_coefficient == 8
    assert c_loc_upper == 32
    assert k0_rational == 262144
    assert h6_majorant < h6_strict_upper
    assert g0_sixth_bound_coefficient == 20000

    return {
        "arithmetic": "fractions.Fraction; no binary floating point",
        "branch_box": {
            "box": [[q(lo), q(hi)] for lo, hi in box],
            "point": [q(value) for value in y_star],
            "left_right_margins": [[q(left), q(right)] for left, right in margins],
        },
        "elementary_parameters": {
            "e_range": "0 < e <= 1/12",
            "x_range": "0 < x",
            "A_numerator_min": q(remote_numerator_min),
            "B_numerator_max": q(b_numerator_max),
            "C_minus_D_numerator_min": q(cd_gap_min),
            "D_numerator_closure_min": q(d_numerator_min),
            "strict_order": "A > B > C > D > 0",
        },
        "finite_free_localization": {
            "coarse_B_over_D_upper": q(coarse_b_over_d_upper),
            "degree_over_D_upper": q(degree_over_d_parameter_upper),
            "jacobi_radius_coefficient": q(jacobi_radius),
            "positive_lower_endpoint_fraction": q(positive_lower_fraction),
            "required_V_over_d_lower": q(required_v_over_degree),
            "provisional_V_over_d_lower": q(provisional_v_over_degree),
            "product_cross_term_upper": q(cross_term_upper),
            "C_loc_formula": "12 + 8 sqrt(6)",
            "sqrt6_strict_upper": q(sqrt6_upper),
            "C_loc_strict_upper": q(c_loc_upper),
            "rational_K0": q(k0_rational),
            "a_priori_threshold": "B,D >= 256 d",
            "conclusion": "8 sqrt(Bd) <= B/2 and 8 sqrt(Dd) <= D/2",
        },
        "saddle_box": {
            "r_sigma_norm_upper": q(saddle_small),
            "scaled_factor_perturbation_upper": q(saddle_factor_perturbation),
            "scaled_factor_norm_lower": q(1 - saddle_factor_perturbation),
            "paper_lower_bound": q(Q(9, 16)),
            "reduced_denominator_perturbation_upper": q(saddle_reduced_perturbation),
            "reduced_denominator_norm_lower": q(4 - saddle_reduced_perturbation),
        },
        "sixth_derivative_majorant": {
            "box_radius": q(saddle_small),
            "reduced_denominator": "(4 + 4 r - 3 sigma)^12",
            "numerator_term_count": q(Q(82)),
            "numerator_total_degree": q(Q(13)),
            "coefficient_majorant": q(h6_majorant),
            "strict_upper": q(h6_strict_upper),
            "G0_sixth_bound_coefficient": q(g0_sixth_bound_coefficient),
            "scope": (
                "exact rational transcription and inequality; independently "
                "reproduced by user-executed Mathematica M4"
            ),
        },
    }


def reject_floats(value: object) -> None:
    if isinstance(value, float):
        raise AssertionError("floating-point value found in exact certificate")
    if isinstance(value, dict):
        for child in value.values():
            reject_floats(child)
    elif isinstance(value, list):
        for child in value:
            reject_floats(child)


def main() -> None:
    expected = build_certificate()
    actual = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    reject_floats(actual)
    if actual != expected:
        raise AssertionError(
            "INTERVAL_CERTIFICATES.json is stale; regenerate from exact definitions"
        )
    print("PASS phase24 exact interval certificates")


if __name__ == "__main__":
    main()
