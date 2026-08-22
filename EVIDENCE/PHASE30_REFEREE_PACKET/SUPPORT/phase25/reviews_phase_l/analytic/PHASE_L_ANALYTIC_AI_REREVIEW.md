# Phase L repaired analytic correlated AI re-review

Candidate commit: `6ee1db8fc5789a01bc0297f850c817f55b529be4`  
Required checkpoint: `5f79158f9c6276dd09142edeea279e35b0d58406`  
Review date: 2026-08-18  
Classification: targeted correlated AI re-review; not independent, human, or peer review  
Evidence boundary: only `Jensen_Two_Thirds_Phase25_Repaired_Analytic_AI_Rereview_Packet.zip`, privately extracted

## 1. Overall verdict and release status

**R1 — analytic re-review passes with two P3 cleanup findings. No P0 or P1
remains.**

The repaired candidate closes both earlier theorem-affecting analytic defects:

1. the contour is now correctly parameterized by `u=L_s+r`, `r` real, with
   the exact Jacobian amplitude `e^r`, the correct quadratic sign, and a
   completed-square treatment of the cubic term;
2. the auxiliary moment `M_z`, the exact gamma bridge, `h=Log M_z`, and the
   saddle main term `G_0` are now explicitly defined and used consistently.

The branch-certificate wording is also narrowed to its actual scope, and this
packet correctly labels the work as a correlated re-review. I found no new
P0/P1 regression. On the analytic track, there is no remaining release
blocker. The two P3 items below should be corrected in the next editorial
revision or explicitly deferred.

## 2. Gate-by-gate review

| Gate | Status | Evidence and falsification method |
|---|---|---|
| A0 completed-xi, Mellin, and factor-eight normalization | **PASS** | Rechecked the centered convention, factor eight, `M_z` definition, and exact `gamma(z)=Gamma(z+1)M_z/Gamma(2z+1)` bridge. The repaired definitions at main lines 250-256 are mutually consistent with duplication. |
| A1 sectorial saddle existence, uniqueness, branches, and Q nonvanishing | **PASS** | Rechecked the Rouché disc geometry, legal logarithms, unique zero counted with multiplicity, branch patching, `|r|,|sigma|<=7/50`, and the prior-to-differentiation margin `|1+r-3sigma/4|>=151/200`. No quantifier regression was introduced. |
| A2 contour deformation, connector control, theta-mode tails, and uniformity | **PASS** | The main paper, supplement, and appendix now use `L_s+r`, not `L_s+i v`. From the definitions, `Phi''(L)=-K`, so the repaired direction gives `-Kr^2/2`; the rejected vertical direction gives `+Kv^2/2`. The exact amplitude is `e^r`, and completing the square yields the displayed normalized cubic moment `3/K^2+1/K^3`. Direct clean-room regressions gave `I_1/A=1.00402848` at `s=80` and `1.00288978-4.76e-6 i` at a complex point. Connector and infinite-mode uniformity remain conventional paper proof, not finite-grid inference. |
| A3 implicit derivative tower through order six and chain constants | **PASS** | The manuscript now defines `h=Log M_z`, distinguishes it from `log gamma`, supplies the exact bridge, and defines `G_0`. A custom exact sparse differentiator reconstructed the post-chain sixth coefficient 48. No half-shift is double-counted. |
| A4 H6 denominator, 82-term numerator, box majorant, and sixth derivative bound | **PASS** | Independent standard-library exact differentiation produced denominator `(4+4r-3sigma)^12`, 82 numerator monomials, degree 13, `H_6(0,0)=24`, post-chain 48, and the exact majorant `6422139805764931584036533551104/702576099728137594188684005 = 9140.845821897... < 10000`. The script reads no frozen output. |
| A5 paired polygamma and elementary cube-integral estimates | **PASS** | The repaired residual uses `h=Log M_z` and exactly one `-psi^(5)(n+1/2+z)` term, which pairs with the `D` boundary. Direct series evaluation still gives `n^5 psi^(5)(n+1/2)->24` for the deliberately unpaired term, while the repaired paired combination has the required extra `1/L` scale. The cube FTC signs and boundary pairing are unchanged and coherent. |
| A6 four-parameter C1 branch and quantified box hypotheses | **PASS** | Recalculated the zero `(3,2,16/3,1/3)`, both inverse identities, `||P||_infinity=304/3`, and the ordering margins. The repaired uniqueness elimination uses two independent equations and correctly forces `t=2`. The main text now says the exact ledger checks rational margins and the implication from the analytic inequalities, and explicitly says it does not compute xi-specific residual/Jacobian enclosures. |
| A7 coefficient asymptotic and transfer to Jensen coefficients | **PASS** | The `M_z` bridge makes the coefficient-to-moment transfer explicit; the `F(N+2)` subtraction, sectorial Stirling assembly, and positive scale `S=B R_1` are unchanged. The repaired derivative object is now compatible with the exact Jensen/model quotient. |
| A8 sixth-order interpolation remainder and theorem-sector uniformity | **PASS** | The six zeros, `1/720` simplex mass, convex thickened domain, proportional-sector containment, and `rho^6=K_r^6(Bd)^3` scaling remain valid. The repaired A3/A5 seam now supplies the required sixth derivative without the former extra `O(n^-5)` term. |
| A9 effectivity ledger and finite-range absorption | **PASS** | The exact ledger remains acyclic and keeps `C_B6` and `N_analytic` symbolic. The finite-range constant still makes every below-threshold antecedent empty. No empirical diagnostic is promoted to a theorem premise. |
| A10 final theorem quantifiers and dependence on imported results | **UNCHECKED in external-source part; PASS for internal quantifiers** | The `d>=1,n>=0` quantifiers, low-degree split, eventual analytic threshold, and finite absorption are coherent. Exact primary texts for the classical Jacobi correspondence, MMP v3, and MSS Theorem 1.6 are not included in this analytic packet, so those imported statements were not independently source-audited. No analytic P0/P1 follows from this limitation. |

