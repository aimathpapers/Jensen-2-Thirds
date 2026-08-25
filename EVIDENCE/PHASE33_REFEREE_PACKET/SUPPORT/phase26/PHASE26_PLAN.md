# Phase 26 staged analytic formalization plan

Date: 2026-08-18

This phase implements the formalization order approved by the author:

1. exact algebra and concrete certificate instantiation;
2. T1, the exact xi/theta/Mellin identity;
3. T2, the quantitative sectorial saddle branch; and
4. the modular T3--T5 contour, higher-mode, and coefficient chain.

No human or peer review is claimed. A Lean declaration counts as closed only
when its concrete hypotheses are supplied in Lean; a structure containing an
unproved analytic field remains an interface, not an instantiated theorem.

## Stage A: exact algebra and certificate instantiation

### A1. Order-six saddle algebra

- Define the saddle equation, implicit derivative operator, saddle main term,
  and reduced variables in one Lean module.
- Prove the first implicit derivative and the exact differentiated recurrence.
- Kernel-check the derivatives through order six by recurrence.
- Identify the sixth reduced rational function with a fixed degree-thirteen
  numerator and denominator `(4 + 4*r - 3*sigma)^12`.
- Prove the coefficientwise bidisc majorant and the exact rational inequality
  `6422139805764931584036533551104 /
  702576099728137594188684005 < 10000`.
- Export a theorem combining the numerator identity, nonvanishing denominator,
  and whole-bidisc norm bound.

The independent SymPy and user-executed Mathematica derivations remain
separate corroboration. Lean will check the frozen exact identity and bound;
it will not import either CAS output as an axiom.

### A2. Concrete finite certificates

- Instantiate every certificate whose fields are already exact or rational:
  saddle denominator margins, leading-system solution/Jacobian/inverse norm,
  branch boxes, ordering margins, recurrence coefficients, and effectivity
  inequalities.
- Replace records that merely restate exact data with constructors proved from
  the underlying equalities and inequalities.
- Keep xi-dependent residual and whole-box derivative estimates visibly open
  until T1--T5 supply them.

### A3. Verification gates

- Add a dedicated Lean umbrella target and axiom audit.
- Add semantic mutations for denominator sign, reduced-variable orientation,
  chain factor, numerator coefficient, bidisc radius, and strict majorant.
- Require the Phase 26 narrow verifier, then the downstream Phase 25, 24, 21,
  and 20 verifiers in serial order before the stage is frozen.

## Stage B: T1 exact xi/theta/Mellin identity

### B1. Kernel and convergence library

- Define the concrete theta kernel used by the paper.
- Prove termwise differentiability and summability on the required half-line.
- Prove the modular transformation needed to pass between the full and
  half-line integrals.
- Connect that integral to Mathlib's completed zeta/xi normalization.

### B2. Coefficient identity

- Differentiate the centered identity under the integral.
- Use evenness to obtain the half-line factor eight.
- Instantiate `centeredXiCoefficient_eq_factorEightMoment` without a remaining
  `hMellin` premise.
- Mutation-test the factorial, exponential half-shift, factor eight, and power
  `2*n`.

T1 is upgraded only after the concrete theorem builds with no custom axioms.

## Stage C: T2 quantitative sectorial saddle

### C1. Fixed sector and branch equation

- Formalize the fixed nested sectors `theta_0 = 1/400` and
  `theta_1 = 1/200`, the comparison center, and the exact saddle equation.
- Choose one proof route—Rouche or a concrete closed-disc contraction—based on
  the smaller Mathlib dependency surface. The route must prove whole-disc
  bounds, not sample-point bounds.

### C2. Uniform branch

- Construct the root for every parameter in the sector.
- Prove uniqueness, overlap compatibility, holomorphy, curvature
  nonvanishing, and the explicit reduced-variable boxes.
- Prove the logarithmic comparison estimates used later by the contour and
  effectivity arguments.
- Construct a concrete `SectorialSaddleCertificate`.

T2 is upgraded only after the generic certificate interface has a concrete
constructor on the paper's full domain.

## Stage D: T3 leading contour and Gaussian localization

- Define the phase, amplitude, legal horizontal ray, rectangular deformation,
  connector, central window, and tails.
- Prove the contour deformation with every boundary segment named.
- Prove quadratic descent, the signed cubic cancellation estimate, amplitude
  control, Gaussian moments, connector decay, and central/tail error bounds.
- Package the result as a leading-mode certificate with explicit constants.

## Stage E: T4 higher theta modes

- Formalize the modewise phases and their comparison with the leading mode.
- Prove a uniform geometric/exponential majorant on the entire fixed sector.
- Justify exchange of sum and contour integral and sum the infinite tail.
- Package a higher-mode suppression certificate consumed by T5.

## Stage F: T5 sectorial coefficient theorem

- Combine the concrete T1 identity, T2 branch, T3 leading mode, and T4 tail.
- Formalize the required fixed-sector Stirling and gamma-ratio bounds.
- Construct the uniform holomorphic relative error on the larger sector.
- Invoke the existing Cauchy transport theorem through order six.
- Instantiate the xi-side logarithmic-derivative and residual records and
  connect them to the final `JensenWedgeAnalyticInputs` constructor wherever
  no external Jacobi/MMP/MSS input is involved.

T5 is upgraded only after the uniform error theorem is concrete. The final
headline theorem will continue to disclose the independent classical
Jacobi/MMP/MSS inputs unless those are separately formalized.

## Stage gates and stop policy

Each stage is committed and pushed separately after its narrow tests pass.
Failures are recorded in `PHASE26_STATUS.md`; interfaces are never relabeled
as completed theorems. A stage may be split into smaller commits, but the
order A, B, C, D, E, F is fixed. No concurrent Lean builds and no dependency
updates are permitted.

