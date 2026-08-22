# Phase 25 notation and normalization crosswalk

Date: 2026-08-17
Scope: every paper-facing convention whose silent reversal or rescaling could
change a theorem statement, coefficient, root sign, or source comparison

## Xi and coefficient conventions

| Object | Authoritative convention in this project | External convention or risk | Adapter/check |
|---|---|---|---|
| Completed function | `xi(s)` is Riemann's entire completed function; the centered even function is `xi(1/2+w)` | Some sources write `Xi(t)=xi(1/2+it)` | The paper works in `w`, not `t`; no unstated factor of `i` enters Jensen coefficients |
| Taylor coefficients | `xi(1/2+w)=sum_{n>=0} gamma(n) w^(2n)/n!` | GORZ's moment convention is eight times Holland/direct-xi convention | T1 displays and verifies the factor-eight identity; Phase 21 and Mathematica evidence pin the normalization |
| Moment integral | `gamma(n)=8 n!/(2n)! integral_0^infty omega(e^(2u)) e^(u/2) u^(2n) du` | The two known transcription hazards are `n! -> 2^(2n)` and `e^(u/2) -> e^u` | Manuscript equation regression evaluates the true xi coefficients independently |
| Continued moment | The complex index uses the branch and normalization fixed in Phase 21 | Printed GORTTW equations mix direct-xi and GORZ scaling | The factor eight is kept visible until logarithmic differentiation, where it cancels |

## Jensen and root conventions

| Object | Authoritative convention | External convention or risk | Adapter/check |
|---|---|---|---|
| Jensen polynomial | `J^(d,n)(X)=sum_{j=0}^d choose(d,j) gamma(n+j) X^j` | Reversed or factorial-normalized Jensen definitions occur in the literature | `JensenPolynomial.lean` specializes the conditional assembly to this exact finite sum |
| Advertised roots | `d` distinct negative real roots in the `X` variable | The comparison polynomial has positive roots in `y` | The final map is `y=-S X` with `S>0`; Lean checks positive-to-negative scaling |
| Hyperbolicity wedge | `n^2 log(n+2) >= K d^3` | Reversing the inequality or dropping the logarithm changes the theorem | Semantic exponent mutation derives `d^3/(n^2 log(n+2))` from the sixth-order scale |
| Low degree | For `d<=5`, six exact coefficient matches cover the polynomial | An argument written only for `d>=6` could omit this range | The paper separates the finite low-degree case before multiplier stability |

## Saddle and derivative conventions

| Object | Authoritative convention | External convention or risk | Adapter/check |
|---|---|---|---|
| Saddle index | `N=2x-2` and `L_N` solves `N=L_N(pi exp(L_N)+3/4)` | Omitting the chain factor changes every derivative constant | SymPy and Mathematica independently reproduce pre- and post-chain constants |
| Reduced variables | `r=1/L_N`, `sigma=L_N/N` | Reversing either ratio changes the H6 denominator | Lean proves the scaled denominator identity and exact norm margins |
| Derivative constants | Post-chain constants through order six are `(2,-2,4,-12,48)` for orders `2,...,6` | The pre-chain fifth/sixth constants are `-6,24` | Mathematica M1 and exact symbolic regressions keep both stages explicit |
| H6 denominator | `(4+4r-3sigma)^12` | Sign or scale changes can preserve superficial degree counts | Exact rational identity, 82-term/degree-13 checks, and coefficientwise majorant are all gated |
| Sector policy | Final theorem uses fixed nested sectors `theta_0=1/400`, `theta_1=1/200` | A free `theta in (0,pi/2)` would overstate constant uniformity | T5 and the manuscript explicitly freeze the two angles |

## Comparison-family conventions

| Object | Authoritative convention | External convention or risk | Adapter/check |
|---|---|---|---|
| Parameters | `A=alpha/(xe)`, `B=(t+we)/x`, `C=t/x`, `D=(1+delta e)/x` | Swapping `C,D` or losing `e` changes positivity and the nonperturbative term | Exact interval certificates prove `A>B>C>D>0` on the branch box |
| Limiting solution | `(alpha,t,w,delta)=(3,2,16/3,1/3)` | Jacobian rows/columns have appeared in different display orders | Manuscript and Mathematica M3 use analytic order `(alpha,t,w,delta)`; Lean declarations document their coordinate order |
| Hypergeometric model | `_3F_2(-d,A,C;B,D; (D/(AC)) y)` | Missing the scale `D/(AC)` invalidates the recurrence | Mathematica M2, SymPy, and Phase D Lean work use the coefficient ratio before expansion |
| Perturbation parameter | `epsilon_p=(C-D)/C`, tending to a nonzero value | Holland's old small-gap parameter is not available on this branch | The direct recurrence retains the nonperturbative term; Holland Lemma 7.3 is not used |

## Finite-free conventions

| Object | Authoritative convention | External convention or risk | Adapter/check |
|---|---|---|---|
| Polynomial orientation | The model is first written in ascending constant-term-one form | MMP/MSS use monic descending elementary-symmetric normalization | Reversal is an explicit adapter; it reciprocates positive roots and preserves logarithmic mesh |
| Root order | `lambda_1 >= ... >= lambda_d > 0` | Increasing root order reverses the displayed logarithmic-mesh ratio | The project pins MMP v3 Definition 2.16 |
| Logarithmic mesh | `lmesh(p)=min lambda_j/lambda_(j+1) >= 1` | The reverse ratio would be `<=1` and invert Proposition 2.17 | Source audit and mutation gate enforce the pinned direction |
| Maximum-root product | MSS published Theorem 1.6 supplies the consumed inequality | Holland cites a different theorem number in the published numbering | The project cites MSS Theorem 1.6 directly and uses reciprocal polynomials for the lower endpoint |
| Localization constant | `C_loc=12+8 sqrt(6)<32`; `K_pre=256` | Earlier drafts transposed `8+12 sqrt(6)` or used an invalid `K_pre=32` | Exact interval and manuscript regression gates pin both values |

## Interpolation and multiplier conventions

| Object | Authoritative convention | External convention or risk | Adapter/check |
|---|---|---|---|
| Six nodes | `0,1,2,3,4,5` | The printed stability lemma only needs five low finite differences to vanish, but the residual uses six coefficient matches | `QuotientAdapter.lean` proves all six matches; Hermite--Genocchi uses the six-node product |
| Simplex mass | `1/6!=1/720` | Losing the factorial changes the residual bound | `HermiteGenocchiCube.lean` and `HermiteGenocchiFTC.lean` independently derive the mass through nested weights; the local open-domain theorem has no free Hermite--Genocchi, Newton, or global-extension premise |
| Critical-point radius | `max_k |y^k p^(k)(y)/p(y)|^(1/k) <= K_r sqrt(Bd)` | Dropping `y^k` or inserting `1/k!` makes the Newton/Cauchy tail unrelated to the recurrence | Manuscript equation regression checks a legal concrete parameter point |
| Multiplier tolerance | The application arranges `sup |c-1|<=1`; the finite lemma permits `<16` | Replacing the application bound by the lemma ceiling would weaken later estimates | Paper and Lean distinguish the constructed `1` from the abstract `16` |

## Review-language convention

All separated reports, Mathematica work, and adversarial recalculations are
AI-assisted evidence. They are not human or peer review. The repository never
calls them human review or peer review. A future human report may be added only as a separately identified
artifact supplied by an actual human reviewer.
