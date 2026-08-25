# Expected Phase 30 verification results

From the repository root, the full Phase-30 gate is:

```bash
C48_PYTHON="$PWD/.venv/bin/python" \
  bash ground_zero_work/phase30/verify_phase30.sh
```

Expected terminal markers include:

- `PASS Phase 30 xi-multiplier semantic source contract`
- nine `PASS Phase 30 mutation rejected` lines
- `PASS Phase 30 independent exact Newton/sign-transfer regressions`
- `PASS Phase 30 typed-input and reader-surface boundary audit`
- `Build completed successfully (8833 jobs)`
- `PASS Phase 30 terminal axiom audit`
- `PASS Phase 30 xi-specific multiplier and headline verification`

The final fresh replay can take many minutes and may be silent while it
checks the imported object graph.

From the extracted referee packet, run:

```bash
bash REPRODUCE/VERIFY_ARCHIVE.sh packet
```

This checks the fail-closed manifest, cryptographic checkpoint ancestry, and
deterministic manuscript rebuild. The reassembled full-audit archive also
supports `quick` and `full` repository replay modes as documented in
`PACKAGE_INDEX.md`.
