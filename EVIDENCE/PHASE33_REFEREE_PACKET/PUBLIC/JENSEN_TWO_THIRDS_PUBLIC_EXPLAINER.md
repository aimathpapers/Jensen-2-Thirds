# Six Matches and a Wider Wedge: A New Route Through the Jensen Polynomials of Riemann's Xi-Function

## A public-facing account of an extensively checked and substantially formalized—but not human-reviewed—proof candidate

There is a familiar temptation whenever the Riemann hypothesis enters a
story: to skip straight to the ending. Has the hypothesis been proved? Has a
new zero been found? Has some hidden door into the distribution of prime
numbers finally opened?

That is not the story here.

The work described in this article concerns a family of polynomials built
from the Taylor coefficients of Riemann's xi-function. These polynomials are
part of a long-established way to study the shape of the xi-function without
attacking its zeros head-on. The new proof candidate enlarges a region in
which those polynomials are predicted to have only real, simple roots. In the
language of the subject, it proposes a **two-thirds hyperbolicity wedge**.

The distinction matters. If the candidate is correct, it would be a genuine
advance in the theory of Jensen polynomials associated with the xi-function.
It would not prove the Riemann hypothesis, locate new zeros of the zeta
function, or improve a known percentage of zeros on the critical line.

There is another important qualification. The argument has been checked in
several unusually elaborate ways: portions are formalized in the Lean proof
assistant; decisive symbolic calculations have been reproduced exactly in
both SymPy and Mathematica; interval and numerical regressions have been run;
and separate AI systems have carried out analytic and algebraic adversarial
reviews. The complete analytic coefficient chain through six derivatives is
now formalized in Lean, along with substantial downstream algebra and
localization. But no human mathematician has reviewed it. The honest
description is therefore **an extensively checked and substantially
formalized proof candidate, not a peer-reviewed theorem**.

With that status made clear, the mathematical idea is worth explaining. It
is a story about translating an infinite and mysterious function into finite
polynomials, designing a better polynomial model, and gaining a new exponent
by forcing one additional layer of cancellation.

## From the zeta function to a more symmetrical object

The Riemann zeta function begins, for real numbers greater than one, with the
innocent-looking series

\[
  \zeta(s)=1+\frac1{2^s}+\frac1{3^s}+\frac1{4^s}+\cdots.
\]

Its analytic continuation carries vastly more information than this series
suggests. Its nontrivial zeros govern the fine fluctuations in the
distribution of the prime numbers. The Riemann hypothesis says that all of
those nontrivial zeros lie on one vertical line in the complex plane.

For many purposes it is better to package the zeta function together with
gamma factors and elementary terms into Riemann's completed xi-function.
This completed function is entire—there are no poles to manage—and it has a
beautiful reflection symmetry. After shifting the center of symmetry to the
origin, one obtains an even Taylor expansion. In the normalization used in
this project,

\[
  \xi\!\left(\frac12+w\right)
    =\sum_{n\ge 0}\frac{\gamma(n)}{n!}w^{2n}.
\]

The numbers \(\gamma(n)\) are real and positive. They are not the zeros of
the zeta function. They are coefficients encoding the whole xi-function,
rather as the genetic sequence of a plant encodes a shape that only becomes
visible after growth.

The central question is how much of the global geometry of xi is already
visible in finite patterns among these coefficients.

## Jensen polynomials: finite shadows of an infinite function

Given the coefficient sequence \(\gamma(0),\gamma(1),\ldots\), form the
degree-\(d\) Jensen polynomial based at position \(n\):

\[
  J^{d,n}(X)=\sum_{j=0}^{d}\binom dj\gamma(n+j)X^j.
\]

This takes a short window of \(d+1\) consecutive coefficients and mixes them
with binomial weights. The resulting object is an ordinary polynomial, so we
can ask an ordinary geometric question: where are its roots?

A real polynomial is called **hyperbolic** when all of its roots are real.
In this setting the desired conclusion is stronger: all \(d\) roots should
be distinct and negative.

Why is that interesting? Classical work of Jensen and Pólya connects the
real-rootedness of such coefficient polynomials with entire functions that
are limits of real-rooted polynomials. This is one of the great recurring
themes of analysis: infinite analytic structure can sometimes be recognized
through a hierarchy of finite algebraic tests.

