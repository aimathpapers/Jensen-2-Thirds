# Sectorial contour research for the GORZ saddle

Research date: 2026-08-16

Target integral:

\[
 I_1(s)=\int_1^\infty(\log t)^s t^{-3/4}e^{-\pi t}\,dt.
\]

Verdict: **RESTATE.** A sufficiently narrow fixed-sector asymptotic appears
viable and there is a concrete branch-safe contour through the GORZ saddle.
The present Milestone 21A should be restated around that contour and around
`Re(K_s lambda^2)>0`, rather than requiring `K_s lambda^2` to be exactly
positive real. There is no evident endpoint or Stokes obstruction in a
small fixed sector. The missing work is a global, quantitative decay lemma,
not a conceptual failure of the saddle method.

**Subsequent Phase-21 status.**  This primary-method research ran concurrently
with the proof construction.  `C48_LEADING_CONTOUR_LOCALIZATION.md` now supplies
the global gap proposed here by proving strict horizontal log-concavity and
quantitative boundary slopes.  That proof has not yet received the fresh
adversarial review required by the execution plan.

## 1. Sources inspected

### Problem-specific primary sources

1. M. J. Griffin, K. Ono, L. Rolen, and D. Zagier (`GORZ`),
   *Jensen polynomials for the Riemann zeta function and other sequences*,
   [arXiv:1902.07321v2](https://arxiv.org/abs/1902.07321v2), Theorem 7 and
   its proof, especially PDF pp. 6--7. This is the source of the exact local
   phase, the saddle equation, the coefficients `A_3,...,A_6`, and the real
   localization claim.
2. M. J. Griffin, K. Ono, L. Rolen, J. Thorner, Z. Tripp, and I. Wagner
   (`GORTTW`), *Jensen polynomials for the Riemann xi-function*,
   [arXiv:1910.01227v3](https://arxiv.org/abs/1910.01227v3), Section 3,
   especially the sentence following (3.2). That sentence asserts the
   complex extension but supplies no contour or uniform sector.

The already frozen source hashes are recorded in
`GORTTW_MELLIN_SOURCE_RECONSTRUCTION.md`.

### Method sources

3. N. M. Temme, *Uniform Asymptotic Methods for Integrals*,
   [arXiv:1308.1547v1](https://arxiv.org/abs/1308.1547v1), especially
   Sections 2.2--2.3 (PDF pp. 7--8) and Remark 3.1 (PDF p. 18). The official
   PDF inspected here has SHA-256
   `93d3557ce4824a823e1fe2b8a3ca1e34a780ad1db46654e9af0f219a81d419a4`.
   Temme is an author-written methodological source, not a secondary
   description of GORZ.
4. NIST DLMF, [Section 2.4(iv), Saddle Points](https://dlmf.nist.gov/2.4.iv),
   and [Section 2.11(iii)](https://dlmf.nist.gov/2.11.iii), authored for the
   DLMF chapter by F. W. J. Olver and R. Wong. DLMF is used as an
   authoritative reference and worked precedent, not as evidence that the
   GORZ hypotheses have already been checked.

## 2. What the method sources actually say

### 2.1 Temme

Temme Section 2.2 treats the Gaussian Laplace form

\[
 \int_{-\infty}^{\infty}e^{-zv^2}f(v)\,dv,
 \qquad \Re z>0,
\]

with `f` analytic in a complex domain containing the real axis. On PDF p. 7
he explicitly discusses rotating the path and states a sector of uniformity
obtained by combining the angular domain of `f` with the convergence
condition `cos(arg z+2 arg v)>0`; see his equations (2.10)--(2.12).

Temme Section 2.3 states that a saddle contour must stay in an analytic
domain and avoid singularities and branches. It describes deformation
through a saddle, usually along a path where the imaginary part of the phase
is constant, followed by reduction to the Gaussian Laplace form.

Most relevantly, Temme Remark 3.1 observes that real-variable stationary
phase can fail to reveal an exponentially small answer. His stated remedy is
analytic continuation into the complex plane, modification of the real
interval into a contour, and the saddle-point method. This is directly
applicable to `I_1(x+iy)`, whose positive-ray integral can be exponentially
smaller than its absolute-value majorant when `y` is proportional to `x`.

### 2.2 DLMF

DLMF Section 2.4(iv) says that an exact steepest-descent path is advantageous
but is not essential merely to derive a saddle expansion. A contour on which
the real part has a strict quadratic maximum is enough if the remaining
Laplace hypotheses and error bounds are proved.

DLMF Section 2.11(iii), equations (2.11.12)--(2.11.14), is a useful worked
analogue. For a complex-parameter integral with a moving saddle, it rotates
the positive integration path through the saddle and obtains an expansion
uniform while the angular parameter stays in a fixed compact subinterval.
This does not prove our estimate, but it confirms that “rotate the tail to
the moving saddle, then apply Laplace uniformly” is a standard rigorous
architecture.

## 3. Exact GORZ local phase

For positive real `s`, GORZ uses

\[
 f_s(t)=(\log t)^s t^{-3/4}e^{-\pi t}
\]

and the saddle `a_s=e^{L_s}`, where

\[
 s=L_s\left(\pi e^{L_s}+\frac34\right).
 \tag{S}
\]

Define

\[
 K_s=\left(L_s^{-1}+L_s^{-2}\right)s-\frac34.
\]

With `t=a_s(1+lambda)`, GORZ's exact local ratio is

\[
 \frac{f_s(a_s(1+\lambda))}{f_s(a_s)}
 =\left(1+\frac{\log(1+\lambda)}{L_s}\right)^s
  (1+\lambda)^{-3/4}e^{-\pi a_s\lambda}.
 \tag{L}
\]

After branches are continued from positive `s`, the logarithm of the right
side has zero linear term and quadratic term

\[
 -\frac12K_s\lambda^2.
 \tag{Q}
\]

These identities are algebraic and continue locally to complex `s`. What
does not follow algebraically is that an integration contour reaches this
saddle and that the complement of its Gaussian neighborhood is uniformly
smaller.

## 4. A concrete branch-safe contour

This section is a derivation, not a statement found in GORZ, GORTTW, or
Temme.

### 4.1 Pass to the logarithmic plane

Put `u=Log t`, using the principal logarithm on the positive ray. Then

\[
 I_1(s)=\int_0^\infty G_s(u)\,du,
 \qquad
 G_s(u)=u^s\exp\left(\frac u4-\pi e^u\right),
 \tag{U}
\]

where `u^s=exp(s Log u)` uses the principal `Log u`. Choose a fixed
`u_0>0` and split off `[0,u_0]`. On the half-strip `Re u>=u_0`, the function
`G_s(u)` is analytic: the branch point `u=0` and the negative real branch cut
are both outside.

Let

\[
 \beta_s=\Im L_s.
\]

For `s` in a sufficiently narrow sector and large `|s|`, the principal
saddle branch has `|beta_s|<beta_0<pi/2`. Apply Cauchy's theorem to the
rectangle with horizontal sides on `Im u=0` and `Im u=beta_s`. The far
vertical side tends to zero because

\[
 \left|e^{-\pi e^{r+iv}}\right|
 =e^{-\pi e^r\cos v}
\]

and `cos v>=cos beta_0>0`. The exact deformation is

\[
 \int_{u_0}^{\infty}G_s(u)\,du
 =i\int_0^{\beta_s}G_s(u_0+iv)\,dv
  +\int_{u_0}^{\infty}G_s(r+i\beta_s)\,dr.
 \tag{C}
\]

The formula is orientation-correct for positive or negative `beta_s` when
the first integral is interpreted from `0` to `beta_s`.

### 4.2 Return to the `t`-plane

The horizontal line `u=r+i beta_s` maps to the ray

\[
 t=e^{i\beta_s}e^r.
\]

Because `a_s=e^{L_s}`, this ray passes exactly through `a_s`. On the ray,
write

\[
 t=a_s(1+\lambda),
 \qquad \lambda\in\mathbb R,
 \qquad
 \lambda>e^{u_0-\Re L_s}-1.
\]

Thus the deformed tail uses **the exact GORZ variable** and the exact local
ratio (L), with real `lambda`. No `Log Log t` branch is crossed: throughout
the deformation `Re u>=u_0>0`.

This contour is simpler to verify than an unspecified global thimble. It is
not exactly a constant-phase path, but the method sources do not require
that. It is enough to prove a uniform real-part decrease.

## 5. Local Gaussian condition on the explicit ray

The saddle-variable estimates give, on a sufficiently narrow fixed sector,

\[
 |L_s|\asymp\log|s|,
 \qquad
 K_s\sim\frac{s}{L_s},
 \qquad
 \Re K_s\ge c|K_s|
 \tag{K+}
\]

for some `c>0`. The last inequality is the relevant one on the explicit
ray. For real `lambda`, (Q) then gives

\[
 \Re\left(-\frac12K_s\lambda^2\right)
 \le-\frac c2|K_s|\lambda^2.
\]

The logarithm of (L), denoted `H_s(lambda)`, is

\[
 H_s(\lambda)
 =s\Log\left(1+\frac{\log(1+\lambda)}{L_s}\right)
  -\frac34\log(1+\lambda)-\pi a_s\lambda.
 \tag{H}
\]

Here `log(1+lambda)` is real and
`L_s+log(1+lambda)=Log t` remains in the right half-plane on the truncated
ray. Hence the branch in (H) is fixed and analytic.

For `|lambda|<=rho` with fixed sufficiently small `rho`, direct Taylor
estimates should yield

\[
 H_s(\lambda)=-\frac12K_s\lambda^2
 +O\left(\frac{|s|}{|L_s|}|\lambda|^3\right),
 \tag{T3}
\]

uniformly in the sector. Since `|K_s|` is comparable to `|s|/|L_s|`, the
usual Gaussian window

\[
 |\lambda|\le
 \sqrt{B\log|s|/|K_s|}
\]

shrinks to zero, and the cubic term is perturbative there for slowly growing
fixed-choice `B`. Temme's Gaussian Laplace result then applies after the
local analytic change of variable, once a uniform amplitude bound is
written down.

The current Milestone 21A asks that the orientation make
`K_s lambda^2` positive real. The explicit ray only guarantees the stronger
fact needed for convergence, namely a uniformly positive **real part**.
One could bend a short central segment by `-arg(K_s)/2` to obtain an exact
steepest direction, but doing so complicates the connectors without adding
analytic value.

## 6. What remains to prove globally

The contour identity (C) is rigorous once the saddle branch and
`|beta_s|<beta_0` are established. It does not by itself prove dominance of
the saddle. A defensible proof still needs the following estimates.

### 6.1 Initial segment and connector

On the compact set consisting of `[0,u_0]` and the vertical connector at
`u_0`, one has for `|Im s|<=kappa Re s`

\[
 |G_s(u)|\le e^{C_{u_0,\kappa}\Re s}.
\]

The saddle main term has logarithmic magnitude

\[
 \Re(s\Log L_s)+O(|s|/|L_s|)
 =\Re s\,\log\log|s|+O_\kappa(\Re s).
\]

Therefore the fixed initial piece and connector are eventually negligible
by a factor exponential in `-Re s log log|s|`. This comparison is
straightforward but must be written with explicit inequalities.

### 6.2 Middle and far parts of the rotated ray

For the exact normalized action (H), prove a three-region estimate:

1. `|lambda|<=rho`: use (T3) and (K+).
2. `lambda` bounded away from zero but before the far tail: prove a strict
   negative gap by quantitative perturbation of the real GORZ phase, whose
   unique maximum is at `lambda=0`.
3. large positive `lambda`: use
   `Re a_s>=c|a_s|` so `-pi a_s lambda` dominates the logarithmic terms.

On the far negative side, the ray stops at
`lambda=e^{u_0-Re L_s}-1`; it never reaches the branch point `-1`. Near that
lower limit the ratio of `Log t` to `L_s` itself supplies a large negative
gap. This is another advantage of splitting at fixed `u_0>0`.

These inequalities are plausible and consistent with the exact phase, but
they are not printed in any inspected source. They are the core proof work
still outstanding.

## 7. Can the positive ray be used without deformation?

There is an exact probabilistic rewriting for `s=x+iy`:

\[
 I_1(x+iy)=I_1(x)\,
 \mathbb E_x\!\left[e^{iy\log\log T}\right],
\]

where the probability density is proportional to
`(log t)^x t^{-3/4}e^{-pi t}`. The real saddle calculation predicts

\[
 \operatorname{Var}_x(\log\log T)\asymp\frac1{xL_x}.
\]

Consequently, when `y=kappa x`, the characteristic-function factor is
expected to have size approximately

\[
 \exp\left(-\frac{\kappa^2x}{2L_x}\right).
\]

This is exponentially small relative to the absolute-value bound
`|I_1(x+iy)|<=I_1(x)`. A finite real-axis Laplace expansion therefore loses
the cancellation needed for a relative error and for nonvanishing. This is
exactly the failure mode Temme discusses in Remark 3.1.

A positive-ray characteristic-function proof might work in a narrower
window such as `|y|=O(sqrt(xL_x))`. For a fixed angular sector, it would need
a complex large-deviation argument equivalent in substance to the contour
shift. The explicit contour (C) is the cleaner route.

## 8. Branches, endpoints, and likely Stokes boundary

### Branches

- In the `u`-plane, the only relevant parameter branch is `u^s`, with cut
  on the nonpositive real axis.
- The deformation stays in `Re u>=u_0>0`, so it crosses no cut.
- In the `t`-plane, this is equivalent to keeping `Log t` in the right
  half-plane and hence keeping `Log Log t` on one branch.

### Endpoint

The branch endpoint `u=0` is isolated before deformation. As `|s|` grows,
the saddle satisfies `Re L_s` tending to infinity, so the saddle moves away
from the endpoint rather than coalescing with it. There is no endpoint
transition in a fixed sector.

### Other saddle sheets

Other formal solutions associated with nonprincipal logarithmic/Lambert
sheets lie outside the horizontal strip used here. The strip
`|Im u|<beta_0<pi/2` contains the continued principal saddle only. No
competing saddle contribution is forced into the contour for small fixed
angle.

### Likely angular obstruction

The horizontal contour decays at infinity only while
`cos(beta_s)>0`. The natural geometric boundary occurs when
`|beta_s|` approaches `pi/2`; there the factor `e^{-pi e^u}` ceases to decay
uniformly on the shifted line. Since `beta_s` is asymptotic to `arg s` on
the principal branch, this points to possible Stokes or contour changes near
`arg s=+/-pi/2`, not near the positive axis.

Nothing in the inspected sources or the phase geometry indicates a Stokes
line inside a sufficiently small fixed sector around the positive axis.

## 9. Restated milestone

The following should replace the present Milestone 21A.

> **Milestone 21A-R (explicit shifted-ray localization).** Prove that there
> exist `theta_0>0`, `R>0`, `u_0>0`, `beta_0<pi/2`, and positive constants
> `c,C` such that for `|s|>=R`, `|arg s|<=theta_0`:
>
> 1. the principal saddle `L_s` exists, `|Im L_s|<=beta_0`, and
>    `Re K_s>=c|K_s|`;
> 2. the exact rectangle deformation (C) holds;
> 3. on the shifted ray through `a_s`, the normalized action (H) obeys a
>    quadratic upper bound in a fixed neighborhood of zero and a uniform
>    strict negative gap outside that neighborhood;
> 4. the initial segment, connector, and far tail are bounded by
>    `C|A_F(s)||s|^{-2}`;
> 5. hence
>    \[
>      I_1(s)=A_F(s)
>      \left(1+O_{\theta_0}(|s|^{-1+\varepsilon})\right)
>    \]
>    uniformly on a slightly smaller closed sector, with a holomorphic
>    relative error.

The `|s|^{-2}` in item 4 is a convenient target, not a source-quoted
constant. Any uniform power saving stronger than the desired final error is
enough.

## 10. Final verdict

**RESTATE, not KILL.** The fixed-sector target itself survives for a
sufficiently small angle. The proposed contour can be made concrete by
shifting the `u=Log t` ray to `Im u=Im L_s`, equivalently rotating the
positive `t`-tail onto the ray through `a_s`. This contour is branch-safe,
has double-exponential decay at infinity, separates the endpoint before
deformation, and places the exact GORZ saddle on a path with
`Re K_s>0`.

The proof is not finished: the global real-part gap for (H) must still be
established uniformly. But the primary method sources support this
architecture, and the likely Stokes boundary is far from the narrow sector
needed by Holland. The right next action is to prove Milestone 21A-R, not to
abandon sectorial verification and not to claim the current informal
Milestone 21A as already complete.
