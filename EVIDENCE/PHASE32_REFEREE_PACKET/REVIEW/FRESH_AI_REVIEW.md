# Phase 27 fresh AI release review

Date: 2026-08-21
Candidate: `3d4d60e32f814647cfd24601f83e360d5155252c`
Verdict: **R2 - release repair required; no P0/P1 theorem finding**

## Review status and separation

This is AI review, not human or peer review. The review target was frozen by
commit and the checks were reconstructed from definitions without reading a
prior verdict as an oracle. However, the reviewing AI shares development and
conversation context with the project. The review is therefore correlated
and is not represented as independent scholarly confirmation.

## Gate results on the frozen target

| Gate | Scope | Result |
|---|---|---|
| A0 | theorem statement and normalization | PASS |
| A1 | T1 theta/Mellin/factor-eight chain | PASS |
| A2 | T2 saddle existence, uniqueness, sector, and curvature | PASS |
| A3 | T3 contour direction, branch domain, connector, and Gaussian sign | PASS |
| A4 | T4 infinite higher-mode suppression | PASS |
| A5 | T5 Gamma/Stirling and holomorphic coefficient theorem | PASS |
| A6 | xi branch, six matches, and actual comparison polynomial | PASS |
| A7 | finite-free orientation, root localization, and critical radius | PASS subject to the disclosed Jacobi/MMP/MSS inputs |
| A8 | Hermite--Genocchi and final sign-transfer boundary | PASS as a boundary; the final xi-specific multiplier certificate is not constructed |
| A9 | Lean source/axiom surface | PASS: 1,217 declarations, only `propext`, `Classical.choice`, and `Quot.sound` |
| A10 | release descriptions and replay package | FAIL pending the P2 repairs below |

## Findings

### F27-1 - P2 - manuscript verification section describes the obsolete formal boundary

The main paper, technical supplement, and detailed appendix still say that
the concrete theta moment, moving saddle, contour, higher modes, and
xi-specific branch remain conventional or unconstructed. Phase 26 now
kernel-checks those components. The error does not weaken the paper theorem,
but it makes the release trust boundary materially inaccurate.

### F27-2 - P2 - theorem map and disclosure materials remain at Phase 25

The current reader map classifies T1--T5 and T8--T9 using the pre-Phase-26
surface, and the package materials advertise a 66-declaration audit. The
current audit has 1,217 declarations. A reviewer following the old map would
look in the wrong place and could not distinguish the actual remaining T15
and literature boundaries.

### F27-3 - P2 - Phase 26 declares its completed endpoint “in progress”

`FORMAL_TARGETS.json`, the status header, and `verify_phase26_plan.py` require
one active stage even though F5c60 is the approved stopping point. This is a
state-machine defect in the evidence layer. It does not change a Lean proof,
but it prevents a coherent release freeze.

### F27-4 - P2 - the authoritative replay and package builder omit Phase 26

`reproduce/VERIFY_ALL.sh` begins at Phase 25, and the mature Phase-M package
builder freezes the older axiom driver, assurance matrix, and disclosures.
The new release must run Phase 26 first and package the Phase-26 audit surface
and Phase-27 trust materials.

## Independent recalculation record

The review reconstructed, rather than copied from a saved verdict:

1. the limiting-system Jacobian determinant `-1/144`, exact inverse, and
   infinity norm `304/3` using exact rationals;
2. the simplex mass `1/720` from the six-dimensional ordered simplex;
3. the strict localization inequality `12 + 8 sqrt(6) < 32`;
4. the exact critical-radius normalization and the presence of the factor
   `y^k` with no inserted `1/k!`;
5. the root-completeness/logarithmic-derivative route used to localize every
   non-root critical point; and
6. the Phase-26 axiom-driver cardinality and source-level absence of proof
   escapes.

These checks supplement, but do not replace, the serial repository verifiers.

## Unchecked claims

- The reviewer did not re-prove the general classical Jacobi theorem, the
  cited MMP propositions, or MSS Theorem 1.6.
- The final xi-specific sixth-multiplier interval certificate is outside the
  approved Phase-26 endpoint and remains a paper-proof boundary.
- No human expert has reviewed the theorem.

## Recommendation

Do not distribute the `3d4d60e` package as the current release. Repair the
four P2 release-description and replay findings, rerun the full serial gates,
perform a targeted AI rereview, and package only the repaired commit.