But there is a huge logical gap between proving that some asymptotic family
of Jensen polynomials is hyperbolic and proving the Riemann hypothesis. The
Riemann hypothesis concerns the entire zero set of xi. An asymptotic wedge
only controls pairs \((n,d)\) satisfying a growth condition. It is valuable
because it reveals more of the coefficient geometry, not because it closes
the original century-and-a-half-old problem.

## What earlier work established

The modern Jensen-polynomial program was transformed by work of Michael
Griffin, Ken Ono, Larry Rolen, and Don Zagier. Among its consequences is a
remarkable asymptotic phenomenon: for each fixed degree, Jensen polynomials
associated with important sequences—including the xi coefficients—eventually
become hyperbolic and, after rescaling, resemble classical Hermite
polynomials. Later work by Griffin, Ono, Rolen, Jesse Thorner, Zachary Tripp,
and Ian Wagner developed the xi-function setting further.

“Fixed degree” is crucial. It means that one chooses, say, degree 10 and then
moves far enough out in the coefficient sequence. A harder question allows
the degree itself to grow with the base point. How rapidly may \(d\) grow
with \(n\) while hyperbolicity still follows from a uniform proof?

The hash-frozen version of a 2026 preprint by Jonathan Holland supplies an
important growing-degree architecture. In simplified form, its wedge has the
shape

\[
 n^3\log^2(n+2)\ \ge\ Kd^5.
\]

Ignoring logarithmic factors, this permits degrees on the scale
\(d\approx n^{3/5}\). Holland's method combines asymptotics for the xi
coefficients, a carefully chosen hypergeometric comparison polynomial,
finite free convolution, derivative estimates, and a sign-transfer
argument.

The present project began by asking whether that architecture could be
pushed one order further.

Its proposed conclusion is

\[
 n^2\log(n+2)\ \ge\ Kd^3,
\]

which permits, again ignoring constants,

\[
 d\ \lesssim\ n^{2/3}\bigl(\log n\bigr)^{1/3}.
\]

The difference between \(3/5\) and \(2/3\) may look modest. In asymptotic
mathematics it is structural. The allowed degree grows by a genuinely larger
power of \(n\), and the proof requires a new cancellation rather than a
numerical sharpening of old constants.

## The guiding idea: build a better shadow

Suppose you are trying to understand an object too complicated to handle
directly. One strategy is to construct a model whose behavior is already
known, make the model agree with the object to high order, and then prove
that the remaining error cannot alter the feature you care about.

Here the complicated object is the actual Jensen polynomial of the xi
coefficients. The model is a terminating hypergeometric polynomial assembled
from two Jacobi-polynomial factors. Jacobi polynomials are classical and
their roots are exceptionally well behaved: under the right parameter
conditions, all roots are positive and simple.

The two factors are combined through a multiplicative operation from finite
free probability. This operation preserves the relevant real-rootedness and
allows the roots of the product model to be localized.

Four positive parameters control the model. Their job is to make the model's
coefficient pattern match the xi coefficient pattern. The central innovation
is to force **six consecutive coefficient matches**.

It helps to picture two curves meeting. If they share only a value, they may
separate immediately. If they share a value and a slope, they remain close a
little longer. If they also share curvature and several higher derivatives,
their separation is postponed to still higher order. The same principle
operates here, though the matching is expressed through logarithmic
coefficient quotients rather than ordinary derivatives.

The proof uses four quotient equations plus two normalizations. Together
they force agreement at six consecutive coefficient positions. A short
finite-difference argument shows why: once the difference sequence starts
with two zeros and its next four second differences vanish, all six entries
must vanish.

That elementary adapter has been formalized in Lean.

## Why one additional match changes the exponent

The sixth match is not decorative. It moves the first uncontrolled term to
sixth order.

Let \(E(z)\) represent the logarithm of the ratio between the actual
coefficient model and the comparison model. The six matches say

\[
  E(0)=E(1)=\cdots=E(5)=0.
\]

A complex version of Newton interpolation, expressed through the
Hermite–Genocchi formula, then bounds \(E(z)\) by a sixth derivative times
the six-factor product

\[
  z(z-1)(z-2)(z-3)(z-4)(z-5).
\]

The argument must control this error not merely on the real interval from 0
to \(d\), but in a complex neighborhood whose radius is governed by the
critical points of the comparison polynomial. The direct recurrence gives a
radius of the approximate size

\[
  \rho\asymp\sqrt{nd}.
\]

