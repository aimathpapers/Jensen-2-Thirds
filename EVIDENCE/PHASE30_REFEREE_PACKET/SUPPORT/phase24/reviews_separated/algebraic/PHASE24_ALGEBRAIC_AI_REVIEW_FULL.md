# Phase 24 Algebraic Adversarial AI Pre-Review — Full Report

**Candidate:** `Jensen_Two_Thirds_Phase24_Algebraic_AI_Review_Packet`
**Manuscript:** *A Two-Thirds Hyperbolicity Wedge for Jensen Polynomials of Riemann's Xi-Function* (unified internal candidate, 17 Aug 2026)
**Candidate proof-source commit:** `8e2781b2dbe065754ba511f3f076abb7f00ab0c6`
**Required historical checkpoint:** `5f79158f9c6276dd09142edeea279e35b0d58406` — verified: is an ancestor of the candidate commit
**Review track:** Algebraic (separated AI pre-review)
**Review class:** AI pre-review — **not human review, not peer review**
**Date:** 2026-08-17
**Embargo:** confidential working mathematics; do not publish

---

## 0. Executive summary

I reviewed the Phase-24 algebraic packet as a separated first pass. I re-entered every decisive formula from the manuscript definitions, re-derived the symbolic identities in my own scripts, rebuilt the Lean target, ran the packet verifiers in their intended repository context, and audited the external citations.

**Result: no P0 (blocking) defect found in the algebraic layer.** Every decisive symbolic identity I recomputed independently matches the candidate: the limiting four-parameter system and its uniqueness, the quotient-to-six-coefficient adapter, the reversal/finite-free adapter and identity (F), the shifted ₃F₂ ODE with all four recurrence coefficients across the complete index range, the exact-rational interval ledger, the `C_loc = 12 + 8√6 < 32` localization arithmetic, and the finite multiplier/scaling steps. The Lean firewall builds cleanly (8710 jobs) with no proof escapes, and the packet's own fail-closed verifiers pass end-to-end.

**What remains unproven is the analytic certificate.** The sectorial saddle analysis, the order-six derivative tower, the parameter-branch convergence, the residual bound, and the assembly of a concrete `JensenWedgeCertificate` are paper-level mathematics, not Lean-formalized, and so far reviewed only by *correlated* AI passes (disclosed by the packet itself). The decisive-CAS common mode is also unbroken: the deferred clean-room Mathematica reconstruction (M1–M4) has not run. These two facts are the P1 items (both already disclosed in the packet) and drive the recommendations.

**Verdict:** conditional acceptance of the algebraic/symbolic layer; the candidate as a whole is a *credible proof candidate*, **not** a completed or formally verified theorem, until R1–R3 below are discharged.

---

## 1. Reviewer identification, tools, and COI/separation statement

- **Reviewer:** an AI system. Model `Qwen3.8-Max` accessed via OpenRouter, operating inside an agentic coding harness.
- **Tools:** Python 3.11 venv (`sympy 1.14.0`, `mpmath 1.3.0`, `numpy 2.0.2`), `elan`/`lake` with Lean toolchain `leanprover/lean4:v4.33.0-rc2`, `ripgrep`, targeted web search of primary-source records.
- **Independence:** this session began with only the packet contents. I read **no** prior review report, author response, finding disposition, or other-track instructions (none are in the packet). All decisive calculations were re-entered from manuscript definitions; frozen JSON/SymPy outputs were never loaded as inputs; Lean closed forms were transcribed by hand **only as comparison targets**, after independent derivation.
- **Correlated-re-review disclosure (required):** I have not reviewed any earlier freeze of this candidate. The repository's `ASSUMPTION_REGISTRY.md` (row `C48-REVIEW`) discloses that the preceding freeze received *correlated* Claude Opus 5 re-reviews that retained prior context and therefore failed the separation gate. That reviewer is a different model family/provider from me; I classify **this** pass as a separated first pass on the algebraic track, with the caveat below.
- **Common-mode caveat (stated plainly):** all of my symbolic recomputation used **SymPy**, the same CAS family as the repository's producers. I mitigated this with method-independent cross-checks (hand elimination and Gröbner bases, exact-rational `Fraction` arithmetic, a symmetric Jacobi matrix re-entered from the Szegő three-term recurrence, 40–50-digit mpmath residual/root evaluations, and an independent ξ(1/2) computed from mpmath `zeta`/`gamma`). Shared-CAS correlation nevertheless cannot be fully excluded by this pass; that is exactly why the packet's deferred clean-room **Mathematica** reconstruction is the correct remaining safeguard (recommendation R1).

