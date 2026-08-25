#!/usr/bin/env python3
"""Clean-room check of the repaired moment/gamma seam and branch algebra.

The script builds all values from the displayed definitions, uses no packet
artifact as expected data, and reads no file.
"""

from __future__ import annotations

from fractions import Fraction as F
import math


def psi(order: int, x: float, terms: int = 80_000) -> float:
    """Positive-series polygamma for odd order 5 used in this audit."""

    if order != 5:
        raise ValueError("this audit only needs psi^(5)")
    partial = math.fsum((x + k) ** -6 for k in range(terms))
    # Integral-test midpoint tail; far below printed precision here.
    lower = (x + terms) ** -5 / 5
    upper = (x + terms - 1) ** -5 / 5
    return 120 * (partial + (lower + upper) / 2)


def real_saddle(n_value: int) -> float:
    target = 2 * n_value - 2
    ell = math.log(target) - math.log(math.log(target)) - math.log(math.pi)
    for _ in range(30):
        exponential = math.exp(ell)
        residual = ell * (math.pi * exponential + 0.75) - target
        derivative = math.pi * exponential * (ell + 1) + 0.75
        ell -= residual / derivative
    return ell


def matmul(left, right):
    return tuple(
        tuple(sum(left[i][k] * right[k][j] for k in range(4)) for j in range(4))
        for i in range(4)
    )


def main() -> None:
    print("exact moment/gamma bridge")
    print("  gamma(z)=Gamma(z+1)*M_z/Gamma(2z+1)")
    print("  gamma(z)=sqrt(pi)*2^(-2z)*M_z/Gamma(z+1/2)")
    print("  (log gamma)^(6)=(Log M)^(6)-psi^(5)(z+1/2)")
    print("  repaired residual uses h=Log M and retains the one half-shift term")

    for n_value in (40, 100, 250):
        ell = real_saddle(n_value)
        alpha, t, weight, delta = 3.0, 2.0, 16 / 3, 1 / 3
        a = alpha * n_value * ell
        b_cap = n_value * (t + weight / ell)
        c_cap = n_value * t
        d_cap = n_value * (1 + delta / ell)
        b_half = n_value + 0.5
        paired = (
            psi(5, b_cap)
            - psi(5, c_cap)
            + psi(5, d_cap)
            - psi(5, b_half)
            - psi(5, a)
        )
        unpaired = psi(5, b_half)
        print(
            f"n={n_value:3d}: n^5*psi5(n+1/2)={n_value**5*unpaired:.10f}; "
            f"n^5*L*paired={n_value**5*ell*paired:.10f}"
        )

    alpha, t, weight, delta = F(3), F(2), F(16, 3), F(1, 3)
    residual = (
        1 / alpha + weight / t**2 + delta - 2,
        weight / t**3 + delta - 1,
        3 * weight / t**4 + 3 * delta - 2,
        4 * weight / t**5 + 4 * delta - 2,
    )
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
    identity = tuple(tuple(F(int(i == j)) for j in range(4)) for i in range(4))
    print(f"limiting branch residual={residual}")
    print(f"J*P=I: {matmul(jacobian, inverse) == identity}")
    print(f"P*J=I: {matmul(inverse, jacobian) == identity}")
    print(f"||P||_infinity={max(sum(abs(x) for x in row) for row in inverse)}")


if __name__ == "__main__":
    main()
