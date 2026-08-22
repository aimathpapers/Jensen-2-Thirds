# Phase-L algebraic adversarial AI review

Candidate commit: `5641348d8ce0aadea5225f31dbb9bb1327778d20`  
Required checkpoint: `5f79158f9c6276dd09142edeea279e35b0d58406`  
Track: special functions, finite-free algebra, and root geometry  
Review date: 2026-08-17

## 1. Overall verdict

**R2 — major revision required.** I use R2 to mean that there is no demonstrated
fatal counterexample (no P0), but at least one theorem-affecting proof defect
must be repaired before release. The finite hypergeometric algebra, convention
adapters, Hermite--Genocchi constant, and conditional sign-transfer assembly
withstood independent recalculation. The release blockers are:

1. the manuscript's radius proof uses an invalid first-failure inference;
2. the displayed leading-system elimination is algebraically false as labeled;
3. the packet does not include the primary texts needed to independently
   check the Jacobi, MSS, and MMP imports while obeying the packet-only rule.

The first blocker has a plausible, apparently complete repair already present
in the packet: replace the first-failure paragraph by the global normalized
maximum argument in `C48_UNIFORM_RADIUS_PROOF.md` and connect it explicitly to
the recurrence bounds. That repair must appear in the released manuscript,
not merely in supporting notes.

Bundle integrity was checked before review:

```text
PASS Phase-L AI reviewer bundle manifest (95 files)
```

## 2. Gate-by-gate result

| Gate | Status | Evidence inspected | Independent falsification/recalculation |
|---|---|---|---|
| B1 leading system, positive solution, Jacobian, inverse, and norm | **FAIL** | Main §§11 and Appendix F; supplement §8; `LeadingSystem.lean`; `QuantitativeBranch.lean` | Definition-first automatic differentiation gives the gauge Jacobian, determinant `-1/144`, two-sided inverse, and inverse infinity norm `304/3`; the candidate solution is exact and the positive solution is uniquely recoverable. However, the displayed elimination `3t F_2-F_3=3w(t-1)-t^4` is false. See Finding 2. |
| B2 quotient-to-six-coefficient adapter and normalizations | **PASS** | Main §9; `QuotientAdapter.lean` | Rebuilding entries 2 through 5 from four second differences and the first two entries recovers all six exactly. Exponentiation then transfers equality of real logarithms. |
| B3 terminating 3F2 producer and shifted differential recurrence | **PASS** | Main §13; supplement §10; `TerminatingHypergeometric.lean` | Exact rational products reconstructed termination, every derivative shift, the coefficientwise Euler equation, and the four-term recurrence for three fresh parameter families. |
| B4 recurrence coefficients and exact property tests | **PASS** | `DirectRecurrence.lean`; `TerminatingHypergeometric.lean`; candidate property test | All four ODE coefficients agreed exactly with the decomposed recurrence coefficients in 320 independently generated identities. Candidate test also passed `27 tuples, 2355 identities`. No small-`epsilon_p` assumption was introduced. |
| B5 finite-free coefficient conventions, reflection, and reciprocal roots | **PASS** | Main §12 and Appendix G; `FiniteFreeAdapters.lean` | Exact coefficient lists confirm the ascending/descending sign conventions, fixed-degree reflection, constant term one, and the two-factor 3F2 factorization. Reciprocal interval direction is elementary and correct. |
| B6 transported Jacobi matrix, Gershgorin interval, and constant eight | **UNCHECKED** | Main §12; supplement §9; Appendix G; `FiniteFreeAdapters.lean`; Phase-16 note | The diagonal formula and 162,000 definition-built entry inequalities survived a deterministic grid; the worst normalized diagonal displacement was `0.348589` and worst adjacent row sum `2.00979`, below the claimed bounds `4` and `4`. Lean proves the `4+4=8` implication from a typed certificate. The general root/matrix identification and the concrete entry estimates are still imported/not fully kernel-connected, and the primary Jacobi source is absent from the packet. |
| B7 MSS product-root bounds in original and reciprocal orientations | **UNCHECKED** | Main §12; supplement §9; Appendix G; `MSSProductRootInput` adapter | The reciprocal direction and product interval algebra are correct; definition-built convolutions in degrees 2--8 met both endpoints and the final constant. The general published MSS theorem and its exact hypotheses could not be checked because its source text is not included. |
| B8 MMP logarithmic mesh adapter and distinctness transfer | **UNCHECKED** | Main §12; supplement §§9, 16; `StrictLogMesh`/`MMPLogMeshInput` | Sampled factor/convolution roots were positive and simple, and every sampled convolution mesh was at least the first-factor mesh (minimum observed gain `0.00609256`). Lean correctly derives injectivity from the typed strict-mesh input. MMP v3 Definition 2.16 and Propositions 2.7(iii), 2.17 were not independently source-verified because the pinned primary text is absent. |
| B9 first-failure/Newton radius with y powers and localization constant | **FAIL** | Main §§12, 14; Appendix H; supplement §11; Phase-16 radius proof; `DominantMaximum.lean`; effectivity ledger | The normalization `T_k=y^k p^(k)(y)/p(y)` has the required powers and no `1/k!`; `C_0=48`, `C_1=96`, `K_r=4096`, `C_loc=12+8sqrt(6)`, and the exact neighbor budget `24579/131072` recalculate. All 196 sampled model jets met the radius. But the printed first-failure proof uses `m=k-2`, whose `P_3 T_(k+1)` term is not controlled by minimality of `k`. See Finding 1. |
| B10 complex Hermite--Genocchi remainder and simplex mass 1/720 | **PASS** | Main §15; Appendix I; `HermiteGenocchiCube.lean`, `HermiteGenocchiFTC.lean`, `ComplexHermiteGenocchi.lean` | The stick-breaking weights integrate to `1/(6·5·4·3·2·1)=1/720`. The degree-six Newton product saturates the bound when its sixth derivative is `720`, confirming the order and constant. The local convex-domain Lean theorem exposes the needed derivative and domain hypotheses. |
| B11 sign transfer, sixth-match gain, and final algebraic assembly | **PASS** | Main §§15--16; Appendix I; `MultiplierStability.lean`; `ConditionalAssembly.lean`; `JensenPolynomial.lean` | The Newton multiplier identity was reconstructed exactly. Five initial multiplier matches eliminate orders 1--4, the finite geometric tail is `<1/16`, and the sixth interpolation match yields `rho^6/(n^5 log n) ~ d^3/(n^2 log n)`. The positive-to-negative scaling is correct conditional on the upstream certificate. |

