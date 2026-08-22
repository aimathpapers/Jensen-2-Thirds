# Phase-L hostile falsification correlated AI re-review

## 1. Overall verdict

**Verdict: R2 — release not recommended from this freeze.** I found **no P0 or
P1 theorem-level counterexample or regression**, but three material P2 defects
remain: the release manuscript overextends the legal shifted contour to a full
horizontal line across the declared logarithm cut, the archive-local replay
entry points are missing or misrooted, and the final effectivity formula uses
an undefined threshold name. These defects are repairable and do not furnish a
counterexample to the stated two-thirds theorem, but they should be corrected
before release. A targeted recheck of those corrections is warranted.

This is a **targeted correlated AI re-review** of repaired candidate
`6ee1db8fc5789a01bc0297f850c817f55b529be4`, not an independent review. The
required checkpoint is `5f79158f9c6276dd09142edeea279e35b0d58406`.

## 2. Gate sheet

`PASS` means that the stated hostile attack found no counterexample within the
scope described; it is not a claim of formal completeness.

| Gate | Status | Hostile evidence and method |
|---|---|---|
| H0 normalization/factorial/sign/factor eight | PASS | `recalculate_factor_eight.py` constructs xi, the theta kernel, and the Mellin moments from definitions. It matched the factor-eight identity at `n=0,1,2` to better than `1e-35` relative error and independently checked the duplication prefactor. |
| H1 sector/domain/branch/uniformity | **FAIL** | The horizontal direction and quadratic sign are repaired: independent finite differences give horizontal descent `-K r^2/2` and vertical ascent `+K v^2/2`. But the literal `r in R` contour in the main paper and supplements hits the principal-Log cut when the legal parameter `s>0`; Finding 1 gives the exact counterexample. |
| H2 positivity/ordering/contraction/Q | UNCHECKED | Endpoint arithmetic gives `A>B>C>D>0` on the stated outer box for `e<=1/12`, and the displayed `|r|,|sigma|<=7/50` implication gives `Q != 0`. The branch ledger wording is now honest. I did not independently construct the xi-specific whole-box residual and derivative inequalities used as analytic premises for the contraction. |
| H3 recurrence denominator/termination/degeneracy | PASS | `reattack_radius_and_legal_box.py` constructs a legal large-`n`, `d=8` parameter tuple, the terminating `3F2` coefficients, all four recurrence coefficients, and the derivative ratios. It verifies the recurrence through `m=d-2`, positive central coefficient, and `T_(d+1)=0`. |
| H4 finite-free/reflection/root orientation/imports | UNCHECKED | I found no convention contradiction in the packet, but the cited third-party MMP/MSS papers were intentionally not supplied and were not consulted outside the archive. I therefore did not independently validate the imported theorem statements or their precise hypotheses. |
| H5 radius/localization/exponent/tails | **FAIL** | The repaired global-maximum radius logic passes: on the legal constructed tuple the worst normalized three-neighbor budget is `0.0119916468261 < 1`, including the higher-neighbor term. The manuscript's full-line tail quantifier is nevertheless not legal on the declared branch; this is the same defect as Finding 1. The included detailed Phase-21 note supplies the correct ray. |
| H6 hidden implication/missing quantifier | **FAIL** | The actual contour has a finite left endpoint after splitting at `u=1`, whereas the release text quantifies `r over R`; the final threshold also contains an undefined symbol. See Findings 1 and 3. |
| H7 effectivity/circularity/finite range | **FAIL** | The choice order is not visibly circular, and the `N_0^2(N_0+2)+1` term is capable of excluding the finite range. However, `N_elementary` in the final manuscript formula is never defined and does not match the ledger's `N_explicit`; literal effectivity therefore cannot be replayed. |
| H8 stale artifacts/source mismatch/verifier false positives | **FAIL** | Both required top-level verifiers pass, and direct Tectonic builds from `manuscript/source` reproduce both frozen PDF hashes exactly. The advertised archive-local replay commands are nevertheless missing or point at the wrong tree; see Finding 2. The manifest verifier does not test these entry points. |
| H9 end-to-end legal-parameter counterexample | UNCHECKED | I attacked the exact limiting system and a legal large-`n`, `d=8` recurrence/radius instance and found no theorem counterexample. I did not exhaust the asymptotic parameter range or independently instantiate the analytic constants, so an end-to-end universal PASS would overstate the evidence. |

## 3. Numbered findings