Six product factors therefore contribute roughly

\[
  \rho^6\asymp n^3d^3.
\]

On the analytic side, the sixth logarithmic derivative of the xi coefficient
model is of size roughly

\[
  \frac{1}{n^5\log n}.
\]

Multiplying these scales gives

\[
  \frac{n^3d^3}{n^5\log n}
  =\frac{d^3}{n^2\log n}.
\]

That quotient must be small. Rearranging it produces exactly the proposed
two-thirds wedge

\[
  n^2\log(n+2)\ge Kd^3.
\]

This is the conceptual heart of the project. The new exponent is the visible
trace of a sixth-order cancellation.

## Finding the four model parameters

For the strategy to work, the comparison polynomial must stay in a safe
region where both Jacobi factors have positive, simple roots. The four model
parameters cannot merely exist abstractly; they must form a positive branch
with quantitative margins.

After rescaling, the limiting matching equations have the exact positive
solution

\[
  (\alpha,t,w,\delta)=\left(3,2,\frac{16}{3},\frac13\right).
\]

The Jacobian determinant at this point is \(-1/144\), so the system is
nonsingular. A fixed-inverse contraction argument then produces a nearby
solution for sufficiently large \(n\). Exact interval checks keep the branch
inside a rational parameter box and prove the required ordering of the four
hypergeometric parameters.

The most delicate estimates here come from logarithms of gamma-function
ratios. Repeated applications of the fundamental theorem of calculus turn
their finite differences into integrals over unit cubes. Those cube
integrals make signs and derivative bounds transparent and prevent a
spurious logarithmic loss.

Lean now verifies both Fubini orientations of the unit cube, the repeated-FTC
finite-difference identities through the four consumed orders,
differentiation under the integral through the required parameter
derivatives, and the paired and remote boundary estimates. The remaining
analytic input is the xi-specific common-box estimate used to instantiate the
formal branch certificate.

## The analytic engine: a saddle in the complex plane

Everything above depends on knowing the xi coefficients and their
derivatives with enough uniformity. Those coefficients have an exact integral
representation involving a rapidly decaying theta-function kernel. For a
large index, the integral is dominated by a narrow region where competing
exponential effects balance. This is a **saddle point**.

The saddle variable \(L\) is defined implicitly by an equation of the form

\[
  N=L\left(\pi e^L+\frac34\right).
\]

On the positive real axis, one can picture the dominant contribution as a
sharp mountain pass: almost all of the integral comes from a small
neighborhood of its summit. But the proof needs derivatives of an analytic
continuation, so a real-axis estimate is not enough. The saddle must be
controlled throughout a narrow complex sector.

The argument constructs a unique holomorphic saddle branch using Rouché's
theorem. It then moves the contour through that saddle, proves a Gaussian
approximation in the central window, bounds the tails and endpoint
connectors, and shows that all higher theta modes are exponentially smaller
than the first.

This produces a sectorial asymptotic for the continued coefficient moment.
Cauchy's integral estimate then transports the small relative error through
six derivatives.

The leading derivative constants are strikingly simple:

\[
  2,\quad -2,\quad 4,\quad -12,\quad 48.
\]

The exact sixth derivative is not simple. After suitable scaling it becomes
a rational function whose denominator is a twelfth power and whose numerator
has 82 terms of total degree 13. That expression is precisely the sort of
place where a sign error can survive pages of human algebra.

For that reason the project did not rely on a single symbolic system. SymPy
derived and checked the expression first. Later, a clean-room Mathematica
notebook reconstructed the derivative tower from definitions without reading
the repository's frozen numerator. Mathematica reproduced the denominator,
the 82-term degree, the constants, and the exact coefficientwise bound. The
two systems therefore agree on the decisive algebra through genuinely
different computer-algebra paths.

One source-normalization issue also had to be handled explicitly. Different
printed conventions for the xi coefficients differ by a factor of eight.
The project rederived the Mellin identity from Riemann's kernel, checked the
factor against direct xi coefficients, and made the normalization visible in
the manuscript. This factor cancels in logarithmic derivatives, but leaving
it ambiguous would undermine source fidelity.

## Keeping the model's roots under control

Knowing that the comparison polynomial is real-rooted is not enough. The
proof also needs quantitative control of its roots and critical points.

