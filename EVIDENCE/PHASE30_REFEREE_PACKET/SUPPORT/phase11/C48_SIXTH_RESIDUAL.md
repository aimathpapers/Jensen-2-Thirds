# C48 sixth saddle derivative and residual multiplier

Date: 2026-08-15  
Status: historical derivation repaired and superseded analytically by
`phase18/C48_COMPLEX_SIXTH_SADDLE.md`; independent human review pending

## 1. Sixth saddle derivative

With the notation of Phases 9--10, exact implicit differentiation of
Holland's saddle main term gives

\[
N^5L_NG_0^{(6)}(N)
=\frac{
24r^8+216r^7+864r^6+2016r^5+3024r^4
+2399r^3+1042r^2+242r+24
}{(1+r)^9}+O(\sigma),
\]

where `r=1/L_N` and `sigma=L_N/N`.  Therefore the normalized main coefficient
is `24`.  The substitution `N=2x-2` contributes the chain-rule ratio
`2^6/2^5=2`, so

\[
h^{(6)}(x)=\frac{48}{x^5\mathcal L_x}
\left(1+O(\mathcal L_x^{-1})\right).
\tag{H6}
\]

Only the bound `h^(6)(x+w)=O(1/(x^5 log x))` is needed below.

The exact main-term producer is
[`sixth_saddle.py`](../c48_jensen/symbolic/sixth_saddle.py), with frozen
artifact
[`sixth_saddle.json`](../c48_jensen/symbolic/sixth_saddle.json), SHA-256

`1d8fdc048c9f8ff0ec0991fca620fb813c35c4df2a478542f70588f0eaa80c27`.

## 2. Order-six sectorial repair

Holland states Proposition 4.1 for remainder derivatives `0<=r<=5`, the
range required in that paper.  The original version of this section sketched
an extension but did not prove the complex-uniform main-term estimate that the
residual argument consumes.  Phase 18 now supplies the complete repair in
[`C48_COMPLEX_SIXTH_SADDLE.md`](../phase18/C48_COMPLEX_SIXTH_SADDLE.md): it
chooses nested sectors and proves the Cauchy estimate

\[
\mathcal R^{(m)}(z)=O(|z|^{-m-1+\epsilon_0}).
\]

at `m=6`; identifies the exact reduced denominator
`(4+4/L_N-3L_N/N)^12` in the normalized sixth derivative of `G_0`; proves it
is uniformly separated from zero; treats the explicit normalization; and
connects the actual thickened interpolation domain to Holland's nonvanishing
sector.  The resulting theorem is

\[
|h^{(6)}(x+w)|\le C/(x^5\log x),\qquad |w|\le\eta x.
\]

The Phase-18 proof, not the old "same argument" sentence, is the dependency
used below.

This is an extension of the proof of the published proposition, not a claim
that the proposition as printed already states `r=6`.

## 3. Sixth derivative of the coefficient residual

Let `E_F(z)` be Holland's logarithmic ratio (82), now using the Phase-10
parameters that match normalized coefficients through `R_5`.  With
`b=n+1/2`, six differentiations give

\[
\begin{aligned}
E_F^{(6)}(z)=&\ h^{(6)}(n+z)
+\psi^{(5)}(B+z)-\psi^{(5)}(b+z)-\psi^{(5)}(A+z)\\
&+\psi^{(5)}(D+z)-\psi^{(5)}(C+z).
\end{aligned}
\]

Regroup the finite-boundary terms as

\[
[\psi^{(5)}(B+z)-\psi^{(5)}(C+z)]
+[\psi^{(5)}(D+z)-\psi^{(5)}(b+z)]
-\psi^{(5)}(A+z).
\]

The parameter branch gives

\[
B-C=O(n/\mathcal L_n),\quad
D-b=O(n/\mathcal L_n),\quad
A\asymp n\mathcal L_n,
\]

while `B,C,D,b` are all comparable to `n`.  The absolutely convergent
polygamma series gives `psi^(6)(z)=O(n^-6)` when `Re z >= c n`.  Phase 18
checks that the straight complex segments joining the paired boundaries stay
in that half-plane and contain no poles.  The complex line-integral formula
therefore bounds both bracketed differences by
`O(1/(n^5 L_n))`; the remote `A` term is smaller.  Together with (H6),

\[
\sup_{\Omega_F}|E_F^{(6)}|
\ll\frac1{n^5\log(n+2)}.
\tag{R6}
\]

The proposed wedge has `d=o(n)` and radius `r_F asymp sqrt(nd)=o(n)`, so all
arguments remain in the common sector and away from polygamma poles.

## 4. Six zeros give the new defect exponent

Exact matching through `R_5` gives

\[
E_F(0)=E_F(1)=\cdots=E_F(5)=0.
\]

The Hermite--Genocchi formula and (R6) imply

\[
|E_F(z)|\ll
\frac{|z(z-1)\cdots(z-5)|}{n^5\log(n+2)}.
\]

On Holland's thickened interval, `|z-j|=O(r_F)` and
`r_F asymp sqrt(nd)`.  Consequently

\[
\sup_{\Omega_F}|E_F|
\ll\frac{r_F^6}{n^5\log(n+2)}
\ll\frac{d^3}{n^2\log(n+2)}.
\]

Thus the multiplier is uniformly close to one whenever

\[
n^2\log(n+2)\ge Kd^3,
\]

which is precisely the proposed
`d << n^(2/3) log^(1/3)n` wedge.

## 5. Multiplier stability

Holland's Proposition 2.2 as printed assumes five matches and
`sup|c-1|<=epsilon<16`.  The application here has six matches and arranges
`epsilon<=1`, so it satisfies the printed proposition without modification.
This is the main proof path.

Independently, repeating Holland's Newton--Cauchy proof with six matches makes
the sum begin at order six and gives the stronger optional estimate

\[
\left|\frac{P(y)}{p(y)}-1\right|
\le\epsilon\sum_{k=6}^{\infty}2^{-k}
=\frac{\epsilon}{32}<1.
\]

when `epsilon<32`.  The signs at all critical points are then preserved, so
the same intermediate-value argument yields `d` distinct positive roots
before reversing the Jensen variable.  Lean checks the exact finite geometric
tail.  This variant is valid but is not described as a verbatim statement of
Holland's proposition and is not needed for the theorem.

## Trust boundary

The exact sixth main coefficient and reduced denominator are externally
reproduced under a pinned symbolic environment.  Phase 18 now displays the
sectorial remainder extension, complex main-term bound, nonvanishing/logarithm
domain, polygamma paths, and Hermite--Genocchi estimate.  These are internal
paper mathematics awaiting independent human review; they are not
Lean-formalized.

Most importantly, this phase is conditional on the comparison polynomial
still satisfying Holland's critical-point derivative ratio with
`r_F=O(sqrt(nd))`.  That is the final dominant gate.  Without it, the
multiplier estimate cannot be converted into hyperbolicity.

Primary source: [Holland, arXiv:2608.08682v1](https://arxiv.org/html/2608.08682v1),
especially Propositions 2.2 and 4.1 and Lemma 8.1.