---

## 2. Packet integrity and candidate fidelity

| Check | Result |
|---|---|
| `python3 VERIFY_BUNDLE.py` | **PASS** — 107 files, all SHA-256 match |
| Packet manuscript vs candidate commit `8e2781b` | **byte-identical** |
| Packet Lean modules (LeadingSystem, QuotientAdapter, DirectRecurrence, MultiplierStability, ConditionalAssembly, JensenPolynomial, DominantMaximum) vs `8e2781b` | **all byte-identical** |
| Packet `INTERVAL_CERTIFICATES.json`, `verify_interval_certificates.py`, `PRIMARY_SOURCE_AUDIT.md` vs `8e2781b` | **byte-identical** |
| `git diff 8e2781b..HEAD` | packaging/release files **only** (build scripts, packet zips, manifests); no manuscript or Lean changes |
| Checkpoint `5f79158f` | verified ancestor of `8e2781b` |

Consequence: building the live repository working tree verifies the candidate's Lean claims faithfully.

---

## 3. Gate table (B1–B11)

Status legend — **VERIFIED**: independently recomputed from definitions and passing. **LEAN-CHECKED**: kernel-checked (build succeeds) and statement/scope audited. **PAPER-LEVEL**: structurally sound and internally consistent, conventional paper mathematics, not formalized and not re-proven by me. **EXTERNAL**: depends on a cited primary source; hypothesis applicability checked.

