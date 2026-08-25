# Uniform non-perturbative critical-point radius

Date: 2026-08-15  
Status: internal paper proof; recurrence algebra and maximum step Lean-checked;
two adversarial AI pre-reviews completed; not peer reviewed

## 1. Statement

On the exact Phase-15 parameter branch, assume

\[
n^2\log(n+2)\ge K_\mathrm w d^3
\]

with `K_w` sufficiently large.  Let `p_F` be the positive-rooted
two-Jacobi comparison polynomial.  There is an absolute `K_r` such that at
every critical point `y` of `p_F`,

\[
\left|\frac{y^kp_F^{(k)}(y)}{p_F(y)}\right|
\le (K_r\sqrt{Bd})^k,
\qquad 0\le k\le d.
\tag{R}
\]

The proof does not assume `(C-D)/C=o(1)`; on this branch that ratio tends to
`1/2`.  Phase 18 makes the favorable margin quantitative: eventually
`C-D>=n/2`, and under the wedge `C-D-d>=n/4`.

## 2. Coarse uniform parameter box

The Phase-15 branch gives

\[
A\sim3n\mathcal L_n,\quad B,C\sim2n,\quad D\sim n.
\]

The wedge implies `d/n -> 0` uniformly as `n -> infinity`.  Before deriving
the localization constant, fix the provisional, non-circular value

\[
 K_{\rm pre}=256.
\]

After one fixed threshold, we may therefore use the coarse inequalities

\[
n\le B\le3n,\quad \frac n2\le D\le2n,
\quad n\le C\le3n,
\]

\[
A\ge8B,\quad A\ge2d,\quad C\ge D+d,\quad
B,D\ge K_{\rm pre}d.
\tag{P}
\]

All constants below are independent of `n,d,m`.

## 3. Root and critical-point localization

We use the following standalone ratio-free lemma, extracted from the
Gershgorin calculation in the proof of Holland's finite-free root lemma.

**Ratio-free Jacobi lemma.**  Put

\[
q_{U,V}(y)={}_2F_1\!\left(-d,U;V;\frac yU\right).
\]

If `U>=V+d` and `V>=32d`, then

\[
\operatorname{roots}(q_{U,V})
\subset[V-8\sqrt{Vd},V+8\sqrt{Vd}].
\tag{J}
\]

Here is the source calculation, separated from Holland's stronger assembled
lemma and hence from its inapplicable upper bound on `(C-D)/D`.  Write
`alpha=V-1`, `beta=U-V-d`, and `H=U-d-1`.  After transporting the standard
Jacobi matrix by `y=U(1-t)/2`, its `k`th diagonal entry is

\[
U\frac{H(V+2k)+2k(k+1)}{(H+2k)(H+2k+2)},
\]

and its off-diagonal entry between rows `k-1` and `k` is

\[
\frac{U}{2k+H}
\left\{
\frac{k(k+V-1)(k+\beta)(k+H)}
{(2k+H-1)(2k+H+1)}
\right\}^{1/2}.
\]

Since `H>=V-1>=31d`, subtracting `V` from the diagonal gives

\[
\frac{2k(k+H+1)(U-2V)+VH(d-1)}
{(H+2k)(H+2k+2)}.
\]

Here `alpha=V-1>-1` and `beta=U-V-d>=0`, so the Jacobi matrix is real and its
off-diagonal radicands are nonnegative.  The absolute value of the displayed
**quotient** is below `4d`, hence below `4\sqrt{Vd}`; the latter step uses
`d<=V`.  The bound `H>=V-1` uses `U>=V+d`.  Also `0<=beta<=H`,
`U/(2k+H)<=33/31`, and
`k+V-1<=(33/32)V`, so every off-diagonal entry is at most
`2\sqrt{Vd}` and the two adjacent entries have sum at most `4\sqrt{Vd}`.
Gershgorin gives `(J)`.  No upper bound on `U/V` or `U-V` enters.

Apply `(J)` first to `(U,V)=(A,B)`.  It gives

\[
\operatorname{roots}(q_{A,B})
\subset[B-C_J\sqrt{Bd},B+C_J\sqrt{Bd}]
\]

from `(P)`, with `C_J=8`.  Applying it again to `(U,V)=(C,D)` gives roots in

\[
[D-C_J\sqrt{Dd},D+C_J\sqrt{Dd}].
\]

Coefficientwise, in the ascending normalization with constant term one,

