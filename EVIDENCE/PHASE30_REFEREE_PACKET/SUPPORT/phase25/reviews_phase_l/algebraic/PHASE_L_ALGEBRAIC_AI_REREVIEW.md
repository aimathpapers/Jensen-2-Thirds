# Phase L algebraic correlated AI re-review

Date: 2026-08-18  
Candidate: `6ee1db8fc5789a01bc0297f850c817f55b529be4`  
Required checkpoint: `5f79158f9c6276dd09142edeea279e35b0d58406`  
Packet SHA-256: `9d4a322bf5ad953b3c13b8181c6121451b0d56aef41b270b7ccd4ed6a3926084`  
Review class: targeted correlated algebraic AI re-review

## 1. Overall verdict

**R1 — mathematically releaseable after one localized P2 manuscript correction.**

**Release status: HOLD for correction and PDF rebuild.** The hold is caused by
one false expanded display of the central recurrence coefficient, repeated in
the technical supplement and the main paper's detailed appendix. The
load-bearing main formula, ODE-derived coefficient, Lean declaration, exact
property tests, and radius estimates all use the correct coefficient. I found
**no remaining P0 or P1 finding** and no new P0/P1 regression.

For this report, R1 means that no theorem-affecting defect was found, but a
material, objectively false display should be repaired before the frozen
candidate is released as a clean mathematical artifact.

This is AI review, not human or peer review.

## 2. Packet integrity and scope discipline

I extracted only
`Jensen_Two_Thirds_Phase25_Repaired_Algebraic_AI_Rereview_Packet.zip` into an
isolated temporary directory. I did not inspect another review track, a prior
report, the author disposition, or repository mathematical evidence outside
the archive. The only non-archive mathematical sources consulted were the
official primary/reference URLs named below for the B6--B8 seam. I made no
change to candidate evidence.

From the extracted packet root:

```text
$ python3 VERIFY_BUNDLE.py
PASS Phase-L AI reviewer bundle manifest (99 files)
```

The candidate commit file and bundle metadata both name
`6ee1db8fc5789a01bc0297f850c817f55b529be4`.

## 3. Gate-by-gate result

| Gate | Result | Evidence and adversarial recalculation |
|---|---|---|
| B1 leading system, positive solution, Jacobian, inverse, norm | **PASS** | Reconstructed the four rational residuals from their definitions. Exact elimination gives `3w(t-1)=t^4` and `6w(t-1)=t^5`; `t,w>0` forces `t=2`, then `w=16/3`, `delta=1/3`, `alpha=3`. Direct differentiation in `(alpha,t,w,delta)` order gives determinant `-1/144`, a two-sided exact inverse, and infinity norm `304/3`. The repaired Lean uniqueness theorem needs only `t,w>0` and derives `t>1`. |
| B2 quotient-to-six-coefficient adapter and normalizations | **PASS** | Equality of the four consecutive logarithmic second differences, together with coordinates 0 and 1, inductively forces coordinates 2 through 5. The Lean theorem has exactly these quantifiers. Independent exact tests reconstructed the recurrence rather than loading expected coefficients. |
| B3 terminating `3F2` producer and shifted differential recurrence | **PASS** | Checked the finite coefficient recurrence, termination at `k=d-m`, derivative shift, Euler ODE, and four-term derivative recurrence. Packet property test: `27` tuples and `2355` exact identities PASS. Independent reconstruction checked the polynomial ODE at exact rational points and derivative orders without SymPy or frozen results. |
| B4 recurrence coefficients and exact property tests | **FAIL (P2 only)** | The compact/decomposed coefficients, Lean source, ODE producer, packet property tests, and load-bearing estimates agree. However, the two expanded manuscript displays use `B+D+3m+1` where exact expansion gives `B+D+2m+1`. See Finding 1. |
| B5 finite-free coefficient conventions, reflection, reciprocal roots | **PASS** | Reindexed the ascending constant-term-one coefficient formula and independently checked that reflection converts it to the descending monic convention. Positive roots reciprocate and `[a,b]` becomes `[1/b,1/a]`. Packet exact adapter test and independent tests pass. |
| B6 transported Jacobi matrix, Gershgorin interval, constant eight | **PASS, with the disclosed classical-input boundary** | With `alpha=V-1` and `beta=U-V-d`, the factor is a transported Jacobi polynomial. Under `U>=V+d`, `V>=32d`, the paper's diagonal displacement and off-diagonal estimates give `4 sqrt(Vd)+4 sqrt(Vd)`, hence `8 sqrt(Vd)`. I checked the quotient inequalities and ran exact squared-entry tests over wide boundary/extreme grids. The root/matrix correspondence and concrete entry certificate remain imported inputs, exactly as the trust-boundary text says. |
| B7 MSS product-root bounds in original and reciprocal orientations | **PASS** | The official published Theorem 1.6 is the nonnegative-root preservation and maximum-root product inequality. Applying it to the original convolution gives the upper endpoint; applying it after reversal gives the lower endpoint. The packet cites Theorem 1.6, not Holland's mismatched published numbering. |
| B8 MMP logarithmic mesh adapter and distinctness transfer | **PASS** | Official arXiv v3 Proposition 2.7(iii) gives nonnegative-root preservation. Definition 2.16 orders roots decreasingly and defines adjacent ratios `>=1`; Proposition 2.17 has the required `lmesh(p boxtimes q)>=lmesh(p)` direction. A simple positive Jacobi factor has strict mesh, so the output has distinct positive roots; constant term one excludes zero. |
| B9 first-failure/global-maximum radius with `y` powers and localization constant | **PASS** | The repaired proof uses the global maximum `M=max_{0<=j<=d}|T_j|/R^j`. If `M>1`, a maximizing `k` is at least 2. At `m=k-2`, the higher neighbor is covered by the same global maximum when `k<d`, and is `T_(d+1)=0` when `k=d`. Exact budgets with `C0=48`, `C1<96`, `Kr=4096` sum below `1/2` after the stated `d/n` caps. The normalization retains `T_k=y^k p^(k)(y)/p(y)` and has no `1/k!`. |
| B10 complex Hermite--Genocchi remainder and mass `1/720` | **PASS** | The local open-convex-domain Lean theorem derives the Newton product by repeated complex FTC and derives, rather than assumes, the integral representation. The stick-breaking weights have exact mass `1/(6*5*4*3*2*1)=1/720`. Independent exact tests reconstruct the mass and six-node factorization. |
| B11 sign transfer, sixth-match gain, final algebraic assembly | **PASS** | Five vanished low finite differences make the geometric tail start at order 5, whose finite sum is strictly below `1/16`; the application has six matches. Relative error below one preserves endpoint signs, disjoint sign-changing intervals produce distinct positive roots, and `y=-S X` with `S>0` preserves distinctness while changing the sign of every root. The Lean end theorem remains correctly conditional on the analytic certificate. |