| Gate | Claim | Status | Evidence / basis |
|---|---|---|---|
| **B1** | Limiting 4-parameter system; positive-orthant uniqueness; solution `(3,2,16/3,1/3)`; Jacobian; `det`; inverse norm | **VERIFIED** + Lean-checked | RC-1 (§4.1): residual exactly 0; uniqueness by elimination **and** lex Gröbner basis; `det DF(y_*) = -1/144`; `‖DF⁻¹‖∞ = 304/3`; inverse equals Lean `gaugeJacobianInv` entrywise. Lean `LeadingSystem.lean` checks candidate, determinant, two-sided inverse, uniqueness (including derivation of `t>1` from `t,w>0`). |
| **B2** | 4 quotient coordinates + 2 normalizations ⇒ exactly 6 coefficient matches; orientation; nonzero/log hypotheses | **VERIFIED** (algebra) / **PAPER-LEVEL** (nonzero/log input) | RC-2 Part A: quotient map invertible given nonzero `(a₀,a₁)`; induction `c_{k+2}=2c_{k+1}−c_k`, `c₀=c₁=0` kills `c₂..c₅` (exact symbolic); matches Lean `QuotientAdapter.lean`. Nonzero/log hypotheses reduce to γ(n+j)>0 — confirmed numerically from the Mellin integral (RC-2 B.3); the general positivity obligation is paper-level (Theorem 21B nonvanishing). |
| **B3** | Eventual parameter ordering and degree-dependent Jacobi hypotheses via the exact rational interval ledger | **VERIFIED** (ledger arithmetic) / **PAPER-LEVEL** (eventual membership) | RC-5 (§4.5): every ledger quantity re-derived in `Fraction`, no floats: margins, `α/e≥30>11/4≥t+we`, `t−1−δe≥103/144>0` ⇒ `A>B>C>D>0`; saddle margins `151/200>9/16` and `151/50`; `B/D≤6`; endpoint positivity ⇔ `B,D≥256d`; `K₀=262144`. That the branch eventually lies in the box is the paper-level contraction argument (U3). |
| **B4** | Ascending/descending reversal adapter for multiplicative finite-free convolution | **VERIFIED** | RC-4 (§4.4): MSS signed-coefficient formula sanity-checked (d=1, d=2 diagonal cases); `(p⊠_d q)^∨ = p^∨⊠_d q^∨` symbolically (generic d=4) and on 5 exact-rational random instances; **identity (F)** `q_{A,B}⊠_d q_{C,D}(D·) = ₃F₂(−d,A,C;B,D;Dy/(AC))` exact in ascending constant-term-one form; reversal reciprocates roots and preserves log mesh. |
| **B5** | MMP v3 Prop 2.7(iii) & 2.17 hypotheses; positive roots; strict log mesh; simplicity; nonzero constant term | **EXTERNAL** (hypotheses checked) | Jacobi factors: positive simple roots (RC-6, two independent root methods, residuals ≤2.1e-13), full degree d; `p_F(0)=1`. MMP genuinely develops finite-free positivity preservation and log-mesh control (web-verified). Exact proposition text rests on the hash-frozen arXiv v3; paywalled IMRN PDF not byte-compared (packet-disclosed). See F-P2-1 for a convention pin. |
| **B6** | Ratio-free Jacobi/Gershgorin bound; provisional threshold 256; multiplicative interval; MSS published Thm 1.6; `C_loc=12+8√6<32`, no circular constants | **VERIFIED** (arithmetic + numeric localization) | RC-5 + RC-6 (§4.5–4.6): constant order non-circular (`K_pre=256` fixed **before** `C_loc`; `K₀=max(256,256·C_loc²)` after); single-factor interval `[V−8√(Vd), V+8√(Vd)]` confirmed in 6 cases; product interval and `|y−B|≤C_loc√(Bd)` confirmed in 3 branch-like cases (exact rationals, 40-digit roots, all real). MSS number correction consistent with independent web check (§6). |
| **B7** | Shifted ₃F₂ ODE and all four recurrence coefficients, complete index range | **VERIFIED** + Lean-checked | RC-3 (§4.3): generic ₃F₂ ODE verified at series-coefficient level; all four `P_{i,m}` derived independently via Euler-operator/Stirling expansion and equal to Lean closed forms; recurrence `ΣᵢP_{i,m}T_{m+i}≡0` holds as an **exact polynomial identity** on genuine ₃F₂ polynomials for **all** `0≤m≤d`, 5 parameter tuples (d=5,6,7,8,10); derivative-shift identity verified. Lean checks the four closed forms. |
| **B8** | Central coefficient lower bound in the non-perturbative `(C−D)/C→1/2` regime | **VERIFIED** (closed form + arithmetic) / **PAPER-LEVEL** (estimate inputs) | Decomposition `P_{2,m}=b_{m+1}+(D+m)a+ε_p(y/A)(A−d+3+3m)` matches Lean `recurrenceP2_closed` (RC-3). Arithmetic of `P_{2,m}≥n/8` re-checked: `|b_{m+1}|≤3n/16+n/16=n/4`, `(D+m)a≥(n/2)(3/4)=3n/8` ⇒ `≥n/8`. The `ε_p→1/2` term has favorable sign and is **not** required to be small — the non-perturbative claim is structurally sound. |
| **B9** | Neighbor coefficient bounds and maximum argument producing radius `O(√(Bd))` | **LEAN-CHECKED** (maximum step) / **PAPER-LEVEL** (coefficient bounds) | Lean `DominantMaximum.lean` kernel-checks the finite contradiction (`u_k≤qM`, `q<1`, `u₀,u₁≤1` ⇒ `M≤1`). Bounds `(N3) |P₃|≤2`, `(N1) |P₁|≤C₁(n√(Bd)+nd)`, `(N0) 0≤P₀≤C₀n²d` are paper-level; the mandatory `(P1-dec)` cancellation decomposition matches the verified symbolic structure. |
| **B10** | Multiplier sign-transfer hypotheses, exterior intervals, continuity, distinctness | **LEAN-CHECKED** | Lean `MultiplierStability.lean`: exact geometric tail `Σ_{k≥5}2^{-k}=1/16`; sharp threshold `ε<16`; sign preservation under relative error <1; IVT construction of one distinct positive root per disjoint sign-changing interval. `MultiplierIntervalCertificate` carries exterior intervals, continuity, separation. Newton/derivative identity and five-match vanishing verified by hand. |
| **B11** | Positive-to-negative Jensen scaling and concrete binomial Jensen definition | **LEAN-CHECKED** | Lean `JensenPolynomial.lean`: `J^{d,n}(X)=Σⱼ C(d,j)γ(n+j)Xʲ` — matches the standard GORZ convention. `ConditionalAssembly.lean`: positive roots of the transformed polynomial map to d distinct **negative** roots of J via `y=−SX`, `S>0`, `normalization≠0`. Logic audited and sound. |

---

## 4. Independent recalculation record (full logs)

Scripts (entered from manuscript definitions; no frozen artifacts read as input): `output/phase24_algebraic_review/rc1_leading_system.py`, `rc2_branch.py`, `rc3_recurrence.py`, `rc4_reversal.py`, `rc5_intervals.py`, `rc6_jacobi_roots.py`. Environment: SymPy 1.14.0, mpmath 1.3.0, NumPy 2.0.2 (Python 3.11).

### 4.1 RC-1 — leading system and Jacobian (Gate B1) — **PASS**

Definitions re-entered: `F = H^∞ + S^∞` with
`H^∞ = (1/α + w/t² + δ, w/t³ + δ, 3w/t⁴ + 3δ, 4w/t⁵ + 4δ)`, `S^∞ = (−2,−1,−2,−2)`.

