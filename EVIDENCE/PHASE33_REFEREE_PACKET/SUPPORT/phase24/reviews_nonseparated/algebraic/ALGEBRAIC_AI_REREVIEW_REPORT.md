# Phase-24 algebraic adversarial AI pre-review — report

**Candidate reviewed:** `Jensen_Two_Thirds_Phase24_Algebraic_AI_Review_Packet`
**Declared proof-source commit:** `7bb179ef62f979d58f2587db87a19d0c1f77b28d`
**Review track:** Algebraic (Gates B1–B11)
**Report date:** 2026-08-16
**Reviewer:** Claude (Opus 5, Anthropic) — **AI pre-review, not human review, not peer review**

---

## 0. Independence, tools, and a separation failure I must declare first

**This is not a clean first pass, and the packet's own protocol was not met.**
`REVIEW_SEPARATION.md` requires a first-pass reviewer to receive no prior verdicts,
author responses, or finding dispositions. The packet correctly omits all of those
files. But **earlier in this same working session I produced the round-3 algebraic
review of the Phase-22 candidate**, and several Phase-24 repairs I am now auditing are
direct responses to my own findings there — specifically the non-circular a-priori
constant `K_pre = 256` and the improved `C_loc = 8 + 12√6` (`ASSUMPTION_REGISTRY.md`
row `C48-RADIUS` records exactly this), and the "direct ascending identity is valid as
well" sentence now in Phase 16. I am therefore **not independent of the repairs**, and
I cannot certify those particular items with the weight of a fresh pass. A genuinely
separated reviewer — ideally a different provider — is still required for them.

What I *can* offer, and what this report is worth: I re-entered every decisive formula
from definitions, and I found two false displayed equations in the new unified
manuscript that no prior report covers, because the manuscript did not exist when those
reports were written.

**Tools and access.** SymPy 1.14.0, mpmath 1.3.0 (the pinned versions), Lean
`leanprover/lean4:v4.33.0-rc2` with Mathlib `51e6992e…` via the user's local build
cache. **No network access**: I could not retrieve the MSS, MMP, GORZ, GORTTW or
Holland PDFs, so every primary-source hypothesis below is recorded as unverified except
where noted. I did not read any frozen JSON or Lean closed form *before* deriving the
corresponding quantity myself; the comparisons in §3 are after-the-fact.

**Conflict disclosure:** none. No financial, institutional, or authorship interest in
the candidate, in Holland's preprint, in GORZ/GORTTW/MMP/MSS, or in the repository.

**Provenance check (mine).** All 99 files under `evidence/` and the manuscript `.tex`
are **byte-identical** to commit `7bb179e`. `python3 VERIFY_BUNDLE.py` → `PASS` (106
files). The repository at `8315d70` differs from the candidate only by release
packaging (`RELEASE_FREEZE.md`, logs, zip, manifests) — no proof source changed — so I
ran the verifiers there.

---

## 1. Overall recommendation

### **R1 — repair, re-freeze, re-review**

No P0. The architecture is sound, and every exact identity I re-derived from
definitions is correct — the leading system and its Jacobian, the quotient adapter, the
shifted `₃F₂` equation and all four recurrence coefficients, the reversal identity, the
squared localization inequalities, the exact `H₆` denominator and majorant, and the
whole saddle derivative tower including the constants `−12` and `48`. The Phase-24
repairs to the localization ordering are correct and the new Lean modules compile and
say what the ledger claims.

**But the unified manuscript — which is the release artifact — contains two false or
mis-stated displayed equations, each of which breaks the manuscript's own logical chain
as written.** Both are transcription-level; both have the correct statement sitting in
the bundled evidence notes; neither threatens the theorem. They are P1 because the
manuscript explicitly routes load through them.

