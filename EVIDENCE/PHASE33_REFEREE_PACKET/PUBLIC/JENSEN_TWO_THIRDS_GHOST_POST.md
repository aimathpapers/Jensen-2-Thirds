*A sixth-order comparison widens a known real-rootedness region for the
Jensen polynomials of Riemann's xi-function. The argument also illustrates
both the reach and the limits of formal proof in contemporary mathematics.*

In 1914 the Danish mathematician Johan Jensen described a way to study an
infinite analytic object through a sequence of finite polynomials. More than
a century later, that idea has become one of the useful approaches to
Riemann's xi-function, the symmetric form of the zeta function at the center
of the Riemann hypothesis.

The finite objects are called Jensen polynomials. Each one is assembled from
a short run of Taylor coefficients of xi. Their roots can be calculated,
plotted and compared with the roots of classical polynomials. More
importantly, their root geometry can sometimes be proved uniformly: not just
for one degree or one starting coefficient, but throughout an expanding
region of the two parameters.

The result described here is a proof candidate for a wider such region. In
simplified asymptotic terms, an earlier growing-degree method allowed the
degree to increase approximately as the three-fifths power of the coefficient
index. The new argument permits growth at the two-thirds power, up to a
logarithmic factor. The change comes from forcing a tractable comparison
polynomial to agree with the xi polynomial through six consecutive
coefficient conditions rather than five.

This is not a proof of the Riemann hypothesis. It is a theorem about a
particular family of finite polynomials associated with xi. Its interest is
threefold: it sharpens a growing-degree real-rootedness result, it exposes a
specific sixth-order mechanism behind the new exponent, and it has been
carried unusually far into machine-checkable form.

The last point requires care. A substantial new chain is checked by Lean, a
formal proof assistant, and decisive algebra has been reconstructed in two
independent computer-algebra systems. But the work has not received human
mathematical review or peer review. It should therefore be read as an
extensively checked, substantially formalized proof candidate whose detailed
argument and verification record are open to inspection.

## From zeta to an even entire function

For real numbers greater than one, the zeta function begins with the familiar
series

> ζ(s) = 1 + 1/2ˢ + 1/3ˢ + 1/4ˢ + ··· .

Analytic continuation extends zeta to almost the entire complex plane. Its
nontrivial zeros carry information about the fine distribution of prime
numbers, and the Riemann hypothesis asserts that every one of those zeros has
real part one-half.

The raw zeta function is not the most convenient form for the present
problem. After adjoining gamma and elementary factors, one obtains Riemann's
completed xi-function. It is entire—there are no poles—and satisfies the
functional equation ξ(s) = ξ(1-s). Centering at one-half therefore produces
an even function. With the normalization used in the paper, it has an
expansion of the form

> ξ(1/2 + z) = Σ γ(n) z²ⁿ/n!.

The positive numbers γ(n) are moments of an explicit, rapidly decaying theta
kernel. They are the data from which the Jensen polynomials are built. For a
starting index n and degree d, define

> Jᵈ,ⁿ(X) = Σₖ₌₀ᵈ (d choose k) γ(n+k) Xᵏ.

This construction keeps only d+1 consecutive coefficients, yet it preserves
enough structure to pose a sharp geometric question: are all d roots real?
In the normalization used here the desired conclusion is stronger. After the
final change of variables, the roots should be real, distinct and negative.

A polynomial with only real roots is called hyperbolic. Jensen and George
Pólya showed that sequences of hyperbolic Jensen polynomials are closely
related to entire functions in the Laguerre–Pólya class. This does not turn
any one finite computation into a statement about all zeros of xi. It does
explain why these polynomials are a natural finite probe of an infinite
function.

> **What the theorem says.** There is an effective constant K such that the
> degree-d Jensen polynomial built from the nth xi coefficient has d distinct
> negative roots whenever n and d lie in a specified two-thirds wedge. In the
> headline asymptotic form, n² log(n+2) is at least Kd³.

> **What it does not say.** It does not prove that every xi Jensen polynomial
> is hyperbolic, and it does not prove that every nontrivial zero of zeta lies
> on the critical line. The effective constant is not optimized and the
> resulting cutoff is far beyond the range of ordinary numerical testing.

## Fixed degree, growing degree

