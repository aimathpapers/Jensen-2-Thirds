# Phase 24 verification record

Date: 2026-08-17
Execution policy: pinned Python and Lean environments; serial runs only

## First complete replay

| Order | Verifier | Observed result |
|---|---|---|
| 1 | `ground_zero_work/phase24/verify_phase24.sh` | exact interval certificate PASS; ten mutation kills PASS; independent factor-eight and radius equation regressions PASS; `Zeta23.Research.JensenWedge` built in 8,710 jobs; Phase-24 final marker PASS |
| 2 | `ground_zero_work/phase21/verify_phase21.sh` | factor-eight, saddle, contour, wide-angle robustness, imaginary bootstrap, assembly algebra, and complete proof-surface marker PASS |
| 3 | `ground_zero_work/phase20/verify_phase20.sh` | headline Lean build PASS at 8,710 jobs; checker and selected axiom audit PASS; final Phase-20 marker PASS |

The release builder includes machine-captured logs from the final post-freeze
serial replay under `verification_logs/`. This prose record is not a
substitute for those logs.

## Environment facts

- Repository checkpoint `5f79158f9c6276dd09142edeea279e35b0d58406` is
  required to be an ancestor by `release_checks.py`.
- Lean and Mathlib versions are frozen by `lean-toolchain` and
  `lake-manifest.json`.
- Python requirements/locks are included without vendoring `.venv`.
- `.lake`, `.venv`, caches, and temporary render files are excluded.
- The equation regression compares the corrected Mellin display against
  high-precision Taylor coefficients of xi itself and checks the radius scale
  on a fixed legal comparison polynomial. It is transcription evidence, not
  a substitute for the paper proof.
