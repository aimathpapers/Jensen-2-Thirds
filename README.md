
# A Two-Thirds Hyperbolicity Wedge for Riemann's Xi-Function

This repository contains the paper, Lean 4 formalization, exact calculations,
and reproducibility record for John Savva's work on Jensen polynomials of
Riemann's xi-function.

The main theorem establishes an absolute constant `K > 0` such that

```text
n^2 log(n+2) >= K d^3
```

implies that the degree-`d` Jensen polynomial based at `n` has `d` distinct
negative real zeros.

This result does **not** prove the Riemann hypothesis and does not locate zeros
of the zeta function.

## Read the work

- [Main paper](PAPERS/JENSEN_TWO_THIRDS_MAIN.pdf)
- [Technical supplement](PAPERS/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf)
- [Reader's synopsis](PAPERS/JENSEN_TWO_THIRDS_READERS_SYNOPSIS.pdf)
- [Expository article](EXPOSITORY/JENSEN_TWO_THIRDS_MAGAZINE_ARTICLE.pdf)
- [Manuscript source](PAPER_SOURCE/)
- [Downloadable reviewer packet](REVIEWER_PACKET/Jensen_Two_Thirds_Reviewer_Packet_v1.0.zip)

## Inspect the evidence

- [Theorem/evidence cross-reference](EVIDENCE/CURRENT_STATUS/THEOREM_EVIDENCE_CROSS_REFERENCE.md)
- [Formal trust boundary](EVIDENCE/CURRENT_STATUS/TRUST_BOUNDARY.md)
- [Phase-32 formal endpoint](EVIDENCE/PHASE32_REFEREE_PACKET/FORMAL/THEOREM_MAP.md)
- [Concrete MMP specialization audit](EVIDENCE/CURRENT_STATUS/MMP_SPECIALIZATION_SOURCE_AUDIT.md)
- [Lean project](EVIDENCE/PHASE32_REFEREE_PACKET/FORMAL/lean-project/)
- [Mathematica and exact computations](EVIDENCE/PHASE32_REFEREE_PACKET/COMPUTATION/)
- [Supporting proof calculations](EVIDENCE/PHASE32_REFEREE_PACKET/SUPPORT/)
- [AI-only review record](EVIDENCE/PHASE32_REFEREE_PACKET/REVIEW/)
- [Reproduction instructions](EVIDENCE/PHASE32_REFEREE_PACKET/REPRODUCE/)
- [Curated-repository verification record](VERIFICATION_RECORD.md)

The concrete headline Lean theorem is conditional only on explicitly typed
Jacobi, MMP, and MSS literature inputs. Those general results are not
re-proved from first principles. The MMP input is attached to the two concrete
Jacobi factors, not to the final xi comparison polynomial; the exact
finite-free convolution identity transports its conclusion to the paper's
particular terminating `_3F_2`. The xi-specific multiplier, its six node
values, the interval certificate, the transformed Jensen identity, the finite
pre-cutoff absorption, and the headline negative-root implication are kernel
checked. Read the trust-boundary document before interpreting the scope of the
formalization.

## Verification

The curated Phase-32 evidence packet has a complete internal manifest. This
repository also has a manifest covering every committed file except the
manifest itself. From the repository root, run:

```bash
python3 VERIFY_REPOSITORY.py
python3 EVIDENCE/PHASE32_REFEREE_PACKET/VERIFY_BUNDLE.py
```

The verifier checks complete manifest coverage, unexpected hidden files,
credential signatures, unsafe ZIP members, required public artifacts, and the
absence of author-only launch and submission material.

## Review and attribution

AI systems assisted substantially with research, formalization, computation,
writing, and adversarial checking. All reviews included here are AI-only.
No human mathematical review or peer review is claimed.

See [PROVENANCE.md](PROVENANCE.md) for the status of historical labels and
frozen calculation records. No repository-wide license is asserted; the Lean
subproject retains its own included license and notice files.
