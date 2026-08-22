# Phase-L reproducibility, source-fidelity, and package adversarial AI review

Date: 2026-08-17  
Candidate identifier stated by packet: `5641348d8ce0aadea5225f31dbb9bb1327778d20`  
Required checkpoint stated by packet: `5f79158f9c6276dd09142edeea279e35b0d58406`  
Packet SHA-256: `1f05e6dacef679807da7f47eaf994b23d9804e9aa65961664fb9d5454efd212c`

## 1. Overall verdict

**R2 — major, repairable release/reproducibility deficiencies; do not release this package as independently reproducible in its present form.** I found no P0 or P1 mathematical falsification in the checks that were actually executable. The corrected factor-eight identity, critical-point radius, exact rational interval arithmetic, Mathematica frozen-artifact hashes, manuscript rendering, and explicit local-versus-hosted Lean boundary survived the checks below. The R2 verdict is driven by multiple P2 failures in commit anchoring, entry-point completeness, mutation connectivity, source mapping, primary-source availability, environment pinning, licensing, and review separation.

The required pre-review command was run first and returned:

```text
PASS Phase-L AI reviewer bundle manifest (105 files)
```

That PASS establishes the 105 predicates programmed into `VERIFY_BUNDLE.py`; it does not authenticate the unmanifested manifest, reject extra files, establish a Git commit or checkpoint ancestry, or make the package self-reproducing.

## 2. Gate sheet

| Gate | Status | Evidence and falsification/recalculation method |
|---|---|---|
| R0 immutable commit, checkpoint ancestry, and manifest integrity | **FAIL** | The current 105 rows are unique, use safe relative paths, and hash correctly; the only unmanifested current file is `EVIDENCE_MANIFEST.sha256`. However, the packet contains no `.git` metadata or Git bundle, so the candidate commit, exact tree, and checkpoint ancestry are strings only. Synthetic tests show `VERIFY_BUNDLE.py` accepts an unmanifested file, duplicate rows, and a changed protected file after rewriting the unauthenticated manifest. No detached signature or externally pinned manifest/ZIP digest is supplied. |
| R1 pinned Lean/Mathlib/Python environments and clean-clone procedure | **FAIL** | Lean `v4.33.0-rc2` and Mathlib commit `51e6992...` are source-pinned, and the inventory records versions. Python requirements pin versions but not wheel/sdist hashes; Tectonic's bundle is not pinned; GitHub Actions use mutable `actions/checkout@v4`, `actions/setup-python@v5`, `leanprover/lean-action@v1.5.0`, and `ubuntu-latest`. Clean mode reuses external Python, Elan, and Tectonic installations. An attempted archive-local Lake invocation could not acquire Mathlib without network; no archive-contained cache/wheelhouse is supplied. |
| R2 deterministic verifier outputs and behavioral mutation coverage | **FAIL** | Repeated runs of the available bundle, exact interval, and Mathematica verifiers produced identical PASS text. The included `reproducibility_behavioral_mutations.py` rejects ten toy mutations, but it reads no candidate source. In a private copy it still passed after the manuscript's factor eight was changed to factor four. The source-connected `phase25_semantic_mutations.py` named by `VERIFY_ALL.sh` is absent, so its claimed coverage cannot be audited or run. |
| R3 Mathematica notebook, PDF, ledger, and checksum provenance | **PASS** | `verify_mathematica_evidence.py` passes. The notebook, 13-page PDF, result ledger, local checksum ledger, environment inventory, and packet manifest agree on all three SHA-256 values. Complete visual inspection found legible input cells; clipped long output lines are disclosed and full expressions remain in the notebook/ledger. The literal external-input operation scan found no listed operation. The claimed human act of executing the notebook remains self-attested rather than independently authenticated; this limitation is listed as unchecked. |
| R4 equation regression for factor eight and critical-point radius | **PASS** | Independent standard-library code derived `xi(1/2)` from the completed-zeta definition and the theta-kernel integral independently: the factor-eight relative error was `2.220e-15`, while factor four had error `0.5`. An explicit scaled polynomial made the displayed `y^k p^(k)/p` radius invariant (`sqrt(8)` at scales 1, 10, 1000), while the stale no-`y^k`, divided-by-`k!` expression scaled as `1, 0.1, 0.001`. The TeX and PDFs show the corrected displays. The archived Phase-24 regression itself is not runnable here because it targets a missing old unified-manuscript path and the supplied environment lacks `mpmath`; that packaging defect is charged to R9. |
| R5 exact interval and Arb/ACB source-versus-frozen-result checks | **UNCHECKED** | `verify_interval_certificates.py` and `branch_interval_certificates.py` both pass from exact `Fraction` constructions. The Arb/ACB source and frozen JSON are present and clearly distinguish continuum enclosures from finite-grid regression, but regeneration could not be run because the packet provides neither `python-flint`/`mpmath` nor an offline hash-pinned environment. Therefore the Arb/ACB source-versus-byte-frozen-result claim is not accepted or rejected. |
| R6 paper/source theorem cross-reference and primary-source fidelity | **FAIL** | The reader-facing Markdown cross-reference matches the current paper at a high level, but `THEOREM_ASSURANCE_MATRIX.json` retains old paper numbering for T2–T18 (for example T2 says Lemma 3.1 instead of 5.1, T5 says Theorem 4.1 instead of 7.1, and T16 says Lemma 11.1 instead of 16.1). T3 and T4 declare a `lean_kernel` channel while listing no Lean declarations. All eight binaries named in `SOURCE_HASHES.sha256` are absent; only an author-generated audit and hashes are included, so the exact MMP, MSS, Holland, GORTTW, and Szegő source statements could not be independently checked under the packet-only rule. |
| R7 archive exclusions, confidentiality, licensing, and secret/cache hygiene | **FAIL** | Confidentiality and the no-publication instruction are explicit. No credential-like secret, `.lake`, `.elan`, `.venv`, Python cache, build log, or `.DS_Store` survived the final packet scan. However, there is no LICENSE, COPYING, or NOTICE file for the distributed code/manuscript, so redistribution and reuse terms are uncheckable. The Mathematica notebook embeds `/Users/jsavva/Desktop/...`. More importantly for separation, 11 included evidence files disclose prior AI-review outcomes, severity results, and reviewer model names. No prior report was read, but this outcome exposure makes this a correlated re-review rather than an evidence-blinded independent pass. |
| R8 disclosed local-versus-hosted kernel-check boundary | **PASS** | The paper and Phase-K record clearly say the end-to-end Lean theorem is conditional on typed analytic inputs, distinguish finite/kernel-checked components from paper analysis, and disclose that local `full`/`clean` included `leanchecker` while the hosted Ubuntu run did not. The hosted run is stated to be at `99d2e753...`, not the candidate `5641348d...`; the relation between them is unchecked because Git history is absent. The boundary is disclosed rather than relabeled. |
| R9 commands and expected PASS markers are independently usable | **FAIL** | `reproduce/VERIFY_ALL.sh quick`, with explicit Python and Tectonic, stops immediately because `ground_zero_work/phase25/verify_phase25_metadata.py` is absent. Six of 12 referenced scripts are absent: Phase-20/21/25 top-level verifiers, `verify_phase25_metadata.py`, `phase25_semantic_mutations.py`, and `effectivity_ledger.py`. `verify_git_bundle.py` fails because the packet is not a Git repository. `manuscript_release_checks.py` looks under absent `evidence/paper/`, while sources are under top-level `manuscript/source/`. The main advertised quick/full/clean commands are therefore not independently usable from this archive. |

