# Known limitations

- The general Jacobi matrix/root theorems, MMP strict-log-mesh theorem, and
  MSS finite-free product-root interval theorem are typed literature inputs,
  not re-proved from first principles in Lean.
- The terminal Lean theorem is stated with the explicit analytic cutoff and
  wedge hypotheses. The passage to the manuscript's no-cutoff existential
  constant uses an elementary empty-antecedent lemma, now kernel checked as
  `not_twoThirdsWedge_finiteCutoffAbsorption`; it does not verify individual
  pre-cutoff Jensen polynomials.
- Official Palomar Comparator/NanoDa replay is pending and is not claimed.
- Mathematica, SymPy, Arb/ACB, mutation testing, and AI review are valuable
  corroboration but are not substitutes for the Lean kernel or independent
  human review.
- No human or peer review is available for this candidate.
