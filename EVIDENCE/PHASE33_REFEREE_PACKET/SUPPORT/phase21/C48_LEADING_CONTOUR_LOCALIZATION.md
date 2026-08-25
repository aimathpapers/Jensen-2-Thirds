# C48 sectorial leading-mode contour and localization

Date: 2026-08-17

Status: self-contained paper proof of Phase-21 Milestone 21A; numerical
regression included; separated Kimi K3 analytic AI pre-review gate passed with
no P0/P1/P2. This is not human or peer review. This proves the leading `k=1`
Mellin-mode estimate only. It does not by itself control the higher theta modes
or assemble the full xi coefficient.

## 1. Statement

For `Re s>0`, define

\[
 I_1(s)=\int_1^\infty(\log t)^s t^{-3/4}e^{-\pi t}\,dt.
\tag{1}
\]

Let `L=L_s` be the branch from Lemma S satisfying

\[
 s=L(\pi e^L+3/4),
\tag{2}
\]

and put

\[
 K=K_s=s(1/L+1/L^2)-3/4.
\tag{3}
\]

> **Lemma 21A (sectorial leading-mode localization).**
> With `theta_1=1/100`, there is `R>0` such that, uniformly for
> `|s|>=R` and `|arg s|<=theta_1`,
> \[
> I_1(s)=\sqrt{\frac{2\pi}{K}}\,L^s
> \exp\!\left(\frac L4-\frac sL+\frac34\right)
> \left(1+O\!\left(\frac1{|K|}\right)\right).
> \tag{4}
> \]
> All powers and the square root use the branches continued from the positive
> real axis.  The relative error is holomorphic on the open sector and
> \[
> |K|\asymp\frac{|s|}{\log|s|}.
> \tag{5}
> \]
> Consequently the error in (4) is
> `O(log|s|/|s|)`, hence `O(|s|^(-3/4))` after increasing `R`.

We write `theta_1=1/100`; no optimization is intended.  Downstream Cauchy
estimates use the explicitly smaller angle `theta_0=1/200`.

## 2. Uniform saddle geometry

Lemma S gives, uniformly on `|arg s|<=theta_1`,

\[
 L=\Log s-\Log\Log s-\log\pi+o(1),\qquad
 |L|\asymp\log|s|,
\tag{6}
\]

with `Re L -> infinity`.  Write

\[
 L=\alpha+ib.
\]

The estimate in (6) alone controls `|L-(\Log s-\Log\Log s-\log\pi)|`,
not its imaginary part sharply enough at a useful threshold.  Instead, use
the saddle equation in the logarithmic form supplied by Lemma S:

\[
 L=\Log s-\Log L-\log\pi
   +\Log\!\left(1-\frac{3L}{4s}\right).
\tag{7a}
\]

Write `b=Im L`.  Lemma S gives `Re L>=m(ell)` for `ell=log|s|>=12`,
where `m(12)>7.290`, and also

\[
 \left|\operatorname{Im}\Log\!\left(1-\frac{3L}{4s}\right)\right|
 \le 2\cdot10^{-4}.
\tag{7b}
\]

Because `Re L>0`, `|arg L|<=|b|/Re L`.  Taking imaginary parts in
(7a), with `|arg s|<=1/100`, therefore gives

\[
 |b|\le\frac1{100}+\frac{|b|}{m(12)}+2\cdot10^{-4},
\]

and hence `|b|<0.012<1/20`.  After increasing `R` only to meet the explicit
Lemma-S bounds, we have

\[
 \alpha>10,\qquad |b|<1/20.
\tag{7}
\]

The exact factorization

\[
 K=\frac{s}{L}\left(1+\frac1L-\frac{3L}{4s}\right)
\tag{8}
\]

and Lemma S's bounds `1/L -> 0`, `L/s -> 0` give (5).  They also give

\[
 \arg K=\arg s-\arg L+o(1),
\]

so, after increasing `R` once more,

\[
 |\arg K|<1/20,
 \qquad \operatorname{Re}K\ge c_0|K|,
 \qquad c_0:=\cos(1/20)>0.
\tag{9}
\]

Thus `K` is nonzero, stays in the open right half-plane, and has a unique
square-root branch continued from positive `s`.  Its exact nonvanishing also
follows independently from `Q_s=L_s^2K_s\ne0` in Lemma S; the right-half-plane
bound itself is the argument estimate above.

## 3. An exact legal contour

Set `u=log t`.  Equation (1) becomes

\[
 I_1(s)=\int_0^\infty g_s(u)\,du,
 \qquad
 g_s(u):=\exp\{h_s(u)\},
\tag{10}
\]

where

\[
 h_s(u)=s\Log u+u/4-\pi e^u.
\tag{11}
\]

Here `Log u` is principal.  The function `g_s` is holomorphic on the slit
plane `\mathbb C\setminus(-\infty,0]`; in particular it is holomorphic
throughout the open right half-plane.  This removes the apparent `Log Log t`
branch problem:
the deformation below never approaches the slit.