### LHR-1 — P2: the literal full horizontal contour crosses the declared logarithm cut

The repaired direction and sign are correct, but the release text now says
that the translated contour is the horizontal line through `L_s`, that the
translation stays in the principal-log domain, and that it is parameterized
by `u=L_s+r` for every real `r`. The technical supplement and detailed
appendices repeat `r in R` and quantify the tail over all `|r|>=V`.

Take the legal positive-real case `s>0`. Then `L_s>0` is real. Choosing

```text
r = -L_s - 1
```

gives `u=-1`, which lies on the excluded cut of the principal `Log u` used in
the phase. Thus the assertion that the full line remains in the declared
domain is false, with no limiting or numerical subtlety.

The packet itself contains the repair: the detailed Phase-21 contour note
splits off `[0,1]`, translates only the ray `x>=1` to `x+i Im(L_s)`, and hence
uses `r>=1-Re(L_s)`. The integral over the full real Gaussian is then a local
comparison after endpoint/tail control, not the actual contour. The release
manuscript and both supplements should state that legal ray and separately
justify extension of the central Gaussian surrogate to `R`. Because a correct
proof route is already present in the frozen packet and no theorem statement
changes, I classify this as P2 rather than P1.

### LHR-2 — P2: the archive-local replay entry points are not executable as documented

`START_HERE.md` now honestly says that full replay uses the exact private
repository commit. That resolves the earlier overclaim that the review archive
itself is a complete full-build environment. Two archive-local artifacts still
contradict a usable replay contract:

1. `evidence/reproduce/README.md` documents `reproduce/VERIFY_ALL.sh` in
   `quick`, `full`, and `clean` modes, but no `VERIFY_ALL.sh` is included.
2. The included `evidence/reproduce/BUILD_MANUSCRIPTS.sh` computes its root as
   `evidence/` and requests `evidence/paper/JENSEN_TWO_THIRDS_MAIN.tex` and the
   supplement. There is no `evidence/paper/`; the archive sources are under
   `manuscript/source/`.

Running the advertised manuscript command from `evidence/` fails in Tectonic
with `primary input not available`. This is not a TeX-source defect: compiling
both files directly from `manuscript/source/` with
`SOURCE_DATE_EPOCH=1786968000` succeeds, and the resulting SHA-256 values
exactly equal the frozen PDFs:

```text
c6bfb6c31ce9f6a74e857a599ffca62e64a393574cbd1ac09a8b2073244d7813  main
d9f167b3333950da301ba0bcecdd696ba3ca4fc3e62279abc2327d02a2cd3448  supplement
```

The packet should either provide archive-aware entry points or label the
included repository-oriented README/script as non-runnable provenance and
give the exact archive-local PDF command. `VERIFY_BUNDLE.py` only validates
manifest bytes, so its PASS cannot detect this behavioral failure.

### LHR-3 — P2: the final effectivity formula names an undefined threshold

The main paper defines

```text
N_0 = max{N_analytic, N_elementary}
```

in the displayed formula for `K_final`, but `N_elementary` has no other
occurrence or definition in the release source. The effectivity ledger instead
defines `N_explicit` and uses `N_0=max(N_explicit,N_analytic)`. This looks like
a one-token name drift, but until it is corrected the manuscript's purported
explicit dependency formula is not a defined mathematical expression. The
existential theorem and its non-circular order of choices are not falsified,
so this is P2 rather than P1.

### LHR-4 — P3: stale tail variables obscure the repaired contour

The technical supplement says “Splitting at `|v|=1`” after switching the
horizontal variable to `r`; the detailed appendix repeats the same stale
variable. These should say `|r|=1` (and be stated on the legal ray from Finding
1). This is editorial by itself.

## 4. Independent recalculation record

All reviewer-authored programs are under `rereview_scripts/`. Each constructs
its inputs from displayed definitions and **does not read any frozen expected
result**.

| Script | Result | Frozen expected data read? |
|---|---|---|
| `rereview_scripts/recalculate_factor_eight.py` | PASS for `n=0,1,2`; reconstructs xi, theta derivatives, omega, Mellin integration, factorial normalization, and duplication identity. | No |
| `rereview_scripts/reattack_contour_and_elimination.py` | PASS for horizontal descent, vertical ascent, and the two corrected elimination identities on exact rational box points; also constructs the exact full-line branch-cut counterexample. | No |
| `rereview_scripts/reattack_radius_and_legal_box.py` | PASS for a constructed legal `n=10^12,d=8` tuple, ordering, finite producer, termination, all used recurrence instances, and global-maximum neighbor budget. | No |

