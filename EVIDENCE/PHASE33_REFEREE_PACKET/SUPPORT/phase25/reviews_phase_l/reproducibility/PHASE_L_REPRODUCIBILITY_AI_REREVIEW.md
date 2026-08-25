# Phase L reproducibility/source-fidelity correlated AI re-review

Date: 2026-08-18  
Artifact reviewed: `Jensen_Two_Thirds_Phase25_Repaired_Reproducibility_AI_Rereview_Packet.zip`  
Candidate commit: `6ee1db8fc5789a01bc0297f850c817f55b529be4`  
Required checkpoint: `5f79158f9c6276dd09142edeea279e35b0d58406`  
Classification: targeted correlated AI re-review; not independent or separated

## Overall verdict and release status

**R1 — qualified release recommendation for the Phase-L reproducibility
track.** The repairs close the earlier archive-integrity, source-connection,
history, theorem-map, Lean-source, primary-source, deterministic-PDF,
classification, and review-permission defects. **No release-blocking P0 or P1
remains.**

This is not R0 because a committed legacy acceptance command still fails
(Finding 1, P2), and the dependency-heavy Lean/Arb/ACB/Mathematica replays were
not independently rerun in this archive-only pass. The P2 is not evidence of a
theorem error and is outside the current `VERIFY_ALL` serial path, but it should
be updated or explicitly retired before describing every shipped phase
verifier as passing.

The packet itself is review-only and does not authorize public distribution.
“Release” here means acceptance of this candidate on this review track, not
permission to publish the packet.

## Gate sheet

| Gate | Result | Adversarial evidence and method |
|---|---|---|
| R0 immutable commit, checkpoint ancestry, manifest integrity | **PASS** | `VERIFY_BUNDLE.py` passed on 452 manifested files; `VERIFY_HISTORY.py` resolved exactly the declared candidate and proved checkpoint ancestry. The ZIP had 453 unique file members under one root and no traversal, duplicate, or symlink member. Nine generated manifest mutations (extra, duplicate, traversal, manifest-self, hash, missing, symlink, malformed, and empty) all failed closed. Independently, 436 `evidence/` files, six top-level manuscript source files, and two PDFs—444 files total—byte-matched the corresponding candidate Git objects. |
| R1 pinned environments and clean-clone procedure | **PASS** | The Lean toolchain is `leanprover/lean4:v4.33.0-rc2`; Mathlib is pinned to `51e6992efd06126df61a496bebf8f49482a4e129` in both `lakefile.toml` and `lake-manifest.json`; Python versions in the lock and inventory agree; local Git 2.55.0 and Tectonic 0.17.0 agree with the inventory. The reconstructed commit contains a clean-clone path that rejects inherited `.lake`, `.venv`, and `AGENTS.md`. The full clean replay itself is listed as unchecked. Mutable `ubuntu-latest` and GitHub Action major-version tags are disclosed CI portability inputs, not the pinned mathematical toolchain. |
| R2 deterministic verifier output and behavioral mutations | **PASS** | Two fresh fixed-epoch PDF builds were mutually byte-identical and matched both candidate and packet PDFs. `verify_git_bundle.py` made two byte-identical bundles and reconstructed the exact head. All 14 definition-level behavioral mutations and all six production-manuscript semantic mutations were rejected for their intended reasons. The separate structural audit generated its own mutation inputs. |
| R3 Mathematica notebook/PDF/ledger/checksum provenance | **PASS** | `verify_mathematica_evidence.py` passed all three artifact hashes, exact ledger sentinels, and the no-external-input-operation scan. The record identifies Mathematica 15.0.1, user execution, AI-supplied cells, and the non-human-review boundary. The single absolute workstation path is an inert saved output value, not an input or executable dependency. Mathematica itself was not rerun. |
| R4 factor-eight and critical-radius equation regression | **PASS** | The independent script equated the two formal-series coefficient definitions to derive `8 n!/(2n)!` exactly for `n=0..20`, then distinguished factor-four and stale-`2^(2n)` mutations. A constructed critical-point polynomial distinguishes the required `y^k p^(k)/p` normalization from the stale `p^(k)/(k!p)` normalization. The production source contains the derived forms and excludes the stale forms. No frozen result was read as expected data. |
| R5 exact interval and Arb/ACB source-versus-result checks | **UNCHECKED** | The exact Phase-24 interval certificate, exact Phase-25 branch intervals, and effectivity DAG passed from definitions. The packaged Arb/ACB implementation and JSON are source-connected to the candidate, but the directed-enclosure recomputation was not run because the packet intentionally contains no Python/Flint runtime. Frozen JSON was not relabeled as a fresh computation. |
| R6 theorem cross-reference and primary-source fidelity | **PASS** | The manuscript labels resolve to the claimed Sections 1 and 4–17; T1–T18 are ordered and mapped; all 66 named Lean declarations exist; the axiom driver and frozen output cover exactly those 66 declarations with only `propext`, `Classical.choice`, and `Quot.sound`. All eight source-ledger hashes independently matched official downloads. MMP v3 Proposition 2.7(iii), Proposition 2.11, Definition 2.16, and Proposition 2.17 agree with the packet’s consumed statements and log-mesh orientation; the MSS publisher record identifies the required root statement as Theorem 1.6. |
| R7 exclusions, confidentiality, licensing, secrets/caches | **PASS** | The review-only notice authorizes inspection/private copies, forbids public distribution, and distinguishes third-party rights. The packet contains source identifiers/hashes rather than redistributed third-party publications. No `.lake`, `.venv`, cache directory, secret/key file, private-key marker, access-token pattern, ZIP symlink, or traversal member was found. |
| R8 local-versus-hosted kernel boundary | **PASS** | The packet explicitly separates the local full build/`leanchecker` record from the hosted Ubuntu build plus axiom audit, and discloses the canceled hosted `leanchecker` attempt. The cited hosted run is at `99d2e753...`; the later candidate changes do not alter `Zeta23` Lean sources. The hosted run URL itself was not independently queried in this restricted pass. |
| R9 independently usable commands and PASS markers | **FAIL** | The two archive-local commands pass, the offline history reconstructs the candidate, the current repository-level deterministic PDF command passes, and current Phase-25 source/mutation gates exercised here pass. However, `ground_zero_work/phase24/verify_phase24.sh` still invokes a stale release assertion and fails before its expected PASS marker (Finding 1). |

