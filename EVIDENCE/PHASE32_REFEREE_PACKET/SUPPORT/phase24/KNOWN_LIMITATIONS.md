# Known limitations and release blockers

1. **No human or peer review.** Two genuinely separated AI pre-reviews now
   cover the analytic and algebraic tracks and found no fatal mathematical
   defect. They remain AI-only evidence and do not substitute for human
   mathematical scrutiny. Their minor documentation findings are tracked in
   `PHASE24_SEPARATED_REVIEW_DISPOSITION.md`.
2. **Conditional end-to-end Lean theorem.** Lean does not yet construct the
   `JensenWedgeCertificate` for the Riemann xi coefficients.
3. **Hermite--Genocchi boundary.** Lean checks complex line-segment FTC, the
   explicit stick-breaking cube, convex-hull containment, the `M/720`
   integral bound, and the order-six product adapter. The Newton equality
   identifying that integral with the recursive divided difference remains a
   paper lemma exposed as `hNewton`; there is no longer a free `hHG` norm
   premise.
4. **Lemma S boundary.** Lean checks the denominator identity and exact norm
   margins. Rouché, branch patching, and uniform logarithmic asymptotics
   remain conventional complex analysis.
5. **Elementary `C^1` boundary.** Lean checks unit-cube volume, denominator,
   reciprocal-power, and uniform integral bounds. The repeated-FTC identity
   and differentiation under every parameter integral remain on paper.
6. **CAS provenance boundary.** The planned Mathematica M1--M4 reconstruction
   has completed with exact matches, breaking the SymPy-versus-Mathematica
   common mode. The user executed cells supplied interactively by Codex, so
   this remains AI-assisted computational evidence rather than independent
   human mathematical review.
7. **Effectivity.** The theorem constant is existential. The proof is
   effective in principle after tracing constants, but the present
   unweighted contraction gives an astronomically large sufficient threshold;
   no computationally useful numerical `K` is claimed.
8. **Primary-source availability.** The MMP published record is cited, while
   the accessible arXiv v3 text is hash-pinned. The paywalled journal PDF was
   not byte-compared.
9. **Publication stop.** The artifact is local and confidential. It has no
   DOI and has not been submitted to arXiv or made available to third parties.
