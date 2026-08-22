# Unified-manuscript theorem inventory

Date: 2026-08-17

The manuscript will use the following dependency order. `Lean finite` means
the exact finite implication is kernel checked; it does not mean that the
analytic hypotheses have already been constructed in Lean.

| ID | Planned statement | Mathematical dependency | Current assurance | Manuscript action |
|---|---|---|---|---|
| T1 | Exact xi/Mellin coefficient identity | Riemann integral, duplication formula | Exact derivation and numerical regression | State and prove |
| T2 | Sectorial saddle branch (Lemma S) | Elementary complex logarithms, Rouché | Full paper proof and regression; finite denominator margins Lean checked | Consolidated; full Rouché step remains paper mathematics |
| T3 | Legal leading-mode contour and Gaussian localization | T2 | Full Phase-21 paper proof | Consolidate |
| T4 | Uniform suppression of higher theta modes | T2--T3 | Full Phase-21 paper proof | Consolidate |
| T5 | Sectorial xi-coefficient asymptotic (Theorem 21B) | T1--T4, Stirling | Full Phase-21 paper proof; separated analytic AI gate passed | State with fixed `theta_0=1/400`, `theta_1=1/200` |
| T6 | Logarithmic derivatives through order six | T5, proportional-disc Cauchy, explicit main term | Paper proof, exact SymPy tower, and exact user-executed Mathematica M1 reconstruction | Consolidate and cite the frozen second-CAS evidence |
| T7 | Quotient-to-six-coefficient adapter | Elementary sequence algebra | Lean kernel checked | Formalized and stated |
| T8 | Elementary `C^1` cube-integral estimates | T6 and elementary reciprocal integrals | Paper proof; unit-cube and reciprocal-kernel bounds Lean checked | Elementary finite core formalized |
| T9 | Exact positive four-parameter branch | T8, contraction mapping | Paper proof; inverse algebra Lean checked; Mathematica M3 exact match | Add rigorous rational interval certificate |
| T10 | Positive/simple Jacobi factors | Classical Jacobi theory | Source and hypotheses checked | State precisely |
| T11 | Positive/simple finite-free comparison polynomial | T10, MMP 2.7(iii), MMP 2.17 | Direct source audit and separated algebraic AI gate passed | State with reversal adapter and pinned `lmesh>=1` convention |
| T12 | Uniform root and critical-point localization | T10--T11, MSS 1.6, Gershgorin | Paper proof; source seam corrected | State self-contained interval lemma |
| T13 | Shifted hypergeometric recurrence | Hypergeometric ODE | Exact producer, Lean closed forms, separated algebraic recalculation, and Mathematica M2 exact match | Print all four readable coefficient decompositions and cite the frozen second-CAS evidence |
| T14 | Critical-point derivative radius | T12--T13 | Paper proof plus Lean maximum implication | Consolidate |
| T15 | Order-six multiplier defect | T6--T9, T14, complex Hermite--Genocchi | Paper proof; line-segment FTC, stick-breaking convex-hull integral, exact `M/720` bound, and normalized remainder adapter Lean checked | Newton/divided-difference equality remains a disclosed Lean gap |
| T16 | Multiplier stability | T15 | Self-contained proof; Lean finite sign transfer | State and cross-reference Lean theorem |
| T17 | Positive-to-negative Jensen scaling | T16 | Lean finite | State and cross-reference Lean theorem |
| T18 | Main two-thirds wedge | T1--T17 | Conventional proof candidate plus conditional Lean assembly; separated analytic/algebraic AI pre-review; Mathematica M1--M4 exact matches | State honestly; no RH consequence claimed and no human/peer-review claim |

The paper theorem is:

> There exists an absolute constant `K>0` such that, for integers `d>=1`
> and `n>=0`, `n^2 log(n+2) >= K d^3` implies that the degree-`d`
> Jensen polynomial of the Riemann xi coefficients has `d` distinct negative
> real zeros.

Effectivity is existential and unoptimized. The manuscript will not print a
numerical value for `K` unless every eventual threshold is propagated by a
rigorous interval certificate.