## 4. Numbered findings

### Finding 1 — P2: expanded `P_{2,m}` display has an extra `m`

The expanded recurrence coefficient printed in both of these frozen sources is

```text
P_{2,m} = B + D + 3m + 1
          - (Dy/AC)(A + C + 3m - d + 3).
```

Locations:

- `manuscript/source/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex:407`, rendered
  on technical supplement page 7;
- `manuscript/source/c48_detailed_appendices.tex:574`, rendered on main-paper
  page 33 as equation (H.2).

Expanding the shifted Euler ODE from the definitions gives

```text
P_{2,m} = B + D + 2m + 1
          - (Dy/AC)(A + C + 3m - d + 3).
```

Indeed the ODE has lower parameters `B+m` and `D+m`, so its non-`y` term is
`(B+m)+(D+m)+1 = B+D+2m+1`. The independent re-review script also expands the
decomposed formula and verifies that the printed expression minus the correct
one is exactly `m`; it detected the mismatch in 96 nonzero-`m` exact
instances.

The correct formula is already present in the load-bearing surfaces:

- main paper equation (13.5), which uses the correct decomposed expression;
- `TerminatingHypergeometric.lean:319`, where the term is
  `B + m + (D + m) + 1`;
- `DirectRecurrence.lean`, theorem `recurrenceP2_closed`, whose numerator has
  `A*C*(B+D+2m+1)` after collection;
- the terminating-hypergeometric exact property test and the frozen
  Mathematica M2 ledger.

The Phase 16 radius estimates use the decomposed formula, not the erroneous
expanded display. Therefore this is material false mathematical text but does
not alter the recurrence actually proved or the radius conclusion; severity
is P2, not P1.

**Required repair:** change `3m` to `2m` in both expanded displays, rebuild
both PDFs, and add a manuscript regression that compares the rendered/source
expanded `P_{2,m}` with the ODE/decomposed coefficient for symbolic or at least
nonzero `m` input. No candidate evidence was edited during this review.

No other P0, P1, P2, or P3 finding was found.

## 5. Recheck of the earlier algebraic findings

