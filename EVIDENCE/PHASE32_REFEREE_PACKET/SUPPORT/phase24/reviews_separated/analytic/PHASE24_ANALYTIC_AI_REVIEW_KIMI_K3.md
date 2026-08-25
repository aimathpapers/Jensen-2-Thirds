# Phase 24 analytic adversarial pre-review — separated first pass

**Object under review.** `Jensen_Two_Thirds_Phase24_Analytic_AI_Review_Packet`,
candidate commit `8e2781b2dbe065754ba511f3f076abb7f00ab0c6` (required
checkpoint `5f79158f9c6276dd09142edeea279e35b0d58406`). Bundle integrity:
`VERIFY_BUNDLE.py` → `PASS Phase-24 reviewer bundle manifest (107 files)`.

**Reviewer identity and classification.** This report is an **AI pre-review,
not human review and not peer review**. The reviewer is **Kimi, model
`kimi-code/k3`, provider Moonshot AI**, running in the Oh My Pi coding harness
on the author's workstation. Per `phase24/REVIEW_SEPARATION.md` this is a
**separated first pass**: I have never reviewed any earlier freeze of this
work, this session had no access to prior review reports, author responses,
finding dispositions, or recalculation outputs (the packet contains none and
I sought none), and I am a different model from a different provider than the
two correlated Claude Opus 5 re-reviews disclosed in the packet's
`KNOWN_LIMITATIONS.md` #1 and `ASSUMPTION_REGISTRY.md` (C48-REVIEW). No
session of mine reviewed an earlier freeze; if that disclosure is wrong, this
report must be reclassified as a correlated re-review and cannot satisfy the
separated first-pass gate.

