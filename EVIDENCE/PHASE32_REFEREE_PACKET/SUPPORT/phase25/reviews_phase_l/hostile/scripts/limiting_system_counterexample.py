#!/usr/bin/env python3
"""Check the manuscript's displayed limiting-system elimination identity.

All quantities are constructed directly from H^infinity and S^infinity as
printed.  No file and no frozen expected output is read.
"""

from fractions import Fraction as Q


def limiting_residual(alpha: Q, t: Q, w: Q, delta: Q) -> tuple[Q, ...]:
    return (
        1 / alpha + w / t**2 + delta - 2,
        w / t**3 + delta - 1,
        3 * w / t**4 + 3 * delta - 2,
        4 * w / t**5 + 4 * delta - 2,
    )


def main() -> None:
    # This point is inside the manuscript's outer rational parameter box.
    alpha, t, w, delta = Q(3), Q(2), Q(5), Q(1, 4)
    residual = limiting_residual(alpha, t, w, delta)
    claimed_left = 3 * t * residual[2] - residual[3]
    claimed_right = 3 * w * (t - 1) - t**4

    assert claimed_left == Q(-3, 2)
    assert claimed_right == Q(-1)
    assert claimed_left != claimed_right

    # The polynomial relation follows instead by eliminating delta from the
    # second and third zero equations; it is not an identity of residuals.
    print("FAIL displayed limiting-system identity")
    print(f"point={(alpha, t, w, delta)}")
    print(f"F={residual}")
    print(f"3*t*F_2-F_3={claimed_left}")
    print(f"3*w*(t-1)-t^4={claimed_right}")


if __name__ == "__main__":
    main()
