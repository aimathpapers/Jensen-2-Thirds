# Curated-repository verification record

The checks below concern integrity and reproducibility. They are not human
mathematical review or peer review.

## Version 1.1 attribution revision

Version 1.1 adds prominent AI-assistance disclosures to the main paper,
technical supplement, reader's synopsis, expository article, citation
metadata, and repository entry points.  The mathematical content, Lean source,
computations, and frozen Version 1.0 reviewer evidence are unchanged.  The
original expository PDF is retained byte-for-byte as the Version 1.0 article
body; Version 1.1 places a disclosure cover before it.


## Phase 33 repair and downstream verification

- `ground_zero_work/phase33/verify_phase33.sh` — **PASS**: guarded MSS source
  contract, eight fail-closed source-contract mutations, 8,830-job Lean build,
  fresh kernel replay, complete multiline axiom audit, and rejection of the
  former unguarded negative-endpoint call.
- Three additional attribution source-contract mutations reject regressions in
  the bibliography, public explainer, and magazine-article source.
- `ground_zero_work/phase21/verify_phase21.sh` — **PASS**.
- `ground_zero_work/phase20/verify_phase20.sh` — **PASS**, including the
  8,833-job top-level build and fresh kernel replay.
- Phase 25 metadata, manuscript, interval, effectivity, Mathematica, mutation,
  and reproducibility gates — **PASS** during extracted full-audit replay.

## Formal boundary

The terminal Phase 33 axiom audit covers the guarded MSS call, exact-degree
adapter, no-`d+1` theorem, exact headline, and global exact headline. It reports
only `propext`, `Classical.choice`, and `Quot.sound`. The general Jacobi, MMP,
and MSS results remain explicitly typed literature inputs, not project axioms
and not first-principles reimplementations.

## Packages and provenance

- Original Phase 33 referee packet — 1,004 manifested files, deterministic
  double build, 214-commit ancestry proof, packet/source binding, and
  extraction-local replay of all three PDFs: **PASS**.
- Full audit archive — 2,104 manifested files, bundled Git-tree binding,
  extraction-local quick replay, and byte-exact 28-part reassembly: **PASS**.
- Curated public evidence tree — 1,004 manifested files after removing only
  the recorded author-facing Palomar guide: manifest and source binding
  **PASS**.
- Curated reviewer ZIP — deterministic double build and internal-manifest
  replay: **PASS**.

The private source candidate is
`1a50e490ad4c7a0d2cdd998af00f4bc1836acb62`. Package hashes are recorded in
`RELEASE_METADATA.json`, `PUBLIC_RELEASE_BINDING.json`, and
`EVIDENCE/CURRENT_STATUS/PHASE33_PACKAGE_INDEX.md`.

## Review status

The fresh clean-packet Phase 32 adversarial review was AI-only and found one
P1 formal-vacuity defect, two P2s, and six P3s. Phase 33 addresses those
findings and has passed the automated gates above. The fresh independent
AI-only re-review of the repaired candidate verified every repair, returned
no release-blocking finding, and raised two P3 advisories; both advisories
are repaired in this record. No human or peer review is claimed.

The Version 1.1 disclosures state that the papers and associated Lean 4
formalization were developed with substantial AI assistance, primarily from
OpenAI GPT-5.6 Sol Pro.  Additional models supplied adversarial testing and
AI-only technical review.  Mathematica's stated role is limited to clean-room
computational corroboration of selected symbolic identities and exact
algebraic calculations.
