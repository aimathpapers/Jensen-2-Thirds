# Phase L Lean AI correlated re-review

Date: 2026-08-18  
Candidate: `6ee1db8fc5789a01bc0297f850c817f55b529be4`  
Packet: `Jensen_Two_Thirds_Phase25_Repaired_Lean_AI_Rereview_Packet.zip`  
Classification: targeted correlated AI re-review; not independent, human, or peer review

## 1. Overall verdict

**R1 — releasable on the Lean theorem/proof-surface gate, with two nonblocking
P2 metadata/documentation corrections recommended before treating the packet
as final.** For this report, R0 means clean, R1 means no theorem blocker but a
material nonfatal repair remains, R2 means a P1 blocks release, and R3 means a
P0 invalidates the claimed result.

**No P0 or P1 remains in this Lean re-review.** I found no new P0/P1
regression. The repaired T15 producer, complete Phase-25 axiom surface, local
source closure, proof-escape scan, historical banner, and conditional analytic
boundaries all survive re-review. The two P2 findings are conservative/stale
evidence descriptions, not defects in the theorem terms or proofs.

Release recommendation: the candidate Lean proof-source freeze may proceed.
Correct the T15 `HG` dependency tag and the supplement's Phase-20 axiom-report
reference before claiming the evidence map itself is final. There is no exact
P0/P1 blocker.

## 2. Scope and method

I used only a private extraction of the supplied archive. I did not inspect
the surrounding repository, another review track, or an author disposition,
and I did not edit candidate evidence.

Executed checks:

1. `python3 VERIFY_BUNDLE.py`
   - `PASS Phase-L AI reviewer bundle manifest (402 files)`.
2. Archive-local `verify_phase25_axioms.py` against the frozen output
   - `PASS complete Phase-25 axiom surface: 66 declarations, only accepted foundational axioms`.
3. `rereview_scripts/audit_packet.py`
   - exact T1--T18 map, driver/output order, declaration existence, transitive
     local imports, proof escapes, historical banner, and typed boundaries.
4. `rereview_scripts/recalculate_hg.py`
   - independent exact reconstruction of the triangular and stick-breaking
     mass `1/720`, plus an exact six-node Newton/HG identity and bound test.

A fresh kernel replay was attempted with the pinned Lean 4.33.0-rc2 toolchain.
The extracted packet contains no `.lake/packages/mathlib`; `lake env lean`
attempted to obtain pinned Mathlib and stopped at DNS/network denial. I did not
consult a repository cache outside the archive. Thus the report distinguishes
the successfully parsed frozen kernel output from a fresh kernel replay.

## 3. Gate sheet

| Gate | Result | Evidence and falsification method |
|---|---|---|
| L0 paper-facing formal claims map to named Lean theorems | **PASS** | Parsed T1--T18 in exact order. There are 67 claim/declaration incidences and 66 unique declarations; the sole overlap is `relativeError_derivatives_through_six` in T5 and T6. Every mapped declaration is present in the transitive local source closure. T3 and T4 correctly have neither a Lean declaration nor a `lean_kernel` channel. |
| L1 hypotheses are not omitted or weakened in prose | **PASS** | Checked the main boundary hypotheses against theorem terms: T1 retains `hMellin`; T2 retains self-map/contraction inputs; T5 retains a uniform domain error; T9 retains center residual and whole-box derivative defect; T10--T12 retain typed external root-theory inputs; T15 retains derivative tower, convex-domain, node, and sixth-derivative hypotheses; T18 consumes a typed analytic-input record. |
| L2 complex HG and quotient adapter honestly scoped | **PASS** | The quotient theorem consumes four quotient equalities and two normalizations. The repaired HG producer derives the local Newton identity and remainder from a derivative tower; the concrete `E_F^(6)` bound remains outside Lean and is stated as such. |
| L3 cube calculus and recurrence are producer proofs | **PASS** | The mapped surface contains the integral shifts/differentiation/error theorems and the finite `_3F_2` coefficient producer, termination, ODE, arbitrary derivative shift, recurrence, and closed coefficient forms. They are not merely restated result records. |
| L4 quantitative certificates quantify the whole box | **PASS** | `FourJacobianIntervalCertificate.differentiable` and `.derivative_defect` quantify `∀ y ∈ closedBall center radius`; the residual certificate separately controls the center. The Banach theorem consumes both. |
| L5 finite-free/Jacobi/MSS/MMP inputs are typed assumptions | **PASS** | `RatioFreeJacobiInput`, `MMPLogMeshInput`, `MSSProductRootInput`, and comparison-root records expose the imported mathematical inputs rather than introducing axioms. |
| L6 analytic adapters do not claim the missing contour theorem | **PASS** | `AnalyticAdapters` proves the factor-eight implication only from `hMellin`, provides generic contraction/Cauchy adapters, and defines `SectorialSaddleCertificate`; it does not construct the theta-kernel seam, contour, or moving sector branch. |
| L7 no proof escape on the relevant source closure | **PASS** | A comment/string-stripped lexical scan covered the 23-module transitive local closure (30 local import edges) for `sorry`, `admit`, `axiom`, `unsafe`, `native_decide`, and `implemented_by`; no hit occurred. |
| L8 axiom surface uses only foundational axioms | **PASS (frozen output); fresh replay unchecked** | Driver and frozen output cover the same 66 declarations in the same order, with only `propext`, `Classical.choice`, and `Quot.sound`. Fresh replay was unavailable because pinned Mathlib was not present in the archive. |
| L9 imported-paper boundary and conditional headline are explicit | **PASS** | The matrix remains 5 green/13 amber; T3/T4 have no Lean channel; T18 is conditional on `JensenWedgeAnalyticInputs`; `C_B6` and `N_analytic` remain null/symbolic in the effectivity ledger. The stale `HG` dependency tag is Finding 1. |