Additional packet checks and experiments:

- `python3 VERIFY_BUNDLE.py`: `PASS Phase-L AI reviewer bundle manifest (478 files)`.
- `python3 VERIFY_HISTORY.py`: history bundle OK; candidate and required
  checkpoint ancestry PASS. I did not unpack or inspect the history bundle.
- The packet's `reproducibility_behavioral_mutations.py` passes, but it is
  candidate-supplied regression evidence, not an independent recalculation.
- The advertised `evidence/reproduce/BUILD_MANUSCRIPTS.sh` fails as described
  in Finding 2. Direct Tectonic 0.17.0 builds from the actual archived source
  reproduce both frozen PDFs byte-for-byte.

## 5. Earlier-finding disposition

1. **Contour direction/sign:** the former vertical-direction Gaussian sign
   error is repaired. The manuscript now uses horizontal displacement and the
   correct negative quadratic. A new/residual domain-range defect remains at
   P2 because the actual ray is incorrectly enlarged to a full line.
2. **Higher-neighbor radius logic:** resolved. The proof uses a global weighted
   maximum, so every neighbor is bounded; termination supplies `T_(d+1)=0` at
   `k=d`. Independent construction found no recurrence or budget regression.
3. **Limiting-system elimination:** resolved. Both displayed combinations are
   exact identities, and positivity gives `t=2`, then `w=16/3`, `delta=1/3`,
   and `alpha=3` without the stale false identity.
4. **Branch evidence wording:** resolved. The manuscript now says exactly that
   the ledger checks rational margins, inverse arithmetic, and the implication
   from the analytic inequalities; it expressly does not claim xi-specific
   residual or Jacobian enclosures.
5. **Packet replay contract:** partially resolved. `START_HERE.md` discloses
   that full replay requires the private repository commit, but the included
   and advertised archive-local commands remain absent or misrooted (LHR-2).

No P0/P1 remains from these five attacks, and I found no new P0/P1 regression.
Release remains blocked in this R2 recommendation by LHR-1, LHR-2, and LHR-3.

## 6. Unchecked claims

- The complete sector-uniform contour estimates, endpoint constants, higher
  theta-mode summation, and six-derivative Cauchy transport were read and
  attacked locally, but were not independently rebuilt with explicit global
  constants.
- The xi-specific whole-box residual and derivative bounds assumed in the
  Banach contraction were not independently interval-certified; the repaired
  manuscript no longer claims that the exact ledger supplies them.
- The imported MMP finite-free and MSS maximum-root theorems and hypothesis
  matching were not checked against the primary publications, because the
  re-review was restricted to this archive and those publications were not
  included.
- The full Lean build, independent kernel replay, Arb/ACB suite, Wolfram
  checks, and clean-clone modes were not rerun: the packet says those require
  the private repository commit, and the documented `VERIFY_ALL.sh` is absent.
- The symbolic `C_B6`, `N_analytic`, and all legal `(n,d)` cases were not
  numerically instantiated or exhaustively searched. Consequently H9 remains
  UNCHECKED rather than a universal counterexample-free certificate.

## 7. Model, tools, separation, and conflicts

- **Provider/model:** OpenAI Codex, GPT-5-family model; the exact deployment
  identifier was not exposed to this session.
- **Tools:** local shell/text search, Python 3.11.16 with `mpmath 1.3.0`,
  Tectonic 0.17.0, the two packet verifiers, and reviewer-authored scripts.
  No network search or external publication lookup was used.
- **Evidence boundary:** evidentiary inputs came only from the privately
  extracted repaired hostile re-review archive. The repository Python
  environment was used only as an execution runtime, not as mathematical or
  expected-result evidence. I did not inspect repository files outside the
  archive, any prior report, another review track, or the author disposition.
- **History separation:** `CANDIDATE_HISTORY.bundle` was passed only to the
  supplied `VERIFY_HISTORY.py`; it was not cloned, unpacked, or browsed.
- **Candidate integrity:** I made no edits to candidate evidence. Reviewer
  scripts and this report were written only in the designated hostile review
  output directory; temporary build products were placed under `/tmp`.
- **Correlation/conflict:** I reviewed the earlier freeze, so this is a
  correlated re-review and cannot be described as separated or independent.
  That continuity is the material review conflict. I have no personal or
  financial conflict to disclose.

This is AI review, not human or peer review.
