# C48 sectorial saddle: execution, review, and freeze plan

**Status:** active execution plan

**Primary open claim:** `C48-GORTTW-SECTOR`

**Purpose:** replace the terse complex-extension sentence following GORTTW (3.2)
by a self-contained proof from the exact xi/Mellin integral, then review and freeze
the entire Jensen two-thirds argument against one immutable commit.

This plan is deliberately fail-closed.  Numerical agreement, the real-axis
asymptotic, or a formal conditional theorem does not close the analytic claim.

## 1. Exact target

For `Re s > 0`, put

\[
 F(s)=\int_1^\infty (\log t)^s t^{-3/4}
       \sum_{k\ge 1}e^{-\pi k^2t}\,dt,
\]

with `(log t)^s = exp(s Log(log t))`.  Let `L_s` be the branch, continued
from the positive real axis, solving

\[
 s=L_s(\pi e^{L_s}+3/4),
\]

and set

\[
 K_s=s(1/L_s+1/L_s^2)-3/4,
 \qquad Q_s=L_s^2K_s=(1+L_s)s-3L_s^2/4.
\]

For the direct-xi normalization
`H(z)=xi(1/2+z)=sum gamma_H(M) z^(2M)/M!`, let `gamma_H(M)` be the
Jensen moment (the ordinary Taylor coefficient multiplied by `M!`) and put
`N=2M-2`.  Define

\[
 A_H(M)=
 \frac{e^{M-2}M^{M+1/2}L_N^N}
      {2^{2M-2}N^{N+1/2}}
 \sqrt{\frac{2\pi}{K_N}}
 \exp\!\left(\frac{L_N}{4}-\frac{N}{L_N}+\frac34\right),
\]

with all powers and square roots taken on branches continued from the
positive real axis.

### Minimal theorem needed downstream

There are fixed angles `0 < theta_0 < theta_1 < pi/2`, constants `R,C > 0`,
and a holomorphic function `E` on

\[
 S_1(R)=\{M:|M|>R,\ |arg M|<theta_1\}
\]

such that `A_H` is holomorphic and nonzero there,

\[
 gamma_H(M)=A_H(M)(1+E(M)),
\]

and, on the closed inner sector `|arg M| <= theta_0`,

\[
 |E(M)|\le C|M|^{-3/4}.
\]

The exponent `-3/4` is a convenient fixed instance of the published
`O(|M|^{-1+epsilon})` form.  It is enough for the Cauchy estimates of every
fixed derivative order used in the Jensen proof.  If the direct proof naturally
gives the stronger all-`epsilon` statement, record that as a corollary rather
than making it a prerequisite.

## 2. Proof execution sequence

### P21.0 — normalization and exact analytic object

**Deliverables**

1. Derive the Mellin integral from Riemann's integral for the completed zeta
   function.
2. Prove `F` is holomorphic on `Re s>0` by locally uniform domination, including
   differentiation under the integral sign.
3. Derive the exact coefficient identity and the factor-eight conversion between
   the GORZ normalization and `H(z)=xi(1/2+z)`.
4. Decompose `F=sum F_k` and identify the exact first-mode phase, saddle equation,
   curvature, and leading factor.
5. State the target sector theorem with every branch and domain explicit.

**Gate P21.0:** all identities pass an independent symbolic regression; no use
of an asymptotic source is hidden in this stage.

### P21.1 — saddle branch and uniform geometry

**Execution status (2026-08-16): completed at internal paper-proof level,
fresh review pending.**  Lemma S and
`C48_LEADING_CONTOUR_LOCALIZATION.md` supply the narrow-sector geometry,
`Re K_s >= c|K_s|`, nonvanishing, and the square-root branch.

Use Lemma S to construct `L_s` on nested sectors.  Add explicit constants for:

- separation of the saddle from `log t=0` and branch cuts;
- `L_s`, `e^{L_s}`, `K_s`, and `Q_s` nonvanishing;
- comparability `|L_s| asymp log|s|`, `|K_s| asymp |s|/log|s|`;
- a square-root branch for `K_s`;
- containment of all later Cauchy discs in the outer sector.

**Gate P21.1:** a single named lemma supplies the domains consumed by the
contour, logarithm, and derivative arguments.  A numerical branch plot is only
a regression, never evidence for the lemma.

### P21.2 — a legal complex contour

**Execution status (2026-08-16): completed at internal paper-proof level,
fresh review pending.**  The implemented contour is the horizontal shift in
`u=Log t`, equivalently a rotation of the `t`-tail through the saddle.  It
requires only `Re K_s >= c|K_s|`, not that `K_s v^2` be exactly positive real.

