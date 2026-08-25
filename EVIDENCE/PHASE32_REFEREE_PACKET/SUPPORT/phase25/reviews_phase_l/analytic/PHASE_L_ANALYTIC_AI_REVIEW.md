# Phase L complex-analysis and asymptotics adversarial AI review

Candidate commit: `5641348d8ce0aadea5225f31dbb9bb1327778d20`  
Required historical checkpoint: `5f79158f9c6276dd09142edeea279e35b0d58406`  
Review date: 2026-08-17  
Track: analytic  
Evidence boundary: only `Jensen_Two_Thirds_Phase25_Analytic_AI_Review_Packet.zip`, extracted in a private temporary directory

## 1. Overall verdict

**R2 — major revision and a new frozen review pass required.** I use `R2` to
mean that I found release-blocking, theorem-affecting defects in the frozen
manuscript, but also found a plausible repair path already represented in the
packet's underlying analytic notes. I found no P0 evidence that the intended
two-thirds theorem is irreparable.

There are two P1 blockers. First, the manuscript parameterizes a purported
horizontal steepest-descent contour as `L_s+i v`; with the manuscript's own
identity `h''(L_s)=-K_s`, this produces `+K_s v^2/2`, not the displayed
decaying `-K_s v^2/2`. Second, it defines `h=log gamma` but then uses the
derivative tower and residual formula for `h=Log M`, the auxiliary moment.
The distinction contributes a load-bearing polygamma term of order `n^-5`,
larger by a factor of `log n` than the claimed residual scale.

The internal Phase-21 contour note uses the correct horizontal coordinate
`L_s+r`, and the Phase-9/18/21 notes consistently use `h=Log M_z`. Thus these
findings refute the frozen manuscript proof as written; they do not, by
themselves, refute the intended repaired argument.

## 2. Gate-by-gate review

