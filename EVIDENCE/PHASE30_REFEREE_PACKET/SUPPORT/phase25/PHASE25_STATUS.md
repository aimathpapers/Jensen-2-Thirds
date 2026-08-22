# Phase 25 status: autonomous high-confidence campaign

Date: 2026-08-18
Current stage: Phase L closed; Phase M package construction next

## Completed in Phase A

- Replayed Phase 24, Phase 21, and Phase 20 serially on the implementation
  baseline; both 8,710-job Lean builds passed.
- Frozen the implementation baseline, mathematical candidate, required
  checkpoint, Mathlib commit, platform, and tool versions.
- Created a machine-readable T1--T18 assurance matrix with an explicit
  green/amber/red policy and no red baseline claim.
- Created and validated an acyclic proof dependency graph with critical seams
  made fail-closed.
- Created a notation/normalization crosswalk covering the factor eight,
  Jensen sign, saddle chain, comparison parameters, finite-free orientation,
  interpolation mass, radius scale, and review language.
- Inventoried every `O(...)`, uniformity, threshold-escalation, and consumed
  “standard” phrase in the 11-page manuscript.
- Added semantic mutations for dependency deletion/cycles, unsupported
  assurance upgrades, hidden MMP input, fifth-for-sixth exponent changes,
  factor-eight factorial transposition, branch point, and H6 majorant.

## Assurance classification

Baseline: 5 green, 13 amber, 0 red. This is an evidence classification, not a
numerical probability of correctness. Green does not mean human reviewed.
All prior specialist reviews are AI pre-review, not human or peer review.

## Completed in Phase B so far

- Added an explicit six-variable stick-breaking integral with Jacobian
  weights of degrees `5,4,3,2,1`.
- Proved the nested Bochner-integral norm estimate `M/720` in Lean.
- Specialized the integral to seven complex nodes and proved every cube point
  remains in an arbitrary convex set containing those nodes.
- Removed the free `hHG` norm premise from the order-six remainder adapter;
  its bound is now derived from the sixth-derivative integrand.
- Added fail-closed mutations for the simplex mass, Jacobian exponent,
  derivative order, node order, and Newton product.
- Proved differentiation under the six nested complex segment integrals from
  a global derivative tower, using compact domination generated inside Lean.
- Proved the six repeated-FTC Newton factorization and the exact triangular
  simplex mass `1/720` without a divided-difference or integral-equality
  premise.
- Derived the complete `M rho^6 / 720` remainder bound for global complex
  derivative towers.
- Localized differentiation under the integral, every moment-triangle
  derivative, all six Newton factors, and the final remainder estimate to an
  arbitrary open convex analytic domain.
- Separated the open analytic domain from the smaller convex set carrying
  the sixth-derivative bound, matching the geometry used in the paper.
- Replayed Phase 25, Phase 21, and Phase 20 serially after localization. All
  passed; the Phase 20 axiom audit reported only `propext`,
  `Classical.choice`, and `Quot.sound` on the audited headline declarations.

## Phase B disposition

Phase B is complete. The application-ready local theorem has no free
Hermite--Genocchi, divided-difference, Newton-equality, or global-extension
premise. T15 remains amber because its concrete saddle-error derivative
tower, branch construction, parameter box, and radius inequalities are the
upstream T6, T8, T9, and T14 work scheduled for later phases, not because an
interpolation lemma is missing.

## Completed in Phase C

- Added both Fubini orientations for the genuine finite-dimensional unit cube,
  with integrability transported through the measurable `Fin (q+1)` product
  equivalence.
- Proved the reciprocal-kernel shift recursion by an inner fundamental theorem
  of calculus, not a formal series.
- Proved the logarithmic finite-difference identity in every consumed order
  `q=1,2,3,4`, including the exact signs and factorials `-1,1,-2,6`.
- Proved the exact large-argument rescaling `U=s/x` and connected all four
  finite differences to `Phi_q(s,x)`.
- Proved differentiation under the cube integral through `r=2`, the exact
  rising multipliers, uniform derivative bounds, and first-order mean-value
  errors.
- Proved exact segment formulas for `Phi_q` and its first derivative, the
  paired `B-C` divided difference, and the first `w`, `t`, and `delta`
  parameter derivatives.
- Proved quantitative remote-boundary bounds, including the surviving `q=1`
  term and its `alpha` derivative, and the explicit `q*x/e` half-shift bound.
