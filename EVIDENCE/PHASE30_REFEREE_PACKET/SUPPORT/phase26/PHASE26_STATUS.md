# Phase 26 status

Date: 2026-08-19
Branch: `codex/c48-phase26-formal-analytic-closure`
Required checkpoint: `5f79158f9c6276dd09142edeea279e35b0d58406`

## Current state

The approved formalization order is frozen in `PHASE26_PLAN.md`. Stage B is
complete and T1 is kernel closed. Stage C is complete and T2 is kernel closed.
Stage D is complete and T3 is kernel closed. Stage E is complete and T4 is
kernel closed on the branch-safe Mellin ray `(1,infinity)`. Stage F is
complete at the approved stronger-middle endpoint: the concrete coefficient
theorem, exact xi branch, six-coefficient comparison, finite-free
specialization, critical-point localization, and normalized critical-radius
bound are kernel checked. The final xi-specific sixth-multiplier
instantiation remains outside Phase 26, as do the typed Jacobi/MMP/MSS
literature inputs.
No human or peer review is claimed.

| Stage | Scope | Status | Concrete closure condition |
|---|---|---|---|
| A | Exact algebra and finite certificate instantiation | complete | order-six identity and bidisc certificate kernel checked; exact rational records constructed |
| B | T1 xi/theta/Mellin | complete | concrete factor-eight theorem with no `hMellin` premise |
| C | T2 sectorial saddle | complete | concrete full-sector `SectorialSaddleCertificate` |
| D | T3 leading contour | complete | uniform deformation/Gaussian certificate |
| E | T4 higher modes | complete | uniform infinite-mode suppression certificate |
| F | T5 coefficient theorem and stronger-middle downstream specialization | complete | concrete uniform relative-error theorem, exact xi branch and six matches, finite-free specialization, and normalized critical-radius bound; final xi-specific multiplier instantiation remains outside the endpoint |

## Current boundaries

- T1 is now unconditional in Lean: the completed-zeta Mellin identity,
  differentiated moments, theta modular symmetry, endpoint cancellation,
  two improper integrations by parts, even fold, and concrete factor-eight
  coefficient theorem are all kernel checked.
- T2 is unconditional in Lean on the fixed outer sector with conservative
  cutoff `log |s| > 10^6`: whole-disc contraction, unique branch, holomorphy,
  exact derivative `L/Q`, reduced boxes, and curvature are kernel checked.
- It proves Cauchy transport of a uniform holomorphic error, but does not yet
  construct that error.
- T3 has a complete kernel-checked leading-mode relative theorem. T4 controls
  the complete infinite higher-mode sum, performs the legal all-mode
  rectangular deformation, and proves the original branch-safe ray theorem
  on `(1,infinity)`. The separate T5 endpoint substage now controls the low
  interval `(0,1)` and joins it exactly to the full moment. The positive-
  integer theta-moment coefficient assembly, the two-shift relative-error
  algebra, and the exact saddle-main differential identities are also kernel
  checked. The fixed-inner-sector saddle-main ratio inequality is concrete,
  and the positive-integer factorial quotient is its traditional Holland
  elementary main times `1 + error`, with `|error| <= 1/(4M)`. This is the
  integer-axis normalization anchor. The complex-sector Gamma quotient used
  by Theorem 7.1 is now also its traditional elementary main times `1+error`,
  with `|error| <= 1/|M|` on the fixed coefficient sector. Its exact complex
  continuation and agreement with every positive-integer centered-xi
  coefficient are kernel checked. The actual continuation, nonzero factored
  main, and explicit relative error are now proved holomorphic on the open
  paired coefficient sector. The full theta moment is identified with a
  Mellin transform and differentiated from explicit endpoint bounds. The
  derivative estimate underlying the Gamma transport is kernel checked at
  every point of the remote right half-plane, including positive integers.
  The factored main is now identified exactly with the manuscript's displayed
  main times three explicit correction factors. Their product is now proved
  within `20 log|N|/|N|` of one. The relative error and holomorphy have now
  been transferred to the displayed main with a concrete constant. The
  Proportional-disc order-six Cauchy transport is now instantiated with
  the paper's radius `x/1000`. The concrete real xi coefficient sequence and
  Jensen target are now connected to the typed final theorem. The exact lower
  saddle tower through order five and the local-FTC adapter for its four
  finite differences are now kernel checked. The active seam is the rigorous
  interval instantiation of the separately exposed saddle and explicit-main
  correction budgets, followed by the finite-`n,d` parameter branch and
  comparison-root inputs; no `ExactXiSaddleIntervalCertificate` is claimed
  from an unfilled structure.
- The final root theorem remains conditional on typed xi analytic inputs and
  on explicitly disclosed classical Jacobi/MMP/MSS inputs.

## Verification record

The branch was created from
`125d36d5b4519178f31b4d37cdf63a70c603be7e`, whose hosted verification
passed. The Phase 25/24/21/20 serial baseline was already green before this
branch was opened. The Phase 26 verifier covers completed Stages A--E and
every frozen T5 submilestone documented below, including the exact
manuscript-main bridge, correction bounds, and holomorphic displayed-main
coefficient theorem. No downstream order-six root-theorem instantiation is
claimed yet.

### Stage A1 submilestone

`SaddleOrderSix.lean` now contains the full 82-term integer numerator and a
generic coefficientwise theorem for complex bidiscs. Lean checks:

- 82 terms and total degree exactly thirteen;
- the exact numerator majorant;
- the exact denominator lower bound `(151/50)^12`;
- the exact quotient
  `6422139805764931584036533551104 /
   702576099728137594188684005`; and
- the strict whole-bidisc conclusion `|H6| < 10000`.

The source-to-Lean verifier independently reconstructs the sixth derivative
from `G0` and the implicit saddle differential operator before comparing all
coefficients. Stage A remains in progress because the formal differential
recurrence and the remaining concrete finite constructors are not yet frozen.

### Stage A2 finite-constructor submilestone

`CanonicalCertificates.lean` now constructs:

- one `SaddleFiniteCertificate` from the exact bidisc hypotheses;
- the four leading residuals in the fixed `(alpha,t,w,delta)` order;
- a concrete, locally unique `PositiveParameterBranch` for the limiting
  four-equation system;
- the center-residual interval certificate for that limiting system; and
- `RadiusThresholdStage` with exact values `K_r=4096`, `C0=48`, `C1=96`.

This does not construct the xi-perturbed center-residual or whole-box
Jacobian-defect certificate. Those remain explicitly analytic and cannot be
filled by the limiting algebra.

### Stage A recurrence closure

`SaddleOrderSixAlgebra.lean` evaluates the exact reduced numerator recurrence
in a bounded integer-polynomial representation. Starting from the explicit
15-term order-two numerator, kernel reduction proves the transitions to the
28-term order-three, 43-term order-four, 61-term order-five, and frozen
82-term order-six numerators. These proofs use no native-decision axiom.

The identification of the order-two starting table with the displayed `G0`
is independently definition-reconstructed by SymPy and the user-executed
Mathematica notebook. The Lean contribution closes all subsequent formal
differentiation and the full bidisc inequality. This is recorded as exact
algebra plus independent base-expression corroboration, not as a formalized
sectorial asymptotic theorem.

Stage A is complete. Stage B (T1) is now active; T1 remains amber until the
concrete theta/Mellin premise is constructed in Lean.

### Stage B1 concrete Mellin seam

`XiMellin.lean` now exposes Mathlib's actual modified Riemann theta kernel and
proves, without a caller-supplied hypothesis,

`completedRiemannZeta₀ s = mellin riemannThetaModifiedKernel (s / 2) / 2`.

It also kernel-checks both pointwise branches of the piecewise modification,
local integrability, rapid decay at zero and infinity, and the exact
weight-one-half modular symmetry. This removes the abstract Mellin seam, but
does not yet prove the differentiated moment identity or the paper's
integration-by-parts conversion to `omega`; therefore T1 remains in progress.

### Stage B2 differentiated Mellin moments

`MellinLogMoments.lean` proves an all-orders dominated-differentiation
theorem. For any locally integrable complex kernel with faster-than-power
decay at both endpoints, the `n`th derivative of its Mellin transform is the
Mellin transform of `(log t)^n` times that kernel. The proof re-establishes
local integrability and endpoint majorants after every logarithmic weight and
then invokes Mathlib's derivative-under-the-Mellin-integral theorem.

The result is instantiated with `riemannThetaModifiedKernel`, including the
exact `s/2` chain-rule factor for every derivative of
`completedRiemannZeta₀`. No differentiability-under-the-integral premise
remains. T1 is still in progress because the change of variables and two
integrations by parts leading to the manuscript's positive `omega` kernel
have not yet been kernel checked.

### Stage B3 theta/omega change-of-variables seam

`ThetaOmega.lean` and `XiOmegaIntegral.lean` now kernel-check the exact
normalizations on both sides of the remaining integration-by-parts step:

- the manuscript theta tail is identified with Mathlib's Jacobi-theta
  series and proved twice continuously differentiable on `t > 0`;
- the first and second logarithmic chain rules are proved concretely;
- `A''(u)-A(u)/4 = 4 exp(u/2) omega(exp(2u))` has no caller-supplied
  differentiability hypotheses;
- the Mellin integral is pulled back to the whole real line exactly;
- the centered completed zeta is represented as the bilateral Laplace
  transform of an even modified-theta amplitude; and
- on the positive half-line that amplitude is exactly twice the paper's
  theta amplitude.

This closes the normalization and differential-algebra portion of T1. T1
remains in progress: the endpoint values, tail limits, half-line fold, and
two improper integrations by parts must still be kernel checked before the
factor-eight theorem can be upgraded.

### Stage B4 exact modular endpoint

The logarithmic theta functional equation is now proved directly from
Mathlib's Jacobi-theta functional equation:

`A(-u) = A(u) + (exp(u/2)-exp(-u/2))/2`.

Differentiating the concrete identity at zero yields the exact endpoint
value `A'(0)=-1/4`. This is the nonzero boundary term required to cancel the
standalone `+1/2` in the entire-xi normalization. No numerical endpoint or
external symbolic calculation is used. The remaining T1 work is the
infinite-endpoint decay/integrability, half-line fold, and the improper
integration-by-parts passage.

### Stage B5 differentiated theta series

`ThetaOmegaDecay.lean` now justifies both differentiations of the one-sided
theta series with explicit summable majorants on a positive neighborhood of
each evaluation point. Lean proves:

- `Theta'` is the sum of the first differentiated modes;
- `Theta''` is the sum of the second differentiated modes;
- both differentiated series are summable for every positive argument;
- `omega` is exactly the convergent sum of the corresponding twice-
  differentiated omega modes; and
- the first derivative of `A(u)` has an exact expression through the first
  differentiated theta series.

No exchange of an infinite sum and derivative is left implicit. T1 remains
in progress while these series majorants are upgraded to the required
weighted integrability and zero-limit statements at `+infinity`.

### Stage B6 uniform differentiated-tail bounds

The differentiated theta modes now have one exact, all-orders majorant.
For every natural `k`, Lean proves that the positive mode sum weighted by
`(n+1)^k` is `O(exp(-pi*t/2))` as `t -> +infinity`.  The first and second
differentiated theta tails are then identified algebraically with the
`k=2` and `k=4` instances, including the exact factors `-pi` and `pi^2`.

This converts the local termwise-differentiation results into uniform tail
control without numerical sampling.  T1 remains in progress while the
bound is transported through `t=exp u` to weighted integrability and
boundary limits for the two improper integrations by parts.

### Stage B7 logarithmic transport, integrability, and endpoint decay

The uniform mode estimates are now transported through `t=exp(2u)`.  Lean
proves exact positive-mode formulas for `A''`, global `C^2` regularity of
the logarithmic theta amplitude, and `O(exp(-u))` bounds for `A`, `A'`, and
`A''`.  A generic kernel theorem then proves, for every natural `m`, both
integrability of `u^m A`, `u^m A'`, and `u^m A''` on `(0,infinity)` and the
zero limits of the weighted `A` and `A'` boundary terms at infinity.

All estimates are symbolic and uniform; no finite grid or numerical
threshold is used.  The hypotheses of the two improper integrations by
parts are now available in Lean.  T1 remains in progress until those
integrations, the even half-line fold, and the coefficient extraction are
assembled into the unconditional factor-eight theorem.

### Stage B8 exact improper integrations by parts

`ThetaOmegaMoments.lean` now performs the two improper integrations by
parts with no packaged endpoint assumption.  Lean checks every derivative,
weighted integrability condition, right-hand endpoint, and infinite-endpoint
limit.  It obtains the exact degree-zero boundary contribution

`integral_0^infinity A''(u) du = 1/4`

from `A'(0)=-1/4`, and for every natural `m` proves

`integral u^(m+2) A'' = (m+2)(m+1) integral u^m A`.

The omega amplitude is simultaneously identified with
`(A''-A/4)/4` and proved integrable under every polynomial weight.  T1
remains in progress only for the even full-line fold and the final
centered-xi coefficient assembly.

### Stage B9 full-line moment and even fold

`XiOmegaCoefficients.lean` now transports the differentiated completed-zeta
Mellin integral to the centered logarithmic variable on the whole real line.
Lean proves a reusable integrable-even folding theorem, checks the evenness
and positive-half-line integrability of every even centered theta moment, and
deduces the exact identity

`L^(2n)(1/2) = 4 integral_0^infinity u^(2n) A(u) du`.

This closes the measure-theoretic full-line fold without symmetry or
integrability assumptions hidden outside the kernel. T1 remains in progress
only for the quadratic centered-xi prefactor and the final omega coefficient
assembly.

### Stage B10 unconditional factor-eight closure

`XiOmegaCoefficients.lean` now expands the translated entire-xi normalization
as its quadratic prefactor times the centered completed zeta. Lean checks the
full Leibniz sum, proves that only prefactor derivatives zero and two survive,
and matches those two terms exactly to the omega integrations by parts. The
degree-zero endpoint contribution cancels the standalone `+1/2` term.

The resulting theorem is unconditional:

`iteratedDeriv (2*n) centeredXi 0 = 8 * halfLineMoment omegaLogAmplitude n`.

It instantiates `centeredXiCoefficient_eq_factorEightMoment` with the concrete
omega kernel, yielding `centeredXiCoefficient_eq_omegaMoment` with no
`hMellin` premise. Stage B is complete and T1 is kernel closed. Stage C (T2)
is active; no claim about T2--T5 has been upgraded.

### Stage C1 exact saddle and honest uniqueness scope

`SectorialSaddle.lean` now defines the paper's two fixed angles, outer sector,
comparison center, exact equation
`s = L * (pi * exp L + 3/4)`, and curvature
`Q = (1+L)s - (3/4)L^2`. Lean proves the exact derivative, the identity
`L * partial_L equation = Q` at a root, and transports the existing
`|1/L|, |L/s| <= 7/50` certificate to `Q != 0`.