| Gate | Status | Evidence tested and falsification method |
|---|---|---|
| A0 completed-xi, Mellin, and factor-eight normalization | **PASS** | Re-derived `8 xi(1/2+w)=(4w^2-1)Lambda(1/2+w)` and the coefficient extraction. A clean-room standard-library calculation compared direct completed-zeta values with `8 integral omega(e^(2u))e^(u/2)cosh(wu)du` at three complex/real `w`; relative differences were `1.6e-15` to `7.8e-15`. The Mellin identity and the factor eight are consistent. |
| A1 sectorial saddle existence, uniqueness, branches, and Q nonvanishing | **PASS** | Checked the whole-boundary Rouché envelope from definitions: `0.78525` at `ell=12` for angle `0.01`, decreasing in the tested range. The disc gives `Re L>0`, `|r|,|sigma|<=7/50`, and hence `|1+r-3sigma/4|>=151/200`. The patching argument establishes the distinguished holomorphic branch, not global pointwise uniqueness of every saddle solution. |
| A2 contour deformation, connector control, theta-mode tails, and uniformity | **FAIL** | `JENSEN_TWO_THIRDS_MAIN.tex:322-371`, `JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex:173-220`, and `c48_detailed_appendices.tex:195-246` call the contour horizontal but use `L_s+i v`. That direction has the wrong quadratic sign. The evidence note `C48_LEADING_CONTOUR_LOCALIZATION.md` instead uses `u=x+i Im L_s=L_s+r`, retains the Jacobian-induced linear term, and gives a viable proof. Independent integrals from the definitions gave `I_1/A=1.004028...` at `s=80` and `1.0028898-4.76e-6 i` at a complex `s`, with the second theta mode around `1e-26` and `1e-34`, respectively; these are regressions, not uniform proofs. |
| A3 implicit derivative tower through order six and chain constants | **FAIL as printed** | A clean-room sparse exact differentiator reconstructed the intended moment tower `(2,-2,4,-12,48)`. But `JENSEN_TWO_THIRDS_MAIN.tex:422` defines `h=log gamma`, for which that tower is false: `gamma(z)=sqrt(pi) 2^(-2z) M_z/Gamma(z+1/2)`, so `(log gamma)^(6)=(Log M)^(6)-psi^(5)(z+1/2)`. The latter term is asymptotic to `24/n^5`, not lower order than `1/(n^5 log n)`. |
| A4 H6 denominator, 82-term numerator, box majorant, and sixth derivative bound | **PASS for the intended moment saddle** | Independent standard-library exact differentiation, without reading frozen results, produced denominator `(4+4r-3sigma)^12`, 82 numerator terms, total degree 13, `H6(0,0)=24`, post-chain coefficient 48, and the exact box majorant `6422139805764931584036533551104 / 702576099728137594188684005 = 9140.845821897... < 10000`. Its use in the manuscript still depends on repairing A3. |
| A5 paired polygamma and elementary cube-integral estimates | **PASS for the intended `Log M` formulation** | The repeated-FTC cube identity, signs, parameter differentiation, remote `A` boundary, and paired `B-C` and `D-(n+1/2)` scales were checked from their displayed definitions. The pairing gives segment length `O(n/log n)` times `psi^(6)=O(n^-6)`. Deliberately leaving the half-shift unpaired gives `n^5 psi^(5)(n+1/2) -> 24`, which falsifies the manuscript's `log gamma` wording and confirms the pairing is load-bearing. |
| A6 four-parameter C1 branch and quantified box hypotheses | **PASS at paper-existence level** | Exact rational recalculation gives the positive solution `(3,2,16/3,1/3)`, both inverse identities, inverse infinity norm `304/3`, and ordering margins `30>11/4` and `103/144>0`. Phase 14-15 gives uniform whole-box `C1` convergence and a valid fixed-inverse Banach argument. The packet does not supply the concrete xi-specific interval enclosures suggested by the main manuscript; see Finding 3. |
| A7 coefficient asymptotic and transfer to Jensen coefficients | **PASS conditional on the A2/A3 repairs** | Rechecked the two-step correction `R_N`; `N^2 log R_N` tends numerically to `-1/6` from the defining formula. The factorization of the smaller `F(N+2)` term and the scale `S=B R_1>0` correctly identify `P(y)=J^{d,n}(-y/S)/gamma(n)`. The printed proof presently inherits both failed gates. |
| A8 sixth-order interpolation remainder and theorem-sector uniformity | **PASS** | The complex six-node Hermite--Genocchi formula has the correct simplex mass `1/720` and six factors. The thickened interval is convex; `d+2rho<=eta n` places `n+Omega` in the smaller sector; and `rho^6=(K_r^6)(Bd)^3` gives the claimed `d^3/(n^2 log n)` exponent. This gate requires the corrected A5 residual. |
| A9 effectivity ledger and finite-range absorption | **PASS for an existential/effective-in-principle constant** | Recomputed the exact ledger DAG and finite branch arithmetic. `K_geometry=522255954073519803473068032000000000000000001`; `C_B6` and `N_analytic` remain honestly symbolic. `K_finite=N_0^2(N_0+2)+1` makes every antecedent with `n<N_0` empty because `d>=1` and `log(n+2)<=n+2`. No useful or fully numerical `K` has been established. |
| A10 final theorem quantifiers and dependence on imported results | **UNCHECKED in part** | The `d>=1,n>=0` quantifiers and low-degree/eventual/finite-absorption split are coherent. However the exact source texts for the classical Jacobi correspondence, MMP v3, and MSS Theorem 1.6 are not in this analytic archive, so their hypotheses and convention translations were not independently audited. The final theorem also cannot pass while A2 and A3 fail in the frozen manuscript. |

## 3. Findings

### Finding 1 — P1: the printed Gaussian direction has the wrong sign

The main manuscript says the contour is translated to the horizontal line
through `L_s`, then writes the local point as `L_s+i v` and claims a quadratic
term `-K_s v^2/2` (`JENSEN_TWO_THIRDS_MAIN.tex:322-371`). The supplement and
detailed appendix repeat the same parameterization. But the displayed
curvature identity is `h''(L_s)=-K_s`; therefore

```text
h(L_s+i v)-h(L_s) = (-K_s)(i v)^2/2 + ... = +K_s v^2/2 + ... .
```