- Added fail-closed mutations for forward orientation, the order-three and
  order-four factorial/sign constants, scaling exponent, remote product,
  half-shift endpoint, and `x/e` orientation.

## Phase C disposition

The finite cube-calculus boundary of T8 is now kernel checked and imported by
the headline module. T8 remains amber rather than being overstated: one
common compact-box four-coordinate sup-norm assembly, and the separate xi
saddle contribution needed by the full `C^1` branch, remain in the Phase-E/I
boundary. No human or peer review is claimed.

## Completed in Phase D

- Defined the terminating `_3F_2` coefficients recursively over exact real
  arithmetic and constructed the genuine finite polynomial.
- Proved the cross-multiplied coefficient ratio under its exact denominator
  hypotheses, termination at degree `d`, and vanishing above the degree.
- Defined shifted Euler operators and proved their coefficient action.
- Derived the generalized hypergeometric Euler ODE coefficientwise from the
  finite polynomial; no CAS identity is imported.
- Proved the shifted ODE for every `0 <= m <= d`.
- Proved the exact derivative-shift coefficient identity and polynomial
  identity for every derivative order through `d`.
- Expanded three shifted Euler operators into scaled derivative jets and
  proved the genuine shifted polynomial satisfies the four-term recurrence.
- Derived the four compact ODE coefficients and proved they equal the existing
  `recurrenceP3,...,recurrenceP0`; the pre-existing closed-form theorems supply
  the expanded forms used by the manuscript.
- Added 2,355 exact rational property checks across 27 deterministic legal
  tuples, without reading repository output as expected values.
- Added fail-closed mutations for the hypergeometric scale, derivative degree,
  Euler constant, zeroth-coefficient sign, and finite-producer connection.

## Phase D disposition

T13's planned assurance upgrade is complete. SymPy and Mathematica are now
independent corroboration of a Lean-produced recurrence, rather than the
producer of a premise. The downstream uniform dominance inequalities remain
T14 work. No human or peer review is claimed.

## Completed in Phase E

- Fixed the analytic gauge coordinate order `(alpha,t,w,delta)`, the exact
  outer rational product box, and a conservative exact inner sup-norm box.
- Proved in Lean that the inner box is contained in the outer box and that the
  latter gives positivity and `A>B>C>D>0` for `0<e<=1/12`.
- Cast the exact Jacobian inverse into the real parameter space, proved its
  row-sum bound `304/3`, and proved the inverse action is injective.
- Introduced separate center-residual and whole-box derivative-defect interval
  certificates. The latter requires a uniform bound at every box point, not a
  numerical center sample.
- Proved the fixed-inverse self-map bound, one-half contraction, Banach fixed
  point existence, zero equivalence, and local uniqueness in the four-
  dimensional sup norm.
- Constructed a `PositiveParameterBranch` from those two exact interval
  certificates and retained its equation, box membership, local uniqueness,
  positivity, and Jacobi ordering consequences.
- Formalized the non-circular constant order: `K_pre=256`,
  `C_loc=12+8*sqrt(6)<32`, and `K_0=262144`, followed by separately typed
  radius and eventual-integer threshold stages.
- Split final analytic data into `XiCoefficientEstimate`,
  `PositiveParameterBranch`, `ComparisonRootCertificate`, and
  `SixthResidualCertificate`, and proved their typed assembly into the
  existing `JensenWedgeCertificate`.
- Added an independent exact-rational branch ledger and fail-closed mutations
  for coordinate order, inverse norm, residual factor, whole-box derivative
  quantifier, contraction, localization constant/threshold, and typed final
  assembly.

## Phase E disposition

The finite quantitative branch implication and certificate builder are
kernel checked. T9 and T18 remain amber: the project does not yet construct
the xi-specific residual/Jacobian interval certificates or the concrete
analytic input records. The remaining hypotheses are now individually named
and mechanically visible. No human or peer review is claimed.

## Completed in Phase F

- Defined the ascending constant-term-one and monic-descending finite-free
  coefficient conventions and proved that fixed-degree reflection commutes
  with the convolution exactly.
- Proved the reciprocal-root zero equivalence and positive interval reversal,
  making the convention bridge used with the cited literature explicit.
- Formalized the transported Jacobi diagonal and off-diagonal entries and
  proved the exact diagonal-displacement identity used in the paper.
