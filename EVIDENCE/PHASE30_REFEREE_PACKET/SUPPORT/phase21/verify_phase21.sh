#!/usr/bin/env bash
set -euo pipefail

PHASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$PHASE_DIR/../.." && pwd)"
PYTHON_BIN="${C48_PYTHON:-python3}"
SYMBOLIC="$REPO_ROOT/ground_zero_work/c48_jensen/symbolic"
HIGH_PRECISION="$REPO_ROOT/ground_zero_work/c48_jensen/high_precision"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
export PYTHONPYCACHEPREFIX="$TMP_DIR/pycache"

if ! "$PYTHON_BIN" -c '
import mpmath, sympy
assert mpmath.__version__ == "1.3.0"
assert sympy.__version__ == "1.14.0"
' >/dev/null 2>&1; then
  echo "missing pinned mpmath 1.3.0 / SymPy 1.14.0 environment" >&2
  echo "set C48_PYTHON to the pinned interpreter" >&2
  exit 2
fi

scripts=(
  "$SYMBOLIC/gorttw_mellin_milestone1.py"
  "$HIGH_PRECISION/leading_contour_check.py"
  "$SYMBOLIC/gorttw_assembly_check.py"
  "$PHASE_DIR/check_phase21_notes.py"
)

for script in "${scripts[@]}"; do
  "$PYTHON_BIN" -m py_compile "$script"
done

"$PYTHON_BIN" "${scripts[0]}" >"$TMP_DIR/milestone1.txt"
"$PYTHON_BIN" "${scripts[1]}" >"$TMP_DIR/contour.txt"
"$PYTHON_BIN" "${scripts[2]}" >"$TMP_DIR/assembly.txt"
"$PYTHON_BIN" "${scripts[3]}" >"$TMP_DIR/notes.txt"
cat "$TMP_DIR/milestone1.txt" "$TMP_DIR/contour.txt" "$TMP_DIR/assembly.txt" "$TMP_DIR/notes.txt"

grep -Fq "PASS: Milestone 1 exact symbolic regression" "$TMP_DIR/milestone1.txt"
grep -Fq "PASS: leading contour ratios converge" "$TMP_DIR/contour.txt"
grep -Fq "PASS: wide-angle contour robustness diagnostic" "$TMP_DIR/contour.txt"
grep -Fq "PASS: direct Im(L) bootstrap" "$TMP_DIR/contour.txt"
grep -Fq "PASS: Phase 21 xi-coefficient assembly algebra" "$TMP_DIR/assembly.txt"
grep -Fq "PASS: Phase 21 repaired note statements" "$TMP_DIR/notes.txt"

grep -Fq "Theorem 21B (\`C48-GORTTW-SECTOR\`)" \
  "$PHASE_DIR/C48_XI_COEFFICIENT_ASSEMBLY.md"
grep -Fq "separated Kimi K3" \
  "$PHASE_DIR/C48_XI_COEFFICIENT_ASSEMBLY.md"
grep -Fq "does not constitute" \
  "$PHASE_DIR/C48_XI_COEFFICIENT_ASSEMBLY.md"

printf '%s\n' "PASS: Phase 21 complete direct-sector proof-surface checks"
