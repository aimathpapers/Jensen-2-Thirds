# Phase 33 trust boundary

Date: 2026-08-25

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
- positive-root transfer and the final negative scaling;
- strict positivity of both MSS interval lower endpoints from the derived
  `B, D >= 256d` geometry before any use of the guarded MSS record;
- the degree-`d` Jensen polynomial object, its nonzero leading coefficient
  `gamma(n+d) > 0`, and the impossibility of `d+1` distinct negative zeros,
  closing the paper's word "exactly" inside the kernel; and
- `riemannXiJensen_twoThirds_global_headline_exactly`: a single global
  declaration whose constant is the literal maximum of the analytic wedge
  constant and the finite-cutoff absorption constant, with the pre-cutoff
  empty-antecedent split (`not_twoThirdsWedge_finiteCutoffAbsorption`) and
  the degree-zero case performed inside the kernel.

The Phase-33 axiom driver reports only `propext`, `Classical.choice`, and
`Quot.sound` for every audited declaration, including the global exact-count
theorem. These are standard Lean/Mathlib logical principles, not
project-specific mathematical axioms.

## Explicit literature inputs

The global theorem accepts, for each in-wedge index above the explicit
cutoff, one `XiNaturalClassicalRootInputs` value. Its fields are exactly two
typed ratio-free Jacobi root/matrix inputs, one guarded MSS finite-free
interval input, and one factor-level `MMPFiniteFreeLogMeshInput`.

- The MMP record is attached to the two displayed Jacobi factor polynomials
  and includes their positive-root and degree hypotheses; it does not assume
  that `xiNaturalComparisonFunction` itself has the desired roots. Lean
  proves the concrete terminating `_3F_2` equals that finite-free
  convolution and transports the roots across the equality.
- The MSS record likewise carries both factor positive-root and degree
  certificates, and its interval field applies only to strictly positive
  lower endpoints. In this guarded form it is the two-orientation
  consequence of MSS Theorem 1.6 for the two concrete factors. The former
  unguarded negative-endpoint call shape is retained as a required
  compile-failure regression.
- In both records the factor-certificate fields are domain side conditions
  that any instantiation must discharge; the downstream Lean proofs consume
  the interval and log-mesh conclusions, not those fields. This is stated so
  that no reader infers that Lean derives the external conclusions from the
  certificates.

Lean checks every project-specific normalization, convention adapter,
interval use, endpoint positivity, and downstream implication, but it does
not re-prove the general third-party Jacobi/MMP/MSS theorems from first
principles.

## Other evidence

SymPy, the user-executed clean-room Mathematica notebook, Arb/ACB, and finite
root regressions are corroborating evidence. They are not premises of the
Lean theorem.

## Review status

A fresh, separated AI-only adversarial review of the Phase-32 candidate
identified the prior unguarded MSS record as release-blocking; Phase 33
repaired every confirmed finding, and the repairs were re-verified by a
fresh AI-only re-review. All reviews available for this project are AI-only.
They are not human or peer review, and no human or peer review is claimed.
