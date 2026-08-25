# Jensen two-thirds Phase 30 reviewer packet

This packet contains the paper, detailed supplement and appendices, complete
Lean project, exact Mathematica clean-room record, SymPy and Arb/ACB
calculations, formal assurance map, source-fidelity records, and AI-only
adversarial review for the Phase-30 candidate.

## Recommended order

1. Read `PAPER/JENSEN_TWO_THIRDS_MAIN.pdf`.
2. Use `FORMAL/THEOREM_MAP.md` to map paper claims T1--T18 to exact Lean
   declarations and external inputs.
3. Read `DISCLOSURE/TRUST_BOUNDARY.md` before interpreting “formalized.”
4. Run `bash REPRODUCE/VERIFY_ARCHIVE.sh packet` in the referee packet. For the full
   repository gate, reassemble the full-audit archive and run
   `bash VERIFY_ARCHIVE.sh quick` or `full` with the pinned tools.
5. Inspect `FORMAL/Phase30Axioms.lean` and `FORMAL/PHASE30_AXIOM_AUDIT.txt`.
6. Read the Mathematica ledger and checksums under
   `COMPUTATION/mathematica/`, then the independent SymPy and Arb/ACB paths.
7. Read `REVIEW/PHASE30_AI_ONLY_ADVERSARIAL_REVIEW.md` last; it is correlated
   AI review, not human or peer review.

## Central formal endpoint

`Zeta23.Research.JensenWedge.riemannXiJensen_twoThirds_headline` constructs
the xi multiplier certificate and proves the negative-root conclusion under
the displayed cutoff/wedge conditions and a typed
`XiNaturalClassicalRootInputs` record. That record contains exactly the
Jacobi/MMP/MSS literature inputs. No project axiom asserts the xi asymptotic,
multiplier estimate, or headline conclusion.

## Review status

All currently available reviews are AI-only. No human or peer review is
claimed.
