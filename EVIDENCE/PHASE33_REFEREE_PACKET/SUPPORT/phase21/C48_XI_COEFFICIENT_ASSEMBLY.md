# C48 sectorial xi-coefficient assembly

Date: 2026-08-17

Status: self-contained paper proof completing `C48-GORTTW-SECTOR` at internal
paper-proof level; exact symbolic regression included; separated Kimi K3
analytic AI pre-review gate passed with no P0/P1/P2. No human or peer review is
claimed.

## 1. Statement

Use the direct-xi Jensen moments

\[
 \xi(1/2+w)=\sum_{M\ge0}\frac{\gamma_H(M)}{M!}w^{2M}.
\]

Let `N=2M-2`, and let `L_N,K_N` be the sectorial saddle quantities from
Lemma S.  Define

\[
 \mathcal G(M)=
 \frac{e^{M-2}M^{M+1/2}L_N^N}
      {2^{2M-2}N^{N+1/2}}
 \sqrt{\frac{2\pi}{K_N}}
 \exp\!\left(\frac{L_N}{4}-\frac{N}{L_N}+\frac34\right).
\tag{1}
\]

> **Theorem 21B (`C48-GORTTW-SECTOR`).**
> With `theta_0=1/400` and `theta_1=1/200`, there are `R,C>0` such that
> `\mathcal G` is holomorphic and nonzero on
> \[
> |M|>R,\qquad |\arg M|<\theta_1,
> \]
> and
> \[
> \gamma_H(M)=\mathcal G(M)(1+\mathcal E(M)),
> \tag{2}
> \]
> where `mathcal E` is holomorphic there and, on the closed inner sector,
> \[
> |\mathcal E(M)|\le C\frac{\log|M|}{|M|}
> \le C|M|^{-3/4}.
> \tag{3}
> \]

All logarithms, powers, and square roots are continued from the positive real
axis.  Equation (3) is the precise fixed-epsilon instance required by the
Phase-20 Holland-interface reconstruction.
The shrink from Lemma 21A's `1/100` sector ensures that
`N=2M-2` remains in that leading-mode sector uniformly after increasing `R`.

## 2. Exact coefficient identity

The factor-eight-corrected identity proved in Milestone 1 is

\[
 \gamma_H(M)=\frac{\Gamma(M+1)}{\Gamma(2M+1)}\,2^{-2M-2}
 \left(32{2M\choose2}F(2M-2)-F(2M)\right).
\tag{4}
\]

Since `N=2M-2`,

\[
 32{2M\choose2}=16(N+2)(N+1).
\tag{5}
\]

The identity is holomorphic for `Re M>1`, and therefore throughout every
sufficiently remote sector used below.

## 3. A two-step moment ratio

Write the auxiliary-moment main term from the preceding two Phase-21 notes as

\[
 \mathcal A(s)=\sqrt{\frac{2\pi}{K_s}}L_s^s
 \exp\!\left(\frac{L_s}{4}-\frac{s}{L_s}+\frac34\right).
\tag{6}
\]

They prove

\[
 F(s)=\mathcal A(s)
 \left(1+O\!\left(\frac{\log|s|}{|s|}\right)\right)
\tag{7}
\]

uniformly on a fixed sector.

Choose the holomorphic logarithm

\[
 a(s)=\Log\mathcal A(s)
 =\tfrac12\log(2\pi)-\tfrac12\Log K_s+s\Log L_s
  +L_s/4-s/L_s+3/4.
\]

The exact derivative `L_s'=1/(L_sK_s)` gives

