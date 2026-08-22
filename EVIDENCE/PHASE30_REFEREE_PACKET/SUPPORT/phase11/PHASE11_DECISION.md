# Phase 11 decision checkpoint

Date: 2026-08-15  
Disposition: sixth residual gate passes internally; root-radius recurrence is
the sole dominant mathematical gate

Exact saddle-main differentiation gives the sixth normalized coefficient
`24`, hence `48` for `h^(6)` after the chain rule.  Holland's sectorial Cauchy
argument extends to the sixth remainder derivative.  On the new parameter
branch, the polygamma terms pair across the two nearby boundaries, giving
`E_F^(6)=O(1/(n^5 log n))`.

Six exact coefficient matches then produce multiplier error

`O(d^3/(n^2 log n))`,

and Holland's abstract sign-stability proof extends from the geometric tail
starting at order five to the tail starting at order six.

These are internal paper derivations and still require independent review.
Subject to that review, the residual mechanism supports the proposed
two-thirds wedge.  The campaign now succeeds or fails on one issue: whether
the differentiated finite-free/Jacobi recurrence retains critical-point
derivative bounds with radius `O(sqrt(nd))` for the new parameter geometry.
No theorem is advertised until that gate is closed.