- Proved the generic Gershgorin implication with the exact `4+4=8` constant
  from a typed entrywise certificate and a typed root-to-eigenvalue seam.
- Split the MSS use into original and reciprocal maximum-root hypotheses and
  proved the resulting two-sided product interval in Lean.
- Proved the complete product-deviation arithmetic with the corrected
  `C_loc=12+8*sqrt(6)` and no use of Holland's inapplicable ratio hypothesis.
- Formalized strict logarithmic mesh, its scaling invariance, injectivity, and
  the exact MMP-to-distinct-positive-roots output adapter.
- Added 909 independent exact-rational checks and fail-closed semantic
  mutations for signs, normalization, reflection, constant eight, both MSS
  orientations, localization, and strict mesh.

## Phase F disposition

T10--T12 remain amber but their internal convention and consequence layers
are now kernel checked. The remaining inputs are small and named: the
classical Jacobi root/eigenvalue identification and entry estimates, MMP v3's
positive-root/log-mesh theorem, and MSS Theorem 1.6 in the original and
reciprocal orientations. Reimplementing general MMP or MSS theory was stopped
under the plan's bounded-scope rule. Holland's assembled Lemma 7.3 and its
false-on-this-branch ratio hypothesis are not imported. No human or peer
review is claimed.

## Completed in Phase G

- Evaluated the completed-zeta Taylor series directly with `python-flint` and
  enclosed `gamma(0),...,gamma(3)` without binary floating point.
- Independently integrated the positive Riemann `omega` kernel and the two
  Mellin `F` moments, with analytic bounds for every omitted theta mode and
  the complete infinite-`u` tail. Both normalizations overlap the direct
  completed-zeta balls, including the factor eight and the one-half in
  `omega`.
- Certified uniform Rouché inequalities, derivative nonvanishing, and
  `Q != 0` on three small complex parameter boxes at the theorem-sector
  center/boundary grid.
- Enclosed the normalized horizontal contour, central window, endpoint
  connector, and theta modes two and three at three grid points. These are
  explicitly labeled finite-grid regression evidence, not a uniform proof.
- Recomputed the order-two-through-six saddle tower by ACB implicit power
  series, without importing the symbolic derivative formulas.
- Isolated pairwise-disjoint negative-real root boxes for Jensen examples
  `(n,d)=(5,3),(10,4),(20,5)` and added 406 fresh exact rational recurrence
  identities across 64 deterministic tuples.
- Added eleven fail-closed semantic mutations, byte-determinism checks across
  two full runs, and the user-executed clean-room Mathematica M1--M4 hash and
  ledger verification to the Phase-25 gate.

## Phase G disposition

The directed enclosures materially reduce numerical and transcription risk,
but do not change a finite grid into a uniform analytic theorem. T1--T6 and
T18 therefore retain their prior assurance colors. The recorded kernel-tail
and Rouché-box statements are genuine continuum certificates on their stated
domains; the contour and finite-root grids are corroboration. No human or
peer review is claimed.

## Completed in Phase H

- Built an acyclic machine-readable dependency graph for the sector choices,
  Cauchy loss, Jacobi and localization constants, recurrence envelopes,
  derivative radius, `d/n` caps, analytic residual, and finite-range
  absorption.
- Propagated every numerical node with exact integers or rational arithmetic;
  no binary floating point or empirical contraction diagnostic enters the
  theorem constant.
- Chose the explicit safe values `C_0=48`, `C_1<96`, and `K_r=4096`, then
  verified the constant recurrence-neighbor contribution is strictly below
  `1/4`.
- Derived one exact common cap on `d/n` sufficient for the vanishing
  recurrence terms, `B,D>=K_0 d`, and `d+2 rho<=eta n`, followed by the
  explicit (very coarse) integer `K_geometry` forcing that cap from the
  theorem wedge.
- Produced crude exact thresholds for `L_(2n-2)>=12` and `2n-2>=e^12` without
  decimal approximations.
- Propagated the `1/720` simplex mass, six Newton factors, `B<=3n`, and the
  exponential comparison into an exact multiplier of the one unresolved
  sixth-derivative constant.
- Consolidated the remaining paper-analysis boundary into one named constant
  `C_B6` and one named threshold `N_analytic`, and displayed a symbolic
  sufficient `K_final` including finite-range absorption.