The generic certificate boundary was also corrected: its uniqueness field is
now quantified only over an explicit admissible moving neighbourhood, and it
requires the distinguished branch to belong to that neighbourhood. This is
the scope proved by the paper's Rouche/contraction argument; global uniqueness
of all roots of the transcendental equation is neither true nor claimed.
Existence, whole-neighbourhood contraction, and holomorphic patching remain
open, so T2 remains in progress.

### Stage C2 uniform contraction-to-branch constructor

`SectorialSaddle.lean` now defines the equation-normalized Newton map
`T_s(L) = L - F_s(L)/s` and proves, for `s != 0`, that its fixed points are
exactly the roots of the saddle equation. Its exact complex derivative is
kernel checked.

The new `SaddleContractionFamily` interface requires a nonnegative radius,
whole-closed-disc self-mapping, and a genuine uniform `ContractingWith`
certificate at every parameter. Banach's theorem then constructs a selected
branch and proves its disc membership, saddle equation, and uniqueness among
all roots in that disc. No existence or uniqueness premise is left in the
selected-branch theorems beyond the explicit whole-disc estimates in the
family record. The next substage must instantiate those estimates on the
fixed outer sector and then prove holomorphic patching; T2 is not yet closed.

### Stage C3 concrete quantitative Newton discs

`SaddleQuantitativeInput` isolates four normalized inequalities: a lower
bound for `|Log s|`, a one-percent logarithmic correction, and small bounds
for `|L0/s|` and `|1/s|`. From only those fields, Lean now proves:

- the exact comparison-center exponential and normalized-residual identities;
- `|F_s(L0)/s| <= 11/1000`;
- the exact derivative decomposition on the entire radius-`1/20` disc;
- `|T_s'(L)| <= 1/4` at every point of that disc;
- whole-disc Lipschitz contraction and self-mapping;
- a unique selected saddle root in the disc;
- the stronger branch boxes `|1/L|, |L/s| <= 7/50`; and
- nonvanishing of the exact curvature denominator on the selected branch.

At this submilestone the Banach and finite-box parts were instantiated, rather
than merely generic adapters; the remaining sector and patching work is closed
in C4 below.

### Stage C4 full-sector and holomorphic T2 closure

Lean now derives all four `SaddleQuantitativeInput` inequalities from the
actual fixed outer sector `|arg s| < 1/200`, using the explicit conservative
cutoff `log |s| > 10^6`. It proves the sector open, proves continuity of the
logarithmic comparison center, and sharpens the selected root from closed-disc
membership to strict interior membership.

At each saddle, the complex inverse-function theorem supplies a local inverse
of `L |-> L(pi exp L + 3/4)`. Strict interior membership plus the whole-disc
uniqueness theorem identifies that local inverse with the selected Banach
branch on overlaps. Lean therefore proves the branch holomorphic and checks
the exact implicit derivative `L/Q`. The concrete
`leanSectorialSaddleCertificate` supplies branch membership, differentiability,
the saddle equation, local uniqueness, and curvature nonvanishing without an
analytic premise. Stage C is complete and T2 is kernel closed; Stage D (T3) is
active. The smaller paper threshold remains supported by the existing exact
and Arb/ACB evidence but is not needed for the eventual theorem.

### Stage D1 exact phase, Gaussian, and legal finite rectangle

`LeadingSaddleContour.lean` now separates the published phase
`s Log u - 3u/4 - pi exp u` from the Jacobian `exp u` and proves that their
product is the exponential of `s Log u + u/4 - pi exp u`. Lean checks the
first four derivatives, the exact saddle identities `h'(L)=1` and
`h''(L)=-K`, the saddle value, and `K=Q/L^2`.

The actual contour coordinate is definitionally horizontal, `L+r`; a named
seam identifies the top rectangle side at height `Im L` with that coordinate.
The full complex Gaussian comparison, including its linear term, is
integrable and has the exact value
`(2*pi/K)^(1/2) exp(1/(2K))` whenever `Re K>0`.

Finally, Cauchy-Goursat is instantiated on the finite rectangle with vertices
`1`, `X`, `X+i b`, and `1+i b`. All four oriented sides are named, and Lean
proves the entire rectangle lies in the fixed right half-plane before
deriving the boundary identity. This rules out both the former vertical
direction and the illegal full horizontal line at the source level. The
infinite right-side limit and quantitative central/connector/tail estimates
remain open, so Stage D and T3 remain in progress.

### Stage D2 uniform branch geometry and infinite rectangle

The fixed outer sector now supplies concrete real and imaginary bounds for
the selected saddle: `Re L > 1000` and `|Im L| < 1/20`. The latter uses the
sharpened Banach displacement `dist(L,L0) <= 11/750`, rather than treating
disc membership as if it were already strict enough. Lean also proves
directly from the normalized branch boxes that the Gaussian curvature has
positive real part.

For every translated height `|b| <= 1/20`, Lean proves absolute integrability
of the bottom and top rays. Beyond the explicit cutoff
`X >= 2(5|s|+1)+2`, the full first-mode integrand on the far side is bounded
by `exp(-X)`. Consequently the right vertical segment tends to zero. Passing
the finite Cauchy rectangle identity to the limit gives the exact infinite
identity
`bottom ray = translated ray + endpoint connector`.

This completes the deformation component without invoking an informal
infinite contour. Quantitative central localization, connector
negligibility, and the outer translated-ray tail remain open, so Stage D and
T3 remain in progress.

### Stage D3 signed Gaussian moments

`LeadingGaussianMoments.lean` proves that every polynomial moment of the
full complex Gaussian `exp(r-Kr^2/2)` is integrable when `Re K>0`. Three
whole-line integration-by-parts identities then give the first, second, and
third signed moments. In particular Lean proves the exact normalized identity

`integral(r^3 exp(r-Kr^2/2)) / integral(exp(r-Kr^2/2)) = 3/K^2 + 1/K^3`.

This kernel-checks the cancellation that makes the cubic perturbation
relative order `O(1/|K|)` after multiplication by a coefficient of size
`O(|K|)`; an absolute cubic estimate would be too weak.

### Stage D4 absolute Gaussian moments and curvature comparability

The concrete branch estimate has been sharpened to the simultaneous bounds
`1 < Re K` and `|K| <= 2 Re K`. This supplies both a fixed positive lower
bound and the comparison needed to translate real-part Gaussian decay into
the paper's `|K|` scale.

For every natural order, `LeadingGaussianMoments.lean` now proves an exact
whole-line absolute Gaussian moment in Gamma-function form and a uniform
absolute-moment upper bound for `exp(r-Kr^2/2)`. Named fourth- and sixth-order
corollaries instantiate precisely the moments used for the quartic remainder
and the square of the cubic remainder. These statements are kernel checked,
included in the axiom audit, and protected by fail-closed semantic mutations.

The local Taylor remainder and truncated-window comparison remain open, so
Stage D and T3 remain in progress.

### Stage D5 exact local Taylor adapter

`LeadingLocalExpansion.lean` now proves a segment-local cubic Taylor theorem
for complex-valued functions with an explicit integral fourth-derivative
remainder. The theorem assumes `C^4` regularity only at points on the segment;
its norm adapter consumes an explicit derivative bound and returns a concrete
`C|r|^4/6` estimate.

For the published phase, Lean proves the horizontal real derivative tower is
exactly `D1,D2,D3,D4`, proves `C^4` regularity while the segment remains in the
right half-plane, and derives the exact identity

`h(L+r)-h(L) = r - K r^2/2 + (D3(L)/6) r^3 + R4(r)`

for `|r| <= 1/10`. The saddle equation supplies `D1(L)=1` and `D2(L)=-K`;
neither is inserted as an assumption. A separate theorem turns any explicit
bound for `D4` on this same segment into a bound for `R4`.

The selected quantitative branch now supplies the concrete missing input.
Lean proves `1 <= |s/L| <= 2|K|`, bounds the fourth derivative throughout
`|r| <= 1/10` by `32|K|`, instantiates the exact expansion on that branch,
and concludes the explicit estimate

`|R4(r)| <= 6 |K| |r|^4`.

These four branch-specific theorems are kernel checked, included in the
axiom audit, and covered by fail-closed mutations of the theorem connections,
the factor `32`, and the fourth-order remainder. The remaining D5 work is the
exponential perturbation and truncated-window comparison; after that, the
central Gaussian and contour-tail estimates can be assembled.

### Stage D6 exponentiated local perturbation

`LeadingExponentialPerturbation.lean` now proves the pointwise step that was
previously compressed into an informal exponential expansion. On the
selected branch, the signed cubic coefficient satisfies `|c3| <= |K|`, and
the full perturbation `z=c3 r^3+R4(r)` satisfies

`|z| <= 2 |K| |r|^3`.

Lean also proves the exact factorization of the original leading integrand
as its saddle value times the full Gaussian times `exp(z)`. Under the central
smallness condition `|K||r|^3 <= 1/2`, Mathlib's complex exponential
remainder is instantiated to give the explicit pointwise error

`|exp(z)-1-c3 r^3| <= 6|K||r|^4 + 4|K|^2|r|^6`.

The final theorem restores the saddle-value and Gaussian factors and states
the corresponding pointwise integrand comparison. All five theorems are in
the kernel axiom audit and the factorization, smallness guard, quartic order,
and complex-exponential producer are protected by fail-closed mutations.
The remaining central task is to instantiate a truncated radius and
integrate this pointwise estimate using the signed cubic and absolute
fourth/sixth Gaussian moments.

### Stage D7 concrete central radius and integrated error

`LeadingCentralWindow.lean` now instantiates the paper's exact radius
`rho=|K|^(-2/5)`. Rather than assuming it is locally admissible, Lean derives
`|K| >= 4000` from the sector cutoff, the normalized center bound, and the
sharpened saddle-disc enclosure. It then proves `0<rho<=1/10` and
`|K|rho^3<=1/2` by exact real-power arithmetic.

Consequently every `r` in `[-rho,rho]` satisfies the hypotheses of the
pointwise exponential comparison. The integrated theorem controls the norm
of the central exact-minus-cubic-Gaussian integral by

`|g(L)| (6|K| J4 + 4|K|^2 J6)`,

where `J4` and `J6` are the whole-line fourth and sixth absolute Gaussian
moments already formalized in Stage D4. The proof explicitly restricts the
integral to the central interval, invokes the pointwise theorem there, and
uses nonnegativity plus set-integral monotonicity to pass to the whole line.
The exact exponent, curvature lower bound, local/smallness seams, moment
orders, and restricted-to-whole-line step are all mutation protected.

What remains for the central Gaussian theorem is the truncation error for
the Gaussian and signed cubic terms and the final division by the exact
nonzero Gaussian main term. Horizontal tails and higher theta modes remain
separate subsequent modules.

### Stage D8 exact cubic Gaussian and truncation tails

`LeadingGaussianTruncation.lean` now replaces the truncated cubic Gaussian
by an exact whole-line quantity without using an informal exponentially
small tail. Lean proves a general higher-moment tail inequality: outside
`[-rho,rho]`, the absolute `k`th Gaussian moment is bounded by
`rho^(-m)` times the whole-line `(k+m)`th moment.

The signed cubic Gaussian is integrable and its whole-line integral is
evaluated exactly as

`integral(G_K(r)(1+c r^3)) = integral(G_K)(1+c(3/K^2+1/K^3))`.

For the paper radius, the truncation error is then controlled by the tenth
absolute Gaussian moment and the eighth absolute moment attached to the
cubic term. The proof uses the exact complement decomposition of the real
line and the already kernel-checked signed moment, rather than replacing
the cubic by an absolute third moment. The tail orders, complement seam,
and exact signed correction are covered by fail-closed mutations, and the
four new theorems are included in the axiom audit.

The remaining central task is to simplify the local and truncation moment
ledger to an explicit relative `C/|K|` bound by dividing by the exact
nonzero Gaussian main term. Horizontal translated-ray tails and higher
theta modes remain separate subsequent modules.

### Stage D9 exact main-term normalization

`LeadingGaussianRelative.lean` now proves that the exact complex Gaussian
main term is nonzero with the quantitative lower bound

`|K|^(-1/2) <= |integral G_K|`.

The proof uses the exact complex square-root and exponential formula. It
checks the complex-power norm, uses `2*pi>1`, and observes that the real part
of `1/(2K)` is nonnegative when `Re K>0`; no branch choice is replaced by an
informal real square root.

The exact signed cubic correction is also normalized. For `|c|<=|K|` and
`|K|>=1`, Lean proves

`|c(3/K^2+1/K^3)| <= 4/|K|`

and therefore bounds the whole-line cubic Gaussian's relative error by
`4/|K|`. Both results are specialized to the concrete selected saddle using
the existing `|K|>=4000` and cubic-coefficient certificates. The exact
Gaussian formula, signed correction, coefficient bound, and constant four
are mutation protected; all five declarations are included in the axiom
audit.

The sole remaining central arithmetic is to reduce the fixed fourth, sixth,
eighth, and tenth Gamma-form moment bounds to explicit powers of `|K|` and
combine them with this main-term lower bound. Horizontal translated-ray
tails and higher theta modes remain separate subsequent modules.

### Stage D10 fixed Gaussian moments on the curvature scale

`LeadingMomentScale.lean` now eliminates the remaining symbolic Gamma
constants. Lean evaluates the four required half-integer Gamma values by the
proved recurrence from `Gamma(1/2)=sqrt(pi)` and uses only `pi<=4` to obtain
the rational upper bounds `2`, `4`, `14`, and `60`.

A reusable scaling theorem combines `1<Re K`, `|K|<=2 Re K`, and the exact
Gamma-form moment bound. It checks `exp(1/Re K)<=exp(1)<3`, transports the
negative power through `|K|/8<=Re K/4`, and returns a pure `|K|` power. The
selected saddle then has the explicit kernel-checked bounds

- `J4 <= 4096 |K|^(-5/2)`;
- `J6 <= 65536 |K|^(-7/2)`;
- `J8 <= 2097152 |K|^(-9/2)`; and
- `J10 <= 67108864 |K|^(-11/2)`.

The use of powers of two is deliberately coarse and exact. It changes only
the eventual effective constant, not the asymptotic exponent. The Gamma
recurrence, exponential bound, curvature comparison, four orders, and four
constants are mutation protected, and all nine declarations are in the
axiom audit.

The remaining central step is finite algebra: insert these four inequalities
into the already proved local and truncation ledgers and use the main-term
lower bound to obtain one explicit relative `C/|K|` theorem. Horizontal
translated-ray tails and higher theta modes remain separate modules.

### Stage D11 relative central Gaussian closure

`LeadingCentralRelative.lean` now finishes the central saddle calculation.
The fourth/sixth local ledger is reduced to

`286720 |K|^(-3/2)`,

while the eighth/tenth truncation ledger is reduced to

`69206016 |K|^(-3/2)`.

Lean then proves the actual central integrand is continuous and integrable on
the concrete interval, rewrites the integral of the local difference as the
difference of the two integrals, and assembles three independently proved
pieces: local exponential error, truncation to the whole-line signed cubic
Gaussian, and the exact signed cubic correction. Using
`|K|^(-1/2)<=|integral G_K|`, the result is the explicit relative theorem

