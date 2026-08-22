# Phase 20 status: Holland dependency firewall

Date: 2026-08-15
Decision: Holland v1 is no longer a black-box theorem dependency

> **Phase-21 supersession (2026-08-16).**  The trust boundary described below
> is the historical Phase-20 boundary.  Theorem 21B now supplies a direct,
> self-contained paper proof of the required sectorial xi-coefficient
> asymptotic.  The replacement is internally discharged but not
> release-cleared: fresh end-to-end adversarial review of the frozen candidate
> remains required, and no human or peer review is claimed.
>
> **Phase-23/24 repair.**  The repaired radius proof uses `K_pre=256`, and
> Phase 24 now retains the derived `C_loc=12+8sqrt(6)<32` with
> `K_0=max(256,256 C_loc^2)`.  The earlier Claude
> Opus 5 reports are AI pre-reviews of the preceding tree; their R0 verdicts
> do not transfer to the repaired candidate.
>
> **Later Phase-24 evidence.**  Separated Kimi K3 and Qwen3.8-Max AI
> pre-reviews of the repaired source completed the analytic and algebraic
> tracks, and a user-executed Mathematica 15.0.1 run returned exact M1--M4
> matches.  Neither is human or peer review, and the Lean theorem remains
> conditional on a concrete xi analytic certificate.

## Completed

1. Holland v1 and GORTTW v3 are frozen by version and SHA-256.
2. The dependency map separates Holland's architecture from actual logical
   inputs.
3. The saddle-variable branch and its sectorial size estimates are proved
   directly by Rouché.
4. The consumed part of Holland Proposition 4.1 is reconstructed from the
   published GORTTW complex saddle input.
5. Holland Proposition 2.2 is reproduced self-containedly with the correct
   `epsilon<16` threshold and all hypotheses.
6. Lean checks the multiplier tail/sign core, interval-root transfer,
   positive-to-negative scaling, and conditional end-to-end assembly.
7. The algebraic second-round correction uses
   `K_0=max(256,256 C_loc^2)` after the provisional positive-interval box,
   and explicitly records finite-free reversal.
8. A post-incorporation source audit corrected two harmless endpoint decimals
   in Lemma S and added a regression at `|N|=e^12` up to angles approaching
   `pi/2`.

## Historical analytic trust boundary

The GORTTW complex-index extension of equation (3.2) is a published but terse
analytic input.  The local reconstruction proves the consequences needed by
the candidate once that input is granted; it does not rederive the full saddle
asymptotic from the xi-kernel integral.

The candidate two-thirds wedge is therefore still an internal, unrefereed
paper claim.  Two Claude Fable adversarial audits are recorded as AI
pre-review, not human or peer review.  No unconditional theorem promotion is
authorized by this phase.

Lemma S itself is not Lean formalized.  Its companion Python program checks
symbolic identities and numerical boundary regressions but is not proof of
Rouche, holomorphic patching, or the sector-uniform estimates.  Lean checks
the downstream finite implication only after an analytic certificate is
supplied.