- Added twelve semantic mutations preventing threshold regression,
  circular constant order, omission of domain containment, fabrication of
  analytic inputs, or promotion of the illustrative `10.7/L_n` diagnostic.

## Phase H disposition

The finite geometry/radius portion now has a fully explicit, intentionally
unoptimized sufficient constant. A fully numerical theorem constant is not
claimed: it still depends on `C_B6` and `N_analytic`, which summarize the
uniform saddle/branch/error estimates in the conventional paper analysis.
The exact symbolic formula is recorded, so this limitation is visible rather
than hidden behind “sufficiently large.” No human or peer review is claimed.

## Completed in Phase I

- Connected the paper's centered function directly to the repository's
  Mathlib-backed entire Riemann xi and proved its evenness in Lean.
- Defined the exact Jensen coefficient convention as `n!/(2n)!` times the
  `2n`-th centered derivative and proved the Taylor normalization.
- Proved the exact factor-eight coefficient formula from a typed half-line
  moment identity, so the remaining theta-kernel input cannot silently alter
  the factorial or normalization.
- Wrapped Mathlib's Banach theorem as a unique fixed-point theorem for a
  contracting self-map of a closed complex disc.
- Proved Cauchy transport of a uniform holomorphic relative error to every
  derivative with the exact `n! epsilon/R^n` loss and exported the explicit
  through-order-six form used by the paper.
- Added a typed `SectorialSaddleCertificate` boundary naming branch
  holomorphy, the saddle equation, uniqueness, and nonvanishing curvature.
- Added fail-closed mutations for the center, derivative parity, factor eight,
  Cauchy factorial, order-six cutoff, and curvature seam.

## Phase I disposition

The highest-value bounded analytic adapters are now kernel checked. The full
theta/Mellin identity would require developing substantial theta-kernel and
Mellin infrastructure; the concrete moving-sector saddle would require
whole-disc bounds, overlap patching, and logarithmic asymptotics comparable
to the paper's Rouche proof. Those tasks were stopped under the approved
bounded-scope rules. The uniform theta-kernel contour theorem and construction
of the sectorial relative error therefore remain paper analysis, not Lean
theorems. No human or peer review is claimed.

## Completed in Phase J

- Replaced the condensed candidate as the primary scholarly source with a
  self-contained 35-page main paper and a 10-page technical supplement.
- Expanded the proof in theorem order, then added detailed appendices for the
  completed-xi normalization, factor eight, nested sectors, Rouché saddle,
  contour connectors, odd-cubic cancellation, theta modes, the derivative
  tower, paired polygamma estimates, cube calculus, quantitative branch,
  finite-free orientation, Jacobi localization, terminating recurrence,
  first-failure radius, complex Hermite--Genocchi interpolation, effectivity,
  and the formal trust boundary.
- Added a pinned bibliography, a reader-facing T1--T18 theorem/evidence map,
  manuscript build instructions, and a revised proof synopsis and public
  explainer.
- Added a fail-closed manuscript gate that checks displayed normalizations,
  the corrected radius, localization constants, labels, references,
  bibliography keys, review language, PDF page counts, and TeX logs.
- Retained the independent numerical equation regression for the factor-eight
  identity and the critical-point radius and made it part of Phase 25.
- Rendered and visually inspected all 35 main-paper pages and all 10
  supplement pages. The visual pass found and removed two literal missing-
  backslash spacing commands that TeX itself accepted as ordinary text.
- Compiled both PDFs with no unresolved citations or references and no
  overfull, underfull, or other LaTeX warnings.

## Phase J disposition

The publication candidate is now long enough to expose the complete proof
architecture and the load-bearing estimates without forcing a reader through
historical phase notes. The supplement keeps computational and formal audit
material separate from the theorem proof. The synopsis remains a proof map,
not the primary paper. The mathematical assurance colors are unchanged:
expanding prose does not turn the remaining uniform analytic boundaries into
Lean proofs. All available reviews remain AI review, not human or peer
review.

## Completed in Phase K

- Added one serial entry point, `reproduce/VERIFY_ALL.sh`, with `quick`,
  `full`, and genuinely fresh-clone `clean` modes.
- Pinned the minimal Python mathematics environment and recorded the operating
  system, architecture, compiler, Git, Lean, Lake, Mathlib, Tectonic, and
  Wolfram evidence hashes.