**Conflicts of interest.** None: no author relationship, no stake in the
result, no prior involvement. The repository working tree on this machine is
at a different commit (`bee90f08…`) and was not used as evidence; only its
Python virtualenv supplied package versions (sympy 1.14.0, mpmath 1.3.0 —
coincidentally identical to the packet's pinned `requirements.lock`).

**Tools and method.** All mandatory recalculations were performed with
independent scripts written by the reviewer from the mathematical
definitions in the manuscript/proof notes (not by running or reading the
repository's result artifacts before deriving): nine scripts
(`independent_scripts/r1`–`r9`, listed with outputs below). Two read-only
subagent passes (same model) compressed the nine Phase-24 disclosure
documents and eight Phase-20/21 dependency notes; every load-bearing claim
they surfaced was re-checked by the reviewer against the primary files.
Lean sources were inspected statically (statement-level reads plus an
escape-hatch scan); the Lean build was **not** rerun (see Unchecked claims).

**Scope.** Gates A0–A10 of `REVIEW_PACKET.md`, the six mandatory independent
recalculations, the formalization trust boundary, and the disclosure
consistency of the unified manuscript.

---

## 1. Gate table

| Gate | Content | Result | Basis |
|---|---|---|---|
| A0 | Factor-eight Mellin identity; xi coefficient convention | **PASS** | R1: three independent evaluations of γ(n) (Cauchy transform of ξ; direct ω-moment quadrature; the (C5) assembly identity with direct F-quadrature) agree to ≥54 digits, n=0..4; pointwise identity at complex w to 60 digits; prefactor duplication form exact. Source audit (GORZ (11) parity, GORTTW (1.1) vs (3.1) factor 8) correctly identifies the defects; the candidate's `γ_H = γ_G/8` convention is the one that matches ξ itself. |
| A1 | Lemma S: Rouché, branch patching, reality, ordering of `Q_N ≠ 0` | **PASS** | R2: worst-case margin `2η(12)+3M(12)/(2e¹²) = 0.80693 < 1`; `m(12)=7.29032…`; `|r| ≤ 0.13717 < 7/50`, `|σ| ≤ 1.0962·10⁻⁴`, `|3L/4N| ≤ 8.22·10⁻⁵ < 10⁻⁴`; `151/200 > 9/16`. Ordering is correct: `Q_N ≠ 0` follows from the exact identity `Q_N = NL_N(1+r−¾σ)` and the norm bounds *before* `L′ = L/Q` is invoked; Rouché gives a *simple* zero, so the holomorphic IFT needs no prior nonvanishing. 60-point functional sweep confirms `|L_N − L_0| < 1`, `L′ = L/Q` (complex-step, rel. err ≤ 8·10⁻²⁵). |
| A2 | Legal shifted contour, connectors, signed Gaussian error, higher theta modes | **PASS** (one P3 display slip) | R3: at `s = 10⁴e^{i/100}` and `10⁵e^{i/100}`: `|Im L| ≈ 0.0086–0.0089 < 1/20`, `|arg K| < 1/20`, `Re K ≥ cos(1/20)|K|`; direct real-ray quadrature matches the main term with relative errors `6.5·10⁻⁵` and `8.1·10⁻⁶` vs scales `log|s|/|s| = 9.2·10⁻⁴`, `1.15·10⁻⁴` (O-constant ≈ 0.07); connector ratio `≤ 10⁻⁷²⁵⁹`; exact contour identity verified. Signed cubic moment ratio `3/K² + 1/K³` verified symbolically. Higher-mode geometric argument (`k²−1 ≥ 3(k−1)`) and region bounds checked on paper. Slip: finding F2. |
| A3 | Fixed nested-sector Theorem 21B; proportional-disc Cauchy differentiation | **PASS** | Angles `1/200 ⊐ 1/400 ⊐ 1/800`; disc `δ_C = 1/1000` angular loss `arcsin(δ_C/(1−δ_C)) = 0.00100100 < 1/800` (R8.3). `R⁽⁶⁾ = O(|z|^{−7+ε₀})` from `6! δ_C^{−6}` Cauchy on `O(|z|^{−1+ε₀})`. R9 end-to-end: direct moment γ_H(M) vs assembled main term `𝒢(M)` agrees at the claimed `O(log M/M)` scale (M=120: 0.0020; M=500: 0.00057); `𝒜(N+2)/𝒜(N) = L_N²(1+O(1/N))` confirmed (constant ≈ 1.1); `F(N+2)/(16(N+2)(N+1)F(N))` below the `L_N²/N²` scale. Stirling-correction logarithm `−1/(6N²)+O(1/N³)` re-expanded independently. |
| A4 | Implicit saddle derivative constants `2,−2,4,−12,48`; normalization; `N=2x−2` chain rule | **PASS** | R4 path A (reviewer's own SymPy implicit tower): normalized limits `(−1)^k (k−2)!`, k=2..6; σ→0 rational forms reproduce the phase-9 order-4/5 displays `(2r⁴+…+2)/(1+r)⁵`, `−(6r⁶+…+6)/(1+r)⁷` exactly; chain rule `2^k/(2x)^{k−1} → 2(−1)^k(k−2)!/(x^{k−1}L)` gives `2,−2,4,−12,48`. R4 path B (independent power-series Newton implicit solve, no symbolic algebra): derivative ratios to leading terms `0.86–1.11` at `L≈6.05`, consistent with `1+O(1/L)`. |
| A5 | Exact sixth-order denominator; coefficientwise majorant; no sampling-as-proof | **PASS** | R4C (reviewer's own exact run): reduced denominator `(4+4r−3σ)¹²` exactly; numerator has **82 terms**, total degrees 0–13 as claimed; exact coefficientwise majorant on `|r|,|σ| ≤ 7/50` over `(151/50)¹²` equals the disclosed rational `6422139805764931584036533551104/702576099728137594188684005 = 9140.8458… < 10⁴`; `|G₀⁽⁶⁾| ≤ 20000/(|N|⁵ log|N|)` then follows from `|L_N| ≥ ½log|N|`. The boundary sampling is labeled diagnostic-only in the evidence and plays no proof role. |
| A6 | Cube-integral `C¹` estimate; paired gamma boundary; parameter-derivative bounds | **PASS** | Identities rederived: `Δʲf₀` cube form with `(−1)^{j+1}j!`; `∂_s^r Φ_q = (−1)^r(q)_r∫(s+zΣu)^{−q−r}`; mean-value constant `(q)_r(q+r)q z s₀^{−q−r−1}`. Limits recomputed: `B−C` pair → `qw/t^{q+1}`; paired `D`–gamma → `qδ` (the `x/2` piece is `O(x/e)`); remote boundary → `1/α` only at q=1; weights `a_j = (1,1/2,1,1)`, `a_j q = (1,1,3,4)` ⇒ `H^∞` exactly as displayed. Pairing necessity (spurious `L_n` loss) confirmed structurally and in R6. |
| A7 | Contraction branch; exact box margins; local uniqueness; threshold consistency | **PASS** | R5 (exact rational): `F(y*) = 0`; reviewer's own elimination (`9(1−δ)(1−2δ) = 2(2−3δ)² ⇒ δ=1/3`) forces the unique positive-orthant zero `(3, 2, 16/3, 1/3)` — consistent with the Lean `SixthOrderLeadingSystem` uniqueness theorems. `det DF(y*) = −1/144` in the manuscript's analytic order `(α,t,w,δ)`; `DF(y*)⁻¹` row sums `87, 15, 304/3, 10/3`, norm `304/3`; `JP = PJ = I`. Margins `(1/2,1/2),(1/4,1/4),(1/3,2/3),(1/12,1/12)` and endpoint arithmetic `30 > 11/4`, `103/144` exact; hence `A > B > C > D > 0` for `0 < e ≤ 1/12`. `S^∞ = (−2,−1,−2,−2)` recomputed from the tower constants and component scales. `‖I−PDF‖ ≤ 1/4` legitimately requires the shrunken `K₀` (corner scan on the outer box reaches 4.89 — consistent with the proof's shrink step, not a gap). Uniqueness is stated locally only. Threshold order (`K_pre=256 → C_loc → K₀=262144 → K_r → n-thresholds`) checked non-circular. |
| A8 | Paired complex polygamma segments; thickened-domain containment | **PASS** | Sign pattern of `E_F⁽⁶⁾` rederived from the γ_H definition (duplication supplies the `b = n+1/2` term). R6: with the proof's own hypothesis `d + 2ρ ≤ n/1000` enforced (n = 10⁸–10¹⁰): `|ψ⁵(B+z)−ψ⁵(C+z)| · n⁵L_n` bounded ≈ 6.3–7.0, `|ψ⁵(D+z)−ψ⁵(b+z)| · n⁵L_n` ≈ 38 (stable in n), remote A-term ≤ 2·10⁻⁶ of target, segments keep `Re ≥ 0.999 n`; the unpaired term is `O(1/n⁵)` — the pairing is exactly what gains the `1/L` factor. Containment `n+Ω` inside the sector follows from `d+2ρ ≤ ηn`, itself from `d/n → 0` and `ρ/n ≍ √(d/n) → 0` under the wedge. |
| A9 | Complex Hermite–Genocchi/Newton remainder; hypotheses; six nodes; exact `1/720` | **PASS** | R7: simplex masses `1, 1/2, 1/6, 1/720` confirmed; the HG integral equals the recursively defined divided difference **exactly** on polynomial tests (z⁶, z⁷, z⁸ incl. a noninteger node, via Dirichlet moments) and to `1.1·10⁻¹⁷` for exp with a complex 7th node (own cube-transform Gauss quadrature); remainder form `f(z) = f[0..5,z]·∏(z−j)` exact for a six-zero test function; bound form `sup|f⁽⁶⁾|·∏|z−j|/720` verified. Hypotheses (holomorphy on a neighborhood of the convex stadium Ω; real nodes `0..5 ⊂ [0,d]`; `E_F(j)=0` via positive-real values killing the `2πi` ambiguity) checked. Lean `hHG` disclosure is accurate. |
| A10 | Exponent arithmetic to `n²log(n+2) ≥ Kd³`; effectivity disclosure | **PASS** | `ρ⁶ = K_r⁶(Bd)³ ≍ n³d³`; `sup|E_F| ≲ ρ⁶/(n⁵log(n+2)) ≍ d³/(n²log(n+2)) ≤ C′/K` under the wedge; `|z−j| ≤ 3ρ` from `ρ ≥ d`; `|eʷ−1| ≤ 2|w|` on `|w| ≤ 1/2` (max ratio 1.297 < 2); tails `Σ_{k≥5} 2^{−k} = 1/16`, `Σ_{k≥6} = 1/32`; `C_loc = 12+8√6 < 32` via `√6 < 5/2`; `K₀ = 262144` — all recomputed (R8). Effectivity wording is consistent with the program's own prescribed disclosure (finding F4 is a wording remark only). |

**Aggregate:** 11/11 gates PASS at the level of this review. No P0/P1/P2
findings. Four P3 items below.

---

## 2. Numbered findings

Severity convention: P0 proof-breaking; P1 material gap requiring repair
before any release; P2 localized defect requiring a displayed fix;
P3 presentation/documentation remark.

- **F1 (P3) — Jacobian determinant sign in `CLAIM_LEDGER.md`.** The ledger
  row for C48-LEADING-SYSTEM prints "Jacobian determinant `1/144`" while the
  manuscript and `MATHEMATICA_FOLLOWUP.md` print `−1/144`. Resolved during
  this review: `LeadingSystem.lean` pins `leadingJacobian_det = 1/144` in the
  algebraic coordinate order `(t,w,δ,α)` and `gaugeJacobian_det = −1/144` in
  the analytic order `(α,t,w,δ)`, with the odd column permutation documented.
  My independent Jacobian in the manuscript's coordinate order gives
  `−1/144`. Both numbers are correct; the ledger row should name its
  coordinate order so future reviewers do not misflag this as an
  inconsistency.

- **F2 (P3) — loose display in `phase21/C48_LEADING_CONTOUR_LOCALIZATION.md`
  eq. (17).** The grouping `log|e^{h_s(L)}| = Re(s Log L − s/L) + O(|L|)`
  absorbs the term `−s/L`, which is `O(|K|) ≍ |s|/log|s|`, not `O(|L|)`. The
  conclusion `log|…| ≥ c|s| log log|s|` is nonetheless correct, because
  `Re(s Log L) ≥ (log log|s| − O(1))·|s|·cos θ` dominates `|s|/log|s|` with
  room to spare; verified numerically in R3 (connector/main-term ratios
  `10⁻⁷²⁵⁹`, `10⁻⁸⁶⁴²⁹`). Reword the display so the `−s/L` term is counted
  at its true scale.

- **F3 (P3) — effectivity wording.** The manuscript's "The constant is
  effective in principle but is not optimized or printed numerically" is
  slightly stronger than `KNOWN_LIMITATIONS.md` #7 / `PAPER_THEOREM_INVENTORY`
  ("existential and unoptimized"), but matches the disclosure sentence
  prescribed by `phase18/C48_EFFECTIVITY_AND_MARGIN.md` §3. Recommend the
  manuscript adopt the phase-18 sentence verbatim (it adds "…the present
  unweighted sup-norm contraction yields an astronomically large sufficient
  threshold…"), which removes any residual overstatement risk.

- **F4 (P3) — threshold bookkeeping for `e ≤ 1/12`.** The ordering
  `A > B > C > D > 0` is proved for `0 < e ≤ 1/12`, i.e. `L_n ≥ 12`; this is
  an eventual-threshold condition. The manuscript states it as a hypothesis
  in §6 (sec:branch) and the phase-18 ledger lists related thresholds, but
  `L_n ≥ 12` itself does not appear in the phase-18 threshold ledger items
  1–5. Add it explicitly for completeness of the threshold stack.

No other defects were found. In particular, the two items a prior review
might be expected to attack — the ordering of `Q_N ≠ 0` relative to
`L′ = L/Q` (A1), and whether the `ε < 16` stability lemma's Cauchy step
really delivers the constant-1 bound `|Δᵏc(0)|/k! ≤ ε/(2r)ᵏ` — both survive:
for the latter, the Genocchi integral form `c[0..k] = ∫_{Σ_k} c^{(k)}(Σ t_j j)
dt` with `Σ t_j j ∈ [0,k]` and Cauchy on radius-`2r` discs inside `Ω_r`
gives the bound with constant exactly 1 (a cruder stadium contour would lose
a factor `1 + k/(2πr)`; the manuscript's one-line appeal to "Cauchy's
estimate" is correct via this route, though it does not say so).

---

## 3. Independent-recalculation record

All scripts are reviewer-written from the definitions; none reads a
repository result artifact as input. Archived at
`independent_scripts/` beside this report. Environment: Python 3.11,
sympy 1.14.0, mpmath 1.3.0.

| # | Gate | Recalculation | Result |
|---|---|---|---|
| R1 | A0 | γ(n), n=0..4, three ways: (a) Cauchy transform of ξ at ½; (b) `8n!/(2n)! ∫ω(e^{2u})e^{u/2}u^{2n}du` with ω summed termwise; (c) the (C5) assembly identity with directly integrated F(s). Plus ξ(½+w) = 8∫ωe^{u/2}cosh(wu) at complex w; prefactor duplication form. | Agreement to ≥54 digits (a vs b vs c); complex-w identity to 60 digits; duplication form exact. γ values match the known GORZ sequence. |
| R2 | A1 | Lemma S constants from scratch: m(12), M(12), η(12), Rouché margin; `|r|,|σ|` bounds; `151/200 > 9/16`, `151/50`; Newton saddle solves at 60 random sector points with `|L−L_0|`, `|1+r−¾σ|`, and complex-step `L′ = L/Q`; direct boundary sampling (diagnostic). | Margin `0.80693 < 1`; sampled `max|G−H| = 0.487 < 1`; worst `|L−L₀| = 0.318`; min `|1+r−¾σ| = 1.018`; derivative formula confirmed to 10⁻²⁵. |
| R3 | A2 | `I_1(s)` by direct real-ray quadrature at `s = 10⁴e^{i/100}`, `10⁵e^{i/100}` vs main term `𝒜(s)` (own saddle solve); `|Im L|`, `|arg K|`, `Re K ≥ cos(1/20)|K|`; connector ratio; exact shifted-contour identity; symbolic signed cubic moment identity. | Rel. errors `6.5·10⁻⁵`, `8.1·10⁻⁶` at scales `9.2·10⁻⁴`, `1.15·10⁻⁴` (constant ≈ 0.07); connectors `≤ 10⁻⁷²⁵⁹`; `∫r³e^{r−Kr²/2}/∫e^{r−Kr²/2} = 3/K²+1/K³` exact. |
| R4 | A4/A5 | Own SymPy implicit tower `𝒟 = ∂_N + (L/Q)∂_L` on `G_0` through order 6; two-scale limits; chain rule. Independent path B: power-series Newton solution of `Ψ(L(t)) = N₀+t` to order 8, then series composition (no rational algebra). Exact H₆ structure: denominator, term count, degrees, coefficientwise majorant. | Constants `(−1)^k(k−2)!` and `2,−2,4,−12,48` confirmed both paths; σ=0 polynomials match phase-9/11 displays; denominator `(4+4r−3σ)¹²`; 82 terms; degrees 0–13; majorant = `9140.8458… < 10⁴`, equal to the disclosed rational. |
| R5 | A7 | Exact rational model algebra: zero, own elimination uniqueness, Jacobian, determinant, inverse, row sums, margins, endpoint arithmetic; corner scan of `‖I−PDF‖`. | All manuscript values confirmed (`det = −1/144`, `304/3`, `87/15/304/3/10/3`, margins, `30 > 11/4`, `103/144`); outer-box corner max 4.89 confirms the shrink step is necessary and consistent. |
| R6 | A8 | Paired polygamma scale at wedge-respecting parameters (n = 10⁸–10¹⁰, `d+2ρ ≤ n/1000`), z on the stadium rim; mpmath.polygamma cross-checked against the defining series. | Pair differences `= O(1/(n⁵L_n))` with stable constants (≈ 6.3–7.0, ≈ 38); A-term negligible; segments `Re ≥ 0.999n`; unpaired term is `O(1/n⁵)` (no log gain) — pairing is load-bearing and correct. |
| R7 | A9 | Hermite–Genocchi: simplex masses; HG = recursive divided differences exactly (Dirichlet-moment route, polynomials) and numerically (own cube-transform Gauss quadrature, exp with complex node); Newton remainder with nodes 0..5; 720·mass = 1 through the integral route. | All identities confirmed (exact on polynomials; ≤ 1.1·10⁻¹⁷ numeric); remainder bound form verified on a six-zero test function. |
| R8 | A3/A7/A10 + localization chain | Geometric tails; `|eʷ−1| ≤ 2|w|`; sector nesting angles; `C_loc` product arithmetic; (Q3),(Q1),(Q0) normalized neighbor coefficients; the shifted ₃F₂ ODE expansion (own derivation of (H3) from `θ(θ+b₁−1)(θ+b₂−1)g = λy(θ+a₁)(θ+a₂)(θ+a₃)g`); closed forms `P₃ = (AC−Dy)/AC`, `P₀ = Dy(A+m)(C+m)(d−m)/AC`; the decomposed `P₂`, `P₁` forms; transported diagonal identity; ratio-free Jacobi lemma (J) by direct root computation with an independently built Jacobi matrix (validated by Vieta + residuals). | All symbolic identities exact. (J) root inclusion held at all 13 tested (d,U,V) including boundary cases `U = V+d`, `V = 32d`, with wide margins. |
| R9 | A3 (end-to-end) | Direct moment computation of γ_H(M) vs the assembled Theorem-21B main term `𝒢(M)`; two-step ratio `𝒜(N+2)/𝒜(N)`; `F(N+2)` subordination with the full theta kernel. | `γ_H/𝒢 − 1 = 0.0020` (M=120), `0.00057` (M=500) at scale `log M/M`; two-step ratio deviation ≈ `1.1/N` = O(1/N); `F(N+2)/(16(N+2)(N+1)F(N))` at 0.06 of the `L_N²/N²` scale. |

Additional analytic re-derivations done on paper (no code): the (C2)
derivatives of `1/(z(z−1))` and the two integral terms; the (C4)/(C5)
coefficient extraction including the `γ_G = 8γ_H` split; the `a′(s)`
cancellation (assembly eq. 8, coefficient of `L′` is `K_s+1`);
`Log R_N = −1/(6N²)+O(1/N³)`; the `P_{2,m} ≥ n/8` chain (`(D+m)a ≥ 3n/8`,
`|b_{m+1}| ≤ n/4` via `C_loc√(Bd) ≤ 3n/16` and `2d+1 ≤ n/16`); the
maximum-argument boundary case `T_{d+1} = 0`; the multiplier lemma's Cauchy
step via the Genocchi form (constant exactly 1, see F2-discussion above);
the `E_F⁽⁶⁾` sign pattern from the γ_H definition; higher-mode geometric
factor and region bounds; strict concavity sign argument
(`|arg(s/(x+ib)²)| ≤ 1/100 + 1/10 < π/2`).

---

## 4. Unchecked claims (explicit non-coverage)

1. **Lean build not rerun.** The pinned toolchain (Lean v4.33.0-rc2, Mathlib
   `51e6992e…`) build was not executed in this review; the packet itself
   notes Lean/Python runtimes are not embedded. Static inspection found no
   `sorry`/`admit`/`axiom`/`unsafe`/`native_decide` in the JensenWedge
   modules, and every module's statements match the formalization ledger
   (conditional certificate firewall; `hHG` named hypothesis; finite sign
   algebra only). A `lake build Zeta23.Research.JensenWedge` plus
   `#print axioms` audit remains to be executed by the release pipeline.
2. **Primary-source PDFs not fetched.** GORZ v2 / GORTTW v3 / MSS / MMP v3
   artifacts were not re-downloaded; their quoted contents (factor-eight
   split, G3.2 normalization, MSS Theorem 1.6 page-810 statement, MMP v3
   Propositions 2.7(iii)/2.17) were checked only for internal consistency
   against the packet's own audit files. The factor-eight convention — the
   only load-bearing normalization — was verified against ξ itself (R1).
3. **Gershgorin off-diagonal chain.** The transported diagonal identity was
   verified exactly and the lemma's *conclusion* (J) numerically (R8.7);
   the intermediate off-diagonal bound chain (`{·} ≤ 4d`, adjacent sum
   `≤ 4√(Vd)`) was read but not independently re-expanded symbolically.
4. **C¹ hidden constants.** The limiting values, exact identities, and
   mean-value constants of Phase 14 were verified; the uniform `O_K(·)`
   constants in the value/derivative error rates were checked for structure
   (pairing, `q ∈ {1,2,3,4}` uniformity) but not given independent explicit
   values.
5. **Repository regression scripts not rerun.** `leading_contour_check.py`,
   `scaled_branch.py`, `saddle_branch_check.py`, `six_coefficient_scan.py`,
   `root_radius_diagnostic.py`, `model_adapter.py`, and the frozen JSON
   artifacts were not executed; their role is regression/diagnostic, and R1–R9
   reproduce their essential content independently.
6. **The `10^1887` effectivity diagnostic** was not rechecked; it is an
   extrapolation from an externally reported, unconverged numerical
   coefficient (10.7), is labeled as such, and enters no proof.
7. **Higher-theta suppression** was verified on paper (geometric factor,
   three regions) but not re-executed numerically beyond the single-mode
   complex contour point of R3.
8. **Small-`d`/small-`n` finite range** (absorbed by increasing `K`) was
   checked logically, not computationally; no finite Jensen polynomial was
   root-counted in this review.

---

## 5. Release recommendation: **R1**

Rubric assumed from the packet's usage (prior correlated reviews "returned
R1 on two manuscript defects, both repaired"): R0 release as-is; R1 release
after minor non-mathematical repairs; R2 hold for material repair and
re-review; R3 reject.

**R1.** No mathematical defect was found in any gate. The four P3 items
(F1–F4) are documentation/display repairs that do not touch the proof. The
candidate's central new mathematics — the factor-eight-corrected sectorial
coefficient asymptotic (Theorem 21B chain), the exact sixth-order saddle
majorant, the non-perturbative critical-point radius, and the sixth-order
Hermite–Genocchi transfer — survived independent recomputation from
definitions at every point the packet designates as high-risk.

This recommendation is explicitly conditioned on the review's own limits
(Section 4): the Lean build and axiom audit must be rerun by the pipeline;
the result remains **AI-pre-reviewed working mathematics that has not
received human or peer review**, and the manuscript's own embargo and
publication-stop language should remain until it does. The deferred
clean-room Mathematica reconstruction (M1–M4) remains a correct and
necessary follow-up for common-mode CAS risk; my independent SymPy/mpmath
paths reduce but do not eliminate that risk, since SymPy is also the
repository's symbolic engine (mitigated here by the mpmath power-series
path B in R4 and by the all-numeric paths in R1/R3/R6/R7/R9, which share no
code with the repository producers).

---

## 6. Conflict/separation statement (formal)

I am an AI system: Kimi, model `kimi-code/k3`, provider Moonshot AI. This
report is an AI pre-review; it is not human review, not peer review, and
must not be described as either. This session is a genuine first pass: no
prior review report, author response, disposition, or recalculation output
was present in the packet or consulted; I had no access to the earlier
correlated Claude Opus 5 re-reviews; and no session of this model reviewed
an earlier freeze. Separation per `REVIEW_SEPARATION.md` is satisfied by
provider difference and by absence of prior context. Tools used: local
Python (sympy/mpmath) for reviewer-written recalculation scripts; read-only
subagents of the same model for document compression; no network fetches of
primary sources. No conflicts of interest. All scripts and this report are
delivered alongside the packet at the reviewer's archive path
`~/Desktop/jensen_phase24_analytic_review_kimi_k3/`.
