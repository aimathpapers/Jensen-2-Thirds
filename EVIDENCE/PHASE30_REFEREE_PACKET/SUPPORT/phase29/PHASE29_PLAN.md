# Phase 29 plan — Palomar packaging for the fully closed T5 theorem

## Objective and stopping rule

Close the literal manuscript Theorem 7.1 (T5), including every relative-error
derivative used through order six, behind a Palomar-compatible Challenge and
Solution pair. Freeze only when the ordinary Lean kernel replay, source and
axiom audits, semantic mutations, downstream phase verifiers, and a fresh
correlated AI-only adversarial review all pass. Do not describe any of this as
human or peer review. The official Comparator/NanoDa/sandbox verdict is a
submission-side gate and cannot be claimed from the local environment.

## 1. Freeze the exact statement surface

- State the theta Mellin kernel with the factor `(evenKernel - 1)/2` and the
  quarter exponent `exp(u/4)`.
- State the exact complex coefficient continuation, including the Gamma
  quotient, dyadic sign, `2M-2` shift, and two Mellin moments.
- Define centered Riemann xi directly from Mathlib's completed zeta and compare
  the continuation with its even Taylor coefficient at every positive integer.
- State the saddle equation, curvature, elementary main, and saddle main.
- Fix the proof/outer/inner angles at `1/100`, `1/200`, and `1/400`, and the
  proportional Cauchy radius at `x/1000`.
- Keep the challenge below Palomar's preferred 300-line/32-KiB surface.
- Import only Mathlib in the Challenge. Embed every trusted definition there;
  do not put any candidate-local import in its transitive closure.

Acceptance: the trusted-surface checker finds every exact formula and rejects
any `Zeta23` or `ChallengeDeps` import.

## 2. Prove the literal three-sector coefficient theorem

- Bridge the public theta moment to the production Mathlib Mellin object by
  definitional equality.
- Bridge the exact coefficient, saddle equation, curvature, sectors, main,
  and relative error one definition at a time.
- Instantiate the production effective theorem with the explicit radius and
  constants.
- Export holomorphy/differentiability, main-term nonvanishing, the quotient
  identity, exact factorization, and `O(log |M|/|M|)` rate.

Acceptance: `lake build Solution.TheoremSevenOne` succeeds without `sorry`,
`admit`, custom axioms, unsafe code, or proof-escape tokens.

## 3. Prove the complete derivative consequence

- Use the same error function as the coefficient theorem, not a new adapter.
- Transport the proportional-disc Cauchy bound through every `j <= 6`.
- Keep the public formula literal: factorial, `D log(3x)/x`, and radius power.
- Verify that the quotient identity holds throughout the open outer sector,
  so derivatives at positive real `x` are derivatives of the exact quotient.

Acceptance: the second compared declaration builds and its axiom output is
exactly `propext`, `Classical.choice`, and `Quot.sound`.

## 4. Harden statement fidelity and trust separation

- Repeat the marked Mathlib-only definition block byte-for-byte in Challenge
  and Solution; fail if the blocks differ.
- Configure Comparator for exactly the two theorem names and require NanoDa.
- Add formalization metadata that identifies scope, literature relationships,
  fixed-angle clarifications, AI assistance, and the absence of human review.
- Check Challenge size, imports, exact formula fragments, theorem shapes,
  permitted axioms, metadata policy, and proof-escape tokens.
- Run at least seventeen semantic mutations covering normalizations, signs,
  shifts, angles, the quotient, derivative ceiling, NanoDa, and trust imports;
  require every mutation to be rejected.

Acceptance: all source-fidelity, mutation, and axiom-policy gates pass.

## 5. Replay the formal and downstream evidence serially

- Build Challenge and Solution with the pinned toolchain.
- Run `#print axioms` and parse it fail-closed.
- Run `leanchecker --fresh` on the Solution import cone.
- Replay Phases 26, 27, and 28, followed by the established serial Phase-21
  and Phase-20 verifiers. Never run concurrent Lean builds or `lake update`.

Acceptance: every named verifier prints PASS and no tracked build artifact or
dependency lock changes.

## 6. Assemble and audit the public-repository candidate

- Copy the pinned Lean project, full `Zeta23` production source, the two T5
  Comparator modules, print-axiom driver, config, metadata, license, and a
  focused README into a clean directory; exclude `.lake`, caches, temporary
  files, unrelated reviewer materials, and confidential prose.
- Add a one-command verifier and SHA-256 manifest.
- Build the archive deterministically twice and require byte-identical hashes.
- Inspect the archive from a fresh extraction, rerun source/manifest checks,
  and record exactly what was and was not independently replayed.
- Perform a fresh correlated AI-only hostile audit against the manuscript
  theorem and Palomar requirements, repair any P0/P1/P2 finding, and rerun all
  affected checks.
- Push the private source branch. Do not publish the dedicated public
  repository or submit to Palomar until the maintainer explicitly authorizes
  that public external action.

Acceptance: a clean deterministic candidate exists with a recorded digest,
the correlated AI-only audit has no unresolved P0/P1/P2, and the remaining
external step is precisely public-repository creation plus Palomar's official
Comparator/NanoDa/editorial run.

The local environment does not contain Comparator, `lean4export`, Landrun, or
NanoDa. Therefore Phase 29 can make the package submission-ready and run
Lean's independent fresh replay locally, but only Palomar's Linux workflow can
complete the official Comparator/NanoDa/sandbox gate.
