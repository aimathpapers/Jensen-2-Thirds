# Phase-L Lean statement-strength and proof-surface adversarial AI review

Candidate proof-source commit: `5641348d8ce0aadea5225f31dbb9bb1327778d20`  
Required historical checkpoint: `5f79158f9c6276dd09142edeea279e35b0d58406`  
Review date: 2026-08-17  
Review class: separated AI adversarial review; not human or peer review

## 1. Overall verdict

**R2 — material, repairable release blockers; no P0 or P1 theorem falsification found.**

I use `R0` for no findings, `R1` for editorial-only findings, `R2` for
material but nonfatal/reparable findings that block the requested gate, and
`R3` for a fatal theorem or trust-boundary failure. The supplied Lean source
is notably candid about its conditional boundary, and the inspected producer
proofs have appropriately strong hypotheses. However, the paper-facing
machine ledger does not consistently identify the Lean channel, its T15
mapping selects the assumption-bearing adapter rather than the stronger
producer theorem, and the packet cannot independently substantiate the
claimed axiom surface. Therefore L0 fails and L8 remains unchecked.

The packet manifest verified both before and after review:

```text
PASS Phase-L AI reviewer bundle manifest (60 files)
```

## 2. Gate-by-gate audit

| Gate | Result | Evidence and adversarial check | Independent recalculation |
|---|---|---|---|
| L0 every paper-facing formal claim maps to the named Lean theorem | **FAIL** | All 63 unique names in `THEOREM_ASSURANCE_MATRIX.json` exist in the supplied sources, but the channel/mapping semantics drift. T2 and T5 name Lean declarations while omitting `lean_kernel`; T3 and T4 claim a `lean_kernel` channel with no named declaration. T15 names `hermiteGenocchiSix_remainder_bound`, whose statement has an explicit `hIntegral` hypothesis, while the actual producer theorems `hermiteGenocchiSix_remainder_bound_of_derivative_tower` and `hermiteGenocchiSix_remainder_bound_on` are not mapped. | `scripts/audit_lean_surface.py` derived the 63-name inventory and four channel conflicts directly from sources and the matrix. It reads no saved expected result. |
| L1 theorem hypotheses are neither omitted nor weakened in prose | **PASS** | The prose preserves the important restrictions: Cauchy transport requires a larger disc/domain and nonvanishing main term; branch uniqueness is local to the certified box; the derivative defect is whole-box; the hypergeometric denominators are discharged by positive parameters; reciprocal reflection uses nonzero roots/degree control; the final theorem is conditional on typed analytic input. I found no source theorem whose load-bearing hypothesis was dropped in the corresponding current manuscript description. | Manual statement comparison, plus exact finite checks in `scripts/recalculate_finite_constants.py`. |
| L2 complex Hermite--Genocchi and quotient adapter are honestly scoped | **PASS** | `QuotientAdapter.lean` proves only second-difference plus two-normalization recovery and exponentiation, and expressly disclaims analytic quotient construction. The complex HG source exposes the weaker `hIntegral` adapter and also contains genuine repeated-FTC producer theorems on global and open convex domains. The manuscript leaves the concrete sixth-derivative bound outside this layer. The T15 mapping defect is recorded under L0 rather than treated as a hidden source assumption. | Source statement/proof inspection; no frozen result used. |
| L3 elementary cube calculus and terminating recurrence are producer proofs | **PASS** | `ElementaryCubeCalculus.lean` constructs Fubini in both orientations, repeated FTC, differentiation under the cube integral, q=1..4 formulas, parameter derivatives, and first-order errors. `TerminatingHypergeometric.lean` defines a finite coefficient recursion/polynomial and derives termination, the Euler ODE, derivative shift, and four-term recurrence with explicit denominator hypotheses; CAS is not a premise. | Exact branch/constant recalculation passed; proof-producer status was assessed from definitions and theorem inputs, not from verifier prose. Independent kernel replay remains L8-UNCHECKED. |
| L4 quantitative branch certificates quantify the whole box | **PASS** | `FourJacobianIntervalCertificate.derivative_defect` and `.differentiable` quantify `∀ y ∈ closedBall center radius`; `fourDimensionalBranch_existsUnique` consumes these quantifiers to obtain a Lipschitz contraction. The residual is correctly a center-only bound and combines with the exact inverse norm to give half-radius displacement. No center-only Jacobian theorem was substituted. | Exact fractions give inverse row norm `304/3`, `(304/3)(3/608)=1/2`, and inner radius `10^-6` below every outer-box margin. This verifies the finite implication, not the existence of an xi-specific interval certificate. |
| L5 finite-free/Jacobi/MSS/MMP inputs are visibly typed assumptions | **PASS** | The trust seams appear as `RatioFreeJacobiInput`, `MSSProductRootInput`, and `MMPLogMeshInput`. The source comments say explicitly that Jacobi root/matrix identification, MSS, and MMP are imported rather than proved. The final `ComparisonRootCertificate` also exposes the roots, ordering, separation, and sign changes consumed by sign transfer. | Manual structure-field audit. External source truth was not checked in this Lean-only packet. |
| L6 analytic adapters do not claim the unformalized contour theorem | **PASS** | `AnalyticAdapters.lean` proves centered xi/evenness, a factor-eight implication from `hMellin`, generic disc contraction, and generic Cauchy transport. `SectorialSaddleCertificate` is a structure requiring a branch/equation/uniqueness/curvature witness; no concrete instance is constructed. The module and manuscript expressly leave the theta moment, moving saddle, contour, sector patching, and mode estimates to paper analysis. | Statement inspection and an adversarial search for concrete certificate constructors/theorems. None was found. |
| L7 no sorry, admit, custom axiom, unsafe, native_decide, or implemented_by escape | **PASS (supplied surface)** | A comment/string-aware scan of all 21 supplied Jensen-wedge Lean files found zero forbidden-token occurrences in executable source. This is stronger than accepting the packet's scanner prose. The packet omits the local transitive import `Zeta23.XiPrime.Defs`, so this PASS is intentionally limited to the supplied Jensen-wedge surface. | `scripts/audit_lean_surface.py`; it scans source text directly and reads no expected PASS log. |
| L8 #print axioms surface uses only standard foundational axioms | **UNCHECKED** | The only bundled driver, `phase20/Phase20Axioms.lean`, contains 40 `#print axioms` commands. Only 27 of the 63 unique declarations credited by the current assurance matrix are directly printed; 36 are not. No generated axiom output is included. An independent `lake build Zeta23.Research.JensenWedge` could not run: Lake attempted to clone Mathlib and failed DNS resolution, and the packet also omits the locally imported `Zeta23/XiPrime/Defs.lean`. Thus neither the printed axiom sets nor a kernel replay can be verified from this packet alone. | The 27/63 coverage comparison is derived by `scripts/audit_lean_surface.py`. The failed build is recorded in Section 4. |
| L9 imported-paper trust boundary and conditional headline are explicit | **PASS** | `conditionalTwoThirdsWedge_jensenPolynomial` requires a certificate for every `(n,d)` satisfying the wedge. `JensenWedgeAnalyticInputs` contains branch, comparison-root, residual, and xi-identification records; no xi instance is provided. The main paper says there is no Lean axiom for the xi asymptotic or main analytic certificate and identifies Jacobi/MMP/MSS as imports. | Manual comparison of `ConditionalAssembly.lean`, `QuantitativeBranch.lean`, `JensenPolynomial.lean`, the main paper, and the supplement. |

