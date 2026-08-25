# Phase 24 analytic adversarial pre-review — findings handoff

**Date:** 2026-08-17
**Reviewed object:** `Jensen_Two_Thirds_Phase24_Analytic_AI_Review_Packet`
(candidate commit `8e2781b2dbe065754ba511f3f076abb7f00ab0c6`; required
checkpoint `5f79158f9c6276dd09142edeea279e35b0d58406`).
**Bundle integrity:** `VERIFY_BUNDLE.py` →
`PASS Phase-24 reviewer bundle manifest (107 files)`.

**Reviewer:** Kimi, model `kimi-code/k3`, provider Moonshot AI — an **AI
pre-review, not human review and not peer review**. Separated first pass:
no access to prior review reports, responses, dispositions, or the other
review track; different provider than the disclosed correlated Claude Opus 5
re-reviews; no session of this model reviewed an earlier freeze. If that
disclosure is ever found wrong, this report must be reclassified as a
correlated re-review and cannot satisfy the separated first-pass gate.
**Conflicts:** none. **Companion artifacts:** nine reviewer-written
recalculation scripts are archived at
`~/Desktop/jensen_phase24_analytic_review_kimi_k3/independent_scripts/`
(`r1`–`r9`, sympy 1.14.0 / mpmath 1.3.0); none reads a repository result
artifact as input.

---

## 1. Verdict

**Release recommendation: R1** (release after minor non-mathematical
repairs; rubric: R0 as-is / R1 minor repairs / R2 material repair +
re-review / R3 reject).

**No mathematical defect was found in any gate. 11/11 gates (A0–A10) PASS.
No P0/P1/P2 findings; four P3 documentation items.** The central new
mathematics — the factor-eight-corrected sectorial coefficient asymptotic
(Theorem 21B chain), the exact sixth-order saddle majorant, the
non-perturbative critical-point radius, and the sixth-order
Hermite–Genocchi transfer — survived independent recomputation from
definitions at every point the packet designates as high-risk. The result
remains AI-pre-reviewed working mathematics; the manuscript's embargo and
publication-stop language should remain until human review occurs.

---

## 2. Gate table