`|I_central-g(L) integral G_K|
   <= (71000000/|K|) |g(L) integral G_K|`.

Thus the central Gaussian component of T3 is kernel closed, including its
normalization and a concrete constant. The four assembly theorems are in the
axiom audit, and fail-closed mutations cover the two ledger constants, the
radius powers, all three producer seams, the exact integral decomposition,
and the final `71000000/|K|` scale.

T3 is not yet complete. The endpoint connector and the translated-ray region
outside the central window must still be bounded relative to the same main
term. Higher theta modes remain the separate T4 stage.

### Stage D12 horizontal-ray sector geometry and strict concavity

`LeadingHorizontalConcavity.lean` starts the noncentral tail proof without
introducing a numerical certificate. The fixed parameter sector is converted
inside Lean to the explicit component estimates

`(99/100)|s| < Re s` and `|Im s| < |s|/200 < Re s/100`.

For every point `u=L+r` of the selected horizontal ray with `Re u>=1`, exact
complex division then proves `Re(s/u^2)>0`. The branch estimate
`|Im L|<1/20`, the elementary cosine lower bound, and positivity of `pi` and
the real exponential independently prove `Re(pi exp u)>0`. Consequently the
named second derivative

`leadingLogD2 s u = -s/u^2-pi exp u`

has strictly negative real part throughout the ray. The module constructs the
real horizontal phase, proves its first two real derivative identities from
the existing complex derivative tower, and applies Mathlib's second-derivative
criterion to obtain strict concavity on

`[1-Re L, infinity)`.

Nine new declarations are covered by the Phase 26 foundational-axiom audit,
which now contains 256 declarations. Nine fail-closed mutations protect the
sector aperture, both component constants, the two curvature producers, the
horizontal rather than vertical coordinate, the second-derivative connection,
the strict-concavity theorem, and the legal left endpoint. T3 remains in
progress: the next unit derives the two boundary phase gaps and endpoint
derivative signs at `r=+-|K|^(-2/5)` before integrating the tails.

### Stage D13 quantitative boundary phase drop and derivative signs

`LeadingHorizontalBoundary.lean` now proves the two quantitative facts that
feed the noncentral tail integrals. First, the curvature lower bound implies

`125 <= |K| rho`, where `rho=|K|^(-2/5)`.

At either signed endpoint `r=+-rho`, the exact local expansion is bounded
term by term. The linear contribution consumes at most `1/125` of
`|K|rho^2`, the cubic at most `1/10`, and the fourth-order remainder at most
`3/50`; the curvature comparison supplies a negative quadratic contribution
of at least `|K|rho^2/4`. Lean therefore obtains the explicit phase gap

`Re(h(L+r)-h(L)) <= -|K|rho^2/20`.

The second result combines this gap with the full-ray strict concavity from
Stage D12. The real derivative at the left boundary is greater than its
exact saddle value `1`, while the derivative at the right boundary is less
than `-|K|rho/20`. No numerical sampling or external interval result enters
these signs.

Four new declarations are in the foundational-axiom audit, now covering 260
declarations. Twelve fail-closed mutations protect the radius exponent, the
constant `125`, all local-expansion producer seams, the phase-drop constant,
both signed endpoints, the strict-concavity connection, and the right
derivative scale. T3 remains active. The next unit integrates concavity into
explicit left- and right-tail bounds before normalizing those bounds by the
Gaussian main term.

### Stage D14 integrated noncentral horizontal tails

`LeadingHorizontalTails.lean` now carries the boundary information through
the measure-theoretic tail integrals. Two generic kernel-checked lemmas first
state the tangent-line inequalities for a differentiable concave real
function. Applied to the selected horizontal phase, they give

- on `1-Re L <= r <= -rho`, phase difference at most
  `-|K|rho^2/20+(r+rho)`; and
- on `rho <= r`, phase difference at most
  `-|K|rho^2/20-(|K|rho/20)(r-rho)`.

Lean then proves exactly that the integrand norm is the exponential of this
real phase. The finite left tail is bounded by its interval length, while the
right tail uses an independently proved improper-integral identity

`integral_[rho,infinity] exp(-a(r-rho)) dr = 1/a`.

The resulting explicit bounds are

`left <= (Re L)|g(L)| exp(-|K|rho^2/20)`

and

`right <= |g(L)| exp(-|K|rho^2/20) 20/(|K|rho)`.

Seven new declarations are in the foundational-axiom audit, now covering 267
declarations. Thirteen hostile mutations protect both abstract tangent
lemmas, the boundary producer seams, the left and right phase signs, the norm
identity, both interval domains, the improper exponential integral, the
right reciprocal scale, and the set-integral comparison. T3 remains active:
the tail bounds must next be compared with the exact Gaussian main, and the
endpoint connector must be bounded on the same relative scale.

### Stage D15 exact relative normalization of the horizontal tails

`LeadingHorizontalRelative.lean` now compares the two tail integrals with the
same exact complex Gaussian main term used by the central theorem. The proved
lower bound `|K|^(-1/2)<=|integral G_K|` is multiplied by the saddle amplitude;
Lean checks the exact cancellation of the two half powers and obtains

`|g(L)| <= |K|^(1/2) |g(L) integral G_K|`.

Combining this with Stage D14 gives the honest relative coefficient

`(Re L + 20/(|K|rho)) exp(-|K|rho^2/20) |K|^(1/2)`.

This is already a complete relative bound for both noncentral horizontal
pieces, with no division by an unproved nonzero quantity. It is intentionally
not yet relabeled as `O(1/|K|)`: the next submilestone must prove the explicit
sector inequality that reduces this exponential coefficient to an inverse
curvature bound.

Two new declarations are in the foundational-axiom audit, now covering 269
declarations. Seven fail-closed mutations protect the Gaussian lower-bound
producer, exact half-power cancellation, integrated-tail producer, amplitude
producer, exact Gaussian main, and the full displayed relative coefficient.

### Stage D16 inverse-curvature scale of the horizontal tails

`LeadingHorizontalScale.lean` now reduces the exact Stage D15 coefficient to
an explicit inverse-curvature bound. The proof first returns to the exact
saddle equation and proves `Re L < |K|`: at the saddle,

`K = s/L^2 + pi exp(L)`,

the two real parts on the right are positive, and the exponential term alone
strictly exceeds `exp(Re L)`, which in turn dominates `Re L + 1`. Lean then
checks the exact radius identity `|K| rho^2 = |K|^(1/5)`, the already-proved
lower bound `|K| rho >= 125`, and the elementary global estimate

`x^15 exp(-x/20) <= 20^15 15!`.

Consequently both horizontal tails together are at most

`(2 * 20^15 * 15!)/|K|`

times the norm of the exact complex Gaussian main. The intentionally large
constant is immaterial to the asymptotic order and keeps every inequality
global and exact. Five new declarations bring the foundational-axiom audit
to 274 declarations. The new mutation gate protects the saddle-equation
link, the degree-15 exponential domination, the exact radius exponent, the
explicit constant, and the final connection between the integral estimate
and its scalar coefficient.

### Stage D17 endpoint connector on the Gaussian scale

`LeadingEndpointConnector.lean` now controls the finite vertical connector
at real part one, so the legal rectangle has no discarded boundary piece.
The proof sharpens the already available branch box to `Re L > 800000`,
derives `Re log L > 10`, and proves the saddle phase lower bound

`8 |s| < Re h_s(L)`.

On the connector, the existing branch-safe logarithm estimate gives
`|log(1+iy)| <= 5`, hence `Re h_s(1+iy) <= 5|s|+1` for
`|y| <= 1/20`.  Integration over the exact finite segment yields the
absolute bound `|connector| <= exp(6|s|)`.  Separately, Lean proves directly
from the curvature factorization that `|K| <= |s|`, so

`|K|^(3/2) <= exp(2|s|)`.

These estimates and the exact lower bound for the complex Gaussian integral
combine to give the clean relative result

`|connector| <= |K|^(-1) |g_s(L) integral G_K|`.

Eight new declarations bring the foundational-axiom audit to 282.  The new
fail-closed mutation gate protects the strengthened branch box, both phase
bounds, the exact connector segment, curvature growth, the Gaussian lower
producer, and the final inverse-curvature conclusion.  T3 can now be
assembled from the central window, both horizontal tails, the connector,
and the exact infinite-rectangle identity.

### Stage D18 complete T3 leading-mode assembly

`LeadingT3Assembly.lean` closes the remaining bookkeeping rather than adding
another analytic estimate.  Lean first translates the legal top ray to the
saddle-centered variable `r`, proves integrability after translation, and
partitions the ray exactly into

`[1-Re L,-rho]`, `[-rho,rho]`, and `(rho,infinity)`.

It then combines the independently proved central-window and two-tail bounds
to obtain the top-ray relative estimate with coefficient

`(71000000 + 2*20^15*15!)/|K|`.

The exact infinite-rectangle identity and the endpoint-connector theorem add
the final unit, yielding the complete leading Mellin-ray theorem

`|I_1(s)-g_s(L) integral G_K| <=`
`((71000001 + 2*20^15*15!)/|K|) |g_s(L) integral G_K|`.

All five assembly declarations are included in the foundational-axiom audit,
which now covers 287 declarations.  The fail-closed assembly gate protects
the centered translation, exact partition, all three estimate producers,
the rectangle identity, and the final connector constant.  Stage D is
complete and Stage E (T4 higher-mode suppression) is active.

### Stage E1 infinite higher-mode factor

`HigherThetaModes.lean` now defines the complete family of modes `k >= 2`
on the legal complex strip.  For the zero-based higher-mode index `n`, Lean
proves the exact arithmetic gap

`(n+2)^2-1 >= 3(n+1)`.

Writing `q = pi Re(exp u)`, it derives the exact complex-factor norm and
majorizes every term by `exp(-3q)^(n+1)`.  The infinite series is proved
summable and evaluated against the geometric series, not truncated.  On
`Re u >= 1`, `|Im u| <= 1/20`, Lean proves `q >= 1` and obtains

`|G_s(u)-g_{1,s}(u)| <= 2 |g_{1,s}(u)| exp(-3q)`.

Thirteen new declarations bring the foundational-axiom audit to 300.  The
mutation gate protects the quadratic mode gap, complex norm identity,
geometric summation, all-mode identity, strip lower bound, and suppression
sign.  Stage E remains active: contour-integral interchange and the three
region integral estimate are not yet claimed.

### Stage E2 infinite sum/integral exchange

`HigherThetaIntegral.lean` proves continuity and restricted measurability for
each complex higher mode on the legal horizontal ray.  Each mode is
dominated by the fixed, parameter-independent geometric factor
`exp(-3)^(n+1)` times the integrable leading mode.  Lean therefore proves
integrability of every mode and summability of the complete series of
integral norms.

The Bochner `integral_tsum_of_summable_integral_norm` theorem then justifies
the exchange

`integral (sum_n mode_n) = sum_n integral(mode_n)`.

The full theta top ray is defined from the all-mode pointwise sum and is
proved exactly equal to the leading top ray plus the higher-mode ray.  Twelve
new declarations bring the foundational-axiom audit to 312.  The mutation
gate protects measurability, geometric domination, norm summability, the
Fubini producer, and both exact ray identities.  Stage E remains active: the
quantitative three-region suppression relative to the Gaussian main term is
the next obligation.

### Stage E3 curvature scale for the central and right regions

`HigherThetaScale.lean` derives the missing quantitative bridge between the
mode factor and the saddle curvature.  From the concrete branch boxes and
the exact curvature factorization, Lean proves at the saddle

`|K|/4 <= pi Re(exp L)`.

Using `rho <= 1/10`, the same comparison propagates throughout
`x >= Re L-rho` with the conservative bound `|K|/5`.  Finally, the exact
curvature floor `|K| >= 4000` and the cubic lower Taylor bound for `exp`
give

`2 exp(-3q) <= |K|^(-2)` whenever `q >= |K|/5`.

These three declarations bring the foundational-axiom audit to 315.  The
mutation gate protects both scale denominators, the branch-box producer,
the curvature floor, and the negative exponential sign.  Stage E remains
active pending the final three-region integral assembly.

### Stage E4 three-region higher-mode assembly

`HigherThetaSuppression.lean` centers the infinite higher-mode ray at the
quantitative saddle and partitions it exactly into

`[1-Re L,-rho]`, `[-rho,rho]`, and `(rho,infinity)`.

On the central window, Lean combines the curvature-scale theorem with the
infinite geometric sum to prove the pointwise bound

`|sum_(k>=2) g_(k,s)(L+r)| <= |K|^(-2) |g_(1,s)(L+r)|`.

It independently bounds the central leading norm integral by twice the
saddle amplitude, normalizes that amplitude by the exact complex Gaussian
main term, and obtains a relative central contribution at most `1/|K|`.
Both noncentral higher-mode integrals are dominated pointwise by their
leading-mode counterparts and hence by the frozen T3 tail coefficient.
Consequently the full higher-mode shifted ray satisfies

`|I_high(s)| <= ((1 + 2*20^15*15!)/|K|) |g_s(L) integral G_K|`.

Combining this with the exact all-mode splitting and the T3 leading top-ray
theorem yields the kernel-checked complete shifted-ray estimate

`|I_full,top(s)-g_s(L) integral G_K| <=`
`((71000001 + 2*(2*20^15*15!))/|K|) |g_s(L) integral G_K|`.

Nine new declarations bring the foundational-axiom audit to 324. The
fail-closed mutation gate protects the pointwise infinite-sum producer,
curvature absorption, centered partition, amplitude normalization, T3 tail
producer, exact all-mode identity, and final coefficient. Stage E remains
active: this theorem is explicitly a shifted-top-ray result, and the
all-mode legal rectangle connecting it to the original Mellin ray is not yet
claimed.

### Stage E5 all-mode legal rectangle and original-ray estimate

`HigherThetaContour.lean` proves a finite Cauchy rectangle for every higher
theta mode on the open right half-plane. The far vertical segment vanishes
uniformly, so each mode has an exact infinite rectangle. A geometric
connector majorant and dominated convergence justify interchanging the
infinite mode sum with the finite vertical integral; separate absolute
summability theorems justify both horizontal ray sums.

These ingredients give exact identities for the complete higher-mode
rectangle and, after joining the leading identity, for the full theta
integrand. The higher connector is bounded by the same endpoint scale as the
leading connector, and a generic kernel-checked normalization lemma converts
that bound to one inverse power of the saddle curvature. The complete
branch-safe bottom ray therefore satisfies

`|I_full,bottom(s)-g_s(L) integral G_K| <=`
`((71000003 + 2*(2*20^15*15!))/|K|) |g_s(L) integral G_K|`.

All 26 new theorems are included in the foundational-axiom audit, bringing
its coverage to 350 declarations. The fail-closed mutation gate protects the
Cauchy producer, modewise far-side limit, connector dominated convergence,
infinite sum assembly, leading/full contour seam, connector normalization,
shifted-ray producer, and final coefficient. Stage E is complete. Stage F is
active; its first obligation is the omitted low interval `(0,1)` and the
exact identification of the resulting full Mellin moment with the T1
coefficient normalization.