Construct a contour `C_s` in the complex `t`-plane through
`a_s=e^{L_s}`.  Prove:

1. deformation from `[1,infinity)` to `C_s` stays inside one domain for
   `Log t`, `Log Log t`, and the theta kernel;
2. all connecting arcs vanish or satisfy a uniform bound;
3. in the central coordinate `t=a_s e^v`, the contour is a uniformly steep
   descent path for the first mode;
4. the Jacobian `a_s e^v` is treated as amplitude.  It must not be absorbed
   into the phase while retaining the unshifted saddle equation.

**Kill gate:** if a single contour cannot be chosen uniformly on the desired
sector, shrink the sector and restate the downstream Cauchy geometry.  Do not
patch the argument with pointwise contours lacking uniform constants.

### P21.3 — central Gaussian estimate

**Execution status (2026-08-16): completed for the leading theta mode at
internal paper-proof level, fresh review pending.**  The signed cubic Gaussian
moment and fourth/sixth absolute moments give relative error `O(1/|K_s|)`.

On `|v| <= rho_s`, Taylor-expand the first-mode phase through a sufficient
order.  Prove uniform bounds on third and higher derivatives and on the
amplitude, choose `rho_s`, and establish

\[
 F_1(s)=\sqrt{2\pi/K_s}\,L_s^s
 e^{L_s/4-s/L_s+3/4}\,(1+E_1(s))
\]

with `E_1(s)=O(|s|^{-3/4})` on the inner sector.

**Gate P21.3:** all remainder estimates use absolute values on the actual
complex contour and have constants uniform in `s`.

### P21.4 — tails and higher theta modes

**Execution status (2026-08-16): completed at internal paper-proof level,
fresh review pending.**  `C48_HIGHER_THETA_MODES.md` deforms the locally
uniform theta series on the same contour and proves exponential suppression
of all `k>=2` modes.

Prove separately:

- the two tails of `C_s` outside the central neighborhood are smaller than the
  leading Gaussian term by the required power;
- `sum_{k>=2} F_k(s)` has the same or better relative bound;
- sum/integral interchange and contour deformation remain locally uniform.

The higher-mode estimate must explicitly exploit `e^{-pi k^2t}` on the chosen
contour; a real-axis positivity estimate is not automatically valid after
deformation.

**Gate P21.4:** central, tail, and higher-mode bounds close on the same pair of
nested sectors and with one common large-radius threshold.

### P21.5 — xi coefficient assembly

**Execution status (2026-08-16): completed at internal paper-proof level,
fresh review pending.**  `C48_XI_COEFFICIENT_ASSEMBLY.md` proves the two-step
moment ratio, factor-eight-corrected assembly, and sectorial Stirling formula,
with final relative error `O(log|M|/|M|)`.

1. Use the exact coefficient formula to show the `F(2M)` term is uniformly
   subordinate to the `F(2M-2)` term.
2. Apply sector-uniform Stirling estimates to the gamma ratio.
3. reconcile every power of two, `e`, `M`, `N`, `L_N`, `K_N`, and `Q_N`;
4. prove `A_H` is holomorphic and nonzero and obtain the target relative error.

**Gate P21.5:** compare the final formula both with the exact direct-xi
coefficient identity and with high-precision real-axis moments.  The numerical
comparison is a regression only.

### P21.6 — downstream closure

**Execution status (2026-08-16): paper dependency discharged and serial
verification replay passed; fresh review pending.**  `C48_DOWNSTREAM_DISCHARGE.md` transports
the holomorphic `O(log|z|/|z|)` error through proportional-disk Cauchy,
nonvanishing, and the fifth/sixth saddle interfaces.

Re-run the Phase-20 Holland-interface reconstruction using the new theorem,
remove `C48-GORTTW-SECTOR` from the assumption registry, and verify:

- sector containment for `n+Omega`;
- a common nonvanishing domain for the continued moments;
- fifth- and sixth-order logarithmic derivative estimates;
- the Hermite--Genocchi residual estimate;
- the conditional Lean assembly now has all analytic inputs discharged on paper.

**Completion criterion:** the claim ledger records an internal paper proof,
not an external premise, and every downstream reference points to exact theorem
and equation labels.

## 3. Final review protocol

### P22.0 — freeze the review candidate

**Execution status (2026-08-16): in progress.**  The serial Phase-21 and
Phase-20 replays pass.  The proof-source candidate is the commit containing
the Phase-22 freeze record; its exact hash is recorded in the packaging
revision and reviewer manifest.  No proof edit after that source commit is
permitted without a new candidate and a restarted review.