| Gate | Verdict | Confidence | Note |
|---|---|---|---|
| B1 limiting system, Jacobian, inverse | **PASS** | High | Re-solved from definitions: unique positive-orthant zero `(3,2,16/3,1/3)`; `det = −1/144`; `‖DF(y_*)^{-1}‖_∞ = 304/3`; `3t·(orderTwo) − (orderThree) = 3w(t−1) − t⁴` exactly, no division |
| B2 four quotients ⇒ six coefficients | **PASS** | High | Recurrence `c_{k+2} = 2c_{k+1} − c_k` with `c_0 = c_1 = 0`; Lean `fourQuotients_twoNormalizations_sixCoefficients` states exactly this; orientation and nonvanishing hypotheses correct |
| B3 parameter ordering / Jacobi hypotheses | **PASS** | High | `A > B > C > D > 0` verified from the box by exact rational arithmetic (`30 > 11/4`, `103/144 > 0`); ledger reproduced independently. See **F5** |
| B4 reversal adapter | **PASS** | High | `ĉ_j^{(1)}ĉ_j^{(2)} = F_j`; and `ê_k(r) = ê_{d−k}(1/r)·e_d(r)` proves ⊠ commutes with reversal, so both orientations are valid — the note now says this |
| B5 MMP 2.7(iii)/2.17, positivity, mesh, simplicity | **PASS (source unverified)** | Medium | Chain is correct given the cited statements; `p_F(0)=1`; Jacobi parameters `α = V−1 > −1`, `β = U−V−d ≥ 0`. I could not open MMP v3. See **F8** |
| B6 Gershgorin, threshold 256, MSS 1.6, `C_loc = 8+12√6` | **PASS** | High | Squared inequalities exact; both factor intervals now lie in `(0,∞)`; `12+8√6 ≤ 8+12√6 < 38`; `K_0 = 256·38² = 369664`; no circularity. Exposition gap: **F3** |
| B7 shifted `₃F₂` and all four coefficients | **PASS** | High | Derived by my own Euler-operator expansion; identical to all four Lean closed forms; verified on genuine polynomials for **every** `0 ≤ m ≤ d` over four parameter tuples |
| B8 central lower bound, `(C−D)/C → 1/2` | **PASS** | High | `P_{2,m} = b_{m+1} + (D+m)a + ε_p(y/A)(A−d+3+3m)`; last term nonnegative; `A−d+3+3m ≥ d+3`; `n/8` follows at `K_0 = 256C_loc²` |
| B9 neighbor bounds and radius | **PASS in the notes, FAIL as printed** | High | Phase-16 statement `(R)` is correct. The manuscript's `eq:radius` is not it — **F2 (P1)** |
| B10 multiplier sign transfer | **PASS in the notes, incomplete as printed** | High | `HOLLAND_MULTIPLIER_REPROOF.md` is faithful and correct. The manuscript states none of the lemma's hypotheses — **F4** |
| B11 positive-to-negative scaling, concrete Jensen | **PASS** | High | `jensenPolynomial γ n d X = Σ C(d,j)γ(n+j)X^j` matches the paper; `y = −SX`, `S > 0`; conditional assembly closes the definition gap |

---

## 2. Findings

### F1 — P1 — manuscript eq. (eq:factor8) is not an identity

**Location.** `manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex` §2 (`\label{eq:factor8}`):

```
  Theta(t) = sum_{m>=1} e^{-pi m^2 t},    omega(t) = (1/2)(2 t^2 Theta''(t) + 3 t Theta'(t))

  gamma(n) = (8 * 2^{2n} / (2n)!) * int_0^infty omega(e^{2u}) e^{u} u^{2n} du        <-- FALSE
```

**Evidence.** I evaluated both sides in 45-digit arithmetic, with `γ(n)` taken from the
Taylor coefficients of `ξ(1/2+w)` itself:

| `n` | `γ(n)` | printed RHS | `γ(n)` / printed |
|---|---|---|---|
| 0 | 0.4971207782 | 0.5432174056 | 0.91514 |
| 1 | 0.01148597216 | 0.05440464428 | 0.21112 |
| 2 | 2.469040361e-4 | 2.455295542e-3 | 0.10056 |
| 3 | 4.994132888e-6 | 6.864386737e-5 | 0.072754 |
| 4 | 9.581343723e-8 | 1.355645437e-6 | 0.070677 |
| 5 | 1.753923091e-9 | 2.034e-8 | 0.086218 |

The ratio is neither `1` nor constant, so this is not a normalization convention
mismatch — the equation is simply false.

**Two independent errors, and the correct statement.**

1. **Amplitude.** The classical kernel satisfies `Φ(u) = 2 e^{u/2} ω(e^{2u})` — I
   verified this to full precision at `u = 0.1, 0.7, 1.5` (ratio `1.0`). The manuscript
   has `e^{u}`.
