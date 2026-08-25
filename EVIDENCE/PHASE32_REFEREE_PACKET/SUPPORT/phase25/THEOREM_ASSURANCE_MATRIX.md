# Phase 25 theorem assurance matrix

Date: 2026-08-17
Machine-readable source: `THEOREM_ASSURANCE_MATRIX.json`

Baseline totals: **5 green, 13 amber, 0 red**.

- **Green** means kernel checked, or supported by a complete paper proof and
  multiple independent channels appropriate to the claim.
- **Amber** means the proof candidate has an explicit formalization or
  external-input boundary scheduled for upgrade.
- **Red** would mean an unresolved correctness gap; no baseline row is red.

The review channel below is separated AI pre-review, not human or peer review.

| ID | Claim | Dependencies | Channels | Baseline | Upgrade | Remaining boundary |
|---|---|---|---|---|---|---|
| T1 | Exact xi/Mellin coefficient identity | — | paper, Lean normalization/adapter, exact CAS, Arb/ACB, high precision, AI review | Amber | Phase I | Lean connects the centered coefficient convention to Mathlib xi and proves the factor-eight implication; the concrete general theta-kernel identity remains paper analysis. |
| T2 | Sectorial saddle branch (Lemma S) | — | paper, Lean finite margins/contraction adapter, Arb Rouché boxes, high precision, AI review | Amber | Phase I | Three complex sample boxes and the generic closed-disc uniqueness implication are certified; concrete whole-disc bounds, full-sector patching, and logarithmic asymptotics remain outside Lean. |
| T3 | Leading-mode contour and Gaussian localization | T2 | paper, Arb/ACB grid, high precision, AI review | Amber | Phase I | Horizontal contour, connector, and central window are enclosed at three points; uniform deformation and cubic cancellation remain paper analysis. |
| T4 | Higher-theta-mode suppression | T2, T3 | paper, Arb/ACB, high precision, AI review | Amber | Phase I | Selected contour modes and full coefficient-integral tails are enclosed; uniform contour summation remains paper analysis. |
| T5 | Sectorial xi-coefficient asymptotic | T1--T4; Stirling | paper, Lean Cauchy transport, Arb/ACB grid, high precision, AI review | Amber | Phase I | Lean transports any uniform holomorphic relative error through every derivative; constructing that error and the fixed-sector Stirling assembly remain paper analysis. |
| T6 | Logarithmic derivatives through order six | T5 | paper, Lean Cauchy transport, SymPy/Mathematica exact, ACB implicit series, high precision, AI review | Green | Phase I | Exact algebra and an independent order-six ACB series agree, and the derivative-error implication is kernel checked; its uniform sectorial input remains upstream in T5. |
| T7 | Quotient-to-six-coefficient adapter | — | paper, Lean | Green | Phase A | Finite adapter complete; analytic quotient construction is downstream. |
| T8 | Elementary C1 cube-integral estimates | T6 | paper, Lean kernel, AI review | Amber | Phase C | Repeated FTC, both Fubini orientations, q=1..4 signs/scales, r=0..2 differentiation, paired/remote terms, and the x/e half-shift are formalized; common-box four-coordinate and xi-side assembly remains. |
| T9 | Positive four-parameter branch | T8 | paper, Lean contraction/box kernel, Mathematica exact, AI review | Amber | Phase E | Exact boxes, inverse norm, Banach existence/local uniqueness, positivity, and `A>B>C>D` are formalized conditional on explicit xi center-residual and whole-box derivative-defect certificates. |
| T10 | Positive/simple Jacobi factors | Jacobi | paper, primary source, Lean adapters, exact CAS, AI review | Amber | Phase F | Transported diagonal and root-to-Gershgorin consequence are formalized; classical root/matrix identification and concrete entry estimates remain external. |
| T11 | Positive/simple finite-free comparison | T10; MMP | paper, primary source, Lean convention/mesh adapters, exact CAS, AI review | Amber | Phase F | Reversal and strict-mesh consequences are formalized; MMP real-root and mesh-monotonicity theorems remain external. |
| T12 | Uniform root and critical-point localization | T10, T11; MSS | paper, primary source, Lean Gershgorin/product/localization, exact CAS, AI review | Amber | Phase F | Constant 8, reciprocal endpoint, product interval, and corrected `C_loc` arithmetic are formalized; concrete entry bounds and MSS Theorem 1.6 remain external. |
| T13 | Shifted hypergeometric recurrence | — | paper, Lean finite producer/ODE/closed forms, SymPy/Mathematica exact, AI review | Green | Phase D | Complete: termination, coefficient ratio, shifted ODE, every derivative order, genuine-polynomial recurrence, and four coefficient matches are kernel checked. |
| T14 | Critical-point derivative radius | T12, T13 | paper, Lean maximum/threshold kernel, exact ledger, CAS, AI review | Amber | Phase E | Phase H fixes `C0=48`, `C1<96`, `K_r=4096`, and an explicit geometry wedge constant; the uniform analytic branch threshold remains in `N_analytic`. |
| T15 | Order-six multiplier defect | T6--T9, T14 | paper, Lean local repeated FTC, exact simplex/constant ledger, AI review | Amber | Phases C/E/I | Lean derives the local Hermite--Genocchi/Newton identity and constant propagation; `C_B6` and `N_analytic` remain named upstream paper-analysis inputs. |
| T16 | Multiplier stability | T15 | paper, Lean, AI review | Green | Phase A | Finite implication complete; analytic hypotheses are supplied by T15. |
| T17 | Positive-to-negative Jensen scaling | T16 | paper, Lean | Green | Phase A | Scaling complete; certificate is supplied upstream. |
| T18 | Main two-thirds wedge | T1--T17 | paper, typed conditional Lean, exact symbolic K ledger, CAS, Arb finite examples, AI review | Amber | Phase E | `K_final` has an exact dependency formula, but concrete xi records plus numerical `C_B6` and `N_analytic` are not constructed. |

## Phase-A disposition

Phase A does not upgrade mathematical claims merely by cataloguing them. Its
purpose is to make drift detectable, prevent hidden dependencies, and give
every later formalization and paper repair one stable theorem identifier.
Colors change only when the corresponding implementation phase passes its
own verification and review gates.
