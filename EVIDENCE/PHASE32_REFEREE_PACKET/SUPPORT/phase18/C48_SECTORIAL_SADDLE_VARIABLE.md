# The sectorial saddle variable: existence, uniqueness, and uniform asymptotics

Date: 2026-08-15
Status: self-contained paper proof closing review finding F1; adversarial AI
pre-review completed; not peer reviewed

## 0. Why this note exists

`C48_COMPLEX_SIXTH_SADDLE.md` §1 asserted, as equation (4),

\[
|L_N|\asymp\log|N|,\qquad
\frac1{L_N}\longrightarrow0,\qquad
\frac{L_N}{N}\longrightarrow0
\]

uniformly on smaller closed sectors, and called these "inherited facts from
the complex saddle."  They are not inherited from Holland's printed text.
Holland writes only

> For real `x>3`, let `L_x` be the positive solution of
> `x = L_x(pi e^{L_x} + 3/4)`.  **For complex `x` in the right half-plane,
> `L_x` denotes the branch of the holomorphic continuation used in
> [3, Section 3].**

so the complex branch is defined by deferral to Griffin--Ono--Rolen--Thorner--
Tripp--Wagner, and no sectorial asymptotics for it appear anywhere in
arXiv:2608.08682v1.  Since (4) is what places `(r,sigma)` inside the bidisc on
which `H_6` is bounded, it is load-bearing for the order-six saddle bound.

This note proves (4) directly from the saddle equation.  Nothing in
Sections 1--6 uses Holland or [3].  Section 7 then shows that the branch
constructed here is necessarily the branch they use, so the deferral becomes
harmless rather than load-bearing.

## 1. Statement

Throughout, all logarithms are principal, `ell := log|N|`, and

\[
\Psi(L):=L\left(\pi e^{L}+\tfrac34\right).
\]

> **Lemma S (sectorial saddle variable).**
> Let `0 < theta < pi/2` and put
> \[
> \mathfrak S_\theta(N_0):=\{N\in\mathbb C:\ |N|\ge N_0,\ |\arg N|\le\theta\}.
> \]
> Take `N_0 = e^{12}`, a value independent of `theta`.  Then there is a
> unique holomorphic `N\mapsto L_N` on `\mathfrak S_\theta(N_0)` such that
>
> **(a)** `N = \Psi(L_N)` throughout;
>
> **(b)** `L_N` is the positive real solution for real `N \ge N_0`.
>
> Writing `w := \log N` and `L_0 := w - \log w - \log\pi`, it satisfies,
> uniformly on `\mathfrak S_\theta(N_0)`:
>
> **(c)** `|L_N - L_0| < 1`, and in fact
> `L_N = \log N - \log\log N - \log\pi + O(\log \ell/\ell)`
> with an absolute implied constant;
>
> **(d)** `\ell - \log(\ell+1) - \log\pi - 1 \le \operatorname{Re}L_N \le |L_N| \le \ell + 2 + \log(\ell+1) + \log\pi + 1`;
> in particular `|L_N| \asymp \log|N|` and `|L_N| \ge \ell/2`;
>
> **(e)** with `r := 1/L_N` and `sigma := L_N/N`, one has
> `|r|,|sigma| \le 7/50` (hence both are at most `1/4`), and
> `r, sigma \to 0` uniformly as `|N|\to\infty`;
>
> **(f)** the exact identity
> `Q_N := (1+L_N)N - \tfrac34 L_N^2 = N L_N\bigl(1 + r - \tfrac34\sigma\bigr)`
> holds, `|1 + r - \tfrac34\sigma| \ge 9/16`, hence `Q_N \neq 0`; and
> `L_N' = L_N/Q_N`.

Parts (d)--(e) are exactly equation (4).  Part (f) supplies `Q_N \neq 0`
*before* it is needed, which removes the ordering defect recorded as F2.

## 2. The logarithmic form of the saddle equation

Fix `N` with `|arg N| \le theta` and let `L` lie in the open right half-plane
with `|3L/(4N)| < 1`.  Define

\[
G(L):=L+\log L+\log\pi-\log\!\left(1-\frac{3L}{4N}\right)-\log N .
\tag{S1}
\]

Every logarithm here is principal and its argument lies in the open right
half-plane, so `G` is holomorphic where defined.

**Claim.**  `G(L)=0` implies `N=\Psi(L)`.

Indeed, exponentiating (S1) at a zero gives

\[
\frac{e^{L}\,L\,\pi}{\bigl(1-\tfrac{3L}{4N}\bigr)N}=1,
\qquad\text{i.e.}\qquad
\pi Le^{L}=N-\tfrac34L,
\]