2. **Prefactor.** `γ(n) = (n!/(2n)!)·∫₀^∞ Φ(u)u^{2n} du`, and
   `n!/(2n)! = √π/(4^n Γ(n+½))` by duplication. The printed `2^{2n}` is `4^n` in the
   **numerator** where it belongs in the denominator, with `Γ(n+½)/√π` dropped — i.e.
   the two equivalent forms have been conflated and the result is neither.

The corrected identity, which **keeps the factor eight**, is

```
  gamma(n) = (8 * n! / (2n)!) * int_0^infty omega(e^{2u}) e^{u/2} u^{2n} du
           = (8 * sqrt(pi) / (4^n Gamma(n+1/2))) * int_0^infty omega(e^{2u}) e^{u/2} u^{2n} du
```

I verified this to **40+ digits for `n = 0,…,6`** against `ξ`'s Taylor coefficients
(relative difference `0.0`). Derivation: `ω(t) = t^{1/2} d/dt[t^{3/2}Θ'(t)]`, so
Riemann's `ξ(s) = 4∫₁^∞ d/dt[t^{3/2}Θ'(t)]·t^{-1/4}cosh(½(s−½)log t) dt` becomes
`ξ(1/2+w) = 8∫₀^∞ ω(e^{2u}) e^{u/2} cosh(wu) du` under `t = e^{2u}`; extracting `w^{2n}`
from `cosh` gives the display.

**Why this is P1 and not editorial.** §4 (`thm:sector`) says *"The main term is the one
obtained from (eq:factor8) and agrees, after the factor-eight normalization, with the
printed GORZ main term."* The manuscript therefore routes its entire sectorial main term
through a false equation, and `PAPER_THEOREM_INVENTORY.md` lists this as **T1**, the base
of the T1→T18 dependency order. A reader reconstructing from the manuscript alone — which
is exactly what `REVIEW_PACKET.md` instructs — gets the wrong `γ(n)`.

**Why the theorem is not affected.** This display is **new manuscript text with no
counterpart in the evidence tree**. The chain actually used is the `F(s)`/`Λ^{(n)}(1/2)`
route of `phase21/C48_GORTTW_SECTOR_MILESTONE1.md`, giving
`M_z = 2^{−2z−2}(32·C(2z,2)F(2z−2) − F(2z))` and `γ(z) = Γ(z+1)M_z/Γ(2z+1)`. I re-derived
that route independently — symbolically for general `n`, including the exact cancellation
of the polar terms — and confirmed it numerically to 60 digits. It is correct. So the
repair is a two-symbol fix to the manuscript.

**Changes the theorem?** No.

---

### F2 — P1 — manuscript eq. (eq:radius) states a strictly weaker conclusion than the sign-transfer step consumes

**Location.** `manuscript` §9 (`\label{eq:radius}`):

```
  max_{0<=k<=d} | p_F^{(k)}(y) / (k! p_F(y)) |^{1/k}  <=  K_r sqrt(Bd)        <-- as printed
```

**What is required.** `phase16/C48_UNIFORM_RADIUS_PROOF.md` proves, correctly, the
statement `(R)`:

```
  | y^k p_F^{(k)}(y) / p_F(y) |  <=  (K_r sqrt(Bd))^k ,     0 <= k <= d
```

and this is verbatim the hypothesis `(M1)` of the multiplier-stability lemma in
`phase20/HOLLAND_MULTIPLIER_REPROOF.md`. The printed version drops the `y^k` and inserts
`1/k!`. Those are not cosmetic: `|p^{(k)}/p| ≤ k!·ρ^k` versus `|p^{(k)}/p| ≤ (ρ/y)^k`,
and on this branch `y ≍ B ≍ 2n` while `ρ = K_r√(Bd) ≪ n`.

**Quantified on the actual branch.** Using the parameters from my own independent
reconstruction at `n = 100`, `d = 10` (`A,B,C,D = 1888.944, 286.592, 164.854, 121.014`,
`√(Bd) = 53.534`), the minimal admissible constant is

```
  Phase-16 (R)        :  K_r = 1.16029
  manuscript eq:radius:  K_r = 0.00226808          (a factor 511.6 slacker)
