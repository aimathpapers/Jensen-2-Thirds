#!/usr/bin/env python3
"""Expose the uncontrolled higher neighbor in the printed first-failure step.

This is a logical probe of the stated recurrence argument, not a claimed
counterexample to the actual hypergeometric radius theorem.  It constructs
all data locally and reads no expected-result artifact.
"""

from fractions import Fraction as Q


def main() -> None:
    # At k=m+2, the recurrence is P3*T_(k+1)+P2*T_k+P1*T_(k-1)+P0*T_(k-2)=0.
    # Lower-index control cannot control T_(k+1).
    p3, p2, p1, p0 = Q(1, 4), Q(1), Q(0), Q(1, 4)
    t0, t1, t2, t3 = Q(1), Q(0), Q(2), Q(-9)
    recurrence = p3 * t3 + p2 * t2 + p1 * t1 + p0 * t0

    assert recurrence == 0
    assert abs(t0) <= 1 and abs(t1) <= 1
    assert abs(t2) > 1  # First failure at k=2.
    assert p3 + p1 + p0 < p2

    print("FAIL first-failure inference from lower-index bounds")
    print(f"recurrence residual={recurrence}")
    print(f"(T0,T1,T2,T3)={(t0, t1, t2, t3)}")
    print("T3 is the uncontrolled higher neighbor; a global-maximum argument is needed.")


if __name__ == "__main__":
    main()
