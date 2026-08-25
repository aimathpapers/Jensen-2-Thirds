# Holland v1 dependency audit for the candidate two-thirds wedge

Date: 2026-08-15  
Source version: arXiv:2608.08682v1, submitted 2026-08-09  
Status: primary-source seam audit complete; Phase 20 supersedes the black-box
Holland dependency; disclosed AI review is not peer review

## 1. Frozen source

Primary records:

- PDF: `https://arxiv.org/pdf/2608.08682v1`
- source: `https://export.arxiv.org/e-print/2608.08682v1`
- version record: `https://arxiv.org/abs/2608.08682v1`

Frozen SHA-256 values:

| Artifact | SHA-256 |
|---|---|
| Holland v1 PDF | `3fc31ba84fb113bc0b3109fb0e569bd1d7183018485aca1eb1dab565c839b49d` |
| Holland v1 arXiv source archive | `f2fe1a202eae2d9a54291f223897b4fc5355011d6f4d0470d64c9d420bbb18af` |
| extracted `jensen.tex` | `f561d6dd53606ae054e5ab5fcb8dad4e9690cb9557c27b0a1a3845260f5205e0` |

The source is a very recent, unrefereed v1.  These hashes identify the exact
dependency but do not validate it.

### 1a. Second-order source: GORTTW

Holland's saddle apparatus is not self-contained.  Proposition 4.1 derives its
central representation (20) from the complex form of `[3, (3.1)--(3.2)]`, and
his complex `L_x` is defined only as "the branch of the holomorphic
continuation used in `[3, Section 3]`".  Holland's `[3]` is

> M. J. Griffin, K. Ono, L. Rolen, J. Thorner, Z. Tripp, and I. Wagner,
> *Jensen polynomials for the Riemann xi-function*, **Adv. Math. 397 (2022),
> Paper No. 108186**; `https://arxiv.org/abs/1910.01227`.

Unlike Holland v1, GORTTW is **published and peer-reviewed**.  It is therefore
a dependency of the whole chain, but a materially lower-risk one, and it must
be listed as such rather than left implicit inside a Holland proposition
number.

Primary records:

- journal: `https://doi.org/10.1016/j.aim.2022.108186`
- arXiv abstract: `https://arxiv.org/abs/1910.01227`
- arXiv v3 PDF: `https://arxiv.org/pdf/1910.01227v3`

| Artifact | SHA-256 |
|---|---|
| GORTTW arXiv v3 PDF | `f203487acc45a58808462e897240ce4929c998d9f0230d9a4bedb6d3841c3b2c` |
| GORTTW arXiv v3 source archive | `d3918516b2310ec7215129122515b394c2735a43cb95a627815f75096f416c1c` |
| extracted `Jensen_Revision.tex` | `e482b9b43840543af9066d67196e31d9166f9920a5be356dc2c35ef3a7773c98` |

Note the version caveat already recorded in
`phase4/C48_PRIMARY_SOURCE_FREEZE.md`: Holland observes that the arXiv v3
effective-Hermite theorem gives `n >= c e^{d/2}` while the published article
states the weaker `n >= c e^d`.  Any citation to GORTTW must therefore name
the version, and the Section 3 saddle material must be diffed between v3 and
the journal text.

> **Phase-21/23 update.**  The dependency table below records the historical
> audit that motivated the direct contour proof.  Theorem 21B now supplies the
> sectorial interface internally; GORTTW (3.2) is retained as a frozen source
> comparison, not consumed as a premise.

## 2. Consumed interfaces

