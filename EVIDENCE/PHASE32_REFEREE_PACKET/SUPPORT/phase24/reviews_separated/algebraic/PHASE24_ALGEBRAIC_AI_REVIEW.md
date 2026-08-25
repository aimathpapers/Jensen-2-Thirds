# Phase 24 Algebraic Adversarial AI Pre-Review

**Candidate:** `Jensen_Two_Thirds_Phase24_Algebraic_AI_Review_Packet`
**Candidate proof-source commit:** `8e2781b2dbe065754ba511f3f076abb7f00ab0c6`
**Required historical checkpoint:** `5f79158f9c6276dd09142edeea279e35b0d58406` (verified: is an ancestor of the candidate commit)
**Review track:** Algebraic
**Review class:** Separated AI pre-review. **Not human review, not peer review.**
**Date:** 2026-08-17
**Embargo:** Confidential working mathematics; do not publish.

---

## 1. Reviewer identification, tools, and separation statement

- **Reviewer:** an AI system. Model `Qwen3.8-Max` accessed via OpenRouter, operating inside an agentic coding harness (file/shell editing, SymPy, mpmath, NumPy, a Lean 4 toolchain, and web search).
- **Tools actually used:** Python 3.11 venv with `sympy 1.14.0`, `mpmath 1.3.0`, `numpy 2.0.2`; `elan`/`lake` with Lean toolchain `leanprover/lean4:v4.33.0-rc2`; `ripgrep`; targeted web search of primary-source records.
- **Access to prior work / independence:** I began this session with **only** the packet contents. I did **not** read any prior review report, author response, finding disposition, or the other track's instructions, and none are present in the packet. I reconstructed every decisive calculation from the manuscript definitions and did **not** load frozen JSON, SymPy producer output, or Lean closed forms as *inputs* to my independent computations (I transcribed Lean closed forms only as *comparison targets*, and I re-derived the mathematics before comparing).
- **Correlated-re-review disclosure (required by the packet):** I have **not** reviewed an earlier freeze of this candidate, in this or (to my knowledge) any prior session. The repository's own `ASSUMPTION_REGISTRY.md` (row `C48-REVIEW`) discloses that the preceding freeze received *correlated* AI re-reviews (Claude Opus 5) that retained prior context and therefore failed the separation gate. That prior reviewer is a **different model family/provider** from me. I therefore classify **this** pass as a genuinely separated first pass **on the algebraic track**, with the caveat below.
- **Residual common-mode caveat (stated plainly):** all of my symbolic recomputation used **SymPy**, the same CAS family as the repository's producers. I mitigated this where possible with method-independent cross-checks (hand elimination and Gröbner bases, exact-rational arithmetic, a symmetric Jacobi matrix re-entered from the Szegő recurrence, 50-digit mpmath residual evaluation, and an independent ξ(1/2) from mpmath's `zeta`/`gamma`). Nevertheless, a shared-CAS correlation cannot be fully ruled out by this pass; that is precisely why the packet's deferred clean-room **Mathematica** reconstruction (see R1) is the correct remaining safeguard, and I endorse it.

**Bottom line of this section:** this is an independent-track, context-free AI algebraic pre-review, not human or peer review; its one structural weakness is shared-CAS (SymPy) common mode, disclosed above and addressed by recommendation R1.

---

## 2. Bundle integrity

- `python3 VERIFY_BUNDLE.py` → **PASS** (107 files, all SHA-256 match).
- I byte-compared the packet against the candidate commit `8e2781b` in the live repository: manuscript, all seven headline Lean modules, `INTERVAL_CERTIFICATES.json`, `verify_interval_certificates.py`, and `PRIMARY_SOURCE_AUDIT.md` all **MATCH**. The packet is a faithful subset of the candidate.
- `git diff 8e2781b..HEAD` touches **only** packaging/release files (build scripts, review-packet zips, manifests); no manuscript or Lean content changed. So building the live working tree verifies the candidate's Lean claims.

---

## 3. Gate table (B1–B11)

Legend for **Status**:
- **VERIFIED** = I independently recomputed it from definitions and it passes.
- **LEAN-CHECKED** = kernel-checked in Lean (build succeeds), and I audited the statement/scope.
- **PAPER-LEVEL** = structurally sound and internally consistent, but the obligation is conventional paper mathematics not yet formalized and not independently re-proven by me.
- **EXTERNAL** = depends on a cited primary source; hypothesis applicability checked, source statement audited to the extent possible.

