#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${C48_PYTHON:-$ROOT/.venv/bin/python}"
LEAN_DIR="$ROOT/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

"$PYTHON_BIN" "$ROOT/ground_zero_work/phase32/phase32_mmp_checks.py"

if rg -n '^\s*(sorry|admit|axiom|unsafe)\b|sorryAx|Lean\.ofReduceBool' \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/ConditionalAssembly.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/FiniteFreeAdapters.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalFiniteFreeSpecialization.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalCriticalRadius.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalMultiplierCertificate.lean"; then
  echo "FAIL Phase 32 proof escape detected" >&2
  exit 1
fi

(
  cd "$LEAN_DIR"
  lake build Zeta23.Research.JensenWedge.XiNaturalMultiplierCertificate
  lake env lean "$ROOT/ground_zero_work/phase32/Phase32Axioms.lean" \
    > "$TMP_DIR/PHASE32_AXIOM_AUDIT.txt"
  lake env leanchecker --fresh \
    Zeta23.Research.JensenWedge.XiNaturalMultiplierCertificate
)

"$PYTHON_BIN" "$ROOT/ground_zero_work/phase32/verify_phase32_axioms.py" \
  --output "$TMP_DIR/PHASE32_AXIOM_AUDIT.txt"

echo "PASS Phase 32 citation, MMP specialization, and cutoff absorption verification"
