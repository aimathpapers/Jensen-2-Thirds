# Phase-24 adversarial analytic AI pre-review

**Candidate proof-source commit:** `7bb179ef62f979d58f2587db87a19d0c1f77b28d`
**Bundle:** `Jensen_Two_Thirds_Phase24_Analytic_AI_Review_Packet`
(`python3 VERIFY_BUNDLE.py` → `PASS Phase-24 reviewer bundle manifest (106 files)`;
I re-ran it and all 106 hashes verify)
**Review date:** 2026-08-16
**Review classification:** **AI pre-review.** Not human review, not peer review.

---

## 0. Reviewer identity, independence, and a separation failure you need to know about

**Reviewer:** Claude Opus 5 (Anthropic), running as Claude Code.
**Tools used:** Python 3.12 with `sympy 1.14.0` and `mpmath 1.3.0`, in a venv I
created for this review; all scripts were written by me from the mathematical
definitions during this review. No repository JSON, `.py` producer, or Lean
artifact was used as an input to any calculation reported below.
**Relationship to the authors:** none. **Conflicts:** none.

### THE IMPORTANT DISCLOSURE

`REVIEW_SEPARATION.md` and `START_HERE.md` ask for a first pass by a reviewer
who has not seen prior reports, responses, or dispositions. **The bundle
correctly excludes all of them.** But separation still failed, for a reason the
bundle could not control:

> **I am the same model that produced the analytic pre-review of the Phase-22
> candidate, and I did so earlier in this same working session. I retain
> complete knowledge of my prior findings F1–F9 and of the calculations I ran
> then.**

This is therefore a **re-review by the original analytic reviewer**, not a
separated first pass. Concretely, that means:

- I knew in advance which parts of the chain I had already verified, and I did
  not re-derive all of them with equal freshness (though I did re-run the
  decisive ones — see §4).
- I was primed to check whether my prior findings had been discharged, which is
  a re-review activity, not a first-pass one.
- The "no P0/P1 in the analytic chain" conclusion of the prior round is
  correlated with, not independent of, this report.

`PROOF_SUPPORT_STATUS`-style claims that Phase 22 received an AI pre-review
"with no P0/P1" and that Phase 24 has now received a *separate* pass would be
**incorrect** if based on this report. If the project wants a genuinely
separated analytic pass, it must be run by a different model or provider, in a
session with no prior context. I recommend that explicitly.

The two P1 findings below are, however, new: both concern the Phase-24 unified
manuscript, which did not exist at the previous freeze.

---

## 1. Overall verdict

# R1 — repairs required, then re-freeze and re-review

**Two P1 findings, both in `manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex`.** No P0.

Both are **wrong printed equations in the release-candidate manuscript**, not
defects in the underlying proof chain. In each case I verified the correct
statement in the evidence notes, and in each case I verified the manuscript's
printed statement is false or vacuous. The repairs are known and I state them
exactly. But the manuscript is the Phase-24 headline artifact, and as printed
it is not correct at two load-bearing points, one of which is its equation (1).

The rest of the analytic chain held up under everything I threw at it. Section 4
records the independent recalculations; several of them are stronger
confirmations than I obtained in the previous round.

**All nine of my prior-round findings have been discharged in the evidence
notes** — see §6. The repair to the `Im L_s` threshold (my prior F2) is
genuinely elegant and removes an astronomical constant. That work is real and I
want it on the record alongside the two new P1s.

---

## 2. Gate table

