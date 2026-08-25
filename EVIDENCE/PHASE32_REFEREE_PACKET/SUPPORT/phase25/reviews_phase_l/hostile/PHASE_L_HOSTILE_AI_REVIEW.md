# Phase L hostile falsification and counterexample review

## 1. Overall verdict

**R2 — major revision required; release blocked.**

I did not find a counterexample to the final existential two-thirds theorem. I did find a legal-parameter counterexample to a load-bearing displayed contour estimate in the main manuscript, detailed appendix, and technical supplement. The sign of the quadratic term on the printed path is reversed. The packet also contains a different, apparently corrective Phase-21 proof using the horizontal path. This is a theorem-affecting source mismatch, not a stylistic issue. Three further false or unsupported proof descriptions and a non-self-contained reproduction entry point require repair.

Status convention below: **PASS** means the claim survived the stated hostile tests; **FAIL** means a concrete falsifier or unrepaired logical/source defect was found; **UNCHECKED** means the packet did not permit an independent resolution.

## 2. Gate-by-gate review

| Gate | Status | Hostile evidence and recalculation method |
|---|---|---|
| H0 normalization/factorial/sign/factor eight | PASS | `scripts/finite_definition_checks.py` constructs `xi(1/2)` from the Dirichlet eta series and real gamma function, constructs the omega integral independently from theta derivatives, and obtains relative error `8.88e-16` at `n=0`. It also reconstructs the duplication prefactor for `n=0..20`. No frozen expected result is read. |
| H1 sector/domain/branch cut/uniformity | FAIL | `scripts/contour_direction_counterexample.py` uses the legal positive-sector input `s=e^12`, solves the displayed saddle equation, and obtains `L=8.69274166925432`, `K=20876.1914873219`. On the manuscript path `L+i v`, `Re(Phi(L+i v)-Phi(L))=0.0104380949051` at `v=10^-3`, agreeing with `+K v^2/2`, not the printed `-K v^2/2`. The path remains in the legal principal-log domain. |
| H2 box positivity/order/contraction/Q | UNCHECKED | Exact endpoint reconstruction passes `A>B>C>D>0` and the `151/200`, `151/50` Q-denominator margins. The packet does not contain an xi-specific whole-box residual/Jacobian interval certificate, so the contraction part was not independently certified. |
| H3 recurrence denominator/termination/degeneracy | PASS | `scripts/finite_definition_checks.py` constructs a legal `A>B>C>D>0` shifted terminating producer at every derivative order and verifies positive denominators and exact termination. No legal recurrence-denominator counterexample was found. The manuscript's *argument* from the recurrence nevertheless has a separate H6 defect below. |
| H4 finite-free reflection/root orientation/MSS/MMP | UNCHECKED | The reversal and interval algebra survived inspection, including reciprocal endpoints and logarithmic-mesh direction. The actual MMP/MSS/Jacobi source artifacts are not in the permitted archive; only an internal source-audit record is present, so the imported theorem text was not independently source-verified. |
| H5 radius/localization/exponent/tail summation | FAIL | The arithmetic `rho^6 ~ (Bd)^3` and the stated `d^3/(n^2 log n)` exponent survived. The printed contour tail proof does not: it is built on the wrong `L+i v` direction. In addition, the printed first-failure radius argument treats the higher neighbor `T_(k+1)` as known; `scripts/first_failure_logic_probe.py` gives an exact recurrence-level countermodel to that inference. The separate Phase-16 global-maximum argument is the needed repair. |
| H6 hidden implication/missing quantifier | FAIL | Three defects: the false contour implication, the invalid first-failure narration, and the claim that exact interval certificates verify the branch although the packaged branch script expressly excludes the analytic residual/Jacobian enclosures. The displayed limiting-system identity is also false away from its zero, as shown exactly by `scripts/limiting_system_counterexample.py`. |
| H7 threshold/effectivity/finite range | PASS | The symbolic dependency order is acyclic: geometry first, then `C_B6`, `N_analytic`, and finite-range absorption. `N_0^2(N_0+2)+1` safely empties antecedents below the eventual threshold. The two analytic quantities remain symbolic and are disclosed rather than inferred from diagnostics. |
| H8 stale artifacts/source mismatch/verifier false positive | FAIL | `VERIFY_BUNDLE.py` passes all 131 manifest entries, but it checks hashes only. It does not detect the manuscript/Phase-21 contour mismatch or the false limiting identity. The packaged `evidence/reproduce/VERIFY_ALL.sh quick` is not runnable from this archive: the pinned `.venv` is absent, and overriding Python then fails because `ground_zero_work/phase25/verify_phase25_metadata.py` is absent. |
| H9 end-to-end legal parameter counterexample | UNCHECKED | I attempted legal positive-sector, branch-box, recurrence, and finite-parameter attacks. The proof chain is falsified at the displayed contour interface, but this is not a counterexample to the final theorem. Because `K` is existential and no complete independent analytic certificate is available, no concrete `(n,d)` can be certified as satisfying the final antecedent for a fixed proposed theorem constant. |