which rearranges to `L(\pi e^{L}+3/4)=N`.  (Only this direction is used; we
locate a zero of `G` and then read off that it solves the saddle equation.)

## 3. Location of the comparison point

Write `w=\log N=\ell+i\varphi` with `|\varphi|\le\theta<\pi/2`.  Then

\[
\ell\le|w|\le\sqrt{\ell^2+\theta^2}\le\ell+\frac{\theta^2}{2\ell}\le\ell+1,
\qquad
|\arg w|=\left|\arctan\frac\varphi\ell\right|\le\frac\theta\ell ,
\tag{S2}
\]

for `\ell\ge2`.  Consequently `\log \ell \le \log|w| \le \log(\ell+1)` and

\[
|\log w|\le\log(\ell+1)+\frac\theta\ell .
\tag{S3}
\]

With `L_0=w-\log w-\log\pi`,

\[
\operatorname{Re}L_0=\ell-\log|w|-\log\pi\ \ge\ \ell-\log(\ell+1)-\log\pi,
\tag{S4}
\]
\[
|L_0|\le|w|+|\log w|+\log\pi\le \ell+1+\log(\ell+1)+\frac\theta\ell+\log\pi .
\tag{S5}
\]

Introduce the two elementary quantities

\[
m(\ell):=\ell-\log(\ell+1)-\log\pi-1,
\qquad
M(\ell):=\ell+2+\log(\ell+1)+\frac\theta\ell+\log\pi ,
\]

so that on the closed disc `\bar D:=\{|L-L_0|\le1\}` we have

\[
\operatorname{Re}L\ge m(\ell),\qquad |L|\le M(\ell).
\tag{S6}
\]

Both are monotone for `\ell\ge12` (`m` increasing, `M(\ell)e^{-\ell}`
decreasing), and since `\theta<\pi/2` every bound below is **uniform in
`theta`**.

At `\ell=12`: `m(12)=12-\log13-\log\pi-1=7.290\ldots>0` and
`M(12)\le17.841`.  So on `\bar D` the point `L` lies in the open right
half-plane, `\log L` is defined, and

\[
\left|\frac{3L}{4N}\right|\le\frac{3M(\ell)}{4e^{\ell}}
\le\frac{3\cdot17.841}{4e^{12}}<10^{-4}<\tfrac12 ,
\tag{S7}
\]

so `1-3L/(4N)` lies in the disc of radius `1/2` about `1` and, using
`|\log(1+u)|\le2|u|` for `|u|\le1/2`,

\[
\left|\log\!\left(1-\frac{3L}{4N}\right)\right|
\le\frac{3M(\ell)}{2e^{\ell}} .
\tag{S8}
\]

Hence `G` is holomorphic on a neighbourhood of `\bar D`.

## 4. Rouché

Put `H(L):=L-L_0`, which has exactly one zero in `D`, at `L_0`, and satisfies
`|H|=1` on `\partial D`.  Subtracting definitions,

\[
G(L)-H(L)=\log L-\log w-\log\!\left(1-\frac{3L}{4N}\right).
\tag{S9}
\]

Since `\operatorname{Re}L>0` and `\operatorname{Re}w>0`, both arguments have
modulus of argument below `\pi/2`, so
`\log L-\log w=\operatorname{Log}(L/w)` with no `2\pi i` ambiguity.  For
`L\in\partial D` write `L=L_0+\zeta` with `|\zeta|=1`; then

\[
\frac Lw=1-\frac{\log w+\log\pi-\zeta}{w},
\qquad
\left|\frac Lw-1\right|\le\eta(\ell):=
\frac{\log(\ell+1)+\dfrac\theta\ell+\log\pi+1}{\ell}.
\tag{S10}
\]

At `\ell=12`, `\eta\le4.841/12=0.4034\le1/2`, and `\eta` is decreasing, so
`|\operatorname{Log}(L/w)|\le2\eta(\ell)` for all `\ell\ge12`.  Combining with
(S8),

\[
\sup_{\partial D}|G-H|
\le2\eta(\ell)+\frac{3M(\ell)}{2e^{\ell}}
\le 0.8068+0.0002<1=\inf_{\partial D}|H| .
\tag{S11}
\]

By Rouché's theorem `G` has **exactly one** zero in `D`, and it is simple.
Call it `L_N`.  By §2 it satisfies `N=\Psi(L_N)`, proving (a), and
`|L_N-L_0|<1` gives the first half of (c).

## 5. Holomorphy, uniqueness, and reality

