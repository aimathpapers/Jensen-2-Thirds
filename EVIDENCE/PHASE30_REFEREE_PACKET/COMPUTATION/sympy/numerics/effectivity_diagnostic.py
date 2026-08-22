#!/usr/bin/env python3
"""Illustrate the scale loss in the unweighted Phase-15 contraction.

The matrix arithmetic is exact.  The coefficient 10.7 is the first
reviewer's reported numerical diagnostic for L_n * ||DG_n-DF||_infinity; it
is not a proved upper bound.  Accordingly, the resulting n and K scales are
diagnostics, not theorem constants.
"""

from __future__ import annotations

import argparse
import json
import math
from fractions import Fraction
from pathlib import Path


GAUGE_INVERSE = (
    (Fraction(-9), Fraction(45), Fraction(-24), Fraction(9)),
    (Fraction(0), Fraction(6), Fraction(-6), Fraction(3)),
    (Fraction(0), Fraction(48), Fraction(-112, 3), Fraction(16)),
    (Fraction(0), Fraction(1), Fraction(-4, 3), Fraction(1)),
)


def build_report(reported_error_coefficient: float) -> dict:
    row_sums = [sum(abs(value) for value in row) for row in GAUGE_INVERSE]
    inverse_norm = max(row_sums)
    c3_error_cap = Fraction(1, 4) / inverse_norm
    required_l = reported_error_coefficient / float(c3_error_cap)

    # L_n means L_(2n-2): 2n-2 = L_n (pi exp(L_n) + 3/4).
    log10_n = (
        required_l + math.log(required_l) + math.log(math.pi / 2)
    ) / math.log(10)
    # The theorem hypothesis has K on the scale n^2 log(n+2) when d=1.
    log10_k = 2 * log10_n + math.log10(math.log(10) * log10_n)

    return {
        "status": "PASS",
        "formal_status": "illustrative only",
        "matrix_arithmetic": "exact rational",
        "gauge_inverse_row_sums": [str(value) for value in row_sums],
        "gauge_inverse_infinity_norm": str(inverse_norm),
        "c3_sufficient_raw_error_cap": str(c3_error_cap),
        "reported_asymptotic_error_coefficient": reported_error_coefficient,
        "illustrative_required_L_n": round(required_l, 12),
        "illustrative_log10_n": round(log10_n, 12),
        "illustrative_log10_K_scale": round(log10_k, 12),
        "interpretation": (
            "If the externally reported 10.7/L_n diagnostic were a rigorous "
            "global bound with no lower-order loss, the unweighted contraction "
            "would not reach its sufficient C3 threshold until n was around "
            "10^1887. This does not provide an explicit theorem threshold."
        ),
        "rescaling_status": (
            "A diagonal rescaling cannot be certified from one aggregate norm "
            "coefficient; componentwise value and Jacobian error constants are "
            "required before optimizing a weighted norm."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reported-error-coefficient", type=float, default=10.7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = build_report(args.reported_error_coefficient)
    encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