```

So the printed inequality is *true* but vacuous, and it does not imply `(R)`. §10
nevertheless says *"At each critical point, (eq:radius) and (eq:HG) bound the exact
multiplier perturbation. The finite multiplier stability lemma therefore preserves every
comparison sign."* That inference does not go through from what is printed.

A secondary symptom that the display is garbled: `max_{0≤k≤d}(·)^{1/k}` is undefined at
`k = 0`.

**Correction.** Replace `eq:radius` by Phase-16 `(R)` verbatim, and cite it as the
hypothesis of the stability lemma by name.

**Changes the theorem?** No.

---

### F3 — P2 — `C_loc = 8 + 12√6` is asserted in the manuscript with none of its inputs, and the exact ledger omits the one that matters

Manuscript §8 states `C_loc = 8+12√6`, `√6 < 5/2`, `C_loc < 38`, `K_0 = 256·38² = 369664`
— with no derivation. The derivation (correct, in Phase 16 §3) is

```
  |(B+u)(1+v) - B|  <=  8 sqrt(Bd) + 8 B sqrt(d/D) + 64 sqrt(Bd) sqrt(d/D)
                    <=  (8 + 8 sqrt(B/D) + 4) sqrt(Bd)   using d/D <= 1/256
                    <=  (12 + 8 sqrt 6) sqrt(Bd)          using B/D <= 6