## 3. Numbered findings

### 1. P1 — the printed central contour has the Gaussian sign reversed

The main manuscript, its detailed appendix, and the technical supplement parametrize the central line as `u=L_s+i v` and claim a quadratic term `-K_s v^2/2`. From the same displayed definitions, the full logarithmic `u`-integrand has

```text
h'(L_s)=1,     h''(L_s)=-K_s.
```

Consequently

```text
Re(h(L_s+i v)-h(L_s))=+Re(K_s)v^2/2+O(v^3).
```

If the Jacobian is kept outside the phase, the phase has zero first derivative but the same second derivative, so the vertical quadratic sign is still positive. At the legal real input `s=e^12`, the independent script obtains

```text
L = 8.69274166925432
K = 20876.1914873219
v = 0.001
Re(Phi(L+i v)-Phi(L)) = 0.0104380949051119
+K v^2/2                = 0.0104380957436610
```

Thus the printed path is locally an ascent direction, not a decaying Gaussian direction. The same defect invalidates the tail-concavity and mode-suppression text when it is tied to `L+i v`.

The packet's `evidence/ground_zero_work/phase21/C48_LEADING_CONTOUR_LOCALIZATION.md` instead uses the legal shifted horizontal contour `u=x+i Im(L)` and the central parametrization `u=L+r`, retaining the linear term

```text
h(L+r)-h(L)=r-Kr^2/2+c_3r^3+R_4.
```

That is a materially different argument. The manuscript must be synchronized to it and semantically retested. Until then, the printed proof of T3, and hence T4–T6 and T18, is not valid as written.

### 2. P2 — the printed first-failure radius argument does not control its higher neighbor

The recurrence at the alleged first failing index `k=m+2` contains

```text
P3_m T_(k+1) + P2_m T_k + P1_m T_(k-1) + P0_m T_(k-2) = 0.
```

Lower-index first-failure information says nothing about `T_(k+1)`. The detailed appendix nevertheless calls all three neighbors known. `scripts/first_failure_logic_probe.py` constructs exact rational data with lower indices bounded, `T_2` the first failure, normalized neighbor coefficients below the central coefficient, and `T_3` cancelling the recurrence.

The packet's Phase-16 note contains the correct repair: take a global maximum over all normalized `T_k`, so `T_(k+1)` is bounded by the same maximum, and handle `k=d` using termination. The main manuscript and appendix should state that maximum argument, not a first-failure induction.

### 3. P2 — the displayed limiting-system elimination identity is false

After defining `F=H^infinity+S^infinity`, the main manuscript displays

```text
3 t F_2 - F_3 = 3 w (t-1) - t^4.
```

At the legal outer-box point `(alpha,t,w,delta)=(3,2,5,1/4)`, direct exact evaluation gives

```text
F=(-1/6,-1/8,-5/16,-3/8),
3 t F_2-F_3=-3/2,
3 w(t-1)-t^4=-1.
```

The polynomial relation follows by eliminating `delta` from the *second and third zero equations*; it is not the printed residual identity. This does not refute the candidate solution `(3,2,16/3,1/3)`, but the displayed equation is false and should be corrected in both the main manuscript and supplement.

### 4. P2 — the manuscript overstates the available branch interval certificate

The main manuscript says that exact interval certificates on a smaller box verify the center displacement and whole-box derivative bound. In contrast:

- `evidence/ground_zero_work/phase25/branch_interval_certificates.py` explicitly says it “does not claim the analytic residual or Jacobian enclosures”;
- `INTERVAL_CERTIFICATES.json` contains box margins, ordering, saddle margins, localization arithmetic, and the sixth-derivative algebra, but no xi-specific center residual or whole-box derivative-defect enclosure;
- the theorem assurance matrix describes these analytic certificates as explicit inputs not constructed in Lean.

The conventional `C^1` convergence argument in the Phase-15 note may still provide an existential branch, but it is not the exact interval certificate claimed in the manuscript. Either supply the actual enclosure, or replace the evidence description with the asymptotic compactness/contraction proof actually available.

### 5. P2 — the packaged reproduction entry point is not self-contained

The archive passes `python3 VERIFY_BUNDLE.py`, which establishes internal hash consistency for 131 manifest entries. It does not establish mathematical correctness or replayability.

Running `evidence/reproduce/VERIFY_ALL.sh quick` fails first because the referenced pinned `.venv` is absent. With `/usr/bin/python3` supplied explicitly, it fails because `evidence/ground_zero_work/phase25/verify_phase25_metadata.py` is absent. Other referenced paths, including the `paper/` layout, are also not present in the archive. This conflicts with the manuscript's statement that the reviewer package lets a reviewer reproduce any channel. Either provide a self-contained replay packet or state precisely that full replay requires a separate repository checkout and is outside this archive.

## 4. Independent recalculation record

