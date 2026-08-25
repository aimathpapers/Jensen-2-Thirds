# Phase K reproducibility and mutation infrastructure

Date: 2026-08-17

## Scope

Phase K makes the proof evidence runnable from a committed clone without
inheriting untracked files, a Python virtual environment, or Lean build state.
It does not change the mathematical theorem or upgrade any assurance color.

## Entry point

`reproduce/VERIFY_ALL.sh` provides three serial modes:

- `quick`: metadata, schema and dependency checks; exact interval and frozen
  Mathematica verification; effectivity; manuscript source invariants;
  behavioral mutations; tool and artifact inventory; deterministic Git
  bundle reconstruction.
- `full`: `quick`, followed by Phase 25, Phase 21, and Phase 20, including the
  independent Lean kernel replay.
- `clean`: a fresh local clone with no `.lake`, `.venv`, `AGENTS.md`, or other
  untracked state; pinned Mathlib cache acquisition; then `full`.

## Mathematical behavioral mutations

The Phase-K suite changes derived mathematical data rather than only source
strings. It rejects:

1. reversed inner/outer sector nesting;
2. the wrong simplex mass `1/120`;
3. `2^(2n)` in place of `n!` in the factor-eight coefficient;
4. a branch-coordinate permutation;
5. a center-only contraction certificate;
6. a hypergeometric recurrence sign change on exact rational coefficients;
7. the stale Jacobi preliminary threshold `32`;
8. a fifth-for-sixth localization exponent;
9. an unqualified peer-review claim;
10. an enlarged branch interval escaping the outer box.

Each mutation must violate its mathematical invariant. Source-semantic
mutations from Phases A--I remain in the Phase-25 verifier.

## Environment and independent platform

`ENVIRONMENT_INVENTORY.json` records the macOS/arm64 platform, compiler, Git,
Lean, Lake, pinned Mathlib commit, Python packages, Tectonic, and the
Mathematica version and hashes. `requirements-c48.lock` is the minimal Python
lock used by the verification surface; every accepted wheel or source archive
is SHA-256 pinned.

`.github/workflows/c48-linux-verification.yml` uses the explicit
`ubuntu-24.04` runner label, pins every action by full commit SHA, records the
hosted image identity in the log, disables inherited Lean build caching,
downloads the Mathlib cache for the exact pinned commit, builds the complete
8,719-job headline target, audits the paper-facing theorem axioms, and runs the
exact, interval, behavioral, effectivity, manuscript-mutation, and Arb/ACB
gates. The exhaustive `leanchecker` replay remains required by local
`full` and clean-clone modes: a hosted Ubuntu attempt completed the build but
the runner canceled the silent kernel replay after 19 minutes without a Lean
error. CI is an additional platform check, not the sole release authority.

## Deterministic Git reconstruction

`verify_git_bundle.py` sets `pack.threads=1`, creates the source bundle twice,
requires byte equality, clones it, checks exact `HEAD`, checks ancestry of
`5f79158f9c6276dd09142edeea279e35b0d58406`, and rejects cache, virtual-
environment, and unrelated-agent files. Multithreaded Git packing was
deliberately not used because its delta search may choose different valid pack
representations.

## Current evidence

- `VERIFY_ALL.sh quick`: PASS on local macOS.
- `VERIFY_ALL.sh full`: PASS on local macOS, including the 8,719-job build,
  independent kernel replay, and standard-axiom report.
- `VERIFY_ALL.sh clean`: PASS from a fresh local clone after the infrastructure
  commit, with no inherited `.lake`, `.venv`, or untracked files; it acquired
  the exact Mathlib cache and completed the full serial replay.
- Independent Ubuntu 24.04 workflow: PASS in GitHub Actions run
  [`32106804666`](https://github.com/jsavva/riemann_hypothesis/actions/runs/32106804666)
  at source commit `99d2e753acc40e9d78fb8b08a3051801ece3fbd6`. The full Lean build,
  paper-facing axiom audit, exact and behavioral gates, Arb/ACB comparison,
  proof-escape scan, and checkpoint ancestry all passed.
- An earlier Ubuntu attempt completed the 8,719-job build but the hosted
  runner canceled the silent `leanchecker` process after 19 minutes without a
  Lean diagnostic. Exhaustive `leanchecker` replay is therefore retained in
  local `full` and `clean`; Ubuntu independently rebuilds and audits theorem
  axioms. This limitation is recorded rather than relabeled as a CI kernel
  replay.

No human or peer review is claimed.
