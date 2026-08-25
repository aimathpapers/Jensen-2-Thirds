# Sixth-order stability and internal theorem assembly

Date: 2026-08-15  
Status: self-contained internal paper proof; **not peer reviewed**

## 1. Internal theorem

There is an absolute constant `K>0` such that, for all integers `n>=0` and
`d>=1`,

\[
n^2\log(n+2)\ge Kd^3
\quad\Longrightarrow\quad
J^{d,n}(X)\text{ has }d\text{ distinct negative real zeros}.
\tag{T}
\]

Equivalently, the unconditional hyperbolicity wedge for the Jensen
polynomials of the xi coefficients extends internally to

\[
d\ll n^{2/3}\log^{1/3}(n+2).
\]

The word *internally* is essential: the analytic and special-function steps
have only AI pre-review.  Phase 21 now proves the formerly imported sectorial
GORTTW-type estimate directly from the xi/Mellin integral; this is an internal
paper proof, not human or peer review.

## 2. Sixth logarithmic residual

Let `E_F(z)` be the exact logarithm of the xi/model coefficient ratio on the
Phase-15 branch.  It is the function displayed in Phase 11 and satisfies

\[
E_F(0)=E_F(1)=\cdots=E_F(5)=0.
\tag{Z6}
\]

The equality follows from exact matching of `R_0,...,R_5` and the real
logarithm of positive coefficient ratios.

Let

\[
\rho=K_r\sqrt{Bd},\qquad
\Omega=\{z\in\mathbb C:\operatorname{dist}(z,[0,d])\le2\rho\}.
\]

The wedge gives `d=o(n)` and `rho=o(n)`, so all gamma arguments have real
part comparable to `n`, while `n+Omega` stays in the fixed saddle sector.

Six differentiations give

\[
\begin{aligned}
E_F^{(6)}(z)=&\ h^{(6)}(n+z)
+\psi^{(5)}(B+z)-\psi^{(5)}(n+1/2+z)-\psi^{(5)}(A+z)\\
&+\psi^{(5)}(D+z)-\psi^{(5)}(C+z).
\end{aligned}
\tag{E6}
\]

The repaired Phase-18 uniform complex sixth-saddle lemma, using the direct
Phase-21 sector theorem,

\[
h^{(6)}(n+z)=O((n^5\log n)^{-1})
\]

uniformly on this domain and explicitly proves that `M_(n+z)` is nonzero on
one compatible logarithm branch.  Pair the remaining finite boundaries as

\[
[\psi^{(5)}(B+z)-\psi^{(5)}(C+z)]
+[\psi^{(5)}(D+z)-\psi^{(5)}(n+1/2+z)]
-\psi^{(5)}(A+z).
\]

The exact branch gives

\[
B-C=O(n/\log n),\quad
D-(n+1/2)=O(n/\log n),\quad
A\asymp n\log n.
\]

On `Re z >= c n`, the polygamma series gives
`psi^(6)(z)=O(n^-6)`.  Phase 18 proves that the straight complex integration
paths remain in this half-plane and avoid every pole.  The two line integrals are therefore
`O((n^5 log n)^-1)`, and the remote `A` term is smaller.  Hence

\[
\sup_{z\in\Omega}|E_F^{(6)}(z)|
\le\frac{C}{n^5\log(n+2)}.
\tag{B6}
\]

## 3. Six zeros and the multiplier defect

The complex Hermite--Genocchi formula stated and proved in Phase 18, applied
to `(Z6)` and `(B6)`, gives

\[
|E_F(z)|\le
\frac{C}{6!\,n^5\log(n+2)}
|z(z-1)\cdots(z-5)|.
\]

The wedge gives `rho/d=K_r sqrt(B/d) -> infinity` for the already fixed
`K_r`, so `rho>=d` after increasing only the eventual threshold.  Hence every
factor on `Omega` is `O(rho)`.  Since `B` is comparable to `n`,

\[
\sup_\Omega|E_F|
\le C\frac{\rho^6}{n^5\log(n+2)}
\le C'\frac{d^3}{n^2\log(n+2)}.
\tag{Def}
\]

Let `c_F=exp(E_F)`.  The gamma and moment logarithms are taken on the
compatible branches constructed in Phase 18; exact positive coefficient
matching makes `E_F(0)=...=E_F(5)=0` rather than merely a multiple of
`2*pi*i`.  Increase the theorem constant until the right side of `(Def)` is at
most `1/2`.  Then

\[
\sup_\Omega|c_F-1|
\le2\sup_\Omega|E_F|
=:\varepsilon,
\qquad \varepsilon\le1<16.
\tag{Mult}
\]

The function is holomorphic on a neighborhood of `Omega`; its integer values
are positive real coefficient ratios; and
`c_F(0)=...=c_F(5)=1`.

## 4. Multiplier stability

Phase 20 reproduces Holland's Proposition 2.2 self-containedly.  Its printed
hypotheses are `d>=5`; all values `c(0),...,c(d)` are real;
`c(0)=...=c(4)=1`; `c(d)>0`; and
`sup_Omega|c-1|<=epsilon<16`, together with the displayed critical-point
bound.  Section 3 and Phase 18 establish every one of these conditions for
`c_F` (indeed with six matches and `epsilon<=1`).  Thus the proposition gives
`d` simple positive roots in its stated degree range.