| Script | Construction and result | Reads a frozen expected result? |
|---|---|---|
| `scripts/finite_definition_checks.py` | Independently constructs `xi(1/2)` via Euler-transformed eta, the omega integral via theta derivatives, duplication prefactors, rational ordering/Q margins, and a legal terminating hypergeometric producer. All checks pass. | No; reads no file. |
| `scripts/contour_direction_counterexample.py` | Solves the saddle equation by Newton iteration and evaluates the phase on horizontal and vertical perturbations. It falsifies the manuscript's vertical Gaussian sign. | No; reads no file. |
| `scripts/limiting_system_counterexample.py` | Constructs `H^infinity+S^infinity` with exact fractions at an outer-box point and falsifies the displayed elimination identity. | No; reads no file. |
| `scripts/first_failure_logic_probe.py` | Constructs exact recurrence data showing that lower-index first-failure control cannot bound the higher `T_(k+1)` neighbor. It supports replacing the narration with the packet's global-maximum proof. | No; reads no file. |

Commands executed:

```text
python3 VERIFY_BUNDLE.py
PASS Phase-L AI reviewer bundle manifest (131 files)

python3 scripts/finite_definition_checks.py
PASS factor-eight n=0 definition check (relative error 8.88e-16)
PASS duplication prefactor n=0..20
PASS exact ordering and Q/reduced-denominator margins
PASS legal terminating coefficient producer at every derivative shift

python3 scripts/contour_direction_counterexample.py
FAIL manuscript vertical Gaussian direction

python3 scripts/limiting_system_counterexample.py
FAIL displayed limiting-system identity

python3 scripts/first_failure_logic_probe.py
FAIL first-failure inference from lower-index bounds
```

The word `FAIL` in the last three script outputs is intentional: those scripts are falsifiers and exit successfully only after reproducing the counterexample.

## 5. Unchecked claims

1. The general `n>=1` theta-kernel moment identity was inspected algebraically but independently recalculated only at `n=0`.
2. The corrected Phase-21 horizontal contour proof was not independently rebuilt with explicit uniform constants over the entire sector.
3. Uniform infinite-mode summation, sectorial Stirling assembly, and the full sixth logarithmic-derivative constant were not independently reconstructed end to end.
4. The xi-specific common-box `C^1` residual and Jacobian bounds for the four-parameter branch were not independently enclosed.
5. The imported classical Jacobi, MMP v3, and MSS Theorem 1.6 statements were not checked against their primary PDFs because those PDFs are not in the only permitted archive and no web access was used.
6. The full 82-term `H_6` numerator and the user-executed Mathematica provenance were not independently regenerated in another CAS.
7. A full Lean build, kernel replay, Arb/ACB replay, and manuscript build were not run; the archive's full/quick entry points are incomplete as packaged.
8. No complete end-to-end numerical counterexample to the final theorem was established, and the existential `K` is not numerically instantiated.

## 6. Release recommendation and exact blockers

**Do not release this freeze as a complete proof.** The minimum blockers are:

1. replace every `u=L+i v` central/tail proof in the main manuscript, detailed appendix, and supplement with the correct horizontal `u=L+r` argument, including the linear term and the actual tail estimates;
2. add a semantic regression that differentiates the phase in the asserted contour direction and fails on the current sign;
3. replace the first-failure radius narration with the global-maximum proof already present in the Phase-16 evidence;
4. correct the limiting-system elimination equation;
5. either provide the claimed xi-specific whole-box interval certificates or accurately describe the conventional `C^1` branch proof;
6. make the reviewer replay entry point self-contained, or clearly delimit the external checkout/environment it requires;
7. regenerate the PDFs and assurance/cross-reference artifacts, rerun all gates, and obtain a fresh separated hostile review of the synchronized freeze.

The legal contour counterexample is a P1 blocker even though a plausible repair already exists elsewhere in the packet. The report does not claim that the final theorem is false.

## 7. Model, provider, tools, separation, and conflicts

- **Provider/model:** OpenAI Codex, GPT-5 family. The exact serving snapshot identifier was not exposed to this reviewer.
- **Tools:** private temporary extraction, `unzip`, Python 3 standard library, `rg`, `sed`, `find`, and shell execution. No network or web search was used. No sub-agent or other reviewer was consulted.
- **Context access:** mathematical review used only `/Users/jsavva/Documents/Math/My Math research/Zeta Function/output/reviewer_packets_phase25_ai/Jensen_Two_Thirds_Phase25_Hostile_AI_Review_Packet.zip` after extraction. I did not inspect repository evidence outside the archive, any prior review report, any author response/disposition, or another Phase-L track. The only writes were this report and its four scripts in the required hostile review directory; candidate evidence was not edited.
- **Earlier freeze:** I have not reviewed an earlier freeze of this candidate in this task and had no earlier review report in context. This is a separated pass, not a correlated re-review.
- **Conflicts:** no financial, personal, authorship, or institutional conflict is known. As an AI system, I cannot supply human independence or scholarly judgment.

This is AI review, not human or peer review.
