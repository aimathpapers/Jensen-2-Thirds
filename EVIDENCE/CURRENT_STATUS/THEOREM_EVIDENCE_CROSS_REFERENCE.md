# Theorem-to-evidence cross-reference

Date: 2026-08-21

This is the current reader-facing rendering of the theorem assurance map. It
incorporates the Phase-28 literal T5 closure, records the Phase-29 local
Palomar submission candidate, and adds the Phase-30 xi-specific multiplier
and headline closure. Official Palomar Comparator/NanoDa replay is pending
and is not claimed.
“Green” and “amber” describe evidence coverage, not a probability of truth
and not human or peer review. A green row may depend on an amber upstream row;
the dependency column and remaining-boundary column are therefore
load-bearing.

| ID | Claim | Main paper | Kernel-checked core | Other evidence | Remaining boundary | Assurance |
|---|---|---|---|---|---|---|
| T1 | Exact xi/Mellin identity | Sections 2, 4; Appendix B | concrete completed-zeta Mellin identity, differentiated log moments, theta/omega conversion, endpoint cancellation, even fold, and factor eight | exact CAS and Arb/ACB | none inside T1 | green |
| T2 | Sectorial saddle branch | Section 5; Appendix C | whole-disc contraction, unique fixed-sector branch, holomorphy, derivative, curvature, and explicit boxes | Arb boxes and high precision | none inside T2 | green |
| T3 | Leading contour and Gaussian | Section 6; Appendix D | legal horizontal-ray deformation, connector, central expansion, Gaussian moments, tails, and uniform relative estimate | contour regressions | none inside T3 | green |
| T4 | Higher theta modes | Section 7; Appendix D | modewise bounds, integral exchange, three-region suppression, infinite sum, and all-mode contour assembly | directed mode checks | none inside T4 | green |
| T5 | Sectorial coefficient asymptotic | Theorem 7.1; Appendices B--E | literal `1/100` proof, `1/200` outer, and closed `1/400` inner sectors; uniform `M -> 2M-2` transport; explicit `R,C`; theta-moment, Gamma/Stirling, holomorphic quotient error, exact factorization, and Cauchy transport through order six (`manuscriptTheoremSevenOne`, `manuscriptPaperRelativeError_derivatives_through_six`) | Arb/ACB and high precision | none inside T5 | green |
| T6 | Derivatives through order six | Section 8; Appendix E | moving-saddle derivative recurrence, H2--H6 tower, 82-term H6 identity, exact whole-bidisc majorant, and xi natural-log decomposition | independent SymPy, user-executed Mathematica, ACB | none inside T6 | green |
| T7 | Four quotients plus two normalizations | Section 9 | exact quotient-to-six-log-coordinates and exponentiation adapters | exact property checks | none | green |
| T8 | Elementary cube estimates | Section 10; Appendix F | Fubini/FTC cube calculus, component derivatives, boundary estimates, whole-box C1 operator, and contraction budgets | semantic mutations | none inside T8 | green |
| T9 | Positive four-parameter branch | Section 11; Appendix F | exact xi residual decomposition, whole-box Jacobian control, explicit cutoff, unique positive ordered branch, actual transformed polynomial, and six matches | rational ledger and Mathematica | none inside T9 | green |
| T10 | Positive simple Jacobi factors | Section 12; Appendix G | concrete factor normalization, scaling, transported intervals, and xi parameter geometry | exact checks and source audit | classical Jacobi root/matrix and entry theorems are typed external inputs | amber |
| T11 | Positive simple finite-free model | Section 12; Appendix G | exact finite-free convolution identity and every convention adapter | source audit | MMP v3 real-root and logarithmic-mesh results are typed external inputs | amber |
| T12 | Root and critical-point localization | Section 12; Appendix G | reciprocal MSS conversion, product interval, complete root-multiset argument, logarithmic-derivative signs, and critical localization | exact checks and source audit | MSS Theorem 1.6 plus the T10/T11 literature inputs | amber |
| T13 | Shifted hypergeometric recurrence | Section 13; Appendix H | finite producer, termination, Euler ODE, derivative shift, four-term recurrence, and closed coefficients | SymPy, Mathematica, and 2,355 exact tests | none | green |
| T14 | Critical-point derivative radius | Section 14; Appendix H | finite attaining maximum, terminal case, coefficient budgets, strict contraction, xi parameter geometry, and literal normalized radius theorem | mutations and exact ledger | theorem consumes the typed T10--T12 root inputs | green, conditional on amber dependencies |
| T15 | Sixth multiplier defect | Section 15; Appendix I | complex six-node FTC/Hermite--Genocchi, simplex mass 1/720, concrete xi multiplier, six exact node values, explicit sixth-residual rate, and uniform `\lvert c_F-1\rvert<1` tube bound | exact CAS and semantic mutations | consumes the T14 radius and earlier analytic chain | green, conditional on T14 |
| T16 | Multiplier stability | Section 16; Appendix I | complete-root factorization, Rolle critical points, natural sign intervals, finite Newton relative-error estimates, and concrete `xiNatural_multiplierIntervalCertificate` | exact and mutation checks | consumes the typed T10--T12 root-input record | green, conditional on amber dependencies |
| T17 | Jensen sign scaling | Section 16 | equality of the actual transformed xi polynomial with the concrete multiplier transform, complete positive-root transfer, and positive-to-negative Jensen scaling | source regression and kernel audit | upstream typed root inputs only | green, conditional on T16 |
| T18 | Main two-thirds wedge | Theorem 1.1; Sections 16--19; Appendix J | concrete `riemannXiJensen_twoThirds_headline`, including low degrees, the explicit wedge, xi multiplier certificate, actual-polynomial identification, and negative-root conclusion | exact CAS, Arb examples, dependency ledger, mutations, and fresh replay | classical Jacobi/MMP/MSS results remain explicitly typed theorem inputs | green, conditional on amber dependencies |

The complete stronger-middle declaration list is
`ground_zero_work/phase26/Phase26Axioms.lean`; its 1,217 declarations use
only Lean’s accepted foundational principles. The three terminal T5
declarations are separately audited by
`ground_zero_work/phase28/Phase28Axioms.lean` and isolated for prospective
Palomar replay by the Phase-29 candidate. Phase 30 separately audits the
xi-specific multiplier and headline declarations and subjects them to
semantic mutation and fresh-kernel replay. The machine-readable current
matrix is `ground_zero_work/phase27/THEOREM_ASSURANCE_MATRIX.json`.
Historical Phase-25 matrices remain immutable evidence of the smaller
surface available at that earlier checkpoint and must not be used as the
current release map.
