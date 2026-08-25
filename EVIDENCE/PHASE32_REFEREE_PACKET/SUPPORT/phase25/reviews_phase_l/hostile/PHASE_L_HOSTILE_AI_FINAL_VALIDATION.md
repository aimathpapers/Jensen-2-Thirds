# Phase-L hostile AI final validation

## Verdict

This targeted final validation finds **no surviving P0 or P1** in the four
requested repair areas. It finds **one surviving P2**: the legal contour is
now geometrically correct on all three manuscript surfaces, but the new exact
rectangle display uses undeclared first-mode notation and never identifies its
`I_1` with the later `F_1`.

The `N_explicit` repair and the corrected expanded `P_{2,m}` coefficient pass
definition-level checks. The old Phase-L packet-local replay defect is
adequately disposed **at Phase-L scope** by preserving those packets as
historical review evidence and making fresh archive-local replay a mandatory
Phase-M acceptance gate. Phase M has not yet been executed in this validation,
so this is a process disposition, not a claim that the future replay passed.

This is a targeted **correlated AI re-review**: I performed the earlier
Phase-L hostile review and final validation cannot be called independent.

## Targeted disposition

| Repair target | Result | Evidence |
|---|---|---|
| Legal contour ray in the main paper | PASS geometry; P2 notation | The paper now splits at `u=1`, uses the rectangle `1,X,X+ib,1+ib`, restricts the actual ray to `r >= 1-Re L_s`, and calls the full real Gaussian only a comparison integral. The earlier branch-cut counterexample no longer applies. |
| Legal contour ray in the technical supplement | PASS geometry; P2 notation | The supplement gives the same exact rectangle and `r >= 1-Re L_N`, controls the finite endpoint term, and restricts both tails to the actual ray. |
| Legal contour ray in the detailed appendices | PASS geometry; P2 notation | The appendix gives the same legal range and explicitly says the full Gaussian is not the deformed contour. The stale `|v|=1` variable is corrected to `|r|=1`. |
| Effectivity threshold | PASS | The main paper now has `N_0=max{N_analytic,N_explicit}`, exactly matching the effectivity ledger. `N_elementary` is absent from the current manuscript surfaces and is rejected by the source gate. |
| Expanded recurrence coefficient | PASS | Direct expansion of the shifted Euler ODE gives `B+D+2m+1-(Dy/(AC))(A+C+3m-d+3)`. Independent symbolic expansion of the decomposed coefficient gives the same expression. The stale `3m` version differs by exactly `m`. |
| Phase-L packet-local replay | CLOSED AS HISTORICAL; PHASE-M GATE PENDING | The old review ZIPs freeze earlier evidence and should not be rewritten after review. They are not listed in the current release manifest. Preserving them as historical evidence is sound provided Phase M creates and actually tests a new final-candidate archive whose documented replay works after extraction without relying on repository-relative paths. |

## Surviving finding

### FLHFV-1 — P2: the repaired contour display is not self-contained in any manuscript surface

The legal contour repair introduces

```text
I_1(s) = E_s + integral g_s(x+ib) dx
```

in the main paper and the analogous `I_1(N),g_N` formulas in the supplement
and appendix. Across the current paper tree:

- `I_1(s)` occurs only in the repaired identity, while the resulting saddle
  formula is subsequently stated for `F_1(s)`;
- the supplement likewise switches from its sole `I_1(N)` occurrence to
  `F_1(N)`;
- `g_s` and `g_N` occur only inside the repaired identity and endpoint term,
  with no definition; and
- `Phi_s`/`Phi_N`, whose Taylor expansion is used immediately afterward, is
  also not defined on these manuscript surfaces.

The geometry can be made self-contained by defining, before the rectangle,
for example

```text
Phi_s(u) = s Log(u) - 3u/4 - pi exp(u),
g_s(u) = exp(Phi_s(u)) exp(u),
I_1(s) := F_1(s) := integral_0^infinity g_s(u) du,
```

