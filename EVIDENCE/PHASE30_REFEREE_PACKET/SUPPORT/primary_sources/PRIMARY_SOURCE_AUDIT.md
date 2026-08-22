# Phase 24 primary-source audit

Date: 2026-08-17
Status: direct source check completed for the finite-free seam; this is an
internal source-fidelity record, not human or peer review

## Scope and retrieval

The following official records and artifacts were checked directly:

| Source | Official record/artifact | Frozen result |
|---|---|---|
| J. Holland, *A new hyperbolicity wedge and a joint semicircle limit for Jensen polynomials of Riemann's xi-function* | [arXiv:2608.08682v1](https://arxiv.org/abs/2608.08682v1) | As of 2026-08-16 the record still has only v1. PDF hash is in `SOURCE_HASHES.sha256`. |
| A. Martínez-Finkelshtein, R. Morales, D. Perales (MMP), *Real roots of hypergeometric polynomials via finite free convolution* | [arXiv:2309.10970v3](https://arxiv.org/abs/2309.10970v3); [IMRN record](https://academic.oup.com/imrn/article/doi/10.1093/imrn/rnae120/7692199) | v3 PDF and source were hash-frozen. The journal record is volume 2024, issue 16, 11642--11687. The paywalled journal PDF was not downloaded or byte-compared. |
| A. Marcus, D. Spielman, N. Srivastava (MSS), *Finite free convolutions of polynomials* | [publisher record and open PDF](https://link.springer.com/article/10.1007/s00440-021-01105-w); [arXiv:1504.00350v2](https://arxiv.org/abs/1504.00350v2) | The open-access publisher PDF and arXiv v2 PDF/source were hash-frozen. |
| Griffin--Ono--Rolen--Thorner--Tripp--Wagner (GORTTW), *Jensen polynomials for the Riemann xi-function* | [arXiv:1910.01227v3](https://arxiv.org/abs/1910.01227v3) | Existing frozen PDF hash rechecked; the complex extension is a comparison target, not a premise after Phase 21. |

The downloaded binaries remain outside the repository. This audit records
their SHA-256 values rather than redistributing them.

## MMP proposition check

The arXiv v3 PDF pages 11--15 and the corresponding TeX source were checked.
The propositions have the following exact scope.

1. **Proposition 2.7(iii).** If both inputs belong to
   `P_n(R_{>=0})`, their degree-`n` multiplicative finite-free convolution
   belongs to `P(R_{>=0})`. Applied here, both reversed Jacobi factors have
   full degree `d` and strictly positive roots, so the hypotheses hold.
2. **Proposition 2.11.** For full-degree real-rooted `p`, `p_tilde`, and
   `q`, the implication `p interlaces p_tilde` is preserved by additive
   convolution when `q` is real-rooted and by multiplicative convolution
   when `q` is nonnegative-rooted. This is the corrected v3 statement.
   It is useful for Holland's ordered refinement but is not needed for the
   candidate's coarse interval lemma.
3. **Definition 2.16 and Proposition 2.17 (convention pinned).** Order the
   positive roots as `lambda_1 >= ... >= lambda_n > 0` and define
   `lmesh(p) = min_{1 <= i < n} lambda_i/lambda_(i+1)`, so `lmesh >= 1`.
   Proposition 2.17 then states exactly that for positive-rooted inputs,
   `lmesh(p boxtimes q) >= lmesh(p)`. The first Jacobi factor has distinct
   positive roots, hence logarithmic mesh strictly greater than one; the
   convolution therefore has distinct positive roots. Its constant term is
   one, so no zero can occur at the origin. This statement and direction were
   rechecked on page 15 of the official arXiv v3 PDF after the separated
   algebraic AI review flagged the convention ambiguity.

The v3 arXiv record says that Proposition 2.11 and the proof of Proposition
2.10 were corrected. Direct comparison with v2 confirms that this matters:
v2 stated a malformed/overbroad two-sided proposition and referred its proof
elsewhere; v3 gives a full-degree one-input preservation statement and a
proof using Propositions 2.7 and 2.10. The candidate therefore pins **v3**,
not an unversioned MMP citation.

## MSS interval check and citation correction

The publisher PDF, page 810, states Theorem 1.6: for polynomials with only
nonnegative real roots, multiplicative convolution preserves that property
and

```text
maxroot(p x_d q) <= maxroot(p) maxroot(q).
```

This is the exact external fact needed for the candidate's interval lemma.
For a polynomial with nonzero constant term set

```text
p^vee(x) = x^d p(1/x) / p(0).
```

The coefficient identity `(p boxtimes_d q)^vee = p^vee x_d q^vee`
and MSS Theorem 1.6 give the lower endpoint after reciprocation; applying the
same maximum-root inequality in the original orientation gives the upper
endpoint. Thus roots in positive intervals `[u_-,u_+]` and `[v_-,v_+]`
produce roots in `[u_-v_-,u_+v_+]`.

Holland Lemma 7.1 cites MSS Theorem 1.13 at this point. In the published MSS
version, Theorem 1.13 is the stronger S-transform inequality, whereas the
displayed largest-root product inequality is Theorem 1.6. Holland's lemma is
mathematically supported, but the candidate cites **MSS Theorem 1.6**
directly and reproduces the reciprocal-polynomial argument. No correctness
claim in the candidate depends on Holland's theorem-number citation.

## Normalization and orientation

MMP and MSS use the descending elementary-symmetric normalization. The
comparison identity in Phase 16 is first displayed in ascending,
constant-term-one normalization. Reversal converts it to the cited monic
descending convolution. Reversal reciprocates positive roots, reverses the
ordered endpoints, and preserves logarithmic mesh. The coefficient identity
also shows that multiplicative convolution commutes with reversal, so this is
a normalization adapter, not an extra mathematical assumption.

## Disposition

The unchecked-primary-source item in Phase 23 is closed at the level of a
direct AI-assisted source audit. This does **not** constitute human review,
peer review, or independent expert certification. The MMP journal PDF is
still not byte-compared with arXiv v3 because it was not openly retrievable;
every use of the published record is therefore paired with the accessible,
hash-pinned v3 preprint as the source for exact proposition text.
