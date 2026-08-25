# Phase I: bounded analytic Lean feasibility

Date: 2026-08-17

Status: completed within the plan's bounded-scope stop rules. No human or peer
review is claimed.

## Retained formal results

The new `AnalyticAdapters.lean` module imports the repository's existing
Mathlib-backed entire Riemann xi and proves:

1. the centered normalization `w |-> xi(1/2+w)` is entire and even;
2. the paper's coefficient convention is exactly
   `n!/(2n)!` times the `2n`-th centered derivative;
3. the factor-eight coefficient formula follows by exact algebra from the
   typed half-line moment identity `D^(2n) xi_centered(0) = 8 M_n`;
4. a self-map that contracts a closed complex disc has a unique fixed point
   in that disc;
5. a holomorphic relative error bounded by `epsilon` on a disc of radius
   `R` has `n`-th derivative bounded by `n! epsilon/R^n`; and
6. the same statement is exported with the explicit order-six cutoff used by
   the manuscript.

The module also defines `SectorialSaddleCertificate`, a typed and honest
boundary for a concrete saddle branch, its equation, uniqueness, and
nonvanishing curvature.

## Stop-rule findings

### Exact theta/Mellin bridge

Mathlib supplies `completedRiemannZeta`, the entire pole-removed
`completedRiemannZeta0`, their functional equations, and the repository
already constructs the standard entire xi from them. It does not supply the
specific Riemann theta-kernel `omega`, its modular transformation, or the
paper's half-line Mellin identity in a form that makes the general
factor-eight integral theorem a bounded adapter proof. Building that chain
would require a substantial theta/Mellin library and was stopped under I1.

Consequently, Lean now checks the completed-zeta side, coefficient
normalization, and factor-eight implication, but not the concrete premise
that the centered derivative equals eight times the manuscript's kernel
moment.

### Concrete saddle branch

The Banach closed-disc theorem is available and now wrapped in the exact
complex form needed for Lemma S. Instantiating it uniformly for the moving
sectorial saddle would still require a concrete self-map, whole-disc
derivative bounds, overlap compatibility, and logarithmic asymptotics.
Those obligations are comparable in size to the planned Rouche proof, so I2
stops at the reusable contraction theorem and typed certificate.

### Cauchy transport

I3 closes cleanly. Mathlib's higher-order Cauchy estimate directly proves the
nested-domain relative-error derivative bound for every order, hence through
order six. The remaining work is upstream: constructing the uniform
holomorphic relative error on the larger sector.

## Assurance effect

This phase reduces the chance of a normalization, factorial, derivative-order,
or Cauchy-loss transcription error. It does not convert the paper's uniform
theta-kernel contour theorem or full sectorial saddle branch into a Lean
theorem. T1, T2, T3, T4, T5, T15, and T18 therefore remain amber, with their
remaining boundaries narrowed and stated explicitly.