## 3. Findings

### Finding 1 — P3: two repaired tail paragraphs retain the old variable name

The repaired local coordinate is `r`, but
`JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex:229` and
`c48_detailed_appendices.tex:253` still say “splitting at `|v|=1`.” These
should read `|r|=1`. The surrounding displays and estimates consistently use
`r`, so this is an editorial residue and does not change the proof.

### Finding 2 — P3: the moment-tower derivation sentence is imprecise

After correctly defining `h=Log M_z` and displaying

```text
log gamma(z) = h(z) + log Gamma(z+1) - log Gamma(2z+1),
```

the main manuscript says that total differentiation of `G_main`, the gamma
main term, yields the displayed tower for `h`. Literally, one must first form

```text
log G_main(x) - log Gamma(x+1) + log Gamma(2x+1),
```

or equivalently differentiate the explicitly defined moment saddle term
`G_0` plus its lower-order moment normalizations. The exact bridge and the
subsequent `G_0` definition make the intended operation recoverable and the
result is independently verified, so this is clarity rather than a remaining
theorem gap. The sentence around main lines 460-463 should state the
subtraction explicitly.

## 4. Independent recalculation record

New scripts are under `rereview_scripts/`. Each constructs all mathematical
inputs from definitions and reads **no frozen expected result, candidate JSON,
notebook, ledger, or saved script output**.

| Script | Construction | Result |
|---|---|---|
| `rereview_scripts/recalc_repaired_contour.py` | Builds the Mellin phase, implicit saddle, curvature, Jacobian amplitude, both real and vertical Taylor directions, Gaussian cubic moment, and direct quadrature | Confirms real-horizontal decay, vertical ascent, the exact `3/K^2+1/K^3` cubic moment, and saddle ratios close to one. |
| `rereview_scripts/recalc_repaired_moment_branch.py` | Builds the duplication bridge, polygamma series, limiting branch, Jacobian, and inverse from definitions | Confirms `h=Log M_z` is the correct object, the half-shift is paired exactly once, the branch residual is zero, and `||P||_infinity=304/3`. |
| `rereview_scripts/recalc_repaired_saddle_exact.py` | Custom sparse rational differentiation of the displayed `G_0` using `L'=L/Q` | Reproduces the denominator, 82 terms, degree 13, coefficients 24/48, and the exact whole-box majorant. |