## Findings

### 1. P2 — the shipped Phase-24 verifier still fails on an obsolete Hermite–Genocchi limitation

From a private checkout reconstructed solely from `CANDIDATE_HISTORY.bundle`,
the command

```text
C48_PYTHON=python3 bash ground_zero_work/phase24/verify_phase24.sh
```

produced:

```text
PASS phase24 exact interval certificates
PASS Mathematica M1--M4 evidence: exact hashes, exact ledger, no external-input operations
FAIL: missing Hermite--Genocchi Lean limitation: 'full six-simplex identity remains a named'
```

`verify_phase24.sh` invokes `release_checks.py` unconditionally. That checker
still requires the quoted earlier limitation, while the later candidate now
maps a local Newton/Hermite–Genocchi producer surface into T15. The current
`reproduce/VERIFY_ALL.sh` deliberately runs Phases 25, 21, and 20—not Phase
24—so this does not invalidate the documented current serial acceptance path.
It nevertheless leaves a named, committed phase verifier with a false expected
PASS contract. Update the Phase-24 assertion to the current truthful boundary,
or mark that verifier superseded and remove it from the supported-command
surface. This is a reproducibility regression, not a theorem-affecting defect.

### 2. P3 — repository-only versus archive-local build instructions remain slightly indirect

`START_HERE.md` now correctly limits the archive-local contract to the packet
verifiers and says that full replay uses the exact private-repository commit.
The history bundle makes that commit reconstructible. However,
`evidence/reproduce/README.md` and the included
`evidence/reproduce/BUILD_MANUSCRIPTS.sh` do not give the one-line bundle
checkout command; the build script’s `$ROOT/paper` path is valid only after
repository reconstruction, not when invoked directly under `evidence/`.
Adding the exact offline checkout invocation would remove the last ambiguity.

### 3. P3 — one absolute workstation path remains in the canonical Mathematica notebook

The only `/Users/...` occurrence in the complete evidence tree is the saved
`LedgerPath` output in
`ground_zero_work/phase24/mathematica_verification/C48_Mathematica_CleanRoom_2.nb`.
Its containing notebook and ledger pass the declared hashes, and no verifier
uses that path. It is therefore inert provenance, not a portability failure or
secret. Rewriting it would destroy the frozen notebook hash; a companion note
is preferable if privacy hygiene requires explicit disposition.

There are **no P0 findings and no P1 findings** in this re-review.

## Primary-source recheck

The packet’s source audit specifically invites official retrieval and hash
comparison, so this was the only external-source exception used. The following
official records/artifacts were consulted:

- MMP [arXiv v3 record](https://arxiv.org/abs/2309.10970v3), [v3 HTML](https://arxiv.org/html/2309.10970v3), [v3 PDF](https://arxiv.org/pdf/2309.10970v3), and [v3 source](https://arxiv.org/e-print/2309.10970v3). The record confirms that v3 corrected Proposition 2.11. The HTML/PDF confirms Proposition 2.7(iii), the full-degree one-input statement of Proposition 2.11, the decreasing-root definition `lmesh=min lambda_i/lambda_(i+1)`, and Proposition 2.17’s nondecrease direction.
- MSS [open publisher record](https://link.springer.com/article/10.1007/s00440-021-01105-w), [publisher PDF](https://link.springer.com/content/pdf/10.1007/s00440-021-01105-w.pdf), [arXiv v2 PDF](https://arxiv.org/pdf/1504.00350v2), and [arXiv v2 source](https://arxiv.org/e-print/1504.00350v2). The publisher record places nonnegative-real-root preservation and its extreme-root inequality at Theorem 1.6 and distinguishes the stronger Theorem 1.13.
- Holland [arXiv v1](https://arxiv.org/abs/2608.08682v1) and its [PDF](https://arxiv.org/pdf/2608.08682v1); the official record showed only v1 at review time.
- GORTTW [arXiv v3](https://arxiv.org/abs/1910.01227v3) and its [PDF](https://arxiv.org/pdf/1910.01227v3).

Every row in `SOURCE_HASHES.sha256` matched. In particular, the apparently
versioned filename `Real_roots_finite_free_convolution_v2.tex` is the internal
filename obtained by decompressing the **v3** arXiv source payload; its hash
`eb42ce1...` matched. The other matched prefixes were `23f228e...`,
`696fbd8...`, `8560452...`, `4dee6f4...`, `67e526d...`, `3fc31ba...`, and
`f203487...`.

The MMP journal PDF remains unexamined because the exact consumed statements
are pinned to and verified against accessible arXiv v3. This is the same
limitation disclosed in the packet and does not undermine the cited statement
fidelity.

## Independent-recalculation record

Reviewer-created scripts are in `rereview_scripts/`:

1. `audit_packet_structure.py`
   - Checks ZIP safety; reruns both mandatory verifiers; creates nine fresh
     hostile manifest fixtures; reconstructs the Git object store; connects all
     packaged evidence/manuscript files to the candidate; closes internal Lean
     imports; checks proof escapes, T1–T18 section labels, all 66 declaration
     names, exact axiom coverage, environment pins, disclosures, and the
     workstation-path surface.
   - It reads candidate metadata and Git objects as claims under test. It does
     **not** read any frozen mathematical result as expected data.
2. `definition_recalculations.py`
   - Constructs the coefficient calculation from the centered-xi and cosh
     definitions using exact rational arithmetic and constructs a fresh
     critical-point polynomial to distinguish the radius normalization.
   - It reads no frozen expected result.
3. `verify_pdf_rebuild.sh`
   - Reconstructs the candidate from the offline bundle, makes two fresh builds
     with Tectonic 0.17.0 and `SOURCE_DATE_EPOCH=1786968000`, and compares the
     resulting byte streams and UTC creation time.
   - It uses candidate/packet PDFs only as artifacts being compared, not as
     mathematical expected data.

Observed independent outputs included:

```text
PASS ZIP container safety: 453 unique files, one root, no traversal or symlink members
PASS manifest fail-closed suite: 9 generated mutations rejected
PASS source-to-history connection: 444 packaged files byte-match candidate 6ee1db8...
PASS Lean source closure: 361 sources, 866 internal imports, no proof escapes
PASS theorem/axiom mapping: 18 claims, 66 declarations, exact accepted-axiom coverage
PASS two fresh PDF builds are mutually identical and match candidate/packet PDFs; fixed creation timestamp confirmed
PASS definition-level equation recalculations (no frozen expected result read)
```

The two rebuilt PDFs had the candidate hashes
`c6bfb6c31ce9f6a74e857a599ffca62e64a393574cbd1ac09a8b2073244d7813`
(main, 36 pages) and
`d9f167b3333950da301ba0bcecdd696ba3ca4fc3e62279abc2327d02a2cd3448`
(supplement, 10 pages). With `TZ=UTC`, both report creation time
`Mon Aug 17 12:00:00 2026 UTC`. Visual inspection of main-paper pages 1, 12,
24, and 36 and supplement pages 1, 5, and 10 found no clipping, overlap, or
missing-glyph defect.

Candidate-provided gates additionally run in the reconstructed checkout were:
the 14 behavioral mutations; six production-source semantic mutations; exact
Phase-24 and branch intervals; effectivity ledger; manuscript source/PDF
checks; Mathematica provenance; axiom-output validation; and deterministic Git
bundle reconstruction. These are useful checks of their programmed predicates,
not independent mathematical rederivations.

## Unchecked claims

1. `reproduce/VERIFY_ALL.sh full` and `clean`, the 8,719-job Lean build, and
   exhaustive local `leanchecker` replay were not rerun. The archive does not
   contain the Mathlib cache, Elan installation, or pinned Python environment.
2. The Arb/ACB directed-enclosure JSON and dependency-heavy Phase-25 semantic
   suite were not recomputed because `python-flint`, SymPy, and mpmath were not
   supplied as archive-local runtimes. Their sources and frozen outputs are
   commit-connected; that is not a fresh numerical verification.
3. Mathematica M1–M4 was not rerun in Mathematica. Only notebook/ledger/PDF
   provenance, exact sentinels, external-input exclusion, and hashes were
   checked.
4. The GitHub Actions run `32106804666` was not queried. The packet’s workflow,
   commit statement, and local-versus-hosted limitation were inspected.
5. The paywalled MMP journal PDF was not byte-compared to arXiv v3. No exact
   consumed statement depends solely on that inaccessible PDF.
6. This track did not attempt a fresh proof of the full two-thirds theorem; it
   audited reproducibility, package integrity, source mapping, and source
   fidelity.

## Earlier-finding disposition

| Rechecked item | Disposition |
|---|---|
| Archive-local contract | **Closed for the declared contract.** Both archive-local verifiers pass; full replay is explicitly repository-only and the offline bundle reconstructs the exact repository. Finding 2 is clarity-only. |
| Manifest fail-closed behavior | **Closed.** Exact coverage plus duplicate, unsafe path, symlink, missing, extra, malformed, empty, and hash mutations were tested. |
| Immutable commit/checkpoint ancestry | **Closed.** Exact bundle head, complete history, and ancestry passed; every packaged candidate-derived file was independently connected to that head. |
| Source-connected mutations | **Closed.** Production manuscript semantic mutations and behavioral mutations run against live candidate definitions/source. |
| Theorem mapping | **Closed.** T1–T18 resolve to actual numbered labels; channel/declaration coherence and all 66 declarations were checked. |
| Complete Lean/axiom source closure | **Closed.** All 866 internal imports resolve within 361 packaged Lean sources; the 66-declaration axiom surface is exact. |
| Primary-source audit limitation | **Closed for the consumed open-source statements.** Official records, statements, and all eight hashes were independently checked. The journal-PDF limitation remains expressly disclosed. |
| Environment/PDF timestamp | **Closed for the reported repair.** Core versions agree and two fixed-epoch builds reproduce exact bytes/timestamps. Full clean replay remains unchecked. |
| Correlated labeling | **Closed.** `START_HERE.md`, `REVIEW_PACKET.md`, and metadata consistently call this a targeted correlated AI re-review. |
| Review-only notice | **Closed.** Permission, confidentiality, public-distribution prohibition, and third-party-rights boundary are explicit. |
| Workstation path | **Accepted residual.** One inert path remains solely in the frozen Mathematica output; it is not used by any command or verifier. |

## Model, tools, access, conflicts, and separation disclosure

- Provider/model: OpenAI Codex, GPT-5 family. The exact serving snapshot was
  not exposed to the reviewer.
- Tools: Python 3.9.6 standard library, Git 2.55.0, Tectonic 0.17.0, shell,
  `rg`, `unzip`, `shasum`, Poppler `pdfinfo`/`pdftoppm`, visual PDF inspection,
  and narrowly scoped official-source retrieval/web inspection.
- Context and access: only the named repaired ZIP, its private extraction, and
  a private Git checkout reconstructed from its included history bundle were
  used as candidate evidence. The official URLs named above were consulted
  solely because the packet’s source audit requested official retrieval/hash
  comparison. Candidate evidence was not edited.
- Correlation/conflict: I reviewed the earlier freeze, so this is necessarily a
  correlated re-review and is not independent or separated. I did not consult
  prior report contents, another track’s report, or the author disposition.
  The history bundle necessarily contains committed history; a name-only Git
  comparison exposed filenames of historical review artifacts, but their
  contents were not opened or used. No additional substantive conflict of
  interest is known.

**Release recommendation:** accept the repaired packet on the reproducibility
track with R1 status; repair or explicitly retire the stale Phase-24 verifier
to reach R0. There is no exact P0/P1 blocker.

This is AI review, not human or peer review.