The two Jacobi factors admit tridiagonal matrix models. Gershgorin-type
estimates place their roots in explicit intervals. Finite free convolution
then transfers these bounds to the comparison polynomial. A reciprocal-
polynomial argument supplies the lower endpoint as well as the upper one.

One previously assembled small-gap hypothesis is unusable on the new
four-parameter branch: the relevant ratio tends toward one rather than
remaining below one quarter. The candidate therefore replaces that route
with a ratio-free localization estimate. This is an important difference
from merely inserting one more term into an earlier proof.

The comparison polynomial is a terminating \({}_3F_2\) hypergeometric
polynomial. Its differential equation gives a recurrence among the scaled
derivatives

\[
  \frac{y^k p^{(k)}(y)}{p(y)}.
\]

At a critical point the first derivative vanishes, and the recurrence can be
turned into a maximum argument. The result is the radius
\(\rho\asymp\sqrt{nd}\) used in the sixth-order error calculation.

This recurrence was derived symbolically, checked coefficient-by-coefficient,
formalized in its closed algebraic form in Lean, and independently reproduced
in Mathematica on terminating polynomials of several degrees.

## From a small coefficient error to real roots

The final step is topological rather than asymptotic.

The comparison polynomial has positive, simple roots. Between consecutive
roots lie its critical points, where its values alternate in sign. If the
actual transformed Jensen polynomial has the same sign at every one of those
critical points—and at the two ends—then the intermediate value theorem
forces one actual root into every intervening interval.

Newton interpolation writes the ratio of the two polynomials as a sum of
finite differences multiplied by derivatives of the comparison polynomial.
Because the first matches are exact, the dangerous low-order terms vanish.
Cauchy's estimate controls the remaining tail. If the analytic multiplier is
close enough to one, none of the critical signs can flip.

This finite sign-transfer mechanism, including the final change from
positive comparison roots to negative Jensen roots, is part of the
kernel-checked Lean formalization.

## What Lean proves—and what it does not

Lean is a proof assistant: a small trusted kernel checks a formal proof term
against exact logical rules. It is exceptionally good at detecting missing
hypotheses, silent changes of convention, and algebraic steps that are “clear
to the author” but not actually justified.

The project now kernel-checks the complete T1--T5 analytic chain used for the
xi coefficients: the concrete theta/Mellin normalization, the moving saddle
branch, the legal contour and Gaussian localization, the infinite sum of
higher theta modes, the fixed-sector Gamma/Stirling assembly, the literal
sectorial coefficient theorem, and its Cauchy derivative consequences
through order six.

Lean also proves the full local six-fold complex FTC and Hermite–Genocchi
remainder with mass \(1/720\), the consumed cube-integral calculus, the
terminating hypergeometric producer and recurrence, the exact positive xi
parameter branch, the transformed xi polynomial and six coefficient matches,
and the normalized critical-radius theorem once narrow classical-root inputs
are supplied. The generic end-to-end conditional theorem then proves the
required distinct negative Jensen roots from the final multiplier
certificate. Phase 30 supplies that concrete certificate: it constructs the
xi multiplier, proves its six exact node values and a uniform distance below
one from the constant multiplier, builds the Rolle-point sign intervals, and
identifies the resulting polynomial with the transformed xi Jensen
polynomial.

A later clean-packet AI review found that the typed MSS interface still
allowed arbitrary negative lower endpoints. That made the imported product
interval record inconsistent at positive degree and therefore made the
formal headline implication vacuous, even though the paper's intended MSS
application used positive endpoints. The repaired interface now requires
positive-root and degree certificates for both factors and strict positivity
of both lower endpoints. Lean derives those inequalities from the displayed
\(B,D\ge 256d\) geometry before invoking the imported MSS result. The terminal
formal statement also proves that the Jensen polynomial has degree exactly
\(d\), excludes \(d+1\) distinct roots, and performs the analytic-range versus
finite-cutoff split in one global theorem.

This is not a hidden axiom. The boundary is explicit in the formal theorem
statements and in a machine-readable ledger. The Lean project contains no
project-specific axiom asserting the xi asymptotic, and its verifiers reject
`sorry`, `admit`, unsafe escape hatches, and custom axioms.

The remaining formal boundary is much narrower than it was in the original
version of this explainer. The final xi-specific sixth-multiplier interval
certificate and sign-transfer assembly are now kernel checked. The endpoint
still treats the classical Jacobi matrix/root correspondence, the MMP
log-mesh theorems, and the MSS product-root theorem as explicitly typed
literature inputs rather than formalizing those third-party papers from first
principles.

