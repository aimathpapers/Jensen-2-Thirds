# Uniform complex sixth saddle and residual closure

Date: 2026-08-15  
Status: repaired paper proof; its former sectorial GORTTW condition now has an
internal Phase-21 proof, with fresh end-to-end review pending; not peer reviewed

**Phase-21 update.**  `../phase21/C48_XI_COEFFICIENT_ASSEMBLY.md` and
`../phase21/C48_DOWNSTREAM_DISCHARGE.md` replace the formerly external premise
by a direct xi/Mellin proof and proportional-disk Cauchy transport.

## 1. Inherited sectorial input

Let

\[
M_z=\int_0^\infty\Phi(u)u^{2z}\,du,
\qquad h(z)=\log M_z,
\qquad N=2z-2.
\]

Historically, Holland's Proposition 4.1 in arXiv:2608.08682v1 supplies a
nonzero sector.  The direct Phase-21 replacement is now used with the fixed
angles

\[
 \theta_{\rm out}=1/200,\qquad
 \theta_{\rm bd}=1/400,\qquad
 \theta_{\rm ctr}=1/800.
\]

After one fixed radial threshold, `M_z` is nonzero on the outer sector

\[
\mathfrak S_{\theta_{\rm out}}
=\{z:|z|\ge x_0,\ |\arg z|<\theta_{\rm out}\}.
\]

It also supplies the branch of `h` that is real on the positive axis and the
decomposition

\[
h(z)=G_0(N)+\log\!\left(32\binom{2z}{2}\right)
-(2z+2)\log2+c_{\rm sad}+\mathcal R(z),
\tag{1}
\]

where

\[
G_0(N)=(N+1)\log L_N+\frac{L_N}{4}-\frac{N}{L_N}
-\frac12\log Q_N,
\qquad
Q_N=(1+L_N)N-\frac34L_N^2,
\tag{2}
\]

and `L_N` is the continued saddle satisfying

\[
N=L_N\left(\pi e^{L_N}+\frac34\right).
\tag{3}
\]

On every smaller closed sector,

\[
|L_N|\asymp\log|N|,\qquad
\frac1{L_N}\longrightarrow0,\qquad
\frac{L_N}{N}\longrightarrow0,
\tag{4}
\]

and in fact `|r|\le1/4`, `|\sigma|\le1/4` for `|N|\ge e^{12}`, where
`r=1/L_N` and `\sigma=L_N/N`.