## 3. Numbered findings

### 1. P2 — The assurance matrix does not give an exact Lean-channel/theorem map

The machine-readable matrix has four objective channel inconsistencies:

- T2 and T5 have named Lean declarations but omit `lean_kernel` from
  `channels`.
- T3 and T4 include `lean_kernel` in `channels` but have empty
  `lean_declarations` arrays.

There is also a statement-strength mapping error at T15. The named
`hermiteGenocchiSix_remainder_bound` requires the equality
`sixNodeDividedDifference f z = hermiteGenocchiIntegralSix ...` as
`hIntegral`. That theorem is an honest adapter, not by itself the claimed
repeated-FTC producer. The source does contain the stronger producer theorems
`hermiteGenocchiSix_remainder_bound_of_derivative_tower` and
`hermiteGenocchiSix_remainder_bound_on`, but the matrix does not name them.

Impact: a reader following the promised exact theorem map can be sent either
to no theorem or to a theorem with a stronger input than the prose summary
suggests. This does not invalidate the stronger source proof, but it defeats
L0's drift-detection purpose.

Required repair: correct T2--T5 channel metadata, map T15 to the local producer
theorem(s) and Newton identity actually supporting its claimed core, then
regenerate and cross-check both Markdown renderings.

### 2. P2 — The packet cannot establish the current axiom surface