| Gate | Verdict | Confidence | Evidence / blocking correction |
|---|---|---|---|
| **A0** factor-eight Mellin identity and xi convention | **FAIL AS PRINTED** | High | **Finding 1.** Manuscript eq. (1) is false: ratio to the true `γ(n)` is 1.09, 4.74, 9.94, 13.7, 14.1, 11.6 for `n=0..5`. Corrected identity verified to 40+ digits. |
| **A1** Lemma S: Rouché, branch patching, reality, `Q_N≠0` ordering | **PASS** | High | Boundary sum `0.80693 < 1` at `ℓ=12`, uniform for `θ↑π/2`; `1/m(12)=0.13717 ≤ 7/50`; `Q_N≠0` is obtained before implicit differentiation, as required. |
| **A2** shifted contour, connectors, signed Gaussian error, theta modes | **PASS** (notes) / minor manuscript defects | High | Contour identity verified to working precision at complex `s` off the real axis; relative error `O(1/|K|)` confirmed. Findings 6, 8 concern the manuscript's compression. |
| **A3** fixed nested sectors for Thm 21B, proportional-disc Cauchy | **PASS** | High | `θ_0=1/400`, `θ_1=1/200` now explicit and consistent with Lemma 21A's `1/100`; verified the contour and localization at both angles. |
| **A4** constants `2,−2,4,−12,48`, normalization and `N=2x−2` | **PASS** | High | Confirmed by **three** independent paths, including a full accounting of the explicit normalization terms agreeing with measurement to 0.02–0.3%. |
| **A5** exact sixth-order denominator and coefficientwise majorant | **PASS** | High | `(4+4r−3σ)^12`, 82-term degree-13 numerator, exact majorant `9140.8458… < 10⁴` reproduced exactly. No numerical sampling is used as proof. |
| **A6** elementary cube-integral `C¹`, paired gamma boundary | **PASS** | High | Kernel bounds and the mean-value error term re-derived; pairing is essential and correctly done. |
| **A7** contraction branch, box margins, local uniqueness, thresholds | **PASS** | High | `det DF=−1/144`, `‖DF⁻¹‖_∞=304/3`, all four margins, and `A>B>C>D>0` for `0<e≤1/12` verified exactly. Uniqueness correctly claimed only in `K_0`. |
| **A8** paired polygamma segments, containment of `Ω` | **PASS** | High | Paired differences bounded (`−9.24`, `−45.07` after scaling by `n⁵ℒ_n`); unpaired terms grow like `ℒ_n`. Pairing verified necessary. |
| **A9** complex Hermite–Genocchi, hypotheses, six nodes, `1/720` | **PASS** | High | Statement now carries the convexity hypothesis; `1/720` verified exactly on a test function with constant sixth derivative. Full six-simplex identity correctly disclosed as a Lean gap. |
| **A10** exponent arithmetic to `n²log(n+2) ≥ Kd³`, effectivity | **FAIL AS PRINTED** | High | **Finding 2** misstates the hypothesis that drives sign transfer, and **Finding 4** means the exponent arithmetic — the paper's headline — is never displayed. Effectivity disclosure itself is honest. |

---

## 3. Findings

### Finding 1 — **P1** — Manuscript equation (1) (`eq:factor8`) is false as printed

**Location:** `manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex`, §2, eq. `\label{eq:factor8}`.

The manuscript prints, with `Θ(t)=Σ_{m≥1}e^{-πm²t}` and
`ω(t)=½(2t²Θ''(t)+3tΘ'(t))`:

```
gamma(n) = ( 8 * 2^{2n} / (2n)! ) * int_0^inf omega(e^{2u}) e^{u} u^{2n} du
```

and says this "follows directly by differentiating the completed-zeta integral
and using the duplication formula; no asymptotic input enters."

**It does not hold.** Evaluating both sides against the true Taylor
coefficients of `ξ(½+z) = Σ γ(n)z^{2n}/n!`:

| `n` | RHS / `γ(n)` |
|---|---|
| 0 | 1.0927 |
| 1 | 4.7366 |
| 2 | 9.9443 |
| 3 | 13.7449 |
| 4 | 14.1488 |
| 5 | 11.5985 |

**Two independent errors.** The correct identity, which I derived and verified,
is

```
gamma(n) = ( 8 * n! / (2n)! ) * int_0^inf omega(e^{2u}) e^{u/2} u^{2n} du
```

— `2^{2n}` must be `n!`, and `e^u` must be `e^{u/2}`. Verified for `n = 0,…,6`
with relative differences `1.3e−51` to `3.1e−38`. The derivation: Titchmarsh's
kernel satisfies `Φ_T(u) = 4 e^{u/2} ω(e^{2u})`, so with Holland's convention
`ξ(½+z) = ∫_0^∞ Φ_H(u)cosh(zu)du`, `Φ_H = 2Φ_T = 8 e^{u/2} ω(e^{2u})`, and
`γ(n) = (n!/(2n)!) ∫Φ_H(u)u^{2n}du`.

