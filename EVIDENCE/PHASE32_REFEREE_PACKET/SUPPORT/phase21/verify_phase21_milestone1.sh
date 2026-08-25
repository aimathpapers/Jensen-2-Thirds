#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${C48_PYTHON:-python3}"
SCRIPT="$REPO_ROOT/ground_zero_work/c48_jensen/symbolic/gorttw_mellin_milestone1.py"
NOTE="$REPO_ROOT/ground_zero_work/phase21/C48_GORTTW_SECTOR_MILESTONE1.md"
PLAN="$REPO_ROOT/ground_zero_work/phase21/C48_GORTTW_SECTOR_EXECUTION_PLAN.md"
SOURCE_AUDIT="$REPO_ROOT/ground_zero_work/phase21/GORTTW_MELLIN_SOURCE_RECONSTRUCTION.md"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

if ! "$PYTHON_BIN" -c 'import sympy; assert sympy.__version__ == "1.14.0"' \
    >/dev/null 2>&1; then
  echo "missing pinned SymPy 1.14.0; set C48_PYTHON to the pinned interpreter" >&2
  exit 2
fi

"$PYTHON_BIN" -m py_compile "$SCRIPT"
output="$($PYTHON_BIN "$SCRIPT")"
printf '%s\n' "$output"
grep -Fq "PASS: Milestone 1 exact symbolic regression" <<<"$output"

grep -Fq "does **not** prove" "$NOTE"
grep -Fq "C48-GORTTW-SECTOR" "$PLAN"
grep -Fq "uniform complex contour" "$PLAN"
grep -Fq "Milestone 21A: sectorial leading-contour lemma" "$SOURCE_AUDIT"

printf '%s\n' "PASS: Phase 21 Milestone 1 fail-closed documentation checks"