| Gate | Claim | Status | Basis |
|---|---|---|---|
| **B1** | Limiting 4-parameter system; positive-orthant uniqueness; solution `(3,2,16/3,1/3)`; Jacobian `det=-1/144`; `‖DF⁻¹‖∞=304/3` | **VERIFIED** (+ Lean-checked) | RC-1: residual at `y_*` is exactly 0; elementary elimination **and** a lex Gröbner basis give uniqueness (basis contains `w(t-2)`, `w(3w-16)`, `w(3δ-1)`); `det=-1/144`; `‖DF⁻¹‖∞=304/3`; my inverse equals Lean `gaugeJacobianInv` entry-for-entry. Lean `LeadingSystem.lean` also checks candidate, determinant, both-sided inverse, and uniqueness. |
| **B2** | Four quotient coordinates + two normalizations ⇒ exactly six coefficient matches; orientation and nonzero/log hypotheses | **VERIFIED** (algebra) / **PAPER-LEVEL** (nonzero/log inputs) | RC-2 Part A: quotient coordinates are invertible given nonzero `(a0,a1)`; second-difference induction `c_{k+2}=2c_{k+1}-c_k` with `c0=c1=0` kills `c2..c5` (exact symbolic). Lean `QuotientAdapter.lean` kernel-checks the same implication + exponentiation. Nonzero/log hypotheses reduce to γ(n+j)>0, which I confirmed numerically for the Mellin integral (RC-2 B.3) and which is the paper-level positivity obligation. |
| **B3** | Eventual parameter ordering + every degree-dependent Jacobi hypothesis via exact rational interval ledger | **VERIFIED** (ledger arithmetic) / **PAPER-LEVEL** (eventual branch membership) | RC-5: all ledger entries re-derived in `Fraction` with **no floats**: box margins `(1/2,1/2),(1/4,1/4),(1/3,2/3),(1/12,1/12)`; `α/e≥30>11/4≥t+we`; `t-1-δe≥103/144>0` ⇒ `A>B>C>D>0`; saddle margins `151/200>9/16`, reduced denominator `151/50`; `B/D≤6`; endpoint positivity ⇔ `B,D≥256d`; `K0=262144`. The "eventual" statement that the branch lies in this box for large `n` is the paper-level contraction argument (see P1). |
| **B4** | Ascending/descending reversal adapter for multiplicative finite-free convolution | **VERIFIED** | RC-4: MSS signed-coefficient formula sanity-checked (d=1, d=2 diagonal); reversal identity `(p⊠_d q)^∨ = p^∨⊠_d q^∨` verified **symbolically** (generic d=4) and on 5 exact-rational random positive-root instances; identity (F) `q_{A,B}⊠_d q_{C,D}(D·) = {}_3F_2(-d,A,C;B,D;Dy/(AC))` verified **exactly** (ascending, constant-term-one); reversal reciprocates positive roots and preserves logarithmic mesh. |
| **B5** | MMP v3 Prop 2.7(iii) & 2.17 hypotheses; positive roots; strict log mesh; simplicity; nonzero constant term | **EXTERNAL** (hypotheses checked) | Jacobi factors have positive simple roots (RC-6, two independent root computations + residuals ≤2e-13) and full degree `d`; `p_F(0)=1`. MMP genuinely develops finite-free real-rootedness preservation and log-mesh control (web-verified existence). Exact proposition text rests on the packet's hash-frozen arXiv v3; the paywalled IMRN PDF was not byte-compared (packet-disclosed). **See Finding F4** for a convention double-check. |
| **B6** | Ratio-free Jacobi/Gershgorin bound; threshold 256; multiplicative interval; MSS published Thm 1.6; `C_loc=12+8√6<32` without circular constants | **VERIFIED** (arithmetic + numeric localization) | RC-5 re-derives `C_loc=12+8√6<32` (via `√6<5/2`) and `K0=256·32²=262144`; constant order is non-circular (`K_pre=256` fixed **before** `C_loc`). RC-6 numerically confirms the single-factor interval `[V-8√(Vd), V+8√(Vd)]` (6 cases) and the product localization `|y-B|≤C_loc√(Bd)` (3 branch-like cases, exact rationals, 40-digit roots, all real). MSS theorem-number correction (1.6 vs Holland's 1.13) is consistent with my web check (see §6). |
| **B7** | Shifted `_3F_2` ODE and all four recurrence coefficients, complete index range | **VERIFIED** (+ Lean-checked) | RC-3: generic `_3F_2` ODE verified at the series-coefficient level; all four `P_{i,m}` derived independently (Euler-operator/Stirling expansion) and match Lean closed forms exactly; recurrence `Σ P_{i,m}T_{m+i}≡0` holds as an **exact polynomial identity** on genuine `_3F_2` polynomials for **all** `0≤m≤d` across 5 parameter tuples (d=5,6,7,8,10); derivative identity `p_F^{(m)} = prefactor·(shifted _3F_2)` (same `λ`) verified. Lean checks the four closed forms and the elimination. |
| **B8** | Central coefficient lower bound in non-perturbative `(C-D)/C→1/2` regime | **VERIFIED** (closed form + arithmetic) / **PAPER-LEVEL** (estimate) | The decomposed central coefficient `P_{2,m}=b_{m+1}+(D+m)a+ε_p(y/A)(A-d+3+3m)` matches Lean `recurrenceP2_closed` (RC-3). The bound `P_{2,m}≥n/8` follows from `|b_{m+1}|≤3n/16+n/16=n/4` and `(D+m)a≥(n/2)(3/4)=3n/8`; arithmetic re-checked and correct. Crucially the `ε_p=(C-D)/C→1/2` term enters with **favorable sign** and the argument does **not** require it to be small (non-perturbative), consistent with the claim. |
| **B9** | Neighbor coefficient bounds + maximum argument giving radius `O(√(Bd))` | **LEAN-CHECKED** (maximum step) / **PAPER-LEVEL** (coefficient bounds) | Lean `DominantMaximum.lean` kernel-checks the finite contradiction (`u_k≤q·M`, `q<1`, `u_0,u_1≤1` ⇒ `M≤1`). The neighbor bounds `(N3) |P_3|≤2`, `(N1) |P_1|≤C_1(n√(Bd)+nd)`, `(N0) 0≤P_0≤C_0 n²d` are paper-level; the mandatory `(P1-dec)` decomposition exposing the `B-y` cancellation matches the Lean/symbolic structure I verified. |
| **B10** | Multiplier sign-transfer hypotheses, exterior intervals, continuity, distinctness | **LEAN-CHECKED** | Lean `MultiplierStability.lean` checks the exact geometric tail `Σ_{k≥5}2^{-k}=1/16`, the sharp threshold `ε<16`, sign preservation under relative error `<1`, and the IVT construction of one distinct positive root per disjoint sign-changing interval. `MultiplierIntervalCertificate` carries exterior intervals, continuity, and separation/distinctness as fields. I verified the Newton/derivative identity `P/p = Σ Δ^k c(0)/k! · y^k p^{(k)}/p` and the five-match vanishing `Δ^1..Δ^4 c(0)=0` by hand. |
| **B11** | Positive-to-negative Jensen scaling + concrete binomial Jensen definition | **LEAN-CHECKED** | Lean `JensenPolynomial.lean` defines `J^{d,n}(X)=Σ_j C(d,j)γ(n+j)X^j` (standard GORZ convention, matches the manuscript). `ConditionalAssembly.lean` proves positive roots of the transformed polynomial map to `d` distinct **negative** roots of `J` via `y=-S·X`, `S>0`, with `normalization≠0`. Logic audited and sound. |

---

## 4. Independent recalculation record

All scripts are in `output/phase24_algebraic_review/` (`rc1_leading_system.py`, `rc2_branch.py`, `rc3_recurrence.py`, `rc4_reversal.py`, `rc5_intervals.py`, `rc6_jacobi_roots.py`). Each re-enters definitions from the manuscript; none reads a frozen packet artifact as input. Results:

- **RC-1 (B1) — PASS.** `F(y_*)=0` exactly; uniqueness by two independent methods; `det DF(y_*)=-1/144`; `‖DF(y_*)^{-1}‖∞=304/3`; my inverse == Lean `gaugeJacobianInv`.
- **RC-2 (B2 + Mellin identity) — PASS.**
  - Quotient-adapter algebra (invertible reconstruction + induction to six coefficients).
  - **Evenness of the Mellin kernel** `f(u)=ω(e^{2u})e^{u/2}`: `f(+u)=f(-u)` to relative `~1e-32` (u=0.5,0.9,1.3), validating the "retain both halves" step behind the factor 8.
  - **Normalization anchor:** `γ(0)=8∫_0^∞ f = 0.49712077818831` equals `ξ(1/2)` computed independently from `ξ(s)=½s(s-1)π^{-s/2}Γ(s/2)ζ(s)` via mpmath `zeta`/`gamma`, relative difference `<1e-14`. This independently confirms the **factor-eight** identity (eq:factor8).
  - **Positivity:** `γ(5),γ(10),γ(15)>0` (nonzero/log hypothesis input).
  - *Informational only:* raw log-moment curvature `h''(x)·x·L_{2x-2}/2 ≈ 0.65–0.69` at x=35,55 — I could not pin down the tower's exact "moment normalization" independently and `O(1/L)` corrections are large at reachable `x`, so this is **not** counted as verification of the tower (see §7, U2).
- **RC-3 (B7) — PASS.** ODE from the series; four coefficients match Lean; recurrence is an exact polynomial identity for all `0≤m≤d`, 5 tuples; derivative-shift identity verified.
- **RC-4 (B4) — PASS.** Reversal identity (symbolic + numeric); identity (F) exact; roots reciprocate, log mesh preserved.
- **RC-5 (B3/B6 arithmetic) — PASS.** Every ledger quantity re-derived in exact rationals (see gate table).
- **RC-6 (B6 numerics) — PASS.** Single-factor Jacobi interval (6 cases, two root methods + 50-digit residuals, all roots simple); product interval and `C_loc` localization (3 cases, exact-rational coefficients, 40-digit root-finding, all roots real).

**Supplementary (not independent):** the packet's own verifier, run in its intended repo-root context, passes end-to-end:
`verify_interval_certificates` (PASS), `release_checks` (PASS), 10 fail-closed `mutation_tests` (all rejected), `manuscript_equation_regression` (factor-eight max rel. error `2.4e-37`; radius regression `K_r=0.880246`, stale-scale ratio `14681.5`), and `lake build Zeta23.Research.JensenWedge` (**8710 jobs, success**) with an escape scan finding **no** `sorry/admit/axiom/unsafe/native_decide/implementedBy`.

---

## 5. Findings (P0–P3)

**Severity key:** P0 = blocks acceptance; P1 = major, must be addressed before any external claim; P2 = should address; P3 = minor/nit.

- **P0 (blocking): none found.** Within the algebraic track I found **no** fatal defect: every decisive symbolic identity I re-derived matches, and the Lean firewall builds cleanly with no proof escapes.

- **P1-1 (major, disclosed): the theorem is conditional, not unconditionally established.** The end-to-end Lean theorem is conditional on constructing a `JensenWedgeCertificate` for the Riemann-xi coefficients, and that certificate is **not** constructed. The analytic core — sectorial saddle (Lemma S Rouché/branch), the sectorial coefficient asymptotic (Thm 21B), the order-six logarithmic-derivative tower, the existence/convergence of the positive parameter branch, and the order-six residual bound — is **paper-level** mathematics, not yet Lean-formalized and (per the packet's own `C48-REVIEW` row) so far reviewed only by *correlated* AI passes. **This is the single most important fact about the candidate.** It is honestly disclosed throughout (`KNOWN_LIMITATIONS.md`, manuscript status box), but any external circulation must say "proof candidate with an unformalized analytic core," not "proved/formally verified theorem."

- **P1-2 (major, disclosed): decisive-CAS common mode is not yet broken.** The exact symbolic identities (saddle tower, `_3F_2` recurrence, leading system, `H_6` majorant) currently rest on SymPy/Lean paths only. The clean-room **Mathematica** reconstruction (`MATHEMATICA_FOLLOWUP.md`, items M1–M4) is explicitly deferred and **not run**. Until it runs, a common SymPy/transcription error cannot be excluded. (My own pass also used SymPy — see §1 — so I do not by myself discharge this.) See R1.

- **P2-1: logarithmic-mesh convention should be pinned against the frozen MMP source.** The candidate uses `lmesh(p)=min λ_{j+1}/λ_j ≥ 1` with `lmesh(p⊠q)≥lmesh(p)`, whereas some MMP-family literature uses the reciprocal `≤1` convention. The substance (distinct positive roots of `p_F`) is robust — the first Jacobi factor has distinct positive roots, positivity is preserved (Prop 2.7(iii)), and `p_F(0)=1` — but the exact statement/direction of Prop 2.17 should be quoted from the hash-frozen v3 text to remove all ambiguity. This is a documentation/verification nicety, not a correctness defect.

- **P2-2: `H_6` majorant constants are not independently reproduced.** The manuscript (Sec. 5) asserts the sixth-derivative numerator is a degree-13 polynomial with 82 terms and a coefficientwise majorant `<10^4` on `|r|,|σ|≤7/50`, yielding `|G_0^{(6)}|≤20000/(|N|^5 log|N|)`. I did not re-derive this object (it is exactly item M4 of the deferred Mathematica work). Recommend landing the majorant value in the exact-rational interval ledger once M4 runs, so the constant is auditable like the others.

- **P3-1: effectivity is existential.** The wedge constant `K` is effective-in-principle but not numerically computed or propagated (disclosed, `KNOWN_LIMITATIONS.md` item 7). This does **not** affect the existential theorem, but the abstract should continue to avoid any numerical `K` claim.

- **P3-2: full four recurrence coefficients are cited but not printed in the manuscript.** The manuscript displays only `P_{3,m}` and `P_{0,m}` and refers to the "full four closed forms" as Lean/SymPy certificates. Since the radius argument (B9) leans on the decomposed `P_{1,m}` cancellation, consider printing all four (they are short) in an appendix for a human reader. Cosmetic.

- **P3-3: paywalled MMP journal PDF not byte-compared.** The published IMRN PDF was not downloaded; the accessible arXiv v3 is hash-pinned (disclosed). Acceptable, but note it wherever the published record is cited.

No finding contradicts any independently recomputed identity; all P1/P2 items are either already disclosed by the packet or are low-cost documentation/verification hardening.

---

## 6. External-citation audit (B5/B6 seam)

- **MSS theorem number.** The candidate cites **MSS published Theorem 1.6** for the coarse largest-root product bound `maxroot(p⊠_d q) ≤ maxroot(p)·maxroot(q)`, and explicitly notes that Holland's Lemma 7.1 cites MSS **Theorem 1.13** at the same point. My independent web check of the MSS literature confirms that the **S-transform inequality** (the quantitatively stronger multiplicative bound) is Theorem **1.13** in the published paper, while the coarse maxroot product bound is a separate, earlier result. This is **consistent with** the packet's correction and supports the claim that the candidate's renumbering (1.13 → 1.6) is a genuine, correct source-fidelity fix rather than a transcription slip. The coarse bound itself is mathematically sound and is exactly what the interval lemma needs.
- **MMP Propositions 2.7(iii) and 2.17.** Web verification confirms MMP develops preservation of real-rootedness/positivity under multiplicative finite-free convolution and introduces/controls logarithmic mesh — matching the scope recorded in `PRIMARY_SOURCE_AUDIT.md`. Exact proposition text and numbering rest on the packet's hash-frozen arXiv v3 (PDF + source); the paywalled journal PDF was not byte-compared (disclosed). See Finding P2-1 (mesh convention).
- **Holland (arXiv:2608.08682v1).** Not independently retrieved by me; hash-frozen in the packet. Not load-bearing as a premise: the `DEPENDENCY_MATRIX.md` shows Holland's three-fifths theorem (Thm 1.1), his parameter branch (Lemma 6.1), and his assembled root lemma (Lemma 7.3) are **not used**; the candidate re-derives the quotient architecture, four-parameter branch, residual, and recurrence, and cites MMP/MSS directly. Consistent with the manuscript's "Holland's main theorem is not a premise."

---

## 7. Unchecked / unverified source hypotheses (record)

These are the obligations that remain open after my pass. Items U1–U6 are **already disclosed** by the packet; U7–U9 are items I could not independently close.

- **U1.** Sectorial saddle branch (Lemma S): Rouché, holomorphic implicit-function branch patching, and uniform logarithmic asymptotics are paper-level; Lean checks only the finite denominator/norm margins (`SaddleBounds.lean`).
- **U2.** Order-six logarithmic-derivative tower (`h'',…,h^{(6)}` with constants `2,-2,4,-12,48`): machine-checked SymPy artifact in the repo; I could **not** independently reproduce the exact "moment normalization" numerically (my raw log-moment curvature ratios were `0.65–0.69`, inconclusive given `O(1/L)` corrections and normalization ambiguity). The clean-room Mathematica reconstruction M1 is the designated discharge.
- **U3.** Existence/uniqueness/convergence of the positive parameter branch (`y_n→y_*` at rate `O(L_n^{-1})`) via the fixed-inverse contraction on `K_0`: paper-level `C^1` estimate; finite inverse/triangular algebra is Lean-checked.
- **U4.** Full six-simplex Hermite–Genocchi equality: a named hypothesis (`hHG`) in Lean; only the complex line-segment FTC and the exact `1/720` Newton-product adapter are kernel-checked.
- **U5.** Elementary `C^1` cube-integral identity and differentiation under all parameter integrals: paper-level; unit-cube volume, denominator, reciprocal-power, and integral bounds are Lean-checked.
- **U6.** Construction of a concrete `JensenWedgeCertificate` for the Riemann-xi coefficients (i.e., the entire analytic certificate): not performed; the end-to-end theorem is conditional on it.
- **U7.** Byte-level verification of MMP Proposition 2.7(iii)/2.17 and MSS Theorem 1.6 exact statements against the frozen PDFs (binaries not committed to the packet; only SHA-256 hashes recorded). I verified existence/scope via web search, not the exact frozen bytes.
- **U8.** Retrieval/verification of Holland v1 (hash-only in the packet).
- **U9.** The `H_6` coefficientwise majorant (`<10^4`, 82 terms, degree 13): not independently re-derived (deferred Mathematica item M4).

---

## 8. Recommendations (R0–R3)

- **R0 (blocking before any external/public claim):** Keep the embargo and the "AI pre-review only, not human/peer review" label until items R1–R3 are addressed. Do **not** describe the candidate as a proved or formally verified theorem; it is a proof candidate with an unformalized analytic core (P1-1).

- **R1 (highest technical priority): run the deferred clean-room Mathematica reconstruction (M1–M4).** This is the only remaining safeguard against SymPy common-mode error on the decisive symbolic identities, and my own SymPy-based pass cannot substitute for a second CAS. Treat any `MISMATCH` as a release blocker, per the follow-up document's own rules. (M1 tower, M2 `_3F_2` ODE/recurrence, M3 leading system/Jacobian, M4 `H_6` majorant.)

- **R2: commission a genuinely separated analytic-track review** (different provider or a context-free session, with prior reports excluded) for the saddle → tower → branch → residual → finite-free chain (U1–U6). My algebraic pass verifies the finite/symbolic skeleton but deliberately does not vouch for those analytic estimates.

- **R3 (low-cost hardening):** (a) Pin the logarithmic-mesh convention and quote MMP Prop 2.17 from the frozen v3 text (P2-1). (b) Land the `H_6` majorant constant in the exact-rational interval ledger once M4 runs (P2-2). (c) Print all four recurrence coefficients in an appendix (P3-2). (d) Keep the existential-`K` / effectivity language exactly as is (P3-1).

---

## 9. Overall assessment

The **algebraic skeleton** of the two-thirds wedge candidate is, to the extent I independently recomputed it, **correct and consistent**: the limiting system and its uniqueness, the quotient-to-six-coefficient adapter, the reversal/finite-free identity (F), the shifted `_3F_2` ODE and all four recurrence coefficients across the complete index range, the exact-rational interval ledger, the `C_loc=12+8√6<32` localization arithmetic, and the finite multiplier/scaling steps all pass my from-scratch checks, and the Lean firewall builds cleanly with no proof escapes. The external seams (MSS 1.6 vs 1.13, MMP positivity/log-mesh) were audited and the candidate's theorem-number correction appears to be a genuine, correct fix.

What is **not** established is the **analytic certificate** (saddle asymptotics, derivative tower, parameter branch, residual bound) and its assembly into a `JensenWedgeCertificate`; that core remains conventional paper mathematics reviewed so far only by correlated AI passes, with the decisive-CAS common mode not yet broken by a second CAS. These facts are disclosed honestly and thoroughly by the packet, which is to its credit.

**Verdict (algebraic track):** no P0; conditional acceptance of the algebraic/symbolic layer; the candidate as a whole is a **credible proof candidate, not yet a completed or formally verified theorem**, subject to R1–R3.

---

*Prepared by an AI reviewer (Qwen3.8-Max via OpenRouter). This document is an AI pre-review on the algebraic track; it is not human review and not peer review. Independent recalculation scripts are preserved under `output/phase24_algebraic_review/`.*
