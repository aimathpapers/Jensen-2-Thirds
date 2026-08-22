# Phase 29 correlated AI-only release audit

Date: 2026-08-21  
Scope: Palomar-facing T5 Challenge/Solution topic and deterministic public
candidate  
Review type: fresh correlated AI-only adversarial audit; not human review and
not peer review

## Verdict

**R1 — submission-ready after local gates, with the official Palomar
Comparator/NanoDa/editorial run still pending.** No P0, P1, or P2 finding
remains on the frozen local surface. The R1 qualifier records a required
external verification gate, not an identified mathematical defect.

## What was audited

The audit compared the trusted declarations against manuscript Theorem 7.1,
its exact centered-xi normalization, and the derivative consequence actually
used through order six. It separately inspected:

- every trusted definition and numerical normalization;
- the positive-integer seam to Mathlib's completed zeta;
- the proof, outer, and closed inner sectors;
- saddle equation, curvature, main term, quotient, and error rate;
- outer holomorphy, main-term nonvanishing, and the derivative ceiling;
- Challenge import separation and size;
- Challenge/Solution definition equality and Comparator configuration;
- terminal axioms, proof-escape tokens, and fresh kernel replay;
- disclosure, licensing, source provenance, and archive reproducibility.

## Findings found and repaired during this audit

### F1 — P2 — Candidate-local trusted helper import

The first packaging draft put the Mathlib-only definitions in
`ChallengeDeps.TheoremSevenOne` and imported that local module into the
Challenge. Current Palomar policy forbids candidate-local modules anywhere in
the Challenge's transitive import closure. The helper was removed. The
Challenge now imports exactly `Mathlib` and embeds every trusted definition;
the marked block is repeated byte-for-byte in the Solution.

Status: **closed**. Lean's `--src-deps` output reaches Lean core and
`Mathlib.lean`, with no `Zeta23`, Solution, or ChallengeDeps source.

### F2 — P2 — Continuation terminology lacked a compared integer seam

The first topic defined the correct theta/Gamma continuation but did not
itself compare it with the actual centered Riemann-xi Taylor coefficient.
That made the word “continuation” depend on an unexposed production theorem.
The trusted surface now defines centered xi directly from Mathlib's
`completedRiemannZeta₀`, defines its even Taylor coefficient, and compares the
positive-integer identity as a third theorem.

Status: **closed**. The Solution bridges definitionally to
`complexXiCoefficientMoment_nat_succ`; its terminal axiom set is the standard
three.

### F3 — P2 — Standalone derivative statement omitted its analytic context

The first derivative declaration constrained the error by the quotient on the
outer sector but did not repeat the saddle-branch and holomorphy clauses. The
two theorem witnesses were existential and therefore were not formally linked
across declarations. Although the concrete proof used the intended function,
the standalone public type was less informative than the prose “same relative
error” suggested.

Status: **closed**. The derivative declaration now repeats openness of both
sectors, saddle-branch differentiability and equation, outer differentiability
of the exact coefficient, main, and error, main-term nonvanishing, and the
exact quotient identity before stating every bound through order six.

### F4 — P3 — Candidate self-audit miscounted deliberate holes

The first deterministic archive passed the archive/source verifier, but its
own candidate-local audit expected an additional explanatory occurrence of
the token `sorry`. The Challenge contains exactly the three deliberate proof
holes and no explanatory token occurrence.

Status: **closed**. The self-audit now requires exactly three occurrences and
the candidate is rebuilt from the corrected immutable commit.

## Statement-fidelity result

The formal result is at least as strong as the concise manuscript theorem in
the following relevant senses:

- it fixes explicit proof/outer/inner angles `1/100`, `1/200`, and `1/400`;
- it exposes an actual saddle branch and its equation;
- it proves holomorphy/differentiability on the open outer sector;
- it proves main-term nonvanishing on the outer sector, stronger than the
  manuscript's inner-sector wording;
- it identifies the error as the exact quotient, not merely an unnamed `O`;
- it gives an explicit existential constant in the
  `log |M| / |M|` normalization; and
- it gives the proportional-radius derivative bound for every `j <= 6`.

The topic intentionally does not claim the final Jensen hyperbolicity theorem
by itself. That theorem also consumes T1--T4 and the finite
free-convolution/algebraic chain. This limitation is stated in the Challenge,
README, and metadata.

## Verification record

The final local gate requires all of the following:

1. Challenge source: under 300 lines and 32 KiB (168 lines, 5,788 bytes).
2. Trusted imports: exactly Mathlib; no candidate-local transitive source.
3. Compared declarations: exactly three; NanoDa enabled.
4. Exact definition block: byte-identical between Challenge and Solution.
5. Semantic mutations: all 17 rejected.
6. Solution/production escapes: no `sorry`, `admit`, custom axiom, `unsafe`,
   `sorryAx`, or `Lean.ofReduceBool` in the selected solution surface.
7. Terminal axioms: exactly `propext`, `Classical.choice`, and `Quot.sound`
   for each compared declaration.
8. Ordinary Lean build and `leanchecker --fresh`: PASS on the final surface.
9. Established downstream replays: Phases 26, 27, 28, 21, and 20 passed
   serially before this packaging-only hardening; the final changes do not
   alter the production proof cone.
10. Candidate archive: complete SHA-256 manifest, no caches/build products,
    safe paths, exact source bytes, and byte-identical output from two builds.

## Remaining external gate

The local environment does not provide Palomar's official Comparator,
`lean4export`, Landrun sandbox, NanoDa service run, or editorial model. Current
Palomar policy requires a public GitHub repository at a full 40-character
commit SHA and then runs all of those checks. They remain pending and are not
claimed here. The candidate must therefore be made public and submitted before
an official Palomar result can be stated.

No human expert or peer review has occurred and none is claimed.
