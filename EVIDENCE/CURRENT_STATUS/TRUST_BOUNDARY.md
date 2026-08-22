# Phase 30 trust boundary

Date: 2026-08-21

## Kernel-checked endpoint

Lean constructs and checks:

- the concrete analytic xi multiplier;
- its exact values `1` at nodes `0,1,2,3,4,5`;
- the uniform strict bound `|c_F(z)-1|<1` on the required complex tube;
- the finite Newton relative-error estimate at every comparison critical
  point;
- a complete comparison-root list, the intervening Rolle points, natural
  sign intervals, and the concrete `MultiplierIntervalCertificate`;
- the equality between the multiplier transform and the actual transformed
  xi Jensen polynomial;
- positive-root transfer and the final negative scaling; and
- `riemannXiJensen_twoThirds_headline`, including the exact low-degree path.

The terminal axiom driver reports only `propext`, `Classical.choice`, and
`Quot.sound`. These are standard Lean/Mathlib logical principles, not
project-specific mathematical axioms.

## Explicit literature inputs

The headline theorem accepts one `XiNaturalClassicalRootInputs` value. Its
fields are exactly two typed ratio-free Jacobi root/matrix inputs, one typed
MSS finite-free interval input, and one typed MMP strict-log-mesh input. Lean
checks every project-specific normalization, convention adapter, interval
use, and downstream implication, but this phase does not re-prove those
third-party Jacobi/MMP/MSS theorems from first principles.

## Other evidence

SymPy, the user-executed clean-room Mathematica notebook, Arb/ACB, and finite
root regressions are corroborating evidence. They are not premises of the
Lean theorem.

All reviews available for this phase are AI-only. They are not human or peer
review, and the correlated Phase-30 review is not represented as independent
of the implementation context.