### Stage F1 low interval and complete theta moment

`FullThetaMoment.lean` treats the missing interval `(0,1)` without moving it
through the logarithmic branch cut. On this interval Lean proves the full
infinite theta integrand has norm at most six: the leading phase is bounded
directly and the complete higher-mode sum is controlled by its convergent
geometric majorant. Measurability and integrability are proved for the
infinite sum rather than inferred from a formal integral.

The low interval is then normalized by the generic endpoint theorem from
Stage E5, giving one inverse curvature relative to the exact Gaussian main.
An exact disjoint-set integral identity joins `(0,1]` and `(1,infinity)`.
Consequently the complete theta moment satisfies

`|F(s)-g_s(L) integral G_K| <=`
`((71000004 + 2*(2*20^15*15!))/|K|) |g_s(L) integral G_K|`.

Nine new theorems bring the foundational-axiom audit to 359 declarations.
The fail-closed mutation gate protects the low endpoint phase bound,
infinite-mode producer, integrability, exact interval split, endpoint
normalization, T4 bottom-ray producer, and final coefficient. Stage F remains
active: the next obligation is the exact analytic coefficient function and
its two-shift moment assembly, followed by the fixed-sector Stirling and
ratio estimates.

### Stage F2 exact theta-moment coefficient assembly

`ThetaMomentAssembly.lean` closes the exact seam between the full complex
theta moment from Stages E--F1 and the T1 centered-xi coefficient. Lean first
reconstructs the all-mode theta tail on the positive real ray. It then checks
the substitution `u=2v` pointwise and under the Bochner integral, including
the Jacobian, to obtain

`F(2n) = 2^(2n+1) integral_0^infinity v^(2n) A(v) dv`.

Combining this identity with the already kernel-checked factor-eight
integration-by-parts theorem and the T1 coefficient producer gives, for
every positive index `m=n+1`,

`gamma(m) = (m!/(2m)!) *`
`(32*choose(2m,2)*F(2m-2)-F(2m)) / 2^(2m+2)`.

Both a denominator-free form and the manuscript's divided form are proved.
Five new declarations bring the foundational-axiom audit to 364 declarations.
The mutation gate protects the theta-tail reconstruction, the integral
change of variables, the T1 and factor-eight producers, the binomial
conversion, the coefficient `32`, and the final assembly. This is an exact
positive-integer identity; it does not yet claim the fixed-sector complex
moment-ratio or Stirling estimates, which remain the next T5 obligations.

### Stage F3 two-shift relative-error assembly

`TwoShiftCoefficient.lean` converts the concrete full-moment subtraction
bound into an actual relative error by first proving that the exact saddle
main term never vanishes on `leanSaddleSector`. This uses the exponential
nonvanishing of the leading integrand and the already proved positive lower
bound for the complex Gaussian integral.

The module then checks the complete cancellation algebra for a lower moment
`F(s)` and an upper moment `F(s+2)`. If the two saddle mains differ by
`L^2(1+rho)`, the exact combined relative error has numerator

`c*e_lower - L^2*(rho+e_upper+rho*e_upper)`

and denominator `c-L^2`. Lean proves both this identity and the sharp direct
norm bound retaining the cross term. The theorem is instantiated with the
concrete T3--T4 full-moment errors at `s` and `s+2`; only the saddle-main
ratio `rho` and a lower bound for the cancellation denominator remain as
explicit inputs. Ten new theorems bring the foundational-axiom audit to 374
declarations. Eight mutations protect nonvanishing, the T3--T4 producer, the
ratio cross term, the denominator sign, and the final quantitative assembly.
No sectorial ratio estimate or Stirling result is claimed by this substage.

### Stage F4a exact saddle-main differential layer

`SaddleMainDifferential.lean` rewrites the concrete saddle main term as the
exponential of a single explicit holomorphic logarithm. The identity includes
the evaluated full-line Gaussian determinant and its exact
`exp(1/(2K))` Jacobian correction. Lean then differentiates the saddle
curvature, the stationary leading phase, the determinant, and the correction,
proving

`(log Main)' = (log leading)' - K'/(2K) - K'/(2K^2)`.

It also proves the derivative and logarithmic derivative of the nonzero
concrete saddle main itself on `leanSaddleSector`. The calculation uses the
actual T2 branch derivative and T3 Gaussian integral, not an asymptotic or a
caller-supplied derivative premise. Thirteen new declarations bring the
foundational-axiom audit to 387 declarations. Eight fail-closed mutations
protect the saddle stationarity, Gaussian evaluation, both correction terms,
sector openness, and final derivative theorem.

This substage is exact differential closure only. It does not yet assert the
uniform two-unit ratio inequality; that estimate, followed by the fixed-sector
Gamma/Stirling theorem, is the next Stage F obligation.

### Stage F4b fixed-sector saddle-main ratio

`SaddleMainRatio.lean` derives all norm estimates needed to integrate the F4a
logarithmic derivative. The bounds come directly from the T2 reduced boxes:
the branch speed, scaled-factor derivative, curvature logarithmic derivative,
and the determinant/Jacobian corrections are each controlled by explicit
rational constants. A reusable complex-valued real-segment FTC inequality is
proved and then applied twice, first to `Log L_s` and then to the full saddle
main logarithm.

On the fixed inner sector

`exp(leanSaddleCutoff+1) < |s|`, `|arg s| < 1/400`,

Lean proves that the complete segment `s+2t`, `0<=t<=1`, remains inside the
T2/T3 outer sector. This includes radial clearance, the exact argument-product
calculation, and the comparison `|s|<=2|s+2t|`. It then constructs a concrete
holomorphic-form relative error `rho` and proves

`Main(s+2) = Main(s) L_s^2 (1+rho(s))`,
`|rho(s)| <= 52/|s|`.

Twenty-nine new declarations bring the foundational-axiom audit to 416
declarations. Ten fail-closed mutations protect the inner/outer sector seam,
branch and curvature derivative producers, segment FTC, logarithmic-error
sign, exponential conversion, exact main identity, factorization, and final
constant. This closes the saddle-main ratio obligation. The integer
Gamma/Stirling quotient is closed in the next substage.

### Stage F5a effective integer Stirling anchor

`FactorialRatioStirling.lean` uses the exact scope of the coefficient formula:
the Gamma quotient is evaluated only at a positive integer `M`. Rather than
introduce an unnecessary complex-Gamma theorem, Lean refines Mathlib's
kernel-checked real Stirling limit with its Robbins step estimate. Telescoping
the step bound to the proved limit gives

`0 <= log(stirlingCorrection(M)) <= 1/(12M)`.

An elementary exponential bound converts this to a multiplicative estimate.
Lean then compares the corrections at `M` and `2M`, proving exactly

`M!/(2M)! = HollandMain(M) * (1+error)`,
`|error| <= 1/(4M)`.

The traditional Holland main is identified algebraically as

`exp(M) * M^M * sqrt(M) / ((2M)^(2M) * sqrt(2M))`.

Fourteen declarations bring the foundational-axiom audit to 430 declarations.
The fail-closed mutation gate protects the Mathlib Robbins and Stirling-limit
producers, the constants `12`, `6`, and `4`, the traditional-main identity,
and the final relative-error theorem. This is the positive-integer
normalization anchor for the next substage. Theorem 7.1 is holomorphic in a
complex sector, so the corresponding complex Gamma/Stirling transport remains
open and no broader complex-sector estimate is claimed here.

### Stage F5b1 right-half-plane digamma remainder

`GammaFacts/StirlingRight.lean` reuses the exact unit-interval
Euler--Maclaurin identities from `StirlingVert.lean`, but replaces every
vertical-line denominator estimate by a real-part estimate. Lean proves the
telescoping bound

`sum_n 1/|n+1+w|^2 <= 1/Re(w)`

and uses it to control both exact remainder series. At noninteger points with
`Re(w)>=1`, the series-level theorem is

`|digamma(w)-Log(w)+1/(2w)| <= 2/Re(w)^2`.

Lean then proves that digamma is holomorphic throughout `Re(w)>0` and passes
this estimate to every formerly excluded positive integer by an explicit
upper-right approximating sequence. Thus the same bound holds at every point
with `Re(w)>=1`; `integerComplement` is no longer a hypothesis of the exported
estimate.

All limits, infinite sums, and the logarithmic increment are connected to the
existing partial-fraction and interval-integral producers; no asymptotic
premise is introduced. Twenty declarations bring the foundational-axiom
audit to 450 declarations. Twelve fail-closed mutations protect the real-part
denominator, telescoping sum, exact series producers, series domain guard,
holomorphicity producer, continuity transfer, and final constant. The Gamma
transport and its multiplicative remainder remain the next substage.

### Stage F5b2 normalized complex Gamma transport

`Research/JensenWedge/GammaRatioStirling.lean` defines the exact holomorphic
continuation

`Gamma(M+1) / Gamma(2M+1)`

and divides it by Holland's elementary main written as the exponential of

`M + (M+1/2) Log M - (2M+1/2) Log(2M)`.

Lean differentiates the Gamma quotient and the elementary main from their
Mathlib producers, applies the digamma recurrence at both scales, and proves
the exact normalized differential equation

`C'(M) = C(M) * (delta(M) - 2 delta(2M))`,

where `delta(M)=digamma(M)-Log(M)+1/(2M)`. The all-point F5b1 theorem then
gives the explicit estimate

`|delta(M)-2 delta(2M)| <= 3/Re(M)^2` for `Re(M)>=1`.

Lean next proves exact specialization of both the Gamma quotient and the
elementary main at every positive integer, so the F5a Robbins correction is a
genuine anchor for the same holomorphic function. Along the straight segment
from `floor(Re M)` to `M`, Grönwall's inequality controls the normalized
quotient. The already checked narrow-sector component bounds prove that this
floor anchor is within one percent of the parameter and that the whole segment
stays in the remote right half-plane. The exported conclusion is

`Gamma(M+1)/Gamma(2M+1) = H(M) * (1+error)`,

with `|error| <= 1/|M|` throughout `leanCoefficientSector`.

Thirty-seven declarations bring the foundational-axiom audit to 487
declarations. Eighteen fail-closed mutations protect the exact Gamma
denominator, elementary main, half-shift residual, two-scale coefficient,
Gamma and recurrence producers, correction derivative, integer anchors,
Grönwall transport, floor selection, sector geometry, and final `1/|M|`
constant. The complex Gamma/Stirling subchain is complete; the final
holomorphic coefficient assembly remains the next T5 substage.

### Stage F5c1 exact complex coefficient normalization

`Research/JensenWedge/CoefficientAssembly.lean` defines the complex Mellin
continuation of the coefficient identity with `N=2M-2`, the exact multiplier
`16(N+2)(N+1)`, the holomorphic dyadic factor
`exp(-(2M+2) Log 2)`, and the normalized complex Gamma quotient. Lean proves
that this continuation specializes exactly to `centeredXiCoefficient (n+1)`
for every natural `n`. This is an equality theorem, not an asymptotic premise.

The eight new public declarations bring the foundational-axiom audit to 495.
Eight fail-closed mutations cover the Mellin shift, multiplier, dyadic
exponent, Gamma source, two-shift sign, and both exact normalization producers.
The next substage supplies concrete sector bounds for the two-shift
denominator and curvature before combining the three relative errors.
The final holomorphic coefficient assembly is therefore still in progress.

### Stage F5c2 coefficient-sector inequalities

The same module now converts the T2 comparison-disc estimates into the
quantitative scales used in the final assembly. Lean proves

- `|L_s| <= 2 log|s|`;
- `1/|K_s| <= 4 log|s|/|s|`;
- `|16(s+2)(s+1)| <= 96|s|^2`; and
- `|16(s+2)(s+1)-L_s^2| >= 8|s|^2`.

In particular, the two-shift cancellation denominator is nonzero everywhere
on the fixed sector. These are derived from the exact branch box and radial
cutoff, not sampled numerically. Five new public declarations bring the
foundational-axiom audit to 500. The coefficient mutation gate now also
protects the logarithmic saddle estimate, curvature rate, multiplier ceiling,
denominator floor, and nonvanishing theorem. The remaining F5 task is to
combine the Gamma, theta-moment, and saddle-ratio errors into one explicit
relative-error theorem and then prove its holomorphic-source properties.

### Stage F5c3 pointwise sectorial coefficient theorem

The exact coefficient extension is now factored as a nonzero main times one
combined relative error. The error definition includes the necessary product
term between the Gamma correction and the moment/two-shift correction. Using
the F5c2 denominator and curvature bounds, Lean proves

`|E(M)| <= (203 C_theta) log|N|/|N|`, where `N=2M-2`.

The exported theorem `complexXiCoefficient_sector_asymptotic` packages the
nonzero main, exact equality, and uniform rate on the paired fixed sector.
No existential analytic premise remains in this pointwise theorem. Fourteen
new public declarations bring the foundational-axiom audit to 514. The
expanded source gate protects the paired sector, exact main and error,
two-shift producer, cross term, individual bounds, nonvanishing, and final
export. T5 is pointwise kernel closed; holomorphic-source closure and exact
identification of this factored main with the simplified manuscript display
remain active.

### Stage F5c4 holomorphic coefficient assembly

`Research/JensenWedge/FullThetaHolomorphic.lean` identifies the complete
theta moment with the Mellin transform of

`exp(u/4) * ThetaTail(exp u)`.

Lean proves continuity and local integrability of this kernel, exponential
decay at infinity through the already checked Hurwitz-theta representation,
and boundedness at zero. Mathlib's dominated Mellin differentiation theorem
then proves that `fullThetaMoment` is holomorphic throughout `Re(s)>-1`.

The fixed coefficient sector and its paired preimage are proved open. Lean
transports the Mellin theorem through the exact Gamma quotient, dyadic scale,
two shifted moments, polynomial multiplier, selected holomorphic saddle
branch, and saddle main. On the paired sector, the explicit combined error is
proved equal to the generic quotient

`complexXiCoefficientMoment / complexXiCoefficientMain - 1`.

Consequently the actual coefficient continuation, the nonzero factored main,
and the explicit relative error are all holomorphic there. The exported
`complexXiCoefficient_sector_holomorphic_asymptotic` packages openness,
holomorphy, exact factorization, nonvanishing, and the previously checked
uniform logarithmic rate. Twenty-one new public declarations bring the
foundational-axiom audit to 535 declarations. Seventeen fail-closed mutations
protect the theta/Hurwitz source, Mellin bridge, differentiation producer,
sector geometry, Gamma and saddle derivatives, quotient equality,
nonvanishing divisor, and final export.

This closes the holomorphic-source portion of T5. The exact identification of
the factored Lean main with the simplified main displayed in the manuscript
remains active; it is not claimed by this submilestone.

### Stage F5c5 exact manuscript-main bridge

`Research/JensenWedge/ManuscriptCoefficientMain.lean` defines the saddle and
elementary factors printed in manuscript Theorem 7.1. It also defines the
three exact factors suppressed by that display:

- the elementary reindexing factor `R_N`;
- the Gaussian linear-amplitude factor `exp(1/(2K_N))`; and
- the two-shift cancellation factor
  `1-L_N^2/(16(N+2)(N+1))`.

Lean proves, throughout the paired coefficient sector, the exact identity

`complexXiCoefficientMain M = manuscriptXiCoefficientMain M *`
`manuscriptMainCorrection M`.

This includes a kernel-checked character calculation showing that the
factorial main, dyadic scale, and two-shift multiplier equal the displayed
elementary main times the paper's exact `R_N`; no numerical or asymptotic
simplification is used. Eleven public declarations bring the foundational-
axiom audit to 546 declarations. Twelve fail-closed mutations protect all
three correction factors, their signs and exponents, the factorial,
multiplier, and saddle producers, and the final exact bridge.

The next substage must estimate the combined correction and transfer the
already checked factored-main asymptotic and holomorphy statements to the
manuscript display. This exact-bridge milestone does not claim that transfer.

### Stage F5c6 manuscript correction bounds

`Research/JensenWedge/ManuscriptCorrectionBounds.lean` proves effective
fixed-sector estimates for all three exact factors. For `N` in the outer
saddle sector, Lean proves

- `|R_N-1| <= log|N|/|N|`;
- `|exp(1/(2K_N))-1| <= 4 log|N|/|N|`; and
- `|1-L_N^2/(16(N+2)(N+1))-1| <= log|N|/|N|`.

The proof of the first bound is not a sampled or imported asymptotic. It
uses the exact one-step complex-log expansion from the Gamma/Stirling
library twice, retains both certified epsilon remainders, proves an exact
second-order rational identity, and first obtains the stronger bound
`|Log R_N| <= 16/|N|^2`. The Gaussian and cancellation estimates are derived
from the checked curvature, branch, and multiplier bounds.

Combining the factors gives

`|manuscriptMainCorrection M - 1| <= 20 log|N|/|N|`.

Ten public declarations bring the foundational-axiom audit to 556
declarations. Eighteen fail-closed mutations protect the log expansions,
epsilon bounds, sector geometry, curvature and branch producers, multiplier
floor, individual estimates, and final product consumer. The remaining
substage is to define the displayed-main relative error, prove its rate and
holomorphy, and export the manuscript-normalized coefficient theorem.

### Stage F5c7 manuscript-normalized holomorphic coefficient theorem

`ManuscriptCoefficientTheorem.lean` now completes the transfer from the exact
factored main to the main printed in manuscript Theorem 7.1. Lean defines the
actual relative error, retains the correction/error cross term exactly, and
proves on the full paired coefficient sector

`|error(M)| <= (20 + 21 A) log|N|/|N|`,

where `A` is the already checked factored-main coefficient. The displayed
main and correction product are nonzero. Every correction factor, their
product, the displayed main, and the resulting relative error are proved
holomorphic on the open sector. The exported theorem packages openness,
holomorphy, exact factorization, nonvanishing, and the explicit rate.

This closes the manuscript-normalized coefficient asymptotic itself. Stage F
continued at the downstream order-six Cauchy seam, which is closed in the
next submilestone. The typed xi analytic inputs remain separate.

### Stage F5c8 proportional-disc Cauchy transport through order six

`ManuscriptCauchyTransport.lean` instantiates the generic Cauchy adapter at
every positive real center `x` above the explicit threshold, with the paper's
radius `x/1000`. The kernel proves that the whole closed disc lies in the
paired coefficient sector: both `M` and `N=2M-2` satisfy the radial and
angular constraints. It also proves `x <= |N| <= 3x`, converting the
pointwise coefficient estimate into the uniform disc bound

`|error(z)| <= C log(3x)/x`.

Cauchy's estimate then gives, simultaneously for every `j <= 6`,

`|error^(j)(x)| <= j! [C log(3x)/x] / (x/1000)^j`.

The theorem consumes the actual and displayed-main holomorphy proofs, main
nonvanishing, the exact quotient identification, the closed-disc geometry,
and the previously generic Cauchy producer. Thus the order-six error
transport is no longer merely an adapter with a caller-supplied uniform
bound. At this submilestone Stage F still required typed xi residual/input
instantiation and connection to the final conditional root theorem; the
target-identity portion is closed below in F5c10.

### Stage F5c9 exact auxiliary-moment bridge

`XiAuxiliaryMoment.lean` now defines the manuscript's holomorphic auxiliary
moment `M_z` directly and proves the character-level identity

`complexXiCoefficientMoment M = complexFactorialRatio M * M_M`.

Lean proves the Gamma quotient is nonzero throughout the relevant right
half-plane, identifies the integer specializations with the T1 centered-xi
coefficients, and removes that exact quotient from the displayed coefficient
main. The resulting auxiliary moment has the same relative-error function,
the same explicit sector bound, and the same order-six proportional-disc
Cauchy transport. Both the auxiliary moment and its quotient main are proved
holomorphic, and the main is nonzero on the full paired coefficient sector.

This closes the manuscript seam between the coefficient asymptotic and the
object denoted `h(z)=Log M_z` in the derivative analysis. It does not yet
formalize the logarithm, the paired polygamma subtraction, or the complete
sixth residual certificate. Fourteen new public declarations bring the
foundational-axiom audit to 594 declarations; fail-closed mutations protect
the exact Gamma factor, integer specialization, factorization, holomorphy,
nonvanishing, shared relative error, and order-six consumer.

### Stage F5c10 concrete Riemann-xi Jensen target

`RiemannXiJensen.lean` fixes the real coefficient sequence by the concrete
omega integral with the exact factor

`8 n!/(2n)!`.

Lean proves that its complexification is the T1 coefficient of Mathlib's
centered xi, verifies the paper's Taylor normalization, proves those complex
coefficients have zero imaginary part, and connects the positive-integer
auxiliary moment directly to the real sequence. The actual Jensen polynomial
is then defined with this sequence and the exact binomial convention.

Two concrete-target root theorems are exported. One consumes the existing
`JensenWedgeCertificate`; the stronger interface exposes the split
`JensenWedgeAnalyticInputs`, so the parameter branch, comparison roots,
sixth residual, and xi identification remain visible rather than being
hidden in a generic sequence premise. These theorems do not construct the
remaining Jacobi/MMP/MSS or sixth-residual inputs. Nine new public
declarations bring the foundational-axiom audit to 603 declarations.

### Stage F5c11 nonvanishing and logarithmic-error transport

`XiLogError.lean` closes the first part of the manuscript's
`h(z)=Log M_z` argument. The explicit error coefficient is combined with the
conservative Lean cutoff to prove, everywhere on the paired sector,

`|error(M)| <= 1/2`.

Consequently `1+error` lies in the open right half-plane and is nonzero, and
the auxiliary moment itself is nonzero. Lean defines the branch
`Log(1+error)`, proves its exponential identity and holomorphy, and uses the
standard sharp local estimate

`|Log(1+error)| <= (3/2)|error|`.

On every paper-radius disc `x/1000`, Cauchy's theorem now yields the explicit
bound through all `j<=6` for the logarithmic error itself. This eliminates a
previous distinction between differentiating the relative error and
differentiating the logarithm of the relative factor. It does not yet prove
the complete displayed formula for `E_F^(6)` or the paired polygamma bound.
Ten new public declarations bring the foundational-axiom audit to 613.

### Stage F5c12 paired fifth-polygamma series estimate

`PolygammaPairing.lean` now kernel-checks the quantitative pairing mechanism
for the two fifth-polygamma differences in the displayed sixth residual.  The
standard series

`120 * sum_{k >= 0} (z+k)^(-6)`

is proved absolutely convergent on every integer-anchored right half-plane.
Lean proves the line segment stays in that half-plane, the exact algebraic
sixth inverse-power Lipschitz estimate, and the integral-test bound

`sum_{k >= 0} (n+k)^(-7) <= 1 / (6 (n-1)^6)`.

The constants cancel to give the uniform paired estimate

`|P5(z)-P5(w)| <= 120 |z-w| / (n-1)^6`

whenever `Re z, Re w >= n >= 2`.  This is the inverse-power gain used to
pair the manuscript's `B-C` and `D-(n+1/2)` terms.  The module explicitly
does not yet identify the series with `iteratedDeriv 5 Complex.digamma`;
that derivative-identification seam and the final residual assembly remain
open rather than being hidden behind the notation.  Nine public declarations
bring the foundational-axiom audit to 622, and a fail-closed mutation gate
protects the segment geometry, exponents, constants, summability source, and
paired conclusion.

### Stage F5c13 fifth-polygamma derivative identification

`PolygammaDerivative.lean` closes the derivative-identification seam left
explicitly open in F5c12.  Lean proves local uniform differentiability of the
generic inverse-power series on `Re z > 1`, with

`S_p'(z) = -p S_{p+1}(z)`.

The existing trigamma theorem excluded every integer because of its source
domain.  The new proof removes that artificial exclusion: at a positive
integer it approaches through noninteger right-half-plane points and uses
holomorphic continuity of both `deriv digamma` and `S_2`.  Induction then
proves the complete tower

`iteratedDeriv (m+1) digamma z = (-1)^m (m+1)! S_(m+2)(z)`.

At `m=4`, this identifies `iteratedDeriv 5 Complex.digamma` exactly with the
`120 * sum (z+k)^(-6)` series from F5c12.  The paired theorem is consequently
exported directly in the manuscript's derivative notation, including at
positive integer arguments.  Twelve public declarations bring the
foundational-axiom audit to 634.  The mutation gate protects termwise
differentiation, the uniform-series theorem, the noninteger approximation,
the factorial/sign tower, and the final paired consumer.

### Stage F5c14 uniform complex logarithmic-error transport

The original `XiLogError.lean` Cauchy consumer bounded derivatives at a
positive real center.  The manuscript residual, however, is evaluated on a
complex neighborhood.  The strengthened theorem now fixes the inner radius
`x/2000`, proves that an inner closed ball about every point of the
`x/2000` center ball lies inside the original `x/1000` manuscript disc, and
applies Cauchy's estimate on that moving inner ball.  Consequently, for
every such complex point `z` and every `j <= 6`, Lean proves

`|logError^(j)(z)| <= j! * ((3/2) epsilon_x) / (x/2000)^j`.

This removes a real-center-only gap before the sixth-residual assembly.  The
proof consumes the actual sector containment and uniform coefficient-error
bound on the outer disc; it is not inferred from a grid.  Three public
declarations bring the foundational-axiom audit to 637, and the expanded
xi-log mutation gate protects the half-radius constant, triangle geometry,
sector containment, and uniform derivative denominator.

### Stage F5c15 exact sixth-residual pairing assembly

`SixthResidualAssembly.lean` now defines the manuscript's displayed
six-term value `E_F^(6)` with its exact signs and half shift, and kernel
checks the regrouping into the `B-C` and `D-(n+1/2)` pairs plus the distant
`A` term.  A second integral-test proof gives

`sum (n+k)^(-6) <= 1 / (5 (n-1)^5)`,

so the unpaired fifth-polygamma derivative is bounded by
`24/(n-1)^5`.  Combining this with the F5c13 paired derivative theorem
produces an explicit norm bound for the entire residual from a supplied
`h^(6)` value.

The module then substitutes the actual sixth derivative of the logarithmic
xi relative error at the translated point `n+z`, using the uniform
complex-disc theorem from F5c14.  The
result is an end-to-end residual inequality in which only the
moving-saddle sixth derivative remains as the visibly named `mainSix`
input.  This is an honest seam, not a hidden assumption: identifying that
input with the exact auxiliary-main logarithm and the checked `H_6`
rational function is the next substage.  Ten public declarations bring the
foundational-axiom audit to 647.  The new fail-closed mutation gate protects
the residual signs, half shift, exponents, constants, pairing sources,
uniform xi-log source, and end-to-end consumer.

### Stage F5c16 concrete residual parameter geometry

`ResidualParameterGeometry.lean` reconstructs the manuscript parameters

`A=alpha*n/e`, `B=n(t+w*e)`, `C=n*t`, `D=n(1+delta*e)`

from the branch coordinates and proves that these are exactly the existing
Jacobi parameters at reciprocal scale `1/n`.  For every point in the fixed
outer parameter box, `n>=8`, `0<e<=1/12`, and every complex offset with
`Re z>=-n/2`, Lean now constructs a `ResidualParameterCertificate` at the
integer anchor `floor(n/4)`.  The certificate contains all five
right-half-plane inclusions and the explicit displacement bounds

`|B-C| <= 6*n*e`,

`|D-(n+1/2)| <= (5/12)*n*e + 1/2`.

The final theorem feeds this concrete certificate, the translated `n+z`
xi-log point, and the outer-box parameters into the F5c15 residual assembly.
Thus no free `A,B,C,D` geometry hypotheses remain.  The moving-saddle
`mainSix` value is still visibly explicit, in accordance with the earlier
decision not to duplicate the decisive base symbolic reconstruction already
performed independently in Mathematica.  Eight public declarations bring
the foundational-axiom audit to 655; a fail-closed mutation gate protects
the scale conventions, Jacobi bridge, quarter anchor, box source,
displacement constants, translated xi point, and final consumer.

### Stage F5c17 moving-saddle sixth bound

`MovingSaddleSixth.lean` now defines the manuscript's concrete saddle main
`G_0`, its curvature denominator `Q_N`, the reduced coordinates
`r=1/L_N` and `sigma=L_N/N`, and the exact reduced sixth-order value

`H_6(r,sigma)/(N^5 L_N)`.

For every `N` in the already constructed Lean saddle sector, the kernel now
proves both reduced coordinates lie in the `7/50` bidisc.  It also derives
the non-asymptotic lower bound `log|N|/2 <= |L_N|` directly from the fixed
Newton disc and the explicit logarithmic comparison center.  Combining
those results with the exact 82-term `H_6` certificate gives

`|H_6(r,sigma)/(N^5 L_N)| <= 20000/(|N|^5 log|N|)`.

The independently reconstructed base symbolic equality
`G_0^(6)=H_6/(N^5 L_N)` remains visible as the single field of
`ManuscriptG0SixthIdentification`; Lean then transports the bound to the
actual iterated derivative.  This records the agreed Mathematica/SymPy
trust boundary without duplicating or hiding it.  Eleven public declarations
bring the foundational-axiom audit to 666.  The mutation gate protects the
coordinate orientation, `G_0` terms, exponent five, half-log bound, constants,
and the exact named identification consumer.

### Stage F5c18 moment-chain saddle residual

`MomentSaddleResidual.lean` applies the exact sixth-order affine-chain factor
`2^6=64` for `N=2M-2`.  The pre-existing manuscript Cauchy geometry now
supplies, for every complex offset in the inner residual disc, both

`coefficientMellinParameter (n+z) in leanSaddleSector`

and `n <= |coefficientMellinParameter (n+z)|`.  Monotonicity of the fifth
power and real logarithm then turns the F5c17 bound into the uniform estimate

`|64 H_6/(N^5 L_N)| <= 1280000/(n^5 log n)`.