- `F(3, 2, 16/3, 1/3) = (0,0,0,0)` exactly.
- Uniqueness by hand-elimination: `F₂−F₃/1 ⇒ w(t−1)/t⁴=1/3`, `F₃−F₄ ⇒ w(t−1)/t⁵=1/6` ⇒ `t=2` forced; then `w=16/3`, `δ=1/3`, `α=3` forced. Cross-checked with a lex Gröbner basis of the denominator-cleared system, which contains `w(t−2)`, `w(3w−16)`, `w(3δ−1)`, `αt³−t³−3w` — zero-dimensional, unique positive solution.
- Jacobian in gauge order `(α,t,w,δ)`:

```
[ -1/9  -4/3   1/4   1 ]
[  0     -1    1/8   1 ]
[  0     -2   3/16   3 ]
[  0    -5/3  1/8   4 ]
```

- `det DF(y_*) = −1/144` (manuscript value confirmed; Lean `gaugeJacobian_det` agrees; the algebraic-order `leadingJacobian` has determinant `+1/144`, the sign flip being the odd column permutation, exactly as Lean documents).
- `‖DF(y_*)⁻¹‖∞ = 304/3` (row sums: 87, 15, 304/3, 10/3).
- My exact inverse equals Lean `gaugeJacobianInv` entry-for-entry.

### 4.2 RC-2 — quotient adapter, Mellin kernel, normalization (Gate B2 + T1 inputs) — **PASS**

**Part A (exact algebra).** Quotient coordinates `q_k = a_{k+2}a_k/a_{k+1}²`: reconstruction `a_{k+2}=q_k a_{k+1}²/a_k` is well-defined for nonzero `a₀,a₁` and reproduces the `q_k` exactly (rational identities). Second-difference form: `c_{k+2}=2c_{k+1}−c_k` with `c₀=c₁=0` gives `c₂=…=c₅=0`. Six coefficients from four quotients + two normalizations; orientation (forward induction) correct.

**Part B (independent high-precision numerics, mpmath dps=45).** Kernel `f(u)=ω(e^{2u})e^{u/2}` with `ω(t)=t²Θ″+(3/2)tΘ′`, `Θ(t)=Σ_{m≥1}e^{−πm²t}` (direct series for t≥1; modularity `θ(t)=t^{−1/2}θ(1/t)` for t<1):

```
B.1 evenness at u=0.5: f(+u)=0.0150943629461 f(-u)=0.0150943629461 rel.diff=6.35e-46
B.1 evenness at u=0.9: f(+u)=2.90731254768e-6 f(-u)=2.90731254768e-6 rel.diff=2.16e-41
B.1 evenness at u=1.3: f(+u)=1.41135263245e-15 f(-u)=1.41135263245e-15 rel.diff=5.14e-32
```

Evenness is what converts `ξ(1/2+w)=4∫_{−∞}^{∞}f(u)e^{wu}du` into `8∫_0^∞ f(u)cosh(wu)du`, i.e., it validates the factor-8 structure of eq. (eq:factor8).

**Normalization anchor (fully independent):**

```
B.2 normalization: xi(1/2)=0.49712077818831  8*int f=0.49712077818831  rel.diff=0.0
```

ξ(1/2) computed from `ξ(s)=½s(s−1)π^{−s/2}Γ(s/2)ζ(s)` with mpmath `zeta`/`gamma`; `8∫₀^∞f` from my Mellin-kernel quadrature. Match to all displayed digits (<1e-14). This independently confirms the **factor-eight** identity.

**Positivity (nonzero/log hypothesis input):**

```
gamma(5)  = 1.75392309121e-9   positive=True
gamma(10) = 2.04042256129e-18  positive=True
gamma(15) = 1.13827818679e-27  positive=True
```

**Informational only (not counted as verification):** raw log-moment curvature vs the tower's leading form, with the paper's saddle `L_{2x−2}`:

```
x=35: L=2.24225  h''=0.0164633  h''*x*L/2=0.64601
x=55: L=2.57393  h''=0.00969553 h''*x*L/2=0.686279
```

I could not pin down the tower's exact "moment normalization" independently, and `O(1/L)` corrections are large at reachable x (L≈2–2.6), so these ratios are suggestive only. The tower (constants `2,−2,4,−12,48`) remains a SymPy-checked artifact whose clean-room second-CAS reconstruction (M1) is still deferred — see U2 and R1.

### 4.3 RC-3 — shifted ₃F₂ ODE and recurrence (Gate B7) — **PASS**