\[
\begin{aligned}
 a'(s)
 &=-\frac12\frac{K_s'}{K_s}+\Log L_s+\frac{sL_s'}{L_s}
   +\frac{L_s'}4-\frac1{L_s}+\frac{sL_s'}{L_s^2}\\
 &=\Log L_s+\frac1{L_sK_s}-\frac12\frac{K_s'}{K_s}.
\end{aligned}
\tag{8}
\]

The cancellation in the second line is exact: the coefficient of `L_s'` in
the first line is `K_s+1`.

From

\[
 K_s=\frac{s}{L_s}\left(1+\frac1{L_s}-\frac{3L_s}{4s}\right)
\]

and the saddle geometry,

\[
 \frac1{L_sK_s}=O(1/s),
 \qquad
 \frac{K_s'}{K_s}=O(1/s).
\tag{9}
\]

The line segment from `N` to `N+2` stays inside a slightly larger sector for
large `N`; moreover `L_{N+z}=L_N(1+O(1/N))` uniformly for `0<=z<=2`.
Integrating (8) gives

\[
 \frac{\mathcal A(N+2)}{\mathcal A(N)}
 =L_N^2(1+O(1/N)).
\tag{10}
\]

Combining (7) and (10),

\[
 \frac{F(N+2)}{F(N)}
 =L_N^2\left(1+O\!\left(\frac{\log|N|}{|N|}\right)\right).
\tag{11}
\]

In particular,

\[
 \frac{F(N+2)}{16(N+2)(N+1)F(N)}
 =O\!\left(\frac{(\log|N|)^2}{|N|^2}\right).
\tag{12}
\]

The already-established relative error `<1/2` also shows that `F(N)` is
nonzero throughout the remote sector, so the quotients above are legitimate.

## 4. Sectorial Stirling and the elementary correction

Uniform Stirling on a fixed sector strictly inside the slit plane gives

\[
 \frac{\Gamma(M+1)}{\Gamma(2M+1)}
 =\frac{e^M M^{M+1/2}}{(2M)^{2M+1/2}}
  (1+O(1/M)).
\tag{13}
\]

Define the exact prefactor multiplying `F(N)` in the leading term of (4):

\[
 P(M):=\frac{\Gamma(M+1)}{\Gamma(2M+1)}
       2^{-2M-2}\,16(N+2)(N+1).
\tag{14}
\]

Equations (13)--(14) imply

\[
 P(M)=\frac{e^{M-2}M^{M+1/2}}
              {2^{2M-2}N^{N+1/2}}
       R_N(1+O(1/M)),
\tag{15}
\]

where

\[
 R_N=e^2\frac{(N+1)N^{N+1/2}}{(N+2)^{N+3/2}}.
\tag{16}
\]

On the declared branches,

\[
 \Log R_N
 =2+\Log(1+1/N)-(N+3/2)\Log(1+2/N)
 =-\frac1{6N^2}+O(1/N^3).
\tag{17}
\]

Therefore `R_N=1+O(1/N^2)`, and (15) has the same form with `R_N` absorbed
into the error.

## 5. Assembly

Factor (4) using (5):

\[
 \gamma_H(M)=P(M)F(N)
 \left(1-\frac{F(N+2)}{16(N+2)(N+1)F(N)}\right).
\tag{18}
\]

Insert (7), (12), and (15)--(17).  The largest relative error is
`O(log|N|/|N|)`, and the explicit main term is exactly (1).  Since
`N=2M-2`, this proves (2)--(3).

The original coefficient identity is holomorphic, while every declared main
factor is holomorphic and nonzero on the outer sector.  Thus the relative
error in (2) is holomorphic.  Increasing `R` makes its modulus `<1/2`, which
also proves sectorial nonvanishing of `gamma_H(M)`.

## 6. What is and is not now discharged

Theorem 21B supplies the previously open analytic premise
`C48-GORTTW-SECTOR` by an internal paper proof rather than importing the terse
sentence after GORTTW (3.2).  It uses:

1. Lemma S for the saddle branch;
2. the exact Mellin and normalization reduction;
3. Lemma 21A for the leading-mode contour and localization;
4. the higher-theta suppression proof;
5. standard sectorial Stirling with its domain stated explicitly.

This promotion is provisional until the new Phase-21 chain receives the fresh
adversarial review required by the execution plan.  It does not constitute
human or peer review, and it does not by itself re-review every downstream
Holland-interface and Jensen-wedge argument.
