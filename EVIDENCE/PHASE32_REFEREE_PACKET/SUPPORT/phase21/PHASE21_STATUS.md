# Phase 21 status: direct C48 sectorial saddle proof

Date: 2026-08-17

Classification: internally complete paper proof; separated Phase-24 analytic
AI pre-review completed with A0--A10 pass and no P0/P1/P2; not human or peer
review

> **Phase-23 update (2026-08-16).**  The analytic and algebraic Claude Opus 5
> AI pre-reviews of the Phase-22 source are archived under `../phase23/`.
> Their five P2 findings and accepted P3 items are repaired, including fixed
> sector/radius constants, the direct imaginary-part bootstrap, the stated
> complex Hermite--Genocchi lemma, the quotient-to-six-coefficient hinge, and
> the provisional Jacobi positivity constant.  Because these are proof edits,
> the repaired freeze is a new candidate.  The earlier R0 verdicts are not
> review of that new tree, and no human or peer review is claimed.

## Completed

- A detailed fail-closed execution, review, repair, freeze, and optional-Lean
  plan is frozen in `C48_GORTTW_SECTOR_EXECUTION_PLAN.md`.
- The official GORZ v2 and GORTTW v3 source chain has been independently
  reconstructed in `GORTTW_MELLIN_SOURCE_RECONSTRUCTION.md`.
- `C48_GORTTW_SECTOR_MILESTONE1.md` proves the elementary exact preliminaries:
  holomorphy of the Mellin moment on the needed half-plane, the parity-correct
  completed-zeta derivative identity, factor-eight normalization, theta-mode
  decomposition, saddle equation, curvature, and leading amplitude.
- `verify_phase21_milestone1.sh` runs the exact pinned-SymPy regression and
  fail-closed documentation checks.
- `C48_LEADING_CONTOUR_LOCALIZATION.md` now gives an internal paper proof of
  the leading-mode sectorial contour and localization lemma.  It shifts the
  `u=Log t` ray horizontally through the published saddle, proves global
  strict log-concavity on that ray, and obtains relative error `O(1/|K_s|)`
  using the signed cubic Gaussian moment.
- `SECTORIAL_CONTOUR_PRIMARY_RESEARCH.md` independently identifies the same
  branch-safe contour and finds no small-sector Stokes or endpoint obstruction.
  It is primary-method research, not a review of the completed proof.
- `verify_phase21_leading_contour.sh` runs the pinned-mpmath complex-sector
  regression and fail-closed proof-surface checks.
- `C48_HIGHER_THETA_MODES.md` proves that all `k>=2` theta modes are
  exponentially smaller on the same shifted contour.
- `C48_XI_COEFFICIENT_ASSEMBLY.md` proves the two-step moment ratio and the
  factor-eight-corrected sectorial Stirling assembly.  Its final relative error
  is `O(log|M|/|M|)`, stronger than the fixed `O(|M|^(-3/4))` target.
- `verify_phase21.sh` runs all exact and numerical Phase-21 regressions in one
  pinned environment and checks the fail-closed theorem surface.

## Review disposition and remaining boundary

The previously external premise `C48-GORTTW-SECTOR` now has an internal
self-contained paper proof across the Phase-21 notes. A separated Kimi K3 /
Moonshot analytic AI pre-review of the immutable Phase-24 packet passed all
eleven gates A0--A10, found no P0/P1/P2, and returned four P3 documentation
findings. Those findings are repaired and dispositioned in Phase 24.

P21.6 has now been replayed through the serial Phase-20 verifier: the
fifth/sixth derivative interfaces, Jensen-wedge Lean target, `leanchecker`,
axiom audit, proof-escape scan, and symbolic artifacts all pass.  The overall
candidate nevertheless remains an internal, non-peer-reviewed result. The
analytic chain is conventional paper mathematics rather than a constructed
Lean certificate, and no human mathematical review has occurred. The later
user-executed Mathematica 15.0.1 M1/M4 reconstruction exactly reproduces the
saddle tower, denominator, and majorant in a second CAS; it does not formalize
the complex-analysis chain or constitute human review.

## Review and formalization

The final analytic and algebraic AI pre-reviews were run against immutable
proof-source commit `8e2781b` using review-history-free packets. The reports
identify the models/providers and are archived in Phase 24. They are
**AI pre-review**; no human or peer review is claimed.

Lean presently checks the finite algebra and conditional assembly.  Lemma S
and the analytic adapters are candidates for later formalization, but their
absence is not obscured and no analytic axiom is accepted as verification.

## Migration checkpoint

The complete pinned Phase-21 symbolic/numerical verifier passed on
2026-08-16.  On the replacement machine, the subsequent serial Phase-20 replay
rebuilt `Zeta23.Research.JensenWedge` successfully (8,705 jobs), and then
completed `leanchecker`, the selected axiom audit, the proof-escape scan, and
all symbolic artifact comparisons with the final marker
`Phase 20 verification PASS`. Exact logs and tool versions are frozen under
`phase22/`; the later Phase-24 serial replay and separated AI review evidence
supersede the former pending-review status.