Apply Cauchy's theorem to the rectangle with vertices

\[
 1,\quad X,\quad X+ib,\quad1+ib.
\]

On its right side, for `|y|<=|b|<1/20`,

\[
 |e^{-\pi e^{X+iy}}|
 =e^{-\pi e^X\cos y}
 \le e^{-\pi e^X\cos(1/20)},
\]

which dominates all remaining factors as `X -> infinity`.  Letting `X` tend
to infinity gives the exact identity

\[
 I_1(s)=E_s+
 \int_1^\infty g_s(x+ib)\,dx,
\tag{12}
\]

where the endpoint connector is

\[
 E_s=\int_0^1g_s(x)\,dx+i\int_0^b g_s(1+iy)\,dy.
\tag{13}
\]

The horizontal contour passes through `L=alpha+ib` and lies entirely in
`Re u>=1`, a single fixed logarithm domain.  Although `b=Im L_s` is not a
holomorphic function of `s`, holomorphic dependence of a chosen contour is
not required: (12) is a pointwise Cauchy identity used only for uniform
estimates.  Holomorphy of the final relative error follows directly from the
original integral and the explicit nonzero main term.

## 4. The endpoint connector is negligible

On `[0,1]`,

\[
 |g_s(x)|\le e^{1/4}x^{\operatorname{Re}s},
\]

so the first integral in (13) is `O(1/Re s)`.  On the vertical connector,
`|1+iy|` and `arg(1+iy)` are bounded uniformly, and therefore

\[
 \left|i\int_0^b g_s(1+iy)\,dy\right|\le e^{C|s|}
\tag{14}
\]

for one absolute `C`.

Define the proposed first-mode main term

\[
 \mathcal A(s):=e^{h_s(L)}\sqrt{2\pi/K}.
\tag{15}
\]

From (2),

\[
 e^{h_s(L)}
 =L^s\exp\!\left(\frac L4-\frac sL+\frac34\right).
\tag{16}
\]

Using (6), the logarithm of its modulus satisfies

\[
 \log|e^{h_s(L)}|
 =\operatorname{Re}(s\Log L)-\operatorname{Re}(s/L)+O(|L|)
 \ge |s|\cos\theta\,\log\log|s|-C|s|
      -C\frac{|s|}{\log|s|}-C\log|s|
 \ge c|s|\log\log|s|
\tag{17}
\]

for some fixed `c>0` and all sufficiently large `R`.  Here
`s/L=O(|s|/log|s|)` is retained at its true scale; the leading
`Re(s Log L)` term dominates it on the fixed sector.  The square-root factor
changes (17) by only `O(log|s|)`.  Equations (14)--(17) therefore give

\[
 E_s=\mathcal A(s)\,O\!\left(e^{-c_1|s|\log\log|s|}\right)
\tag{18}
\]

for a possibly smaller `c_1>0`.  This is much smaller than the error claimed
in (4).

## 5. Strict horizontal concavity

For real `x>=1`, put

\[
 f_s(x):=\operatorname{Re}h_s(x+ib).
\]

Direct differentiation gives

\[
 f_s''(x)=-\operatorname{Re}\left(\frac{s}{(x+ib)^2}
                                      +\pi e^{x+ib}\right).
\tag{19}
\]

By (7), `|arg(x+ib)|<=1/20`.  Thus

\[
 |\arg(s/(x+ib)^2)|\le 1/100+1/10<\pi/2,
\]

and `cos b>0`.  Both real parts inside (19) are positive, whence

\[
 f_s''(x)<0\qquad(x>=1).
\tag{20}
\]

The modulus of the integrand on the shifted ray is therefore strictly
log-concave.

The published saddle is not quite the stationary point of the full
`u`-integrand, because the Jacobian `dt=e^u du` is amplitude in the published
normalization.  This is visible in the exact identities

\[
 h_s'(L)=1,
 \qquad h_s''(L)=-K.
\tag{21}
\]

Thus `f_s'(alpha)=1`, and the true maximum on the horizontal ray lies only
`O(1/|K|)` to the right of `alpha`.  Keeping the linear term is what makes the
calculation below consistent with the published saddle rather than silently
changing it.

## 6. Central Gaussian calculation

Let

\[
 \rho:=|K|^{-2/5}.
\tag{22}
\]

For real `|r|<=rho`, Taylor's theorem on the horizontal segment through `L`
and (21) give

\[
 h_s(L+r)-h_s(L)
 =r-\frac12Kr^2+c_3r^3+R_4(r),
\tag{23}
\]

where

