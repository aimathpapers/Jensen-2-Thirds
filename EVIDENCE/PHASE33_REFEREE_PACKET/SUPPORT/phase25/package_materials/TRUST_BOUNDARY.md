# Trust boundary for the Jensen two-thirds proof candidate

## Claimed paper theorem

The manuscript claims that there is an absolute constant `K > 0` such that,
for integers `n,d >= 1`,

```text
n^2 log(n+2) >= K d^3
```

implies that the degree-`d` Jensen polynomial formed from the centered Taylor
coefficients of Riemann's xi-function has `d` distinct negative real roots.
This is a growing-degree Jensen-polynomial hyperbolicity statement. It is not
the Riemann hypothesis and does not assert that all Jensen polynomials are
hyperbolic.

## Kernel-checked layer

Lean checks the finite and conditional implication layer: normalization
adapters, the quotient-to-six-coefficient argument, local complex repeated
FTC/Hermite--Genocchi with exact mass `1/720`, elementary cube calculus, the
terminating hypergeometric producer and recurrence, quantitative contraction
and interval implications, finite-free convention and root-geometry adapters,
the global-maximum radius implication, multiplier sign transfer, and final
positive-to-negative root scaling.

The complete paper-facing audit covers 66 declarations. Its frozen output
reports only Lean's standard foundational dependencies `propext`,
`Classical.choice`, and `Quot.sound`. There is no custom axiom asserting the xi
asymptotic or the headline theorem.

## Conventional paper-analysis layer

Lean does not construct the xi-specific analytic certificate. The following
remain conventional mathematics in the paper:

- the concrete theta-kernel/Mellin identity in the consumed normalization;
- the uniform Rouch\'e saddle construction and branch patching;
- the legal translated-ray contour deformation and uniform Gaussian tails;
- uniform suppression of higher theta modes;
- fixed-sector Stirling assembly;
- the xi-specific common-box residual and Jacobian bounds;
- construction of the final analytic input record consumed by Lean.

The exact finite constants are propagated in a machine ledger, but the
uniform analytic constant `C_B6` and threshold `N_analytic` remain named
paper-analysis inputs. The theorem is existentially effective, not supplied
with a practical numerical threshold.

## Imported mathematics

The proof also consumes explicitly identified classical or published inputs:
Jacobi root/matrix facts, MMP v3 logarithmic-mesh preservation, MSS published
Theorem 1.6 in original and reciprocal orientations, and fixed-sector complex
Stirling estimates. The package records exact versions, consumed statements,
official retrieval locations, and hashes. It does not redistribute third-party
papers unless permission is known.

## Computational evidence

SymPy and a user-executed clean-room Mathematica notebook independently
reconstruct the decisive symbolic algebra. Arb/ACB, interval certificates,
high-precision contour checks, and finite examples provide additional
corroboration. These calculations test their programmed statements; they are
not substitutes for the uniform paper proof.

## Review status

All reviews currently available for this project are AI reviews. Initial and
targeted correlated analytic, algebraic, Lean, reproducibility, and hostile
reviews are included with their scripts and author dispositions. No human or
peer review is claimed.
