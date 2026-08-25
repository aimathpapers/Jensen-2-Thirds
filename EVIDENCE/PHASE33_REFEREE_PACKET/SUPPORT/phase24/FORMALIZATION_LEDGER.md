# Phase 24 formalization ledger

> Historical snapshot.  This ledger records the Phase-24 boundary and is
> superseded for the complex Hermite--Genocchi producer, elementary cube
> calculus, terminating `_3F_2` producer, quantitative branch, finite-free
> adapters, and analytic adapters by the current Phase-25 assurance matrix and
> theorem/evidence cross-reference.  It must not be read as the current formal
> boundary for those rows.

Date: 2026-08-17
Policy: distinguish kernel-checked implications from analytic hypotheses

| Interface | Lean module | What is kernel checked | What is not claimed |
|---|---|---|---|
| Four quotients plus two normalizations | `QuotientAdapter.lean` | Six consecutive coefficient equalities, and the exponentiated version | Construction of the analytic quotient equalities |
| Complex segment calculus | `HermiteGenocchiCube.lean`, `ComplexHermiteGenocchi.lean` | Complex line-segment FTC; six-variable stick-breaking integrand; convex-hull containment; exact `M/720` nested-integral bound; Newton product transfer | The Newton equality identifying the integral with the recursive divided difference is still the explicit `hNewton` input |
| Elementary cube estimates | `ElementaryCubeBounds.lean` | Unit-cube volume one, denominator lower bound, reciprocal-power pointwise bound, uniform-bound-to-integral step | Repeated-FTC identity and differentiation under all integrals |
| Lemma S finite kernel | `SaddleBounds.lean` | Scaled denominator identity, `9/16` nonvanishing margin, `151/50` reduced-denominator margin | Rouché, holomorphic implicit branch, logarithmic asymptotics |
| Concrete Jensen definition | `JensenPolynomial.lean` | Conditional assembly specialized to the actual binomial Jensen polynomial | Construction of the `JensenWedgeCertificate` for xi coefficients |
| Existing finite algebra | `Zeta23.Research.JensenWedge` | Leading system, recurrence closed forms, maximum implication, multiplier sign transfer, negative-root scaling | Analytic estimates named above |

There are no new axioms, `sorry`, `admit`, or unsafe escape hatches in these
modules. A successful build proves only the statements actually declared.

The separate user-executed Mathematica 15.0.1 run reproduces the decisive
symbolic M1--M4 interfaces exactly and breaks the SymPy CAS common mode. It is
computational evidence, not an enlargement of the Lean proof surface and not
human or peer review. Its exact notebook, ledger, PDF, hashes, and provenance
record are frozen under `mathematica_verification/`.