## 3. Numbered findings

1. **P2 — The advertised reproduction entry point is not self-contained.** `VERIFY_ALL.sh quick` fails at its first missing script. Six referenced verifier scripts are absent, the manuscript checker points to a directory not packaged, and the Git-bundle verifier has no Git repository to operate on. A reviewer cannot obtain the advertised PASS markers from the supplied archive even with Python and Tectonic explicitly provided.

2. **P2 — The packet does not establish an immutable candidate commit or checkpoint ancestry.** Commit and checkpoint strings agree across the metadata files, but no Git objects are supplied. The manifest has no external trust anchor and its verifier is fail-open with respect to extras and duplicate rows. Rewriting the manifest after changing a file still yields PASS. Supply a signed or externally published ZIP/manifest digest and a Git bundle containing the stated commit and checkpoint, and make the verifier reject non-allowlisted files, duplicates, absolute paths, and traversal.

3. **P2 — The included behavioral mutation gate is disconnected from production evidence.** It proves that ten locally constructed bad objects fail locally constructed invariants; it does not mutate or import the manuscript, Lean declarations, interval builder, or assurance matrix. A copied manuscript changed from factor eight to factor four did not affect the suite. The potentially source-connected semantic mutation driver is missing from the packet.

4. **P2 — The machine-readable theorem/source map is stale against the included manuscript.** T2–T18 use pre-expansion section/theorem numbering. Representative mismatches are T2 `Lemma 3.1` versus manuscript Lemma 5.1, T5 `Theorem 4.1` versus Theorem 7.1, T7 `Lemma 6.1` versus Lemma 9.1, and T16 `Lemma 11.1` versus Lemma 16.1. T3 and T4 additionally advertise a `lean_kernel` channel with empty declaration lists. This is material because the JSON is described as the machine-readable assurance source.

