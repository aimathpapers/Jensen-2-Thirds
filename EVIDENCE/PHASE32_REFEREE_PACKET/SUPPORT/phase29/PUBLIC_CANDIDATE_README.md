# Lean verification of Theorem 7.1 (T5)

This is a focused public-repository candidate for the literal analytic input
T5 in *A two-thirds hyperbolicity wedge for Jensen polynomials of Riemann's
xi-function*. It formalizes:

1. exact agreement of the continuation with the actual centered-xi Taylor
   coefficient at every positive integer;
2. the exact three-sector asymptotic for the analytically continued centered
   xi coefficients; and
3. the proportional-disc Cauchy estimates for the same relative error through
   derivative order six.

The trusted statement is
[`comparator/Challenge/TheoremSevenOne.lean`](comparator/Challenge/TheoremSevenOne.lean).
It imports only Mathlib, embeds all definitions needed to read the statement,
and contains the three deliberate `sorry` holes used by Comparator. The proved
counterpart is
[`comparator/Solution/TheoremSevenOne.lean`](comparator/Solution/TheoremSevenOne.lean).
Its production proof cone is under `Zeta23/Research/JensenWedge/`.

## Reproduce locally

Install `elan`, then run:

```bash
lake exe cache get
bash VERIFY.sh
```

`VERIFY.sh` checks the trusted surface and seventeen decisive semantic
mutations, builds both compared modules, checks the exact terminal axiom set,
and performs a fresh `leanchecker` replay. The expected axioms for each proved
declaration are exactly `propext`, `Classical.choice`, and `Quot.sound`.

For the strongest registry-side check, submit
`comparator/config-theorem-seven-one.json` to Palomar. The configuration
requires NanoDa. A local pass is not represented as an official Palomar
Comparator/NanoDa verdict.

## Scope and disclosure

This candidate closes Theorem 7.1/T5, not the final Jensen-polynomial theorem
in isolation. The final result also uses the T1--T4 algebraic and asymptotic
chain formalized in the larger source repository.

AI systems contributed substantially to the Lean code, verification harness,
and prose. The human maintainer directed the work and independently ran a
clean-room Mathematica recalculation. Multiple AI reviews were performed, but
no human expert or peer review has occurred and none is claimed. Palomar is an
independent formal-verification service, not peer review and not a novelty
assessment.

See `comparator/THEOREM_SEVEN_ONE_README.md`,
`comparator/formalization-theorem-seven-one.yaml`, and
`AI_ONLY_RELEASE_AUDIT.md` for the exact statement map, fidelity notes, and
remaining external gate.

## Integrity and license

`SOURCE_COMMIT.txt` records the source revision used to assemble the candidate.
`SHA256SUMS` covers every other packaged file. The code is released under the
Apache License 2.0; see `LICENSE` and `NOTICE`.
