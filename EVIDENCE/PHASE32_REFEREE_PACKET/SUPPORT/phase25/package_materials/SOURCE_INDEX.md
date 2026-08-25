# Source and evidence index

## Read first

- `PAPER/JENSEN_TWO_THIRDS_MAIN.pdf`: primary 37-page manuscript.
- `PAPER/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf`: computational and formal
  supplement.
- `DISCLOSURE/TRUST_BOUNDARY.md`: exact division among paper, Lean,
  computation, and imported mathematics.
- `DISCLOSURE/KNOWN_LIMITATIONS.md`: nonclaims and remaining boundaries.

## Formal proof

- `FORMAL/lean-project/`: complete pinned Lean project, excluding build caches.
- `FORMAL/THEOREM_MAP.md`: T1--T18 paper/evidence map.
- `FORMAL/AXIOM_AUDIT.txt`: frozen 66-declaration axiom output.
- `FORMAL/Phase25Axioms.lean`: reproducible audit driver.

## Independent computation

- `COMPUTATION/mathematica/`: evaluated notebook, PDF, exact ledger,
  verification record, and hashes.
- `COMPUTATION/sympy/`: exact symbolic scripts and frozen calculation records.
- `COMPUTATION/arb_acb/`: rigorous ball-arithmetic method, source, and result.
- `COMPUTATION/interval_certificates/`: exact rational boxes and verifiers.
- `COMPUTATION/effectivity/`: exact dependency DAG and sufficient-constant
  ledger.

## Supporting proof records

- `SUPPORT/phase21/`: direct sectorial saddle, contour, higher modes, and xi
  coefficient assembly.
- `SUPPORT/phase20/`: Holland dependency firewall and re-proved multiplier
  interfaces.
- `SUPPORT/assurance/`: theorem matrix, dependency graph, normalization
  crosswalk, and current status.
- `SUPPORT/primary_sources/`: versions, hashes, consumed statements, and
  official retrieval locations.

## Reproduction

- `VERIFY_BUNDLE.py`: fail-closed per-file manifest verifier.
- `VERIFY_ANCESTRY.py`: verifies a cryptographic commit-parent proof from the
  candidate to the required checkpoint.
- `REPRODUCE/VERIFY_ARCHIVE.sh`: extraction-local package and manuscript
  replay. The audit archive also supports repository `quick` and `full` modes
  through its offline Git bundle.
- `REPRODUCE/EXPECTED_RESULTS.md`: commands, prerequisites, and PASS markers.

The full audit archive adds the complete relevant repository snapshot, every
supporting phase note, calculation source/output, mutation, AI report and
disposition, environment record, and offline candidate history.