- Generic ₃F₂ ODE `[θ(θ+b₁−1)(θ+b₂−1) − z(θ+a₁)(θ+a₂)(θ+a₃)]g=0` verified from the series definition (coefficient residual simplifies to 0).
- Euler-operator expansion (Stirling numbers) gives the four coefficients; comparison with Lean closed forms (transcribed by hand):

```
Part2: P3 matches Lean closed form: True
Part2: P2 matches Lean closed form: True
Part2: P1 matches Lean closed form: True
Part2: P0 matches Lean closed form: True
P3 = (AC − Dy)/(AC)
P2 = [AC(B+D+2m+1) − Dy(A+C−d+3m+3)]/(AC)
P0 = Dy(A+m)(C+m)(d−m)/(AC)
```

- Exact polynomial-identity check of `P₃T_{m+3}+P₂T_{m+2}+P₁T_{m+1}+P₀T_m ≡ 0` with `T_k=y^k p_F^{(k)}/p_F`, on genuine `₃F₂(−d,A,C;B,D;(D/AC)y)` polynomials with rational parameters, **all** `0≤m≤d`:

```
tuples: (d=6,A=40,B=12,C=11,D=6), (d=8,A=120,B=16,C=15,D=8),
        (d=10,A=300,B=20,C=19,D=10), (d=5,A=7/2,B=3,C=5/2,D=3/2),
        (d=7,A=50,B=9,C=17/2,D=4)
Part3: recurrence identity holds for all (d,m) across 5 tuples: True
Part3b: p_F^(m) == prefactor * shifted _3F_2 (same lambda): True
```

This covers the packet's "genuine exact polynomial at multiple orders" obligation, across the **complete** index range (including `m=d−1`, `m=d` where `P₀` degenerates correctly).

### 4.4 RC-4 — reversal adapter and identity (F) (Gate B4) — **PASS**

- MSS signed-coefficient rule `(p⊠_d q)_k = (−1)^k p_k q_k / C(d,k)` (descending monic inputs) sanity-checked on d=1 (`x−a ⊠ x−b = x−ab`) and d=2 diagonal rank-one cases.
- Reversal identity `(p⊠_d q)^∨ = p^∨⊠_d q^∨`: symbolic verification with generic coefficients (d=4) **and** 5 random exact-rational positive-root instances (d=5).
- **Identity (F)** in ascending constant-term-one normalization, exact rationals, d=6 with `(A,B,C,D)=(39,13,25/2,6)`:

```
3. identity (F): q_{A,B} x_d q_{C,D}(D.) == _3F_2(-d,A,C;B,D;Dy/(AC)): True
```

- Reversal maps positive roots to reciprocals and preserves logarithmic mesh (exact check).

### 4.5 RC-5 — interval ledger arithmetic (Gates B3/B6) — **PASS**

All in `fractions.Fraction`, zero floating point:

```
margins:               (1/2,1/2) (1/4,1/4) (1/3,2/3) (1/12,1/12)
A numerator min:       30      B numerator max: 11/4    (30 > 11/4)
C−D numerator min:     103/144 > 0
saddle perturbation:   49/200  lower 151/200 > 9/16
reduced denominator:   49/50   lower 151/50
B/D max:               6
endpoint positivity:   8√(Bd) ≤ B/2  ⇔  B ≥ 256d  (same for D)
C_loc:                 12 + 8√6,  √6 < 5/2 (since 24<25)  ⇒  C_loc < 32
K0:                    256 · 32² = 262144
cross term:            64·(1/16) = 4;  8 + 4 = 12 constant part, 8√6 radical part
```

The deviation algebra `|(B+u)(1+v)−B| ≤ 8√(Bd) + 8B√(d/D) + 64√(Bd)√(d/D) ≤ (12+8√6)√(Bd)` re-derived: `8B√(d/D) = 8√(Bd)√(B/D) ≤ 8√6√(Bd)` (coarse box `B/D≤6`) and `64√(d/D) ≤ 4` (provisional `D≥256d`). The order of constants is non-circular: `C_J=8` → provisional `K_pre=256` → `C_loc` → `K₀=max(256,256C_loc²)` → `K_r` → eventual thresholds, matching §9 of the phase-16 note.

### 4.6 RC-6 — Jacobi localization numerics (Gate B6) — **PASS**

**Single-factor ratio-free lemma** `roots(q_{U,V}) ⊂ [V−8√(Vd), V+8√(Vd)]` for `U≥V+d`, `V≥32d`, with `q_{U,V}(y)=₂F₁(−d,U;V;y/U)`. Roots computed via the symmetric Jacobi matrix re-entered from the Szegő recurrence (`α=V−1`, `β=U−V−d`, transport `y=U(1−t)/2`), then verified by 50-digit Horner evaluation of `q_{U,V}` at each candidate root:

