# Concrete MMP specialization source audit

Date: 2026-08-24

This is an AI-assisted source-fidelity audit, not human or peer review.

The authoritative source is Martínez-Finkelshtein, Morales, and Perales,
*Real roots of hypergeometric polynomials via finite free convolution*,
[arXiv:2309.10970v3](https://arxiv.org/abs/2309.10970v3). The version is
pinned because the authors corrected finite-free statements between earlier
versions.

The concrete specialization is now displayed in Appendix G of the paper:

1. The two factors are
   `Q_(A,B)^(1) = 2F1(-d,A;B;X/A)` and
   `Q_(C,D)^(D) = 2F1(-d,C;D;DX/C)`.
2. Direct finite coefficient multiplication proves their ascending
   multiplicative finite-free convolution is exactly
   `3F2(-d,A,C;B,D;(D/(AC))X)`.
3. The Jacobi identity translates the two factors to parameters
   `(B-1,A-B-d)` and `(D-1,C-D-d)`. The branch inequalities give both
   entries greater than `-1`, so the classical Jacobi theorem supplies full
   degree and simple positive roots after the displayed positive affine
   rescaling.
4. Fixed-degree reflection converts the project's ascending convention to
   MMP's descending convention and commutes with the convolution.
5. MMP v3 Proposition 2.7(iii) gives nonnegative roots of the convolution;
   constant term one excludes zero.
6. MMP v3 Definition 2.16 and Proposition 2.17 preserve the first factor's
   strict logarithmic mesh, giving simple positive convolution roots for
   degree at least two. Degrees zero and one are treated directly.

The Lean boundary was narrowed at the same time. `MMPFiniteFreeLogMeshInput`
is parameterized by the two concrete factor polynomials and contains their
positive-root/degree hypotheses. It supplies the cited MMP conclusion only
for their `finiteFreeAscending` convolution. Lean's independent
`xiNaturalComparisonPolynomial_eq_finiteFree` theorem then transports those
roots to the actual xi comparison polynomial. The old interface that took
the final `xiNaturalComparisonFunction` directly has been removed.

The general Jacobi and MMP theorems remain explicitly typed literature
inputs; this work formalizes the project-specific specialization, not the
third-party papers from first principles.