5. **P2 — Primary-source fidelity cannot be independently verified from the source-fidelity packet.** `SOURCE_HASHES.sha256` lists eight source artifacts, but none is present. The author-produced source audit is detailed and identifies exact theorem numbers, versions, and a journal/preprint limitation, but it cannot substitute for the primary text in an adversarial source-fidelity pass restricted to this archive. Include redistributable originals, licensed excerpts containing every consumed statement, or an offline retrieval bundle with independently anchored hashes and provenance.

6. **P2 — Environment pinning is version-level, not artifact-level, and current-candidate hosted coverage is not established.** Python distributions lack hashes, action references and `ubuntu-latest` are mutable, and the Tectonic bundle is not identified. The cited Ubuntu run is for `99d2e753...`; there is no evidence in the packet that candidate `5641348d...` is identical for all exercised surfaces or descends from it. Re-run on the exact candidate and archive logs, runner image identity, action SHAs, package hashes, and output hashes.

7. **P2 — The claimed separated review is not evidence-blinded.** Although no prior report is included or was read, the packet itself exposes earlier AI reviewers, passed gate ranges, severity outcomes such as “no P0/P1/P2,” and repaired-finding summaries in 11 evidence files. Under `REVIEW_PACKET.md`'s own rule, this must be called a **correlated re-review**, not an independent pass. Prepare a blinded evidence variant that removes outcome-bearing ledgers, or label the review class accordingly.

8. **P2 — Licensing is not auditable.** No license or notice accompanies the packaged Lean/Python/shell/manuscript materials. Confidentiality is not a license grant. Add an explicit repository/package license and third-party notices, or state precise review-only permissions and prohibit redistribution in machine-readable and human-readable terms.

9. **P3 — Byte-identical PDF reproduction needs an undocumented timestamp input.** Both TeX sources compiled cleanly with Tectonic 0.17.0, without warnings, to 35 and 10 pages. Default rebuilds differed only as generated binaries, but setting `SOURCE_DATE_EPOCH` to the frozen PDFs' embedded creation times produced exact hashes `6a2f...bbb3` and `a7df...9a57`. Record these epochs, preferably in a build script, instead of requiring reverse engineering from PDF metadata.

10. **P3 — The clean-room notebook leaks a workstation path.** The evaluated output contains `/Users/jsavva/Desktop/Jensen_Mathemtica_Cleanroom/...`. It is not a secret, but it is unnecessary personal-environment metadata and conflicts with package hygiene. Clear or normalize path-bearing outputs before freezing.

## 4. Independent-recalculation record

All independent scripts are in `reproducibility/scripts/`. None reads a frozen result JSON, checksum ledger, or prior review result as expected mathematical data.

| Script / action | Inputs constructed or inspected | Result | Reads frozen expected result as expected data? |
|---|---|---|---|
| `scripts/recalculate_equations.py` | Completed-zeta definition via Euler-transformed eta series; theta/omega definition; adaptive Simpson integral; exact formal coefficient comparison; explicitly defined scaled polynomial; current TeX only for presence/absence of displayed formulas | PASS, factor-eight relative error `2.220e-15`; factor-four error `0.5`; correct radius invariant; stale radius scale-dependent | **No** |
| `scripts/audit_packet_structure.py` | Current manifest as object under test; independently constructed temporary verifier mutations; metadata consistency; command references; source ledger names; hygiene/disclosure scans | Current hashes PASS; verifier fail-closed mutations survive; six command inputs missing; eight primary-source artifacts absent; prior-review outcomes exposed; Python hashes absent | **No** |
| `scripts/audit_theorem_crosswalk.py` | Manuscript section titles and claim subjects, compared to the machine JSON under test | 17 stale T2–T18 location entries; T3/T4 `lean_kernel` channel has no declarations | **No** |
| Exact interval replay | `verify_interval_certificates.py` constructs every expected rational from definitions and compares the JSON as the artifact under test | PASS twice | No frozen value is treated as expected; the JSON is the actual artifact |
| Branch rational replay | `branch_interval_certificates.py` constructs margins, inverse norm, ordering extrema, and thresholds from `Fraction` definitions | PASS | **No** |
| PDF rebuild | Current TeX/Bib sources; Tectonic 0.17.0; creation epochs inferred from the PDFs only for byte reproducibility | Clean 35/10-page builds; exact bytes when epoch is supplied; no compile warnings | No mathematical expected data |
| Mathematica integrity replay | Candidate hardcoded hashes/checksum ledger/notebook/ledger/PDF as artifacts under test | PASS twice; visual inspection complete | Not an independent mathematical recalculation; classified only as frozen provenance/integrity evidence |

Commands executed from the extracted packet included:

```text
python3 VERIFY_BUNDLE.py
python3 evidence/ground_zero_work/phase24/verify_interval_certificates.py
python3 evidence/ground_zero_work/phase24/verify_mathematica_evidence.py
python3 evidence/ground_zero_work/phase25/branch_interval_certificates.py
python3 evidence/ground_zero_work/phase25/reproducibility_behavioral_mutations.py
env C48_PYTHON=/usr/bin/python3 C48_TECTONIC=/opt/homebrew/bin/tectonic bash reproduce/VERIFY_ALL.sh quick
```

The first five commands passed. The last failed because `verify_phase25_metadata.py` is not in the archive. `verify_git_bundle.py`, `manuscript_release_checks.py`, and the archived equation regression were also deliberately attempted and failed respectively for absent Git metadata, absent `evidence/paper/`, and absent `mpmath` before reaching its missing old-manuscript path.

## 5. Unchecked claims

1. Existence of Git commit `5641348d...`, identity of its tree with this packet, ancestry from `5f79158f...`, and repository cleanliness.
2. The ancestry/diff relation between hosted-run commit `99d2e753...` and candidate `5641348d...`.
3. The claimed local `full` and `clean` PASS runs, 8,719-job Lean build, exhaustive local `leanchecker` replay, and standard-axiom output.
4. GitHub Actions run `32106804666`, its logs/artifacts, and the exact runner/action identities; no network or external records were consulted.
5. Arb/ACB regeneration and byte comparison with `ARB_ACB_RESULTS.json`.
6. Every exact theorem statement and convention in the eight absent MMP, MSS, Holland, GORTTW, and related primary-source artifacts, including the unavailable MMP journal PDF.
7. The human-act provenance claim that the author, rather than another process, entered and executed the Mathematica cells. The artifacts establish internal consistency, not operator identity.
8. Licensing and redistribution rights for the packaged code, manuscript, and any incorporated third-party material.
9. Cross-platform deterministic PDF bytes under a pinned Tectonic bundle; exact local reproduction was obtained only after supplying inferred epochs.
10. Mathematical correctness of the full analytic proof beyond the narrow reproducibility/source-fidelity checks and definition-derived equations performed here.

## 6. Release recommendation and exact blockers

**Recommendation: hold release.** The packet can be circulated internally as a confidential evidence snapshot only if it is labeled non-self-contained and correlated. Do not label it an independently reproducible release package.

Exact release blockers:

1. Supply a Git bundle or equivalent history containing the candidate and checkpoint, plus a signed or externally anchored ZIP/manifest digest and a fail-closed manifest verifier.
2. Make `quick`, `full`, and `clean` runnable from the delivered package, or change the package contract. Include the six missing verifier scripts, correct the manuscript layout assumptions, and provide an offline reproducible dependency path.
3. Regenerate `THEOREM_ASSURANCE_MATRIX.json` from the current 19-section manuscript and remove or qualify empty `lean_kernel` channels.
4. Provide auditable primary-source inputs or licensed exact excerpts for every imported theorem.
5. Hash-pin Python artifacts, GitHub actions, runner image, Tectonic bundle, and PDF `SOURCE_DATE_EPOCH`; rerun local/clean, Arb/ACB, and hosted checks on the exact candidate commit and archive raw logs/digests.
6. Produce an evidence-blinded Phase-L packet or explicitly relabel the result as correlated re-review.
7. Add licensing/NOTICE material and remove the workstation path.

## 7. Model, provider, tools, conflicts, and separation disclosure

- **Model/provider:** OpenAI Codex, GPT-5-based model; provider OpenAI. The exact serving subversion was not exposed to the reviewer.
- **Tools:** private `/private/tmp` extraction; Python 3.9.6 standard library; zsh/bash; `unzip`, `zipinfo`, `shasum`, `rg`, `find`, `git` 2.55.0; Tectonic 0.17.0; Poppler `pdfinfo`/`pdftoppm`; raster visual inspection through Codex's local image viewer; Lean/Lake version probe only. No web browsing, network source retrieval, external connector, prior report, repository file outside the extracted archive, or other Phase-L track was consulted. The final report and its new scripts are the only files written outside the private extraction directory.
- **Earlier freeze/report access:** none. I did not review an earlier freeze or any prior review report. However, prior-review outcomes and reviewer identities were embedded in the allowed packet evidence, so this is a **correlated re-review**, not a fully independent pass.
- **Conflicts:** no personal, financial, authorship, or institutional conflict is known. The sole methodological conflict is the outcome-bearing evidence contamination just described.
- **Candidate evidence:** no candidate evidence was intentionally edited. A failed Lake version probe briefly created an untracked `.lake` directory inside the disposable extraction; it was immediately removed, and `VERIFY_BUNDLE.py` was rerun successfully before continuing. All adversarial mutations were performed only in separate temporary copies.

## 8. Required classification sentence

This is AI review, not human or peer review.
