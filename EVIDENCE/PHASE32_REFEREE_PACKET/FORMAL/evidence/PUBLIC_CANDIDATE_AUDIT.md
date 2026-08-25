# Audit map for the T5 public candidate

## Compared declarations

| Public declaration | Informal source | Production theorem |
|---|---|---|
| `centered_xi_continuation_agrees_at_positive_integers` | Exact normalization seam used in manuscript Theorem 7.1 | `complexXiCoefficientMoment_nat_succ` |
| `sectorial_centered_xi_coefficient_asymptotic` | Manuscript Theorem 7.1 | `manuscriptTheoremSevenOne_effective` plus the exact definition bridges in `Solution.TheoremSevenOne` |
| `sectorial_centered_xi_error_derivatives_through_six` | Theorem 7.1 Cauchy consequence used in the sixth-order residual | `manuscriptPaperRelativeError_derivatives_through_six` |

The Challenge spells out the theta tail, Mellin moment, Gamma quotient,
dyadic factor, coefficient continuation, saddle equation, curvature, main
term, all three sectors, and the Cauchy radius. A reviewer therefore does not
need to trust names imported from the production library to understand what
is being compared.

## Trust boundary

- Trusted statement: `comparator/Challenge/TheoremSevenOne.lean`.
- Allowed trusted dependency: pinned Mathlib only.
- Untrusted proof: `comparator/Solution/TheoremSevenOne.lean` and its `Zeta23`
  import cone.
- Compared declarations: exactly the three names in
  `comparator/config-theorem-seven-one.json`.
- Permitted axioms: exactly `propext`, `Classical.choice`, `Quot.sound`.
- Independent kernel requested from Palomar: NanoDa enabled.

The Challenge contains three intentional `sorry` placeholders. The Solution and
production cone are required to be sorry-free. Comparator checks equality of
the exported theorem types; NanoDa provides an additional kernel replay.

## Local evidence

`VERIFY.sh` runs four fail-closed layers:

1. exact source-fidelity and disclosure checks;
2. seventeen mutations of decisive normalizations, signs, parameters, sectors,
   derivative order, quotient structure, NanoDa policy, and trusted imports;
3. ordinary Lean compilation and exact terminal `#print axioms`; and
4. `leanchecker --fresh` replay of the Solution cone.

The release archive is additionally built twice with fixed ordering,
timestamps, and permissions. Its verifier checks safe archive paths, complete
SHA-256 coverage, absence of caches/build artifacts, and byte fidelity to the
selected source revision.

## Honest limit

The local workstation does not provide the official Palomar Comparator,
Landrun, `lean4export`, and NanoDa service environment. Consequently this
package is submission-ready, but the official Comparator/NanoDa/sandbox gate
remains pending until the dedicated repository is public and submitted at a
full commit SHA. No human expert or peer review is claimed.
