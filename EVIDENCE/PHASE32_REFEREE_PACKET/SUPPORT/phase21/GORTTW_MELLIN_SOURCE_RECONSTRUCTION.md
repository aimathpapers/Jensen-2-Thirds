# GORTTW Mellin-source reconstruction

Audit date: 2026-08-15

Question: what exact integral and real saddle lie behind GORTTW (3.1)--(3.2),
and what is the first genuinely missing step in a sector-uniform complex proof?

Conclusion: **the exact Mellin identities and real saddle algebra reconstruct
cleanly, but neither GORZ nor GORTTW prints a complex contour or a uniform
complex saddle estimate. The first decisive proof milestone is a uniform
contour-localization lemma for the leading `k=1` Mellin integral.**

**Subsequent Phase-21 status.**  This source audit preceded the new proof.
`C48_LEADING_CONTOUR_LOCALIZATION.md`, `C48_HIGHER_THETA_MODES.md`, and
`C48_XI_COEFFICIENT_ASSEMBLY.md` now claim an internal self-contained discharge
of the identified gap. A separated Kimi K3 analytic AI pre-review subsequently
passed A0--A10 with no P0/P1/P2. This remains AI-only evidence, not human or
peer review.

## 1. Primary sources and frozen copies

1. M. J. Griffin, K. Ono, L. Rolen, and D. Zagier (`GORZ`),
   *Jensen polynomials for the Riemann zeta function and other sequences*,
   [arXiv:1902.07321v2](https://arxiv.org/abs/1902.07321v2), Section 4,
   equations (11)--(16) and the proof of Theorem 7; published in *PNAS*
   **116** (2019), 11103--11110,
   [DOI 10.1073/pnas.1902572116](https://doi.org/10.1073/pnas.1902572116).
2. M. J. Griffin, K. Ono, L. Rolen, J. Thorner, Z. Tripp, and I. Wagner
   (`GORTTW`), *Jensen polynomials for the Riemann xi-function*,
   [arXiv:1910.01227v3](https://arxiv.org/abs/1910.01227v3), Section 3,
   equations (3.1)--(3.2); published in *Advances in Mathematics* **397**
   (2022), Paper 108186,
   [DOI 10.1016/j.aim.2022.108186](https://doi.org/10.1016/j.aim.2022.108186).
3. J. Holland, *A new hyperbolicity wedge and a joint semicircle limit for
   Jensen polynomials of Riemann's xi-function*,
   [arXiv:2608.08682v1](https://arxiv.org/abs/2608.08682v1), equations
   (14)--(20) and Proposition 4.1.

| Official arXiv artifact | SHA-256 |
|---|---|
| GORZ v2 PDF | `e3cac568f996d050786c1e5cfc1420483db581de1fdf98fef4d5f1b73a9908fd` |
| GORZ v2 source download (gzip-compressed `PNASFinalVersion.tex`) | `7881fa4a36e1f4c22f6715c41072d467b0581d6aca870748f7b58440c4bbfaa2` |
| Decompressed GORZ TeX bytes | `6574a94142883c26fd91cbd5d4629c1a6d735b52b2f715451572bf1899a15ec0` |
| GORTTW v3 PDF | `f203487acc45a58808462e897240ce4929c998d9f0230d9a4bedb6d3841c3b2c` |
| GORTTW v3 source download | `d3918516b2310ec7215129122515b394c2735a43cb95a627815f75096f416c1c` |
| Decompressed GORTTW TeX bytes | `e482b9b43840543af9066d67196e31d9166f9920a5be356dc2c35ef3a7773c98` |

The GORZ equation audit used its official v2 PDF and TeX, downloaded during
this audit. GORTTW was checked against the already frozen v3 PDF and TeX.
Publisher records establish the journal metadata; journal PDFs were not
byte-diffed here.

## 2. Riemann's integral and the exact auxiliary Mellin integral

### 2.1 Printed source

GORZ Section 4 begins with

\[
 \Lambda(s)=\pi^{-s/2}\Gamma(s/2)\zeta(s)
 =\int_0^\infty t^{s/2-1}\theta_0(t)\,dt,
 \qquad
 \theta_0(t)=\sum_{k\ge1}e^{-\pi k^2t}.
 \tag{R1}
\]

The first integral is initially valid in its usual half-plane of absolute
convergence, `Re s>1`. Using

\[
 \theta_0(t)=\frac12(t^{-1/2}-1)+t^{-1/2}\theta_0(1/t),
\]

GORZ prints the meromorphic continuation

\[
 \Lambda(s)=\frac1{s(s-1)}+
 \int_1^\infty
 \left(t^{s/2}+t^{(1-s)/2}\right)\theta_0(t)\frac{dt}{t}.
 \tag{R2}
\]

It then defines, for real `n>=0`,

\[
 F(n)=\int_1^\infty(\log t)^n t^{-3/4}\theta_0(t)\,dt
 \tag{GORZ 12}
\]

and prints for positive derivative order `n`

\[
 \Lambda^{(n)}\!\left(\frac12\right)
 =-2^{n+2}n!+2^{1-n}F(n),
 \tag{GORZ 11}
\]

followed by the parenthetical assertion that both sides are zero when `n` is
odd. Literally, the displayed right side is not zero for odd `n`, because
`F(n)>0`. The display is correct for the even derivative orders actually
used later; it is missing parity factors if read for all `n`.

GORTTW Section 3 extends the auxiliary function by

\[
 F(z)=\int_1^\infty(\log t)^z t^{-3/4}
       \sum_{k\ge1}e^{-\pi k^2t}\,dt
 \tag{G-F}
\]

and states that it is holomorphic for `Re z>0`.

### 2.2 Direct derivations

For `t>1`, the base `log t` is a positive real number, so (G-F) has an
unambiguous parameter branch:

\[
 (\log t)^z:=\exp(z\log\log t),
\]

where both logarithms on the integration ray are real. Near `t=1`,
`log t` is comparable to `t-1`; at infinity, the theta series has
exponential decay. Compact-set domination therefore proves that (G-F) is
actually holomorphic on the larger half-plane `Re z>-1`. GORTTW's printed
`Re z>0` is conservative and is sufficient for its use.

Differentiating (R2) at `s=1/2` gives the parity-correct identity

\[
 \Lambda^{(n)}\!\left(\frac12\right)
 =\begin{cases}
 -2^{n+2}n!+2^{1-n}F(n),&n\text{ even},\\
 0,&n\text{ odd}.
 \end{cases}
 \tag{R3}
\]

Indeed, for even `n`, the two integral derivatives add to
`2^{1-n}F(n)`, while

\[
 \frac1{(1/2+w)(-1/2+w)}
 =-4\sum_{m\ge0}(4w^2)^m
\]

contributes `-2^{n+2}n!`. For odd `n`, the two integral derivatives cancel
and the rational term is even about `1/2`. Thus the parity omission in the
printed (11) is harmless for GORZ (13), which uses only orders `2n-2` and
`2n`, but it should be corrected in any self-contained reconstruction.

No complex contour is used in (R1), (R2), or (G-F): all three are integrals
over a positive real `t`-ray.

## 3. Coefficients, moments, and the factor eight

### 3.1 Printed definitions

GORZ defines `gamma_G(n)` by

\[
 (4w^2-1)\Lambda\!\left(\frac12+w\right)
 =\sum_{n\ge0}\frac{\gamma_G(n)}{n!}w^{2n}.
 \tag{GORZ 1}
\]

Its exact equation (13) is

\[
 \gamma_G(n)=\frac{n!}{(2n)!}
 \frac{32\binom{2n}{2}F(2n-2)-F(2n)}{2^{2n-1}}.
 \tag{GORZ 13}
\]

By contrast, GORTTW equation (1.1) defines `gamma_H(n)` by the centered xi
function itself:

\[
 \xi\!\left(\frac12+w\right)
 =\sum_{n\ge0}\frac{\gamma_H(n)}{n!}w^{2n}.
 \tag{GORTTW 1.1}
\]

GORTTW (3.1) nevertheless reproduces (GORZ 13) without changing the
constant.

### 3.2 Exact normalization derivation

Since

\[
 \xi(s)=\frac12s(s-1)\Lambda(s),
\]

substitution of `s=1/2+w` gives

\[
 (4w^2-1)\Lambda\!\left(\frac12+w\right)
 =8\xi\!\left(\frac12+w\right).
\]

Therefore

\[
 \gamma_G(n)=8\gamma_H(n).
 \tag{N8}
\]

Thus GORTTW (1.1) and (3.1) differ by exactly `8`. In the direct-xi
normalization, the correct continuation is

\[
 \gamma_H(M)=\frac{\Gamma(M+1)}{\Gamma(2M+1)}
 \frac{32\binom{2M}{2}F(2M-2)-F(2M)}{2^{2M+2}},
 \qquad \Re M>1.
 \tag{C3.1}
\]

Holland's moment normalization is

\[
 \gamma_H(z)=\frac{\Gamma(z+1)}{\Gamma(2z+1)}M_z
 =\frac{\sqrt\pi M_z}{4^z\Gamma(z+1/2)}.
 \tag{H14}
\]

Combining (C3.1) and (H14) yields the exact formula

\[
 M_z=2^{-2z-2}
 \left(32\binom{2z}{2}F(2z-2)-F(2z)\right),
 \qquad \Re z>1,
 \tag{H17}
\]

which is Holland (17). The factor error changes absolute logarithms by a
constant and does not change coefficient ratios or positive-order
logarithmic derivatives.

## 4. The real saddle printed in GORZ

### 4.1 Leading theta term and saddle variable

GORZ approximates the integrand in (GORZ 12) by its `k=1` theta term

\[
 f_n(t)=(\log t)^n t^{-3/4}e^{-\pi t}.
\]

For positive real `n`,

\[
 t\frac{d}{dt}\log f_n(t)
 =\frac n{\log t}-\pi t-\frac34.
\]

The unique real maximum is `t=a=e^L`, where

\[
 n=L\left(\pi e^L+\frac34\right).
 \tag{S}
\]

GORZ states `L(n) approximately log(n/log n)`. GORTTW strengthens the
notation to

\[
 L_M\sim\log\frac{M}{\log M},
 \qquad
 K_M=(L_M^{-1}+L_M^{-2})M-\frac34,
 \tag{LK}
\]

and asserts that `L_M` and `K_M` extend holomorphically and without zeros to
`Re M>1`.

### 4.2 Exact local change of variables

GORZ sets

\[
 t=(1+\lambda)a,
 \qquad
 \varepsilon=L^{-1},
 \qquad
 C=(\varepsilon+\varepsilon^2)n-\frac34.
\]

On the real integral, `lambda` runs from `-1+1/a` to infinity. The exact
local identity is

\[
 \frac{f_n((1+\lambda)a)}{f_n(a)}
 =\left(1+\frac{\log(1+\lambda)}L\right)^n
  (1+\lambda)^{-3/4}e^{-\pi\lambda a}.
 \tag{Local}
\]

Using the saddle equation, the linear logarithmic term vanishes and the
quadratic term is `-C lambda^2/2`. GORZ writes

\[
 \frac{f_n((1+\lambda)a)}{f_n(a)}
 =e^{-C\lambda^2/2}
  (1+A_3\lambda^3+A_4\lambda^4+\cdots),
 \tag{Taylor}
\]

where `A_i` is a polynomial of degree `floor(i/3)` in `n` with coefficients
in `Q[epsilon]`. It prints `A_3,A_4,A_5,A_6` explicitly on arXiv PDF p. 7.

The Gaussian curvature is exactly the later `K`:

\[
 C=K_n.
 \tag{CK}
\]

Also, if

\[
 Q_n=(1+L)n-\frac34L^2,
\]

then

\[
 Q_n=L^2K_n.
 \tag{QK}
\]

This identity explains the equivalence between the denominator in GORZ
Theorem 7 and the `sqrt(2 pi/K)` form used later.

### 4.3 Printed localization and estimates

GORZ formally integrates (Taylor) to obtain

\[
\begin{aligned}
 \int_1^\infty f_n(t)\,dt
 &=a f_n(a)\sqrt{\frac{2\pi}{C}}
 \left(1+\frac{3A_4}{C^2}+\frac{15A_6}{C^3}
       +\cdots\right).
\end{aligned}
 \tag{Gaussian}
\]

It states that only the region

\[
 C\lambda^2<B\log n,
 \tag{Window}
\]

contributes, where `B=B(n)` may be any function tending to infinity. It
interprets the display as an asymptotic expansion and says that the resulting
approximation may be truncated at `O(n^{-A})` for “some `A>0`.” The theorem's
“to all orders” formulation intends arbitrary fixed truncation order, but the
proof paragraph itself does not quantify that statement further.

GORZ Theorem 7 consequently states, for positive real `n`, the all-orders
expansion

\[
 F(n)\sim
 \sqrt{2\pi}\frac{L^{n+1}}
 {\sqrt{(1+L)n-\frac34L^2}}
 e^{L/4-n/L+3/4}
 \left(1+\frac{b_1}{n}+\frac{b_2}{n^2}+\cdots\right),
 \tag{GORZ 7}
\]

with

\[
 b_1=\frac{2L^4+9L^3+16L^2+6L+2}{24(L+1)^3}.
\]

The leading term may equivalently be written

\[
 \mathcal A_F(n)
 :=\sqrt{\frac{2\pi}{K_n}}L_n^n
   \exp\left(\frac{L_n}{4}-\frac n{L_n}+\frac34\right).
 \tag{AF}
\]

GORZ also states that replacing `F` by the two-term approximation in the
coefficient formula gives

\[
 \widehat\gamma_G(n)
 =\gamma_G(n)\left(1+O(n^{-2+\varepsilon})\right).
 \tag{GORZ 14}
\]

The proof says the higher theta terms are super-polynomially negligible near
the saddle. The displayed wording in the TeX says
`f(t)/theta_0(t)=1+e^{-3 pi t}+...`; literally this cannot be right because
`f` includes the factors `(log t)^n t^{-3/4}`. The intended exact relation is

\[
 \frac{(\log t)^n t^{-3/4}\theta_0(t)}{f_n(t)}
 =\frac{\theta_0(t)}{e^{-\pi t}}
 =1+e^{-3\pi t}+e^{-8\pi t}+\cdots.
\]

This appears to be a harmless typographical slip, but it should not be
copied into a new proof.

### 4.4 What the real proof does not quantify

The GORZ proof does not provide explicit inequalities for:

- the complement of (Window);
- the Taylor remainder uniformly up to the edge of (Window);
- interchange of the formal local series and integration;
- or the higher-theta tail away from the real saddle.

Those omissions do not create a visible contradiction in the published
real theorem, but they mean the printed proof is a compact saddle-point
argument, not a ready-made complex-uniform lemma.

## 5. How GORTTW obtains its equation (3.2)

### 5.1 Printed real formula

GORZ combines (GORZ 13), (GORZ 14), and Stirling to obtain its equation
(16). Besides the saddle main term, (16) retains the correction factors

\[
 \frac{1+1/(12M)}{1+1/(12N)},
 \qquad
 1+\frac{b_1(N)}N,
 \qquad N=2M-2,
\]

and a final relative error `O(M^{-2+epsilon})`.

GORTTW drops these first-order corrections into a coarser relative error.
With `N=2M-2`, its (3.2), in the GORZ normalization, is

\[
\begin{aligned}
 \gamma_G(M)
 &=\frac{e^{M-2}M^{M+1/2}L_N^N}
 {2^{2M-5}N^{N+1/2}}
 \left(\frac{2\pi}{K_N}\right)^{1/2}
 \exp\left(\frac{L_N}{4}-\frac N{L_N}+\frac34\right)\\
 &\quad\times\left(1+O_\varepsilon(M^{-1+\varepsilon})\right).
\end{aligned}
 \tag{G3.2}
\]

For the direct-xi/Holland coefficients, the right side must be divided by
`8`; equivalently, `2^{2M-5}` becomes `2^{2M-2}`.

The ignored `F(2M)` term in (GORZ 13) is covered on the real axis by GORZ
(14). At the level of the leading saddle formula, its relative scale is
approximately `L_N^2/M^2`, hence it is smaller than the coarser GORTTW
error. A complex proof must establish that comparison uniformly rather than
infer it from the real estimate.

### 5.2 The only printed complex statement

Immediately after (3.2), GORTTW says that analytic continuation of `L_M`
and Stirling allow the same error term for complex `M` after `M` is replaced
by `|M|`.

No complex contour is defined in GORZ or GORTTW. No deformation of the
positive `t`-ray is described. Neither paper states:

- a sector for `M`;
- uniformity in `arg M`;
- branches for `M^{M+1/2}`, `N^{N+1/2}`, `L_N^N`, or `sqrt(K_N)`;
- a holomorphic relative-error function;
- or a complex analogue of the localization estimate (Window).

Analytic continuation of the explicit saddle variable and sectorial
Stirling control the **explicit factors** in (G3.2). They do not by
themselves propagate a real-axis asymptotic for the integral `F` into a
two-dimensional sector. That propagation is the missing analytic work.

## 6. Branches and domains required by a complex proof

This subsection records derivations, not printed GORTTW specifications.

### 6.1 Saddle branch

Let

\[
 \mathcal F(L)=L\left(\pi e^L+\frac34\right).
\]

On a sufficiently narrow sector `|arg z|<theta`, a branch `L_z` continued
from positive real `z` should be selected by

\[
 \mathcal F(L_z)=z,
 \qquad
 L_z\sim\log\frac z{\log z}.
\]

The natural construction is a perturbation of the principal Lambert branch
`W(z/pi)`. It should give, uniformly on a closed subsector,

\[
 \Re L_z\asymp\log|z|,
 \quad |L_z|\asymp\log|z|,
 \quad e^{L_z}\asymp\frac{|z|}{\log|z|}.
\]

Implicit differentiation gives

\[
 \mathcal F'(L)=\pi e^L(L+1)+\frac34,
 \qquad
 K_z=\frac{\mathcal F'(L_z)}{L_z},
 \qquad
 L_z'=\frac1{L_zK_z}.
 \tag{D-LK}
\]

Thus nonvanishing of the inverse derivative and `L_z` implies nonvanishing
of `K_z`. This explains, but does not replace a proof of, GORTTW's assertion.

### 6.2 Complex powers

On a sector inside `Re z>1`, use the logarithms continued from the positive
axis:

\[
 z^{z+1/2}=\exp((z+1/2)\Log z),
 \quad
 N^{N+1/2}=\exp((N+1/2)\Log N),
 \quad
 L_N^N=\exp(N\Log L_N).
\]

Choose `sqrt(K_N)=exp(Log K_N/2)` by the same continuation. The complex
binomial `binom(2z,2)=z(2z-1)` is a polynomial and has no branch.

### 6.3 Integral phase and contour domain

For the leading theta term define

\[
 I_1(z)=\int_1^\infty
 (\log t)^z t^{-3/4}e^{-\pi t}\,dt.
\]

Near the positive ray its phase is

\[
 \Psi_z(t)=z\Log\Log t-\frac34\Log t-\pi t.
 \tag{Phase}
\]

The saddle is `a_z=e^{L_z}` because `Psi_z'(a_z)=0` is exactly (S).
Locally, with `t=a_z(1+lambda)`, the identity (Local) continues
holomorphically after all logs are fixed, and its quadratic coefficient is
`-K_z lambda^2/2`.

The endpoint `t=1` is a branch point of `Log Log t`. A contour proof must
therefore specify a slit domain, control a short endpoint segment separately,
and only then deform the remaining ray through `a_z`. No source does this.

## 7. Smallest rigorous first proof milestone

The elementary saddle-branch estimates in Section 6.1 are a prerequisite,
but they do not address the source gap. The smallest **decisive unresolved**
milestone is the following contour/localization lemma for `I_1`.

### Milestone 21A: sectorial leading-contour lemma

Prove that there exist `theta>0`, `R>0`, `rho>0`, and branches as in
Section 6 such that for every

\[
 z\in\mathcal S_\theta
 :=\{|z|>R,\ |\arg z|\le\theta\},
\]

there is a contour `Gamma_z`, deformable from the positive ray after a
separately controlled endpoint piece, with these properties:

1. `Gamma_z` lies in one fixed branch domain for `Log t` and `Log Log t`
   and passes through `a_z=e^{L_z}`.
2. On its central portion, `t=a_z(1+lambda)` and the orientation is chosen
   so that `K_z lambda^2` is positive real. Uniformly for
   `|lambda|<=rho`,

   \[
   \Psi_z(t)-\Psi_z(a_z)
   =-\frac12K_z\lambda^2+
     O\left(\frac{|z|}{|L_z|}|\lambda|^3\right).
   \]

3. On the central Gaussian window
   `|K_z lambda^2|<=B log|z|`, the Taylor remainder is uniformly
   integrable. On the complement of that window, the contour satisfies a
   uniform decay estimate strong enough to contribute
   `O(|z|^{-A})` times the saddle main term for one fixed `A>1`.
4. The contour deformation contributes no branch-jump or endpoint term.

This lemma is deliberately narrower than the full desired theorem. It
contains no theta-tail estimate, no `F(2z)/F(2z-2)` comparison, no gamma
factors, and no Cauchy differentiation. It resolves exactly the unsupported
passage from the real saddle to a uniform complex neighborhood.

Once Milestone 21A is proved, the local Gaussian calculation gives

\[
 I_1(z)=\mathcal A_F(z)
 \left(1+O_\varepsilon(|z|^{-1+\varepsilon})\right)
\]

uniformly on a smaller sector, with a holomorphic relative error. The
remaining proof can then proceed in separate, testable steps:

1. bound `sum_{k>=2} I_k(z)` uniformly relative to `I_1(z)`;
2. compare `F(N+2)` with `N^2F(N)` uniformly;
3. insert the exact factor-eight-corrected coefficient identity;
4. apply sectorial Stirling with the declared branches;
5. obtain nonvanishing from relative error `<1/2`, take the logarithm, and
   use Cauchy disks for every fixed derivative order.

## 8. Printed-source versus derivation ledger

| Statement | Status |
|---|---|
| Riemann integral (R1)--(R2) and `F(n)` | Printed in GORZ |
| GORZ (11) | Correct for even `n`; its printed all-`n` wording omits parity factors |
| `F(z)` holomorphic for `Re z>0` | Printed in GORTTW |
| `F(z)` holomorphic for `Re z>-1` | Direct dominated-convergence derivation here |
| Coefficient formula GORZ (13) | Printed and exact in the `8 xi` normalization |
| GORTTW (3.1) in its own direct-xi normalization | Off by factor `8` |
| Real saddle, local variable, `C`, `A_3` through `A_6` | Printed in GORZ, PDF pp. 6--7 |
| `C=K_n` and `Q_n=L_n^2K_n` | Exact algebraic derivations here |
| Real all-orders `F(n)` asymptotic | Theorem 7 in GORZ |
| Real coefficient error `O(n^{-2+epsilon})` | GORZ (14) |
| Coarser real error `O_epsilon(n^{-1+epsilon})` | GORTTW (3.2) |
| Complex error after replacing `M` by `|M|` | Asserted in one GORTTW sentence |
| Fixed-sector uniformity, contour, branches, holomorphic error | Not printed in GORZ or GORTTW |
| Holland nonvanishing/logarithm/Cauchy estimates | Correct deductions once the missing sectorial input is proved |

## 9. Bottom line

The source chain is now explicit:

\[
 \text{Riemann Mellin identity}
 \longrightarrow F(n)
 \longrightarrow \text{real }k=1\text{ saddle}
 \longrightarrow \gamma_G(n)
 \longrightarrow \gamma_H(n)=\gamma_G(n)/8.
\]

The real saddle uses the original positive `t`-ray and the real variable
`lambda`; it contains no hidden complex contour. GORTTW's later complex
sentence is not backed in either source by the sectorial contour,
localization, branch bookkeeping, or uniform tail estimates that Holland's
Proposition 4.1 needs. Milestone 21A is therefore the correct next proof
target: it is the smallest result that attacks the genuine missing step,
while leaving normalization, theta tails, gamma algebra, and Cauchy
differentiation as independent subsequent lemmas.
