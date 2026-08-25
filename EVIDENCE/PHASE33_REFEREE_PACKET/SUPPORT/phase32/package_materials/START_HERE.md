# Jensen two-thirds Phase 32 reviewer packet

This packet contains the corrected paper, detailed supplement and appendices,
complete Lean project, exact Mathematica clean-room record, SymPy and Arb/ACB
calculations, formal assurance map, source-fidelity records, and the existing
AI-only review record for the Phase-32 candidate.

## Recommended order

1. Read `PAPER/JENSEN_TWO_THIRDS_MAIN.pdf`, especially Section 12 and
   Appendix G.2.
2. Read `FORMAL/evidence/MMP_SPECIALIZATION_SOURCE_AUDIT.md` for the exact
   two-Jacobi-factor specialization of the pinned MMP v3 propositions.
3. Use `FORMAL/THEOREM_MAP.md` to map claims T1--T18 to Lean declarations,
   computations, and external inputs.
4. Read `DISCLOSURE/TRUST_BOUNDARY.md` before interpreting “formalized.”
5. Run `bash REPRODUCE/VERIFY_ARCHIVE.sh packet` in the extracted packet.
6. Inspect `FORMAL/Phase32Axioms.lean` and
   `FORMAL/PHASE32_AXIOM_AUDIT.txt`.
7. Read the Mathematica ledger and checksums under
   `COMPUTATION/mathematica/`, then the independent SymPy and Arb/ACB paths.

## What Phase 32 changes

The formal MMP boundary no longer assumes that the final xi comparison
polynomial has the desired roots. It is attached to the two concrete Jacobi
factors. Lean proves their finite-free convolution is the paper's particular
terminating `_3F_2` and transports the factor-level MMP conclusion through
that identity. The paper displays the coefficient calculation, Jacobi
parameters, convention reversal, and exact MMP propositions. Lean also
checks the finite pre-cutoff absorption without assuming low-index
hyperbolicity.

The general classical Jacobi theorem, MMP v3 Propositions 2.7(iii) and 2.17,
and MSS Theorem 1.6 remain explicitly typed literature inputs. They are not
re-proved from first principles.

## Review status

All included reviews are AI-only. The Phase-30 adversarial review predates
the narrower Phase-32 interface and is retained as historical evidence, not
represented as an independent review of this repair. No human or peer review
is claimed.