## 4. Exact T1--T18 channel/declaration map

All declaration names below have prefix
`Zeta23.Research.JensenWedge.`. Channel tokens are reproduced exactly from
`THEOREM_ASSURANCE_MATRIX.json`.

| ID | Exact channels | Exact mapped declarations |
|---|---|---|
| T1 | `paper_proof`, `lean_kernel`, `exact_cas`, `arb_acb`, `high_precision`, `separated_ai_review` | `centeredXi_even`; `centeredXiCoefficient_taylor_normalization`; `centeredXiCoefficient_eq_factorEightMoment` |
| T2 | `paper_proof`, `lean_kernel`, `arb_acb`, `high_precision`, `separated_ai_review` | `saddlePolynomialDenominator_scaled`; `saddle_scaled_factor_ne_zero`; `complexClosedBall_existsUnique_fixedPoint` |
| T3 | `paper_proof`, `arb_acb`, `high_precision`, `separated_ai_review` | — |
| T4 | `paper_proof`, `arb_acb`, `high_precision`, `separated_ai_review` | — |
| T5 | `paper_proof`, `lean_kernel`, `arb_acb`, `high_precision`, `separated_ai_review` | `relativeError_iteratedDeriv_le`; `relativeError_derivatives_through_six` |
| T6 | `paper_proof`, `lean_kernel`, `exact_cas`, `arb_acb`, `high_precision`, `separated_ai_review` | `saddle_reduced_denominator_norm_lower`; `relativeError_derivatives_through_six` |
| T7 | `paper_proof`, `lean_kernel` | `fourQuotients_twoNormalizations_sixCoefficients`; `exp_sixCoefficients_of_log_sixCoefficients` |
| T8 | `paper_proof`, `lean_kernel`, `separated_ai_review` | `unitCube_volume_real`; `integral_unitCube_succ_tail`; `elementaryCubeIntegral_shift_sub`; `elementaryLogFactor_scaled_q1`; `elementaryLogFactor_scaled_q2`; `elementaryLogFactor_scaled_q3`; `elementaryLogFactor_scaled_q4`; `hasDerivAt_elementaryPhi_firstDerivative`; `elementaryPhi_paired_dividedDifference`; `hasDerivAt_elementaryPhi_paired_w`; `hasDerivAt_elementaryPhi_paired_t`; `hasDerivAt_elementaryPhi_boundary_delta`; `elementaryPhiD2_firstOrder_error`; `elementaryPhi_remote_q1_error`; `elementaryPhi_halfShift_div_bound` |
| T9 | `paper_proof`, `lean_kernel`, `exact_cas`, `separated_ai_review` | `leadingJacobian_det`; `leadingJacobian_mul_inv`; `sixthOrderLeadingSystem_unique_of_t_w_pos`; `branchInnerBox_subset_outer`; `gaugeInverseAction_norm_le`; `fourDimensionalBranch_existsUnique`; `PositiveParameterBranch.jacobi_ordering` |
| T10 | `paper_proof`, `primary_source`, `lean_kernel`, `exact_cas`, `separated_ai_review` | `transportedJacobiDiagonal_sub`; `RatioFreeJacobiInput.root_interval` |
| T11 | `paper_proof`, `primary_source`, `lean_kernel`, `exact_cas`, `separated_ai_review` | `reflect_finiteFreeAscending`; `MMPLogMeshInput.hasDistinctPositiveRoots` |
| T12 | `paper_proof`, `primary_source`, `lean_kernel`, `exact_cas`, `separated_ai_review` | `eigenvalue_mem_jacobi_interval`; `MSSProductRootInput.product_interval`; `productDeviation_le_localizationConstant` |
| T13 | `paper_proof`, `lean_kernel`, `exact_cas`, `separated_ai_review` | `terminating3F2Coefficient_ratio_cross`; `terminating3F2_euler_ode`; `iterate_derivative_terminating3F2Polynomial`; `terminating3F2_shifted_fourTerm_recurrence`; `hypergeometricOdeCoefficients_match_directRecurrence`; `recurrenceP3_closed`; `recurrenceP2_closed`; `recurrenceP1_closed`; `recurrenceP0_closed` |
| T14 | `paper_proof`, `lean_kernel`, `exact_cas`, `separated_ai_review` | `dominantMaximum_le_one`; `localizationConstant_lt_32`; `localizationThreshold_eq`; `localization_controls_squared_constant` |
| T15 | `paper_proof`, `lean_kernel`, `separated_ai_review` | `sixNode_newton_identity`; `hermiteGenocchiSix_newton_identityOn`; `hermiteGenocchiSix_remainder_bound_of_derivative_tower`; `hermiteGenocchiSix_remainder_bound_on`; `norm_hermiteGenocchiCubeSix_le`; `norm_hermiteGenocchiIntegralSix_le`; `hermiteGenocchiCubePoint_mem_convex`; `norm_sixNodeProduct_le` |
| T16 | `paper_proof`, `lean_kernel`, `separated_ai_review` | `finiteMultiplierError_lt_one`; `MultiplierIntervalCertificate.actual_hasDistinctPositiveRoots` |
| T17 | `paper_proof`, `lean_kernel` | `JensenWedgeCertificate.target_hasDistinctNegativeRoots` |
| T18 | `paper_proof`, `lean_kernel`, `exact_cas`, `arb_acb`, `separated_ai_review` | `conditionalTwoThirdsWedge_jensenPolynomial`; `JensenWedgeAnalyticInputs.target_hasDistinctNegativeRoots` |