\[
 c_3=\frac{h_s'''(L)}6=O(|K|),
 \qquad |R_4(r)|\le C|K||r|^4.
\tag{24}
\]

Indeed, for every fixed `j>=3`,

\[
 h_s^{(j)}(u)=(-1)^{j-1}(j-1)!\frac{s}{u^j}-\pi e^u,
\tag{25}
\]

and on `|u-L|<=1/10` both terms are `O_j(|s|/|L|)=O_j(|K|)`.

Since `|K|rho^3=|K|^{-1/5}`, expansion of the last exponential in (23) is
uniformly legitimate and yields

\[
 e^{c_3r^3+R_4(r)}
 =1+c_3r^3+O\!\left(|K|r^4+|K|^2r^6\right).
\tag{26}
\]

For `Re K>0`, completing the square gives

\[
 \int_{-\infty}^{\infty}e^{r-Kr^2/2}\,dr
 =\sqrt{\frac{2\pi}{K}}e^{1/(2K)},
\tag{27}
\]

on the branch fixed in Section 2.  Differentiating this Gaussian identity
with respect to its linear parameter gives

\[
 \frac{\int_{-\infty}^{\infty}r^3e^{r-Kr^2/2}\,dr}
      {\int_{-\infty}^{\infty}e^{r-Kr^2/2}\,dr}
 =\frac3{K^2}+\frac1{K^3}.
\tag{28}
\]

Consequently the signed cubic term in (26) contributes `O(1/|K|)`, not the
larger absolute-value estimate `O(|K|^(-1/2))`.  The two remainder terms have
the same relative order because the absolute Gaussian moments satisfy

\[
 |K|\int |r|^4e^{r-\operatorname{Re}K r^2/2}\,dr
 =O(|K|^{-3/2}),
\]

\[
 |K|^2\int |r|^6e^{r-\operatorname{Re}K r^2/2}\,dr
 =O(|K|^{-3/2}),
\]

whereas the modulus of (27) is comparable with `|K|^(-1/2)`.  Truncating
these integrals at `|r|=rho` changes them by
`O(exp(-c|K|^(1/5)))`.  Hence

\[
 \int_{-\rho}^{\rho}g_s(L+r)\,dr
 =e^{h_s(L)}\sqrt{\frac{2\pi}{K}}
  \left(1+O(1/|K|)\right).
\tag{29}
\]

Here `e^(1/(2K))=1+O(1/|K|)` has been absorbed into the error.

## 7. Horizontal tails

Taking real parts in (23), using (9), and differentiating the same expansion
once show, for sufficiently large `R`,

\[
 f_s(\alpha\pm\rho)-f_s(\alpha)
 \le-c_2|K|^{1/5},
\tag{30}
\]

\[
 f_s'(\alpha-\rho)>0,
 \qquad
 f_s'(\alpha+\rho)<-c_3|K|^{3/5}
\tag{31}
\]

with fixed positive constants.  Since `f_s'` is strictly decreasing by
(20), `f_s` is increasing on `[1,alpha-rho]`, while for
`x>=alpha+rho`,

\[
 f_s(x)\le f_s(\alpha+\rho)
           -c_3|K|^{3/5}(x-\alpha-\rho).
\]

It follows that

\[
 \int_1^{\alpha-\rho}|g_s(x+ib)|\,dx
 \le\alpha e^{f_s(\alpha)-c_2|K|^{1/5}},
\tag{32}
\]

and

\[
 \int_{\alpha+\rho}^{\infty}|g_s(x+ib)|\,dx
 \le\frac{e^{f_s(\alpha)-c_2|K|^{1/5}}}
          {c_3|K|^{3/5}}.
\tag{33}
\]

Relative to
`|\mathcal A(s)|\asymp e^{f_s(\alpha)}|K|^{-1/2}`, both bounds are
`O(exp(-c_4|K|^(1/5)))`.  Equations (12), (18), (29), and (32)--(33)
prove (4).

## 8. Holomorphic relative error

The original integral (1) is holomorphic for `Re s>-1` by locally uniform
domination.  Lemma S makes `L_s`, `K_s`, and the declared powers holomorphic
on the open sector, and Sections 2 and 4 show that the main term is nonzero.
Therefore

\[
 \mathcal E_1(s):=I_1(s)/\mathcal A(s)-1
\]

is holomorphic there.  The pointwise contour identity established the uniform
bound; it did not define the error function.

## 9. Scope and next gate

Lemma 21A closes the first genuinely unsupported step identified by the
primary-source audit: a legal complex contour and uniform localization for the
leading theta mode.  It does not yet prove `C48-GORTTW-SECTOR`.  The remaining
steps are:

1. bound `\sum_{k\ge2} I_k(s)` relative to `I_1(s)` on the same sector;
2. compare `F(N+2)` with `N^2F(N)` uniformly;
3. assemble the exact factor-eight-corrected xi coefficient with sectorial
   Stirling;
4. rerun the downstream fifth/sixth logarithmic-derivative proof and fresh
   end-to-end review.

The companion script `leading_contour_check.py` is a high-precision regression
of (12) and (4).  It is not part of the proof.
