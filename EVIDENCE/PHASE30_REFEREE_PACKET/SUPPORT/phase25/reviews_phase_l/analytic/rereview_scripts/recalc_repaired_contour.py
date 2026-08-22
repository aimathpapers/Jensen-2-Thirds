#!/usr/bin/env python3
"""Clean-room check of the repaired contour coordinate and amplitude.

Inputs are constructed from the displayed first-mode Mellin phase.  The
script uses only Python's standard library and reads no frozen result.
Numerical quadrature is regression evidence, not a uniform contour proof.
"""

from __future__ import annotations

import cmath
import math


PI = math.pi


def saddle(s: complex) -> complex:
    ell = cmath.log(s) - cmath.log(cmath.log(s)) - math.log(PI)
    for _ in range(40):
        exponential = cmath.exp(ell)
        residual = ell * (PI * exponential + 0.75) - s
        derivative = PI * exponential * (ell + 1) + 0.75
        step = residual / derivative
        ell -= step
        if abs(step) <= 1e-14 * max(1.0, abs(ell)):
            return ell
    raise AssertionError("saddle Newton iteration did not converge")


def simpson(function, left: float, right: float, panels: int) -> complex:
    if panels % 2:
        panels += 1
    step = (right - left) / panels
    total = function(left) + function(right)
    total += 4 * sum(function(left + j * step) for j in range(1, panels, 2))
    total += 2 * sum(function(left + j * step) for j in range(2, panels, 2))
    return total * step / 3


def phase(s: complex, u: complex) -> complex:
    # Jacobian exp(u) is deliberately not included.
    return s * cmath.log(u) - 0.75 * u - PI * cmath.exp(u)


def leading_ratio(s: complex) -> complex:
    ell = saddle(s)
    curvature = s * (1 / ell + 1 / ell**2) - 0.75
    log_main = phase(s, ell) + ell + 0.5 * cmath.log(2 * PI / curvature)

    def normalized_integrand(u: float) -> complex:
        if u == 0:
            return 0j
        # exp(u) is the exact Jacobian amplitude after t=exp(u).
        return cmath.exp(phase(s, u) + u - log_main)

    return simpson(normalized_integrand, 0.0, 10.0, 120_000)


def main() -> None:
    for s in (80 + 0j, 120 * cmath.exp(0.002j)):
        ell = saddle(s)
        curvature = s * (1 / ell + 1 / ell**2) - 0.75
        rho = abs(curvature) ** (-0.4)
        real_increment = phase(s, ell + rho) - phase(s, ell)
        vertical_increment = phase(s, ell + 1j * rho) - phase(s, ell)
        gaussian_moment_ratio = 3 / curvature**2 + 1 / curvature**3

        print(f"s={s:.10g}")
        print(f"  L={ell:.12g}; K={curvature:.12g}; Re(K)={curvature.real:.12g}")
        print(f"  phase'(L) residual={abs(s/ell-0.75-PI*cmath.exp(ell)):.3e}")
        print(f"  full exponent derivative at L = 1 (Jacobian amplitude)")
        print(f"  Re phase change along L+r at r=rho: {real_increment.real:.12g}")
        print(f"  Re phase change along L+i*rho: {vertical_increment.real:.12g}")
        print(f"  exact normalized cubic Gaussian moment: {gaussian_moment_ratio:.12g}")
        print(f"  direct I1/A regression: {leading_ratio(s):.12g}")

    print("derived Taylor signs")
    print("  Phi''(L)=-K")
    print("  Phi(L+r)-Phi(L)=-K*r^2/2+O(r^3)")
    print("  Phi(L+i*v)-Phi(L)=+K*v^2/2+O(v^3)")


if __name__ == "__main__":
    main()
