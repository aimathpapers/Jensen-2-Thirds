# Reconstruction of the consumed Holland sectorial saddle interface

Date: 2026-08-17
Status: paper-level derivation; its formerly external sectorial input now has
an internal Phase-21 proof and a separated analytic AI pre-review pass; not
Lean formalized, human reviewed, or peer reviewed

**Phase-21 update.**  Theorem 21B in
`../phase21/C48_XI_COEFFICIENT_ASSEMBLY.md` proves the exact input `(P4)`
directly from the xi/Mellin integral with relative error
`O(log|z|/|z|)`.  The present note is the downstream transport of that
theorem; `../phase21/C48_DOWNSTREAM_DISCHARGE.md` records the final dependency
closure.

## 1. Purpose and exact analytic input

This note reconstructs the part of Holland Proposition 4.1 used by the
candidate proof.  It does not assume Holland Proposition 4.1 or Holland
Theorem 1.1.

The analytic input is now the internally proved Theorem 21B: after replacing
the positive integer index by a complex index in a fixed closed sector of the
right half-plane, the factor-eight-corrected saddle formula holds with
relative error `O(log|M|/|M|)`.  Phase 21 proves it from the original
xi/Mellin integral, with the contour, branches, higher theta modes, and
coefficient assembly displayed.  Everything below is a derivation from that
theorem, exact identities, and standard sectorial complex analysis.

## 2. Moment normalization from definitions

Write

\[
\Xi(t)=\xi\!\left(\tfrac12+it\right)
      =\int_0^\infty\Phi(u)\cos(tu)\,du,
\qquad
M_z=\int_0^\infty\Phi(u)u^{2z}\,du.
\]

For integer `n>=0`, comparing the power series of
`xi(1/2+z)=Xi(-iz)` and `cosh(zu)` gives

\[
\gamma(n)=\frac{n!}{(2n)!}M_n.
\tag{P1}
\]

Absolute Mellin convergence in the initial half-plane and analytic
continuation give

\[
\gamma(z)=\frac{\Gamma(z+1)}{\Gamma(2z+1)}M_z
          =\frac{\sqrt\pi\,M_z}{4^z\Gamma(z+\tfrac12)}.
\tag{P2}
\]

The second equality is Legendre duplication.  This derivation fixes the local
normalization independently of Holland.

GORTTW use the coefficients associated with

\[
(4w^2-1)\Lambda(\tfrac12+w)=8\xi(\tfrac12+w).
\]

Consequently their moment-side leading expression must be divided by `8` to
match `(P1)`--`(P2)`.  The factor contributes only an additive real constant
after taking logarithms, so it does not affect any derivative or coefficient
ratio.  It is nevertheless displayed to prevent a normalization ambiguity.

## 3. The saddle branch and its denominators

Put `N=2z-2`.  The saddle `L_N` solves

\[
N=L_N\left(\pi e^{L_N}+\tfrac34\right),
\qquad
Q_N=(1+L_N)N-\tfrac34L_N^2.
\tag{P3}
\]

Lemma S in `phase18/C48_SECTORIAL_SADDLE_VARIABLE.md` proves directly, on
every fixed sector `|arg N|<=theta<pi/2` for sufficiently large `|N|`, that:

1. the branch exists, is unique and holomorphic, and agrees with the positive
   real saddle;
2. `L_N=log N-log log N-log pi+O(log log|N|/log|N|)`;
3. `|1/L_N|,|L_N/N|<=7/50`;
4. `Q_N=NL_N(1+1/L_N-3L_N/(4N))` is nonzero; and
5. `L_N'=L_N/Q_N`.

This removes Holland/GORTTW as a dependency for the saddle-variable branch
itself and puts every later logarithm and implicit derivative on an explicit
nonvanishing domain.

## 4. Transport of Theorem 21B

In the normalization `(P1)`--`(P2)`, Theorem 21B gives