The final theorem inserts this exact reduced value into the F5c16 outer-box
residual inequality.  Consequently neither `mainSix` nor an abstract
`Hmain` bound remains in that theorem: its right side consists only of the
explicit moving-saddle term, the already proved xi-log Cauchy term, the two
paired polygamma displacements, and the distant tail.  The CAS identification
boundary remains visibly separate.  Five public declarations bring the
foundational-axiom audit to 671, with a new mutation gate protecting the
chain factor, shifted-sector source, radial comparison, exponent, constant,
and final residual insertion.

### Stage F5c19 distant-parameter logarithmic gain

`SixthResidualAssembly.lean` now permits a distinct integer anchor for the
distant `A` polygamma argument. `ResidualParameterGeometry.lean` proves that
the outer branch box and `0<e<=1/12` place this argument to the right of the
much larger anchor `floor(n/e)`, while retaining `floor(n/4)` for the four
nearby paired arguments. `MomentSaddleResidual.lean` instantiates the sharper
assembly with the reduced moving-saddle value. Its final distant tail is

`24/(floor(n/e)-1)^5`,

so the logarithmic gain needed for the ultimate `1/(n^5 log n)` estimate is
not discarded by the common quarter-scale anchor. Three public declarations
bring the foundational-axiom audit to 674. A fail-closed mutation gate
protects the separate assembly, reciprocal-scale geometry, outer-box source,
fifth-power tail, and end-to-end consumer.

### Stage F5c20 explicit one-constant residual rate

`SixthResidualRate.lean` reduces the F5c19 ledger to one explicit bound. The
only scale input added is the manuscript relation

`e <= 2/log n`.

Lean proves that the conservative cutoff makes the Cauchy envelope at most
`1/2`, that the common nearby anchor is at least `n/12`, and that the distant
anchor is at least `n log n/4`. It then assigns and proves the four individual
ledger constants

`540*2000^6`, `1440*12^6`, `160*12^6`, and `24*4^5`,

and combines them with the moving-saddle constant `1280000`. The final
theorem bounds the concrete complex-uniform residual by

`C_res/(n^5 log n)`

throughout the inner Cauchy disc and outer parameter box. Fifteen public
declarations bring the foundational-axiom audit to 689. Fourteen fail-closed
mutations protect the scale premise, both floor anchors, all four constants,
the four component bounds, the F5c19 producer, and the final consumer.

### Stage F5c21 exact xi parameter map and six-match hinge

`ExactParameterMap.lean` now defines the actual four-parameter map used by
the manuscript from `riemannXiCoefficientReal`, the exact half-shift, and the
four Jacobi logarithmic quotients at `A,B,C,D`.  The four triangular scales
are retained verbatim.  Lean proves, for nonzero integer and saddle scales,
that the vector equation is equivalent first to four vanishing forward
differences and then to the four unscaled quotient residual equations.

The same module connects this concrete zero equation to the existing
four-quotient/two-normalization adapter, yielding equality of all six
logarithmic coefficient coordinates once the residual is identified with the
two second-difference sequences.  Positivity and the uniform `C^1` interval
bounds remain separate obligations; the exact map is no longer an unnamed
paper-level object. Fourteen public declarations bring the foundational-
axiom audit to 703. Fourteen fail-closed mutations protect the xi source,
half-shift, `A,B,C,D` signs, second difference, four triangular scales, and
both exact quotient/six-match consumers.

### Stage F5c22 elementary cube vector and exact limiting target

`ElementaryParameterMap.lean` fixes the four-component cube-integral vector
with its exact `(1,1/2,1,1)` coefficients, remote `e^q` factor, `B-C` pair,
`D` boundary, and gamma half-shift.  It separately defines the rational
elementary limit, adds the audited xi saddle vector `(-2,-1,-2,-2)`, and
proves that the resulting map vanishes at `branchCenter`.

For nonzero `alpha,t`, the zero equation is proved equivalent to the existing
`SixthOrderLeadingSystem`; positivity then gives uniqueness of the center.
Thus the forthcoming `C^1` inequalities now compare two concrete Lean
functions rather than a paper-level `G_n -> F` slogan. Twelve public
declarations bring the foundational-axiom audit to 715. Eleven fail-closed
mutations protect every elementary term, the normalization, saddle signs,
leading-system bridge, and positive uniqueness consumer.

### Stage F5c23 logarithmic-boundary/cube identity

`ElementaryParameterIdentity.lean` closes the exact source seam between the
five logarithmic boundaries in the Jacobi quotient and the cube-integral
elementary map.  Lean proves the simultaneous denominator scaling law,
derives the first four finite differences of the scaled logarithmic quotient,
and transports their exact signs and factorial constants through the
triangular normalization.

For every point in the outer branch box and positive scales, the resulting
four-vector is proved equal to `exactElementaryParameterMap`.  Thus the
elementary map is no longer merely a separately transcribed expression: it is
kernel-connected to the actual logarithmic quotient at all four orders.
Twelve public declarations bring the foundational-axiom audit to 727.  The
fail-closed mutation gate protects the scaling direction, five-boundary sign
pattern, all four triangular coefficients, all four forward-difference
producers, and the final vector-equality consumer.

### Stage F5c24 quantitative elementary boundary estimates

`ElementaryBoundaryEstimates.lean` converts the exact cube calculus into
explicit inequalities.  It proves the reciprocal-power mean-value bound and
the first- and second-derivative errors with both displacement and cube-scale
terms retained.  A kernel-checked averaging lemma then yields the full `B-C`
divided-difference estimate.

The `D` boundary is paired with the exact gamma half-shift before taking
absolute values.  Its final bound displays the unavoidable `q*x/e` term
separately from the `O(e+x)` paired-boundary error, preventing the historical
spurious loss from re-entering. Seven public declarations bring the
foundational-axiom audit to 734. Seven fail-closed mutations protect the
power increment, derivative orders and signs, averaging producer, pairing,
and explicit `x/e` term.

### Stage F5c25 elementary parameter derivatives

`ElementaryParameterDerivatives.lean` decomposes every exact elementary
component into its remote, paired `B-C`, and paired `D`/gamma boundaries.
It proves the exact `HasDerivAt` statements in all four parameters and
quantifies their errors from the rational leading map.  The nontrivial
`t` derivative is produced from an exact first-derivative segment formula
and a kernel-checked average of the second cube derivative.

The surviving `q=1` remote alpha derivative keeps its explicit
`2*x*e*alpha_0^-3` error, while all other derivative bounds display their
full `x+e` dependence. Thirteen public declarations bring the
foundational-axiom audit to 747. The fail-closed mutation gate protects the
three-term decomposition, all four derivative producers, the second-order
average, derivative signs and orders, and the remote scale.

### Stage F5c26 componentwise elementary differential

`ElementaryComponentDifferential.lean` exposes one exact elementary map
component as a scalar function of `(alpha,t,w,delta)`, proves that it is the
corresponding entry of the exact parameter map, and supplies independent
`HasDerivAt` producers for all four partial derivatives.  This removes any
ambiguity about how the boundary estimates populate the Jacobian.

The module also defines the three nonzero leading partials and proves the
exact componentwise `t`, `w`, and `delta` error inequalities before box
instantiation. Sixteen public declarations bring the foundational-axiom
audit to 763. The fail-closed mutation gate protects the exact-map seam,
all four partial definitions and producers, the leading derivative signs,
and all three quantitative consumers.

### Stage F5c27 componentwise elementary value estimate

`ElementaryComponentValue.lean` defines the limiting component in the same
order-indexed coordinates as the exact cube map and proves it equals
`leadingElementaryParameterMap`.  It then isolates the sole surviving
remote limit in component zero and proves the four-case remote error from
the actual cube integral.

The final theorem combines that remote estimate with the `B-C` and paired
`D`/gamma bounds to give the full exact component value inequality.  The
`x/e` half-shift term remains visible. Six public declarations bring the
foundational-axiom audit to 769. The mutation gate protects the remote case
split, leading-map seam, remote error source, half-shift scale, and final
three-boundary consumer.

### Stage F5c28 remote alpha differential

`ElementaryAlphaDifferential.lean` completes the fourth derivative channel.
It defines the limiting alpha column with its sole nonzero entry in component
zero and proves the exact four-case error against the remote cube-integral
derivative. The `q=1` error is `2*x*e*alpha_0^-3`; the higher components
retain their explicit powers of `e`.

Three public declarations bring the foundational-axiom audit to 772. The
fail-closed mutation gate protects the surviving component, inverse-square
order, remote power, and final alpha-column consumer.

### Stage F5c29 elementary Jacobian assembly

`ElementaryJacobianAssembly.lean` assembles the four scalar partials into
the exact elementary Jacobian and their four limiting values into the
limiting Jacobian. A bundled theorem records all four `HasDerivAt` producers
for every row, and a single entrywise theorem dispatches to the alpha, t, w,
or delta quantitative bound according to the column.

Five public declarations bring the foundational-axiom audit to 777. The
mutation gate protects column order, exact/leading separation, the bundled
partial producer, all four error columns, and the unified matrix consumer.

### Stage F5c30 fixed-box elementary `C¹` bounds

`ElementaryC1Box.lean` instantiates the componentwise value and Jacobian
estimates on the manuscript's exact rational outer parameter box.  Lean
first proves the scale comparisons `x*e <= x <= x/e` and `e^2,e^3 <= e`
for `0<e<=1`, then performs all four value cases and all sixteen Jacobian
entry cases.  The resulting uniform certificates are

`|F_elementary(y,x,e)_j - F_limit(y)_j| <= 10000*(e+x/e)`

and

`|DF_elementary(y,e,x)_(j,k) - DF_limit(y)_(j,k)| <= 10000*(e+x)`.

All nonlinear box products, including `w^2 e` and `delta^2 e`, are bounded
by explicit order-monotonicity lemmas before rational normalization. Three
public declarations bring the foundational-axiom audit to 780. The
fail-closed mutation gate protects the exact outer-box source, both error
scales, both matrix/value producers, and their fixed constants.

### Stage F5c31 exact elementary/xi-saddle decomposition

`ExactParameterDecomposition.lean` splits the true normalized xi parameter
map at the definition level.  Lean proves that the printed half-shift
logarithm is exactly the negative fifth elementary log-ratio boundary, with
all positivity conditions required by `Real.log_div` explicit.  It then
proves, before asymptotic estimation,

`exactXiQuotientResidual = elementaryQuotientResidual +
  (halfShift + Delta^2 log(gamma))`

and hence on the full outer parameter box

`exactXiParameterMap = exactElementaryParameterMap + exactXiSaddleParameterMap`.

The parenthesized term is exactly the auxiliary-moment second difference by
Gamma duplication. It depends only on `n,L`, so the later derivative theorem can
kernel-check rather than merely assert that the xi saddle contributes no
parameter derivative. Four public declarations bring the foundational-axiom
audit to 784. The mutation gate protects the half-shift sign, second-
difference order, all four triangular signs/scales, the cube-map source, and
the final exact decomposition consumer.

### Stage F5c32 full elementary Fréchet derivative

`ElementaryFrechet.lean` upgrades the four independently checked scalar
partial derivatives to the genuine derivative of the four-variable map.
Lean differentiates the remote, paired, and gamma boundary terms on the
positive orthant, restricts the resulting Fréchet derivative to each
coordinate line through `Function.update`, and proves that its four basis
columns are exactly the entries of `exactElementaryJacobian`.

Linearity on the coordinate basis then identifies the complete continuous
linear map with `Matrix.mulVec exactElementaryJacobian`.  Thus the later
operator-norm certificate will bound the actual derivative, not an
unconnected table of partial derivatives. Four public declarations bring
the foundational-axiom audit to 788. The fail-closed mutation gate protects
the matrix action, all four scalar producers, the coordinate-line bridge,
and the final full-Jacobian consumer.

### Stage F5c33 elementary operator-norm certificate

`ElementaryJacobianOperator.lean` converts an arbitrary uniform entrywise
bound on a four-by-four matrix difference into the exact row-sum estimate
`||A-B||_op <= 4C` for the branch-space sup norm. Applying it to the fixed
outer-box estimate proves

`||DF_elementary(y,e,x)-DF_limit(y)||_op <= 40000*(e+x)`.

The same module packages the audited rational inverse matrix as a continuous
linear map, identifies its action with `gaugeInverseAction`, and upgrades
the existing row-sum estimate to `||P||_op <= 304/3`. Five public
declarations bring the foundational-axiom audit to 793. The mutation gate
protects the dimension factor, inverse matrix and constant, entrywise source,
and final operator envelope.

### Stage F5c34 inner-box limiting-Jacobian variation

`LeadingJacobianVariation.lean` proves a symmetric reciprocal-power
perturbation lemma and its `w*t^{-p}` product form, then instantiates them on
the exact radius-`10^{-6}` branch box.  It first checks that the limiting
Jacobian at `branchCenter` is literally `gaugeJacobianReal`.  Every one of
the sixteen entries is then enclosed uniformly by

`|DF_limit(y)_(i,j)-DF_limit(center)_(i,j)| <= 1/50000`,

and the four-row operator conversion yields the whole-box bound `1/12500`.
All bounds are rational and symbolic; no sample grid is involved. Six public
declarations bring the foundational-axiom audit to 799. The mutation gate
protects the inner radius, reciprocal and product producers, center identity,
entry envelope, and operator-norm consumer.

### Stage F5c35 elementary whole-box contraction

`ElementaryContraction.lean` verifies the missing inverse order
`P*DF_limit(center)=I`, differentiates the fixed-inverse Newton map, and
identifies its derivative exactly as

`P*(DF_limit(center)-DF_elementary(y,e,x))`.

The finite-scale operator estimate and inner-box variation are combined and
multiplied by the audited `||P|| <= 304/3`.  At the explicit threshold
`e+x <= 10^{-8}`, the resulting defect is below `1/2` on every point of the
closed inner box. Lean therefore constructs the actual
`FourJacobianIntervalCertificate` for the elementary map plus an arbitrary
parameter-independent saddle vector. Nine public declarations bring the
foundational-axiom audit to 808. The mutation gate protects the inverse
order, Fréchet producer, both operator sources, fixed inverse, scale
threshold, and final typed certificate.

### Stage F5c36 elementary center residual and positive branch

`ElementaryResidualBranch.lean` converts the componentwise fixed-box value
estimate into the genuine branch-space sup-norm bound at the exact rational
center. Using the already verified identity
`F_limit(branchCenter)=0`, Lean separates the center residual as

`(F_elementary-F_limit) + (S_exact-S_limit)`.

Consequently an independently supplied exact-xi saddle enclosure
`||S_exact-S_limit|| <= epsilon`, together with the explicit rational budget

`10000*(e+x/e)+epsilon <= (3/608)*branchInnerRadius`,

constructs the actual `FourResidualIntervalCertificate`. Combining it with
the whole-box Jacobian certificate from Stage F5c35 then constructs a locally
unique `PositiveParameterBranch`; existence is no longer an input premise.
The exact-xi saddle estimate remains visibly isolated as the next analytic
instantiation target. Four public declarations bring the foundational-axiom
audit to 812. The mutation gate protects the fixed-box producer, center-zero
identity, saddle sign, both rational budgets, and both typed certificate
consumers.

