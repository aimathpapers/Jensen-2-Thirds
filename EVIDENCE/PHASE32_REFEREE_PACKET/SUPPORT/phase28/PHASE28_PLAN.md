# Phase 28 plan: literal T5 closure and Palomar release

Phase 28 turns the already kernel-checked conservative coefficient theorem
into a literal formal version of manuscript Theorem 7.1 and isolates that
result for Palomar Comparator. All review remains AI review, not human or
peer review.

## Acceptance stages

1. **Trust and statement freeze.** Record the exact paper theorem, the two
   terminal Lean declarations, the permitted foundational axioms, and the
   immutable Phase-27 baseline.
2. **Three-sector geometry.** Prove the analytic chain on the `1/100` proof
   sector, coefficient estimates on the `1/200` manuscript outer sector, and
   the final rate on the closed `1/400` inner sector. Prove the affine shift
   `M -> 2M-2` maps the two paper sectors into their required larger sectors.
3. **Literal Theorem 7.1.** Export an explicit effective theorem and the
   paper's existential `R,C` theorem, with outer holomorphy/nonvanishing,
   exact factorization, and the inner `C log|M|/|M|` rate.
4. **Derivative consequence.** Export Cauchy transport for the literal paper
   error through order six.
5. **Fail-closed verification.** Add axiom, source, statement-fidelity, and
   semantic mutation gates; replay Phase 26 and downstream verification
   serially.
6. **Palomar isolation.** Construct a short Mathlib-only `Challenge.lean`, an
   identically typed proved `Solution.lean`, Comparator configuration,
   `formalization.yaml`, and public-reader documentation.
7. **Release candidate.** Build a clean public-repository candidate that
   contains the substantive Lean closure and paper but no confidential review
   packets, private paths, build products, or large audit archives.
8. **Fresh audit and freeze.** Run a fresh AI-only fidelity/reproducibility
   audit, repair findings, freeze manifests and hashes, and push the private
   candidate. Public publication and Palomar registration require separate
   user authorization.

## Required terminal declarations

- `manuscriptTheoremSevenOne_effective`
- `manuscriptTheoremSevenOne`
- `manuscriptPaperRelativeError_derivatives_through_six`

All three must report only `propext`, `Classical.choice`, and `Quot.sound`
under `#print axioms`.
