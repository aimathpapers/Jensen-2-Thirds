#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${C48_PYTHON:-$ROOT/.venv/bin/python}"
LEAN_DIR="$ROOT/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

"$PYTHON_BIN" "$ROOT/ground_zero_work/phase33/phase33_source_checks.py"
"$PYTHON_BIN" "$ROOT/ground_zero_work/phase32/phase32_mmp_checks.py"

(
  cd "$LEAN_DIR"
  lake build Zeta23.Research.JensenWedge.XiNaturalMultiplierCertificate
  lake env lean "$ROOT/ground_zero_work/phase33/Phase33Axioms.lean" \
    > "$TMP_DIR/PHASE33_AXIOM_AUDIT.txt"
  cmp "$TMP_DIR/PHASE33_AXIOM_AUDIT.txt" \
    "$ROOT/ground_zero_work/phase33/PHASE33_AXIOM_AUDIT.txt"
  lake env leanchecker --fresh \
    Zeta23.Research.JensenWedge.XiNaturalMultiplierCertificate
)

"$PYTHON_BIN" "$ROOT/ground_zero_work/phase33/verify_phase33_axioms.py" \
  --output "$TMP_DIR/PHASE33_AXIOM_AUDIT.txt"
"$PYTHON_BIN" "$ROOT/ground_zero_work/phase33/verify_mss_guard_regression.py"

if rg -n '^\s*(sorry|admit|axiom|unsafe)\b|sorryAx|Lean\.ofReduceBool' \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/MultiplierStability.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/RiemannXiJensen.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalFiniteFreeSpecialization.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalMultiplierCertificate.lean"; then
  echo "FAIL Phase 33 proof escape detected" >&2
  exit 1
fi

echo "PASS Phase 33 fresh-review repair verification"
