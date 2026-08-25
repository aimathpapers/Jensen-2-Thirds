# Fresh Phase 32 independent AI review findings

Date received: 2026-08-25

This was an AI-only adversarial review performed from a clean extraction of
the Phase 32 referee packet. It was not human or peer review. The reviewer
quarantined historical review reports until freezing its findings and supplied
independent Lean, SymPy, and numerical scripts.

## Frozen verdict

The reviewer reported one P1, two P2s, and six P3s:

1. **P1 — vacuous MSS formal hypothesis.** `MSSFiniteFreeIntervalInput`
   quantified over arbitrary lower endpoints without requiring positivity.
   By choosing negative symmetric intervals, the reviewer kernel-proved that
   `XiNaturalClassicalRootInputs` was uninhabitable for every positive degree.
   Thus the shipped Lean headline theorem was vacuous, although the paper's
   intended MSS use had positive endpoints.
2. **P2 — failing Phase 32 source gate.** The appendix split
   `not_twoThirdsWedge_finiteCutoffAbsorption` across two code spans, while the
   gate required the literal source name.
3. **P2 — mutation-language overstatement.** The seven Phase 32 mutations were
   source-string contract tests, not semantic execution mutations, and none
   targeted the MSS guard defect.
4. **P3 — MMP bibliography.** Rafael Morales was incorrectly listed as Ramón
   Morales.
5. **P3 — no single global Lean declaration.** The above-cutoff headline and
   below-cutoff empty-antecedent theorem were separate declarations.
6. **P3 — at least versus exactly.** `HasDistinctNegativeRoots` asserted at
   least `d` roots; exactness followed mathematically from degree `d` but was
   not part of the terminal Lean conclusion.
7. **P3 — MMP factor fields are domain side conditions.** The factor-root and
   degree fields document applicability but are not used to derive the
   imported MMP conclusion inside Lean; this needed explicit disclosure.
8. **P3 — provenance gaps.** The extracted review environment did not include
   the original ZIP, the sanitized commit was absent, and the packet manifest
   was not cryptographically bound to a candidate Git tree.
9. **P3 — multiline axiom parser.** The checker parsed only the first line of
   each `#print axioms` summary, so a custom axiom on a continuation line could
   evade the allow-list.

## Independently reproduced positives

The reviewer independently reproduced the factor-eight identity, the concrete
two-factor finite-free coefficient identity, the Jacobi specialization and
convention reversal, the exact MMP v3 statements, the saddle derivative tower
through order six, the 82-term majorant, the parameter branch and Jacobian,
the recurrence coefficients, the multiplier tail, finite absorption, the
full Lean build, fresh kernel replay, and the standard-axiom-only terminal
audit. Six independent mutations supplied by the reviewer were rejected.
