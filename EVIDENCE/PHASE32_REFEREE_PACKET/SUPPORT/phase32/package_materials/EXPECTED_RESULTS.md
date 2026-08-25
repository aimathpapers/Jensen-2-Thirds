# Expected Phase 32 verification results

From the repository root, run:

```bash
C48_PYTHON="$PWD/.venv/bin/python" \
  bash ground_zero_work/phase32/verify_phase32.sh
```

Expected terminal markers include:

- `PASS Phase 32 Holland citation and concrete MMP source contract`
- seven `PASS Phase 32 mutation rejected` lines
- `PASS all Phase 32 semantic mutations`
- `Build completed successfully (8830 jobs)` or a later equivalent count
- `PASS Phase 32 axiom audit`
- `PASS Phase 32 citation, MMP specialization, and cutoff absorption verification`

The final `leanchecker --fresh` replay can take many minutes and can be silent
while it reloads the imported object graph.

From the extracted referee packet, run:

```bash
bash REPRODUCE/VERIFY_ARCHIVE.sh packet
```

This checks the fail-closed manifest, cryptographic checkpoint ancestry, and
deterministic manuscript rebuild. The reassembled full-audit archive also
supports the documented `quick` and `full` repository replay modes.