The literal T5 coefficient theorem has been isolated in a local Palomar
Comparator candidate. The local package and mutation gates pass, but official
Palomar Comparator and NanoDa replay is still pending. That candidate is
automated formal-verification evidence, not human or peer review.

## A layered approach to trust

No single verification method catches every error.

- **Paper proof** is best for mathematical architecture and conceptual
  explanation, but compressed arguments can hide missing uniformity.
- **Lean** checks exact formal implications, but only after the right theorem
  has been stated and formalized.
- **Symbolic algebra** catches expansions and identities, but a program can
  faithfully verify the wrong formula if the formula was transcribed
  incorrectly.
- **Independent computer-algebra systems** reduce common-mode software and
  simplification errors.
- **Rigorous interval arithmetic** can turn selected numerical statements
  into certified enclosures.
- **Mutation tests** check that verification gates actually fail when a sign,
  exponent, normalization, or constant is deliberately damaged.
- **Adversarial review** looks for conceptual gaps, but AI review remains
  correlated with AI-generated work and cannot be represented as human
  judgment.

The project uses all of these layers to varying degrees. It has since added
Arb/ACB ball arithmetic, semantic mutation tests, and a complete exact
dependency ledger for every finite constant. A fresh local reconstruction and
an independent Ubuntu build have passed. Role-specific AI reviews and targeted
correlated re-reviews have also run; they are retained as AI evidence and are
not described as human or peer review.

## What the adversarial reviews actually changed

The reviews were not ceremonial. They found mistakes serious enough to block
the manuscript as it then stood, even though the underlying proof notes often
contained the correct route.

One version called the path (L+iv) “horizontal.” It is vertical, and at a
saddle its quadratic term has the wrong sign: the supposed Gaussian descent
becomes ascent. Replacing (iv) with a real increment (r) fixed the local
direction, but a later hostile pass caught a second subtlety. The whole line
(L+r), (r\in\mathbb R), crosses the principal logarithm's branch cut. The
legal proof splits the original integral at (u=1), translates only the ray
from (1) to infinity, and uses the full real Gaussian merely as a comparison
after the missing left tail has been bounded. The final paper now states that
geometry explicitly.

Another review found that the manuscript defined its sixth-derivative object
as the logarithm of a gamma-normalized coefficient while the calculation
actually differentiated the auxiliary Mellin moment. That would double-count
a polygamma term. The paper now displays the exact gamma/moment bridge before
defining the logarithmic object.

The algebraic review rejected a “first failure” maximum argument that did not
control its higher neighbor. The corrected proof chooses a global normalized
maximum, so every recurrence neighbor is bounded and the terminal neighbor is
exactly zero. Later reviews also caught an extra (m) in two expanded
recurrence displays, an undefined threshold name, and stale descriptions of
the Lean axiom audit. Each correction is tied to a source-level mutation test
designed to fail if the old text returns.

This history is not evidence that AI review is equivalent to expert human
review. It is evidence that adversarial checking can be useful when its
findings, limitations, and correlations are preserved rather than summarized
away. The latest repairs pass the project's Lean, source, mutation, and
reproducibility gates; a fresh independent AI re-review of that repaired
candidate remains pending. Human mathematical scrutiny is still absent.

## How significant would the result be?

If the proof survives further scrutiny, its significance is specific and
real.

First, it would widen the known growing-degree region for xi Jensen
hyperbolicity from a three-fifths scale to a two-thirds scale, relative to the
frozen prior architecture used by the project.

Second, it would identify a reusable mechanism: an additional coefficient
match, supported by one more analytic derivative and a sufficiently robust
comparison family, can translate directly into a better growth exponent.
That principle may matter beyond this particular sequence.

Third, the work exposes and repairs several delicate interfaces that are
easy to overlook: coefficient normalization, sectorial rather than merely
real asymptotics, a failed small-gap condition, theorem-number and convention
seams in finite free convolution, and the need for a non-perturbative
derivative recurrence.

What it would not do is equally important. It would not show that every
Jensen polynomial is hyperbolic. It would not make the existential constant
numerically useful—the present unoptimized contraction produces an
astronomically large sufficient threshold. And it would not turn asymptotic
coefficient regularity into a proof that all xi zeros lie on the critical
line.