## 5. T15 producer-strength review

The earlier producer-strength problem is repaired.

- `hermiteGenocchiSix_newton_identityOn` derives the six-factor Newton
  identity by repeated local complex FTC on an open convex domain; it does not
  accept a Newton or divided-difference identity.
- `hermiteGenocchiSix_remainder_bound_of_derivative_tower` derives the global
  `M ρ^6 / 720` bound from a derivative tower.
- `hermiteGenocchiSix_remainder_bound_on` is the application-ready local
  version: an open convex analytic domain supplies differentiation, a smaller
  convex subset supplies the sixth-derivative bound, and the theorem derives
  the remainder without a global-extension or HG premise.
- `norm_hermiteGenocchiCubeSix_le` and
  `norm_hermiteGenocchiIntegralSix_le` derive the six nested weights and exact
  simplex mass.

The older auxiliary `hermiteGenocchiSix_remainder_bound` still accepts an
integral equality, but it is no longer the sole or strongest T15 producer and
is not used to justify the repaired producer claim. The mapped application
surface contains the stronger theorems above.

## 6. Numbered findings

### Finding 1 — P2: T15 still carries a stale external `HG` dependency

`THEOREM_ASSURANCE_MATRIX.json` lists `external_inputs: ["HG"]` for T15, and
`PROOF_DEPENDENCY_GRAPH.json`/`.md` draw `HG -> T15`. In the same packet, the
graph prose says the interpolation layer is closed and T15 remains amber only
through upstream analytic/parameter dependencies. The repaired T15 theorem
surface in fact derives the local HG/Newton identity and `M/720` bound.

Impact: conservative underclaim and an internally inconsistent dependency
map; no theorem, axiom, or P0/P1 effect. Repair by removing the `HG` external
edge/tag from T15 (or explicitly redefining it as a non-logical citation
channel rather than a consumed input) and regenerating both graph renderings
and the matrix Markdown.