```

and `8+12√6 ≈ 37.394 > 12+8√6 ≈ 31.596` is a harmless enlargement. But:

- the manuscript never displays the coarse box `n ≤ B ≤ 3n`, `n/2 ≤ D ≤ 2n`,
  `n ≤ C ≤ 3n`, `A ≥ 8B`, `A ≥ 2d`, `C ≥ D+d` that supplies `B/D ≤ 6`;
- `INTERVAL_CERTIFICATES.json` records `sqrt6_strict_upper`, `C_loc_strict_upper`,
  `rational_K0` and the squared-localization coefficients, but **not `B/D ≤ 6`** —
  the single hypothesis on which the `√6` depends.

Gate B6 asks the reviewer to check `C_loc = 8+12√6` "without circular constants". From
the manuscript plus the ledger alone that is impossible; it requires opening Phase 16.

Also worth recording: the manuscript's own compact box gives
`B/D = (t+we)/(1+δe) ≤ 11/4`, so `C_loc ≤ 8+12√(11/4) = 8+6√11 ≈ 27.9` is available for
free. Either way `38` is a valid strict upper bound.

**Correction.** Display the coarse box in the manuscript, add the `B/D ≤ 6` (or `11/4`)
row to the interval ledger, and give the three-term bound in one line.

---

### F4 — P2 — §10 invokes "the finite multiplier stability lemma" without stating it or its hypotheses

Gate B10 asks for "multiplier sign-transfer hypotheses, exterior intervals, continuity,
and distinctness". The manuscript's §10 asserts the conclusion and names no hypothesis.
The lemma actually consumed (`HOLLAND_MULTIPLIER_REPROOF.md`, matching Holland's printed
Proposition 2.2) needs all of: `d ≥ 5`; `p` with `d` simple positive zeros and
`p(0) ≠ 0`; `c` holomorphic on a neighbourhood of `Ω_r = {dist(z,[0,d]) ≤ 2r}`;
`c(0),…,c(d)` real; `c(0)=…=c(4)=1`; `c(d) > 0`; `sup_{Ω_r}|c−1| ≤ ε < 16`; and `(M1)`.
The manuscript supplies `E_F(0)=…=E_F(5)=0` and `ε ≤ 1` in §9, so the pieces exist — but
the lemma should be stated, since it is the step that converts everything else into the
theorem.

---

### F5 — P3 — the `|G_0^{(6)}|` bound uses a lower bound on `|L_N|` that is not among Lemma S's conclusions

§5 concludes `|G_0^{(6)}(N)| ≤ 20000/(|N|^5 log|N|)` from a majorant "less than `10^4`".
I reproduced the majorant exactly (see §3.3: `9140.85 < 10⁴`), so the numerator is right.
The step from `1/|L_N|` to `2/log|N|` needs `|L_N| ≥ ½log|N|`, which Lemma S gives only
inside its proof (`Re L ≥ ℓ − log(ℓ+1) − logπ − 1`, and `ℓ/2 − log(ℓ+1) − logπ − 1 > 0`
for `ℓ ≥ 12`); the numbered conclusions give only `|1/L_N| ≤ 7/50`. Promote it.

---

### F6 — P3 — undefined symbol in the Lemma S Rouché estimate

The displayed bound `sup_{∂D}|G−H| ≤ 2(log(ℓ+1)+θ/ℓ+logπ+1)/ℓ + 3M(ℓ)/(2e^ℓ) < 1` uses
`M(ℓ)`, which is never defined. From context it is the disc bound on `|L|` displayed two
lines above. Define it.

---

### F7 — P3 — the release gates cannot see a false equation, and the interval "certificate" has one tautological entry

`release_checks.py` and `mutation_tests.py` are well built and they do fail closed on the
seven mutations they model — I ran them and all seven were rejected. But they are string
gates: **they passed on a manuscript containing a false displayed identity.** Add one
numerical oracle to `verify_phase24.sh` that evaluates `eq:factor8` against `ξ`'s Taylor
coefficients at `n = 0,…,4`; it is a ten-line mpmath check and it would have caught F1.

Separately, in `verify_interval_certificates.py`,

```python
localization_square_left_coefficient  = 8**2                 # 64
localization_square_right_coefficient = Q(1,2)**2 * 256      # 64
assert localization_square_left_coefficient == localization_square_right_coefficient
```

is `64 == 64`. It does encode the correct relation (`8√(Bd) ≤ B/2 ⟺ B ≥ 256d`), but as
coded it cannot fail for any input, so it certifies nothing beyond JSON staleness. State
the inequality it stands for, or drop the pretence of a certificate for that line.

---

### F8 — P3 — primary-source hypotheses I could not verify

I had no network access, and the packet ships hashes rather than binaries (a correct
choice). The following remain **unchecked by me** and rest entirely on
`PRIMARY_SOURCE_AUDIT.md`, which is itself AI-produced:

- **MSS published Theorem 1.6** — that it states `maxroot(p ×_d q) ≤ maxroot(p)·maxroot(q)`
  for nonnegative-rooted inputs, and that Theorem 1.13 is the S-transform inequality that
  Holland cites. This is now the sole external input to the interval lemma, so it is the
  single most load-bearing unverified citation in the algebraic track.
- **MMP v3 Propositions 2.7(iii), 2.11, 2.17** — including the claim that v3 corrected a
  "malformed/overbroad" v2 Proposition 2.11.
- The coefficient identity `(p ⊠_d q)^∨ = p^∨ ×_d q^∨` is asserted as "coefficient
  comparison"; I verified the underlying symmetry `ê_k(r) = ê_{d−k}(1/r)·e_d(r)`
  symbolically, which makes it very plausible, but not the ⊠/× normalization bookkeeping.

`KNOWN_LIMITATIONS.md` item 8 already discloses that the paywalled MMP journal PDF was
not byte-compared. Keep that, and add the MSS theorem-number check to the list of items a
human must confirm — a corrected citation is exactly the kind of claim that should not
rest on an AI reading.

---

## 3. Independent recalculation record

Every item below was entered from definitions in my own code. No frozen JSON, no Lean
closed form, and no packet-produced symbolic output was used as an input.

### 3.1 Mandatory item — leading system and Jacobian

Solved `F(α,t,w,δ) = 0` in SymPy: the **only** solution is `(3, 2, 16/3, 1/3)`.
`3t·(orderTwo) − (orderThree)` expands identically to `3w(t−1) − t⁴`, a pure polynomial
combination with no division, so `w > 0, t > 0 ⟹ t > 1`.
`det DF(y_*) = −1/144`; `‖DF(y_*)^{-1}‖_∞ = 304/3` with absolute row sums
`87, 15, 304/3, 10/3`.

### 3.2 Mandatory item — hypergeometric ODE, recurrence, genuine polynomials

I expanded `θ(θ+b₁−1)(θ+b₂−1)g = λy(θ+a₁)(θ+a₂)(θ+a₃)g` myself with
`a = (m−d, A+m, C+m)`, `b = (B+m, D+m)`, `λ = D/(AC)`. All four coefficients are
**identical** to the Lean closed forms (`recurrenceP3_closed`…`recurrenceP0_closed`):

| | ODE == Lean |
|---|---|
| `P₃ = (AC−Dy)/(AC)` | yes |
| `P₂` | yes |
| `P₁` | yes |
| `P₀ = Dy(A+m)(C+m)(d−m)/(AC)` | yes |

Verified on genuine polynomials in the cleared form `Σ P_k y^{m+k}p^{(m+k)} = 0` for
**every** `0 ≤ m ≤ d` at `(A,B,C,D,d) =` `(37,11,7,3,5)`, `(101,13,17,5,6)`,
`(29,7,11,4,4)`, `(4000,2100,1800,1000,12)` — 31 instances, all identically zero,
including `m = d−1` and `m = d`.

### 3.3 New for Phase 24 — the saddle derivative tower and `H₆`, from the saddle equation only

Starting from `G₀(N) = (N+1)Log L_N + L_N/4 − N/L_N − ½Log Q_N`,
`Q_N = (1+L_N)N − ¾L_N²`, and the implicit rule `L_N' = L_N/Q_N`, I differentiated six
times and passed to `r = 1/L`, `σ = L/N`:

```
   k :  lim N^{k-1} L G_0^{(k)}     (-1)^k (k-2)!
   2 :  1                            1
   3 : -1                           -1
   4 :  2                            2
   5 : -6                           -6
   6 : 24                           24
```

With the chain rule `N = 2x−2` this gives `h^{(k)} = 2c_k/(x^{k−1}L)`, i.e.
`2, −2, 4, −12, 48` — **reproducing eq:tower exactly, including the two new constants
`−12` and `48`.**

The exact sixth derivative in `(r,σ)`:

```
   denominator = (4r - 3 sigma + 4)^12         <- matches the manuscript exactly
   numerator   : total degree 13, 82 monomials <- matches "degree-thirteen ... 82 terms"
   value at (0,0): 402653184 / 16777216 = 24
```

Coefficientwise majorant on `|r|,|σ| ≤ 7/50`, divided by `(151/50)^12`:

```
   |N^5 L_N G_0^{(6)}(N)|  <=  9140.85        (manuscript claims "< 10^4")   OK
```

This closes the manuscript's `M1` Mathematica follow-up item to the extent one CAS can:
it is an independent reconstruction, but it is SymPy again, not a different CAS, so the
common-mode risk `KNOWN_LIMITATIONS.md` item 6 identifies is **not** retired.

### 3.4 Mandatory item — the reversal identity

`ĉ_j^{(1)}·ĉ_j^{(2)} = F_j|_{S=1}` symbolically for `j = 0,…,5`, where
`ĉ^{(1)}_j = (A)_j/(A^j(B)_j)` and `ĉ^{(2)}_j = (C)_jD^j/(C^j(D)_j)`.
And `ê_k(r) = ê_{d−k}(1/r)·e_d(r)` for `d = 4` symbolically, which is why ⊠ commutes with
reversal and both orientations of the identity are valid. The Phase-16 sentence now says
this; it is correct.

### 3.5 Mandatory item — squared localization inequalities

`8√(Bd) ≤ B/2 ⟺ 64Bd ≤ B²/4 ⟺ B ≥ 256d` (equality at `B = 256d`), and
`1 − 8√(d/D) ≥ 1/2` at `D = 256d`. So at the a-priori `K_pre = 256` **both factor
intervals lie in `(0,∞)`** and the multiplicative interval theorem's positivity
hypothesis is genuinely verified before `C_loc` is derived. `√6 < 5/2` since `25/4 > 6`;
`256·38² = 369664`.

### 3.6 Verifiers re-run by me

- `python3 VERIFY_BUNDLE.py` → `PASS` (106 files).
- All 99 bundled `evidence/` files byte-identical to commit `7bb179e`.
- `bash ground_zero_work/phase24/verify_phase24.sh` → **PASS**:
  `PASS phase24 exact interval certificates`; `PASS phase24 release-source checks`;
  all seven mutation tests rejected (`wedge exponent`, `review overclaim`,
  `Lean proof escape`, `missing headline import`, `malformed source hash`,
  `CAS clean-room rule`, `branch-box point`); `lake build Zeta23.Research.JensenWedge`
  → `Build completed successfully (8710 jobs)`; escape scan clean.
- Lean statements read, not exit codes. `QuotientAdapter`, `JensenPolynomial`,
  `ComplexHermiteGenocchi`, `ElementaryCubeBounds`, `SaddleBounds` all say what
  `FORMALIZATION_LEDGER.md` claims, and their unproved inputs (`hHG`, `hNewton`) are
  visible named hypotheses, not axioms. `unitCube_volume_real`,
  `saddle_scaled_factor_norm_lower` (`151/200 ≥ 9/16`), and
  `saddle_reduced_denominator_norm_lower` (`151/50`) are all correct arithmetic.

