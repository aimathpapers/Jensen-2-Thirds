# Phase 30 AI-only adversarial review

Date: 2026-08-21  
Scope: xi-specific multiplier, interval certificate, actual Jensen connection,
headline theorem, and Phase-30 release claims  
Technical verdict: **R0 on the Phase-30 delta; no P0, P1, or P2 finding**  
Release recommendation: **R1 qualified release**

## Review-status disclosure

This is a fresh adversarial pass performed by an AI system in the same
repository and conversation context as the implementation. It is therefore
correlated AI-only review, not an independent human review and not peer
review. The release recommendation is qualified because the Jacobi/MMP/MSS
inputs remain typed imports and because no human reviewer is available.

## Gate verdicts

| Gate | Question | Verdict |
|---|---|---|
| A0 | Is the concrete multiplier tied to the actual xi/model logarithmic coordinates? | PASS |
| A1 | Are all six node values `c_F(j)=1`, `0<=j<=5`, kernel checked? | PASS |
| A2 | Does the strict unit bound follow from the existing sixth-residual theorem on the consumed tube? | PASS |
| A3 | Is the finite Newton identity used with the correct factorial, Euler jet, and tail order? | PASS |
| A4 | Are the comparison roots complete, positive, simple, and correctly ordered before sign transfer? | PASS, conditional on typed MMP input |
| A5 | Do the Rolle endpoints give one comparison sign change per separated interval? | PASS |
| A6 | Is `MultiplierIntervalCertificate` instantiated rather than merely assumed? | PASS |
| A7 | Is the multiplier transform definitionally connected to the actual transformed xi Jensen polynomial? | PASS |
| A8 | Are degrees zero through five covered without using the high-degree tail theorem? | PASS |
| A9 | Does the terminal theorem expose, rather than hide, the literature boundary? | PASS |
| A10 | Do axiom, mutation, and fresh-replay gates fail closed? | PASS |

## Independent recalculation record

`phase30_adversarial_checks.py` does not read Lean output or frozen numerical
certificates. For every degree 6 through 12 it constructs a rational
polynomial with roots `1,...,d`, constructs a coefficient multiplier with
the first six values exactly one, and verifies over exact rationals that

1. the Gregory--Newton/Hasse expansion reproduces `P(x)/p(x)-1`;
2. every selected interval contains one comparison sign change;
3. strict unit relative error at both endpoints transfers that sign change;
4. the perturbed polynomial has `d` distinct positive numerical roots.

The same script independently parses the `XiNaturalClassicalRootInputs`
record and confirms that it contains exactly `first_jacobi`, `second_jacobi`,
`mss`, and `mmp`; verifies that the terminal theorem consumes both its
low-degree and high-degree branches; checks the T18 assurance entry; and
rejects stale reader-facing claims that the multiplier remains unconstructed.

## Proof-surface audit

The serial Phase-30 verifier:

- rejected nine semantic source mutations, including five-node, non-strict
  unit-bound, disconnected finite-Newton, disconnected Rolle-certificate,
  disconnected actual-Jensen, and removed low-degree variants;
- built the 8,833-job Jensen-wedge target;
- found no `sorry`, `admit`, custom `axiom`, `unsafe`, `sorryAx`, or
  `Lean.ofReduceBool` escape on the new surface;
- audited twelve terminal declarations, each depending only on `propext`,
  `Classical.choice`, and `Quot.sound`; and
- completed `leanchecker --fresh` on
  `Zeta23.Research.JensenWedge.XiNaturalMultiplierCertificate`.

## Findings

No P0, P1, or P2 defect was found in the Phase-30 delta.

### F1 — P3 — The terminal theorem is an effective-cutoff theorem

`riemannXiJensen_twoThirds_headline` takes the explicit cutoff and wedge as
ordinary hypotheses. The manuscript already states this correctly. The
paper's finite pre-cutoff absorption remains a paper-level existential-
constant step rather than a separate global Lean wrapper. This does not
weaken the kernel-checked asymptotic endpoint or hide an analytic premise,
but readers should not mistake the declaration for a no-cutoff formulation.

### F2 — P3 — Third-party theorem statements are not re-proved

The two Jacobi inputs, MSS interval input, and MMP strict-log-mesh input are
ordinary typed theorem parameters. This is the selected stopping point and
is accurately disclosed. Their source-fidelity audit remains load-bearing.

## Unchecked claims

- This pass did not formalize the cited Jacobi, MMP, or MSS papers from first
  principles.
- It did not run official Palomar Comparator or NanoDa services; no official
  Palomar result is claimed.
- It did not supply human or peer review.

## Recommendation

Release the Phase-30 candidate as a qualified, AI-reviewed formal-evidence
package. Lead with the exact Lean theorem and the typed literature boundary,
retain the Mathematica/SymPy/Arb channels as corroboration rather than proof
premises, and invite third parties to attack the four external-input adapters
and the paper's finite-cutoff absorption first.