\[
p_F=q_{A,B}\boxtimes_d\bigl(q_{C,D}(D\,\cdot)\bigr).
\tag{F}
\]

The finite-free theorems are stated in the monic descending normalization.
Thus `(F)` is applied after reversing all three polynomials.  Reversal maps
positive roots to their reciprocals, sends `[m,M]` to `[1/M,1/m]`, and
preserves logarithmic mesh.  Equivalently, the normalized elementary
symmetric functions of the reciprocal roots multiply in the displayed
ascending normalization.  The direct ascending identity is valid as well,
because multiplicative finite-free convolution commutes with reversal; the
reversal is used solely to match the cited theorem's monic descending
normalization.  It changes no positivity, interval, or simplicity conclusion.

The second factor in `(F)` has roots in

\[
[1-C_J\sqrt{d/D},1+C_J\sqrt{d/D}].
\]

Both factor intervals are admissible positive intervals for the following
direct consequence of Marcus--Spielman--Srivastava, Theorem 1.6.  If the
roots of `p` lie in `[u_-,u_+] subset (0,infinity)` and those of `q` lie in
`[v_-,v_+] subset (0,infinity)`, then every root of `p boxtimes_d q` lies in
`[u_-v_-,u_+v_+]`.  Indeed, for
`p^vee(x)=x^d p(1/x)/p(0)`, coefficient comparison gives
`(p boxtimes_d q)^vee=p^vee times_d q^vee`.  Theorem 1.6 bounds the largest
root of a positive-rooted multiplicative convolution by the product of the
two largest roots.  It gives the lower endpoint after reciprocation and the
upper endpoint in the original orientation.  (Holland Lemma 7.1 cites MSS
Theorem 1.13 here; the displayed largest-root inequality is Theorem 1.6 in
the published paper.)

Thus `B,D>=256d` gives lower endpoints at least `B/2` and `1/2`.  If `u` and
`v` denote their deviations from `B` and `1`, respectively, then

\[
 |(B+u)(1+v)-B|
 \le 8\sqrt{Bd}+8B\sqrt{d/D}+64\sqrt{Bd}\sqrt{d/D}.
\]

The coarse box gives `B/D<=6` and `d/D<=1/256`, so the right side is at most
`(12+8sqrt(6))sqrt(Bd)`.  Fix the derived constant explicitly,

\[
 C_{\rm loc}=12+8\sqrt6,
\]

and note that `sqrt(6)<5/2` gives `C_loc<32`.  The preceding MSS interval
consequence then yields, for every root of `p_F`,

\[
|y-B|\le C_\mathrm{loc}\sqrt{Bd}.
\tag{L}
\]

This derivation does not invoke Holland's assembled lemma,
whose extra hypothesis `(C-D)/D<=1/4` fails on the present branch.  Critical
points satisfy the same bound by interlacing.  Now fix

\[
 K_0=\max\{256,256C_{\rm loc}^2\}
\]

and enlarge the eventual branch threshold until `B,D>=K_0d`.  This later
strengthening does not enter the derivation of `C_loc`.  It gives

\[
\frac B2\le y\le2B,\qquad \frac yA\le\frac14.
\tag{Y}
\]

Both Jacobi factors have simple positive roots by the classical Jacobi
parameter conditions `V>0` and `U-V-d>-1`.  Multiplicative finite-free
positivity is Martínez-Finkelshtein--Morales--Perales, Proposition 2.7(iii).
Pin the convention from their Definition 2.16: if
`lambda_1>=...>=lambda_d>0`, then

\[
\operatorname{lmesh}(p)
=\min_{1\le j<d}\frac{\lambda_j}{\lambda_{j+1}}\ge1.
\]

Their Proposition 2.17 gives
`\operatorname{lmesh}(p\boxtimes_dq)\ge\operatorname{lmesh}(p)` in exactly
this convention.  Since the first factor has distinct positive roots, its
logarithmic mesh is strictly greater than one; scaling the second factor does
not change this.  Hence `p_F` has `d` distinct positive roots.  Also
`p_F(0)=1`, so `p_F(y)` is nonzero at every critical point.  Exact wording is
pinned to arXiv:2309.10970v3; the paywalled journal PDF was not byte-compared.

## 4. Exact direct recurrence

Set

\[
\lambda=\frac D{AC},\qquad
p_F(y)={}_3F_2(-d,A,C;B,D;\lambda y).
\]

