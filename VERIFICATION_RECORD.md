
# Curated-repository verification record

The following checks were run on 22 August 2026 as final validation of the
clean publication tree. They concern integrity and reproducibility; they are
not human mathematical review or peer review.

## Repository and packet integrity

- `python3 VERIFY_REPOSITORY.py` — **PASS**, with 978 manifested files,
  allowed hidden paths only, no credential signature, and a clean reviewer ZIP.
- `python3 EVIDENCE/PHASE30_REFEREE_PACKET/VERIFY_BUNDLE.py` — **PASS**, with
  950 files in the curated Phase-30 manifest.
- The reviewer ZIP's internal manifest was independently replayed, and neither
  it nor its nested Phase-30 ZIP contains a `SUBMISSION`, `LAUNCH`, or `GHOST`
  component.
- Text extracted with `pypdf 6.10.0` from all nine PDFs contained no email
  address.

## Manuscripts and ancestry

- `bash EVIDENCE/PHASE30_REFEREE_PACKET/REPRODUCE/VERIFY_ARCHIVE.sh packet`
  — **PASS** for the curated manifest, the 194-commit cryptographic ancestry
  proof back to checkpoint `5f79158f9c6276dd09142edeea279e35b0d58406`, and
  the fixed-epoch Phase-30 manuscript replay.
- The current Version 1.0 main-paper and supplement sources compiled cleanly
  with Tectonic 0.17.0 from the curated source directory.

## Lean

The Lean project was copied to a separate clean temporary directory. Using
the pinned toolchain `leanprover/lean4:v4.33.0-rc2` and Mathlib revision
`51e6992efd06126df61a496bebf8f49482a4e129`:

- `lake exe cache get` — **PASS**.
- `lake build Zeta23.Research.JensenWedge` — **PASS**, 8,833 jobs.
- The Phase-30 terminal `#print axioms` audit — **PASS**; only `propext`,
  `Classical.choice`, and `Quot.sound` occur on the audited surface.
- `lake env leanchecker --fresh
  Zeta23.Research.JensenWedge.XiNaturalMultiplierCertificate` — **PASS**.

The build emitted ordinary style and deprecation warnings but no compilation
error. No `sorry`, `admit`, custom project axiom, or unsafe escape hatch is
claimed on the audited terminal surface.
