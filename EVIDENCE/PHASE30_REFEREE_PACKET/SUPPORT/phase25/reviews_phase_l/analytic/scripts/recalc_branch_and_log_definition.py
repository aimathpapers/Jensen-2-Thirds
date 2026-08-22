#!/usr/bin/env python3
"""Clean-room exact branch checks and the logarithm-definition audit.

The script constructs all rational data locally.  It deliberately does not
open a candidate artifact.  Its final section derives the distinction between
log(M_z) and log(gamma(z)) from the duplication formula and quantifies the
unpaired polygamma term created if the two are conflated.
"""

from __future__ import annotations

from fractions import Fraction as F
import math


def matrix_multiply(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(4)) for j in range(4))
        for i in range(4)
    )


def psi5_series(x: float, terms: int = 1_000_000) -> float:
    # psi^(5)(x)=120 sum_{k>=0}(x+k)^-6.  Add an integral tail bracket via
    # the midpoint of its elementary lower and upper integral bounds.
    partial = math.fsum((x + k) ** -6 for k in range(terms))
    lower_tail = (x + terms) ** -5 / 5
    upper_tail = (x + terms - 1) ** -5 / 5
    return 120 * (partial + (lower_tail + upper_tail) / 2)


def main() -> None:
    alpha, t, w, delta = F(3), F(2), F(16, 3), F(1, 3)
    limiting_residual = (
        1 / alpha + w / t**2 + delta - 2,
        w / t**3 + delta - 1,
        3 * w / t**4 + 3 * delta - 2,
        4 * w / t**5 + 4 * delta - 2,
    )
    print(f"limiting-system residual at constructed positive solution = {limiting_residual}")

    jacobian = (
        (F(-1, 9), F(-4, 3), F(1, 4), F(1)),
        (F(0), F(-1), F(1, 8), F(1)),
        (F(0), F(-2), F(3, 16), F(3)),
        (F(0), F(-5, 3), F(1, 8), F(4)),
    )
    inverse = (
        (F(-9), F(45), F(-24), F(9)),
        (F(0), F(6), F(-6), F(3)),
        (F(0), F(48), F(-112, 3), F(16)),
        (F(0), F(1), F(-4, 3), F(1)),
    )
    identity = tuple(
        tuple(F(int(i == j)) for j in range(4)) for i in range(4)
    )
    print(f"J*J^-1 is identity: {matrix_multiply(jacobian, inverse) == identity}")
    print(f"J^-1*J is identity: {matrix_multiply(inverse, jacobian) == identity}")
    print(
        "inverse infinity norm = "
        f"{max(sum(abs(value) for value in row) for row in inverse)}"
    )

    # Exact endpoint checks for A>B>C>D after multiplying out x>0.
    e_max = F(1, 12)
    remote_min = F(5, 2) / e_max
    near_max = F(9, 4) + F(6) * e_max
    lower_gap = F(7, 4) - 1 - F(5, 12) * e_max
    print(f"alpha/e lower endpoint = {remote_min}; t+w*e upper endpoint = {near_max}")
    print(f"t-1-delta*e lower endpoint = {lower_gap}")

    print("\nnormalization identity derived from Legendre duplication")
    print("gamma(z) = sqrt(pi) * 2^(-2z) * M_z / Gamma(z+1/2)")
    print("therefore D^6 log(gamma) = D^6 log(M) - psi^(5)(z+1/2)")
    print(
        "If h means log(M), the residual contains h^(6)-psi^(5)(z+1/2); "
        "if h means log(gamma), that separate term must be removed."
    )

    print("\nsize of the term that becomes unpaired under the manuscript definition")
    for n in (20, 50, 100, 250):
        value = psi5_series(n + 0.5, terms=30_000)
        print(
            f"n={n:3d}: n^5*psi5(n+1/2)={n**5*value:.12f}; "
            f"log(n)*n^5*psi5={math.log(n)*n**5*value:.12f}"
        )


if __name__ == "__main__":
    main()