| Source interface | What Holland states | Local use or extension | Audit requirement |
|---|---|---|---|
| Coefficient normalization and moment continuation, equations (13)--(14) | `gamma(z)` in terms of `M_z` and `Gamma(z+1/2)` | Defines the exact coefficient-ratio logarithm and produces the gamma/polygamma terms | Check the factor `4^z`, the centered-xi normalization, and the positive real branches |
| Proposition 2.2 | Five-match multiplier stability with `epsilon<16` | Applied unchanged because the new multiplier has six matches and `epsilon<=1` | Confirm PDF/TeX threshold and every sign/critical-point hypothesis |
| Proposition 4.1 | Sectorial nonvanishing of `M_z`; a real-on-positive-axis logarithm; saddle decomposition; remainder derivatives through order five | Supplies the nonvanishing sector and order-zero holomorphic remainder estimate; Phase 18 proves the new order-six corollary | Recheck the complex saddle input, nested-sector geometry, and logarithm normalization |
| Lemma 4.2 | Signed derivatives through order four and complex proportional-neighborhood bounds at orders four and five | Supports the existing branch proof and supplies the model for the new order-six statement | Confirm the bounds are complex for `|w|<=eta*x`, not merely real bounded-shift claims |
| Quotient coordinates and Laguerre/Jacobi/two-Jacobi model | Exact finite ratio families and coefficient recovery | The local proof frees `D` and matches one additional quotient | Reconstruct all orientations, scales, and parameter-domain hypotheses |
| Finite-free factorization, positive roots, and simplicity | Positive-rooted two-Jacobi comparison in Holland's parameter range | Reused on a different branch where `(C-D)/C -> 1/2` | Audit the cited finite-free and logarithmic-mesh theorems directly, not only Holland's paraphrase |
| Ratio-free Jacobi localization and derivative recurrence | Root localization and critical-point derivative control for Holland's branch | Phase 16 replaces the small-perturbation step by an exact nonperturbative recurrence | Recheck the source localization hypotheses and the local recurrence coefficients |
| Lemma 8.1 residual construction | Holomorphic logarithmic residual, paired polygamma terms, interpolation, and exponentiation at order five | Phase 18 follows the same architecture at order six with a new parameter pairing | Check every complex domain, line-integral path, and logarithm-zero assertion |
| **GORTTW `[3]`, Section 3, equations (3.1)--(3.2)** (published, Adv. Math. 397 (2022)) | Exact kernel identity and real saddle formula; one terse sentence asserts a complex extension after replacing the index by its modulus | Exact identity and main-term comparison only; Phase 21 directly proves `C48-GORTTW-SECTOR`, including `M_z != 0`, the logarithm branch, and the remainder | The source does **not** spell out sector, branches, holomorphic error, or uniformity; see `phase20/GORTTW_PRIMARY_INPUT.md` |
| **GORTTW `[3]`, Section 3**, holomorphic continuation of `L_x` | The branch of the saddle variable off the real axis | **No longer consumed.** Phase 18 proves existence, uniqueness, holomorphy, and sectorial asymptotics of the branch outright (Lemma S) | Confirm only that GORTTW's branch is the continuation of the positive real solution; uniqueness then identifies it with Lemma S's |

## 3. New mathematics that must not be attributed to Holland

The following are local claims:

1. the signed fifth coefficient `-12`;
2. the sixth main coefficient `48` and the exact normalized denominator
   `(4+4/L_N-3L_N/N)^12`;
3. **Lemma S**: existence, uniqueness, holomorphy, and uniform sectorial
   asymptotics of the saddle variable `L_N`, together with `Q_N != 0` and the
   conservative effective bound
   `|G_0^(6)(N)| <= 20000/(|N|^5 log|N|)` for `|N| >= e^12`;
4. the complex-uniform sixth-saddle lemma;
5. the four-parameter positive branch matching `R_0,...,R_5`;
6. positive-orthant uniqueness of its limiting system;
7. the nonperturbative derivative-radius recurrence on the new branch;
8. the `2/3` Jensen wedge.

Holland's paper motivates these extensions and supplies several interfaces,
but it proves only the `3/5` wedge stated in his Theorem 1.1.

## 4. Proposition 2.2 correction

The official PDF and TeX source state