This is progress inside one sophisticated program surrounding the Riemann
hypothesis, not the resolution of the hypothesis itself.

## Why the paper must become longer

The original unified manuscript compresses the architecture into about 11 pages.
That is useful as a map, especially for someone entering a large evidence
repository. It is too short to serve as the only paper for a result whose
proof crosses Mellin transforms, saddle-point analysis, complex
interpolation, special functions, finite free convolution, root geometry,
and formal verification.

A mature manuscript should be several times longer. The expanded main paper
and technical supplement now print the contour estimates, quantifiers and
sector choices, cube-integral argument, contraction constants, finite-free
normalization adapters, recurrence inequalities, and Hermite–Genocchi
derivation. The largest symbolic expressions are referenced through exact,
hash-frozen artifacts, but every logical bridge is visible from the paper and
supplement without asking a reviewer to search historical phase notes.

The concise manuscript should not be discarded. It can become an extended
overview or “reader's map” accompanying the full proof.

## What the review package contains

A reviewer should receive more than a PDF and less than an unstructured dump
of a research directory.

The package design has a short `START_HERE` guide, the expanded paper and
technical supplement, the complete pinned Lean project, the Mathematica
notebook and exact result ledger, the SymPy and interval scripts, the full
supporting derivations, a theorem-to-code map, a trust-boundary statement,
known limitations, source versions and hashes, and a one-command serial
verifier.

Every file should be covered by a SHA-256 manifest. The archive should be
deterministic, so rebuilding it from the same source produces the same bytes.
Third-party papers should be identified by official links, versions, and
hashes rather than redistributed without regard to copyright.

There are three intended package classes:

- a navigable referee packet centered on the proof;
- a full audit archive containing all calculations and review history;
- separated adversarial packets for complex analysis, algebra, formal proof,
  reproducibility, and hostile falsification, each excluding prior reviews so
  that a new reviewer is not anchored by earlier verdicts.

The full audit archive also carries a cryptographic parent-chain proof from
the candidate commit to the required historical checkpoint and an offline Git
bundle. Its replay command reconstructs the candidate inside a temporary
directory. The referee packet can rebuild both manuscripts directly from its
own extracted source tree. In other words, “run this command” is itself a
tested claim rather than a pointer back to the author's workstation.

This packaging cannot supply the mathematical taste and skepticism of a
human expert. It can make every available piece of evidence transparent,
reproducible, and difficult to misrepresent.

## The broader lesson

The romance of mathematics often emphasizes a flash of insight: a single
line on a blackboard that changes everything. Real research also depends on a
less glamorous craft. Normalizations must agree. Branches of logarithms must
be legal. Uniform estimates must really be uniform. A theorem cited in one
convention must survive translation into another. A computation must be
reconstructible from definitions rather than trusted because it printed a
large expression.

This project is an experiment in making that craft unusually visible.

Its mathematical wager is simple to state: six exact matches should buy a
sixth-order error, and a sixth-order error should buy a two-thirds wedge. The
work surrounding that sentence—complex saddles, Jacobi factors, recurrences,
formal kernels, independent algebra systems, manifests, and adversarial
checks—is what turns the wager into a serious proof candidate.

Whether it ultimately becomes a theorem depends on the scrutiny still to
come. For now, its value lies both in the proposed exponent and in the clear
map it provides of what has been checked, what remains on paper, and what
would have to be formalized to make the argument substantially harder to
break.

## Further reading

- M. Griffin, K. Ono, L. Rolen, and D. Zagier, *Jensen polynomials for the
  Riemann zeta function and other sequences*, PNAS 116 (2019), 11103–11110.
- M. Griffin, K. Ono, L. Rolen, J. Thorner, Z. Tripp, and I. Wagner,
  [*Jensen polynomials for the Riemann xi-function*](https://arxiv.org/abs/1910.01227).
- J. Holland,
  [*A new hyperbolicity wedge and a joint semicircle limit for Jensen
  polynomials of Riemann's xi-function*](https://arxiv.org/abs/2608.08682),
  frozen v1 as used by this project.
- A. Martínez-Finkelshtein, R. Morales, and D. Perales,
  [*Real roots of hypergeometric polynomials via finite free
  convolution*](https://arxiv.org/abs/2309.10970).
- A. Marcus, D. Spielman, and N. Srivastava,
  [*Finite free convolutions of polynomials*](https://arxiv.org/abs/1504.00350).