### Stage F5c37 exact-xi finite certificate and branch

`ExactXiBranch.lean` exposes the four normalized finite-difference
inequalities for orders two through five with their exact signs and factors
`nL`, `n^2 L/2`, `n^3 L/2`, and `n^4 L/6`. Lean proves that these four
scalar enclosures are precisely a sup-norm enclosure of
`exactXiSaddleParameterMap-leadingXiSaddleVector`.

The certificate then instantiates Stage F5c36 at `x=1/n`, `e=1/L` and uses
the exact elementary/xi decomposition at every point of the inner box. The
result is a locally unique `PositiveParameterBranch` for the actual
`exactXiParameterMap`, not merely for an affine surrogate. The four analytic
finite-difference inequalities remain explicit inputs for the next
coefficient-log instantiation. Three audited declarations bring the
foundational-axiom audit to 815. The mutation gate protects all four signs
and scales, the saddle-norm bridge, the exact decomposition, and the final
branch consumer.

### Stage F5c38 direct positivity of the xi coefficients

`XiCoefficientPositivity.lean` discharges the real-log branch condition that
was previously only implicit in the integral definition. Each differentiated
theta mode is proved strictly positive for `t>=1` using the exact mode
formula and `pi>3`; the already verified first- and second-mode summability
then makes the omega kernel strictly positive on that half-line.

After the logarithmic substitution this gives
`omegaLogAmplitude(u)>0` for every `u>=0`. Its existing integrability theorem
and a support-measure argument prove the defining omega moment is strictly
positive, hence `riemannXiCoefficientReal(n)>0` for every natural `n`.
Thus every `Real.log` in `exactXiCoefficientLog` is now applied to a proved
positive value. Five declarations bring the foundational-axiom audit to 820.
The mutation gate protects the pi bound, both summability sources, theta-sum
identity, support integral, and final coefficient positivity theorem.

### Stage F5c39 integer/holomorphic coefficient-log bridge

`XiCoefficientLogBridge.lean` uses Stage F5c38 positivity to fix the
principal logarithm at every positive integer. Lean proves that the real
`exactXiCoefficientLog(m)`, cast to `C`, is literally
`Log(complexXiCoefficientMoment(m))`; the proof passes through the exact T1
integer specialization and the real centered-xi coefficient identity.

The module then transports the second difference and its zeroth through
third forward differences to explicit complex-valued formulas. All binomial
coefficients and signs are retained by equality, giving the analytic
coefficient estimates a direct typed path to the coefficient-log part of
the four fields of `ExactXiSaddleIntervalCertificate`; Stage F5c43 restores
the exact Gamma half-shift before the analytic instantiation. Nine declarations bring the
foundational-axiom audit to 829. The mutation gate protects the integer
specialization, positivity and principal-log sources, and every forward-
difference sign and coefficient.

### Stage F5c40 repeated-FTC forward-difference calculus

`ForwardDifferenceCalculus.lean` defines the recursive complex unit-step
forward difference and proves that it commutes with every level of a global
complex derivative tower. Repeated application of the complex line-segment
fundamental theorem then proves the quantitative adapter

`||Delta^q f^(r)(z)-c|| <= M`

from the uniform derivative estimate `||f^(r+q)(w)-c|| <= M`. The averaging
interval has mass one, so there is no factorial loss. This is the exact
calculus interface needed to turn holomorphic coefficient-log derivative
estimates into the four finite fields of
`ExactXiSaddleIntervalCertificate`; the coefficient-sector localization is
the next instantiation checkpoint. Four audited declarations bring the
foundational-axiom audit to 833. The mutation gate protects the recursive
sign, derivative-tower source, complex FTC producer, constant subtraction,
and final no-loss norm estimate.

### Stage F5c41 coefficient-interval localization

`LocalForwardDifferenceCalculus.lean` removes the global-domain hypothesis
from Stage F5c40. Lean first proves a unit-segment FTC whose derivative input
is needed only on the integration interval, then proves that a forward
difference commutes with a derivative tower whenever its finitely many real
translates lie in the local domain. The resulting quantitative theorem uses
derivative information only on `[x,x+q]` and retains the same constant with
no factorial loss.

This is the domain-correct adapter for the manuscript: the four xi finite
differences use only real nodes between `n` and `n+5`, while holomorphy is
known on the surrounding coefficient sector. Four audited declarations
bring the foundational-axiom audit to 837. The mutation gate protects the
real-segment identity, localized FTC hypothesis, finite translate condition,
local interval, derivative order, constant subtraction, and unit interval
mass.

### Stage F5c42 xi logarithmic-error forward differences

`XiLogErrorForwardDifferences.lean` instantiates the localized repeated-FTC
adapter for the actual holomorphic error in `Log M_z`. Lean proves the
enormous manuscript cutoff is above `10000`, so every real point from `n`
through `n+5` lies in the inner `n/2000` Cauchy disc. It upgrades sectorial
differentiability to an analytic derivative tower and then applies the
uniform half-disc Cauchy estimate at every point of that finite interval.

Consequently, for every `q <= 5`, the norm of the order-`q` forward
difference of `manuscriptXiLogRelativeError` is at most

`q! * (3/2 * manuscriptCauchyEpsilon n) /
  manuscriptInteriorCauchyRadius n^q`.

This is a concrete kernel-checked contribution to each of the four exact-xi
finite fields, with the coefficient-sector domain and branch of the complex
log explicit. Five audited declarations bring the foundational-axiom audit
to 842. The mutation gate protects the cutoff proof, analytic tower,
`n`-through-`n+5` domain bridge, inner Cauchy radius, local FTC consumer, and
final derivative bound.

### Stage F5c43 exact quotient/Gamma seam correction

The staged coefficient-log instantiation exposed a release-blocking defect
in the earlier Lean evidence map. The paper and the Phase-8 source note use

`Q_(n,k) = halfShift - Delta^2 log M = -Delta^2 log gamma`,

but `ExactParameterMap.lean` had substituted `log gamma` for `log M` inside
the first expression, thereby counting the half-shift twice. The corrected
exact residual is now definitionally

`exactJacobiLogQuotient + Delta^2 log gamma`.

`ExactParameterDecomposition.lean` introduces the exact auxiliary coordinate

`exactXiAuxiliarySecondDiff = halfShift + Delta^2 log gamma`

and proves the corrected whole-box split into the five-boundary elementary
map plus that auxiliary-moment coordinate. `ExactXiBranch.lean` now requires
its four interval fields for this corrected coordinate. Thus the limiting
constants `(-2,-1,-2,-2)` are attached to `Log M_z`, exactly as in the
manuscript, rather than incorrectly to `log gamma` alone.

This correction supersedes the formulas recorded in Stage F5c31 and the
coefficient-only wording in Stage F5c39. One new definition brings the
foundational-axiom audit to 843. The strengthened mutation gates reject
reversal of the true quotient sign, removal of the Gamma half-shift, or
reconnection of the certificate to the coefficient-only second difference.

### Stage F5c44 exact auxiliary-moment integer log bridge

`XiAuxiliaryLogBridge.lean` proves the exact Gamma-duplication seam that the
corrected certificate requires. Lean defines the positive real factorial
ratio `m!/(2m)!` and the corresponding real auxiliary moment, identifies
their complexifications with `complexFactorialRatio(m)` and
`complexXiAuxiliaryMoment(m)`, and proves positivity at every positive
integer. The principal complex logarithm therefore agrees with the real
auxiliary-moment logarithm at every sampled node.

The exact recurrence

`factorialRatio(m+1) = factorialRatio(m) / (2*(2m+1))`

is proved from factorial identities. Its second logarithmic difference is
exactly the negative half-shift. Hence Lean obtains

`halfShift + Delta^2 log gamma = Delta^2 log M`

at positive integers and transports its zeroth through third forward
differences without changing signs or coefficients. These are now literally
the four sampled auxiliary-log expressions required by the corrected
`ExactXiSaddleIntervalCertificate`. Fourteen audited declarations bring the
foundational-axiom audit to 857. The mutation gate protects the factorial
recurrence, positivity, coefficient/auxiliary product, half-shift
cancellation, principal-log branch, and all four forward-difference bridges.

### Stage F5c45 natural Gamma-free auxiliary factorization

`XiNaturalAuxiliaryFactorization.lean` removes the coefficient Gamma
quotient before any logarithmic differentiation. Lean defines the natural
auxiliary main as

`dyadicScale * saddleMomentMain(N) * (c(N)-L_N^2)`

and derives its exact factorization directly from the two shifted theta
moments. The quotient-defined relative error is proved literally equal to
the existing moment/two-shift error, rather than to the larger coefficient
error containing the now-cancelled Gamma correction. The main is nonzero,
both main and error are holomorphic on the paired coefficient sector, and
the sharper moment-only logarithmic rate is inherited unchanged. Nine
audited declarations bring the foundational-axiom audit to 866. The
mutation gate protects the dyadic factor, the sign of `c-L^2`, the direct
two-shift producer, exact error identity, holomorphy, and bound producer.

### Stage F5c46 natural auxiliary logarithmic error

`XiLogError.lean` now exposes the cutoff calculation as a reusable theorem:
the entire displayed coefficient-error envelope is at most `1/2` on the
paired sector. `XiNaturalLogError.lean` proves that the sharper Gamma-free
moment error lies under that envelope. Therefore `1+error` is nonzero with
strictly positive real part on the whole sector, so its principal logarithm
is a single holomorphic branch. Lean proves its exact exponential identity
and the bound `|Log(1+error)| <= (3/2)|error|`. Nine audited declarations
bring the foundational-axiom audit to 875. The mutation gate protects the
shared cutoff, constant comparison, nonzero and right-half-plane branches,
exponential identity, holomorphy, and logarithmic norm producer.

### Stage F5c47 natural-log Cauchy and forward-difference transport

`XiNaturalLogErrorForwardDifferences.lean` defines the moment-only
proportional-disc envelope and proves it uniformly on the original
`x/1000` coefficient disc. A second `x/2000` disc about every point of the
inner half-disc stays inside that domain. Cauchy's theorem therefore bounds
all derivatives of the natural logarithmic error through order six with the
exact factorial and radius powers. The localized repeated-FTC theorem then
converts those derivative estimates into unit forward-difference bounds for
every order through five on the actual integer interval `n,...,n+5`. Six
audited declarations bring the foundational-axiom audit to 881. The mutation
gate protects the moment-only constant, shifted-sector geometry, nested
discs, Cauchy producer, holomorphic derivative tower, five-node domain, and
localized FTC consumer.

### Stage F5c48 explicit branch-safe auxiliary logarithm

`XiNaturalLogMain.lean` factors the two-shift denominator as
`16(N+2)(N+1)(1-L_N^2/c_N)`. The final factor is proved within `1/2` of one
on the paired sector and hence lies in the open right half-plane. Lean then
constructs a branch-safe sum of logarithms and proves that its exponential is
exactly `c_N-L_N^2`. Adding the dyadic exponent and the already verified
saddle-moment logarithm gives an explicit holomorphic logarithm of the
natural auxiliary main. Adding the natural logarithmic error produces a
holomorphic function whose exponential is the exact auxiliary moment, with
no Gamma quotient or untracked branch choice. Thirteen audited declarations
bring the foundational-axiom audit to 894. The mutation gate protects every
factor, the cancellation sign and branch, the saddle log, both exponential
identities, the exact factorization source, and holomorphy.

### Stage F5c49 positive-real saddle and integer logarithm bridge

`PositiveRealSaddle.lean` proves that the contraction-selected saddle is
real on the positive real axis. The comparison center and saddle equation
are invariant under conjugation, conjugation preserves the certified closed
disc, and the contraction theorem's in-disc uniqueness identifies the
conjugate root with the selected root. This is a proof from the existing
quantitative branch, not a new branch-selection assumption.

`XiNaturalLogIntegerBridge.lean` propagates that reality through the leading
phase, curvature, Gaussian determinant, two-shift factor, and natural
auxiliary main. The main is strictly positive. At positive integer nodes,
the exact auxiliary moment is also strictly positive, so the quotient error
factor and its principal logarithm are real. Lean then uses the exact
exponential identity and injectivity of the real exponential to prove that
the constructed analytic logarithm equals the discrete principal logarithm,
not merely modulo `2*pi*i`.

The equality is transported through the auxiliary second difference and
all four certificate coordinates. The last theorem explicitly requires the
six nodes `n,...,n+5` to lie in the paired coefficient sector, so no domain
condition is hidden. Twenty-one audited declarations bring the
foundational-axiom audit to 915. The mutation gate protects conjugation
invariance, in-disc uniqueness, positivity, the exact exponential source,
the principal-log identification, and the six-node forward-difference
bridge.

### Stage F5c50 exact certificate decomposition

`XiNaturalLogCertificateDecomposition.lean` discharges the six separate
integer-sector premises from one explicit lower bound
`exp(leanSaddleCutoff+2)<n`. The proof puts each positive integer center in
the already certified proportional coefficient disc and then transports the
left-endpoint bound monotonically to `n,...,n+5`.

The exact auxiliary second difference is identified with the order-two
complex forward difference of the branch-fixed analytic logarithm. Forward
difference linearity then splits all four real certificate coordinates
exactly into orders two through five of the explicit natural main plus the
same orders of the holomorphic logarithmic error. The latter four terms are
simultaneously bounded by the existing localized Cauchy/FTC theorem, with
the exact factorial and radius powers displayed in the theorem statement.

Thus no sector membership, branch choice, sign, or finite-difference
coefficient remains implicit at the analytic/discrete seam. Seven audited
declarations bring the foundational-axiom audit to 922. The mutation gate
protects the six-node domain producer, proportional-disc source, linearity,
second-difference identification, integer bridge, order-five endpoints, and
all four error-bound consumers.

### Stage F5c51 lower natural-main derivative tower and FTC adapter

Four new modules formalize the lower-order saddle contribution needed by the
remaining finite xi certificate. `SaddleLowerOrders.lean` freezes the exact
reduced rational functions `H2,...,H5`, their central values
`(1,-1,2,-6)`, exact coefficientwise numerator majorants, and conservative
whole-bidisc norm bounds. `SaddleLowerOrderLimits.lean` then checks the four
denominator-cleared error polynomials and proves on the exact tiny bidisc
`|r|,|sigma| <= 10^-7` that every reduced value lies within `2*10^-6` of
its limiting constant.

`MovingSaddleLowerOrders.lean` puts the contraction-selected saddle into that
bidisc from two explicit scalar rate inequalities and transports the four
limits to the normalized derivatives of the displayed `G0`. As at order six,
the base symbolic identification is a named four-equality record: it is the
specific seam independently checked by SymPy and Mathematica, not a hidden
Lean theorem or a claim that Lean re-derived the CAS tower.