**Holomorphy.**  Interpret holomorphy on the closed truncated sector as
holomorphy on its interior with continuation to a neighbourhood of every
point of the sector.  The function
`L_0(N)=\log N-\log\log N-\log\pi` and the two-variable function `G(L;N)` are
holomorphic on the open domains used above.  Rouché counts the zero of `G` in
`D(N)` **with multiplicity** and gives total multiplicity one, so that zero is
simple.  The holomorphic implicit-function theorem therefore supplies a local
holomorphic branch through it.  For nearby `N`, the strict uniform inequality
(S11) keeps the local zero inside the corresponding disc `D(N)`; uniqueness
there forces any two local branches to agree on overlaps.  They consequently
patch to a single holomorphic `N\mapsto L_N` on the sector.  This route does
**not** presuppose the explicit formula `L_N'=L_N/Q_N`; the nonvanishing of
`Q_N` and that derivative formula are derived independently in §6.

**Uniqueness.**  `\mathfrak S_\theta(N_0)` has connected, simply connected
interior: `\exp` maps the convex half-strip
`\{\operatorname{Re}u>\log N_0,\ |\operatorname{Im}u|<\theta\}`
biholomorphically onto it, since `\theta<\pi`.  Any holomorphic solution of
(a) agreeing with `L_N` on a real ray therefore agrees with it everywhere, by
the identity theorem.

**Reality.**  For real `N\ge N_0` the point `L_0` is real and `\bar D` is
stable under conjugation; moreover `\overline{G(\bar L;N)}=G(L;N)`, because
all coefficients are real and every logarithm is evaluated in the right
half-plane.  So the conjugate of the unique zero is again a zero in `D`,
forcing `L_N\in\mathbb R`.  Since `\operatorname{Re}L_N\ge m(\ell)>0` and
`t\mapsto\Psi(t)` is a strictly increasing bijection of `(0,\infty)` onto
itself, `L_N` is *the* positive real solution.  This proves (b).

## 6. Quantitative consequences

**(c), sharp form.**  Rearranging `G(L_N)=0`,

\[
L_N-L_0=-\operatorname{Log}\frac{L_N}{w}
+\log\!\left(1-\frac{3L_N}{4N}\right),
\]

so by (S8) and (S10),

\[
\bigl|L_N-(\log N-\log\log N-\log\pi)\bigr|
\le2\eta(\ell)+\frac{3M(\ell)}{2e^{\ell}}
=O\!\left(\frac{\log\ell}{\ell}\right),
\tag{S13}
\]

with an absolute implied constant.  In particular the error tends to `0`.

**(d).**  Immediate from (S6) and `|L_N|\ge\operatorname{Re}L_N`.  For
`\ell\ge12` one checks `m(\ell)\ge\ell/2` (at `\ell=12`, `7.29\ge6`, and
`\ell/2-\log(\ell+1)` is increasing), so `|L_N|\ge\ell/2=\tfrac12\log|N|`,
while
`|L_N|\le M(\ell)\le\ell+\log(\ell+1)+4`.  Hence
`|L_N|\asymp\log|N|`, and in fact
`|L_N|/\log|N|\to1`.

**(e).**  `|r|=1/|L_N|\le1/m(\ell)\le1/7.29<7/50` and
`|\sigma|\le M(\ell)/e^{\ell}<1/7500<7/50`, both `\to0`.  The
`1/7500` bound follows directly from (S7), because
`(3/4)|\sigma|<10^{-4}`.  (The sharper assertion
`|\sigma|<10^{-4}` would be slightly false at the left endpoint and is not
used.)

**(f).**  Directly from the definition,

\[
Q_N=(1+L_N)N-\tfrac34L_N^2
=NL_N\left[\frac{1+L_N}{L_N}-\frac34\frac{L_N}{N}\right]
=NL_N\left(1+r-\tfrac34\sigma\right),
\tag{S14}
\]

an **exact** identity requiring no asymptotics.  By (e),

\[
\left|1+r-\tfrac34\sigma\right|\ \ge\ 1-\tfrac14-\tfrac34\cdot\tfrac14
=\tfrac9{16}>0 ,
\]

so `Q_N\neq0` and `Q_N=NL_N(1+O(1/L_N))`.  Differentiating `N=\Psi(L_N)` and
substituting `\pi e^{L_N}=N/L_N-3/4` gives

\[
1=L_N'\left[\pi e^{L_N}+\tfrac34+L_N\pi e^{L_N}\right]
=L_N'\cdot\frac{(1+L_N)N-\tfrac34L_N^2}{L_N}
=L_N'\cdot\frac{Q_N}{L_N},
\]

hence `L_N'=L_N/Q_N`.  This completes the proof of Lemma S.  `∎`

