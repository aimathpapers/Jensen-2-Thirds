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
JENSEN_BUILD_DIR="$(mktemp -d)"
cd PAPER_SOURCE
SOURCE_DATE_EPOCH=1788436800 tectonic -X compile \
  JENSEN_TWO_THIRDS_MAIN.tex --outdir "$JENSEN_BUILD_DIR"
SOURCE_DATE_EPOCH=1788436800 tectonic -X compile \
  JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex --outdir "$JENSEN_BUILD_DIR"
SOURCE_DATE_EPOCH=1788436800 tectonic -X compile \
  JENSEN_TWO_THIRDS_UNIFIED.tex --outdir "$JENSEN_BUILD_DIR"
```

Build the Version 1.1 expository article by placing its disclosure cover before
the frozen Version 1.0 article body:

```bash
JENSEN_BUILD_DIR="$(mktemp -d)"
SOURCE_DATE_EPOCH=1788436800 pandoc \
  EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_FRONT_MATTER.md \
  --standalone --pdf-engine=tectonic -V geometry:margin=0.85in \
  -V fontsize=10pt -V colorlinks=true \
  -o "$JENSEN_BUILD_DIR/JENSEN_TWO_THIRDS_MAGAZINE_COVER.pdf"
SOURCE_DATE_EPOCH=1788436800 swift EXPOSITORY/merge_pdf_cover.swift \
  "$JENSEN_BUILD_DIR/JENSEN_TWO_THIRDS_MAGAZINE_COVER.pdf" \
  EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_ARTICLE_V1.0.pdf \
  EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_ARTICLE.pdf
```

The fixed epoch records the Version 1.1 attribution revision.

The release gate rejects unresolved references, layout warnings, changed
normalizations, incorrect page counts, and claims of human or peer review.
All reviews currently available are AI adversarial reviews.

The maintained submission version is Version 1.1 (3 September 2026).  This is
an attribution-only revision of Version 1.0; the author is identified as an
independent researcher.  A version-specific DOI
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

The post-Phase-32 repair makes the MSS reciprocal boundary non-vacuous:
positive-root and degree side conditions are explicit, both lower endpoints
must be strictly positive, and Lean derives those inequalities from the
`256d` geometry before applying the typed MSS result.  It also adds one
all-`n` global theorem and a degree argument proving the paper's literal
"exactly `d`" root count.  The terminal axiom checker now parses complete
multiline summaries and includes a continuation-line custom-axiom mutation.