```
d=  5 U= 400.0 V= 320.0 interval [     0.00,  640.00] in-interval=True residual<4.3e-16 distinct=True
d=  8 U= 600.0 V= 400.0 interval [   -52.55,  852.55] in-interval=True residual<4.2e-15 distinct=True
d= 10 U= 900.0 V= 320.0 interval [  -132.55,  772.55] in-interval=True residual<2.2e-14 distinct=True
d= 12 U=1500.0 V= 384.0 interval [  -159.06,  927.06] in-interval=True residual<2.1e-13 distinct=True
d=  6 U=1000.0 V= 192.0 interval [   -79.53,  463.53] in-interval=True residual<1.4e-15 distinct=True
d=  4 U= 300.0 V= 128.0 interval [   -53.02,  309.02] in-interval=True residual<1.3e-16 distinct=True
```

Note the intervals legitimately extend below 0 at the minimal `V=32d` (coarse localization); positivity of the roots comes from the separate classical Jacobi parameter conditions, as the candidate states.

**Product/localization step.** For branch-like parameters satisfying the full coarse box (`A≥8B`, `C≥D+d`, `B,D≥256d`), build `p_F=₃F₂(−d,A,C;B,D;(D/AC)y)` in exact rationals and find roots at 40 digits:

```
d=6  A=40000  B=4000  C=4000  D=2000:  product interval=True  |y−B|≤C_loc√(Bd)=True  (rad=4894.819, imag=0)
d=8  A=60000  B=6000  C=6000  D=3000:  product interval=True  |y−B|≤C_loc√(Bd)=True  (rad=6922.319, imag=0)
d=10 A=100000 B=10000 C=10000 D=5000:  product interval=True  |y−B|≤C_loc√(Bd)=True  (rad=9991.507, imag=0)
```

All roots real (imag ≤ 0 at 40 digits), inside the factor-product interval `[(B−8√(Bd))(1−8√(d/D)), (B+8√(Bd))(1+8√(d/D))]`, and inside the `C_loc` radius. This is numerical evidence for the MSS 1.6 consequence on genuine instances (the theorem itself remains the external input).

---

## 5. Repository-side verification (supplementary, not independent)

Run in the intended repo-root context against the candidate-identical working tree:

```
PASS phase24 exact interval certificates
PASS phase24 release-source checks
PASS mutation rejected: wedge exponent
PASS mutation rejected: review overclaim
PASS mutation rejected: factor-eight factorial
PASS mutation rejected: factor-eight kernel weight
PASS mutation rejected: critical-point radius
PASS mutation rejected: Lean proof escape
PASS mutation rejected: missing headline import
PASS mutation rejected: malformed source hash
PASS mutation rejected: CAS clean-room rule
PASS mutation rejected: branch-box point
PASS all phase24 mutation tests
PASS manuscript factor-eight equation regression (n=0..4, max relative error 2.3963e-37)
PASS manuscript critical-point radius regression (correct K_r=0.880246, stale-scale ratio=14681.5)
PASS all Phase-24 manuscript equation regressions
Build completed successfully (8710 jobs).
PASS Phase 24 formalization, interval, and mutation gates
```

Additional checks I ran myself:
- `lake build Zeta23.Research.JensenWedge` (pinned toolchain v4.33.0-rc2): **success, 8710 jobs**.
- Escape scan over all JensenWedge Lean sources for `sorry|admit|axiom|unsafe|native_decide|implementedBy`: **none found**.
- Lean trust-boundary audit: every module's docstring accurately states what is kernel-checked vs. what is a paper-level hypothesis (Hermite–Genocchi `hHG`, Rouché/branch, repeated-FTC, certificate construction). `KNOWN_LIMITATIONS.md`, `FORMALIZATION_LEDGER.md`, and `PAPER_THEOREM_INVENTORY.md` are mutually consistent and consistent with the Lean sources.

---

## 6. External-citation audit (B5/B6 seam)