The current matrix credits 63 unique Lean declarations. The bundled
`Phase20Axioms.lean` directly audits only 27 of those names; 36 mapped names,
including the terminating-hypergeometric producer, cube calculus, T15 HG
adapter, concrete Jensen specialization, and several analytic adapters, have
no direct `#print axioms` command in the packet. The packet includes neither
the output of the 40 existing commands nor a self-contained build closure.

The attempted headline build failed before elaboration because Mathlib was
not present and network resolution was unavailable. Independently of that
transport failure, `AnalyticAdapters.lean` imports the local module
`Zeta23.XiPrime.Defs`, which is not present in the 60-file archive. Therefore
the assertion that the audited declarations depend only on `propext`,
`Classical.choice`, and `Quot.sound` cannot be independently checked under the
packet's archive-only rule.

Impact: L8 cannot receive PASS. Static absence of a custom `axiom` command in
the supplied leaf modules is not a substitute for transitive `#print axioms`
output.

Required repair: include the complete local transitive source closure (or an
otherwise independently buildable manifest-verified source bundle), add a
Phase-L axiom driver covering every paper-facing mapped declaration or a
documented sufficient set of downstream closures, and freeze/reproduce the
actual output showing only the accepted foundational axioms.

### 3. P3 — A historical formalization ledger conflicts with the current source without a superseded banner

`phase24/FORMALIZATION_LEDGER.md` says the Newton equality remains an explicit
input and says repeated FTC/differentiation for elementary cube estimates is
not claimed. The current Phase-25 source contains the stronger local HG
producer and the full `ElementaryCubeCalculus.lean` development, while the
current manuscript claims those upgrades. The file is dated Phase 24, so this
is plausibly historical rather than mathematical regression, but it is
included in the review evidence without a conspicuous superseded/current
scope label.

Required repair: mark the Phase-24 ledger as historical/superseded for these
rows or replace it with a current formalization ledger aligned with the
assurance matrix.

## 4. Independent-recalculation and execution record

### Bundle and source checks

- `python3 VERIFY_BUNDLE.py`: PASS, 60 manifest files, executed before review
  and repeated after review.
- `scripts/audit_lean_surface.py`: PASS as a static source audit. It found 21
  Lean files, 314 declarations/definitions, zero executable forbidden-token
  hits, 63 unique matrix-mapped names, and zero mapped names missing from
  source. It independently found the four channel conflicts and the 27/63
  direct axiom-driver coverage.
- `lake --version`: Lake `5.0.0-src+d8b1897`, Lean `4.33.0-rc2`.
- `lake build Zeta23.Research.JensenWedge`: not completed. Lake attempted to
  obtain Mathlib and failed with `Could not resolve host: github.com`. The
  archive also lacks the local `Zeta23.XiPrime.Defs` import needed by
  `AnalyticAdapters.lean`. No build result or axiom output was inferred from
  this failure.

### Exact finite recalculation