| Earlier issue | Re-review disposition |
|---|---|
| Radius proof selected a lower-index extremum and did not control the higher neighbor | **Closed.** The repaired proof selects a global maximum over all `0<=j<=d`. For interior `k`, `T_(k+1)` is in the maximum; for `k=d`, termination gives zero. The index and budget logic were reconstructed independently. |
| Leading-system elimination/positivity was incorrect or under-justified | **Closed.** The two corrected eliminants are exact; `t,w>0` imply `t>1`, then uniqueness. The solution, Jacobian, inverse, determinant, and norm all recompute exactly. |
| B6--B8 source versions, theorem number, orientation, or mesh direction were ambiguous | **Closed at the stated external-input boundary.** MMP is pinned to v3 with the required proposition text and mesh direction. MSS published Theorem 1.6 is the exact maximum-root inequality, and reversal supplies the lower endpoint. The Jacobi mapping and zero facts agree with DLMF/Szegő; the concrete matrix certificate remains an openly imported paper premise. |
| Phase 16 overstated what Lean proves | **Closed.** The trust-boundary paragraph accurately says the recurrence and abstract maximum contradiction are checked, while the classical Jacobi correspondence, concrete entry estimates, MMP/MSS theorems, and coarse parameter inequalities remain paper/external mathematics. `RatioFreeJacobiInput` visibly contains `entry_certificate` and `root_is_eigenvalue` fields rather than proving them. |

## 6. Load-bearing algebra reconstructed

### Leading system

Writing `F_j` as in the manuscript,

```text
3 F1 - F2     = 3w(t-1)/t^4 - 1,
(4/3)F2 - F3 = 4w(t-1)/t^5 - 2/3.
```

At a positive zero, these are `3w(t-1)=t^4` and
`6w(t-1)=t^5`. Positivity excludes every division hazard and gives `t=2`.
Substitution gives the remaining three coordinates. Direct exact Gaussian
elimination on the reconstructed Jacobian gives determinant `-1/144` and
inverse norm `304/3`.

### Jacobi/product localization

The standard hypergeometric representation with
`alpha=V-1`, `beta=U-V-d` identifies

```text
2F1(-d,U;V;y/U)
```

with a nonzero multiple of `P_d^(alpha,beta)(1-2y/U)`. The legal parameter
box has `alpha>-1`, `beta>=0`. The diagonal displacement formula and each
off-diagonal square passed exact rational boundary and large-ratio tests. The
paper inequalities then give the single-factor radius `8 sqrt(Vd)`.

For the product, the second scaled factor has deviation at most
`8 sqrt(d/D)`. With `B/D<=6` and `d/D<=1/256`,

```text
8 sqrt(Bd) + 8 B sqrt(d/D) + 64 sqrt(Bd) sqrt(d/D)
 <= (12 + 8 sqrt(6)) sqrt(Bd) < 32 sqrt(Bd).
```

The preliminary value `K_pre=256` gives lower relative endpoint `1/2`; using
`32` there would indeed make that endpoint negative.

### Radius maximum

At the maximizing index `k`, the recurrence with `m=k-2` contains neighbors
`T_(k-2), T_(k-1), T_k, T_(k+1)`. This confirms that only a global, not a
lower-index, maximum controls the last neighbor. The exact constant part is

```text
8*96/4096 + 8*48/4096^2 = 24579/131072 < 1/4.
```

The ledger caps make the `P3` and vanishing `P1` pieces at most `1/8` each,
so the total is below `1/2`. This gives the strict maximality contradiction.

### Sixth-order remainder and sign assembly

The six nested weights integrate to `1/720`. The Newton product supplies six
powers of the localization radius. The multiplier tail begins at order five
and is strictly smaller than `1/16`; hence the abstract tolerance `epsilon<16`
gives relative error below one. The final positive-to-negative scaling is
injective because its scale is positive and nonzero.

## 7. External B6--B8 source record

I checked the packet audit against these official pages:

