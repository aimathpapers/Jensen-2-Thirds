# Phase 24 correlated AI re-review intake

Date received: 2026-08-17
Candidate reviewed: `7bb179ef62f979d58f2587db87a19d0c1f77b28d`
Classification: AI re-review; not separated first-pass review; not human or
peer review

## Provenance and separation status

Both reports identify their reviewer as Claude Opus 5 (Anthropic). Each
report discloses that the same model retained knowledge of its earlier review
of the pre-Phase-24 candidate in the same working session. The packet files
themselves satisfied document separation, but reviewer-level separation did
not occur. These reports are therefore archived as correlated AI re-review
evidence and must not be described as fresh separated review.

The analytic reviewer supplied seven independently entered Python scripts and
a README. Those files are preserved byte-for-byte under `analytic/scripts/`.
No separate algebraic recalculation scripts accompanied the algebraic report.

## Consolidated verdict

Both actual Phase-24 reports return `R1`: two P1 manuscript defects, no P0.
The pasted constant-32 algebraic paragraph belongs to the earlier review and
is stale for this candidate; Phase 24 already uses the repaired provisional
threshold 256.

The two accepted P1 findings are:

1. manuscript equation `eq:factor8` has the wrong factorial prefactor and
   exponential weight;
2. manuscript equation `eq:radius` omits `y^k`, inserts `1/k!`, and includes
   the undefined `k=0` root expression.

The underlying Phase-21 and Phase-16 proof notes state the correct identities.
The repair candidate must also state the multiplier-stability lemma, display
the two-thirds exponent arithmetic, make the localization enlargement and
Gaussian half-plane input explicit, repair the listed P3 exposition defects,
and add equation-regression gates.

## Disposition policy

The reports and scripts below are historical evidence for the repair. They
must be excluded from the next first-pass reviewer ZIPs. After repair, serial
verification, and a new immutable source freeze, review must be performed by
a different provider or a genuinely context-free reviewer. Any AI reviewer
must be identified as such.
