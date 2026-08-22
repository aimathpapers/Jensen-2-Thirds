# C48 first-review repair plan

Date: 2026-08-15  
Status: implementation complete; independent-human-review gate remains

## 1. Objective and release rule

The objective is to convert the Phase-17 internal argument into a
reviewable candidate proof of

\[
n^2\log(n+2)\ge Kd^3
\quad\Longrightarrow\quad
J^{d,n}\text{ has }d\text{ distinct negative real zeros}.
\]

The first review is favorable on the exact algebra and numerics, but it finds
one decisive analytic gap: the proof consumes a sixth derivative bound for
the continued moment logarithm on a proportional complex neighborhood, while
the current Phase-11 note displays only a real-axis asymptotic and a sketch of
the complex extension.  No release or claim-ledger promotion is permitted
until that seam is closed in a named lemma.

The review is classified as an `R0` technical pre-review because its author is
an AI system.  It sharpens the proof but does not count as either of the two
required independent human reviews.

## 2. Source correction that must accompany the repair

Holland's Proposition 2.2 in arXiv:2608.08682v1 assumes

\[
\sup_{\Omega_r}|c-1|\le\varepsilon<16,
\]

not `epsilon < 1/6`.  The PDF and TeX source are unambiguous.  The existing
sixth-order `epsilon < 32` argument is a valid new variant, but the phrase
"generalizes verbatim" is inaccurate.  The main proof will instead invoke
Holland's proposition unchanged: six exact matches imply the five matches he
requires, and the local application already arranges `epsilon <= 1 < 16`.

## 3. Deep proof modules and interfaces

The repair is organized as four modules with narrow interfaces.

### A. Complex saddle module

**Interface.**  Constants `eta,C,x0>0` such that, for real `x>=x0` and
complex `w` with `|w|<=eta*x`, the continued moment is nonzero, the
positive-axis logarithm is defined consistently, and

\[
|h^{(6)}(x+w)|\le C/(x^5\log x).
\]

**Implementation obligations.**  Nested sectors; proportional-disk Cauchy
estimate at order six; sectorial estimates for `L_N`, `Q_N`, and the exact
saddle main term; explicit normalization derivatives; the substitution
`N=2z-2`; and branch compatibility.

### B. Residual module

**Interface.**  On the thickened interpolation domain `Omega`,

\[
\sup_\Omega |E_F^{(6)}|\le C/(n^5\log(n+2)).
\]

**Implementation obligations.**  Prove `n+Omega` lies in the complex-saddle
module's domain; pair the polygamma boundaries by complex line integrals;
exclude poles along every path; define the logarithmic residual on one
holomorphic branch; and prove the six exact logarithmic zeros.

### C. Stability module

**Interface.**  Holland Proposition 2.2 with its printed threshold `16`.

**Implementation obligations.**  Show the multiplier is holomorphic, real at
integer points, equals one at `0,...,5`, has positive leading value, and has
supremum defect at most one.  The independent `1/32` geometric-tail lemma is
retained as a checked strengthening but is not required by the main proof.

### D. Evidence and release module

**Interface.**  One verification command producing a manifest that separates
Lean-checked algebra, exact symbolic identities, non-rigorous numerical
diagnostics, and human-analysis obligations.

**Implementation obligations.**  Version the primary-source hashes; add the
positive-orthant uniqueness theorem; preserve the reviewer computations as
external corroboration until scripts are supplied; quantify the favorable
`C-D` margin; disclose the enormous unoptimized threshold; rebuild and
visually inspect the reviewer DOCX/PDF packets.

## 4. Ordered implementation waves

### Wave 18.1 - freeze the review and gates

1. Record every reviewer point as accept, correct, or corroborating evidence.
2. Freeze Holland v1 PDF/source hashes and the exact `epsilon < 16` text.
3. Mark `C48-H6-RESIDUAL` and `C48-TWO-THIRDS` blocked on the complex lemma.

**Gate:** no document may say Phase 11 proves the complex sixth bound.

### Wave 18.2 - close the complex analytic seam

1. Prove the uniform complex sixth-saddle lemma.
2. Prove explicit sector containment for `n+Omega`.
3. Prove the complex polygamma difference bounds and the residual theorem.
4. State precisely which facts are inherited from Holland and which are new.

**Gate:** every use of a logarithm, Cauchy estimate, or complex line integral
has a displayed domain and nonvanishing/pole-exclusion argument.

### Wave 18.3 - simplify stability and strengthen formal algebra

1. Replace the advertised `<32` dependency by Holland's printed `<16`
   proposition in the main assembly.
2. Retain the order-six tail only as an optional strengthening.
3. Add a Lean corollary proving uniqueness in the whole positive orthant,
   removing the externally supplied `t>1` hypothesis.
4. Build, run `leanchecker`, audit axioms, and reject proof escapes.

### Wave 18.4 - robustness and effectiveness

1. Turn `C-D asymp n` into a fixed eventual lower bound.
2. Record the current inverse norm and resulting threshold scale.
3. Try a diagonal coordinate scaling and report whether it materially reduces
   the contraction loss; do not claim a numerical theorem constant without
   interval-certified analytic constants.

### Wave 18.5 - reproducible evidence

1. Re-run all pinned symbolic producers.
2. Add regression coverage for the derivative tower and sixth rational bound.
3. Re-run the existing true-moment branch and radius diagnostics.
4. Record the reviewer's stronger computations as `EXTERNAL-REPORTED` until
   their scripts, raw outputs, versions, and hashes are received.

### Wave 18.6 - publication packet rebuild

1. Write a self-contained Holland-dependency appendix.
2. Update the theorem draft, ledgers, decisions, packet questions, and evidence
   manifest.
3. Rebuild both DOCX/PDF packets and reviewer ZIP bundles.
4. Render every page, inspect for layout defects, and rerun content/hash checks.

### Wave 18.7 - hostile closeout

1. Search for stale statements that overclaim the complex lemma, the epsilon
   constant, effectiveness, or review status.
2. Run all Phase 13-18 verification commands.
3. Issue a final disposition with separate statuses for the analytic proof,
   Lean algebra, numerics, primary-source dependency, and human review.

## 5. Completion criteria

Implementation is complete only when all of the following hold:

- the uniform complex sixth-saddle lemma is fully written with its domain;
- `M_z != 0` and logarithm compatibility are connected to every downstream
  use;
- the residual `B6` estimate is proved on the actual `Omega`;
- the main proof uses Holland's real `<16` threshold accurately;
- positive-orthant uniqueness is kernel-checked;
- the favorable positivity margin and ineffective threshold are disclosed;
- external numerical reports are not silently promoted to verified evidence;
- regenerated reviewer artifacts pass build, render, and hash checks;
- the result remains explicitly pending two independent human reviews.