Since `Re K_s>0`, this is ascent. A horizontal line through
`L_s=alpha+i b` is `L_s+r`, `r` real. The packet's later note
`C48_LEADING_CONTOUR_LOCALIZATION.md:110-449` uses that correct coordinate,
retains `h'(L_s)=1` after the Jacobian is included, and obtains the Gaussian
estimate. The manuscript must be repaired throughout the leading-mode and
higher-mode sections; merely changing a symbol without reconciling the
Jacobian/amplitude and cubic calculation would be insufficient.

### Finding 2 — P1: `h=log gamma` double-counts the gamma half-shift

At `JENSEN_TWO_THIRDS_MAIN.tex:422`, the manuscript defines
`h(x)=log gamma(x)`. It then states the moment-saddle derivative tower and,
at lines 795-820, separately subtracts `psi^(5)(n+1/2+z)` in `E_F^(6)`.
The packet's actual derivation instead defines `h=Log M_z` in
`phase9/C48_SIGNED_FIFTH_SADDLE.md:15`,
`phase18/C48_COMPLEX_SIXTH_SADDLE.md:16-17`, and
`phase21/C48_DOWNSTREAM_DISCHARGE.md:35-43`.

Legendre duplication gives

```text
gamma(z) = sqrt(pi) 2^(-2z) M_z / Gamma(z+1/2),
(log gamma)^(6) = (Log M)^(6) - psi^(5)(z+1/2).
```

Thus the printed definition and printed residual formula count the half-shift
twice. More basically, the displayed tower is not the tower of `log gamma`:
`psi^(5)(n+1/2) ~ 24/n^5`, whereas the claimed moment term is
`48/(n^5 L_n)`. The independent script finds
`n^5 psi^(5)(n+1/2)=23.99700049` at `n=100` and convergence toward 24.
This term cannot be absorbed into `C/(n^5 log n)`.

The repair should define the analytic continuation `M_z`, set
`h=Log M_z`, derive it from the sectorial coefficient theorem using the exact
gamma ratio, and then retain the paired half-shift in `E_F^(6)`. All later
uses of “logarithmic coefficient derivatives” must be audited for the same
object.

### Finding 3 — P2: the manuscript overstates the branch interval evidence

`JENSEN_TWO_THIRDS_MAIN.tex:601-615` says “Exact interval certificates” verify
the center displacement and whole-box contraction for `G_n`. The included
`branch_interval_certificates.py` explicitly says it **does not claim the
analytic residual or Jacobian enclosures**; it checks only rational margins,
inverse row sums, ordering extrema, and implication arithmetic. Phase 14-15
does provide a conventional uniform-`C1` existence proof, so this is not a
new theorem gap, but the evidence description must be narrowed or the
xi-specific enclosures actually supplied.

### Finding 4 — P2: the supposedly separated packet exposes prior verdicts

`BUNDLE_METADATA.json` says prior reports are excluded, but the included
`ground_zero_work/CLAIM_LEDGER.md` and several analytic-note status headers
state earlier analytic-review outcomes. I did not open a prior full report or
an author response, and I had not reviewed an earlier freeze, but I was
exposed to previous verdict summaries while following the packet's evidence
map. This pass must therefore be described as a **separated correlated
re-review**, not a pristine blind independent pass. Future blind packets
should remove verdicts and finding-disposition language from all included
evidence, not only omit report files.

### Finding 5 — P3: `G_0` is never defined in the manuscript

`JENSEN_TWO_THIRDS_MAIN.tex:446-461` invokes `G_0^(6)` and its exact rational
form, but neither the main manuscript, supplement, nor included detailed
appendix defines `G_0`. The definition exists only in internal notes. Add the
explicit saddle main term before differentiating it; this will also make the
`Log M_z` repair in Finding 2 auditable by a reader.

## 4. Independent recalculation record

The scripts are in `scripts/` beside this report. Each constructs its inputs
from definitions and reads **no frozen expected result, JSON, ledger, notebook,
or candidate script output**.