Archive-local checks run:

```text
python3 VERIFY_BUNDLE.py
  PASS Phase-L AI reviewer bundle manifest (91 files)

python3 evidence/ground_zero_work/phase25/branch_interval_certificates.py
  PASS exact branch intervals ...

python3 evidence/ground_zero_work/phase21/check_phase21_notes.py
  PASS: Phase 21 repaired note statements and display delimiters

python3 evidence/ground_zero_work/phase25/verify_phase25_axioms.py
  PASS complete Phase-25 axiom surface: 66 declarations, only accepted foundational axioms
```

All three new scripts compile and run under the available standard-library
Python. The aggregate Phase-21 SymPy/mpmath replay and Arb/ACB suite were not
rerun because this isolated packet does not provide their pinned executable
environment and the available Python lacks those packages. Saved results were
not substituted for independent execution.

## 5. Unchecked claims

- Exact statement/hypothesis fidelity of the imported MMP v3, MSS Theorem 1.6,
  and classical Jacobi results; their primary texts are intentionally absent
  from this analytic packet.
- Uniform contour, connector, and infinite theta-mode estimates beyond the
  displayed paper proof and finite directed regressions; they are not
  kernel-checked.
- A fresh local execution of the frozen Mathematica and Arb/ACB channels.
- A fully numerical value for `C_B6`, `N_analytic`, or `K_final`; only the
  existential dependency and exact finite ledger are established.
- PDF visual fidelity; equations were checked from the supplied TeX sources.

## 6. Earlier-finding disposition and release recommendation

| Earlier finding | Disposition in repaired freeze |
|---|---|
| P1 horizontal contour/sign/amplitude/cubic defect | **Resolved.** `u=L_s+r`, `e^r`, the completed-square moment, real Gaussian domination, and higher-mode `e^(L_s+r)` are now consistent across main paper, supplement, and appendix. |
| P1 `h=log gamma` versus `h=Log M_z` defect | **Resolved.** `M_z`, the exact gamma bridge, the moment logarithm, and the one half-shift term are explicit. Independent recalculation confirms the repaired scale. |
| P2 overstatement of branch interval certificates | **Resolved.** The manuscript now accurately limits the ledger to rational margins and conditional implication arithmetic and attributes the xi-specific inequalities to uniform paper `C1` estimates. |
| P2 separation/blinding mismatch | **Resolved for this workflow.** The packet and prompt explicitly call this a targeted correlated re-review. Prior full reports and author disposition were not supplied or consulted. |
| P3 undefined `G_0` | **Resolved.** `G_0` is defined in main equation `eq:G0-definition` and repeated in the supplement/appendix. |

**Release recommendation:** clear the repaired candidate on the analytic
re-review track. There is **no remaining P0/P1 blocker**. Correct the two P3
items in the next editorial pass or record their explicit deferral. This
recommendation does not certify the separate imported-source, algebraic,
formal, or reproducibility tracks.

## 7. Model, provider, tools, context, conflicts, and correlation

- Model/provider: OpenAI Codex, GPT-5-family model; the exact deployment
  identifier was not exposed.
- Tools: private ZIP extraction, `python3`, `rg`, `sed`, archive-local verifier
  scripts, and three new standard-library clean-room recalculations. No web,
  external repository file, other track, or author disposition was consulted.
- Context: I reviewed the earlier freeze and authored the earlier analytic
  report, so this is explicitly a **correlated AI re-review**, not an
  independent or separated pass.
- Conflicts: no personal, financial, or institutional conflict is known. AI
  review of AI-assisted mathematics carries a material correlated-error risk.
- Candidate evidence was not edited. Only this report and new scripts were
  written in the designated review output directory.

## 8. Review-status disclosure

This is AI review, not human or peer review.
