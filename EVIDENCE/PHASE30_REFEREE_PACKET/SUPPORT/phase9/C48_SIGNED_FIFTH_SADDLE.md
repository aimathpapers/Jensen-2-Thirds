# C48 signed fifth saddle derivative

Date: 2026-08-15  
Status: paper-level derivation with the former Holland/GORTTW sector premise
replaced by the direct Phase-21 xi/Mellin proof; main-term algebra exactly
reproduced; AI pre-reviewed, not human or peer reviewed

**Phase-21/23 update.**  References below to Holland's sectorial remainder
describe the historical decomposition.  Its holomorphy and derivative control
are now supplied internally by Theorem 21B and the proportional-disk Cauchy
transport in Phases 18 and 21; GORTTW (3.2) is not an imported premise.

## Statement

Let `h(z)=log M_z` and

\[
\mathcal L_x=L_{2x-2},
\qquad 2x-2=L_{2x-2}
\left(\pi e^{L_{2x-2}}+\frac34\right),
\]

with the notation of Holland's Proposition 4.1.  Then, as `x` tends to
positive infinity,

\[
\boxed{
h^{(5)}(x)=
-\frac{12}{x^4\mathcal L_x}
\left(1+O(\mathcal L_x^{-1})\right).}
\]

The same leading asymptotic holds uniformly for `x+w` with `w` in any fixed
bounded interval.

This strengthens the absolute fifth-derivative bound displayed in Holland's
Lemma 4.2 by retaining its leading coefficient and sign.

## 1. Exact saddle-main differentiation

Set

\[
Q_N=(1+L_N)N-\frac34L_N^2,
\qquad L_N'=\frac{L_N}{Q_N},
\]

and

\[
G_0(N)=(N+1)\log L_N+\frac{L_N}{4}
-\frac{N}{L_N}-\frac12\log Q_N.
\]

Differentiate with the exact total-derivative operator

\[
\mathscr D=\partial_N+\frac{L_N}{Q_N}\partial_{L_N}.
\]

Put `r=1/L_N` and `sigma=L_N/N`.  Exact symbolic simplification gives

\[
N^4L_N\,\mathscr D^5G_0(N)
=-\frac{
6r^6+42r^5+126r^4+210r^3+146r^2+47r+6
}{(1+r)^7}+O(\sigma).
\]

The `O(sigma)` statement here is elementary rational algebra: the exact
difference from the displayed rational function is `sigma` times a rational
function whose denominator is nonzero in a fixed neighborhood of
`(r,sigma)=(0,0)`.  Therefore

\[
\mathscr D^5G_0(N)
=-\frac{6}{N^4L_N}
\left(1+O(L_N^{-1}+L_N/N)\right).
\]

As a regression, the same calculation at order four gives

\[
N^3L_N\,\mathscr D^4G_0(N)
=\frac{2r^4+10r^3+20r^2+11r+2}{(1+r)^5}
+O(\sigma),
\]

whose limit is `2`, reproducing Holland's displayed fourth-derivative main
term.

The pinned exact producer is
[`saddle_main_term.py`](../c48_jensen/symbolic/saddle_main_term.py).  Its
frozen artifact is
[`saddle_main_term.json`](../c48_jensen/symbolic/saddle_main_term.json),
SHA-256

`7816d5144a672d96d6f386fea14e2b2113404bfad3f7d484141becad29d367e2`.

## 2. Chain rule

Holland's saddle formula uses `N=2x-2`.  Hence the fifth derivative of the
main composition carries a factor `2^5`, while `N^4/x^4` tends to `2^4`.
It follows that

\[
\frac{d^5}{dx^5}G_0(2x-2)
=-\frac{12}{x^4\mathcal L_x}
\left(1+O(\mathcal L_x^{-1}+\mathcal L_x/x)\right).
\]

Since `L_x` is asymptotic to `log x`, the `L_x/x` term is absorbed by
`O(1/L_x)`.

## 3. Explicit normalization terms

Holland's Proposition 4.1 writes

\[
h(x)=G_0(2x-2)
+\log\left(32\binom{2x}{2}\right)
-(2x+2)\log2+c_{\rm sad}+\mathcal R(x).
\]

The fifth derivative of the logarithmic polynomial term is `O(x^-5)`,
which is smaller than `1/(x^4 L_x)` by a factor `O(L_x/x)`.  The linear and
constant terms vanish after five derivatives.

The direct Phase-21 remainder is holomorphic on the fixed outer sector and is
`O(x^{-1+epsilon_0})` on a smaller closed sector for every fixed
`0<epsilon_0<1/2`.  Cauchy's estimate on the explicit proportional disks from
Phase 18 therefore gives, without importing Holland Proposition 4.1,

\[
\mathcal R^{(5)}(x)=O(x^{-6+\epsilon_0}).
\]

Relative to the proposed main term this is
`O(L_x x^(-2+epsilon_0))=o(1/L_x)`.  Combining these estimates with the exact
main-term calculation proves the boxed formula.

## 4. Uniform bounded shifts

The source saddle expansion is uniform on a smaller closed sector.  Replacing
`x` by `x+w` for bounded `w` preserves that sector and changes `x`, `L_x`, and
the displayed powers by relative `1+O(1/x)`.  The same proof is therefore
uniform on every fixed bounded shift range, which is precisely what the
fivefold finite-difference integral in Phase 8 consumes.

## Scope and remaining work

This lemma supplies the missing fourth xi-side constant in the parameter
map.  It does not prove the full `C^1` adapter, because the elementary
model-side remainders still need uniform derivative bounds and the four
pieces must be assembled with one explicit error rate.

It also does not provide the later sixth derivative bound required by a
six-coefficient residual-multiplier theorem.  No Jensen-wedge or zeta-zero
claim follows from this lemma alone.

Primary source: [Holland, arXiv:2608.08682v1](https://arxiv.org/html/2608.08682v1),
especially Proposition 4.1 and Lemma 4.2.
