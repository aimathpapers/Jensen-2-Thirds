# Full `C^1` map and exact six-coefficient branch

Date: 2026-08-15  
Status: internal paper proof; finite algebra Lean-checked; independent review
pending

## 1. Result

Let `G_n` and `F` be the exact normalized quotient map and limiting map in
the Phase-13 repair specification.  On the fixed compact box `K`,

\[
\sup_{y\in K}\max\left\{
\|G_n(y)-F(y)\|_\infty,
\|DG_n(y)-DF(y)\|_\infty
\right\}
=O_K\left(\frac1{\mathcal L_n}+\frac{\mathcal L_n}{n}\right).
\tag{C1}
\]

Consequently, for every sufficiently large integer `n`, the four exact
quotient equations have a unique solution in one fixed neighborhood of

\[
y_\ast=(\alpha,t,w,\delta)=(3,2,16/3,1/3),
\]

and

\[
y_n=y_\ast+O(\mathcal L_n^{-1}).
\tag{B}
\]

The associated positive two-Jacobi model matches the normalized xi
coefficients through `R_5` exactly.

This is the missing branch theorem.  It does not by itself prove the wider
Jensen hyperbolicity wedge.

## 2. Exact decomposition

Phase 14 proves, uniformly with all four parameter derivatives, that the
Jacobi logarithms paired with the exact gamma half-shift contribute

\[
H_n(y)=H_\infty(y)+
O_K(\mathcal L_n^{-1}+\mathcal L_n/n)
\]

in value and

\[
D_yH_n(y)=D_yH_\infty(y)+O_K(\mathcal L_n^{-1}+1/n)
\]

in the parameter Jacobian.  The limiting elementary vector is

\[
H_\infty(y)=\left(
\frac1\alpha+\frac w{t^2}+\delta,
\frac w{t^3}+\delta,
\frac{3w}{t^4}+3\delta,
\frac{4w}{t^5}+4\delta
\right).
\tag{E}
\]

The only remaining term is the xi moment saddle.  It is independent of
`y`, so it contributes nothing to the parameter Jacobian.

## 3. Four saddle values

For `j=0,1,2,3`, the exact residual contains `Delta^(j+2)h(n)`.  Repeated
fundamental theorem of calculus gives

\[
\Delta^{j+2}h(n)=
\int_{[0,1]^{j+2}}
h^{(j+2)}(n+s_1+\cdots+s_{j+2})\,ds.
\tag{S1}
\]

Holland's signed derivatives through order four and the Phase-9 order-five
lemma state, uniformly on these bounded shifts,

