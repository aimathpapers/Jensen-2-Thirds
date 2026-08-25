# Self-contained fifth-order multiplier stability

Date: 2026-08-15
Status: conventional proof reproduced; finite sign/tail core Lean checked

## Lemma

Let `d>=5`, and let

\[
p(y)=\sum_{j=0}^d p_jy^j
\]

be a real degree-`d` polynomial with `d` simple positive zeros and
`p(0)!=0`.  For `r>0`, set

\[
\Omega_r=\{z\in\mathbb C:\operatorname{dist}(z,[0,d])\le2r\}.
\]

Let `c` be holomorphic on a neighborhood of `Omega_r`.  Assume:

1. `c(0),...,c(d)` are real;
2. `c(0)=...=c(4)=1`;
3. `c(d)>0`;
4. `sup_(Omega_r)|c-1|<=epsilon<16`; and
5. at every critical point `y` of `p`,

   \[
   \left|\frac{y^kp^{(k)}(y)}{p(y)}\right|\le r^k
   \qquad(0\le k\le d).
   \tag{M1}
   \]

Define

\[
P(y)=\sum_{j=0}^dp_jc(j)y^j.
\]

Then `P` has `d` distinct positive real zeros.  Moreover the positive-root
counting functions of `p` and `P` differ by at most one at every cutoff.

This is Holland Proposition 2.2, restated with every printed hypothesis.  The
constant in Holland v1 is `16`, not `1/6`.

## Proof

Write

\[
\Delta^kc(0)=\sum_{\ell=0}^k(-1)^{k-\ell}\binom{k}{\ell}c(\ell).
\]

Substitute Newton interpolation

\[
c(j)=\sum_{k=0}^j\binom jk\Delta^kc(0)
\]

into the definition of `P` and interchange the two finite sums.  Direct
termwise differentiation of `p` identifies the inner binomial sum and gives
the exact identity

\[
P(y)=\sum_{k=0}^d\Delta^kc(0)\frac{y^kp^{(k)}(y)}{k!}.
\tag{M2}
\]

For `k>=1`, repeated use of the fundamental theorem of calculus gives

\[
\Delta^kc(0)=\int_{[0,1]^k}c^{(k)}(t_1+\cdots+t_k)
\,dt_1\cdots dt_k.
\tag{M3}
\]

For every `rho<2r`, the closed disk of radius `rho` about any point of
`[0,d]` lies in the neighborhood on which `|c-1|<=epsilon`.  Cauchy's
estimate applied to `c-1`, followed by `rho` increasing to `2r`, gives

\[
\frac{|\Delta^kc(0)|}{k!}\le\frac{\varepsilon}{(2r)^k}.
\tag{M4}
\]

The five exact matches give

\[
\Delta^0c(0)=1,
\qquad
\Delta^kc(0)=0\quad(1\le k\le4).
\tag{M5}
\]

Let `y` be a critical point of `p`.  Since `p` has only simple roots,
`p(y)!=0`.  Equations `(M1)`--`(M5)` imply

\[
\left|\frac{P(y)}{p(y)}-1\right|
\le\varepsilon\sum_{k=5}^d2^{-k}
<\frac{\varepsilon}{16}<1.
\tag{M6}
\]

Hence `P(y)` and `p(y)` have the same sign at every critical point.  They
also have the same sign at zero because `c(0)=1`, and the same sign for large
positive `y` because `c(d)>0`.  The signs of a real polynomial with `d`
simple positive roots alternate at zero, its `d-1` critical points, and
positive infinity.  The intermediate value theorem therefore puts a
sign-changing zero of `P` in each of the `d` intervening intervals.  The
intervals are disjoint; since `P` has degree `d`, these zeros exhaust its
degree and are all simple and positive.

The critical points strictly interlace the zeros of `p`, so `p` also has one
zero in every such interval.  Below an arbitrary cutoff `t`, the two counts
agree on completed intervals and can differ only inside the one interval
containing `t`.  Their difference is therefore at most one.  This proves the
lemma.

## Six-match specialization used locally

The candidate multiplier satisfies the stronger conditions

\[
c(0)=\cdots=c(5)=1,
\qquad
\sup_{\Omega_r}|c-1|\le1<16.
\]

It consequently invokes the preceding lemma unchanged.  Independently, the
extra match moves the geometric tail to order six and gives the sufficient
bound `epsilon<32`; that refinement is supplementary and is not attributed
to Holland.

## Lean boundary

`Zeta23.Research.JensenWedge.MultiplierStability` checks:

- the exact order-five finite geometric tail and reciprocal constant `16`;
- termwise-to-total relative-error control;
- preservation of sign under relative error less than one; and
- construction of distinct roots from separated sign-changing intervals.

`Zeta23.Research.JensenWedge.ConditionalAssembly` then checks the positive-to-
negative scaling and the final conditional theorem.  The complex Cauchy
estimate `(M4)`, polynomial critical-point interlacing, and the construction
of the concrete xi certificate remain conventional-analysis inputs.  No Lean
axiom is declared for them.