\[
\begin{aligned}
\gamma(z)
={}&\frac{e^{z-2}z^{z+1/2}L_N^N}
 {2^{2z-2}N^{N+1/2}}
 \left(\frac{2\pi}{K_N}\right)^{1/2}
 \exp\!\left(\frac{L_N}{4}-\frac{N}{L_N}+\frac34\right)\\
&\times(1+\varepsilon(z)),
\end{aligned}
\tag{P4}
\]

where

\[
K_N=(L_N^{-1}+L_N^{-2})N-\tfrac34=Q_N/L_N^2,
\qquad
\varepsilon(z)=O(|z|^{-1+\varepsilon_0})
\tag{P5}
\]

uniformly on a fixed closed sector.  All powers and square roots are the
branches continued from the positive ray.  Lemma S shows that `L_N`, `Q_N`,
and therefore the leading factor in `(P4)`, are holomorphic and nonzero after
shrinking the sector and enlarging the radius.

Choose the radius so that `|epsilon(z)|<1/2`.  Then `(P4)` proves
`gamma(z)!=0`; equation `(P2)` and the nonvanishing of `Gamma` prove
`M_z!=0`.  On the simply connected smaller sector there is therefore one
branch

\[
h(z)=\log M_z
\]

that is real on the positive ray.  This establishes nonvanishing before the
logarithm is used.

## 5. Logarithmic decomposition

Take the logarithm of `(P4)`, use `K_N=Q_N/L_N^2`, substitute `(P2)`, and
apply sectorial Stirling to `Gamma(z+1/2)`.  Elementary collection gives

\[
h(z)=G_0(N)+\log\!\left(32\binom{2z}{2}\right)
      -(2z+2)\log2+c_{\rm sad}+\mathcal R(z),
\tag{P6}
\]

with

\[
G_0(N)=(N+1)\log L_N+\frac{L_N}{4}-\frac{N}{L_N}
       -\frac12\log Q_N.
\tag{P7}
\]

Here `c_sad` is a real normalization constant.  The logarithm of
`1+epsilon(z)`, the sectorial Stirling remainder, and the explicitly lower
order elementary terms combine into a holomorphic remainder satisfying

\[
\mathcal R(z)=O(|z|^{-1+\varepsilon_0}).
\tag{P8}
\]

The assertion of holomorphy is essential: it follows because `(P4)` is an
identity of holomorphic functions, its leading factor is nonzero, and the
relative error is smaller than `1/2` on the chosen sector.

## 6. Derivative remainders by proportional-disk Cauchy

Use the explicit nested closed sectors inherited from Phase 21,

\[
S_{1/800}\Subset S_{1/400}\Subset S_{1/200}.
\]

Take `delta_C=1/1000`.  For sufficiently large `z` in the smallest sector,
the disk `|zeta-z|<=delta_C|z|` lies in the middle sector and satisfies
`0.999|z|<=|zeta|<=1.001|z|`.  Cauchy's inequality applied to `(P8)` gives,
for every fixed integer `r>=0`,

\[
\mathcal R^{(r)}(z)
=O_{r,\varepsilon_0}(|z|^{-r-1+\varepsilon_0}).
\tag{P9}
\]

Thus the mechanism proves not only Holland's printed range `0<=r<=5`, but
also the order-six remainder used locally.  No analytic continuation of an
`O`-symbol is being differentiated: the proof first identifies a holomorphic
remainder and then applies Cauchy on a displayed interior disk.

## 7. Exact scope of this reconstruction

Equations `(P1)`--`(P3)` and the direct saddle-variable lemma are independent
of Holland.  Equations `(P4)`--`(P9)` now follow from the self-contained
Phase-21 saddle proof.  Neither Holland's Proposition 4.1 nor GORTTW's terse
complex-extension sentence is a logical premise.  The remaining trust
boundary is ordinary paper verification of the new contour and asymptotic
estimates; those are not Lean-formalized. A separated Kimi K3 analytic AI
pre-review passed A0--A10 with no P0/P1/P2, but this is not human or peer
review.
