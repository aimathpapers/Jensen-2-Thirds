
# Manuscript source

This directory contains the Version 1.0 scholarly source.

- `JENSEN_TWO_THIRDS_MAIN.tex` is the self-contained main paper.
- `c48_detailed_appendices.tex` supplies the detailed appendices loaded by the
  main paper.
- `JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex` records the formal,
  computational, interval, source-fidelity, and reproducibility details.
- `c48_common.tex` contains shared notation and theorem environments.
- `references.bib` is the version-pinned bibliography.
- `THEOREM_EVIDENCE_CROSS_REFERENCE.md` maps claims T1--T18 to their evidence.

With `tectonic` on `PATH`, build from this directory using an output directory
outside the source tree:

```bash
mkdir -p ../paper-build
tectonic -X compile JENSEN_TWO_THIRDS_MAIN.tex --outdir ../paper-build
tectonic -X compile JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex --outdir ../paper-build
```

The formal endpoint includes the Phase-30 xi-specific multiplier and headline
theorem. The theorem retains explicitly typed Jacobi, MMP, and MSS literature
inputs. All included reviews are AI-only; no human or peer review is claimed.
