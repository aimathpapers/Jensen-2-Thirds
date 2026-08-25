# Jensen two-thirds Phase 33 reviewer packet

This is the repaired successor to the Phase 32 packet. It contains the main
paper, technical supplement, unified manuscript, full Lean project,
Mathematica clean-room notebook and ledger, exact and interval calculations,
the fresh Phase 32 AI-only review, and the Phase 33 author disposition.

## Recommended reading order

1. Read `PAPER/JENSEN_TWO_THIRDS_MAIN.pdf`, especially Sections 12, 18, and
   Appendix G.2.
2. Read `REVIEW/PHASE32_FRESH_AI_REVIEW_FINDINGS.md`, followed by
   `REVIEW/PHASE33_REPAIR_DISPOSITION.md`.
3. Use `FORMAL/THEOREM_MAP.md` to map claims T1--T18 to Lean declarations,
   calculations, and typed external inputs.
4. Inspect `FORMAL/Phase33Axioms.lean` and
   `FORMAL/PHASE33_AXIOM_AUDIT.txt`.
5. Read `FORMAL/evidence/MMP_SPECIALIZATION_SOURCE_AUDIT.md` for the concrete
   Jacobi-to-MMP adapter and the explicit literature boundary.
6. Run `bash REPRODUCE/VERIFY_ARCHIVE.sh packet` from the extracted packet.
7. Inspect `SOURCE_TREE_BINDING.json`; `VERIFY_SOURCE_BINDING.py` checks the
   packet payloads against it, and the full audit archive additionally checks
   the binding against the included Git history bundle.

## What Phase 33 repairs

The typed MSS product theorem now requires positive-root and degree
certificates for both factors and strict positivity of both interval lower
endpoints. Lean derives the concrete positive endpoints from `B,D >= 256d`.
The former negative-endpoint instantiation is retained as a required
elaboration failure. The terminal theorem now also proves exact degree,
exactly `d` distinct negative roots, and the all-index cutoff split in one
declaration.

The classical Jacobi theorem, MMP v3 Propositions 2.7(iii) and 2.17, and MSS
Theorem 1.6 remain explicitly typed literature inputs. They are not re-proved
from first principles.

## Review status

The included independent review was performed by an AI system. The Phase 33
repairs have passed local Lean, mutation, source, and reproducibility gates,
but have not yet received a fresh independent re-review. No human or peer
review is claimed.

