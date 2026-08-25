# Jensen two-thirds manuscript set

This directory contains the maintained scholarly sources for the Jensen
two-thirds candidate.

- `JENSEN_TWO_THIRDS_MAIN.tex` is the self-contained main paper.
- `c48_detailed_appendices.tex` contains the detailed proof appendices loaded
  by the main paper.
- `JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex` records formal, exact,
  interval, source-fidelity, and reproducibility details.
- `c48_common.tex` contains shared notation and theorem environments.
- `references.bib` is the version-pinned bibliography.
- `THEOREM_EVIDENCE_CROSS_REFERENCE.md` maps T1--T18 to paper, Lean,
  computation, external sources, and remaining boundaries.

Build from the repository root with:

```bash
/opt/homebrew/Cellar/tectonic/0.17.0/bin/tectonic -X compile \
  paper/JENSEN_TWO_THIRDS_MAIN.tex --outdir output/pdf \
  --keep-logs --keep-intermediates
/opt/homebrew/Cellar/tectonic/0.17.0/bin/tectonic -X compile \
  paper/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex --outdir output/pdf \
  --keep-logs --keep-intermediates
```

The release gate rejects unresolved references, layout warnings, changed
normalizations, incorrect page counts, and claims of human or peer review.
All reviews currently available are AI adversarial reviews.

The maintained submission version is Version 1.0 (21 August 2026).  The
author is identified as an independent researcher.  A version-specific DOI
will be inserted after it is reserved during the public-deposit sequence;
until then the date, version, immutable source commit, and SHA-256 manifest
are the citation anchors.

The maintained source includes the Phase-28 literal T5 Lean closure.  The
Phase-29 Palomar package is locally verified and submission-ready, but an
official Comparator/NanoDa result must not be claimed until Palomar publishes
one.

Phase 30 closes the xi-specific multiplier endpoint in Lean: the concrete
multiplier, its six node values and uniform unit bound, the complete
Rolle-point interval certificate, the actual transformed Jensen identity,
and the headline negative-root theorem are kernel checked.  The headline
theorem retains only explicitly typed Jacobi/MMP/MSS literature inputs.

Phase 32 narrows the MMP boundary from the final xi comparison polynomial to
its two concrete Jacobi factors.  Appendix G derives their exact finite-free
convolution identity with the published terminating `_3F_2`, checks the
Jacobi parameter range, and applies the pinned MMP v3 positivity and log-mesh
statements.  Lean transports the resulting convolution roots to the xi
comparison through the kernel-checked coefficient identity.  It also checks
the finite pre-cutoff absorption arithmetically, without assuming low-index
hyperbolicity.