The modern study of xi's Jensen polynomials changed markedly with work by
Michael Griffin, Ken Ono, Larry Rolen and Don Zagier. They proved that for
each fixed degree d, the suitably shifted and rescaled Jensen polynomials
approach the Hermite polynomial of that degree as n tends to infinity.
Hermite polynomials have simple real roots, so the xi Jensen polynomials are
eventually hyperbolic for every fixed d.

The phrase “for every fixed d” leaves open a uniform question. Suppose d is
allowed to grow with n. How fast can it grow while one proof still controls
all the polynomials in the region? A fixed-degree limit does not answer this:
the error terms may deteriorate with d, and neighboring roots of a degree-d
comparison polynomial become closer together as d increases.

One way to picture a growing-degree theorem is to place log n on the
horizontal axis and log d on the vertical axis. The allowed pairs occupy a
wedge beneath a sloping boundary. An architecture developed by Jonathan Holland
leads, after suppressing constants, to a condition of the form

> n³ log²(n+2) ≥ Kd⁵,

which permits d to grow roughly as n³⁄⁵. The present candidate instead proves

> n² log(n+2) ≥ Kd³,

so d can grow roughly as n²⁄³ times a mild logarithmic factor.

![Schematic comparison of the three-fifths and two-thirds admissible wedges.](assets/JENSEN_WEDGE_COMPARISON.png)

The diagram is deliberately schematic. It suppresses the different
constants and logarithmic corrections and is not a plot of verified finite
cases. Its point is the slope: two-thirds eventually dominates
three-fifths. The extra region is not obtained by tightening a numerical
constant. It requires one more order of cancellation in the comparison
between xi and the model polynomial.

## A model made from two Jacobi factors

The argument does not try to locate the roots of the xi Jensen polynomial
directly. It constructs a comparison polynomial whose roots are easier to
control and then proves that the xi polynomial is close enough to preserve
their sign pattern.

The model is a terminating hypergeometric polynomial of the form

> ₃F₂(-d, A, C; B, D; (D/AC)y).

It can be produced from two Jacobi-polynomial factors by a multiplicative
finite-free convolution. Jacobi polynomials are classical orthogonal
polynomials. In their natural parameter range their roots are real, simple
and confined to a known interval. Finite-free convolution provides a way to
combine those factors while retaining useful control over the product's root
geometry.

Four positive parameters in the model are allowed to vary with n and d. Two
normalizations already force the first two coefficient conditions; four
equations then use the four parameters to enforce four more. In total, the
normalized xi and model coefficients agree at six consecutive positions.

At the limiting point the parameter system has the exact positive solution

> (α, t, w, δ) = (3, 2, 16/3, 1/3).

Its Jacobian determinant is exactly -1/144, and the infinity norm of the
inverse Jacobian is 304/3. Those exact values matter because the proof needs
more than a numerical solution at one point. A quantitative implicit-function
argument must show that a unique positive solution persists throughout the
prescribed parameter box for all sufficiently large n.

Why does the sixth match change the exponent? Write the normalized
coefficient quotient as the exponential of a logarithmic error. If six node
values agree, the lower-order portion of that error disappears. A
Hermite–Genocchi or Newton remainder then expresses the first surviving term
using a sixth derivative. Schematically, the comparison error changes from a
fifth-order scale to a sixth-order scale. The root-separation cost grows with
d, and balancing those two quantities produces the new cubic inequality
Kd³ ≤ n² log n.

This is the central structural claim of the work: the power two-thirds is the
analytic and algebraic consequence of six matches, not an empirically fitted
number.

## The analytic engine inside γ(n)

Six coefficient matches are useful only if one has a uniform sixth-order
description of the true xi coefficients. That is the more delicate analytic
part of the argument.

Riemann's theta representation gives γ(n) as a Mellin-type integral of a
rapidly decaying kernel. After the relevant substitution, the dominant
exponential contains a term πeᵘ. For a large complex parameter N, its saddle
L_N is determined by the equation

> N = L_N(πeᴸᴺ + 3/4).

On the positive real axis this equation has a unique solution. The proof must
do considerably more: it constructs a holomorphic saddle branch in a fixed
complex sector, chooses the logarithm and square root consistently, and
tracks quantitative bounds on the branch and its derivatives.