**Why it matters.** This is the manuscript's Section 2, its first equation, the
sole displayed derivation of the normalization, and the entire content of
Gate A0. The manuscript itself stresses that "the factor eight … is important
when the main term is compared character for character with the printed
GORZ/GORTTW convention" — precisely the check that this equation is supposed
to underwrite. A reader working from the manuscript alone gets a normalization
wrong by a factor that grows with `n`. It is not a single-symbol typo: both the
prefactor and the exponential are wrong, so the reader cannot repair it by
inspection.

**Does it change the theorem?** No. The evidence tree uses a different and
*correct* route — `γ_H(M) = Γ(M+1)/Γ(2M+1)·2^{−2M−2}(32C(2M,2)F(2M−2) − F(2M))`
— which I verified to 20+ digits in the previous round and which drives every
downstream estimate. The defect is confined to the manuscript.

---

### Finding 2 — **P1** — Manuscript equation `eq:radius` misstates the hypothesis that drives sign transfer

**Location:** `manuscript/JENSEN_TWO_THIRDS_UNIFIED.tex`, §7, eq. `\label{eq:radius}`,
consumed in §9 ("At each critical point, (eq:radius) and (eq:HG) bound the exact
multiplier perturbation").

The manuscript prints

```
max_{0<=k<=d} | p_F^{(k)}(y) / ( k! p_F(y) ) |^{1/k}  <=  K_r sqrt(B d)
```

Three lines earlier, the same section defines `T_k = y^k p_F^{(k)}(y)/p_F(y)`.
Every supporting note — `phase16/C48_UNIFORM_RADIUS_PROOF.md` (statement (R) and
the definition of `T_k`), `phase17/…` §4, and `phase20/HOLLAND_MULTIPLIER_REPROOF.md`
(M1) — states the bound as

```
| y^k p^{(k)}(y) / p(y) |  <=  rho^k ,      rho = K_r sqrt(B d).
```

The printed version **drops `y^k` and inserts `1/k!`**, so the manuscript states
a bound on a different quantity from the one its own `T_k` denotes and from the
one Holland's Proposition 2.2 hypothesis (6) requires.

**Quantified on a concrete legal parameter point.** Using the numerically solved
branch at `n = 4000` (`A=103773.4`, `B=9370.0`, `C=6664.7`, `D=4309.6`) with
`d = 16` (legal: `B,D ≥ 256d`), I built `p_F = ₃F₂(−d,A,C;B,D;(D/AC)y)`, found
its 16 distinct positive roots and 15 critical points, and evaluated both
quantities:

| quantity | max over critical points | as a multiple of `√(Bd)=387.2` |
|---|---|---|
| `max_k \|y^k p^{(k)}/p\|^{1/k}` (**needed**) | 340.83 | `K_r = 0.880` |
| `max_k \|p^{(k)}/(k!p)\|^{1/k}` (**printed**) | 0.02321 | `6.0 × 10⁻⁵` |

The two differ by a factor `1.47 × 10⁴ ≈ y ≈ B`. The printed inequality is true
but vacuous. If one feeds it into the Newton/Cauchy tail
`Σ_{k≥6} (ε/(2ρ)^k)·|y^k p^{(k)}/p|`, it yields `Σ_k k!(y/2)^k`, which
diverges: the sign-transfer step cannot be run from the manuscript as written.

Incidentally, this run also independently confirms the *correct* statement with
margin (`K_r = 0.88`), confirms `p_F` has `d` distinct positive roots at these
parameters, and shows the localization constant actually needed is `≈ 2.25`
against a proved `C_loc < 38` — a 17× margin.

**Correction.** Replace `eq:radius` by
`|y^k p_F^{(k)}(y)/p_F(y)| ≤ (K_r√(Bd))^k` for `0 ≤ k ≤ d`, matching `T_k`.

**Does it change the theorem?** No — the notes are right. But §9 of the
manuscript is unprovable from §7 of the manuscript.

---

### Finding 3 — **P2** — The manuscript never states the multiplier stability lemma it invokes

**Location:** §9, "The finite multiplier stability lemma therefore preserves
every comparison sign."

No statement, no hypotheses, no `ε` threshold, no numbered result, no citation.
The manuscript also never defines `ε`, never states `sup_Ω|c_F−1| ≤ ε`, and
never records `c_F(0)=…=c_F(5)=1`, `c_F(d)>0`, or that `c_F(0),…,c_F(d)` are
real. Given that this project's history includes a round in which the `ε<16`
threshold was misread as `1/6`, and a round in which the `d≥5` and reality
hypotheses were omitted from the gate text and had to be restored, the release
candidate must state the lemma in full. `phase20/HOLLAND_MULTIPLIER_REPROOF.md`
already contains a correct self-contained version; import it.

---

### Finding 4 — **P2** — The exponent arithmetic, which is the entire point of the paper, is not displayed

**Location:** §8, final paragraph: "The wedge and `|z| ≪ ρ` turn this into a
uniform logarithmic multiplier defect `ε ≤ 1` after enlarging the eventual
threshold."

That sentence replaces the three-line computation that produces the headline
exponent:

```
rho = K_r sqrt(B d) asymp sqrt(n d)   =>   rho^6 asymp n^3 d^3
sup_Omega |E_F| << rho^6 / (n^5 log n) asymp d^3 / (n^2 log n) <= 1/K
```

This is exactly why the wedge is `n²log(n+2) ≥ Kd³` (two-thirds) and not
Holland's `n³log²(n+2) ≥ Kd⁵` (three-fifths) — the same mechanism at order five
gives `d^{5/2}/(n^{3/2}log n)`. Gate A10 asks the reviewer to check it; a
referee cannot check it from the manuscript. The notes contain it
(`phase18/…` (25), `phase17/…` (Def)); display it.

Separately, the stated condition `|z| ≪ ρ` is not the right one. What is needed
is `ρ ≥ d`, so that each `|z−j| = O(ρ)` on `Ω`; the notes now justify this
correctly from the wedge (`ρ/d = K_r√(B/d) → ∞`). Use that.

---

### Finding 5 — **P2** — `C_loc` is a transposition of its own derivation, and the exact-certificate layer cannot catch it

**Locations:** manuscript §7 eq. `\label{eq:local}`;
`phase16/C48_UNIFORM_RADIUS_PROOF.md`; `phase24/INTERVAL_CERTIFICATES.json`;
`phase24/verify_interval_certificates.py` (`assert c_loc_upper == 38`);
`ASSUMPTION_REGISTRY.md`, row `C48-RADIUS`.

The Phase-16 derivation gives, correctly,

```
8 sqrt(Bd) + 8 B sqrt(d/D) + 64 sqrt(Bd) sqrt(d/D)
   <= ( 8 + 8 sqrt6 + 4 ) sqrt(Bd) = (12 + 8 sqrt6) sqrt(Bd) = 31.596 sqrt(Bd)
```

using `B/D ≤ 6` and `d/D ≤ 1/256`. I verified this arithmetic. The next line
then fixes `C_loc = 8 + 12√6 = 37.394` — the two coefficients transposed. It is
*larger*, so every downstream conclusion survives, and the note's parenthetical
"a harmless larger constant" is literally true. But it inflates
`K_0 = 256 C_loc²` from `262144` to `369664`, and it is now hard-frozen into the
exact interval certificate, the registry, and the manuscript.

The point worth making is not the 40% inflation. It is that Phase 24's stated
purpose is exact rational certification, and
`verify_interval_certificates.py` **passes** on this — because it asserts
internal consistency of the *stated* constants (`c_loc_upper == 38`,
`k0_rational == 369664`) and never checks that they follow from the displayed
derivation. An exact-certificate layer that cannot detect a transposed constant
in the one constant it certifies should be extended to re-derive, not just
re-check.

---

### Finding 6 — **P2** — The manuscript cites nonvanishing where a half-plane bound is required

**Location:** §4: "On the shifted ray the real part of the phase is strictly
concave, the quadratic curvature is nonzero by `eq:Qbound`, and the two endpoint
connectors vanish."

The Gaussian step needs `Re K_s ≥ c_0|K_s|` — equivalently `|arg K_s| < 1/20`,
which `phase21/C48_LEADING_CONTOUR_LOCALIZATION.md` proves by an argument
estimate on `K = (s/L)(1+1/L−3L/(4s))`. `eq:Qbound` gives only `Q_N ≠ 0`, hence
`K_N ≠ 0`, which is strictly weaker and does not give a convergent Gaussian or
a well-defined `√(2π/K)` branch.

This is worth flagging precisely because the Phase-21 note *was corrected on
exactly this point in this revision* ("its exact nonvanishing also follows
independently from `Q_s = L_s²K_s ≠ 0`; the right-half-plane bound itself is the
argument estimate above"). The manuscript reintroduces the weaker citation the
note just removed. My measurements: `|arg K| = 0.0041` at `|s| = 3200`,
`arg s = 1/200` — comfortable, but it needs the argument estimate to say so.

---

### Finding 7 — **P3** — Undefined symbol and a mismatched bound inside the Lemma S proof

§3 of the manuscript displays `|L| ≤ ℓ+2+log(ℓ+1)+logπ+1` and then, two lines
later, uses `3M(ℓ)/(2e^ℓ)` in the Rouché estimate. `M(ℓ)` is never defined in
the manuscript. In `phase18/C48_SECTORIAL_SADDLE_VARIABLE.md` it is
`M(ℓ) = ℓ+2+log(ℓ+1)+θ/ℓ+logπ`, which differs from the manuscript's displayed
bound (the manuscript replaces `θ/ℓ` by `1`). Both are valid — the manuscript's
is looser — but the symbol must be defined, and the two should agree.

---

### Finding 8 — **P3** — Two imprecise statements in the compressed contour section

1. "the two endpoint connectors vanish" (§4). They do not vanish; they are
   `𝒜(s)·O(e^{−c|s|log log|s|})`. I measure `|E_s/𝒜(s)| ≤ 2×10⁻⁷⁴` at
   `|s| = 200` — negligible, but the word is wrong in a proof document.
2. §4 asserts strict concavity on the shifted ray without recording the
   hypotheses that make it true (`|arg s| ≤ 1/100` and `|Im L_s| < 1/20`). The
   `Im L_s` bound is the repair this revision introduced; it deserves to appear.

---

### Finding 9 — **P3** — `eq:radius` maximizes over `k = 0`, where `|·|^{1/k}` is undefined

Range should be `1 ≤ k ≤ d`, with `T_0 = 1` recorded separately (as the notes do).

---

### Finding 10 — **P3** — The Phase-24 gate apparatus is string-level and cannot detect a false equation

`release_checks.py` and `mutation_tests.py` guard: the wedge exponent *as a
string*, review-status language, `sorry`/`admit`, Lean imports, source-hash
format, and the CAS clean-room rule. These are good process hygiene and the
mutation suite does fail closed on each fixture.

But the suite passes on a manuscript whose equation (1) is false and whose
`eq:radius` is off by a factor of `10⁴`. Both P1s above are invisible to every
gate in the Phase-24 apparatus, including the exact interval certificates. I
recommend adding an **equation regression gate**: a small set of displayed
identities evaluated numerically against high-precision ground truth (the
factor-eight identity, `det DF = −1/144`, the derivative constants, the
`H_6` majorant, the radius statement on a concrete `p_F`). Each of the two P1s
would have been caught in seconds by such a gate; I caught them that way.

---

## 4. Independent recalculations performed

All computed here, from the definitions, with scripts I wrote during this
review. Saved to `~/Desktop/Jensen_Phase24_review_scripts/`.

**A0 — factor-eight identity.** Built `Θ`, `Θ'`, `Θ''`, `ω` from the definition;
computed `γ(n)` independently from the `ξ(½+z)` Taylor series. Manuscript form
fails (table in Finding 1); corrected form verified to 40+ digits for `n=0..6`.

**A1 — Lemma S.** Rouché boundary sum, worst case `θ ↑ π/2`:

| `ℓ` | `2η(ℓ)` | `3M/(2e^ℓ)` | sum | `<1` |
|---|---|---|---|---|
| 12 | 0.80676 | 1.64e−4 | 0.80693 | ✔ |
| 13 | 0.75456 | 6.41e−5 | 0.75462 | ✔ |
| 20 | 0.52678 | 8.12e−8 | 0.52678 | ✔ |
| 50 | 0.24432 | 1.65e−20 | 0.24432 | ✔ |

Also `m(12) = 7.2903 > 0`; `1/m(12) = 0.137168 ≤ 7/50 = 0.14` (true, and tight);
`M(12)/e¹² = 1.096e−4 ≤ 7/50`; `3M(12)/(4e¹²) = 8.22e−5 < 10⁻⁴`;
`m(12) ≥ 6`, giving `|L_N| ≥ ½log|N|`. `Q_N ≠ 0` is derived from the exact
identity `Q_N = NL_N(1+r−¾σ)` with `|1+r−¾σ| ≥ 151/200 > 9/16`, **before**
implicit differentiation — the ordering the gate asks about is correct.

**A2/A3 — contour off the real axis, in the new sectors.** For each `s`, I
computed `∫_0^∞ g_s(u)du` on the positive ray and
`E_s + ∫_1^∞ g_s(x+ib)dx` on the shifted ray, `b = Im L_s`:

| `|s|` | `arg s` | `Im L_s` | `\|arg K\|` | contour rel. err. | `\|E₁\|·\|K\|` |
|---|---|---|---|---|---|
| 3200 | 1/200 | +0.0042062 | 0.0040776 | 0 | 0.1275 |
| 3200 | 1/400 | +0.0021031 | 0.0020388 | 0 | 0.1275 |
| 51200 | 1/200 | +0.0044232 | 0.0043565 | 0 | 0.1128 |
| 51200 | 1/400 | +0.0022116 | 0.0021783 | 0 | 0.1128 |

The identity holds to working precision at complex `s`; `|Im L_s| ≪ 1/20` and
`|arg K| ≪ 1/20` as required; and `|E₁|·|K|` is identical to its real-axis
value, confirming sectorial uniformity of the `O(1/|K|)` rate.

**A4 — derivative constants by a third, independent path.** Previously I used
the exact symbolic tower and 7-point central differences. Here I added
**Cauchy circle integrals** of the true Mellin `h` (32 points, radius 1), a
different numerical path. At `n = 400`, `ℒ_n = 4.1181`:

| `m` | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| Cauchy circles | 1.593 | −1.832 | 3.960 | −12.544 | 52.318 |
| central differences | 1.593 | −1.832 | 3.961 | −12.544 | 52.320 |
| tower + chain rule + normalization terms | 1.5926 | −1.8296 | 3.953 | −12.515 | 52.17 |

(values are `h^{(m)}(n)·n^{m−1}·ℒ_n`). The third row is the exact rational
tower evaluated at `r = 1/ℒ_n = 0.24283`, times `2^m/2^{m−1}` from `N = 2x−2`,
**plus** the explicit `d^m/dz^m[log(2z)+log(2z−1)]` normalization contribution
`(−1)^{m−1}(m−1)!·2ℒ/z`. All three agree to 0.02–0.3%. This confirms
simultaneously the limits `2, −2, 4, −12, 48`, the `O(1/ℒ)` correction
structure, and the manuscript's claim that the explicit normalization terms are
lower order — the latter accounts for `−2.47` of the gap at `m = 6`.

**A5 — sixth-order denominator and majorant.** Rebuilt `G_0` and
`𝒟 = ∂_N + (L/Q)∂_L`, iterated six times. Reduced denominator is exactly
`(4+4r−3σ)¹²`; numerator has exactly 82 terms of total degree 13; the exact
coefficientwise majorant on `|r|,|σ| ≤ 7/50` is
`6422139805764931584036533551104 / 702576099728137594188684005 = 9140.8458… < 10⁴`.
No boundary sampling is used.

**A7 — branch box.** `F(y_*) = 0`; `det DF(y_*) = −1/144`; `DF(y_*)⁻¹` has
absolute row sums `87, 15, 304/3, 10/3` so `‖·‖_∞ = 304/3`; positive-orthant
uniqueness of `y_*`. Exact box arithmetic for `0 < e ≤ 1/12`: `α/e ≥ 30`,
`t+we ≤ 11/4`, `t−1−δe ≥ 103/144 > 0`, hence `A > B > C > D > 0`; margins
`(1/2,1/2)`, `(1/4,1/4)`, `(1/3,2/3)`, `(1/12,1/12)`. All confirmed.

**A8 — polygamma pairing** at the Phase-24 test parameters (`n = 4000`), scaled
by `n⁵ℒ_n`: paired `[ψ⁵(B)−ψ⁵(C)] = −9.24`, `[ψ⁵(D)−ψ⁵(b)] = −45.07`, remote
`−ψ⁵(A) = −1.2e−5`; unpaired `ψ⁵(b) = 145.03` (grows like `ℒ_n`). The pairing is
both necessary and sufficient. Also `B−C = 2705.3 = n·w/ℒ_n` exactly, matching
the claimed `O(n/ℒ_n)`.

**A9 — Hermite–Genocchi.** `vol(Δ₆) = 1/6! = 1/720`. On `f(z) = z⁶` with nodes
`0,1,2,3,4,5` and `z = 2+3i`, the divided difference `f[x₀..x₆] = 1.0` exactly,
equal to `f⁽⁶⁾/720 = 720/720`. Normalization confirmed.

**Finding-2 demonstration.** Built `p_F` at real branch parameters with `d = 16`
and compared both radius quantities at all 15 critical points — table in
Finding 2.

**Finding-5 arithmetic.** `12 + 8√6 = 31.596` (derived) vs `8 + 12√6 = 37.394`
(printed); `K_0` `262144` vs `369664`.

**Bundle integrity.** `VERIFY_BUNDLE.py` → PASS, 106/106 files. I also ran
`verify_interval_certificates.py` → PASS (and read it: exact `Fraction`
arithmetic, no floats, but it asserts the *stated* `c_loc_upper == 38`).

**Lean sources.** Read all 14 modules. Scanned for `sorry`, `admit`, `axiom`,
`native_decide`, `unsafe`, `@[implemented_by]`, `partial def` — **none found**.
The new modules are honestly scoped: `QuotientAdapter.lean` proves exactly the
`c_{k+2} = 2c_{k+1} − c_k` induction and nothing more;
`ComplexHermiteGenocchi.lean` takes the divided-difference estimate as the named
hypothesis `hHG` and marks the unused zero-hypothesis with an underscore;
`SaddleBounds.lean` proves the `9/16` and `151/50` margins and explicitly
disclaims Rouché. The `FORMALIZATION_LEDGER.md` descriptions match what the
files actually prove — I checked each row.

---

## 5. Claims I could not check

1. **Primary PDFs.** GORZ v2, GORTTW v3, Holland v1, MMP v3, MSS are not in the
   bundle and I did not retrieve them. `SOURCE_HASHES.sha256` pins them but the
   binaries are outside. I verified the *mathematics* that matters numerically
   instead (the coefficient identity, GORZ's `b₁`, Holland's eq. (20)); I cannot
   certify the MMP 2.7(iii)/2.11/2.17 or MSS Theorem 1.6 statements or the
   claimed theorem-number correction. `PRIMARY_SOURCE_AUDIT.md` is careful and
   self-consistent, but it is an author-side audit.
2. **Lean build.** No toolchain here; I ran nothing. I read every module and
   independently reproduced the finite facts they certify that touch the
   analytic gates.
3. **Algebraic gates.** The `₃F₂` ODE, the ratio-free Gershgorin lemma, the
   finite-free convolution steps, and the dominant-maximum argument are the
   other track's. I did confirm, at concrete parameters, that `p_F` has `d`
   distinct positive roots and that the localization holds with a 17× margin.
4. **Uniformity.** My numerics reach `n ≈ 10⁴`, `|s| ≈ 10⁷`. The argument bites
   at thresholds the project itself describes as astronomical.
5. **`release_checks.py` / `mutation_tests.py` end to end.** They need a
   repository root; I read them and ran only `verify_interval_certificates.py`.
6. **The deferred Mathematica reconstruction** (`MATHEMATICA_FOLLOWUP.md`) has
   not run. My symbolic work used SymPy, so it does **not** supply the CAS
   diversity that item asks for — it is the same common-mode risk. That
   limitation is correctly disclosed in `KNOWN_LIMITATIONS.md` item 6.

---

## 6. Disposition of the prior analytic round's findings

Since separation already failed (§0), withholding this would help no one. All
nine of my prior findings are discharged in the evidence notes:

| Prior | Subject | Status in Phase 24 |
|---|---|---|
| F1 | Sector `θ` unfixed; `θ`-uniformity scope | **Closed.** `θ_1 = 1/100` in Lemma 21A, `θ_1 = 1/200`, `θ_0 = 1/400` in Theorem 21B, with the shrink argument stated. |
| F2 | `\|Im L_s\| < 1/20` needed `\|s\| ≳ 10¹⁸²` | **Closed, and well.** New (7a)/(7b): taking imaginary parts of `L = Log s − Log L − logπ + Log(1−3L/(4s))` with `\|arg L\| ≤ \|b\|/Re L` gives `\|b\| ≤ 1/100 + \|b\|/7.290 + 2e−4`, hence `\|b\| < 0.012 < 1/20` **at `ℓ ≥ 12`**. I verified the inequality. This removes an astronomical constant for the cost of four lines. |
| F3 | Complex Hermite–Genocchi never stated | **Closed.** Stated in `phase18/…` §8 with the convexity hypothesis and `1/m!` mass, plus a Lean adapter. |
| F4 | Quotient hinge asserted, not displayed | **Closed.** Manuscript Lemma 5.1 plus `QuotientAdapter.lean`. |
| F5 | Stale conditionality in the dependency firewall | **Closed.** Firewall, phase9, phase17 all updated. |
| F6 | Prop 2.2 hypotheses omitted; `ρ ≥ d` wrongly reasoned | **Closed.** phase17 §4 now lists `d≥5`, reality, `c(d)>0`, `ε<16`; `ρ ≥ d` now derived from the wedge. |
| F7 | LaTeX defects; `R_N = O(1/N)` | **Closed.** `\frac` and `\log` repaired, brackets closed, and `Log R_N = −1/(6N²) + O(1/N³)` — which matches my own expansion exactly. |
| F8 | Effectivity ledger incomplete | **Partly closed.** `KNOWN_LIMITATIONS.md` item 7 is honest; the unconverged `10.7` diagnostic and the `n ≈ 10²¹` box-entry threshold are still not recorded. Not re-raised. |
| F9 | Registry and claim ledger missing from the bundle | **Closed.** Both present and hash-verified. |

The repair work is real and careful. That makes the two new P1s more, not less,
worth fixing: they entered when the notes were compressed into a manuscript, and
nothing in the Phase-24 gate apparatus was capable of catching them.

---

## 7. Release recommendation

**R1. Do not release, cite, announce, or circulate.** The manuscript's own
status box and `KNOWN_LIMITATIONS.md` item 9 already say this; they are correct.

**Blocking (must clear before the next freeze):**

1. **Finding 1** — replace `eq:factor8` with the verified identity
   `γ(n) = (8n!/(2n)!)∫_0^∞ ω(e^{2u})e^{u/2}u^{2n}du`, and re-derive the
   displayed sentence about character-for-character GORZ/GORTTW comparison from
   the corrected form.
2. **Finding 2** — replace `eq:radius` with `|y^k p_F^{(k)}(y)/p_F(y)| ≤ ρ^k`,
   `1 ≤ k ≤ d`, matching the `T_k` the same section defines.

**Strongly recommended before the next freeze:**

3. **Finding 3** — state the multiplier stability lemma with all hypotheses.
4. **Finding 4** — display the three-line exponent arithmetic.
5. **Finding 5** — use the derived `C_loc = 12+8√6` (or say explicitly that
   `8+12√6` is a deliberate over-estimate), and propagate to the certificate,
   registry, and `K_0`.
6. **Finding 10** — add a numerical equation-regression gate. This is the
   structural lesson of this round: every existing gate passed on a manuscript
   with a false equation (1).
7. Findings 6–9 — editorial.

**And, separately from the mathematics:**

8. **Get a genuinely separated analytic pass.** §0 explains why this report is
   not one. The bundle's separation protocol is sound; the failure was that the
   same model reviewed both freezes in the same session. Use a different
   provider, or at minimum a fresh session with no prior context, and record in
   `REVIEW_SEPARATION.md` that model-level separation — not just document-level
   separation — is required.
9. **Human review remains necessary.** `KNOWN_LIMITATIONS.md` item 1 is right
   and should not soften.
10. **Scope discipline** is correctly maintained throughout (asymptotic
    hyperbolicity of Jensen polynomials; no RH consequence; existential
    constant). Keep it.

---

## 8. Certification

I have identified every unresolved P0/P1 issue known to me: two, both in the
unified manuscript, both stated above with verified corrections. I have not
treated Lean compilation or repository symbolic artifacts as proof of any
analytic statement; where I state a computation as verified I performed it here
from the definitions, and the scripts are attached.

I record two non-standard disclosures: **the reviewer is an AI language model**,
and **the reviewer is the same model that reviewed the previous freeze, in the
same session, with full memory of that round** — so this is a re-review, not the
separated first pass the packet requested.

**Reviewer:** Claude Opus 5 (Anthropic) — AI pre-review
**Separated first-pass completed before cross-review:** **NO** (see §0)
**Date:** 2026-08-16
