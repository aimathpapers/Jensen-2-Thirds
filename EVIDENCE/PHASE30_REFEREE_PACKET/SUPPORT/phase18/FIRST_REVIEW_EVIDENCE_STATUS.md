# First-review evidence disposition

Date: 2026-08-15  
Policy: corroboration is not promoted beyond the artifacts actually received

## Reproduced locally

| Review item | Local disposition | Evidence |
|---|---|---|
| Saddle coefficients through orders 2--6 form the factorial-sign tower | Exact symbolic `PASS` | `saddle_derivative_tower.py`; frozen JSON gives saddle tower `(1,-1,2,-6,24)` and `h` tower `(2,-2,4,-12,48)` |
| Order-four regression, fifth and sixth rational functions | Exact symbolic `PASS` | `saddle_main_term.py`, `sixth_saddle.py`; the sixth normalized denominator is exactly `(4+4r-3sigma)^12` |
| Limiting system, normalization weights, Jacobian determinant and inverse | Lean-checked `PASS` | `LeadingSystem.lean`, `ElementaryMap.lean`, `TriangularMap.lean`; Phase-18 build, `leanchecker`, and axiom audit |
| Positive-orthant uniqueness of the limiting root | Lean-checked `PASS` | New theorem `sixthOrderLeadingSystem_unique_positive` |
| Positive six-coefficient fits from true theta moments | Numerical `PASS`, not a theorem | Phase-4 two-quadrature scan |
| High-precision branch approaches the formal target | Numerical `PASS`, not a theorem | Phase-6 70-digit scan at `n=100,10^4,10^6` |
| Finite critical-point radius mechanism | Numerical `PASS`, not uniform | Existing 80-digit diagnostic at `n=10^4`, degrees `6,8,10`, with required `K<0.89` |
| Unweighted contraction threshold scale | Exact matrix arithmetic plus reported coefficient | `effectivity_diagnostic.py`; the `10.7` coefficient remains external-reported |

## Reported by the first reviewer but not artifact-reproduced here

The following claims are recorded as `EXTERNAL-REPORTED`, not as locally
verified evidence, because the reviewer supplied conclusions but not scripts,
raw outputs, environment locks, or hashes:

- independent construction of `Phi` and 20-digit validation against zeta and
  gamma evaluations;
- convergence of every effective-saddle offset to a bounded constant;
- the numerical limits `6.4` for `L_n ||G_n(y_*)||` and `10.7` for
  `L_n ||DG_n-DF||`;
- residual zeros at `10^-87` through `10^-126`;
- positive-rootedness and radius constants on the full grid through
  `(n,d)=(3200,24)`.

These are strong corroborating observations.  They do not discharge the
complex analytic lemma, the uniform radius proof, or the `C^1` theorem.

## Artifact request for promotion

To promote an `EXTERNAL-REPORTED` item to independently reproduced evidence,
obtain:

1. source scripts and raw machine-readable outputs;
2. exact dependency versions and interpreter/platform metadata;
3. all precision, quadrature, truncation, and root-certification settings;
4. SHA-256 hashes;
5. an executable command that regenerates each output in a clean temporary
   directory;
6. for any claim called certified, interval or exact error enclosures rather
   than agreement of floating-point methods alone.

## Review classification

The first report is retained as an `R0` technical pre-review.  Its corrections
have been implemented, but it does not count toward either mandatory
independent human audit.