For `0<=m<=d`, `p_F^(m)` is a nonzero constant multiple of

\[
g_m(y)={}_3F_2(-(d-m),A+m,C+m;B+m,D+m;\lambda y).
\]

Put `a_1=m-d`, `a_2=A+m`, `a_3=C+m`, `b_1=B+m`, `b_2=D+m`, and let
`e_1,e_2,e_3` be the elementary symmetric functions of the three `a_i`.
The generalized hypergeometric differential equation is

\[
\theta(\theta+b_1-1)(\theta+b_2-1)g_m
=\lambda y(\theta+a_1)(\theta+a_2)(\theta+a_3)g_m,
\qquad \theta=y\frac d{dy}.
\tag{H}
\]

Using
`theta^2 g=y^2g''+yg'` and
`theta^3 g=y^3g'''+3y^2g''+yg'`, equation `(H)` becomes

\[
\begin{aligned}
 &(1-\lambda y)y^3g_m'''\\
 &+[b_1+b_2+1-\lambda y(3+e_1)]y^2g_m''\\
 &+[b_1b_2-\lambda y(1+e_1+e_2)]yg_m'\\
 &-\lambda y e_3g_m=0.
\end{aligned}
\tag{H3}
\]

For every `y` with `p_F(y)!=0`, multiply `(H3)` by `y^m/p_F(y)`.
With

\[
T_k=\frac{y^kp_F^{(k)}(y)}{p_F(y)},
\]

this proves, for every `0<=m<=d`,

\[
P_{3,m}T_{m+3}+P_{2,m}T_{m+2}
+P_{1,m}T_{m+1}+P_{0,m}T_m=0.
\tag{D}
\]

The four ODE coefficients in `(H3)` are exactly the decomposed coefficients
used below.  At a critical point, `T_0=1` and `T_1=0`; the maximum argument
uses `(D)` only for `0<=m<=d-2`.  Thus the recurrence is a polynomial identity,
not a critical-point identity.

The pinned exact producer `direct_recurrence.py` checks the ODE-to-decomposed
coefficient identities symbolically and checks the shifted ODE for 31 pairs
`(polynomial,m)` across four independent parameter tuples.  Lean checks the
subsequent elimination and all four closed coefficient forms, but does not
formalize the hypergeometric differential equation.  We use, especially,

\[
P_{0,m}=\frac{Dy(A+m)(C+m)(d-m)}{AC},
\qquad P_{3,m}=\frac{AC-Dy}{AC}.
\tag{C}
\]

## 5. Uniform central lower bound

Write

\[
a=1-y/A,\qquad
b_m=B+m-y+(d-1-2m)y/A,\qquad
\varepsilon_p=(C-D)/C.
\]

The exact central coefficient is

\[
P_{2,m}=b_{m+1}+(D+m)a
+\varepsilon_p\frac yA(A-d+3+3m).
\]

Every factor in the last term is nonnegative under `(P)` and `(Y)`.  The
fixed margin `C-D-d>=n/4` shows that this sign is stable rather than a
near-boundary artifact.  Also

\[
|b_{m+1}|
\le C_\mathrm{loc}\sqrt{Bd}+2d+1.
\]

The fixed choice of `K_0` already makes this uniform.  Indeed,
`d<=B/K_0`, `B<=3n`, and `K_0>=256C_loc^2` give

\[
C_\mathrm{loc}\sqrt{Bd}\le\frac{3n}{16}.
\]

Since `C_loc>=1`, also `K_0>=256`; after the harmless fixed condition
`n>=128`, one has `2d+1<=n/16`.  Thus `|b_{m+1}|<=n/4`, while
`(D+m)a >= (n/2)(3/4)=3n/8`.  Therefore

\[
P_{2,m}\ge n/8.
\tag{Center}
\]

Thus the non-small epsilon term has the favorable sign, but the proof does
not even need its full asymptotic size.

## 6. Neighbor bounds

Equations `(P)`, `(Y)`, `(L)`, and the definitions give

\[
|P_{3,m}|\le2.
\tag{N3}
\]

For

\[
c_m=(d-m)(1+m/A)y
\]

we have `|c_(m+1)|<=Cnd`.  The exact decomposed coefficient is

\[
P_{1,m}=c_{m+1}+(D+m)b_m
+\varepsilon_p\frac yA\beta_m.
\tag{P1-dec}
\]

This form is mandatory: in the expanded ODE coefficient
`b_1b_2-\lambda y(1+e_1+e_2)`, the two displayed terms are individually of
order `n^2`.  Their leading parts cancel through `B-y`, and `(P1-dec)` exposes
that cancellation before estimation.  Bounding the expanded terms separately
would destroy the radius argument.  Moreover

\[
|b_m|\le C(\sqrt{Bd}+d),
\]

and the explicit polynomial

\[
\beta_m=A(2m+1-d)-d(2m+1)+3m^2+3m+1
\]

satisfies `|beta_m|<=CAd` because `m<=d` and `A>=2d`.  Hence the exact
formula for `P_1` yields

\[
|P_{1,m}|\le C_1(n\sqrt{Bd}+nd).
\tag{N1}
\]

Finally, the closed form `(C)` and the coarse ratios
`(A+m)/A<=2`, `(C+m)/C<=2` give

\[
0\le P_{0,m}\le C_0n^2d
\tag{N0}
\]

with, for example, `C_0=48` under the displayed coarse box.

A direct termwise use of `B<=3n`, `D<=2n`, `y<=2B`, `A>=8B`,
`d<=B/K_0`, and `(L)` permits the explicit choice

\[
 C_1=\max\{3C_{\rm loc},66\}
\]

in `(N1)`; no hidden parameter-dependent constant is used later.

## 7. Choice of radius

Put

\[
\rho=K_r\sqrt{Bd}.
\]

Divide `(D)` by `P_(2,m) rho^(m+2)` and use `(Center)` and
`(N3)`--`(N0)`.  The three normalized neighbor coefficients are bounded by

\[
16K_r\sqrt{3d/n},
\tag{Q3}
\]

\[
\frac{8C_1}{K_r}
\left(1+\sqrt{d/B}\right),
\tag{Q1}
\]

and

\[
\frac{8C_0}{K_r^2}\frac nB
\le\frac{8C_0}{K_r^2}.
\tag{Q0}
\]

First choose the fixed `K_r` so that the constant parts of `(Q1)` and
`(Q0)` have sum below `1/4`.  Then increase the `n` threshold so that `(Q3)`
and the `sqrt(d/B)` part of `(Q1)` have sum below `1/4`.  This order of
choices is legitimate because `d/n -> 0` uniformly in the wedge.  Therefore
the total neighbor coefficient is at most

\[
q=1/2<1.
\tag{Q}
\]

## 8. Maximum argument

Let

\[
u_k=|T_k|/\rho^k,\qquad
\mathcal M=\max_{0\le k\le d}u_k.
\]

If a maximizing index is at least two, equation `(D)` and `(Q)` give
`u_k<=q M`.  The boundary case `k=d` is identical because
`T_(d+1)=0`.  The base values are `u_0=1` and `u_1=0`.  Therefore
`M<=1`.

Lean theorem `dominantMaximum_le_one` checks this finite contradiction in an
abstract form once the analytic coefficient sum `q<1` has been supplied.
It follows that `|T_k|<=rho^k` for all `k`, proving `(R)`.

## 9. Order of constants and thresholds

For clarity, the choices are not circular.  First derive the absolute
single-factor constant `C_J=8`.  Next derive an absolute `C_loc` using only
`d<=B` and the coarse `B/D` bound.  Then fix
`K_0=max(256,256C_loc^2)`.  After that choose `K_r` from `(Q1)` and `(Q0)`,
and finally enlarge the one eventual `n` threshold so that the Phase-15 branch
lies in the displayed parameter box and `n>=128`.  The already fixed radius
satisfies `rho/d=K_r sqrt(B/d) -> infinity` under the wedge, so `rho>=d`
follows by increasing only this eventual threshold; similarly `rho=o(n)`.
Finally make the
vanishing terms in `(Q3)` and `(Q1)` total less than `1/4`.  These conditions
are mutually compatible under the proposed wedge.

## Trust boundary

Lean checks the terminating finite `_3F_2` producer, its coefficientwise Euler
ODE, derivative shift, genuine four-term recurrence, the four closed forms,
and the global-maximum contradiction.  The classical Jacobi root/matrix
correspondence, its uniform entry estimates, and the published MSS/MMP inputs
remain external paper mathematics behind explicitly typed adapters.  The
parameter/root inequalities and coarse analytic coefficient estimates are
also paper mathematics.  They are stated with a fixed order of constants
rather than only asymptotic arrows.  Available review is AI review, not human
or peer review.