Create one candidate commit containing the manuscript, proof notes, scripts,
Lean sources, manifests, and generated reviewer packets.  Record:

- commit hash and clean-worktree status;
- Lean, Mathlib, Python, and package versions;
- SHA-256 hashes for primary-source PDFs/source archives and every packet;
- exact verification commands and their logs;
- a machine-generated file manifest.

No proof edits are permitted after this freeze without creating a new candidate
commit and restarting the final review.

### P22.1 — fresh end-to-end reviews

Run at least two independent review passes against that same commit:

1. **analytic pass:** integral representation, branch domains, contour
   deformation, uniform saddle errors, logarithmic derivatives, and asymptotic
   implication;
2. **algebraic/formal pass:** coefficient normalization, finite-difference
   matching, positivity lemma, constants, Lean theorem surface, axiom audit,
   and reproducibility.

Review prompts must include the full frozen bundle and ask for one of
`R0`, `R1`, or `REJECT`, with findings labelled `P0` through `P3`.  The second
reviewer must not be shown the first reviewer's conclusions before producing an
initial report.

If only AI reviewers are available, every manuscript, packet, and status page
must say so plainly.  Use the term **AI pre-review**, not human review, peer
review, or independent expert certification.  Record model/provider/version,
date, prompt, supplied files, and raw response.  Agreement between AI agents
does not upgrade the proof to peer-reviewed status.

### P23 — defect-resolution loop

- `P0`: stop release immediately; fix or retract the theorem.
- `P1`: release-blocking; fix with a proof and regression, then rerun both final
  reviews against a new frozen commit.
- `P2/P3`: resolve, defer with a documented reason, or narrow wording; no silent
  dismissal.

Maintain one disposition table mapping each finding to source lines, repair
commit, verification evidence, and reviewer confirmation.  Search all generated
documents for stale constants and superseded claims after every repair.

### P24 — manuscript/evidence freeze

After no P0/P1 findings remain:

1. render PDF and DOCX and visually inspect every page;
2. rebuild all reviewer packets from the final commit;
3. run clean Lean builds, axiom audits, `leanchecker`, symbolic regressions, and
   packet-manifest verification;
4. ensure the manuscript distinguishes paper-proved analysis, Lean-checked
   finite algebra, numerical regression, and AI pre-review;
5. sign a final support-status table and generate checksums;
6. tag the exact release commit and retain the complete frozen evidence bundle.

The theorem may be described as a manuscript result at this point, but not as
peer reviewed until actual scholarly peer review occurs.

## 4. Optional Lean formalization track

Lean work should follow, not precede, stabilization of the paper proof.

1. Formalize remaining scalar inequalities, domain containments, and exact
   normalization identities.
2. Define an `AnalyticSaddleCertificate` interface and keep the end-to-end Jensen
   theorem conditional on that explicit structure.
3. Formalize Lemma S: moving discs, explicit Rouché estimates, unique local root,
   overlap/identity-theorem patching, holomorphy, and asymptotic bounds.
4. Formalize elementary adapters: Cauchy derivative bounds on nested sectors,
   logarithm/nonvanishing lemmas, Hermite--Genocchi, and sector containment.
5. Only after the contour proof is stable, assess full formalization of the
   Mellin saddle theorem.  This is a substantial complex-analysis project, not
   a release prerequisite.

Every formal theorem must pass a clean pinned build, `#print axioms`, and
`leanchecker`; no `sorry`, `admit`, custom axiom, or opaque imported analytic
premise may be described as machine verification.

## 5. Stop conditions

Stop and narrow or withdraw the two-thirds claim if any of the following occurs:

- no uniform legal contour exists on any sector large enough for downstream
  Cauchy discs;
- higher theta modes are not uniformly subordinate;
- the required relative error fails on the complex sector;
- the exact xi coefficient assembly changes the saddle main term materially;
- an unresolved P0/P1 remains after the final review cycle.

## 6. Immediate execution

The first executed milestone is P21.0.  Its derivation and regression are in
`C48_GORTTW_SECTOR_MILESTONE1.md` and
`../c48_jensen/symbolic/gorttw_mellin_milestone1.py`.  The independent
primary-source reconstruction is `GORTTW_MELLIN_SOURCE_RECONSTRUCTION.md`.
Completion of P21.0 does **not** close `C48-GORTTW-SECTOR`; the first genuinely
new analytic gate is P21.2, the uniform complex contour.