The contour of integration is then deformed through the saddle in the
horizontal steepest-descent direction. Near L_N, the phase has a negative
quadratic term, so the central contribution becomes Gaussian. Outside a
small window, connector segments, remote tails and higher theta modes must
all be shown uniformly smaller than the main contribution. The contour must
stay inside the legal domain of the principal logarithm; otherwise a familiar
formal Gaussian calculation would rest on an invalid deformation.

The paper organizes this analytic chain into five modules:

1. the exact Mellin normalization connecting the theta integral to γ(n);
2. the existence and control of the sectorial saddle branch;
3. the leading contour calculation, including its central Gaussian and
   tails;
4. the uniform suppression of every higher theta mode; and
5. the assembled sectorial coefficient theorem, on a domain slightly larger
   than the one ultimately used.

The larger domain in the fifth step permits Cauchy's integral formula to
differentiate the asymptotic expansion without differentiating an informal
big-O term. After the chain rule and the gamma normalization are handled
consistently, the leading derivative constants from orders two through six
are

> 2, -2, 4, -12, 48.

At sixth order the exact rational function has denominator
(4+4r-3σ)¹². Its reduced numerator has 82 terms and total degree 13. On the
certified parameter box, a coefficientwise rational majorant is less than
10,000.

These fingerprints are useful because they can be independently
recalculated. Recovering the same denominator power, term count, total degree,
chain-rule factor 48 and exact majorant does not prove that the surrounding
analysis is correct. It does, however, make several classes of algebraic and
normalization error comparatively easy to detect.

## Why six equal values control an interval

The sixth-order remainder is the bridge between local coefficient matching
and uniform control.

Suppose a function F vanishes at six designated nodes. The divided-difference
form of the Hermite–Genocchi formula represents F at another point as a
sixfold product times an average of F's sixth derivative over a simplex. The
simplex has mass 1/6! = 1/720. This exact factorial is not cosmetic: losing it
would destroy the numerical scale needed by the later comparison.

For the xi/model quotient, the six matches provide those six zeros. The
analytic derivative theorem bounds the sixth derivative throughout a complex
tube around the real interval. The result is a uniform sixth-order residual
estimate, rather than six isolated equalities.

There are two ways this step can go wrong in a manuscript. One can quote a
real-variable interpolation formula even though the nodes and intermediate
points are complex; or one can state that six coefficient equalities are
“equivalent” to the quotient-node conditions without displaying the
normalizations. The supporting development now includes both adapters
explicitly: a complex Hermite–Genocchi theorem and the algebraic identity
that converts the four solved equations plus two normalizations into the six
node values.

## From a small multiplier to d real roots

Controlling coefficients is not yet controlling roots. A polynomial whose
roots nearly collide can be sensitive to a small perturbation. The algebraic
side of the proof therefore develops quantitative root separation for the
model before transferring any conclusion to xi.

The Jacobi factors admit symmetric tridiagonal matrix representations. Matrix
localization bounds place their roots in explicit intervals. A strict
logarithmic-mesh theorem controls their multiplicative spacing, and a
finite-free product-root inequality transports localization through the
convolution. The hypergeometric differential equation supplies a recurrence
for the model and its derivatives. A global maximum argument then rules out a
first normalized derivative that exceeds the prescribed radius.

Now package the difference between the transformed xi polynomial and the
model as a multiplier c_F. The six matches give c_F = 1 at the six nodes. The
sixth-order residual theorem proves, uniformly on the interval containing the
model's critical points,

> |c_F - 1| < 1.

At successive critical points the model polynomial alternates sign. A
multiplicative correction lying strictly inside the unit disk cannot erase
those signs. The intermediate value theorem therefore supplies a root in
each intervening interval. The intervals are disjoint, so the roots are
distinct. Degree counting gives all d roots, and the final reciprocal and
scale transformation places them on the negative real axis in the original
xi Jensen coordinate.

The word “concrete” is important here. It is easy to formalize a general
lemma saying that *if* some multiplier obeys the right node and interval
conditions, roots are preserved. The latest stage goes further: it constructs
the xi-specific multiplier, proves its six node values, derives its strict
unit bound from the residual theorem, instantiates the interval certificate,
and identifies the output with the actual transformed xi Jensen polynomial.

![Diagram of the analytic and algebraic proof streams, their sixth-order meeting point, and the typed literature inputs.](assets/PROOF_ARCHITECTURE.png)

