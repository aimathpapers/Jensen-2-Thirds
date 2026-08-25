# Phase 20 completion record

Date: 2026-08-15
Historical Phase-20 disposition: Holland dependency firewall implemented; the
candidate theorem remained conditional on the explicit sectorial GORTTW premise

> **Phase-21 supersession (2026-08-16).**  This disposition records the state
> at the end of Phase 20.  Theorem 21B now derives the sectorial premise
> directly from the xi/Mellin integral, and
> `phase21/C48_DOWNSTREAM_DISCHARGE.md` transports it through the fifth/sixth
> derivative interfaces.  A separated Kimi K3 analytic AI pre-review of the
> frozen Phase-24 source subsequently passed A0--A10 with no P0/P1/P2.  The
> available review evidence remains AI-only, not human or peer review.  A
> later user-executed Mathematica 15.0.1 run completed M1--M4 with exact
> matches and breaks the SymPy CAS common mode without changing that review
> classification.

## Mathematical changes

- Holland Theorem 1.1 is excluded from the candidate proof's premises.
- Holland Proposition 2.2 is reproduced self-containedly with its exact
  `epsilon<16`, reality, degree, endpoint, and critical-point hypotheses.
- The saddle-variable branch is proved directly by Rouché.
- The consumed sectorial consequences of Holland Proposition 4.1 are
  reconstructed from a separately named GORTTW premise.
- The factor-eight mismatch between GORTTW (1.1) and (3.1) is explicitly
  corrected and frozen.
- The algebraic radius proof now uses `K_0=max(256,256C_loc^2)`, states the
  reversal convention, and orders all constants noncircularly.

## Formal changes

- `MultiplierStability.lean` checks the exact order-five geometric tail,
  relative-sign transfer, and distinct roots from separated sign-changing
  intervals.
- `ConditionalAssembly.lean` checks the final positive-to-negative scaling
  and an end-to-end theorem conditional on construction of the analytic
  certificate.
- `LeadingSystem.lean` now exposes the sharp uniqueness theorem requiring
  only positivity of the two shape coordinates.
- No analytic source claim is installed as a Lean assumption declaration.

## Verification observed

| Gate | Result |
|---|---|
| Phase 18 exact saddle/Lean replay | PASS |
| Phase 19 shifted `_3F_2`/Lean replay | PASS |
| Phase 20 combined build | PASS: 8,705 jobs |
| `leanchecker` on `Zeta23.Research.JensenWedge` | PASS |
| Phase 20 selected axiom audit | PASS: only `propext`, `Classical.choice`, `Quot.sound` |
| Proof-escape scan | PASS |
| Exact whole-bidisc `H_6` coefficient majorant | PASS: `<10000` |
| Direct recurrence frozen-artifact comparison | PASS |
| Sixth-saddle frozen-artifact comparison | PASS |

## Review status

The two second-round Claude Fable reports found no P0/P1.  Their remaining
corrections are implemented in the Phase-20 source and versioned responses.
They are disclosed AI technical audits, not human or peer review.

At the Phase-20 checkpoint the primary-source audit found one surviving
material dependency: GORTTW's printed complex extension of (3.2) did not
specify the needed sector, branches, holomorphic error, or uniform constants.
Phase 21 has since rederived that statement directly.  The two-thirds wedge
still remains an internal paper claim because the replacement and downstream
adapters have AI-only review, not because GORTTW (3.2) remains a premise.
