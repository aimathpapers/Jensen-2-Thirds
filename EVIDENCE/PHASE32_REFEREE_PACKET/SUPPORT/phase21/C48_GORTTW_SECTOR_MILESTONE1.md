# C48-GORTTW-SECTOR, Milestone 1: exact Mellin and saddle reduction

**Status:** P21.0 complete.  This note fixes the analytic object, normalization,
branches, saddle equation, curvature, and target theorem.  By itself it does
**not** prove the sector-uniform saddle asymptotic.  Subsequent Phase-21 notes
now supply an internal paper proof of that target; fresh review remains pending.

## 1. Primary-source starting point

GORZ derive the coefficient formula from Riemann's completed-zeta integral and
analyze the real saddle to all orders.  GORTTW restate the Mellin moment and the
leading saddle formula and add only a short sentence asserting a complex
extension.  The proof below uses their exact formulas as provenance, then
rederives every identity consumed by the proposed complex proof.

Primary sources:

- Griffin--Ono--Rolen--Zagier, arXiv:1902.07321v2, especially equations
  (9)--(12) and Theorem 7.
- Griffin--Ono--Rolen--Thorner--Tripp--Wagner, arXiv:1910.01227v3, Section 3,
  especially (3.1)--(3.2).

## 2. The exact Mellin moment is holomorphic

Write

\[
 \vartheta_0(t)=\sum_{k\ge1}e^{-\pi k^2t},\qquad
 F(s)=\int_1^\infty (\log t)^s t^{-3/4}\vartheta_0(t)\,dt,
\tag{M1}
\]

where `(log t)^s=exp(s Log(log t))` and `Log(log t)` is real for `t>1`.

For a compact set `K subset {Re s>0}`, choose
`0<alpha<=Re s<=beta` and `|Im s|<=B` on `K`.  On `1<t<=2`, put
`u=log t`; the absolute value of the `m`-th `s`-derivative is bounded by a
constant times

\[
 u^\alpha(1+|\log u|^m),
\]

which is integrable at `u=0`.  On `t>=2`, the elementary bound
`vartheta_0(t)<=e^{-pi t}/(1-e^{-3pi t})` gives a constant multiple of

\[
 (\log t)^\beta(1+\log^m\log t)e^{-\pi t}.
\]

This is integrable and independent of `s in K`.  Dominated differentiation
therefore proves that `F` is holomorphic on `Re s>0` and

\[
 F^{(m)}(s)=\int_1^\infty (\log t)^s
 (\Log\log t)^m t^{-3/4}\vartheta_0(t)\,dt.
\tag{M2}
\]

The same domination and Tonelli on the positive real axis, followed by local
uniform domination for complex `s`, give

\[
 F(s)=\sum_{k\ge1}F_k(s),\qquad
 F_k(s)=\int_1^\infty(\log t)^s t^{-3/4}e^{-\pi k^2t}\,dt,
\tag{M3}
\]

locally uniformly on `Re s>0`.

## 3. Exact xi coefficient and the factor eight

Let

\[
 \Lambda(z)=\pi^{-z/2}\Gamma(z/2)\zeta(z).
\]

Riemann's integral is

\[
 \Lambda(z)=\frac1{z(z-1)}+
 \int_1^\infty\left(t^{z/2}+t^{(1-z)/2}\right)
 \vartheta_0(t)\frac{dt}{t}.
\tag{C1}
\]

For even `n>0`, differentiation at `z=1/2` yields

\[
 \Lambda^{(n)}(1/2)=-2^{n+2}n!+2^{1-n}F(n).
\tag{C2}
\]

Indeed, the two integral terms contribute
`2(1/2)^n integral (log t)^n t^{-3/4}vartheta_0(t)dt`, while direct
differentiation of `1/(z(z-1))` at `1/2` gives `-2^(n+2)n!` for even `n`.

GORZ use

\[
 8\xi(1/2+w)=(4w^2-1)\Lambda(1/2+w).
\tag{C3}
\]

If GORZ define their Jensen moments by
`(4w^2-1)Lambda(1/2+w)=sum gamma_G(n)w^(2n)/n!`, coefficient extraction
and (C2) give

\[
 \gamma_G(n)=\frac{\Gamma(n+1)}{\Gamma(2n+1)}
 \frac{32{2n\choose2}F(2n-2)-F(2n)}{2^{2n-1}}.
\tag{C4}
\]

For the direct normalization

\[
 H(w)=\xi(1/2+w)=\sum_{n\ge0}\frac{\gamma_H(n)}{n!}w^{2n},
\]

one has `gamma_H=gamma_G/8`.  Consequently the analytic continuation of the
moment factor is