## What the latest Lean theorem adds

Lean is a language in which mathematical objects, hypotheses and conclusions
are written precisely enough for a small kernel to verify every logical
inference. A Lean proof is valuable only to the extent that its formal
statement matches the intended mathematics and its assumptions are visible.

Earlier formal stages established much of the analytic and algebraic
infrastructure but stopped before the final xi-specific sixth-multiplier
certificate. That endpoint left a reasonable question: had the generic
stability mechanism actually been connected to the polynomial named in the
paper?

The newest development closes that seam. Its terminal declaration,
`riemannXiJensen_twoThirds_global_headline_exactly`, builds the concrete
multiplier certificate, performs the analytic-range versus finite-cutoff
split, and concludes that the xi Jensen polynomial has exactly the expected
number of distinct negative roots. Lean separately proves that the polynomial
has degree exactly `d`, so “exactly” is not being inferred from informal
degree counting outside the theorem.

The theorem does not import the entire mathematical literature into Lean.
It takes one structured value containing three families of classical root
facts:

- the required Jacobi root and matrix properties;
- the strict log-mesh preservation theorem associated with
  Martínez-Finkelshtein, Morales and Perales; and
- the finite-free product-root inequality associated with Marcus, Spielman
  and Srivastava.

Those are ordinary, explicitly typed hypotheses. They are not hidden project
axioms. The terminal axiom audit reports only Lean's standard logical
principles, and automated scans reject `sorry`, `admit`, custom axioms, unsafe
escape hatches and equivalent shortcuts.

> **The formal boundary.** Lean checks the new xi-specific analytic,
> sixth-order, multiplier and sign-transfer assembly. The three cited
> literature inputs above remain literature inputs; their original proofs
> have not been reimplemented from first principles. The typed MSS interface
> requires positive-root and degree certificates for both factors and strict
> positivity of both interval lower endpoints; Lean proves the concrete
> lower-endpoint inequalities before invoking that external result.

This boundary is a feature, not a disclaimer to be minimized. A reader can
see exactly which statements are checked by the kernel and exactly which are
being accepted from cited work. That is more informative than the undivided
label “formally verified.”

## Independent algebra and interval tripwires

Formal proof and computer algebra address different risks. Lean is well
suited to logical composition and explicit dependencies, but it is not the
best environment in which to discover or independently reconstruct an
82-term rational function. Computer-algebra systems can do that efficiently,
but a successful symbolic simplification does not certify the analytic
domain on which an identity is used.

The project therefore uses a layered verification record.

SymPy scripts build the parameter equations, derivative tower,
hypergeometric recurrence and interval polynomials from their definitions.
A separate clean-room Mathematica notebook was executed without importing
the repository's frozen expressions, JSON records, Lean terms or SymPy
outputs. It recovered the positive parameter solution, determinant, inverse
norm, shifted recurrence, sixth-derivative denominator, 82-term numerator and
exact majorant. This is a second-computer-algebra-system recalculation, not an
independent human derivation: the notebook cells themselves were prepared
with AI assistance and executed by the author.

Directed Arb/ACB computations add rigorous enclosures for selected complex
boxes, contour quantities and polynomial roots. Exact rational interval
checks verify the margins in the branch boxes and parameter inequalities.
Numerical evaluations of the Mellin representation and its saddle
approximation test the normalization across widely separated scales.

Finally, semantic mutation tests deliberately alter load-bearing statements:
a factor of eight, a strict inequality, the saddle phase, a recurrence
coefficient, the multiplier alias or its connection to xi. The verification
gate must fail on each mutation. Mutation testing is not a proof of the
theorem. It is evidence that the tests are attached to the claimed seam
rather than merely recognizing filenames or reassuring phrases.

## What automated scrutiny has already changed

The review archive is intentionally not a sequence of unbroken passes.
AI-only adversarial reviews found substantive defects in earlier drafts.
One version printed an incorrect coefficient integral. Another misstated the
critical-radius hypothesis used in sign transfer. A later review noticed that
a contour described as horizontal had been parameterized in the imaginary
direction, changing Gaussian descent into ascent. Another caught a mismatch
between the logarithm of the Mellin moment and the logarithm of the normalized
coefficient.