- **MSS theorem number.** The candidate cites **published MSS Theorem 1.6** for `maxroot(p⊠_d q) ≤ maxroot(p)·maxroot(q)` and records that Holland's Lemma 7.1 cites **Theorem 1.13** at the same point. Independent web audit of the MSS literature confirms the **S-transform inequality** (the strictly stronger multiplicative bound) is Theorem **1.13** in the published paper, while the coarse largest-root product inequality is a separate earlier result. This is consistent with the packet's seam correction and indicates the renumbering is a genuine source-fidelity fix, not a transcription slip. The coarse bound is mathematically sound and exactly what the interval lemma consumes; the reciprocal-polynomial argument for the lower endpoint is elementary and re-derived in the phase-16 note.
- **MMP.** Web audit confirms MMP (IMRN 2024; arXiv:2309.10970) develops real-rootedness/positivity preservation under multiplicative finite-free convolution and introduces logarithmic-mesh control, matching the recorded scope of Props 2.7(iii) and 2.17. Exact proposition text/numbering rests on the packet's hash-frozen v3 PDF+source (hashes in `SOURCE_HASHES.sha256`); the paywalled journal PDF was not byte-compared (disclosed). See F-P2-1.
- **Holland (arXiv:2608.08682v1).** Not independently retrieved (hash record only). Not load-bearing: the `DEPENDENCY_MATRIX.md` shows Holland's Thm 1.1, Lemma 6.1, and assembled Lemma 7.3 are **not used**; the candidate re-derives the quotient architecture, four-parameter branch, residual, and recurrence, and cites MMP/MSS directly. Consistent with the manuscript's "Holland's main theorem is not a premise."
- **GORZ/GORTTW conventions.** The Jensen definition `J^{d,n}(X)=Σ C(d,j)γ(n+j)Xʲ` and the ξ convention `ξ(1/2+w)=Σγ(n)w^{2n}/n!` match the standard printed conventions; the factor-8 reconciliation with the GORZ main term was independently confirmed numerically (§4.2).

---

## 7. Findings (P0–P3)

Severity: **P0** blocks acceptance; **P1** major, must address before any external claim; **P2** should address; **P3** minor.

### P0 — none
No fatal defect found in any independently recomputed identity or in the formal firewall.

### P1
- **F-P1-1 — The theorem is conditional, not unconditionally established (disclosed).** The end-to-end Lean theorem requires constructing a `JensenWedgeCertificate` for the xi coefficients; no such construction exists. The analytic core (Lemma S Rouché/branch; sectorial asymptotic Thm 21B; order-six tower; parameter-branch existence/convergence; order-six residual bound) is paper-level, not Lean-formalized, and has so far received only *correlated* AI review per the packet's own `C48-REVIEW` row. Any circulation must describe this as a proof candidate with an unformalized analytic core — never as a proved or formally verified theorem.
- **F-P1-2 — Decisive-CAS common mode unbroken (disclosed).** The exact symbolic identities rest on SymPy/Lean paths only. The designated safeguard — clean-room Mathematica reconstruction M1–M4 (`MATHEMATICA_FOLLOWUP.md`) — has **not run**. My pass also used SymPy (§1), so it does not discharge this item.

### P2
- **F-P2-1 — Pin the logarithmic-mesh convention.** The candidate uses `lmesh = min λ_{j+1}/λ_j ≥ 1` with `lmesh(p⊠q) ≥ lmesh(p)`; some MMP-family literature uses the reciprocal `≤1` convention. The mathematical conclusion (distinct positive roots of `p_F`) is robust — distinct positive roots of the first Jacobi factor give mesh `>1` in the candidate's convention, positivity is preserved by Prop 2.7(iii), and `p_F(0)=1` — but the exact Prop 2.17 statement/direction should be quoted verbatim from the frozen v3 text to eliminate ambiguity.
- **F-P2-2 — `H₆` majorant not independently reproduced.** The manuscript's degree-13/82-term numerator with coefficientwise majorant `<10⁴` on `|r|,|σ|≤7/50` (giving `|G₀⁽⁶⁾| ≤ 20000/(|N|⁵ log|N|)`) is item M4 of the deferred Mathematica work. Land the majorant value in the exact-rational interval ledger once M4 runs so the constant is auditable like the others.

### P3
- **F-P3-1 — Effectivity is existential.** `K` is effective-in-principle, not numerically propagated (disclosed). Keep all numerical-`K` claims out of any abstract.
- **F-P3-2 — Print all four recurrence coefficients.** The manuscript displays only `P₃` and `P₀`; since the radius argument leans on the decomposed `P₁` cancellation, printing all four (short) forms in an appendix would help human readers.
- **F-P3-3 — Paywalled MMP PDF not byte-compared** (arXiv v3 pinned instead; disclosed). Note it wherever the published record is cited.

---

## 8. Unchecked / unverified source hypotheses (record)

U1–U6 are already disclosed by the packet; U7–U9 are items I could not independently close.