### 3.7 Cross-check of the corrected coefficient identity (context for F1)

The route actually used in the evidence tree is correct, and I verified it end to end:
`Λ^{(n)}(1/2) = −2^{n+2}n! + 2^{1−n}F(n)` for even `n`; the polar terms cancel exactly in
`γ_G(n)`; `γ_H = γ_G/8`; `M_z = 2^{−2z−2}(32C(2z,2)F(2z−2) − F(2z))`. Verified
symbolically for **general `n`** and numerically against `ξ`'s Taylor coefficients to 60
digits. This is what makes F1 a manuscript regression rather than a proof defect.

---

## 4. Unchecked-claims list

1. MSS published Theorem 1.6 and the Theorem 1.13 correction (**most load-bearing**).
2. MMP v3 Propositions 2.7(iii), 2.11, 2.17 and the v2→v3 correction narrative.
3. `(p ⊠_d q)^∨ = p^∨ ×_d q^∨` normalization bookkeeping.
4. Everything analytic: the contour localization, higher-theta suppression, sectorial
   Stirling domain, Rouché step of Lemma S, the six-simplex Hermite–Genocchi identity,
   the proportional-disc Cauchy transport, and the polygamma path containment. These are
   the analytic reviewer's, and none of them is Lean-checked.
5. Whether `θ_0 = 1/400`, `θ_1 = 1/200` are wide enough for every later use — I checked
   only that `n + Ω` has `|arg| = O(ρ/n) → 0`, which is fine, but I did not audit the
   Phase-21 contour construction.
6. `MATHEMATICA_FOLLOWUP.md` has not been run; my §3.3 reconstruction is SymPy, so
   CAS-diversity risk remains open.

---

## 5. Blocking list and release recommendation

**Blocking for the next freeze (both free, both manuscript-only):**

1. **F1** — replace `eq:factor8` by
   `γ(n) = (8·n!/(2n)!)∫₀^∞ ω(e^{2u}) e^{u/2} u^{2n} du`, and add a numerical oracle for
   it to `verify_phase24.sh`.
2. **F2** — replace `eq:radius` by Phase-16 `(R)`:
   `|y^k p_F^{(k)}(y)/p_F(y)| ≤ (K_r√(Bd))^k` for `0 ≤ k ≤ d`.

**Recommended before circulation:** F3 (display the coarse box; add `B/D` to the ledger),
F4 (state the stability lemma), F5–F7, and put the MSS theorem-number check on the
human-verification list (F8).

**Release:** do not circulate, do not describe as reviewed. The correct classification
remains *internal proof candidate, not release-certified*, and the manuscript's own
review box and §11 publication stop say so correctly — the release gates verify that
wording, which is good practice.

**A structural observation worth acting on.** Both P1s are the same failure mode: the
unified manuscript re-derives or re-displays material that the evidence notes already
state correctly, and the re-display is wrong. `eq:factor8` in particular has *no*
counterpart anywhere in `evidence/` — it is new prose. The Phase-24 release gates check
that certain strings are **present**; nothing checks that newly written displays are
**true**. Before the next freeze I would run every displayed equation in the manuscript
against either an evidence-note counterpart or a numerical oracle, and record which of
the two it is. That is a mechanical pass and it would have caught both findings.

---

## 6. Reviewer certification

I have identified every P0/P1 issue known to me: two, both in the unified manuscript,
both listed above with an exact correction and reproducible evidence. I did not treat a
successful Lean build or a passing verifier script as proof of any source theorem or
analytic estimate; the Phase-24 gates pass and I still found two false displayed
equations, which is the point of the exercise. I re-entered every decisive formula from
definitions before comparing with any repository artifact.

I state again, because it materially limits this report's value: **I am not a separated
first-pass reviewer of this candidate.** I wrote the round-3 algebraic review of the
Phase-22 tree in this same session, and the Phase-24 localization repairs I audited in
Gate B6 answer my own earlier findings. Those items need a reviewer who is not me — and
preferably not from the same provider.

**Signature:** Claude (Opus 5, Anthropic) — algebraic / special-functions AI reviewer
**Date:** 2026-08-16
