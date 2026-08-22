# Phase 25 proof dependency graph

Date: 2026-08-17
Machine-readable source: `PROOF_DEPENDENCY_GRAPH.json`

```mermaid
flowchart TD
  T1["T1 Xi/Mellin identity"] --> T5["T5 Sectorial coefficient theorem"]
  T2["T2 Sectorial saddle"] --> T3["T3 Leading contour"]
  T2 --> T4["T4 Higher theta modes"]
  T3 --> T4
  T2 --> T5
  T3 --> T5
  T4 --> T5
  ST["Fixed-sector Stirling"] --> T5
  T5 --> T6["T6 Derivatives through order six"]
  T6 --> T8["T8 Elementary C1 estimates"]
  T8 --> T9["T9 Positive parameter branch"]
  JAC["Classical Jacobi theory"] --> T10["T10 Positive Jacobi factors"]
  T10 --> T11["T11 Finite-free comparison"]
  MMP["MMP v3"] --> T11
  T10 --> T12["T12 Root localization"]
  T11 --> T12
  MSS["MSS Theorem 1.6"] --> T12
  T12 --> T14["T14 Critical-point radius"]
  T13["T13 Hypergeometric recurrence"] --> T14
  T6 --> T15["T15 Sixth-order defect"]
  T7["T7 Six-match adapter"] --> T15
  T8 --> T15
  T9 --> T15
  T14 --> T15
  T15 --> T16["T16 Multiplier stability"]
  T16 --> T17["T17 Negative-root scaling"]
  T1 --> T18["T18 Two-thirds wedge"]
  T2 --> T18
  T3 --> T18
  T4 --> T18
  T5 --> T18
  T6 --> T18
  T7 --> T18
  T8 --> T18
  T9 --> T18
  T10 --> T18
  T11 --> T18
  T12 --> T18
  T13 --> T18
  T14 --> T18
  T15 --> T18
  T16 --> T18
  T17 --> T18
```

## Critical cut sets

- **Analytic cut:** T1--T6. This is the largest remaining conventional
  complex-analysis surface.
- **Parameter cut:** T8--T9. Phase C and Phase E target its remaining finite
  formalization gaps.
- **External root-theory cut:** T10--T12. Phase F targets the exact adapters
  and narrow special cases rather than recreating all of MMP/MSS.
- **Recurrence cut:** T13--T14. Phase D makes the terminating polynomial the
  Lean source of the recurrence.
- **Interpolation layer:** closed in Phase B. Lean derives the exact six-node
  Newton factorization and `M/720` estimate on an open convex analytic domain,
  with a separate convex bound set. Hermite--Genocchi is therefore not an
  external logical input. T15 remains amber only through its upstream analytic
  and parameter dependencies.
- **Kernel-checked tail:** T16--T17 and the conditional assembly in T18.

The headline theorem cannot be advertised as end-to-end Lean checked until
the xi coefficient sequence constructs the concrete certificate consumed by
T18. Phase I is a bounded feasibility study, not a promise to close the full
analytic cut.
