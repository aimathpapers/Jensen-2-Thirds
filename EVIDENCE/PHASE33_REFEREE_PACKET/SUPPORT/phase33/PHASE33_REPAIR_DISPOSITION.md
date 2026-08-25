# Phase 33 disposition of the fresh Phase 32 AI review

Date: 2026-08-25

The review is technically strong. The P1 finding is correct and was reproduced
locally by compiling the reviewer's refutation theorem against the Phase 32
sources. The intended paper proof survives, but the formal headline theorem
could not be released while its literature-input bundle was inconsistent.

## Finding-by-finding disposition

| Finding | Disposition | Repair |
|---|---|---|
| F1, P1 | Confirmed | `MSSFiniteFreeIntervalInput` now requires factor positive-root and degree certificates plus `0 < uLower` and `0 < vLower`. The concrete call derives both strict inequalities from `B,D ≥ 256d` before invoking MSS. The former negative-endpoint attack is a required compile failure. |
| F2, P2 | Confirmed | The appendix prints the exact Lean name in one code span. The source gate is also relocatable between the monorepo and extracted packet layouts. |
| F3, P2 | Confirmed | Phase 32 labels these checks honestly as fail-closed source-contract mutations and adds an MSS lower-endpoint mutation. A separate Lean elaboration regression targets the vacuity mechanism. |
| F4, P3 | Confirmed | The bibliography now names Rafael Morales. |
| F5, P3 | Confirmed | `riemannXiJensen_twoThirds_global_headline` performs the all-`n` cutoff split in one declaration. |
| F6, P3 | Confirmed | A polynomial object, degree-`d` theorem, no-`d+1` theorem, and `HasExactlyDistinctNegativeRoots` adapter culminate in `riemannXiJensen_twoThirds_global_headline_exactly`. |
| F7, P3 | Confirmed as disclosure issue | The manuscript, appendix, and supplement now say explicitly that factor fields are domain side conditions on externally supplied literature conclusions. |
| F8, P3 | Partly environment-specific, substantively valid | The replacement release includes the original archive checksum beside the packet and a source-tree binding from packaged source files to a committed candidate tree. The outer sanitized release record binds the packet digest to the public repository tag/commit. |
| F9, P3 | Confirmed | The axiom parser now consumes complete multiline summaries and rejects a synthetic custom axiom placed on a continuation line. |

No human or peer review is claimed. A fresh AI-only adversarial re-review of
the Phase 33 release remains required before public release.

## Final publication-attribution audit

A final public-tree audit found that two explanatory sources still called
Jonathan Holland “James Holland,” even though the scholarly bibliography was
already correct. Both sources and the derived magazine PDF now use Jonathan
Holland. The Phase 33 source gate rejects regressions in the bibliography,
public explainer, and magazine-article source.