Earlier drafts called (4) an inherited fact of the complex saddle.  That was
wrong: Holland defines the complex `L_N` only by deferral ("the branch of the
holomorphic continuation used in [3, Section 3]") and states no sectorial
asymptotics for it.  **(4) is now proved outright in
`C48_SECTORIAL_SADDLE_VARIABLE.md`, Lemma S**, by Rouché applied to the
logarithmic form of (3), with no input from Holland or from [3].  Lemma S also
supplies existence, uniqueness, and holomorphy of the branch on the sector,
its agreement with the positive real solution, the sharp form
`L_N=\log N-\log\log N-\log\pi+O(\log\ell/\ell)` with `\ell=\log|N|`, and
`|L_N|\ge\tfrac12\log|N|`.  Because a holomorphic continuation of the positive
real solution into the (simply connected) sector is unique, the branch of
Lemma S *is* the branch of [3, Section 3]; that citation is therefore an
identification remark here, not an analytic input.

Phase 20 no longer imports Proposition 4.1 as a black box.  Phase 21 now also
removes the terse GORTTW complex-extension sentence as an input: Theorem 21B
proves the nonvanishing sector and decomposition (1) from the xi/Mellin
integral, with relative error `O(log|z|/|z|)`.

## 2. A Cauchy corollary at derivative order six

The printed statement of Holland's Proposition 4.1 records remainder
derivatives only for orders `0,...,5`.  The Phase-20 reconstruction of its
proof first establishes that
`mathcal R` is holomorphic and that, for every fixed
`0<epsilon0<1/2`,

\[
\mathcal R(z)=O(|z|^{-1+\varepsilon_0})
\tag{5}
\]

on a fixed closed sector.

Use the explicit nested closed sectors

\[
\mathfrak S_{\theta_{\rm ctr}}\Subset
\mathfrak S_{\theta_{\rm bd}}\Subset
\mathfrak S_{\theta_{\rm out}}.
\]

Take the explicit proportional radius `delta_C=1/1000`.  For every
sufficiently large `z in S_{theta_ctr}`, the disk

\[
|\zeta-z|\le\delta_{\rm C}|z|
\]

lies in `S_{theta_bd}` and satisfies
`(1-delta_C)|z|<=|zeta|<=(1+delta_C)|z|`.  Indeed, its angular displacement is
at most `arcsin(delta_C/(1-delta_C))<1/1000+10^-5`, which is smaller than
`theta_bd-theta_ctr=1/800`.  Applying Cauchy's
inequality to (5) on this disk gives the new, explicit corollary

\[
|\mathcal R^{(6)}(z)|
\le 6!\,\delta_{\rm C}^{-6}|z|^{-6}
\sup_{|\zeta-z|=\delta_{\rm C}|z|}|\mathcal R(\zeta)|
\ll |z|^{-7+\varepsilon_0}.
\tag{6}
\]

Equation (6), rather than the printed derivative range of Proposition 4.1,
is the order-six remainder input used below.

## 3. Complex-uniform sixth derivative of the saddle main term

Differentiate (3):

\[
L_N'=\frac{L_N}{Q_N}.
\tag{7}
\]

Put

\[
r=\frac1{L_N},\qquad \sigma=\frac{L_N}{N}.
\]

Then

\[
Q_N=NL_N\left(1+r-\frac34\sigma\right).
\tag{8}
\]

Repeated application of the exact total derivative

\[
\mathscr D=\partial_N+\frac{L_N}{Q_N}\partial_{L_N}
\]

to (2) gives

\[
G_0^{(6)}(N)=\frac{H_6(r,\sigma)}{N^5L_N},
\tag{9}
\]

where `H_6` is rational and its reduced denominator is

\[
(4+4r-3\sigma)^{12}.
\tag{10}
\]

The numerator is a polynomial, so (10) shows directly that `H_6` is
holomorphic and bounded in a fixed bidisc about `(0,0)`.  Lemma S(e) gives the
stronger bounds `|r|,|\sigma|\le7/50`.  On that bidisc the denominator obeys
`|4+4r-3\sigma|\ge151/50>0`.  The exact coefficientwise majorant in Lemma S
§8 gives the conservative whole-bidisc bound `|H_6|<10^4`; boundary sampling
is retained only as a non-rigorous diagnostic and is not used here.  Lemma
S(d) also gives `|L_N|\ge\tfrac12\log|N|`.  Consequently

\[
|G_0^{(6)}(N)|
\le\frac{10^4}{|N|^5|L_N|}
\le\frac{2\cdot10^4}{|N|^5\log|N|}
\tag{11}
\]

uniformly there.

Two ordering remarks, correcting an earlier draft.  First, `Q_N\neq0` is
**not** deduced from (10).  It is needed before the differentiated formula is
written at all, and Lemma S(f) supplies it independently, from the exact
identity `Q_N=NL_N(1+r-\tfrac34\sigma)` together with `|r|,|\sigma|\le1/4`,
which give `|1+r-\tfrac34\sigma|\ge9/16`.  Lemma S obtains the branch by
Rouché rather than by the implicit function theorem, precisely so that
`Q_N\neq0` is an output and never a hidden hypothesis.  Second, the bidisc
constant is a deliberately loose exact majorant; sampled boundary values are
not rigorous suprema and do not enter the theorem.

For the real-axis leading coefficient, setting `sigma=0` in the same exact
identity gives

\[
H_6(r,0)=
\frac{24r^8+216r^7+864r^6+2016r^5+3024r^4
+2399r^3+1042r^2+242r+24}{(1+r)^9},
\]

which tends to `24`.  The chain rule for `N=2x-2` gives the real leading
coefficient `48`.  The bound (11), not the sign of this coefficient, is what
the residual proof consumes.

The exact producer `c48_jensen/symbolic/sixth_saddle.py` checks (9)--(10),
the displayed `sigma=0` identity, and the coefficient `48`.  Its role is
regression checking; the proof of boundedness is the elementary rational
argument above.

## 4. Explicit normalization and the uniform saddle lemma

The sixth derivative of

\[
\log\!\left(32\binom{2z}{2}\right)
\]

is `O(|z|^-6)` on a smaller sector: after an additive constant, the term is
`log(2z)+log(2z-1)`.  The sixth derivative of the linear term in (1) is zero.
Combining this observation with (6) and (11) proves the missing lemma.

> **Uniform complex sixth-saddle lemma.**  There exist absolute constants
> `C,x1>0` such that, for every real `x>=x1` and complex `w` with
> `|w|<=x/1000`, the point `x+w` lies in the Phase-21 nonvanishing sector,
> the positive-axis branch of `h=log M` is holomorphic there, and
> \[
> |h^{(6)}(x+w)|\le\frac{C}{x^5\log x}.
> \tag{12}
> \]

Indeed, set `eta=1/1000`.  Then

\[
|\arg(x+w)|\le\arctan\frac{\eta}{1-\eta}<\theta_{\rm ctr}.
\]

Then `|x+w| asymp x`, and (12) follows from the preceding uniform estimates.
Nonvanishing and the logarithm branch come from Theorem 21B and the Phase-21
downstream discharge on the same sector; they are not inferred from the
derivative estimate.

## 5. The actual interpolation domain lies in the saddle sector

On the Phase-15 parameter branch,

\[
A\asymp n\mathcal L_n,\qquad
B\asymp C\asymp2n,\qquad D\asymp n,
\tag{13}
\]

and the Phase-16 radius is

\[
\rho=K_r\sqrt{Bd}\asymp\sqrt{nd}.
\]

Let

\[
\Omega=\{z\in\mathbb C:\operatorname{dist}(z,[0,d])\le2\rho\}.
\tag{14}
\]

The wedge `n^2 log(n+2) >= K d^3` implies

\[
\frac dn\longrightarrow0,
\qquad
\frac\rho n\ll\sqrt{\frac dn}\longrightarrow0
\tag{15}
\]

uniformly after increasing the fixed theorem constant and the eventual
threshold.  Thus

\[
\sup_{z\in\Omega}|z|\le d+2\rho\le\eta n.
\tag{16}
\]

Equation (16) is the previously omitted bridge: it puts every `n+z` used in
the residual proof inside the domain of (12).  It also proves
`M_(n+z) != 0` and provides one consistent logarithm branch throughout
`n+Omega`.

## 6. Complex polygamma bounds

Put `b=n+1/2`.  Six differentiations of the exact logarithmic coefficient
ratio give

\[
\begin{aligned}
E_F^{(6)}(z)=&\ h^{(6)}(n+z)
+\psi^{(5)}(B+z)-\psi^{(5)}(b+z)-\psi^{(5)}(A+z)\\
&+\psi^{(5)}(D+z)-\psi^{(5)}(C+z).
\end{aligned}
\tag{17}
\]

For `Re u>0`, the absolutely convergent series

\[
\psi^{(m)}(u)=(-1)^{m+1}m!
\sum_{k=0}^\infty(u+k)^{-m-1}
\tag{18}
\]

gives, uniformly for `Re u>=c n`,

\[
|\psi^{(5)}(u)|\ll n^{-5},
\qquad
|\psi^{(6)}(u)|\ll n^{-6}.
\tag{19}
\]

The branch theorem supplies

\[
B-C=O(n/\mathcal L_n),\qquad
D-b=O(n/\mathcal L_n).
\tag{20}
\]

For `z in Omega`, (13), (16), and positivity of the real parameters show
that every point on the straight segments joining `C+z` to `B+z` and
`b+z` to `D+z` has real part at least `c n`.  Therefore the complex line
integral identity

\[
\psi^{(5)}(U+z)-\psi^{(5)}(V+z)
=(U-V)\int_0^1\psi^{(6)}(V+z+t(U-V))\,dt
\tag{21}
\]

and (19)--(20) give `O(1/(n^5 L_n))` for both paired differences.  There
are no polygamma poles on the paths because their real parts are positive.
The remote term satisfies

\[
|\psi^{(5)}(A+z)|\ll A^{-5}
\ll(n^5\mathcal L_n^5)^{-1}.
\]

Together with (12), this proves

\[
\boxed{
\sup_{z\in\Omega}|E_F^{(6)}(z)|
\le\frac{C}{n^5\log(n+2)}.}
\tag{22}
\]

## 7. Logarithm branches and six exact zeros

All gamma arguments in the definition of `E_F` lie in the right half-plane
on `Omega`, so the gamma factors are nonzero and admit the logarithm branches
continued from the positive axis.  Section 5 supplies the corresponding
branch for `M_(n+z)`.  Hence `E_F` is holomorphic on a neighborhood of the
convex set `Omega`.

Exact matching through `R_5` gives

\[
\exp(E_F(j))=1\qquad(0\le j\le5).
\]

At those integer points every coefficient and model parameter is positive,
and all logarithms are on their real branches.  Therefore `E_F(j)` is real;
the preceding equality implies

\[
E_F(0)=E_F(1)=\cdots=E_F(5)=0.
\tag{23}
\]

This rules out the otherwise possible `2*pi*i` ambiguity.

## 8. Hermite--Genocchi and the multiplier defect

We use the following complex form, stated here to make the interpolation
step self-contained.  If `f` is holomorphic on a neighborhood of a convex
set containing `x_0,...,x_m`, then

\[
 f[x_0,\ldots,x_m]
 =\int_{\substack{t_j\ge0\\\sum_{j=0}^m t_j=1}}
   f^{(m)}\!\left(\sum_{j=0}^m t_jx_j\right)\,d\mathbf t,
\tag{HG}
\]

where `d\mathbf t` is the standard `m`-dimensional simplex measure, of total
mass `1/m!`.  Repeated application of the complex fundamental theorem of
calculus along line segments proves `(HG)`; convexity keeps every segment in
the holomorphy domain.  In particular, if `f(0)=...=f(5)=0`, the Newton
remainder identity gives

\[
 f(z)=f[0,1,2,3,4,5,z],z(z-1)\cdots(z-5).
\tag{HG6}
\]

The set (14) is the Minkowski sum of a real interval and a disk, hence is
convex.  For `z in Omega`, Hermite--Genocchi applied to the nodes
`0,1,...,5,z`, together with (22)--(23), gives

\[
|E_F(z)|\le
\frac{C}{6!\,n^5\log(n+2)}
|z(z-1)\cdots(z-5)|.
\tag{24}
\]

The wedge itself gives
`rho/d=K_r sqrt(B/d) -> infinity` for the already fixed `K_r`; hence
`rho>=d` after increasing only the eventual threshold.  Thus every factor on
the right of (24) is `O(rho)`.  Because `B asymp n`,

\[
\sup_\Omega|E_F|
\ll\frac{\rho^6}{n^5\log(n+2)}
\ll\frac{d^3}{n^2\log(n+2)}.
\tag{25}
\]

Increasing the theorem constant makes (25) at most `1/2`.  Thus, with
`c_F=exp(E_F)`,

\[
\sup_\Omega|c_F-1|\le2\sup_\Omega|E_F|\le1.
\tag{26}
\]

The multiplier is real at all integer points, equals one at `0,...,5`, and
has `c_F(d)>0`.

## 9. Exact trust statement

The new contribution of this note is the passage from the reconstructed
sectorial holomorphy and order-zero remainder estimate to the complete proportional-
neighborhood order-six lemma, followed by its explicit connection to the
actual interpolation domain and complex polygamma paths.  Phase 20 supplies
the dependency firewall and reconstruction; Holland's printed proposition
does not state the order-six derivative estimate.

The rational saddle differentiation is exactly reproduced, but the sectorial
analysis in Sections 1--8 and the new Phase-21 contour proof are conventional
paper mathematics.  Earlier layers passed disclosed AI pre-review; the new
combined chain still requires a fresh end-to-end AI pre-review and has not
received human peer review.

Primary sources: GORTTW, arXiv:1910.01227v3, Section 3; Jonathan Holland,
arXiv:2608.08682v1, Proposition 4.1, Lemma 4.2, and Lemma 8.1.