\[
\sup_{\Omega_r}|c-1|\le\varepsilon<16.
\]

The first review's `1/6` reading is an HTML/text-conversion error.  The
Phase-17 main proof now invokes the proposition exactly as printed.  Its
independent sixth-match refinement, with sufficient threshold `32`, is
retained only as supplementary algebra.

## 5. Sectorial order-six dependency

Proposition 4.1 states the remainder estimate only through derivative order
five.  Phase 18 writes the derivative-six argument as a separate corollary and
combines it with a direct uniform bound for the analytically continued saddle
main term.  The two halves now rest on different footings, and the audit
should record the distinction.

**Remainder half — printed, not proof-internal.**  Earlier drafts said this
corollary depends on the internals of Holland's proof.  It does not, and the
weaker claim should be dropped:

- `R(z) = O(|z|^{-1+eps0})` is exactly the `r = 0` case of the **printed**
  estimate (19);
- holomorphy of `R` follows from the **printed** decomposition (18), since
  `h` is holomorphic on the sector by the printed Proposition 4.1 (`M_z != 0`,
  branch real on the positive axis), the explicit terms are elementary, and
  `G_0(2z-2)` is holomorphic by Lemma S.

Cauchy on proportional discs then gives order six from printed statements
alone.  Holland's own proof uses the same device ("a disk `|zeta - z| <=
delta|z|` about a point in a smaller closed sector stays in the original
sector, and `|zeta| asymp |z|` there"), so the mechanism is confirmed, but it
is no longer load-bearing that it be.

**Main-term half — closed by Lemma S.**  This half previously rested on the
unproved assertion `|L_N| asymp log|N|`, `1/L_N -> 0`, `L_N/N -> 0`, wrongly
described as inherited.  `C48_SECTORIAL_SADDLE_VARIABLE.md` now proves it
outright by Rouché, with no input from Holland or GORTTW, and supplies the
conservative effective bound
`|G_0^(6)(N)| <= 20000/(|N|^5 log|N|)` for `|N| >= e^12`.

Both halves remain new local mathematics and must be reviewed as such.  What
has changed is that neither is now discharged by citing a proposition number,
and neither depends on reading inside another author's proof.

## 6. Ratio-free Jacobi extraction

Holland's assembled finite-free root lemma also assumes
`(C-D)/D<=1/4`; that hypothesis fails on the new branch, where the ratio
tends to one.  The local proof therefore does not cite the assembled lemma.

The proof of Holland's lemma first establishes a genuinely ratio-free
single-factor statement.  In the frozen TeX this is the calculation from
`eq:jacobi-diagonal` through `eq:Jacobi-block-location`.  For

\[
q_{U,V}(y)={}_2F_1(-d,U;V;y/U),
\]

the only hypotheses used are `U>=V+d` and `V>=32d`.  The transported Jacobi
matrix has diagonal displacement below `4d` and total adjacent off-diagonal
mass at most `4sqrt(Vd)`.  Gershgorin therefore gives

\[
\operatorname{roots}(q_{U,V})
\subset[V-8\sqrt{Vd},V+8\sqrt{Vd}].
\]

Phase 16 now restates this lemma and its matrix calculation before applying
it separately to `(A,B)` and `(C,D)`.  The subsequent multiplicative interval
bound and the choice of `K_0` are local arguments.  A human reviewer must
still compare the displayed matrix entries and inequalities line by line with
the frozen PDF/TeX.

One further extraction is available and should be used rather than
reconstructed.  Holland's **Lemma 7.2**, the multiplicative finite-free
interval bound

\[
\operatorname{roots}(q)\subset[v_-,v_+]\subset(0,\infty)
\ \Longrightarrow\
v_-u_i\le w_i\le v_+u_i ,
\]

is itself ratio-free.  It is proved from preservation of interlacing under
multiplicative finite-free convolution, citing Martínez-Finkelshtein--Morales--
Perales Proposition 2.11 (IMRN 2024, refereed), and uses no part of (57).
Phase 16 may therefore cite Lemma 7.2 directly for the product-interval step.

## 6a. Second-order dependency on GORTTW Section 3

Recorded here because it was previously invisible: it sat inside a Holland
proposition number rather than in this table.

**What is consumed.**  Holland's Proposition 4.1 is proved by transporting the
complex form of `[3, (3.1)--(3.2)]` into his normalization, yielding his (20).
Everything Phase 18 inherits from Proposition 4.1 — non-vanishing of `M_z` on
the sector, the branch of `h` real on the positive axis, the decomposition
(18), and the remainder estimate (19) — therefore rests on GORTTW Section 3.
This is a genuine load-bearing dependency of the `2/3` chain.

**What is no longer consumed.**  Holland defines the complex `L_x` only as
"the branch of the holomorphic continuation used in `[3, Section 3]`".  That
deferral used to carry the assertions `|L_N| asymp log|N|`, `1/L_N -> 0`,
`L_N/N -> 0`.  Lemma S now proves all of them from the saddle equation alone.
Since a holomorphic continuation of the positive real solution into the simply
connected sector is unique, Lemma S's branch *is* GORTTW's branch.  The
citation survives only as an identification remark.

**Net effect on risk.**  Favourable.  The surviving GORTTW dependency is on a
**published, peer-reviewed** paper (Adv. Math. 397 (2022), Paper No. 108186),
whereas the rest of the chain rests on an unrefereed v1 preprint.  Moving this
dependency out of the shadows lowers, rather than raises, the assessed risk —
but only once it is actually audited.

**Audit obligations.**

1. Read GORTTW Section 3 directly.  Confirm (3.1)--(3.2), the sentence
   following (3.2) asserting uniformity on fixed closed sectors in
   `Re z > 1`, and the construction of the continued saddle variable.
2. Confirm Holland's renormalization of `[3, (3.1)--(3.2)]` into his (20),
   including the `2^{2z-2}` factor and the division by `8` arising from
   `(4w^2-1)Lambda(1/2+w) = 8 xi(1/2+w)`.
3. Diff GORTTW arXiv v3 against the published Adv. Math. text over Section 3,
   and cite the version used.  A version discrepancy is already known to exist
   elsewhere in that paper (`e^{d/2}` versus `e^{d}`).
4. Confirm that GORTTW's `L_x` is the continuation of the positive real
   solution, which is all Lemma S needs for identification.

## 7. Version and author protocol

Before submission:

1. check the arXiv record for a v2 or published version;
2. diff every consumed statement and normalization against the frozen v1;
3. ask Holland whether any correction is known, especially around the
   normalization paragraph following the complex saddle expansion;
4. send Holland the precise sixth-saddle lemma and ask whether the sectorial
   continuation introduces an overlooked obstruction;
5. retain a self-contained proof of the new order-six corollary even if a
   later Holland version states it;
6. freeze the GORTTW artifacts named in §1a, name the version cited, and diff
   Section 3 between arXiv v3 and the journal text;
7. retain Lemma S even if a later version of Holland or GORTTW states the
   sectorial asymptotics, so that the `2/3` chain never depends on another
   paper's choice of branch.

## 8. Release disposition

The source dependency is identified and locally scoped.  Phase 21 has now
proved the explicit GORTTW-type sectorial statement directly from the Mellin
integral, so GORTTW Section 3 is no longer a premise.  Available analytic and
algebraic reviews are AI technical audits, not human or peer review.  Their
Phase-23 findings are repaired, and the repaired tree must be frozen and
re-reviewed before circulation.

Three dependencies have been *removed* rather than merely documented, and the
release note should say so: the sectorial asymptotics of `L_N` (now Lemma S)
the branch of `L_N` itself (now unique by continuation), and the complex
coefficient asymptotic (now Theorem 21B).  None is an inherited assumption.