For completeness, the following independent order-six refinement explains
the extra margin supplied by the sixth match, but the assembled theorem does
not depend on changing Holland's proposition.

Let

\[
p(y)=\sum_{j=0}^dp_jy^j
\]

have `d` simple positive roots and nonzero constant term.  Suppose `c` has
the properties in `(Mult)`, including `c(0)=...=c(5)=1` and `c(d)>0`, and
put

\[
P(y)=\sum_{j=0}^dp_jc(j)y^j.
\]

If every critical point of `p` satisfies

\[
\left|\frac{y^kp^{(k)}(y)}{p(y)}\right|\le\rho^k,
\]

then `P` has `d` simple positive roots.

To prove this, Newton interpolation gives

\[
P(y)=\sum_{k=0}^d
\Delta^kc(0)\frac{y^kp^{(k)}(y)}{k!}.
\tag{N}
\]

Repeated fundamental theorem of calculus and Cauchy's estimate on radius
`2rho` disks centered on `[0,d]` give

\[
\frac{|\Delta^kc(0)|}{k!}
\le\frac\varepsilon{(2\rho)^k}.
\tag{C}
\]

The six matching values imply `Delta^0 c(0)=1` and
`Delta^k c(0)=0` for `1<=k<=5`.  At a critical point, `(N)`--`(C)` and the
derivative-ratio bound give

\[
\left|\frac{P(y)}{p(y)}-1\right|
\le\varepsilon\sum_{k=6}^d2^{-k}
<\frac\varepsilon{32}<1.
\tag{Sign}
\]

Lean theorems `sixthOrderTail_eq` and `sixthOrderTail_lt` check the exact
finite geometric sum and its strict `1/32` cap.

Thus, under the optional weaker threshold `epsilon<32`, `P` and `p` have the
same sign at every critical point.  They also have
the same sign at zero and at positive infinity because `c(0)=1` and
`c(d)>0`.  The signs of a simple positive-rooted degree-`d` polynomial at
these endpoints and its `d-1` critical points alternate.  The intermediate
value theorem therefore places one sign-changing zero of `P` in each of the
`d` intervening intervals.  These exhaust its degree and are simple.

## 5. Application to the exact comparison

Phase 15 supplies a positive two-Jacobi comparison `p_F` matching six
coefficients.  Phase 16 supplies its critical-point derivative ratios with
`rho=K_r sqrt(Bd)`.  Sections 2--3 and the Phase-18 repair supply the
multiplier `c_F`.  Holland's printed stability theorem therefore gives `d`
simple positive roots for
the transformed Jensen polynomial whenever `d>=6` and `n` exceeds all fixed
thresholds.

For `1<=d<=5`, the exact coefficient match through `R_5` makes the transformed
Jensen polynomial equal to its positive-rooted comparison polynomial up to
the harmless positive scaling, so the same conclusion holds.

Undoing `X=-y/S`, with `S>0`, changes the simple positive `y` roots into
simple negative `X` roots.

## 6. Finite range and one absolute constant

Let `n_0` exceed the fixed thresholds used in the branch, saddle, root, and
recurrence lemmas.  Choose the theorem constant large enough for all analytic
smallness conditions above.  Increase it once more so that

\[
K>\max_{0\le n<n_0} n^2\log(n+2).
\]

For such excluded `n` and every `d>=1`, the hypothesis in `(T)` is false.
For `n>=n_0`, the preceding proof applies.  This completes the internal proof
of `(T)` with one absolute existential constant.

## 7. What this does and does not mean

If independently validated, `(T)` improves Holland's August 2026 exponent
`3/5` to `2/3` for Jensen-polynomial hyperbolicity of the xi coefficient
sequence.  It is potentially publishable progress in the Jensen-polynomial
program.

It does **not** prove the Riemann hypothesis, improve a known proportion of
zeta zeros on the critical line, or locate new zeta zeros.  The theorem's
relationship to RH remains the established Jensen-polynomial framework.

The absolute constant is existential and presently not computationally
useful.  The unweighted contraction diagnostic in Phase 18 suggests a
sufficient threshold on the scale `n approximately 10^1887` even before all
analytic constants are propagated.  This is an ineffectivity disclosure, not
a claimed explicit value of `K`.

## Trust boundary and embargo

Lean checks the finite leading system, coordinate-ordered inverse, exact
finite-difference signs, triangular equivalence, recurrence elimination and
closed coefficients, maximum contradiction, and the sixth-order geometric
tail.  Pinned symbolic calculations reproduce the saddle and recurrence
algebra.

The sectorial derivative extensions, exact `C^1` calculus, finite-free source
applications, uniform recurrence inequalities, Hermite--Genocchi step, and
sign-stability assembly are paper mathematics.  Separate analytic and
algebraic Claude Opus 5 reviews are being used because human pre-review is not
available; they are correlated AI audits from one provider/model, not human or
peer review.  Every repair must be re-reviewed, and the result remains an
internal, unrefereed proof even though Phase 21 has discharged the former
GORTTW premise internally.
