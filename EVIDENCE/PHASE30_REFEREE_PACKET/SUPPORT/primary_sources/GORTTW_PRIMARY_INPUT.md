# GORTTW primary-input audit for the Holland saddle

Audit date: 2026-08-15
Scope: the complex saddle input from Griffin--Ono--Rolen--Thorner--Tripp--Wagner
(`GORTTW`) and its use in Holland, Proposition 4.1
Status: historical primary-source audit; the printed GORTTW text does not
document all of Holland's claimed sector-uniformity, and Phase 21 now proves
the required sectorial statement directly rather than importing it

> **Phase-21/23 update.**  The source limitations catalogued below remain
> accurate.  Their disposition changed: GORTTW (3.2) is now a comparison
> target and normalization check, not an external analytic premise.

## 1. Primary sources and frozen artifacts

1. M. J. Griffin, K. Ono, L. Rolen, J. Thorner, Z. Tripp, and I. Wagner,
   *Jensen polynomials for the Riemann xi-function*,
   [arXiv:1910.01227v3](https://arxiv.org/abs/1910.01227v3), especially
   Section 3, equations (3.1)--(3.4). The official record identifies v3 as
   revised 17 December 2020 and links the published version,
   *Advances in Mathematics* **397** (2022), Paper 108186,
   [DOI 10.1016/j.aim.2022.108186](https://doi.org/10.1016/j.aim.2022.108186).
2. M. J. Griffin, K. Ono, L. Rolen, and D. Zagier (`GORZ`),
   *Jensen polynomials for the Riemann zeta function and other sequences*,
   [arXiv:1902.07321v2](https://arxiv.org/abs/1902.07321v2), equations
   (1), (11)--(16); published in *PNAS* **116** (2019), 11103--11110,
   [DOI 10.1073/pnas.1902572116](https://doi.org/10.1073/pnas.1902572116).
3. J. Holland, *A new hyperbolicity wedge and a joint semicircle limit for
   Jensen polynomials of Riemann's xi-function*,
   [arXiv:2608.08682v1](https://arxiv.org/abs/2608.08682v1), equations
   (10), (14)--(20) and Proposition 4.1, PDF pp. 5--7.

The equation-level comparison below was made against the official arXiv
source/PDF artifacts, not an HTML-to-text reconstruction. The publisher
record confirms the GORTTW bibliographic publication, but no claim is made
here that the journal PDF was byte-compared with arXiv v3.

| Frozen artifact | SHA-256 |
|---|---|
| GORTTW official arXiv v3 PDF | `f203487acc45a58808462e897240ce4929c998d9f0230d9a4bedb6d3841c3b2c` |
| GORTTW official arXiv v3 source download (gzip-compressed single TeX file) | `d3918516b2310ec7215129122515b394c2735a43cb95a627815f75096f416c1c` |
| Decompressed GORTTW `Jensen_Revision.tex` bytes | `e482b9b43840543af9066d67196e31d9166f9920a5be356dc2c35ef3a7773c98` |
| Holland official arXiv v1 PDF | `3fc31ba84fb113bc0b3109fb0e569bd1d7183018485aca1eb1dab565c839b49d` |
| Holland official arXiv v1 source archive | `f2fe1a202eae2d9a54291f223897b4fc5355011d6f4d0470d64c9d420bbb18af` |
| Holland v1 `jensen.tex` | `f561d6dd53606ae054e5ab5fcb8dad4e9690cb9557c27b0a1a3845260f5205e0` |

## 2. Exact printed GORTTW saddle statement

GORTTW Section 3 defines, for `Re s > 0`,

\[
 F(s)=\int_1^\infty (\log t)^s t^{-3/4}
       \sum_{k\ge 1}e^{-\pi k^2t}\,dt.
\]

Its equation (3.1), on printed p. 6 of the arXiv v3 PDF, is

\[
 \gamma(M)=\frac{\Gamma(M+1)}{\Gamma(2M+1)}
 \frac{32\binom{2M}{2}F(2M-2)-F(2M)}{2^{2M-1}}.
 \tag{G3.1}
\]

The paper then says that this formula is holomorphic for `Re M > 1`. For
real `M>0`, it defines `L_M` as the positive solution of

\[
 M=L_M\left(\pi e^{L_M}+\frac34\right),
 \qquad
 K_M=(L_M^{-1}+L_M^{-2})M-\frac34.
 \tag{S}
\]

It **asserts**, without a proof in Section 3, that `L_M` and `K_M` extend as
holomorphic nonvanishing functions to `Re M>1`. Its equation (3.2) is

\[
\begin{aligned}
 \gamma(M)
 &=\frac{e^{M-2}M^{M+1/2}L_{2M-2}^{,2M-2}}
 {2^{2M-5}(2M-2)^{,2M-3/2}}
 \left(\frac{2\pi}{K_{2M-2}}\right)^{1/2} \\
 &\quad\times
 \exp\left(\frac{L_{2M-2}}4-
             \frac{2M-2}{L_{2M-2}}+\frac34\right)
 \left(1+O_\varepsilon(M^{-1+\varepsilon})\right).
\end{aligned}
\tag{G3.2}
\]

The displayed equation is introduced after the real definition (S), and its
cited precursor, GORZ (16), is a real/integer asymptotic. The only printed
complex extension is the single sentence immediately following (3.2): the
analytic continuation of `L_M` and Stirling's formula allow the same error
term for complex `M` after replacing `M` by `|M|`.

That sentence is the entire primary-source basis for the complex use. The
passage does **not** state:

- an angular sector or another precise complex asymptotic domain;
- whether the implied constant is uniform as `arg M` varies;
- the branches used in `M^{M+1/2}`, `(2M-2)^{2M-3/2}`, or the square root;
- a threshold uniform on a closed sector;
- or a theorem identifying a holomorphic relative-error function on a
  neighborhood of that sector.

The subscript `epsilon` is printed, but Section 3 does not restate its range
at (3.2). Holland later fixes `0<epsilon_0<1/2`, which is compatible with the
intended positive-small-`epsilon` use.

## 3. Normalization and the factor eight

This point is exactly checkable, and Holland's correction is right.

GORZ defines its coefficients `gamma_G(n)` by

\[
 (4w^2-1)\Lambda\!\left(\frac12+w\right)
   =\sum_{n\ge0}\frac{\gamma_G(n)}{n!}w^{2n},
 \qquad
 \Lambda(s)=\pi^{-s/2}\Gamma(s/2)\zeta(s).
 \tag{GORZ 1}
\]

Since

\[
 \xi(s)=\frac12s(s-1)\Lambda(s),
 \qquad
 s=\frac12+w,
\]

direct algebra gives

\[
 (4w^2-1)\Lambda\!\left(\frac12+w\right)
 =8\xi\!\left(\frac12+w\right).
 \tag{8xi}
\]

By contrast, GORTTW equation (1.1) defines `gamma(n)` directly by

\[
 \xi\!\left(\frac12+w\right)
 =\sum_{n\ge0}\frac{\gamma(n)}{n!}w^{2n}.
 \tag{G1.1}
\]

But GORTTW (3.1) reproduces the GORZ (13) formula for `gamma_G`, with no
division by eight. Thus GORTTW (1.1) and (3.1) are inconsistent by the
constant factor `8`. This is not a conjectural objection: it follows from
the two displayed definitions and (8xi).

Holland uses the direct-xi normalization. From

\[
 \xi\!\left(\frac12+z\right)
 =\int_0^\infty\Phi(u)\cosh(zu)\,du,
 \qquad
 M_z=\int_0^\infty\Phi(u)u^{2z}\,du,
\]

coefficient comparison at integers gives Holland (10):

\[
 \gamma_H(n)=\frac{n!}{(2n)!}M_n.
\]

GORZ (13) and (8xi) therefore give the exact continued-moment identity
printed as Holland (17):

\[
 M_z=2^{-2z-2}
 \left(32\binom{2z}{2}F(2z-2)-F(2z)\right).
 \tag{H17}
\]

Equivalently, `gamma_G=8 gamma_H`. Consequently the GORTTW saddle (3.2)
must be divided by `8` in Holland's normalization. This changes the
denominator `2^{2z-5}` to `2^{2z-2}`, exactly as in Holland (20). It changes
an absolute logarithm only by the additive constant `-log 8`; it cancels
from coefficient ratios and disappears under positive-order logarithmic
differentiation.

## 4. What Holland Proposition 4.1 claims

Holland, Proposition 4.1 (PDF p. 7), states that there are
`0<theta<pi/2` and `x_0>0` such that the continued moment `M_z` is nonzero
on

\[
 \mathfrak S_\theta
 =\{z:|z|\ge x_0,\ |\arg z|\le\theta\}.
\]

It then chooses `h=log M` real on the positive axis and, with `N=2z-2`,
writes

\[
 h(z)=G_0(N)+\log\left(32\binom{2z}{2}\right)
 -(2z+2)\log2+c_{\rm sad}+\mathcal R(z),
 \tag{H18}
\]

where

\[
 G_0(N)=(N+1)\log L_N+\frac{L_N}{4}
 -\frac{N}{L_N}-\frac12\log Q_N,
 \qquad
 Q_N=(1+L_N)N-\frac34L_N^2.
\]

For fixed `0<epsilon_0<1/2`, Holland claims on a slightly smaller closed
sector

\[
 \mathcal R^{(r)}(z)
 =O_{\epsilon_0,r,\theta}
   (|z|^{-r-1+\epsilon_0}),
 \qquad 0\le r\le5.
 \tag{H19}
\]

The proof labels the complex form of GORTTW (3.2) as uniform on every fixed
closed sector in `Re z>1`. It then derives the rest as follows:

1. choose a sufficiently narrow sector on which the continued main factor
   and all branches are holomorphic and nonzero;
2. make the relative error smaller than `1/2`, obtaining nonvanishing of
   `gamma_H(z)` and hence of `M_z` through Holland (14);
3. take a logarithm and use sectorial Stirling to obtain (H18) with an
   order-zero holomorphic remainder;
4. place disks of radius `delta |z|` inside a larger sector and apply
   Cauchy's inequalities to obtain (H19).

Conditional on a genuinely **uniform holomorphic relative asymptotic** on
the larger sector, these four deductions are standard and correct. The
Cauchy step actually works for every fixed derivative order, not only
`r<=5`; in particular, `r=6` is a corollary of the same order-zero premise.
Holland's printed proposition stops at five because that is all his theorem
uses.

## 5. Asserted versus derived

| Item | GORTTW status | Holland status | Audit conclusion |
|---|---|---|---|
| Exact `F` formula and continuation of `gamma` | Printed in (3.1), `Re M>1` | Reused through the corrected moment formula (17) | Exact after dividing by `8` |
| `L_M`, `K_M` holomorphic and nonzero | Asserted for `Re M>1`; no proof in the short Section 3 passage | Used to choose analytic branches | External assertion, not locally derived from (S) |
| Real saddle asymptotic | Printed in (3.2), citing GORZ (16) | Reused | Strong primary support, subject to the factor `8` |
| Complex saddle asymptotic | One sentence says replace `M` by `|M|` | Restated as uniform on each fixed closed sector | **The exact domain and uniformity are not explicit in GORTTW** |
| Holomorphic relative error | Not separately stated | Inferred from the exact quotient by the main factor | Valid once branches, nonvanishing of the main factor, and a sector-uniform bound are supplied |
| Nonvanishing of `gamma_H` and `M_z` | Not stated as a saddle corollary | Derived from relative error `<1/2` | Valid conditional on the uniform complex asymptotic |
| Sectorial logarithm of `M_z` | Not stated | Derived | Valid conditional on nonvanishing on a simply connected open sector |
| Derivative remainder bounds | Not stated | Derived by Cauchy for `r<=5` | Valid for every fixed `r`, conditional on a larger-sector order-zero bound |

## 6. The precise defensible external premise

The candidate manuscript should not say merely “by GORTTW (3.2)” and should
not import Holland's full Theorem 1.1 as a black box. It should isolate the
following statement as the one surviving deep analytic premise:

> **Sectorial GORTTW input.** There exist `theta>0` and `R>0` such that,
> after continuation from the positive axis, the factor on the right of the
> factor-eight-corrected GORTTW (3.2) is holomorphic and nonzero for
> `|z|>R`, `|arg z|<theta`, and the exact quotient of `gamma_H(z)` by that
> factor equals `1+E(z)`, where `E` is holomorphic and, for every fixed
> `0<epsilon<1/2`,
> `sup |E(z)| = O_epsilon(|z|^{-1+epsilon})` on a slightly larger closed
> sector.

From this premise, Holland's nonvanishing, logarithm, order-zero remainder,
and all fixed-order Cauchy derivative bounds can be reproved self-containedly.
The normalization correction is exact and should be included in that proof.

## 7. Gaps and ambiguities that remain

1. **Uniformity wording (material).** GORTTW's sentence after (3.2) does not
   explicitly say “uniform on every fixed closed sector,” even though Holland
   attributes that formulation to it. This is the main citation gap.
2. **Complex-domain proof (material).** Analytic continuation and Stirling
   alone do not, without an accompanying saddle/contour argument or a stated
   complex-uniform theorem, automatically propagate a real-axis relative
   asymptotic to a two-dimensional sector. GORTTW asserts the complex result
   but does not show that argument in Section 3.
3. **Branch data (repairable).** GORTTW does not print branch choices for the
   complex powers and square root. On a sufficiently narrow simply connected
   sector, the branches can be fixed by continuation from the positive axis,
   provided the asserted nonvanishing of `L` and `K` is accepted or reproved.
4. **Factor-eight defect (repaired).** GORTTW (1.1) and (3.1) use inconsistent
   normalizations. Holland's division by `8` is correct, and the defect does
   not affect GORTTW's ratio-based conclusions.
5. **Journal comparison (procedural).** This audit used the official arXiv v3
   equation text and the publisher's bibliographic record. A final submission
   packet should, if the journal PDF is obtained, compare its Section 3
   sentence and equations (3.1)--(3.2) against the frozen v3 source.

## 8. Bottom line

The factor-eight issue is fully resolved, and Holland's deductions from a
sector-uniform holomorphic relative asymptotic are mathematically coherent.
What is **not** yet source-verified is that GORTTW actually proves, rather
than tersely asserts, the exact sector-uniform complex asymptotic Holland
needs. The defensible package should therefore expose the “Sectorial GORTTW
input” above as its deepest external analytic dependency and should not
describe Proposition 4.1, or its order-six corollary, as independently
verified until that input is reproved from the Mellin/saddle integral or
confirmed by the GORTTW authors.