`XiNaturalMainLowerForwardDifferences.lean` exposes the exact affine-chain
factors `4,8,16,32`, separates the actual natural-main derivatives into the
moving-saddle term and an explicit correction term, and combines separate
saddle/correction budgets by a kernel-checked triangle inequality. A
localized repeated-FTC theorem then transports uniform pointwise estimates on
the complete interval `[n,n+5]` to the four forward differences without a
factorial loss. The primitive interval budgets remain to be constructed in
the next checkpoint; this stage does not instantiate them by assumption.

Seventy-eight audited declarations bring the foundational-axiom audit to
exactly 1000 declarations. The mutation gate rejects changed limiting signs,
weakened radii, removal of the CAS seam, altered chain factors, disconnected
correction terms, loss of either error budget, or replacement of the local
FTC consumer.

### Stage F5c52 effective lower-xi interval budgets

`SaddleLowerOrderLimits.lean` now supplies the final exact rational bidisc
`|r|,|sigma| <= 10^-14`, on which all four reduced saddle coordinates are
within `10^-12` of `(1,-1,2,-6)`.  The rate-to-box theorem in
`MovingSaddleLowerOrders.lean` is parameterized by explicit inverse,
`sigma`, and scale-ratio inequalities, and its final specialization produces
the normalized target constants `(-2,-1,-2,-2)`.

`XiNaturalMainCorrectionBounds.lean` proves that the denominator in the
displayed `G0` is curvature times the square of the selected saddle and lies
in the open right half-plane.  It then cancels the large saddle terms from
the natural-main remainder exactly, proves logarithmic size on proportional
discs, and applies Cauchy's theorem through order five.  The resulting four
correction identities consume the named `ManuscriptG0LowerIdentification`;
Lean does not claim to have re-derived that frozen symbolic tower.

`XiNaturalMainIntervalBudgets.lean` collects seven explicit endpoint
inequalities.  From them Lean proves uniform membership of all six samples,
the four saddle estimates, four correction estimates, and four logarithmic-
error estimates with separate budgets of `10^-10`.  The exact natural-log
decomposition is then used to construct
`ExactXiSaddleIntervalCertificate n (xiNaturalSaddleScale n) (3*10^-10)`.
This is a conditional constructor from the seven displayed scalar endpoint
inequalities and the disclosed four-equality symbolic identification; it is
not yet a proof that a particular numeral `n` satisfies those hypotheses.

Fifty-two new audited declarations bring the foundational-axiom audit to
exactly 1052 declarations.  The new semantic gate rejects weakened final
radii, disconnected curvature or cancellation identities, an order-five
Cauchy scale error, omission of the logarithmic endpoint inequality, hiding
the symbolic seam, disconnection of the exact auxiliary-log decomposition,
or removal of the final certificate constructor.

Serial verification on 2026-08-19 passed the full Jensen-wedge Lean umbrella,
the Phase 26 verifier and 1052-declaration axiom audit, and the downstream
Phase 25, Phase 24, Phase 21, and Phase 20 verifiers.  The Phase 20 run
included its independent whole-library `leanchecker` replay.  These are
machine checks and AI-maintained review gates; no human or peer review is
claimed.

### Stage F5c53 explicit cutoff and exact lower-xi branch

`XiNaturalExplicitBranch.lean` discharges all seven scalar endpoint
conditions from the single explicit cutoff
`n >= ceil(exp(10^15)) + 1`.  Exact elementary logarithm and square-root
bounds prove the remote-sector, inverse, reduced-coordinate, scale-ratio,
natural-main correction, and holomorphic log-error budgets.  The resulting
kernel theorem constructs
`ExactXiSaddleIntervalCertificate n (xiNaturalSaddleScale n) (3*10^-10)`
with no residual asymptotic premise.

The same cutoff proves the two contraction side conditions: the inverse
saddle scale is at most `1/(5*10^14)`, the scale-to-index ratio is at most
`8*10^-40`, and the reciprocal index is at most `10^-160`.  Lean therefore
constructs `PositiveParameterBranch` for the exact normalized xi parameter
map.  Its one non-Lean mathematical input is still named in the theorem:
`XiNaturalLowerCASCertificate`, the four displayed lower derivative
identities packaged through `ManuscriptG0LowerIdentification`.  Those
identities have independent SymPy and Mathematica corroboration, but this
stage does not claim that Lean re-derived the decisive symbolic tower.

Eleven audited declarations bring the foundational-axiom audit to exactly
1063 declarations.  The semantic gate rejects a reduced cutoff, removal of
the strict successor or fixed power bound, any disconnected endpoint field,
hiding the CAS seam, bypassing the exact certificate, changing the fixed
branch scales, or disconnecting the final positive-branch constructor.
These are machine checks and AI-maintained gates; no human or peer review is
claimed.

Serial verification on 2026-08-20 passed the Jensen-wedge umbrella, the
Phase 26 verifier and 1063-declaration axiom audit, and the downstream Phase
25, Phase 24, Phase 21, and Phase 20 verifiers.  Phase 20 included its
independent whole-library `leanchecker` replay.

### Stage F5c54 kernel moving-saddle derivative identification

`MovingSaddleDerivativeIdentification.lean` removes the last external
symbolic-algebra premise from the explicit lower-xi branch.  Lean now
differentiates every frozen bivariate monomial, proves the two-variable chain
rule, derives the exact reduced numerator recurrence, and verifies the four
table transitions `H2 -> H3 -> H4 -> H5 -> H6` by denominator-cleared ring
identities.  It also derives the scaled curvature identity, the derivatives
of the inverse-saddle and saddle-ratio coordinates, and the first two
derivatives of the displayed moving-saddle logarithm.  Induction through the
generic reduced derivative then identifies its second through sixth iterated
derivatives with the frozen `H2,...,H6` formulas.

The kernel theorems construct both `ManuscriptG0LowerIdentification` and
`ManuscriptG0SixthIdentification` on the full Lean saddle sector.  At the
explicit cutoff, sector membership therefore constructs the uniform
six-sample lower identification automatically.  Consequently
`exactXiSaddleIntervalCertificate_of_explicitCutoff` and
`exactXiPositiveParameterBranch_of_explicitCutoff` no longer accept a CAS or
other symbolic-identification argument.  The SymPy and Mathematica results
remain independent corroboration, not premises.

Forty-four new audited declarations bring the foundational-axiom audit to
1107 declarations.  A new semantic gate rejects changes to either monomial
derivative, the recurrence sign or exponent factor, the `H2` and `H5` table
transitions, the curvature identity, the inverse-saddle and generic reduced
derivatives, the base second derivative, or either final identification
producer.  The explicit-branch gate now rejects reintroduction or
disconnection of the kernel producer.  The narrow modules, the full
Jensen-wedge umbrella, both mutation gates, and the 1107-declaration audit
pass.  These are kernel and machine checks; no human or peer review is
claimed.

### Stage F5c55 exact transformed-xi and six-coefficient comparison

`XiNaturalTransformedPolynomial.lean` fixes the paper's actual normalized
polynomial literally as the Riemann-xi Jensen polynomial evaluated at the
negative, positively scaled variable and divided by the positive base
coefficient.  The scale is the exact product `B R_1`; Lean proves its
positivity and constructs the complete `XiCoefficientEstimate` record from
the defining equality.  The comparison polynomial is fixed at the same
branch parameters as the genuine terminating
`_3F_2(-d,A,C;B,D;(D/(AC))X)` polynomial.

`XiNaturalSixCoefficientMatch.lean` then closes the quotient-to-coefficient
seam.  The exact four quotient residuals are proved to be the differences of
the actual and model logarithmic second differences.  The constant
normalization and `S=B R_1` supply the first two coordinates, so the existing
kernel six-coefficient adapter turns a zero of the exact xi parameter map
into equality of logarithmic coordinates zero through five.  Lean also
proves positivity of `A,B,C,D`, exponentiates the model increments, derives
the alternating-binomial recurrence, and inducts on the finite coefficient
index.  Consequently the model log polynomial is exactly the terminating
`_3F_2` comparison polynomial, not an unconnected intermediate definition.
At the explicit xi cutoff, the kernel-produced positive branch therefore
matches the first six coefficients of the actual transformed xi polynomial
directly with the published comparison polynomial.

Forty-four new audited declarations bring the foundational-axiom audit to
exactly 1151 declarations.  The semantic gate rejects changes to the scale,
variable sign, hypergeometric argument, log-coordinate signs, quotient
adapter, parameter positivity, exponentiated increment, alternating choose
step, terminating recursion, polynomial identity, actual evaluation, direct
six matches, or explicit-cutoff specialization.  Serial verification on
2026-08-20 passed the full Jensen-wedge umbrella, Phase 26, Phase 25, Phase
24, Phase 21, and Phase 20.  Phase 20 included its independent whole-library
`leanchecker` replay.  These are kernel and machine checks; no human or peer
review is claimed.

### Stage F5c56 exact finite-free specialization and root localization

`XiNaturalFiniteFreeSpecialization.lean` specializes the finite-free layer
to the paper's actual comparison polynomial. Lean defines both normalized
Jacobi factors coefficient by coefficient, proves their exact scaling law,
derives the finite-free convolution coefficient, and identifies that
convolution with the terminating `_3F_2` comparison polynomial. Combined
with Stage F5c55, this ties the concrete xi comparison directly to the
finite-free operation rather than leaving the operation behind an abstract
polynomial alias.

The remaining classical root inputs are now isolated in two narrow typed
records: the general Jacobi root bounds plus MMP root producer, and the MSS
finite-free interval theorem. Assuming only those named literature inputs,
Lean scales the second Jacobi interval, consumes the MSS product interval,
and derives the corrected `12 + 8*sqrt 6` localization bound. It also proves
the `B,D >= 256d` and `B <= 6D` geometry from the explicit xi branch and
shows that the exact two-thirds wedge with `K >= 2*256^3` supplies
`n >= 256d`. Thus the explicit-cutoff theorem instantiates every
normalization, branch-box, parameter, and localization inequality
internally; no root-localization certificate is assumed.

Thirty audited declarations bring the foundational-axiom audit to exactly
1181 declarations. Thirteen fail-closed mutations protect the factor
scaling, convolution, terminating `_3F_2` identity, concrete xi identity,
typed MSS/MMP boundary, product interval, corrected localization constant,
coarse geometry, wedge constant, and explicit-cutoff consumer. The Lean
module and Jensen-wedge umbrella compile cleanly. These are kernel and
machine checks; no human or peer review is claimed.

Serial verification on 2026-08-20 passed Phase 26 and the downstream Phase
25, Phase 24, Phase 21, and Phase 20 verifiers. Phase 20 included its
independent whole-library `leanchecker` replay.

### Stage F5c57 complete finite critical-radius maximum

`CriticalRadiusRecurrence.lean` closes the finite maximum argument that
turns an exact four-term derivative recurrence into the paper's global
critical-radius estimate. Lean constructs the actual supremum over
`0,...,d`, chooses an attaining index, handles the endpoint
`T_(d+1)=0`, and proves that the denominator-free coefficient budget is a
strict contraction. The resulting theorem gives `|T_k| <= R^k` for every
`k <= d`; there is no unrecorded maximum or terminal-index premise.

The certificate deliberately exposes the genuine recurrence, positivity of
its center coefficient, and the explicit coefficient contraction as fields.
The next specialization must discharge those fields from the already proved
terminating `_3F_2` ODE and the xi parameter inequalities; this checkpoint
does not pretend that specialization is complete. Six new audited
declarations bring the foundational-axiom audit to exactly 1187
declarations. Ten fail-closed mutations protect the actual finite supremum,
terminal case, recurrence, center positivity, coefficient contraction, and
final radius conclusion. These are kernel and machine checks; no human or
peer review is claimed.

### Stage F5c58 genuine terminating-polynomial radius adapter

`Terminating3F2CriticalRadius.lean` connects the complete maximum theorem to
the paper's actual terminating `_3F_2` polynomial. Lean transports the
shifted derivative polynomial back to the original derivative jet, consumes
the finite Euler ODE and the four exact coefficient identifications, and
proves the recurrence for
`y^k p^(k)(y) / p(y)` literally. It also proves degree termination,
`T_0=1`, and `T_1=0` at a critical point, then constructs the complete
critical-radius certificate.

The remaining hypotheses are now only the explicit coefficient inequalities
and their parameter geometry; no recurrence or derivative-normalization seam
remains. Nine new audited declarations bring the foundational-axiom audit to
exactly 1196 declarations. Ten fail-closed mutations protect the normalized
ratio, derivative shift, ODE producer, coefficient identification,
termination, critical base case, certificate constructor, and final radius
consumer. These are kernel and machine checks; no human or peer review is
claimed.

### Stage F5c59 explicit critical-radius coefficient budgets

`CriticalRadiusCoefficientBounds.lean` discharges the paper's four concrete
recurrence inequalities from an explicit positive parameter box. Lean proves
`P_2 >= n/8`, `|P_3| <= 2`,
`|P_1| <= 96(n S + n d)`, and `|P_0| <= 48 n^2 d`. The `P_1` proof uses the
decomposed coefficient and kernel-checks the cancellation through `B-y`;
it does not estimate the two order-`n^2` expanded terms separately.

The module then assigns separate `1/8`, `1/2`, and `1/8` budgets to the
three neighboring terms at `R=4096 S`, obtains a strict `3/4` contraction,
and instantiates the complete finite maximum theorem for the genuine
terminating `_3F_2` derivative ratios. The remaining radius seam is geometric:
derive this concrete box and the localization of every critical point from
the already formalized xi finite-free root interval and wedge inequalities.
Twelve new audited declarations bring the foundational-axiom audit to
exactly 1208 declarations. The source contract has dedicated fail-closed
mutations for the central, cubic, linear, constant, and contraction constants
and for the decomposed `P_1` cancellation. These are kernel and machine
checks; no human or peer review is claimed.

### Stage F5c60 xi critical-point localization and radius closure

`XiNaturalCriticalRadius.lean` closes the geometric specialization left by
F5c59. A generic Lean theorem shows that a non-root real critical point of a
degree-at-most-`d` polynomial lies between `d` supplied distinct real roots:
the proof identifies the complete root multiset and uses the exact
logarithmic-derivative sum, whose sign is strict outside the root interval.
The typed MMP root list therefore transfers the already proved finite-free
root localization to every comparison critical point.

The module then derives the `A,B,C,D` parameter box from the exact xi branch,
proves `524288 sqrt(Bd) <= n` from the explicit fixed wedge constant
`2 * 824633720832^3`, and instantiates the F5c59 certificate. The final theorem
gives the paper's literal normalized derivative radius
`|y^k p_F^(k)(y)/p_F(y)| <= (4096 sqrt(Bd))^k` at every non-root critical
point. The only classical inputs are the same explicitly typed Jacobi, MSS,
and MMP records already isolated at the literature boundary; no additional
paper or asymptotic premise is introduced.

Nine new audited declarations bring the foundational-axiom audit to exactly
1217 declarations. Dedicated fail-closed mutations protect completeness of
the root list, the logarithmic-derivative sign argument, critical-point
localization, the wedge and scale constants, the exact branch-box consumer,
and the final normalized radius theorem. These are kernel and machine checks;
no human or peer review is claimed.