Those were not stylistic objections. Each could have invalidated the printed
argument at that point. The formulas were repaired, the affected reasoning
was rechecked, and targeted regressions were added. Subsequent review also
forced the contour's logarithmic branch cut, the definition of the phase and
amplitude, and the identity of the multiplier polynomial to be stated rather
than inferred.

A fresh clean-packet AI review then found a formal defect of a different
kind. The MSS input record quantified over arbitrary lower endpoints. At
positive degree, choosing negative symmetric endpoints made that record
inconsistent, so the headline implication could be satisfied only vacuously
even though the paper's intended application used positive intervals. The
interface now carries the missing positive-root, degree and strict-endpoint
conditions, and Lean derives the two endpoint inequalities from
`B,D ≥ 256d`. A regression test preserves the old call and requires Lean to
reject it at the missing positivity argument.

This history does not make the present candidate infallible. AI reviewers can
share blind spots, especially when trained on similar mathematical language
or supplied with the same evidence. Its value is narrower: it records real
attempts to falsify the argument and shows how the proof surface changed in
response. The repaired candidate has passed the project's Lean, source,
mutation and reproducibility gates; a fresh independent AI re-review of that
candidate remains pending.

## What a wider wedge would mean

If the proof survives expert scrutiny, it establishes a larger uniform
real-rootedness region for the xi Jensen polynomials. It also demonstrates
that the Jacobi finite-free comparison architecture can be pushed one order
beyond its five-match form. The analytic work shows that the required sixth
derivative remains uniformly controlled in a complex sector; the algebraic
work shows how that derivative control reaches actual roots.

The exponent should not be interpreted as a universal barrier. It describes
what six matches buy within this architecture. A seventh match would require
additional parameters or a new relation among the existing ones. Optimizing
the effective constant would be a different project: many present estimates
were chosen for transparency and uniformity rather than numerical sharpness.

Nor is the theorem a practical algorithm for checking small Jensen
polynomials. Direct numerical root finding works far below the asymptotic
cutoff. The theorem's purpose is to explain a uniform regime as n and d grow
together.

The broader methodological point may be equally interesting. Formal proof is
often most persuasive not when it presents a monolithic seal of correctness,
but when it makes the architecture inspectable. Here one can move from the
coefficient integral to the saddle theorem, from the saddle theorem to six
derivatives, from six matches to a residual, and from the residual to the
actual xi polynomial. One can also see where the chain leaves the formal
development and invokes established literature.

That kind of transparency is especially important for research conducted
outside an academic institution and developed with substantial AI
assistance. Software can make a long argument easier to explore, formalize
and test. It can also make an incorrect argument look finished. The proper
response is not to treat computation as a substitute for mathematical
judgment, but to expose enough structure that knowledgeable readers can test
the claims at their most vulnerable seams.

## Questions for a critical reader

The most useful response to this work is not a general vote of confidence.
It is a precise challenge. Among the questions the release is designed to
make answerable are:

- Does the Mellin normalization reproduce the stated xi coefficients?
- Is the complex saddle branch controlled on the full sector used by
  Cauchy's formula?
- Does the contour deformation remain clear of the principal-logarithm cut?
- Are all higher theta modes bounded uniformly rather than sampled?
- Do the four parameter equations plus two normalizations give exactly the
  six quotient-node values?
- Does the complex sixth-order remainder carry the correct 1/720 mass?
- Are the hypotheses of the cited Jacobi, log-mesh and product-root theorems
  satisfied in the chosen parameter range?
- Is the strict multiplier bound connected definitionally to the actual
  transformed xi Jensen polynomial?
- Does the prose theorem have the same quantifiers and cutoff as the formal
  headline theorem?

The paper, supplement, formal source, clean-room notebook and mutation record
are supplied so that these questions can be investigated at the level of
definitions rather than slogans.

## Read and inspect the work

- **Full paper:** [PAPER PDF URL]
- **Permanent Version 1.0 record and DOI:** [VERSION DOI URL]
- **Public source and immutable release:** [PUBLIC GITHUB RELEASE URL]
- **Technical supplement and complete reviewer package:** included with the
  permanent record

**Disclosure:** AI systems assisted substantially with the research, formalization, software, writing, and AI-only adversarial review. No human mathematical review or peer review is claimed. The work does not prove the Riemann hypothesis.