- Added ten behavioral mutations that alter derived mathematical data and
  must fail for the intended invariant, rather than merely matching source
  strings.
- Made Git reconstruction byte deterministic with single-threaded packing;
  two bundles are required to match, reconstruct exact `HEAD`, retain the
  checkpoint `5f79158f9c6276dd09142edeea279e35b0d58406` in history, and reject
  caches, virtual environments, and unrelated agent files.
- Replayed `quick`, `full`, and `clean` successfully on macOS. The clean mode
  cloned the committed source without `.lake` or `.venv`, downloaded the
  exact pinned Mathlib cache, rebuilt the 8,719-job target, ran `leanchecker`,
  and then passed Phase 25, Phase 21, and Phase 20 serially.
- Passed independent Ubuntu 24.04 verification in GitHub Actions run
  `32106804666`: an 8,719-job Lean rebuild, paper-facing axiom audit, exact and
  behavioral mathematical gates, Arb/ACB byte comparison, proof-escape scan,
  and checkpoint-ancestry check all passed.
- Recorded the hosted-runner boundary explicitly. An earlier Ubuntu attempt
  rebuilt Lean successfully but the hosted runner canceled silent
  `leanchecker` after 19 minutes without a Lean error; exhaustive kernel
  replay therefore remains a required local `full`/`clean` gate, while Linux
  independently rebuilds and audits the theorem axioms.

## Phase K disposition

Phase K is complete. The candidate is reconstructible from a clean clone and
has passed both local macOS and independent Ubuntu builds. Reproducibility and
mutation evidence reduce environmental, stale-cache, and transcription risk;
they do not change the mathematical assurance colors. No human or peer review
is claimed.

## Phase L initial AI reviews and repair

- Froze candidate `5641348d8ce0aadea5225f31dbb9bb1327778d20` into five
  role-separated analytic, algebraic, Lean, reproducibility, and hostile AI
  packets. Every report and independent script is preserved verbatim.
- The analytic and hostile tracks independently found the same P1 contour
  sign error: the manuscript called `L_s+iv` horizontal, although it is the
  ascent direction. The corrected proof uses `L_s+r`, the `e^r` amplitude,
  and the signed cubic Gaussian moment.
- The analytic track found a second P1 conflating `log gamma` with the
  required `log M_z`. The exact gamma/moment bridge and the correct
  logarithmic object are now explicit.
- The algebraic and hostile tracks independently rejected the local
  first-failure radius narration; all paper surfaces now use the valid global
  normalized-maximum proof already present in Phase 16.
- Corrected the false displayed leading-system elimination, narrowed the
  branch-certificate claim, defined `G_0`, synchronized current theorem
  numbering, and updated stale trust-boundary ledgers.
- Added production-source mutations for all these manuscript seams and a
  deterministic PDF build with fixed `SOURCE_DATE_EPOCH`.
- Corrected the T1--T18 Lean-channel map and T15 producer mapping. A new
  66-declaration axiom driver, parser, and frozen output now cover the complete
  paper-facing Lean surface and report only `propext`, `Classical.choice`, and
  `Quot.sound`.
- Replayed Phase 25, Phase 21, and Phase 20 serially after repair. All passed,
  including exhaustive local `leanchecker` in Phase 20.

## Phase L targeted correlated re-reviews and closure

- Froze deterministic role-specific replacement packets at repaired candidate
  `6ee1db8fc5789a01bc0297f850c817f55b529be4`, with complete manifests and
  explicit correlated-AI classification.
- The analytic, algebraic, Lean, reproducibility, and hostile tracks all found
  no surviving P0/P1. Their reports and independent scripts are preserved
  verbatim; none is described as independent human or peer review.
- Replaced the illegal full-line contour description with the exact Phase-21
  identity: split at `u=1`, translate only the ray in `Re u >= 1`, use
  `r >= 1-Re L`, and extend to the full real Gaussian only as an exponentially
  accurate comparison. Defined `Phi`, `g`, and `I_1=F_1` on every paper
  surface.
- Corrected the two expanded recurrence displays from `B+D+3m+1` to
  `B+D+2m+1`, and corrected `N_elementary` to the ledger's `N_explicit`.
- Removed the stale external `HG` edge from T15 because the local
  Hermite--Genocchi/Newton producer is now derived in Lean. Updated the
  supplement to the 66-declaration Phase-25 axiom audit.