The three `UNCHECKED` statuses are not failures found by finite tests. They
record that a finite regression and a typed adapter do not prove the general
external theorem supplied to the adapter.

## 3. Findings

### 1. P1 — The printed first-failure radius argument does not control its higher neighbor

Appendix H says to take the first index `k` with `|T_k|>R^k`, use the
four-term recurrence at `m=k-2`, and bound the "three known neighbors." At
that index the recurrence is

```text
P3_(k-2) T_(k+1) + P2_(k-2) T_k
  + P1_(k-2) T_(k-1) + P0_(k-2) T_(k-2) = 0.
```

First-failure minimality controls `T_(k-1)` and `T_(k-2)`, but it does not
control `T_(k+1)`. The independent audit gives an exact normalized local
counterexample to that inference: with target coefficient one, higher-neighbor
coefficient `1/4`, `T_2=2`, and `T_3=-8`, index two is the first violation,
the neighbor coefficient is `<1`, and the recurrence still cancels exactly.

This does not refute the radius proposition. The Phase-16 note contains the
correct repair: let `M=max_(0<=j<=d) |T_j|/R^j`; every neighbor is then at most
`M`, and the coefficient sum `q<1` contradicts any maximizing index at least
two. `DominantMaximum.lean` proves precisely this abstract maximum step. The
manuscript must use that global-maximum proof and explain the endpoint
`T_(d+1)=0`; calling it a first-failure proof is not valid.

### 2. P2 — The displayed leading-system elimination is false

The main paper and supplement attribute

```text
3 t F_2 - F_3 = 3 w (t-1) - t^4.
```

That is not an identity for the displayed residuals. The exact useful
combinations of the last three equations are instead

```text
3 F_1 - F_2 = 3w(t-1)/t^4 - 1,
(4/3) F_2 - F_3 = 4w(t-1)/t^5 - 2/3.
```

At a zero these give `3w(t-1)=t^4` and `6w(t-1)=t^5`; positivity forces
`t=2`, after which `w=16/3`, `delta=1/3`, and `alpha=3`. Thus the claimed
positive solution and uniqueness are correct, and `LeadingSystem.lean`
contains a valid proof, but the displayed manuscript derivation must be
replaced.

### 3. P2 — The packet cannot independently substantiate the external B6--B8 source seams

The packet records hashes and assertions that MMP arXiv v3 and the published
MSS theorem were audited, but it does not contain those primary texts or
verbatim theorem records. The review instructions forbid access outside the
archive. Consequently I could test the adapters and many instances, but I
could not verify the exact theorem statements, hypotheses, proposition
version, or convention direction. For a packet intended to support a
separated source-fidelity review, include the hash-matched source artifacts or
self-contained, page-addressed theorem excerpts sufficient to check the
consumed claims.

### 4. P3 — One supporting trust-boundary note is stale about the Lean ODE coverage

The trust-boundary paragraph of `C48_UNIFORM_RADIUS_PROOF.md` says the 3F2 ODE
is not formalized in Lean. In the frozen candidate,
`TerminatingHypergeometric.lean` does prove the finite producer,
coefficientwise Euler ODE, shifted ODE, derivative shift, and genuine shifted
four-term recurrence. The main manuscript and assurance matrix reflect the
new status; the older Phase-16 note should be updated or explicitly marked
superseded.

