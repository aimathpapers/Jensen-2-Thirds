# Completed Mathematica M1--M4 reconstruction

Date: 2026-08-16
Owner: user-executed Mathematica run using cells supplied interactively by Codex
Status: completed with exact `MATCH` results for M1--M4; second-CAS evidence,
not human or peer review

The decisive symbolic algebra was reconstructed in Mathematica 15.0.1 on
ARM64 without importing repository JSON, Python, SymPy, Lean-generated
expressions, or the frozen numerator. The user entered and executed cells
supplied interactively by Codex. This breaks the SymPy-versus-Mathematica CAS
common mode, but is not independent human mathematical review.

## Clean-room rules used

1. Start from the printed definitions in the unified manuscript and the
   cited primary papers. Do not import JSON, Python, SymPy, Lean-generated
   expressions, or copied rational numerators from this repository.
2. Record the Mathematica version, operating system, notebook hash, and every
   exact input cell. Use exact integers and rationals; do not use machine
   precision to establish an identity.
3. Export both a human-readable notebook/PDF and a plain-text result ledger.
4. Compare outputs only after the independent derivation is complete. A
   discrepancy is a release blocker until explained.

## M1. Saddle derivative tower

- Enter the saddle equation and derive `L'(N)` implicitly.
- Starting from the printed leading saddle main term, compute total
  derivatives through order six without copying repository expressions.
- Reduce orders five and six in `r=1/L`, `sigma=L/N`.
- Confirm the signs and limiting constants `-12` and `48` after the
  `N=2x-2` chain rule.
- Independently reduce the sixth-order denominator and compare only at the
  end with `(4+4r-3sigma)^12` and the archived numerator.

## M2. Shifted hypergeometric differential equation

- Derive the `_3F_2` differential equation from the coefficient ratio.
- Differentiate `m` times by shifting all upper and lower parameters.
- Expand the Euler operators and derive all four recurrence coefficients.
- Compare them with the Lean closed forms and the exact JSON only after
  derivation.
- Test the identity on exact polynomials for all `0 <= m <= d` for several
  integer parameter tuples satisfying the paper hypotheses.

## M3. Four-parameter leading system

- Reconstruct the four limiting residual equations from the manuscript.
- Solve in the positive orthant and verify the unique solution
  `(3,2,16/3,1/3)`.
- Compute the exact Jacobian, determinant `-1/144`, inverse, and infinity norm
  `304/3`.

## M4. Coefficientwise sixth-order majorant

- Starting from the independently produced `H_6`, collect the numerator in
  `r,sigma` and count terms and total degree.
- On `|r|,|sigma| <= 7/50`, compute an exact rational coefficientwise
  majorant and compare it to the repository value only at the end.

## Acceptance record

| Item | Result | Exact terminal evidence |
|---|---|---|
| M1 | `MATCH` | implicit check `0`; post-chain constants `(2,-2,4,-12,48)`; denominator `(4+4r-3sigma)^12` |
| M2 | `MATCH` | cross-multiplied recurrence `0`; four coefficient differences `(0,0,0,0)`; exact polynomial tests pass at degrees 5, 8, 11 for every derivative order |
| M3 | `MATCH` | positive solution `(3,2,16/3,1/3)`; determinant `-1/144`; inverse infinity norm `304/3` |
| M4 | `MATCH` | 82 terms, degree 13, exact majorant `6422139805764931584036533551104/702576099728137594188684005 < 10000` |

All mathematical outputs are exact and the frozen ledger reports
`ExactResultsContainNoMachineReals -> True`. The canonical artifacts, hashes,
method disclosure, and PDF-layout note are recorded under
`mathematica_verification/`. `verify_mathematica_evidence.py` fails closed on
hash, result, or external-input-operation changes.