| Gate | Content | Result | Basis (independent recalculations R1–R9) |
|---|---|---|---|
| A0 | Factor-eight Mellin identity; exact xi coefficient convention | **PASS** | γ(n) computed three independent ways (Cauchy transform of ξ at ½; direct ω-moment quadrature with ω summed termwise; the (C5) assembly identity with directly integrated F) agree to ≥54 digits for n=0..4; `ξ(½+w) = 8∫ω(e^{2u})e^{u/2}cosh(wu)du` verified at complex w to 60 digits; prefactor duplication form `8√π/(4ⁿΓ(n+½))` exact. The candidate's `γ_H = γ_G/8` convention is the one that matches ξ itself; the GORTTW (1.1)-vs-(3.1) factor-8 defect is correctly identified in the source audit. |
| A1 | Lemma S Rouché comparison, branch patching, reality, ordering of `Q_N ≠ 0` | **PASS** | Worst-case margin `2η(12)+3M(12)/(2e¹²) = 0.80693 < 1` (ℓ=12, θ→π/2); `m(12)=7.29032…`; `|r| ≤ 0.13717 < 7/50`, `|σ| ≤ 1.0962·10⁻⁴`, `|3L/4N| ≤ 8.22·10⁻⁵ < 10⁻⁴`; `151/200 > 9/16`. Ordering correct: `Q_N ≠ 0` comes from the exact identity `Q_N = NL_N(1+r−¾σ)` + norm bounds *before* `L′ = L/Q`; Rouché gives a simple zero so the holomorphic IFT needs no prior nonvanishing. 60-point functional sweep: `|L_N−L_0| < 1` (max 0.318), `L′ = L/Q` to 10⁻²⁵; diagnostic boundary sample max `|G−H| = 0.487`. |
| A2 | Legal shifted contour, endpoint connectors, signed Gaussian error, higher theta modes | **PASS** (one P3 display slip, F2) | At `s = 10⁴e^{i/100}`, `10⁵e^{i/100}`: `|Im L| ≈ 0.0086–0.0089 < 1/20`; `|arg K| < 1/20`; `Re K ≥ cos(1/20)|K|`; direct real-ray quadrature vs main term: relative errors `6.5·10⁻⁵`, `8.1·10⁻⁶` against scales `9.2·10⁻⁴`, `1.15·10⁻⁴` (O-constant ≈ 0.07); connector/main ratio `≤ 10⁻⁷²⁵⁹`; exact shifted-contour identity verified; signed cubic moment `∫r³e^{r−Kr²/2}/∫e^{r−Kr²/2} = 3/K²+1/K³` exact. Higher-mode geometric argument (`k²−1 ≥ 3(k−1)`) and three-region bounds checked on paper. |
| A3 | Fixed nested-sector Theorem 21B; proportional-disc Cauchy differentiation | **PASS** | Nesting `1/200 ⊐ 1/400 ⊐ 1/800`; disc angular loss `arcsin(δ_C/(1−δ_C)) = 0.00100100 < 1/800` for `δ_C = 1/1000`; `R⁽⁶⁾ = O(|z|^{−7+ε₀})` chain verified. End-to-end: direct moment γ_H(M) vs assembled main term 𝒢(M) agrees at the claimed `O(log M/M)` scale (M=120: 0.0020; M=500: 0.00057); `𝒜(N+2)/𝒜(N) = L_N²(1+O(1/N))` confirmed (constant ≈ 1.1); `F(N+2)/(16(N+2)(N+1)F(N))` at 0.06 of the `L_N²/N²` scale; `Log R_N = −1/(6N²)+O(1/N³)` re-expanded independently. |
| A4 | Implicit saddle derivative constants `2,−2,4,−12,48`; normalization; `N=2x−2` chain rule | **PASS** | Two independent paths. (A) Reviewer's own SymPy implicit tower `𝒟 = ∂_N + (L/Q)∂_L`: normalized limits `(−1)^k(k−2)!`, k=2..6; σ→0 forms reproduce the phase-9/11 displayed polynomials exactly; chain rule gives `2,−2,4,−12,48`. (B) Power-series Newton implicit solve to order 8 (no symbolic algebra): derivative/leading ratios 0.86–1.11 at L≈6.05, consistent with `1+O(1/L)`. |
| A5 | Exact sixth-order denominator; coefficientwise majorant; no sampling-as-proof | **PASS** | Own exact run: reduced denominator `(4+4r−3σ)¹²`; numerator 82 terms, total degrees 0–13; coefficientwise majorant on `|r|,|σ| ≤ 7/50` over `(151/50)¹²` equals the disclosed rational `6422139805764931584036533551104/702576099728137594188684005 = 9140.8458… < 10⁴`; hence `|G₀⁽⁶⁾| ≤ 20000/(|N|⁵log|N|)` via `|L_N| ≥ ½log|N|`. Boundary sampling is labeled diagnostic-only in the evidence and plays no proof role. |
| A6 | Cube-integral `C¹` estimate; paired gamma boundary; common parameter-derivative bounds | **PASS** | Rederived: `Δʲf₀ = (−1)^{j+1}j! ∫_{[0,1]^q}(U+Σu)^{−q}`; `∂_s^r Φ_q = (−1)^r(q)_r∫(s+zΣu)^{−q−r}`; mean-value constant `(q)_r(q+r)q z s₀^{−q−r−1}`. Limits recomputed: B−C pair → `qw/t^{q+1}`; paired D–gamma → `qδ`; remote boundary → `1/α` only at q=1; `a_j = (1,1/2,1,1)`, `a_jq = (1,1,3,4)` ⇒ `H^∞` exactly as displayed. Pairing necessity (spurious `L_n` loss) confirmed structurally and numerically (R6). |
| A7 | Contraction branch; exact box margins; local (not global) uniqueness; threshold consistency | **PASS** | Exact rational check: `F(y*)=0`; own elimination (`9(1−δ)(1−2δ)=2(2−3δ)² ⇒ δ=1/3`) forces the unique positive-orthant zero `(3,2,16/3,1/3)`, consistent with the Lean uniqueness theorems. `det DF(y*) = −1/144` (analytic order); inverse row sums `87, 15, 304/3, 10/3`, norm `304/3`; `JP = PJ = I`. Margins `(1/2,1/2),(1/4,1/4),(1/3,2/3),(1/12,1/12)`; endpoint arithmetic `30 > 11/4`, `103/144`; hence `A>B>C>D>0` for `0 < e ≤ 1/12`. `S^∞ = (−2,−1,−2,−2)` recomputed. `‖I−PDF‖ ≤ 1/4` legitimately requires the shrunken `K₀` (outer-box corner scan reaches 4.89 — consistent with the proof's shrink step). Threshold order `K_pre=256 → C_loc → K₀=262144 → K_r → n`-thresholds checked non-circular. |
| A8 | Paired complex polygamma segments; thickened-domain containment | **PASS** | `E_F⁽⁶⁾` sign pattern rederived from the γ_H definition (duplication supplies the `b = n+1/2` term). With the proof's own hypothesis `d+2ρ ≤ n/1000` enforced (n = 10⁸–10¹⁰): `|ψ⁵(B+z)−ψ⁵(C+z)|·n⁵L_n` bounded ≈ 6.3–7.0; `|ψ⁵(D+z)−ψ⁵(b+z)|·n⁵L_n` ≈ 38, stable in n; remote A-term ≤ 2·10⁻⁶ of target; segments keep `Re ≥ 0.999n`; the unpaired term is `O(1/n⁵)` — the pairing is exactly what gains the `1/L` factor. Containment `n+Ω` in the sector follows from `d/n → 0`, `ρ/n ≍ √(d/n) → 0` under the wedge. |
| A9 | Complex Hermite–Genocchi/Newton remainder; hypotheses; six nodes; exact `1/720` | **PASS** | Simplex masses `1, 1/2, 1/6, 1/720` confirmed; HG integral equals recursively defined divided differences exactly (Dirichlet-moment route on z⁶, z⁷, z⁸ incl. a noninteger node) and to `1.1·10⁻¹⁷` for exp with a complex 7th node (own cube-transform Gauss quadrature); remainder form `f(z) = f[0..5,z]·∏(z−j)` exact on a six-zero test function; bound form `sup|f⁽⁶⁾|·∏|z−j|/720` verified; `720·mass = 1` through the integral route. Hypotheses (convex stadium, real nodes in `[0,d]`, `E_F(j)=0` via positive-real values killing the `2πi` ambiguity) checked. Lean `hHG` disclosure accurate. |
| A10 | Exponent arithmetic to `n²log(n+2) ≥ Kd³`; effectivity disclosure | **PASS** | `ρ⁶ = K_r⁶(Bd)³ ≍ n³d³`; `sup|E_F| ≲ ρ⁶/(n⁵log(n+2)) ≍ d³/(n²log(n+2)) ≤ C′/K` under the wedge; `|z−j| ≤ 3ρ` from `ρ ≥ d`; `|eʷ−1| ≤ 2|w|` on `|w| ≤ 1/2` (max ratio 1.297 < 2); tails `Σ_{k≥5}2^{−k} = 1/16`, `Σ_{k≥6} = 1/32`; `C_loc = 12+8√6 < 32` via `√6 < 5/2`; `K₀ = 262144` — all recomputed. Effectivity wording consistent with the program's own prescribed disclosure (see F3). |

---

## 3. Numbered findings

Severity: P0 proof-breaking; P1 material gap requiring repair before
release; P2 localized defect requiring a displayed fix; P3
presentation/documentation remark. **No P0, P1, or P2 findings.**

- **F1 (P3) — Jacobian determinant sign in `evidence/ground_zero_work/CLAIM_LEDGER.md`.**
  The C48-LEADING-SYSTEM row prints "Jacobian determinant `1/144`" while the
  manuscript and `phase24/MATHEMATICA_FOLLOWUP.md` print `−1/144`. Resolved
  in this review: `LeadingSystem.lean` pins `leadingJacobian_det = 1/144`
  in the algebraic coordinate order `(t,w,δ,α)` and `gaugeJacobian_det =
  −1/144` in the analytic order `(α,t,w,δ)`, with the odd column
  permutation documented. My independent Jacobian in the manuscript's
  coordinate order gives `−1/144`. Both numbers are correct; the ledger row
  should name its coordinate order so future reviewers do not misflag this.

- **F2 (P3) — loose display in `phase21/C48_LEADING_CONTOUR_LOCALIZATION.md`, eq. (17).**
  The grouping `log|e^{h_s(L)}| = Re(s Log L − s/L) + O(|L|)` absorbs
  `−s/L = O(|K|) ≍ |s|/log|s|`, which is not `O(|L|)`. The conclusion
  `log|…| ≥ c|s|log log|s|` is nonetheless correct because
  `Re(s Log L) ≥ (log log|s| − O(1))·|s|cos θ` dominates `|s|/log|s|`;
  verified numerically (connector/main ratios `10⁻⁷²⁵⁹`, `10⁻⁸⁶⁴²⁹`).
  Reword so the `−s/L` term is counted at its true scale.

- **F3 (P3) — effectivity wording.**
  The manuscript's "The constant is effective in principle but is not
  optimized or printed numerically" is slightly stronger than
  `KNOWN_LIMITATIONS.md` #7 / `PAPER_THEOREM_INVENTORY` ("existential and
  unoptimized"), but matches the sentence prescribed by
  `phase18/C48_EFFECTIVITY_AND_MARGIN.md` §3. Recommend adopting the
  phase-18 sentence verbatim (it adds the "astronomically large sufficient
  threshold" clause), removing residual overstatement risk.

- **F4 (P3) — threshold bookkeeping for `e ≤ 1/12`.**
  The ordering `A > B > C > D > 0` is proved for `0 < e ≤ 1/12`, i.e.
  `L_n ≥ 12` — an eventual-threshold condition. The manuscript states it as
  a hypothesis in the branch section, but `L_n ≥ 12` does not appear in the
  phase-18 threshold ledger items 1–5. Add it explicitly.

**Two anticipated attack points that survive scrutiny.** (i) The ordering of
`Q_N ≠ 0` relative to `L′ = L/Q` (A1) is correct as displayed. (ii) The
multiplier-stability lemma's one-line "Cauchy's estimate" giving
`|Δᵏc(0)|/k! ≤ ε/(2r)ᵏ` with constant exactly 1 is correct via the Genocchi
integral `c[0..k] = ∫_{Σ_k} c^{(k)}(Σ t_j j)dt` (evaluation points lie in
`[0,k]`, and radius-`2r` discs stay inside `Ω_r`); a cruder stadium contour
would lose a factor `1 + k/(2πr)`, so the Genocchi route is the right one —
the manuscript might name it, but the bound is right.

---

## 4. Independent-recalculation record

All scripts reviewer-written from the mathematical definitions; archived at
`~/Desktop/jensen_phase24_analytic_review_kimi_k3/independent_scripts/`.

| # | Gate | What was recomputed | Result |
|---|---|---|---|
| R1 | A0 | γ(n), n=0..4, three ways (Cauchy transform of ξ; direct ω-moment quadrature; (C5) assembly with direct F-quadrature); pointwise complex-w identity; duplication prefactor form | ≥54-digit agreement across all paths; complex identity to 60 digits; matches the known GORZ sequence |
| R2 | A1 | Lemma S constants and Rouché margin from scratch; 60-point Newton saddle sweep; `L′ = L/Q` by complex step; boundary sampling (diagnostic) | Margin `0.80693 < 1`; sampled max `|G−H| = 0.487`; worst `|L−L_0| = 0.318`; min `|1+r−¾σ| = 1.018`; derivative formula to 10⁻²⁵ |
| R3 | A2 | `I_1(s)` direct real-ray quadrature at two complex s values vs main term; saddle/curvature geometry; connector size; shifted-contour identity; symbolic signed cubic moment | Rel. errors `6.5·10⁻⁵`, `8.1·10⁻⁶` at scales `9.2·10⁻⁴`, `1.15·10⁻⁴`; connectors `≤ 10⁻⁷²⁵⁹`; `3/K²+1/K³` exact |
| R4 | A4/A5 | Own SymPy implicit tower through order 6; independent power-series Newton path; exact H₆ structure and majorant | `(−1)^k(k−2)!` and `2,−2,4,−12,48` both paths; σ=0 polynomials match displays; `(4+4r−3σ)¹²`, 82 terms, degrees 0–13; majorant `9140.8458… < 10⁴`, equal to the disclosed rational |
| R5 | A7 | Exact rational model algebra: zero, elimination uniqueness, Jacobian, determinant, inverse, row sums, margins, endpoint arithmetic; `‖I−PDF‖` corner scan | All manuscript values confirmed (`−1/144`, `304/3`, `87/15/304/3/10/3`, margins, `30 > 11/4`, `103/144`); shrink-to-`K₀` step confirmed necessary and consistent |
| R6 | A8 | Paired polygamma scale at wedge-respecting parameters (n = 10⁸–10¹⁰, `d+2ρ ≤ n/1000`), z on the stadium rim; polygamma cross-checked against its defining series | Pair differences `O(1/(n⁵L_n))` with stable constants ≈ 6.3–7.0 and ≈ 38; A-term negligible; segments `Re ≥ 0.999n`; unpaired term `O(1/n⁵)` (no log gain) |
| R7 | A9 | Hermite–Genocchi: simplex masses; HG = recursive divided differences (exact Dirichlet-moment route + own cube-transform Gauss quadrature); Newton remainder; `720·mass = 1` | Exact on polynomials (z⁶, z⁷, z⁸, incl. noninteger node); ≤ `1.1·10⁻¹⁷` numeric for exp with complex node; remainder/bound forms verified |
| R8 | A3/A7/A10 + localization chain | Geometric tails; `|eʷ−1| ≤ 2|w|`; nesting angles; `C_loc` product arithmetic; (Q3),(Q1),(Q0); own derivation of the shifted ₃F₂ ODE (H3) and closed forms `P₃, P₂, P₁, P₀` incl. the decomposed forms; transported diagonal identity; ratio-free Jacobi lemma (J) via independently built Jacobi matrix (validated by Vieta + residuals) | All symbolic identities exact; (J) root inclusion held at all 13 tested (d,U,V) incl. boundary cases `U=V+d`, `V=32d`, with wide margins |
| R9 | A3 end-to-end | Direct moment computation of γ_H(M) vs assembled Theorem-21B main term; two-step ratio; `F(N+2)` subordination with full theta kernel | `γ_H/𝒢 − 1 = 0.0020` (M=120), `0.00057` (M=500), scale `log M/M`; two-step deviation ≈ `1.1/N`; subordination at 0.06 of the `L_N²/N²` scale |

**Paper-level re-derivations (no code):** the (C2) derivative computation
and the (C4)/(C5) coefficient extraction including `γ_G = 8γ_H`; the
`a′(s)` cancellation (assembly eq. 8; coefficient of `L′` is `K_s+1`);
`Log R_N = −1/(6N²)+O(1/N³)`; the `P_{2,m} ≥ n/8` chain (`(D+m)a ≥ 3n/8`,
`|b_{m+1}| ≤ n/4` via `C_loc√(Bd) ≤ 3n/16`, `2d+1 ≤ n/16`); the
maximum-argument boundary case `T_{d+1} = 0`; the stability lemma's Cauchy
step via the Genocchi form (constant exactly 1); the `E_F⁽⁶⁾` sign pattern;
the higher-mode geometric factor and region bounds; the strict-concavity
sign argument; the two connector estimates; the `B/D ≤ 6` and `V ≥ 256d`
box consequences.

---

## 5. Unchecked claims (explicit non-coverage)

1. **Lean build not rerun.** Static inspection only: no `sorry`/`admit`/
   `axiom`/`unsafe`/`native_decide` in the JensenWedge modules; all module
   statements match the formalization ledger (conditional certificate
   firewall; `hHG` named hypothesis; finite algebra only). The pinned
   toolchain build (`lake build Zeta23.Research.JensenWedge`) and
   `#print axioms` audit remain for the release pipeline.
2. **Primary-source PDFs not fetched** (GORZ v2, GORTTW v3, MSS, MMP v3);
   their quoted contents were checked for internal consistency against the
   packet's audit files only. The load-bearing normalization was verified
   against ξ itself (R1).
3. **Gershgorin off-diagonal chain:** the transported diagonal identity was
   verified exactly and the lemma's conclusion numerically (13 cases); the
   intermediate off-diagonal bounds were read but not re-expanded
   symbolically.
4. **Phase-14 `O_K(·)` constants:** limiting values, exact identities, and
   mean-value constants verified; the uniform hidden constants were checked
   for structure, not given independent explicit values.
5. **Repository regression scripts not rerun** (`leading_contour_check.py`,
   `scaled_branch.py`, `saddle_branch_check.py`, `six_coefficient_scan.py`,
   `root_radius_diagnostic.py`, `model_adapter.py`, frozen JSONs); R1–R9
   reproduce their essential content independently.
6. **The `10^1887` effectivity diagnostic** not rechecked; it is an
   extrapolation from an externally reported, unconverged coefficient,
   labeled as such, and enters no proof.
7. **Higher-theta suppression** verified on paper; not re-executed
   numerically beyond the single-mode complex point of R3.
8. **Finite small-n/small-d range** (absorbed by increasing `K`) checked
   logically, not computationally.

---

## 6. Formal separation statement

I am an AI system (Kimi, model `kimi-code/k3`, provider Moonshot AI). This
review is an **AI pre-review — not human review, not peer review** — and
must not be described as either. It is a genuine separated first pass: the
packet contained no prior review reports, author responses, finding
dispositions, or recalculation outputs, and none were sought; no session of
this model reviewed an earlier freeze; the reviewer differs in provider and
model from the two disclosed correlated Claude Opus 5 re-reviews.
Separation per `phase24/REVIEW_SEPARATION.md` is satisfied by provider
difference and absence of prior context. Tools: local Python
(sympy/mpmath) for reviewer-written recalculation scripts; read-only
same-model subagents for document compression; no network fetches. No
conflicts of interest. Companion scripts archive:
`~/Desktop/jensen_phase24_analytic_review_kimi_k3/independent_scripts/`.

**Bottom line: R1.** No mathematical defects; four P3 documentation repairs
(F1–F4); keep the embargo and the "awaiting human scrutiny" trust boundary
exactly as the manuscript states them.
