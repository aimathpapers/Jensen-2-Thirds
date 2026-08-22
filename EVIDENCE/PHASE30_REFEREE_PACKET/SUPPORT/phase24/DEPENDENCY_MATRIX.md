# Phase 24 dependency matrix

Date: 2026-08-16
Policy: every paper-facing external premise has a precise source and an
internal adapter; Holland's main theorem is never a premise

| Paper interface | External input | Exact consumed statement | Local adapter or replacement | Status |
|---|---|---|---|---|
| Riemann xi coefficient integral | Riemann/GORZ/GORTTW printed integral conventions | Mellin representation and coefficient normalization | `phase21/GORTTW_MELLIN_SOURCE_RECONSTRUCTION.md` derives the factor-eight identity | Directly reconstructed |
| Real saddle architecture/main-term comparison | GORZ and GORTTW | Real-axis saddle definitions and printed main term | Phase 21 proves the needed complex-sector theorem independently | Comparison only; not a premise |
| Holland quotient architecture | Holland v1, Lemma 2.1 and Sections 5--10 | Quotient coordinates, comparison-family design, recurrence strategy | Order-six quotient adapter, four-parameter branch, residual, and recurrence are rederived | Architectural/formula source only |
| Holland Theorem 1.1 | Holland v1 | Three-fifths wedge | None | **Not used** |
| Holland Proposition 4.1 | Holland v1 | Sectorial coefficient interface | `phase20/HOLLAND_PROP41_REPROOF.md` plus Theorem 21B | Replaced |
| Holland Lemma 6.1 | Holland v1 | Three-variable parameter branch | Phase 14--15 four-variable/six-match branch | Replaced |
| Holland Lemma 7.3 | Holland v1 | Assembled finite-free localization | Ratio-free Jacobi lemma plus direct MMP/MSS citations | **Not used**; its ratio hypothesis fails here |
| Positive real-rootedness | MMP arXiv v3, Proposition 2.7(iii) | Nonnegative-rooted inputs give nonnegative-rooted convolution | Reversal and scaling adapter in Phase 16 | Hypotheses checked |
| Simplicity | MMP arXiv v3, Proposition 2.17 | Logarithmic mesh does not decrease | Strict mesh of the first Jacobi factor | Hypotheses checked |
| Coarse product interval | MSS published Theorem 1.6 | `maxroot(p x_d q) <= maxroot(p) maxroot(q)` | Reciprocal-polynomial lower endpoint and direct upper endpoint | Hypotheses checked; corrected theorem number |
| Ordered finite-free refinement | MMP arXiv v3, Proposition 2.11 | Interlacing preservation under positive multiplicative convolution | Holland Lemma 7.2 | Not consumed by the coarse candidate proof |
| Jacobi zeros and Jacobi matrix | Szegő, *Orthogonal Polynomials* | Classical Jacobi root location/three-term matrix for parameters greater than `-1` | Ratio-free Gershgorin calculation displayed in Phase 16 | Formula rederived; classical input cited |
| Hermite--Genocchi remainder | Standard divided-difference theorem | Complex line-segment/simplex integral representation | Paper proof plus Lean line-segment FTC, stick-breaking cube, convex-hull theorem, `M/720` estimate, and normalized-remainder adapter | Integral estimate checked; Newton/divided-difference equality still paper mathematics |
| Rouché, Cauchy, Stirling, polygamma bounds | Standard complex analysis | Named classical theorems in stated domains | Domains, branches, and constants proved in Phases 18 and 21 | Conventional proof; selected finite adapters to be formalized |
| Finite sign transfer and final scaling | None beyond Mathlib | Explicit certificate implies distinct negative roots | `Zeta23.Research.JensenWedge` | Kernel checked, conditional on certificate |

The result depending most heavily on Holland is therefore backed up at the
interface level: the candidate imports neither Holland's three-fifths theorem
nor his parameter branch nor his assembled root lemma. The remaining uses
are either cited architecture or formulas that the repository reproduces.