\[
\begin{aligned}
h''(n+u)&=\frac{2}{n\mathcal L_n}
  (1+O(\mathcal L_n^{-1})),\\
h'''(n+u)&=-\frac{2}{n^2\mathcal L_n}
  (1+O(\mathcal L_n^{-1})),\\
h^{(4)}(n+u)&=\frac{4}{n^3\mathcal L_n}
  (1+O(\mathcal L_n^{-1})),\\
h^{(5)}(n+u)&=-\frac{12}{n^4\mathcal L_n}
  (1+O(\mathcal L_n^{-1})).
\end{aligned}
\tag{S2}
\]

Here one may either use the already stated bounded-shift versions or note
directly that `(n+u)^(-m)=n^(-m)(1+O(1/n))` and
`L_(n+u)/L_n=1+O(1/n)` for bounded `u`.  The latter follows
from the differentiated saddle equation

\[
L_N'=\frac{L_N}{(1+L_N)N-3L_N^2/4}=O(1/N).
\]

Insert (S2) in (S1) and apply the exact Phase-7 component scales.  The four
limits are

\[
(-1)\cdot2,\quad
(1/2)\cdot(-2),\quad
(-1/2)\cdot4,\quad
(1/6)\cdot(-12),
\]

namely

\[
S_\infty=(-2,-1,-2,-2),
\tag{S3}
\]

with common error `O(1/L_n)`.  Lean theorem
`saddleWeight_values` checks these signs and rational factors.

Adding (S3) to (E) gives exactly

\[
F(y)=\left(
\delta+\frac w{t^2}+\frac1\alpha-2,
\delta+\frac w{t^3}-1,
3\delta+\frac{3w}{t^4}-2,
4\delta+\frac{4w}{t^5}-2
\right).
\]

Together with the Phase-14 derivative estimate, this proves (C1).

## 4. Fixed-inverse contraction

Let

\[
J=DF(y_\ast)
\]

in the analytic coordinate order `(alpha,t,w,delta)`, and let `P=J^(-1)`.
Lean checks `det J=-1/144` and both identities `JP=PJ=I`.

Throughout this section, vector norms are sup norms and matrix norms are the
induced maximum-row-sum norms in that fixed coordinate order.  Thus every
displayed operator-norm inequality is submultiplicative with the same
convention.

Choose a closed sup-norm box `K_0` centered at `y_*` and contained in the
interior of `K`.  Since `P DF(y_*)=I` and `DF` is continuous, shrink `K_0`
so that

\[
\sup_{y\in K_0}\|I-PDF(y)\|_\infty\le1/4.
\tag{C2}
\]

By (C1), for all sufficiently large `n`,

\[
\sup_{y\in K_0}\|P(DG_n(y)-DF(y))\|_\infty\le1/4.
\tag{C3}
\]

Define

\[
T_n(y)=y-PG_n(y).
\]

Equations (C2)--(C3) give `||DT_n||_infty<=1/2` on `K_0`.  Also
`F(y_*)=0`, so (C1) implies `T_n(y_*)-y_* -> 0`.  Increase the threshold
until this displacement is at most half the distance from `y_*` to the
boundary of `K_0`.  Then `T_n` maps `K_0` to itself and is a contraction.
Banach's fixed-point theorem supplies a unique `y_n in K_0` with
`G_n(y_n)=0`.

The standard contraction estimate gives

\[
\|y_n-y_\ast\|_\infty
\le2\|P\|_\infty\|G_n(y_\ast)\|_\infty
=O(\mathcal L_n^{-1}+\mathcal L_n/n)
=O(\mathcal L_n^{-1}),
\]

because `L_n^2/n -> 0`.  This proves (B).

## 5. Positivity and exact coefficient matching

The convergence (B) gives, for sufficiently large `n`,

\[
\alpha_n>0,\quad t_n>1,\quad w_n>0,\quad\delta_n>0.
\]

Therefore

\[
A_n\sim3n\mathcal L_n,\quad
B_n,C_n\sim2n,\quad D_n\sim n,
\]

and in particular `A_n>B_n>0` and `C_n>D_n>0` eventually.

The four components of `G_n` are nonzero scalar multiples of the zeroth
through third forward differences of `E_(n,k)`.  Lean theorem
`forwardDiffs_zero_iff_values_zero` checks that their simultaneous vanishing
is equivalent to

\[
E_{n,0}=E_{n,1}=E_{n,2}=E_{n,3}=0.
\]

Hence the model and xi quotient invariants agree for `q_0,...,q_3`.  Choose
the free scale so that `R_1` agrees.  Here is the exact hinge, including its
index count.  Put

\[
 r_k=\log\frac{\gamma_H(n+k+1)}{\gamma_H(n+k)},\qquad
 m_k=\log\frac{(A+k)(C+k)}{(B+k)(D+k)}.
\]

Legendre duplication and the definitions in the Phase-13 specification give

\[
 Q_{n,k}=-\Delta_k r_k,\qquad
 M_{n,k}=-\Delta_k m_k,
\]

and therefore

\[
 \boxed{E_{n,k}=\Delta_k(r_k-m_k).}
\tag{QH}
\]

Thus `E_(n,0)=...=E_(n,3)=0` says that `r_k-m_k` is one constant for
`k=0,...,4`: the five consecutive coefficient ratios agree up to a single
geometric scale.  Both target and comparison sequences have constant term
`R_0=F_0=1`.  The model has `F_1=S/B`, so the positive choice
`S=B R_1` fixes the remaining scale.  The five ratio equalities and this
constant-term normalization give exact agreement for `R_0,...,R_5`.
Equivalently, the degree-of-freedom count is four quotient equations plus two
normalizations, yielding six matched coefficients.

## Trust boundary

The coordinate-ordered inverse, triangular equivalence, and all saddle
normalization factors are Lean-checked.  The exact elementary `C^1` proof is
fully displayed in Phase 14.  The signed fifth saddle lemma and the analytic
contraction are paper mathematics and still require independent review.

Accordingly, this branch is internally proved but not release-certified.