## 7. Identification with the branch used by Holland and by [3]

Lemma S produces *the* holomorphic solution of the saddle equation on
`\mathfrak S_\theta(e^{12})` that restricts to the positive real solution on
the real ray.  By the uniqueness argument in §5, there is no other.  Holland's
phrase "the branch of the holomorphic continuation used in [3, Section 3]"
denotes, by the meaning of *continuation*, the analytic continuation of that
same positive real solution.  Therefore the two coincide.

The practical consequence is that **no property of [3] is needed to establish
(4)**.  The dependency on [3, §3] for the saddle variable drops from
load-bearing to an identification remark.  It remains load-bearing elsewhere:
Holland's Proposition 4.1 derives its representation (20), and hence the
non-vanishing of `M_z` and the remainder estimate (19), from the complex form
of [3, (3.1)--(3.2)].  See `C48_HOLLAND_DEPENDENCY_AUDIT.md` §6a.

## 8. Effective form of the order-six main-term bound

Combining Lemma S(e) with the exact rational identity of
`C48_COMPLEX_SIXTH_SADDLE.md` §3,

\[
G_0^{(6)}(N)=\frac{H_6(r,\sigma)}{N^5L_N},
\qquad
H_6=\frac{(\text{polynomial in }r,\sigma\text{ of total degree }13)}
{(4+4r-3\sigma)^{12}},
\]

we may now make the compactness argument quantitative.  On the closed bidisc
`|r|,|\sigma|\le7/50`, the denominator obeys
`|4+4r-3\sigma|\ge4-7(7/50)=151/50>0`, so `H_6` is holomorphic there.

The maximum principle by itself only says that the maximum occurs on the
distinguished boundary; **sampling that boundary does not prove a numerical
upper bound**.  The exact producer therefore uses a coefficientwise majorant.
Writing `P` for the 82-term numerator, it verifies in exact rational arithmetic
that

\[
\sum_{a,b}|[r^a\sigma^b]P|\,(7/50)^{a+b}
\big/(151/50)^{12}
=\frac{6422139805764931584036533551104}
{702576099728137594188684005}
<10^4.
\]

This is a triangle-inequality proof on the whole bidisc, not a numerical grid
estimate.  The boundary samples retained by the producer are labelled only as
conditioning diagnostics.  Since Lemma S(d) gives
`|L_N|\ge\tfrac12\log|N|`, we obtain the conservative effective statement

\[
\boxed{\;
|G_0^{(6)}(N)|\le\frac{20000}{|N|^5\log|N|}
\quad\text{for }|N|\ge e^{12},\ |\arg N|\le\theta<\frac\pi2 . \;}
\tag{S15}
\]

This is the quantitative form of `C48_COMPLEX_SIXTH_SADDLE.md` (11), and it
is uniform in `theta` on `(0,\pi/2)`.

## 9. Numerical regression

`c48_jensen/symbolic/saddle_branch_check.py` solves the saddle equation in the
well-scaled logarithmic form at `|N| = 10^4,\dots,10^{600}` and
`\arg N \in\{0,\,0.6,\,1.4\}` and confirms:

| `|N|` | `\ell` | `|L_N-L_0|` | `|L_N-L_0|\cdot\ell/\log\ell` | `|L_N|/\ell` | `|r|` | `|\sigma|` |
|---|---|---|---|---|---|---|
| `10^4` | 9.21 | 0.388 | 1.61 | 0.688 | 0.158 | 6.3e-4 |
| `10^8` | 18.42 | 0.232 | 1.47 | 0.795 | 0.068 | 1.5e-7 |
| `10^{16}` | 36.84 | 0.134 | 1.37 | 0.875 | 0.031 | 3.2e-15 |
| `10^{80}` | 184.21 | 0.035 | 1.23 | 0.966 | 0.0056 | 1.8e-78 |
| `10^{600}` | 1381.55 | 0.0061 | 1.16 | 0.994 | 7.3e-4 | ~0 |

The fourth column is bounded, confirming (S13); the fifth tends to `1`,
confirming (d).  The bound (S13) is loose by a factor of roughly `2.6`, which
is expected from the crude `|\log(1+u)|\le2|u|` step.  The regression also
confirms the exact identity (S14) to full working precision.

The numerics are a regression check only.  Sections 2--8 are the proof.

## Trust boundary

Sections 1--8 are elementary complex analysis: Rouché, the argument
principle, the identity theorem, and the maximum principle on a polydisc.
They use no unpublished input and no property of arXiv:2608.08682v1 or of
[3].  They have not been formalized in Lean.  They have passed an adversarial
AI pre-review but not human peer review.
