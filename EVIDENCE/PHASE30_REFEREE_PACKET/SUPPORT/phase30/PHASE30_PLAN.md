# Phase 30 plan: xi-specific multiplier closure

Date: 2026-08-21

## Objective

Close the previously disclosed stronger-middle endpoint without importing a
project axiom: construct the concrete xi multiplier, prove its six node
values and strict unit bound, instantiate the interval certificate, connect
it to the actual transformed xi Jensen polynomial, and expose a headline
Lean theorem whose only non-project mathematical inputs are the explicitly
typed Jacobi/MMP/MSS literature records.

## Gates

1. Kernel-build the concrete multiplier and six-node interpolation chain.
2. Kernel-build the residual-to-unit-bound specialization.
3. Kernel-build the complete-root/Rolle interval constructor and concrete
   `MultiplierIntervalCertificate`.
4. Kernel-build the transformed-xi identity and headline root transfer,
   including degrees zero through five.
5. Audit the terminal declarations for unexpected axioms and scan the whole
   new proof surface for proof escapes.
6. Reject semantic source mutations that weaken a node count, strict bound,
   interval constructor, actual-polynomial connection, or headline branch.
7. Replay the terminal module in a fresh Lean kernel process.
8. Update the paper and assurance map, perform a correlated AI-only
   adversarial review, and build a deterministic comprehensive reviewer
   package.

The phase must not describe AI-only review as human or peer review.
