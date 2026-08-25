#!/usr/bin/env bash
set -euo pipefail

PHASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$PHASE_DIR/../.." && pwd)"
PYTHON_BIN="${C48_PYTHON:-python3}"
SCRIPT="$REPO_ROOT/ground_zero_work/c48_jensen/high_precision/leading_contour_check.py"
PROOF="$PHASE_DIR/C48_LEADING_CONTOUR_LOCALIZATION.md"
RESEARCH="$PHASE_DIR/SECTORIAL_CONTOUR_PRIMARY_RESEARCH.md"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

if ! "$PYTHON_BIN" -c 'import mpmath; assert mpmath.__version__ == "1.3.0"' \
    >/dev/null 2>&1; then
  echo "missing pinned mpmath 1.3.0; set C48_PYTHON to the pinned interpreter" >&2
  exit 2
fi

"$PYTHON_BIN" -m py_compile "$SCRIPT"
"$PYTHON_BIN" "$SCRIPT" >"$TMP_DIR/leading_contour_check.txt"
cat "$TMP_DIR/leading_contour_check.txt"
grep -Fq "PASS: leading contour ratios converge" \
  "$TMP_DIR/leading_contour_check.txt"

grep -Fq "Lemma 21A (sectorial leading-mode localization)" "$PROOF"
grep -Fq "It does not yet prove" "$PROOF"
grep -Fq "Verdict: **RESTATE.**" "$RESEARCH"

printf '%s\n' "PASS: Phase 21 leading-contour proof-surface checks"
