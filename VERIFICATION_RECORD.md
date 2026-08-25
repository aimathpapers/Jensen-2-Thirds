
# Curated-repository verification record

The following checks were run on 24 August 2026 as final validation of the
clean publication tree. They concern integrity and reproducibility; they are
not human mathematical review or peer review.

## Repository and packet integrity

- `python3 VERIFY_REPOSITORY.py` — **PASS**, with 998 manifested files,
  allowed hidden paths only, no credential signature, and a clean reviewer ZIP.
- `python3 EVIDENCE/PHASE32_REFEREE_PACKET/VERIFY_BUNDLE.py` — **PASS**, with
  970 files in the curated Phase-32 manifest.
- The reviewer ZIP's internal manifest was independently replayed, and neither
  it nor its nested Phase-32 ZIP contains a `SUBMISSION`, `LAUNCH`, or `GHOST`
  component.
- Text extracted with `pypdf 6.10.0` from all nine PDFs contained no email
  address.

## Manuscripts and ancestry

- `bash EVIDENCE/PHASE32_REFEREE_PACKET/REPRODUCE/VERIFY_ARCHIVE.sh packet`
  — **PASS** for the curated manifest, the 207-commit cryptographic ancestry
  proof back to checkpoint `5f79158f9c6276dd09142edeea279e35b0d58406`, and
  the fixed-epoch Phase-32 manuscript replay.
- The current Version 1.0 main-paper and supplement sources compiled cleanly
  with Tectonic 0.17.0 from the curated source directory.

## Lean

The Lean project was copied to a separate clean temporary directory. Using
the pinned toolchain `leanprover/lean4:v4.33.0-rc2` and Mathlib revision
`51e6992efd06126df61a496bebf8f49482a4e129`:

- `lake exe cache get` — **PASS**.
- `lake build Zeta23.Research.JensenWedge` — **PASS**, 8,833 jobs.
- The Phase-32 MMP/cutoff and Phase-30 terminal `#print axioms` audits —
  **PASS**; only `propext`,
  `Classical.choice`, and `Quot.sound` occur on the audited surface.
- `lake env leanchecker --fresh
  Zeta23.Research.JensenWedge.XiNaturalMultiplierCertificate` — **PASS**.

The Phase-32 source contract and seven semantic mutations also passed. They
reject the wrong Holland attribution, restoration of the former final-function
MMP seam, disconnection of either Jacobi factor, removal of the exact `_3F_2`
transport, and weakening of the finite-cutoff theorem.

The build emitted ordinary style and deprecation warnings but no compilation
error. No `sorry`, `admit`, custom project axiom, or unsafe escape hatch is
claimed on the audited terminal surface.