- Repaired the obsolete Phase-24 Hermite--Genocchi release sentinel and added
  source-connected mutations for every new correction.
- Rebuilt both PDFs deterministically and visually inspected the changed
  pages. Phase 25, Phase 24, Phase 21, and Phase 20 then passed serially,
  including the 8,719-job build and exhaustive kernel replay.

The original and repaired review packets remain historical AI-review evidence,
not the final referee archive. Their repository-relative replay limitation is
an explicit Phase-M gate: new packages must pass extraction-only archive-local
rebuilds. Phase L is closed with no unresolved P0/P1. No human or peer review
is claimed.

## Completed in Phase M

- Completed the substantive source freeze at
  `d4207c6a3859ef57addc3107a2598d2ee7d8443a`. Later Phase-M commits are
  confined to package-status and distribution mechanics; each generated
  package prints its exact candidate. The release set contains a navigable
  referee packet, a full audit archive, and five fresh prior-verdict-free
  AI-review packets for analytic, algebraic, Lean, reproducibility, and
  hostile review.
- Added reader-specific entry points, a source index, expected-results guide,
  trust boundary, known-limitations statement, and AI-assistance disclosure.
- Expanded the public explainer into a detailed nontechnical account of the
  Jensen-polynomial strategy, the sixth-order gain, the role of computation
  and Lean, and the limits of the present evidence.
- Built every archive twice from the same commit and required byte-identical
  output. Each archive carries a fail-closed manifest and a blob-free
  cryptographic parent-chain proof retaining checkpoint
  `5f79158f9c6276dd09142edeea279e35b0d58406`.
- Privately extracted every archive, verified its manifest and ancestry,
  rejected added-file and ancestry mutations, and rebuilt both manuscript
  PDFs byte-for-byte using only extraction-local manuscript sources.
- Included a deterministic complete Git history bundle in the full audit
  archive. Its quick gate reconstructed exact candidate `d4207c6` solely from
  that bundle and passed the repository `VERIFY_ALL.sh quick` suite without a
  pre-existing Lake package checkout or network access.
- Recorded external SHA-256 hashes in
  `output/reviewer_packages_phase25/SHA256SUMS.txt`. The full audit ZIP is
  distributed as checked sub-100-MiB parts for GitHub compatibility, together
  with a byte-exact hash-verifying reassembler.

## Phase M disposition

The reviewer-package construction and extraction-local quick replay are
complete. The archives are self-identifying, tamper-evident, role separated,
and explicit about what is kernel checked, computationally reproduced, or
still conventional paper analysis. The audit archive's extraction-local
`full` replay is reserved for Phase N; it is not claimed here. All review in
the package remains AI review, not human or peer review.

## Completed in Phase N

- Passed `reproduce/VERIFY_ALL.sh full` on the release branch, including
  Phase 25, Phase 21, and Phase 20 serially, both full Lean builds, the
  66-declaration axiom audit, and exhaustive `leanchecker`.
- Passed the standalone Phase 24 gate, including exact interval and
  Mathematica evidence, equation regressions, mutations, and formalization.
- Reassembled the committed split audit archive, extracted it privately,
  reconstructed exact candidate `69ab401` solely from the included Git
  bundle, initialized the pinned Mathlib dependency/cache state, and ran the
  complete archive-local full replay to
  `PASS extraction-local audit repository full replay`.
- The first clean replay exposed a stale-cache masking defect: the Phase 25
  component target list omitted the umbrella module imported by its axiom
  driver. Added the umbrella target to the source and archive initialization,
  reproduced the repair in a separate clean clone, regenerated the archives,
  and repeated the entire full replay successfully. The initial failure log is
  retained beside the final PASS log.
- Rendered and visually inspected all 37 main-paper pages and all 11
  supplement pages. No corruption, clipping, broken display, collision, or
  obvious layout anomaly was found.
- Preserved exact logs, hashes, remaining-boundary analysis, and release
  disposition in `PHASE_N_FINAL_HANDOFF.md`.

## Phase N disposition

Phase N is complete. The release artifacts are ready for third-party
circulation, subject to the explicit assurance matrix: five claims are green
and thirteen remain amber because their concrete uniform analytic or imported
theorem interfaces are not fully kernel checked. This campaign does not assign
a numerical correctness probability. All completed review is AI review, not
human or peer review. Merge or broader release remains a user decision.