\[
 M_z=2^{-2z-2}\left(32{2z\choose2}F(2z-2)-F(2z)\right),
\qquad
 \gamma_H(z)=\frac{\Gamma(z+1)}{\Gamma(2z+1)}M_z.
\tag{C5}
\]

This is the factor-eight correction that must be preserved throughout the
Holland-interface reconstruction.

## 4. First-mode saddle and curvature

For the first theta mode use the phase

\[
 \Phi_s(t)=s\Log\Log t-\frac34\Log t-\pi t.
\tag{S1}
\]

The saddle `a_s=e^{L_s}` satisfies

\[
 0=a_s\Phi_s'(a_s)=\frac{s}{L_s}-\frac34-\pi e^{L_s},
 \quad\text{or}\quad
 s=L_s(\pi e^{L_s}+3/4).
\tag{S2}
\]

In the local coordinate `t=a_s e^v`, keep the measure
`dt=a_s e^v dv` as an amplitude.  Then

\[
 -\left.\frac{d^2}{dv^2}\Phi_s(a_se^v)\right|_{v=0}
 =\frac{s}{L_s^2}+\pi e^{L_s}
 =s(1/L_s+1/L_s^2)-3/4=:K_s.
\tag{S3}
\]

Equivalently

\[
 Q_s=L_s^2K_s=(1+L_s)s-3L_s^2/4.
\tag{S4}
\]

At the saddle, the phase together with the value `a_s` of the Jacobian
amplitude is

\[
 a_s e^{\Phi_s(a_s)}=
 L_s^s\exp(L_s/4-s/L_s+3/4).
\tag{S5}
\]

Thus the predicted first-mode main term is

\[
 F_1(s)\sim \sqrt{2\pi/K_s}\,L_s^s
 \exp(L_s/4-s/L_s+3/4).
\tag{S6}
\]

This is exactly the GORZ/GORTTW form because `Q_s=L_s^2K_s`.

### Jacobian warning

If one substitutes `t=e^u` and absorbs the Jacobian `e^u` into the exponent,
the stationary point shifts.  It is legitimate to do so only after redefining
the saddle and propagating that change.  The present proof fixes the published
saddle (S2), so the Jacobian is amplitude.  This distinction is harmless on the
real axis but load-bearing in a uniform complex contour proof.

## 5. The theorem targeted here and discharged downstream

Let `0<theta_0<theta_1<pi/2`.  Lemma S supplies a branch `L_s` on an outer
sector, continued from positive real `s`, together with the necessary
nonvanishing and comparability estimates.  For `N=2M-2`, define

\[
 A_H(M)=
 \frac{e^{M-2}M^{M+1/2}L_N^N}
      {2^{2M-2}N^{N+1/2}}
 \sqrt{\frac{2\pi}{K_N}}
 \exp(L_N/4-N/L_N+3/4).
\tag{T1}
\]

The required statement is: for some `R,C`, `A_H` is holomorphic and nonzero
on `|M|>R, |arg M|<theta_1`, and there is a holomorphic `E` there with

\[
 \gamma_H(M)=A_H(M)(1+E(M)),\qquad
 |E(M)|\le C\frac{\log|M|}{|M|}\le C|M|^{-3/4}
\tag{T2}
\]

on `|arg M|<=theta_0`.

At this milestone the direct proof of (T2) still had to establish:

1. a legal, uniform contour through `e^{L_s}` with compatible logarithm branches;
2. a central Gaussian expansion with a uniform complex remainder;
3. uniform tail bounds on that contour;
4. uniform subordination of every `k>=2` theta mode;
5. uniform subordination of `F(2M)` in (C5);
6. sectorial Stirling assembly for the gamma ratio.

The subsequent leading-contour, higher-theta, xi-assembly, and downstream
discharge notes prove all six items, with the stronger first bound displayed
in (T2).  Their review evidence is AI-only; this historical milestone does not
claim human or peer review.

## 6. Machine regression

`../c48_jensen/symbolic/gorttw_mellin_milestone1.py` verifies exactly:

- (C3), including the factor eight;
- the saddle equation (S2);
- the curvature identities (S3)--(S4);
- the leading saddle value (S5).

The regression checks algebra, not the unproved analytic estimates in (T2).

The separate primary-source audit
`GORTTW_MELLIN_SOURCE_RECONSTRUCTION.md` reproduces this chain from the
official GORZ v2 and GORTTW v3 sources.  It also records two source-level
presentation defects that are harmless here but must not be copied: GORZ (11)
needs parity factors when read beyond even derivative orders, and its final
theta-ratio sentence reverses/omits factors from the intended ratio.