- [DLMF 18.5.7, Jacobi hypergeometric representation](https://dlmf.nist.gov/18.5.E7)
  and [DLMF 18.2, general orthogonal-polynomial zero facts](https://dlmf.nist.gov/18.2);
- [MMP arXiv:2309.10970v3 HTML](https://arxiv.org/html/2309.10970v3),
  especially Proposition 2.7(iii), Definition 2.16, and Proposition 2.17;
- [MSS publisher PDF](https://link.springer.com/content/pdf/10.1007/s00440-021-01105-w.pdf),
  Theorem 1.6 on published page 810.

The official MMP record confirms that v3 corrected Proposition 2.11 and added
its proof, supporting the packet's insistence on a versioned citation. The
candidate does not consume Proposition 2.11 for the coarse interval. The MMP
journal PDF was not openly byte-compared; exact proposition wording is tied to
the accessible v3 preprint, as the packet discloses.

## 8. Independent-recalculation record

The new script is
`reviews_phase_l/algebraic/rereview_scripts/algebraic_rereview.py`.
It uses only Python's standard library and reads **no frozen expected result,
JSON ledger, manuscript, or repository output**. It constructs inputs from the
definitions and performs exact `fractions.Fraction` arithmetic. Jacobi radical
bounds are checked after squaring. Its run produced:

```text
PASS B1 leading system/Jacobian: 80 exact checks
PASS B2 quotient adapter: 114 exact checks
PASS B3-B4 terminating producer/recurrence: 648 exact checks
PASS B5 convention adapter: 119 exact checks
PASS B6-B8 Jacobi/product/mesh arithmetic: 25604 exact checks
PASS B9 global maximum/radius budgets: 14857 exact checks
PASS B10-B11 HG/finite assembly: 80 exact checks
DETECTED manuscript P2 display discrepancy: B+D+3m+1 differs from the reconstructed P2 by +m in 96 nonzero-m exact instances
PASS total exact checks: 41502
```

Additional packet-local reruns:

```text
PASS exact terminating 3F2 properties: 27 tuples, 2355 identities
PASS 909 exact finite-free/Jacobi adapter checks: reflection, diagonal displacement, reciprocal/product endpoints, and localization
PASS exact branch intervals: margins, inner inclusion, inverse norm, ordering extrema, half-radius factor, and K_pre -> C_loc -> K_0
PASS complete Phase-25 axiom surface: 66 declarations, only accepted foundational axioms
PASS no sorry/admit/axiom/unsafe token on packet Lean proof surface
```

The packet's SymPy scripts were not used as the independent path because
SymPy was unavailable in the isolated system Python. This does not leave the
load-bearing finite algebra unchecked: the new standard-library script
reconstructs it without importing those scripts or their saved JSON.

The exact-grid runs are falsification/regression evidence, not universal
proofs. Universal finite identities are additionally visible in the Lean
source; source-fidelity premises remain explicitly external.

## 9. Unchecked claims and retained boundaries

1. A fresh Lean build was not run from this review extraction. The archive
   supplies source, toolchain/manifest pins, and frozen axiom output but not an
   archive-local Mathlib cache. I ran the packet's axiom-output verifier and
   inspected the relevant declarations. This is not a replacement for fresh
   kernel replay.
2. The classical theorem identifying the displayed transported Jacobi matrix
   eigenvalues with the factor roots remains an external input. I checked the
   hypergeometric-to-Jacobi mapping, legal parameters, zero location, entry
   algebra, and Gershgorin consequence, but did not re-prove the general
   spectral theorem.
3. The MMP journal PDF was not byte-compared with arXiv v3; the official
   journal record and official v3 preprint are used exactly as disclosed.
4. The analytic construction of `C_B6`, `N_analytic`, and the concrete
   xi-specific certificate is outside this algebraic track. B10--B11 were
   checked as algebraic/conditional implications, not as a new audit of those
   analytic premises.

These retained boundaries are not newly discovered P0/P1 defects because the
candidate labels them as external or analytic premises. They must not be
described as kernel-proved facts.

## 10. Release recommendation and exact blockers

There is **no P0 or P1 blocker**. The sole release blocker for this repaired
freeze is Finding 1:

1. change `B+D+3m+1` to `B+D+2m+1` in the technical supplement and detailed
   appendix;
2. rebuild and re-freeze both PDFs;
3. add a regression with at least one `m>0` case so the erroneous display
   cannot agree vacuously at `m=0`;
4. rerun the bundle manifest verifier and the B3--B4 exact checks.

After that localized repair, my algebraic recommendation is release from this
track, subject to the separately disclosed analytic, Lean-replay,
reproducibility, and human-review limitations.

## 11. Model, tools, context, and conflict disclosure

- Reviewer: OpenAI Codex, GPT-5 family AI model. The exact serving snapshot is
  not exposed to the review process.
- Tools: archive-local shell reads, `rg`/`sed`, Python 3 standard-library exact
  arithmetic, packet verifiers/property tests, Poppler PDF metadata/rendering,
  visual inspection of the relevant rendered pages, and official-source web
  access limited to DLMF, arXiv v3, and the Springer publisher article/PDF.
- Context access: the designated repaired algebraic packet, the named official
  source URLs, and the new report/script output paths only. No other review
  track or author disposition was inspected.
- Separation/conflict: this is a **correlated re-review**. The task context
  identifies this reviewer as having reviewed the earlier freeze. I therefore
  do not claim independence or separation from that earlier algebraic pass,
  even though the recalculation script reads no frozen expected result.
- Human status: no human mathematical reviewer or peer reviewer participated
  in this report.

This is AI review, not human or peer review.
