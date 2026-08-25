# Expected verification results

Run commands from the extracted package root.

## No-dependency integrity checks

```bash
python3 VERIFY_BUNDLE.py
python3 VERIFY_ANCESTRY.py
```

Expected markers:

```text
PASS package manifest (... files)
PASS candidate/checkpoint cryptographic ancestry proof (... commits)
```

Both checks use only Python's standard library.

## Extraction-local manuscript replay

With Tectonic 0.17.0 available:

```bash
bash REPRODUCE/VERIFY_ARCHIVE.sh packet
```

Expected final marker:

```text
PASS extraction-local packet, ancestry, and manuscript replay
```

The command compiles from `PAPER/source/` into a private temporary directory
and byte-compares both PDFs with the frozen package copies.

## Audit-archive repository replay

The full audit archive additionally contains
`AUDIT/CANDIDATE_HISTORY.bundle`. Supply the pinned Python environment and use:

```bash
C48_PYTHON=/absolute/path/to/python \
  bash REPRODUCE/VERIFY_ARCHIVE.sh quick
```

Expected final marker:

```text
PASS extraction-local audit repository quick replay
```

For the full serial Lean/kernel/analytic replay:

```bash
C48_PYTHON=/absolute/path/to/python \
C48_ELAN_HOME=/absolute/path/to/elan-home \
  bash REPRODUCE/VERIFY_ARCHIVE.sh full
```

Full mode first runs `lake exe cache get` in the reconstructed pinned Lean
project. It therefore needs network access to the Mathlib release cache unless
the required artifacts are already available through the configured Elan/Lake
environment. Quick mode does not initialize Lake packages and remains offline.

Expected repository markers include:

```text
PASS Phase 25 formal, exact, interval, effectivity, manuscript, reproducibility, and semantic gates
PASS Phase 21 complete direct-sector proof-surface checks
Phase 20 verification PASS
PASS VERIFY_ALL full
PASS extraction-local audit repository full replay
```

Warnings from Lean linters are not failures. No verification marker is a
claim of human or peer review.