with the corresponding `N` notation in the two other surfaces. This preserves
the manuscript's convention that the Jacobian `exp(u)` is outside the phase.
The exact rectangle identity and all subsequent range statements then become
literal. This is P2 because the intended integrand is reconstructible from the
preceding Mellin definition and the proof geometry is correct, but an “exact
identity” should not depend on undeclared notation or an unspoken `I_1=F_1`
alias.

## Definition-level checks

Reviewer script:

```text
ground_zero_work/phase25/reviews_phase_l/hostile/final_validation_checks.py
```

It constructs the shifted contour geometry and `P_{2,m}` from definitions,
symbolically expands both ODE and decomposed forms, checks the current three
manuscript surfaces and effectivity ledger, and reads no frozen calculation as
expected data. Its result is:

```text
PASS legal contour geometry, exact P2 coefficient, and N_explicit consistency
FOUND P2 manuscript surfaces do not define I_1/g/Phi or identify I_1 with F_1
```

Additional current-working-tree checks:

- `manuscript_release_checks.py`: PASS.
- `manuscript_semantic_mutations.py`: PASS, including rejection of the full
  contour line, stale `3m`, `N_elementary`, and `|v|` mutations.
- `effectivity_ledger.py --check`: PASS.
- `reproduce/VERIFY_ALL.sh quick`: PASS.
- Both manuscripts compile successfully with Tectonic 0.17.0 to a private
  temporary output directory; candidate PDFs were not overwritten.

The existing source gate does not catch FLHFV-1 because it checks the repaired
range and stale formulas but not declaration/alias completeness for the new
contour symbols.

## Phase-M replay requirement

Treating the Phase-L ZIPs as historical evidence is an adequate disposition
of their packet-local path defect; retroactively changing reviewed archives
would blur provenance. It does not waive replay. Before release, Phase M must:

1. freeze the final candidate, including the contour-notation repair;
2. package every file needed by its declared archive-local checks;
3. document only commands that exist at the documented extracted paths;
4. run those commands from a new private extraction with no repository checkout
   supplying implicit files; and
5. record the commands, PASS markers, manifest identity, and any intentionally
   external full-build boundary.

If Phase M omits or fails this extraction-only replay, the replay defect should
be reopened as P2. No Phase-M archive was available in the present validation,
so the gate remains pending rather than silently passed.

## Scope and disclosure

I reviewed only the requested current repair surfaces and their directly
connected source gates. I did not edit candidate evidence. The only new file
beside this report is the reviewer-authored validation script. Tools were local
shell/text search, Python 3.11 with SymPy, the current quick verifier, and
Tectonic. No human judgment, external publication search, or peer-review
status is inferred from these checks.

This is AI review, not human or peer review.

## Final addendum — contour notation repair closed

This addendum supersedes the earlier FLHFV-1 disposition. The current working
tree now defines, before contour deformation, on all three manuscript
surfaces,

```text
Phi_q(u) = q operatorname{Log}(u) - 3u/4 - pi exp(u),
g_q(u) = exp(u) exp(Phi_q(u)),
I_1(q) := F_1(q) := integral_0^infinity g_q(u) du,
```

with `q=s` in the main paper and `q=N` in the supplement and appendix. Thus
`g_q(u)=exp(q Log(u)+u/4-pi exp(u))`, exactly reconstructing the original
first-mode integrand, while `Phi_q'(L_q)=0` is equivalent to
`q=L_q(pi exp(L_q)+3/4)`. The phase/Jacobian separation and the `I_1=F_1`
alias are therefore literal rather than inferred.

The production source gate passes. The new mutations that (i) absorb the
Jacobian into the phase by replacing `-3u/4` with `+u/4`, and (ii) disconnect
the `I_1:=F_1` alias are both rejected. An independent SymPy reconstruction of
the integrand and saddle equation also passes for both `s` and `N`.
Reviewer-authored `post_repair_validation_checks.py` records `PASS post-repair Phi/g/I_1=F_1, legal ray, recurrence, and effectivity validation`.

**Final targeted status: FLHFV-1 is closed; no P0, P1, or P2 survives in the
four requested repair areas.** The separate Phase-M archive-local replay gate
remains a mandatory future acceptance condition exactly as stated above; this
addendum does not claim that Phase M has run.

This addendum is a correlated AI re-review, not human or peer review.
