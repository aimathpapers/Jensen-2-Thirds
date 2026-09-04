# A Two-Thirds Hyperbolicity Wedge for Riemann's Xi-Function

This repository contains the paper, Lean 4 formalization, exact calculations,
and reproducibility record for John Savva's work on Jensen polynomials of
Riemann's xi-function.

The main theorem establishes an absolute constant `K > 0` such that

```text
n^2 log(n+2) >= K d^3
```

implies that the degree-`d` Jensen polynomial based at `n` has exactly `d`
distinct negative real zeros.

This result does **not** prove the Riemann hypothesis and does not locate zeros
of the zeta function.

Version 1.1 (3 September 2026) is an attribution-only revision.  The
mathematical content and frozen Version 1.0 reviewer evidence are unchanged.

Permanent Version 1.1 record: [doi:10.5281/zenodo.22293642](https://doi.org/10.5281/zenodo.22293642).

## Read the work

- [Main paper](PAPERS/JENSEN_TWO_THIRDS_MAIN.pdf)
- [Technical supplement](PAPERS/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf)
- [Reader's synopsis](PAPERS/JENSEN_TWO_THIRDS_READERS_SYNOPSIS.pdf)
- [Expository article](EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_ARTICLE.pdf)
- [Expository front matter and disclosure](EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_FRONT_MATTER.md)
- [Manuscript source](PAPER_SOURCE/)
- [Frozen Version 1.0 reviewer packet](REVIEWER_PACKET/Jensen_Two_Thirds_Reviewer_Packet_v1.0.zip)

## Inspect the evidence

- [Theorem/evidence cross-reference](EVIDENCE/CURRENT_STATUS/THEOREM_EVIDENCE_CROSS_REFERENCE.md)
- [Formal trust boundary](EVIDENCE/CURRENT_STATUS/TRUST_BOUNDARY.md)
- [Phase 33 status](EVIDENCE/CURRENT_STATUS/PHASE33_STATUS.md)
- [Fresh Phase 32 AI-only findings](EVIDENCE/CURRENT_STATUS/PHASE32_FRESH_AI_REVIEW_FINDINGS.md)
- [Phase 33 repair disposition](EVIDENCE/CURRENT_STATUS/PHASE33_REPAIR_DISPOSITION.md)
- [Concrete MMP specialization audit](EVIDENCE/CURRENT_STATUS/MMP_SPECIALIZATION_SOURCE_AUDIT.md)
- [Lean project](EVIDENCE/PHASE33_REFEREE_PACKET/FORMAL/lean-project/)
- [Mathematica and exact computations](EVIDENCE/PHASE33_REFEREE_PACKET/COMPUTATION/)
- [Supporting proof calculations](EVIDENCE/PHASE33_REFEREE_PACKET/SUPPORT/)
- [AI-only review record](EVIDENCE/PHASE33_REFEREE_PACKET/REVIEW/)
- [Reproduction instructions](EVIDENCE/PHASE33_REFEREE_PACKET/REPRODUCE/)
- [Curated-repository verification record](VERIFICATION_RECORD.md)

The concrete global Lean theorem is conditional only on explicitly typed
Jacobi, MMP, and MSS literature inputs. Those general results are not
re-proved from first principles. The MMP input is attached to the two concrete
Jacobi factors, not to the final xi comparison polynomial. The finite-free
identity transports its conclusion to the terminating `_3F_2` model.

Phase 33 repairs a vacuity defect found by fresh AI-only review. The MSS record
now requires positive-root and degree certificates for both factors and
strictly positive interval lower endpoints. Lean derives those endpoint
inequalities from the displayed `B,D >= 256d` geometry before using the typed
MSS result. It also proves exact degree, rules out `d+1` distinct roots, and
performs the analytic-range versus finite-cutoff split in one global theorem.
The final publication audit also corrected Jonathan Holland's first name in
both public-facing explanatory sources and added attribution mutation checks.

## Verification

The curated Phase 33 evidence packet has a complete internal manifest and a
packet-to-source-tree binding. This repository has a separate manifest
covering every committed file except that manifest itself. From the repository
root, run:

```bash
python3 VERIFY_REPOSITORY.py
python3 EVIDENCE/PHASE33_REFEREE_PACKET/VERIFY_BUNDLE.py
python3 EVIDENCE/PHASE33_REFEREE_PACKET/VERIFY_SOURCE_BINDING.py
```

The verifier checks complete manifest coverage, unexpected hidden files,
credential signatures, unsafe ZIP members, required public artifacts, and the
absence of author-only launch and submission material.

## Review and attribution

These papers and the associated Lean 4 formalization were developed with
substantial artificial-intelligence assistance, primarily from **OpenAI
GPT-5.6 Sol Pro**. Additional models assisted with adversarial testing, source
comparison, independent recalculation, and AI-only technical review.
**Wolfram Mathematica 15.0.1** was used in a clean-room computation executed
by the author to check selected symbolic identities and exact algebraic
calculations. Those computations provide independent-CAS corroboration of the
specified calculations; they do not constitute a proof of the entire theorem,
human mathematical review, or peer review. The author directed, reviewed, and
edited the work, authorized the repository changes, and accepts responsibility
for the contents. AI systems are not authors.

The clean-packet Phase 32 review found a P1 formal-vacuity defect, which Phase
33 repairs. A fresh independent AI-only re-review of the repaired candidate
returned no release-blocking finding and two P3 advisories; both advisories are
repaired in the frozen record.


See [PROVENANCE.md](PROVENANCE.md) for source and curation hashes. No
repository-wide license is asserted; the Lean subproject retains its own
included license and notice files.