`scripts/recalculate_finite_constants.py` uses only Python's exact
`fractions.Fraction` arithmetic and inputs transcribed from displayed
definitions. It reads no repository artifact, frozen result, JSON, PASS log,
or expected data. It independently obtained:

```text
det(J) = -1/144
J*P = I: True
P*J = I: True
absolute row sums(P) = 87, 15, 304/3, 10/3
induced infinity bound = 304/3
(304/3)*(3/608) = 1/2
inner radius is below every outer-box margin: True
min(alpha/e) at displayed endpoints = 30
max(t+w*e) at displayed endpoints = 11/4
min(t-1-delta*e) at displayed endpoints = 103/144
localization threshold = 262144
12+8*sqrt(6) < 32 from sqrt(6)<5/2: True
infinite geometric tail sum_(k>=5) 2^-k = 1/16
```

Neither independent script reads a frozen expected result as expected data.

## 5. Unchecked claims

1. Independent kernel elaboration/build of the supplied Lean modules and the
   actual `#print axioms` output.
2. The contents and axiom status of the omitted local import
   `Zeta23.XiPrime.Defs` and all omitted transitive source dependencies.
3. Construction of the concrete theta-kernel moment identity, moving-sector
   saddle certificate, uniform contour deformation, higher-mode summation,
   and uniform sectorial relative error (T1--T5 analytic boundaries).
4. The xi-specific center-residual and whole-box derivative-defect
   certificates. L4 passes for the Lean quantifiers and conditional theorem;
   this review did not verify that a concrete `G_n` supplies the records.
5. The mathematical truth and convention fidelity of the external Jacobi,
   MMP v3, and MSS inputs; their source texts are not included in this
   Lean-only packet.
6. The concrete uniform constants `C_B6` and `N_analytic`, the assembled
   sixth-derivative input, and construction of a xi-specific
   `JensenWedgeAnalyticInputs` record.
7. Numerical/CAS/Arb claims described by the manuscript whose producer
   scripts and result files are outside this deliberately narrow packet.

## 6. Release recommendation and exact blockers

**Do not mark the Phase-L Lean gate passed or advertise the current packet as
an independently reproduced Lean/axiom audit.** This recommendation is about
the formal-evidence package; I found no P0/P1 demonstration that the paper
theorem is false.

Exact blockers:

1. Repair the T2--T5 channel metadata and the T15 theorem-strength mapping,
   then regenerate the paper-facing theorem maps.
2. Supply a self-contained, manifest-verified transitive Lean source/build
   closure and a current axiom driver/output sufficient for all 63 mapped
   declarations (or explicitly justified downstream closures), and rerun the
   kernel and axiom checks.

The P3 historical-ledger clarification should be repaired before circulation
but is not independently theorem-fatal.

## 7. Model, provider, tools, separation, and conflicts

- **Provider/model:** OpenAI Codex, based on GPT-5. The exact deployment point
  version was not exposed in this session.
- **Tools:** local shell; Python 3 standard library; `unzip`, `rg`, `sed`,
  `nl`, `wc`; the bundled `VERIFY_BUNDLE.py`; Lake/Lean version query and one
  attempted build; and the two independent scripts listed above. No web
  browsing, external source lookup, remote CAS, prior report, or repository
  checkout was used.
- **Context access:** mathematical evidence access was limited to
  `Jensen_Two_Thirds_Phase25_Lean_AI_Review_Packet.zip` extracted in a private
  temporary directory. I did not inspect any repository file outside that
  archive, any earlier review report, any author response, or another review
  track. I had not reviewed an earlier freeze in this task, so this is a
  separated independent pass rather than a correlated re-review.
- **Conflicts:** no personal, financial, or scholarly conflict is known to the
  model. The evidence was selected by the author and the reviewer is an AI
  system supplied by OpenAI; separation limits but does not eliminate
  correlated model or packet-selection risk.
- Candidate evidence was not edited. Only this report and the two scripts in
  the assigned review directory were created.

This is AI review, not human or peer review.