Evidence locations:

- `evidence/ground_zero_work/phase25/THEOREM_ASSURANCE_MATRIX.json:256`
- `evidence/ground_zero_work/phase25/PROOF_DEPENDENCY_GRAPH.json:3,24`
- `evidence/ground_zero_work/phase25/PROOF_DEPENDENCY_GRAPH.md:32,64-67`

### Finding 2 — P2: supplement points to the incomplete Phase-20 axiom report

The technical supplement says, “The Phase-20 axiom report prints every
audited declaration.” The Phase-20 driver has 40 rows; the repaired complete
surface is the 66-row `Phase25Axioms.lean` plus
`PHASE25_AXIOM_AUDIT.txt`. A reader following the supplement is therefore
sent to an incomplete predecessor even though the correct complete artifact
is present and passes its verifier.

Impact: evidence/reproducibility description error only; no theorem or axiom
effect. Replace “Phase-20” with the Phase-25 driver/frozen audit reference.

Evidence location:

- `manuscript/source/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex:479`

No P0, P1, or P3 finding is reported.

## 7. Independent recalculation record

`recalculate_hg.py` reads no candidate or frozen expected result. It builds
the recurrence

`mass(0,r)=1/(r+1)`, `mass(i+1,r)=mass(i,r+1)/(r+1)`

using exact `Fraction` arithmetic and obtains `mass(5,0)=1/720`. It separately
integrates the six stick-breaking monomial masses as
`1/6·1/5·1/4·1/3·1/2·1=1/720`. It then constructs the polynomial
`c ∏_{j=0}^5 (z-j)`, differentiates it six times exactly, and checks the
six-node Newton/HG identity and `M ρ^6/720` inequality at an internally chosen
rational point. Frozen expected results read: **none**.

`audit_packet.py` is not presented as an independent mathematical
recalculation. It deliberately reads the frozen matrix, driver, output, and
source files to test their mutual consistency and closure.

## 8. Earlier-finding disposition

| Earlier Lean issue named for this re-review | Disposition |
|---|---|
| Exact T1--T18 channel/declaration map | **Substantively closed.** Exact IDs, channels, 67 incidences/66 unique declarations, source existence, and driver order pass. One stale conservative T15 `HG` external tag remains as P2 Finding 1. |
| T15 producer strength | **Closed.** The local derivative-tower producer derives rather than assumes the Newton/HG seam. |
| Complete Phase25Axioms driver/frozen output | **Closed.** Exactly 66 unique declarations in matching order, with only the three accepted foundational axioms. Supplement pointer remains P2 Finding 2. |
| Local `Zeta23.XiPrime.Defs` and transitive local source closure | **Closed.** Root closure contains 23 local modules, including `Zeta23.XiPrime.Defs` and its local dependency `Zeta23.Defs`; no local import is missing. |
| Proof-escape scan | **Closed on the relevant transitive proof surface.** No prohibited token survives comment/string stripping. |
| Historical-ledger banner | **Closed.** Phase-24 ledger begins with a prominent historical/superseded/not-current warning. |
| Honest conditional analytic boundaries | **Closed.** Missing contour, theta, xi branch, root-theory, `C_B6`, `N_analytic`, and final-certificate construction obligations remain explicit. |

## 9. Unchecked claims

1. A fresh Lean build and fresh `#print axioms` replay are unchecked in this
   isolated packet because pinned Mathlib sources/cache are not included and
   network retrieval was unavailable. The frozen output was checked for exact
   66-row coverage and accepted-axiom content.
2. Archive-to-Git-object identity beyond the manifest and the two embedded
   candidate-commit records is unchecked because this reviewer packet does
   not include a Git history bundle. The 402-file archive manifest itself
   passes.

No other gate-sheet claim was left unchecked.

## 10. Reviewer/tool disclosure and separation statement

Reviewer: OpenAI Codex, GPT-5-family AI agent. Tools used: local shell,
Python 3 exact/static scripts, the packet's manifest verifier, and the
packet's axiom-output verifier. No subagents, web search, external repository
files, other review reports, or author disposition were used. Candidate
evidence was not edited.

This reviewer had task-directed knowledge of the earlier Lean findings and
was asked to recheck a repaired freeze. This is therefore a **correlated AI
re-review**, not an independent review. The work itself is AI-assisted, which
is an epistemic correlation and must not be presented as scholarly
independence.

**This is AI review, not human or peer review.**
