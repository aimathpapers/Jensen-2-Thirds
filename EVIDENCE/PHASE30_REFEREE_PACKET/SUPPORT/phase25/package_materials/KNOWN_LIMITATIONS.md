# Known limitations and nonclaims

1. **No human review.** The available adversarial reports are AI review, not
   human or peer review. Their correlation with AI-assisted development is
   disclosed.
2. **Partial formalization.** Lean proves a large finite and conditional
   surface, but not the complete theta-kernel, saddle, contour, and xi-specific
   certificate construction.
3. **External theorem boundary.** Jacobi, MMP, MSS, and sectorial Stirling
   inputs remain cited mathematics. The package verifies versions and
   interfaces; it does not re-prove the general theories.
4. **Existential effectivity.** `K_final` is expressed in terms of exact
   finite constants plus `C_B6` and `N_analytic`. No practical numerical
   threshold is claimed.
5. **Finite enclosures are not uniform theorems.** Arb/ACB contour points,
   branch boxes, and Jensen examples are rigorous on their stated domains or
   grids, but do not replace the paper's uniform sector argument.
6. **Computer algebra has a statement boundary.** SymPy and Mathematica agree
   on the derivative tower and other exact algebra, but both can only verify
   the definitions supplied to them. Source-connected equation and mutation
   tests reduce, rather than eliminate, transcription risk.
7. **No measured correctness probability.** The evidence is intentionally
   layered, but it does not justify a numerical claim such as “98% proven.”
8. **No Riemann-hypothesis claim.** The result concerns an asymptotic
   growing-degree region of Jensen polynomials. It neither proves RH nor
   establishes hyperbolicity for every degree and base point.
9. **Third-party source licensing.** Official URLs, exact versions, consumed
   statements, and hashes are supplied in place of unlicensed source PDFs.
10. **External tool prerequisites.** Full replay requires the pinned Lean
    toolchain/Mathlib cache, Python packages, Tectonic, Git, and standard shell
    tools. The package contains locks and exact source, not executables for
    every platform.

Historical Phase-L review packets remain immutable evidence of what reviewers
saw. Their repository-relative replay instructions are not release commands.
The Phase-M referee and audit packages instead provide extraction-local
verification and, in the audit archive, an offline Git history bundle.
