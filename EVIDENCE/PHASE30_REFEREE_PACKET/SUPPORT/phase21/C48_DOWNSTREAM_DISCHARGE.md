# Phase-21 discharge of the Holland-interface saddle premise

Date: 2026-08-16

Status: internal paper derivation from Theorem 21B; downstream finite Lean
assembly replay passed; fresh end-to-end adversarial review pending.

## 1. Exact replacement of the former external premise

Theorem 21B in `C48_XI_COEFFICIENT_ASSEMBLY.md` proves, with outer angle
`1/200` and closed bound angle `1/400`,

\[
 \gamma_H(z)=\mathcal G(z)(1+\mathcal E(z)),
 \qquad
 \mathcal E(z)=O(\log|z|/|z|),
\tag{1}
\]

where `\mathcal G` is exactly the factor-eight-corrected main term `(P4)` in
`phase20/HOLLAND_PROP41_REPROOF.md`.  Both `\mathcal G` and `\mathcal E` are
holomorphic on the outer sector, `\mathcal G` is nonzero, and the estimate is
uniform on an intermediate closed sector.

Thus the “complex GORTTW saddle input” in the Phase-20 note is no longer an
external assumption.  Equation (1), including its branch conventions, is now
proved directly from the xi/Mellin integral in Phase 21.

## 2. Nonvanishing and the moment logarithm

Increase the radius until `|mathcal E(z)|<1/2`.  Equation (1) then gives
`gamma_H(z) != 0`.  The exact duplication identity

\[
 \gamma_H(z)=\frac{\Gamma(z+1)}{\Gamma(2z+1)}M_z
\]

and nonvanishing of the gamma function give `M_z != 0` on the same sector.
On a simply connected smaller sector there is consequently a unique branch

\[
 h(z)=\Log M_z
\]

that is real on the sufficiently large positive axis.

## 3. Remainder derivatives

Taking the declared logarithm in (1), the new contribution to the Phase-20
remainder is

\[
 r(z)=\Log(1+\mathcal E(z)).
\]

It is holomorphic and satisfies

\[
 r(z)=O(\log|z|/|z|)
\tag{2}
\]

on the `1/400` closed sector.  Choose the center sector of angle `1/800` and
the explicit proportional radius `delta_C=1/1000`.  For sufficiently large
`z`, the disk

\[
 |\zeta-z|\le\delta_{\rm C}|z|
\]

lies in the `1/400` sector and satisfies
`0.999|z|<=|zeta|<=1.001|z|`.
Cauchy's inequality applied to (2) gives, for every fixed `j>=0`,

\[
 r^{(j)}(z)=O_j\!\left(\frac{\log|z|}{|z|^{j+1}}\right).
\tag{3}
\]

The sectorial Stirling remainder and the other lower-order terms already
treated in Phase 20 satisfy the same or stronger estimates.  In particular,

\[
 r^{(5)}(z)=O(\log|z|/|z|^6),
 \qquad
 r^{(6)}(z)=O(\log|z|/|z|^7).
\tag{4}
\]

These are negligible compared with the main fifth and sixth saddle scales
`1/(|z|^4 log|z|)` and `1/(|z|^5 log|z|)`.

## 4. Downstream consequences

Substituting (3)--(4) into the already explicit Phase-20 calculation removes
the conditional phrase “assuming `C48-GORTTW-SECTOR`” from the following
paper-level interfaces:

1. `C48-H5-SIGNED`: the real fifth derivative has leading coefficient `-12`;
2. `C48-SADDLE6`: `h^(6)(x+w)=O(1/(x^5 log x))` uniformly for
   `|w|<=x/1000`;
3. `C48-H6-RESIDUAL`: the six-match residual is
   `O(d^3/(n^2 log n))` on the interpolation domain;
4. nonvanishing and the single logarithm branch on `n+Omega`.

No new finite algebra is introduced here.  The existing conditional Lean
theorem remains a faithful firewall: it proves the Jensen conclusion from
these analytic interfaces, while the interfaces themselves remain paper
mathematics rather than Lean theorems.

## 5. Release work at the Phase-22 candidate freeze

The mathematical dependency is now internally closed, but the result is not
release-ready.  The serial Phase-20 build, axiom audit, `leanchecker`, and
symbolic regressions have passed, the manuscript/packet references have been
updated to Theorem 21B, and one proof-source candidate is frozen.  Remaining
actions are:

1. obtain fresh analytic and algebraic AI pre-reviews against that exact
   commit, explicitly disclosing that they are not human or peer review;
2. resolve every P0/P1 before the final manuscript/evidence freeze.