- **U1.** Lemma S: Rouché, holomorphic branch patching, uniform logarithmic asymptotics — paper-level (Lean checks only finite denominator/norm margins).
- **U2.** Order-six derivative tower (constants `2,−2,4,−12,48`): SymPy-checked artifact; my independent numerics could not pin down the exact normalization (§4.2); discharge via M1.
- **U3.** Positive parameter branch existence/uniqueness/convergence (`y_n−y_*=O(L_n^{-1})`) via contraction on `K₀`: paper-level `C¹` estimate; finite inverse algebra Lean-checked.
- **U4.** Full six-simplex Hermite–Genocchi equality: named hypothesis `hHG` in Lean; line-segment FTC and exact `1/720` adapter are checked.
- **U5.** Elementary `C¹` cube-integral identity and differentiation under all parameter integrals: paper-level; unit-cube/denominator/reciprocal-power/integral bounds Lean-checked.
- **U6.** Construction of the `JensenWedgeCertificate` (the entire analytic certificate): not performed.
- **U7.** Byte-level verification of MMP Prop 2.7(iii)/2.17 and MSS Thm 1.6 exact statements against the frozen PDFs (binaries not committed; hash records only). I verified scope via web search, not the exact frozen bytes.
- **U8.** Holland v1 retrieval/verification (hash record only).
- **U9.** `H₆` coefficientwise majorant (`<10⁴`, 82 terms, degree 13): not independently re-derived (M4).

---

## 9. Recommendations

- **R0 (blocking before any external claim):** maintain embargo and the "AI pre-review only" label until R1–R3 are addressed. Never describe the candidate as a proved/formally verified theorem (F-P1-1).
- **R1 (highest technical priority): run the clean-room Mathematica reconstruction M1–M4.** It is the only remaining safeguard against SymPy common-mode error on the decisive symbolic identities, and no SymPy-based pass (including mine) can substitute. Any `MISMATCH` is a release blocker, per the follow-up document's own rules.
- **R2: commission a separated analytic-track review** (different provider or genuinely context-free session, prior reports excluded) for the saddle → tower → branch → residual → finite-free chain (U1–U6). This algebraic pass deliberately does not vouch for those estimates.
- **R3 (low-cost hardening):** (a) pin the log-mesh convention and quote MMP Prop 2.17 verbatim from frozen v3 (F-P2-1); (b) land the `H₆` majorant in the interval ledger after M4 (F-P2-2); (c) print all four recurrence coefficients in an appendix (F-P3-2); (d) keep existential-`K` language unchanged (F-P3-1).

---

## 10. Overall assessment

The algebraic skeleton of the two-thirds wedge candidate is, to the extent independently recomputed here, **correct and consistent**: leading system and uniqueness, quotient adapter, reversal and identity (F), shifted ₃F₂ ODE and all four recurrence coefficients over the complete index range, the exact-rational interval ledger, the `C_loc=12+8√6<32` localization arithmetic, and the finite multiplier/scaling steps all pass from-scratch checks; the Lean firewall builds cleanly with no proof escapes; the external seams were audited and the MSS theorem-number correction appears genuine and correct.

What is **not** established is the **analytic certificate** and its assembly into a `JensenWedgeCertificate`: that core remains conventional paper mathematics, so far reviewed only by correlated AI passes, with the decisive-CAS common mode not yet broken by a second CAS. The packet discloses all of this honestly and thoroughly, which is to its credit.

**Verdict (algebraic track):** no P0; conditional acceptance of the algebraic/symbolic layer; the candidate as a whole is a **credible proof candidate, not yet a completed or formally verified theorem**, subject to R1–R3.

---

## Appendix A — Reproducibility

- Reviewer scripts: `output/phase24_algebraic_review/rc1_leading_system.py`, `rc2_branch.py`, `rc3_recurrence.py`, `rc4_reversal.py`, `rc5_intervals.py`, `rc6_jacobi_roots.py` (all self-contained; requirements: `sympy`, `mpmath`, `numpy`).
- Packet verification: `python3 VERIFY_BUNDLE.py` from the packet directory (PASS, 107 files).
- Repo verifier: `C48_PYTHON=<venv>/bin/python ELAN_HOME=$HOME/.elan bash ground_zero_work/phase24/verify_phase24.sh` (PASS, log above).
- Lean: `lake build Zeta23.Research.JensenWedge` in `Kimi_Agent_Riemann Lean Exploration/zeta-23-lean` with pinned toolchain `leanprover/lean4:v4.33.0-rc2`.

---

*Prepared by an AI reviewer (Qwen3.8-Max via OpenRouter) as a separated algebraic-track pre-review. This document is an AI pre-review; it is not human review and not peer review. Confidential working mathematics — do not publish.*
