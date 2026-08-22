# C48 sectorial suppression of the higher theta modes

Date: 2026-08-17

Status: self-contained paper proof; separated Kimi K3 analytic AI pre-review
gate passed with no P0/P1/P2. This is not human or peer review. This note
combines with `C48_LEADING_CONTOUR_LOCALIZATION.md` to give the complete
sectorial asymptotic for the auxiliary Mellin moment `F(s)`. It does not by
itself assemble the xi coefficient.

## 1. Statement

For `Re s>0`, let

\[
 F(s)=\sum_{k\ge1}I_k(s),\qquad
 I_k(s)=\int_1^\infty(\log t)^s t^{-3/4}e^{-\pi k^2t}\,dt.
\tag{1}
\]

On the same fixed sector as Lemma 21A,

\[
 \sum_{k\ge2}I_k(s)
 =\mathcal A(s)O\!\left(e^{-c|K_s|^{1/5}}\right),
\tag{2}
\]

where

\[
 \mathcal A(s)=\sqrt{\frac{2\pi}{K_s}}L_s^s
 \exp\!\left(\frac{L_s}{4}-\frac{s}{L_s}+\frac34\right).
\tag{3}
\]

Consequently

\[
 F(s)=\mathcal A(s)
 \left(1+O(1/|K_s|)\right)
\tag{4}
\]

uniformly on the sector, with a holomorphic relative error.  Since
`|K_s|` is comparable with `|s|/log|s|`, (4) has relative error
`O(log|s|/|s|)`.

## 2. Deform the full theta kernel at once

After `u=log t`, write

\[
 G_s(u)=u^s e^{u/4}\sum_{k\ge1}e^{-\pi k^2e^u}.
\tag{5}
\]

On the closed strip

\[
 \operatorname{Re}u\ge1,\qquad
 |\operatorname{Im}u|\le1/20,
\]

one has `Re(e^u)>=e^(Re u)cos(1/20)>0`.  The theta series in (5) and all of
its `u`-derivatives therefore converge locally uniformly.  Thus `G_s` is
holomorphic on the strip and the same rectangle used for Lemma 21A gives

\[
 F(s)=E_s^{\vartheta}+
 \int_1^\infty G_s(x+ib)\,dx,
\tag{6}
\]

where `b=Im L_s` and `E_s^vartheta` consists of `[0,1]` and the vertical
connector at `Re u=1`.

The theta sum is uniformly bounded on those two fixed endpoint pieces.  The
argument of Section 4 of the leading-mode proof therefore gives

\[
 E_s^{\vartheta}=\mathcal A(s)
 O\!\left(e^{-c_0|s|\log\log|s|}\right).
\tag{7}
\]

## 3. A pointwise higher-mode factor

Let

\[
 g_{1,s}(u)=u^se^{u/4-\pi e^u}.
\]

For `u=x+ib` on the shifted ray,

\[
 \sum_{k\ge2}|e^{-\pi k^2e^u}|
 =e^{-\pi e^x\cos b}
  \sum_{k\ge2}e^{-\pi(k^2-1)e^x\cos b}.
\]

Put `q=pi e^x cos b`.  Since
`k^2-1>=3(k-1)` for `k>=2`,

\[
 \sum_{k\ge2}e^{-(k^2-1)q}
 \le\frac{e^{-3q}}{1-e^{-3q}}.
\tag{8}
\]

For `x>=1` and `|b|<1/20`, the denominator is bounded below by an absolute
positive constant.  Hence

\[
 \left|G_s(x+ib)-g_{1,s}(x+ib)\right|
 \le C|g_{1,s}(x+ib)|e^{-3\pi e^x\cos b}.
\tag{9}
\]

## 4. Left of the Gaussian window

Use the notation of Lemma 21A:

\[
 L_s=\alpha+ib,\qquad
 \rho=|K_s|^{-2/5},\qquad
 f_s(x)=\log|g_{1,s}(x+ib)|.
\]

On `1<=x<=alpha-rho`, the exponential factor in (9) is at most a fixed
constant, while strict concavity and the boundary gap from Lemma 21A give

\[
 \int_1^{\alpha-\rho}|g_{1,s}(x+ib)|\,dx
 \le\alpha e^{f_s(\alpha)-c_1|K_s|^{1/5}}.
\tag{10}
\]

Since `|\mathcal A(s)|` is comparable with
`e^{f_s(\alpha)}|K_s|^{-1/2}`, the higher-mode contribution on this interval
is

\[
 \mathcal A(s)O\!\left(e^{-c_2|K_s|^{1/5}}\right).
\tag{11}
\]

Polynomial factors such as `alpha|K_s|^(1/2)` have been absorbed by reducing
`c_2`.

## 5. The central and right regions

For `x>=alpha-rho`, equation (9) gives the uniform factor

\[
 \exp\{-3\pi e^{\alpha-\rho}\cos b\}.
\tag{12}
\]

The saddle equation and the sectorial geometry imply

\[
 \pi e^\alpha\asymp |s|/|L_s|\asymp|K_s|,
\qquad e^{-\rho}=1+o(1),
\tag{13}
\]

so (12) is `O(e^(-c_3|K_s|))`.  The absolute central Gaussian estimate and
the right-tail estimate from Lemma 21A give

\[
 \int_{\alpha-\rho}^{\infty}
 |g_{1,s}(x+ib)|\,dx
 \le C e^{f_s(\alpha)}|K_s|^{-1/2}.
\tag{14}
\]

Combining (9), (12), and (14), the higher modes on the central and right
regions contribute

\[
 \mathcal A(s)O(e^{-c_4|K_s|}).
\tag{15}
\]

Equations (7), (11), and (15) prove (2).

## 6. Holomorphy and scope

The locally uniform theta series and the original positive-ray integral show
that `F(s)` is holomorphic for `Re s>-1`.  The main term is nonzero on the
chosen sector.  Thus

\[
 F(s)/\mathcal A(s)-1
\]

is holomorphic, while the shifted contour supplies its uniform bound.

This closes the higher-theta part of P21.4 at internal paper-proof level.
The remaining analytic steps for `C48-GORTTW-SECTOR` are the
`F(N+2)/(N^2F(N))` comparison and sectorial Stirling/xi-coefficient assembly,
followed by fresh review.