| Script | Independent construction | Result |
|---|---|---|
| `scripts/recalc_saddle_tower.py` | Custom sparse exact rational differentiator using only `fractions.Fraction`; starts from the implicit saddle equation and explicit `G_0` | Reproduced denominator power 12, 82 terms, degree 13, origin 24, chain 48, and exact `9140.845821897...` box majorant. |
| `scripts/recalc_normalization_contour.py` | Standard-library Hasse zeta, Lanczos gamma, theta/omega kernel, saddle Newton solve, and direct Simpson integrals | Reproduced the factor eight numerically, strict Rouché envelope at `ell=12`, leading saddle ratios approaching one, strong second-mode suppression, and the `-1/6` two-step correction. Numerical only. |
| `scripts/recalc_branch_and_log_definition.py` | Exact rational branch/Jacobian arithmetic plus the duplication formula and a directly summed polygamma series | Reproduced the positive branch and inverse norm, and exposed the `Log M` versus `log gamma` mismatch with the unpaired `24/n^5` term. |

Commands run successfully:

```text
python3 VERIFY_BUNDLE.py
  PASS Phase-L AI reviewer bundle manifest (89 files)

python3 scripts/recalc_saddle_tower.py
python3 scripts/recalc_normalization_contour.py
python3 scripts/recalc_branch_and_log_definition.py
python3 evidence/ground_zero_work/phase25/branch_interval_certificates.py
```

The included Phase-21 aggregate verifier was attempted but could not run in
this isolated archive because the available `python3` lacks the pinned
`mpmath==1.3.0` and `sympy==1.14.0`; `python-flint` is also unavailable. I did
not use a repository virtual environment outside the archive, because the
review instructions limited evidence to the ZIP. This execution limitation
does not affect the standard-library clean-room calculations above.

## 5. Unchecked claims

- Exact hypotheses and statement directions of MMP v3 Proposition 2.7(iii),
  Definition 2.16, Proposition 2.17, and MSS Theorem 1.6; primary texts were
  not supplied in this analytic archive.
- The classical transported Jacobi matrix/root correspondence and the exact
  entry bounds used before Gershgorin.
- Lean kernel/build claims and axiom audit; this was the analytic track and the
  archive lacks a runnable isolated Lean build surface.
- Frozen Mathematica and Arb/ACB outputs as independent executions. Their
  records were available as candidate evidence, but Mathematica had no kernel
  configured and `python-flint` was unavailable; I did not treat saved outputs
  as my recalculation.
- A fully numerical value of `C_B6`, `N_analytic`, or `K_final`. The existential
  dependency formula is checked, not a practical threshold.
- PDF visual fidelity. Mathematical equations were reviewed from the supplied
  TeX sources; no mathematical conclusion depends on page rendering.

## 6. Release recommendation and exact blockers

**Do not release candidate commit `5641348d...` as a complete proof.** Before
a new freeze:

1. replace the `L_s+i v` contour with the legal horizontal coordinate
   `L_s+r`, and reconcile the Jacobian/amplitude, linear term, cubic
   cancellation, tails, and higher-mode formulas in the main paper,
   supplement, and appendices;
2. define `M_z` and `h=Log M_z`, insert the exact duplication bridge from the
   sectorial coefficient theorem, and remove every `log gamma`/moment
   conflation in the derivative and residual sections;
3. define `G_0` explicitly and make the manuscript proof agree with the
   repaired evidence notes;
4. correct or substantiate the “exact interval certificates” claim;
5. freeze a new commit and rerun the required separated reviews. A genuinely
   blind packet must remove previous-verdict summaries from included notes.

## 7. Model, provider, tools, context, conflicts, and separation

- Model/provider: OpenAI Codex, GPT-5-family model. The exact deployment
  identifier was not exposed in the review environment.
- Tools: archive extraction, `python3`, standard Unix text tools (`rg`, `sed`),
  and custom standard-library recalculation scripts. No web access, external
  repository source, prior full review report, or other Phase-L track was used.
- Context access: the supplied analytic ZIP, the task instructions, and the
  required output directory only. Candidate evidence was not edited.
- Conflicts: no personal, financial, or institutional conflict is known. This
  is an AI system reviewing AI-assisted work, which is itself a material
  correlated-error risk.
- Earlier freeze: I had not reviewed an earlier freeze. However, prior verdict
  summaries embedded inside this packet were visible, as described in Finding
  4. Accordingly this is a separated correlated re-review, not a fully blind
  independent pass.

## 8. Review-status disclosure

This is AI review, not human or peer review.
