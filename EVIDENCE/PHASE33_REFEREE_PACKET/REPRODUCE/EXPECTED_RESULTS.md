# Expected Phase 33 verification results

From the repository root, run serially:

```bash
C48_PYTHON="$PWD/.venv/bin/python" \
  bash ground_zero_work/phase33/verify_phase33.sh
C48_PYTHON="$PWD/.venv/bin/python" \
  bash ground_zero_work/phase21/verify_phase21.sh
C48_PYTHON="$PWD/.venv/bin/python" ELAN_HOME="$HOME/.elan" \
  bash ground_zero_work/phase20/verify_phase20.sh
```

Expected terminal markers include:

- `PASS Phase 33 guarded MSS, exact-root, global, and attribution source checks`;
- three `PASS Phase 33 attribution source-contract mutation rejected` lines;
- eight `PASS Phase 32 source-contract mutation rejected` lines;
- `PASS Phase 33 multiline axiom audit and continuation mutation`;
- `PASS Phase 33 unguarded MSS negative-endpoint attack rejected`;
- `PASS Phase 33 fresh-review repair verification`;
- `PASS: Phase 21 complete direct-sector proof-surface checks`;
- `Phase 20 verification PASS`.

The `leanchecker --fresh` steps can run silently for many minutes.

From an extracted packet, run:

```bash
bash REPRODUCE/VERIFY_ARCHIVE.sh packet
```

This checks the fail-closed manifest, cryptographic checkpoint ancestry,
source-tree binding, and deterministic rebuild of all three manuscripts. In
the full audit archive, the same binding is also checked against the included
offline Git history bundle.
