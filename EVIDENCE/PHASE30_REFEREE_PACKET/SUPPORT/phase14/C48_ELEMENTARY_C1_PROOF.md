# Elementary and gamma-baseline `C^1` estimate

Date: 2026-08-15  
Status: internal paper proof; finite sign algebra Lean-checked; independent
review pending

## Theorem

Let `K` be the compact box fixed in the Phase-13 repair specification.  Put
`x=1/n`, `e=1/L_n`, and use the exact parameters

\[
A=\frac{\alpha}{xe},\quad B=\frac{t+we}{x},\quad
C=\frac{t}{x},\quad D=\frac{1+\delta e}{x}.
\]

Let `H_(n,j)` be the contribution to the `j`th normalized component from the
four Jacobi logarithms **together with** the exact gamma half-shift in the xi
quotient.  For `0<=j<=3`, uniformly for `y in K`,

\[
H_{n,j}=H_j^\infty+O_K(e+x/e),
\qquad
D_yH_{n,j}=D_yH_j^\infty+O_K(e+x),
\tag{E-C1}
\]

where

\[
(H_0^\infty,H_1^\infty,H_2^\infty,H_3^\infty)
=\left(
\frac1\alpha+\frac w{t^2}+\delta,
\frac w{t^3}+\delta,
\frac{3w}{t^4}+3\delta,
\frac{4w}{t^5}+4\delta
\right).
\]

This theorem is elementary.  It does not use a formal power series and does
not use any asymptotic property of xi.

## 1. Exact cancellation before expansion

Define

\[
f_k(U)=\log(U+k)-\log(U+k+1).
\]

The gamma baseline in the exact xi quotient satisfies

\[
\log\left(1+\frac1{n+k+1/2}\right)
=-f_k(n+1/2).
\tag{G}
\]

Since the residual is `model - xi quotient`, the elementary part of the
residual is therefore

\[
f_k(A)-f_k(B)+f_k(C)-f_k(D)+f_k(n+1/2).
\tag{R}
\]

The last two terms must be paired before taking an estimate.  Bounding them
separately creates a spurious term of size `L_n` after normalization.

Lean theorem `logRatio_forwardDiffs` checks, through the four required
orders, that `f` is exactly the negative first forward difference of
`log(U+k)`.  The same module checks all scale/sign constants below.

## 2. Exact cube-integral identity

For `q=j+1`, repeated use of the fundamental theorem of calculus gives

\[
\Delta^jf_0(U)=(-1)^{j+1}j!
\int_{[0,1]^q}(U+s_1+\cdots+s_q)^{-q}\,ds.
\tag{1}
\]

For `s>0`, `z>=0`, put

\[
\Phi_q(s,z)=\int_{[0,1]^q}
(s+z(s_1+\cdots+s_q))^{-q}\,ds.
\]

If `U=s/x`, equation (1) becomes

\[
\Delta^jf_0(s/x)=(-1)^{j+1}j!x^q\Phi_q(s,x).
\tag{2}
\]

For the remote boundary `A=alpha/(xe)`, the same identity is

\[
\Delta^jf_0(A)=(-1)^{j+1}j!(xe)^q\Phi_q(\alpha,xe).
\tag{3}
\]

## 3. Uniform kernel bounds

On the fixed compact domain, every first argument below is at least one
fixed `s_0>0`.  Differentiation under the finite cube integral gives, for
`r=0,1,2`,

\[
\partial_s^r\Phi_q(s,z)
=(-1)^r(q)_r\int_{[0,1]^q}
(s+z\textstyle\sum u_i)^{-q-r}\,du,
\tag{4}
\]

where `(q)_r=q(q+1)...(q+r-1)`.  The mean-value theorem and
`0<=sum u_i<=q` imply

\[
\left|\partial_s^r\Phi_q(s,z)
-(-1)^r(q)_rs^{-q-r}\right|
\le (q)_r(q+r)q\,z\,s_0^{-q-r-1}.
\tag{5}
\]

All constants are uniform because `q` belongs to `{1,2,3,4}`.  Equations
(4)--(5) also justify every parameter derivative used below.

## 4. Exact normalized formula

Let

\[
(a_0,a_1,a_2,a_3)=(1,1/2,1,1).
\]

These are the products of the Phase-7 component scales with
`(-1)^(j+1)j!`; `elementaryWeight_values` checks them in Lean.  Applying
(2)--(3) to (R) gives the exact identity

\[
\begin{aligned}
H_{n,j}=\frac{a_j}{e}\{&e^q\Phi_q(\alpha,xe)
-\Phi_q(t+we,x)+\Phi_q(t,x)\\
&-\Phi_q(1+\delta e,x)+\Phi_q(1+x/2,x)\}.
\end{aligned}
\tag{6}
\]

This formula displays the cancellation that the truncated series only
suggested.

## 5. Remote boundary

The `A` term in (6) is

\[
a_je^{q-1}\Phi_q(\alpha,xe).
\]

For `q=1`, (5) gives `1/alpha+O_K(xe)`, together with its alpha
derivative.  For `q>=2`, the value and alpha derivative are `O_K(e)`.
It has no `t,w,delta` derivatives.

## 6. The `B-C` pair

The fundamental theorem of calculus in the first argument gives the exact
divided difference

\[
\frac{\Phi_q(t,x)-\Phi_q(t+we,x)}e
=-w\int_0^1\partial_s\Phi_q(t+uwe,x)\,du.
\tag{7}
\]

By (5), (7) equals

\[
\frac{qw}{t^{q+1}}+O_K(e+x).
\]

For the `w` derivative, differentiate the original divided difference to get
`-partial_s Phi_q(t+we,x)`.  For the `t` derivative, apply (7) with
`partial_s Phi_q` and use the `r=2` case of (5).  The `alpha` and `delta`
derivatives vanish.  Thus the value and all parameter derivatives have a
common `O_K(e+x)` error.

## 7. The paired `D` and gamma boundaries

Split their exact divided difference as

\[
\begin{aligned}
&\frac{\Phi_q(1+x/2,x)-\Phi_q(1+\delta e,x)}e\\
&\quad=\frac{\Phi_q(1+x/2,x)-\Phi_q(1,x)}e
+\frac{\Phi_q(1,x)-\Phi_q(1+\delta e,x)}e.
\end{aligned}
\tag{8}
\]

The first term is `O(x/e)` by (4).  It has no parameter derivatives.  The
second is exactly

\[
-\delta\int_0^1\partial_s\Phi_q(1+u\delta e,x)\,du
=q\delta+O_K(e+x).
\tag{9}
\]

Its delta derivative is `-partial_s Phi_q(1+delta e,x)`, which is
`q+O_K(e+x)`; the other parameter derivatives vanish.

## 8. Assembly

Multiplying the `B-C` and paired-boundary limits by `a_j` gives

\[
a_jq=(1,1,3,4),
\]

checked by Lean theorem `boundaryWeight_values`.  Combining Sections 5--7
proves (E-C1).  Since `e<=1` eventually, the harmless `O(x)` terms are
absorbed by `O(x/e)`.

The only remaining part of the full `C^1` map is the xi saddle contribution.
That contribution has no parameter derivatives; it is a four-value estimate
using the signed derivatives `h^(2),...,h^(5)`.

## Trust boundary

Lean checks the exact finite-difference sign identities and all rational
normalization coefficients.  The cube-integral identity and uniform calculus
bounds are paper mathematics.  They are elementary and fully displayed here,
but have not been independently reviewed or formalized in Lean.

