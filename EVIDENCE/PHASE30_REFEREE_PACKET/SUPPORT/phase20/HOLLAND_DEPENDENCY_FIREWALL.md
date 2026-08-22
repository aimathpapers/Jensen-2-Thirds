# Holland dependency firewall

Date: 2026-08-15
Status: implemented research dependency policy; the candidate theorem remains
unrefereed and is not advertised as established

## Decision

The candidate two-thirds Jensen wedge does **not** assume Holland's Theorem
1.1.  Holland v1 is used as an architectural guide and as the source of a
small number of formulas whose proofs are reproduced or replaced below.  This
prevents a defect in Holland's parameter branch, final assembly, or stated
constant from automatically propagating into the candidate theorem.

**Phase-21/23 update.**  No complex-uniform saddle estimate is now imported as
a premise.  Phase 21 derives the required fixed-sector estimate directly from
the xi/Mellin integral, including a legal contour, higher-theta suppression,
the factor-eight normalization, and sectorial Stirling.  GORTTW remains a
frozen primary source for the real-axis architecture and printed main term;
its terse complex-extension sentence is a comparison target, not an assumed
step.

## Frozen sources

| Source | Frozen version | SHA-256 |
|---|---|---|
| Holland PDF | arXiv:2608.08682v1 | `3fc31ba84fb113bc0b3109fb0e569bd1d7183018485aca1eb1dab565c839b49d` |
| Holland source archive | arXiv:2608.08682v1 | `f2fe1a202eae2d9a54291f223897b4fc5355011d6f4d0470d64c9d420bbb18af` |
| Holland `jensen.tex` | extracted from v1 | `f561d6dd53606ae054e5ab5fcb8dad4e9690cb9557c27b0a1a3845260f5205e0` |
| GORTTW PDF | arXiv:1910.01227v3 | `f203487acc45a58808462e897240ce4929c998d9f0230d9a4bedb6d3841c3b2c` |
| GORTTW source archive | arXiv:1910.01227v3 | `d3918516b2310ec7215129122515b394c2735a43cb95a627815f75096f416c1c` |
| GORTTW `Jensen_Revision.tex` | extracted from v3 | `e482b9b43840543af9066d67196e31d9166f9920a5be356dc2c35ef3a7773c98` |
| MMP PDF | arXiv:2309.10970v3 | `23f228e0682430c1ae6285be4abed4d730e9a08accad6c3f540fbdf4eb5bb4a3` |
| MMP source download | arXiv:2309.10970v3 | `696fbd8ca0187d95826e6c14f096cb6a3df1ecaf70e56c4330d0f3486fa3b99a` |
| MSS publisher PDF | PTRF 182 (2022), DOI `10.1007/s00440-021-01105-w` | `8560452b14504605fed2db0b6a57fd2f48a4bfeea9b75dfef0f66cd54f464219` |

Primary records:

- [Holland arXiv:2608.08682v1](https://arxiv.org/abs/2608.08682v1).
- [GORTTW arXiv:1910.01227v3](https://arxiv.org/abs/1910.01227v3),
  published as *Advances in Mathematics* 397 (2022), 108186.
- [Martínez-Finkelshtein--Morales--Perales
  arXiv:2309.10970v3](https://arxiv.org/abs/2309.10970v3), published in
  IMRN (2024).

## Interface disposition

| Interface used by the candidate | Disposition after Phase 20 |
|---|---|
| Holland Theorem 1.1 (`3/5` wedge) | **Not a premise** |
| Moment/coefficient normalization | Re-derived from the xi kernel and Legendre duplication; the GORTTW factor-eight convention is displayed |
| Saddle-variable existence, uniqueness, holomorphy, and `L_N ~ log N` | Proved directly in `phase18/C48_SECTORIAL_SADDLE_VARIABLE.md` by Rouché |
| Holland Proposition 4.1 | Not cited as a black box; its required interface is reconstructed in `HOLLAND_PROP41_REPROOF.md`, with the former GORTTW-sector premise discharged directly by Phase 21 |
| Fifth-order multiplier stability, Holland Proposition 2.2 | Reproved in `HOLLAND_MULTIPLIER_REPROOF.md`; finite sign/tail core formalized in Lean |
| Holland parameter branch, Lemma 6.1 | **Not used**; replaced by the four-parameter branch in Phases 14--15 |
| Holland assembled finite-free Lemma 7.3 | **Not used**; one hypothesis fails on the new branch; replaced by a ratio-free Jacobi lemma plus direct MMP citations |
| Holland residual Lemma 8.1 | Architectural precedent only; the order-six residual is proved in Phase 18 |
| Holland recurrence Lemma 9.1 | **Not used**; replaced by the shifted `_3F_2` ODE derivation in Phase 16 |
| MMP positivity/log-mesh preservation | Direct published input; exact reversal/orientation stated in Phase 16 |
| MSS largest-root product bound | Direct published Theorem 1.6; reciprocal-polynomial interval adapter stated in Phase 16 |

Phase 24 checked MMP Propositions 2.7(iii), 2.11, and 2.17 against the
hash-frozen v3 PDF/source and MSS Theorem 1.6 against the open publisher PDF.
The corrected v3 MMP statement is used.  Holland's citation of MSS Theorem
1.13 in his interval lemma is replaced by the direct published Theorem 1.6
citation, which is the displayed largest-root product inequality.

## Logical boundary after the firewall

The proof chain is now

```text
direct xi/Mellin contour and theta-mode analysis (Phase 21)
  + direct saddle-variable lemma
  + sectorial Stirling/Cauchy transport
      -> logarithmic moment derivatives through order six
  + local C1 parameter branch
  + direct finite-free/Jacobi/ODE estimates
      -> analytic certificate for multiplier intervals
  + Lean-checked finite sign transfer and conditional assembly
      -> d distinct negative target roots.
```

The last implication is kernel checked.  The analytic long arrows contain
conventional complex analysis and special-function mathematics and are not
Lean checked.  No Lean `axiom` is introduced for them: the conditional theorem
takes the completed certificate as a parameter, so the formal development
cannot accidentally promote an unproved analytic claim.

## What is and is not verified

The project has independently regenerated the exact rational algebra, the
saddle derivative tower, the shifted ODE recurrence, and multiple numerical
diagnostics.  Two adversarial Claude Fable review rounds found no P0/P1 defect
after repair.  These are AI technical audits, not human peer review.  The
manuscript and any circulation note must say exactly that.

The candidate theorem remains a conventional-paper claim while every direct
analytic adapter is audited end to end.  Phase 21 has removed the former
GORTTW complex input, but its replacement has only AI pre-review.  The absence
of human pre-review is recorded as a limitation rather than converted into a
false certification claim.
