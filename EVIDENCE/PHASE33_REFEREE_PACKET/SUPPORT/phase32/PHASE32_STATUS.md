# Phase 32 status

Date: 2026-08-24

## Corrections

- Corrected Jonathan Holland's name in the authoritative bibliography and
  comparator metadata.
- Added a hand-checkable appendix deriving the exact two-Jacobi-factor
  finite-free representation of the comparison `_3F_2`, translating its
  parameters to the classical Jacobi range, and applying the exact MMP v3
  positivity and log-mesh propositions.
- Replaced the overbroad `MMPLogMeshInput` on the final xi comparison by
  `MMPFiniteFreeLogMeshInput` on the two concrete Jacobi factors. Lean now
  performs the `_3F_2` transport through its coefficientwise identity.
- Displayed the finite pre-cutoff absorption and formalized it as
  `not_twoThirdsWedge_finiteCutoffAbsorption`. The proof makes the wedge
  antecedent empty; it does not assume unverified low-index hyperbolicity.

## Remaining external boundary

The general classical Jacobi zero/matrix theorem, MMP v3 Propositions
2.7(iii) and 2.17, and MSS Theorem 1.6 remain typed literature inputs. The
project-specific normalization and specialization are now explicit in both
the paper and Lean. No human or peer review is claimed.

## Verification

The following gates passed serially from the repository root:

```bash
C48_PYTHON="$PWD/.venv/bin/python" bash ground_zero_work/phase32/verify_phase32.sh
C48_PYTHON="$PWD/.venv/bin/python" bash ground_zero_work/phase30/verify_phase30.sh
C48_PYTHON="$PWD/.venv/bin/python" bash ground_zero_work/phase21/verify_phase21.sh
```

Phase 32 rejects eight fail-closed source-contract mutations, rebuilds the xi-specific Lean
target, audits its axioms, and performs a fresh kernel replay.  The Phase 30
headline verifier likewise passed its full build, terminal axiom audit, and
fresh replay.  Phase 21 reproduced the exact symbolic and sectorial analytic
checks.  The Phase 20 target rebuild, axiom driver, escape scan, and source
gates also passed; its redundant non-fresh `leanchecker` invocation was
stopped after an extended silent run because the stricter Phase 30
`leanchecker --fresh` on the same target had already completed successfully.

All three maintained PDFs were rebuilt.  Automated text extraction confirms
the corrected Holland attribution and the new MMP/cutoff material on every
surface; every changed page was rendered and visually inspected; the TeX logs
contain no overfull, underfull, or unresolved-reference warnings.