## 4. Independent-recalculation record

All reviewer-written scripts are beside this report under `scripts/`. None
opens the extracted archive, any candidate result JSON, or any frozen expected
mathematical output.

| Script | Method | Result | Reads frozen expected results? |
|---|---|---|---|
| `scripts/recalculate_exact_algebra.py` | Standard-library rational arithmetic, forward automatic differentiation, Gauss--Jordan inversion, finite Pochhammer products, derivative lists, and coefficientwise convolution | PASS; B1 determinant/norm reconstructed; false elimination detected; 320 B3/B4 identities and 117 B5 checks | **No** |
| `scripts/adversarial_root_geometry.py` | In-file real-root isolation by derivative interlacing and bisection, deterministic entry grid, model factor/convolution roots constructed from finite definitions | PASS finite regression; 162,000 entry inequalities and 280 root/mesh/localization checks | **No** |
| `scripts/audit_radius_hg_stability.py` | Exact neighbor budgets, definition-built critical-point jets, logical mutation of the first-failure step, simplex integration, Newton differences, and sixth-power scaling | PASS calculations; first-failure method falsified | **No** |

Reproduction commands:

```bash
python3 scripts/recalculate_exact_algebra.py
python3 scripts/adversarial_root_geometry.py
python3 scripts/audit_radius_hg_stability.py
```

I also ran three candidate-authored corroborative scripts. These are not
counted as independent reviewer calculations:

```text
PASS exact terminating 3F2 properties: 27 tuples, 2355 identities
PASS 909 exact finite-free/Jacobi adapter checks
PASS exact branch intervals
```

`VERIFY_BUNDLE.py` necessarily reads the frozen manifest hashes; it was used
only for bundle integrity, not as expected mathematical data.

## 5. Unchecked claims

1. The general classical Jacobi root/eigenvalue correspondence in the exact
   transported normalization, and a complete proof of the uniform entry
   inequalities for all legal real parameters.
2. The exact statement and hypotheses of MMP v3 Definition 2.16 and
   Propositions 2.7(iii), 2.17.
3. The exact published statement and hypotheses of MSS Theorem 1.6.
4. Kernel replay of the Lean project. I statically inspected the supplied Lean
   sources and found no `sorry`, `admit`, custom `axiom`, or `unsafe` escape,
   but the packet does not contain a vendored Mathlib/Lake build state and the
   archive-only constraint precluded fetching one.
5. The xi-specific center residual and whole-box Jacobian certificates that
   construct the positive parameter branch.
6. The uniform complex sixth-derivative constant `C_B6`, analytic threshold
   `N_analytic`, and the upstream sectorial analytic estimates. They are
   expressly symbolic boundaries in the packet and outside the finite
   recalculations here.
7. Any claim that the finite numerical root grids establish the general
   Jacobi, MSS, or MMP theorems; they do not.

## 6. Release recommendation and exact blockers

**Do not release this freeze unchanged.** A revised freeze is reviewable after:

1. replacing every first-failure description in the main paper, supplement,
   and detailed appendix with the global normalized-maximum proof, including
   the `k=d`/`T_(d+1)=0` endpoint;
2. correcting the leading-system elimination in the main paper and supplement;
3. including independently checkable, version-pinned source material for the
   exact B6--B8 external statements, or obtaining a separate source-fidelity
   review that is allowed to access those primary sources;
4. updating the stale Phase-16 Lean trust-boundary sentence.

After items 1--3, rerun the algebraic track. Item 4 is editorial and may be
verified in the same revision. No change to the candidate evidence was made
during this review.

## 7. Model, provider, tools, separation, and conflicts

- Model/provider: OpenAI Codex, GPT-5 family. The exact serving snapshot is not
  exposed in this review context.
- Tools: `unzip`, the packet's `VERIFY_BUNDLE.py`, Python 3 standard library
  (`fractions`, `math`, built-in complex arithmetic), `rg`, `sed`, and static
  inspection of the supplied Lean/TeX/Markdown sources. No web or network
  source was used.
- Context access: only the named algebraic review ZIP was extracted into the
  private temporary directory `/private/tmp/phase25_algebraic.HDWB4Q`. I did
  not inspect repository evidence outside that archive, another Phase-L track,
  an author response, or a prior review report. The only writes were this
  report and reviewer-authored scripts in the designated output directory.
- Earlier freeze: I have not reviewed an earlier freeze in this task context.
  Candidate notes mention that earlier AI pre-reviews existed, but those
  reports were not present and were not sought or read. This is therefore a
  separated first pass, not a correlated re-review, subject to the ordinary
  caveat that model-training exposure cannot be audited from this interface.
- Conflicts: no authorship, financial, personal, or coordination conflict is
  known. I did not communicate with the authors or other review tracks.

## 8. Review classification

This is AI review, not human or peer review.
