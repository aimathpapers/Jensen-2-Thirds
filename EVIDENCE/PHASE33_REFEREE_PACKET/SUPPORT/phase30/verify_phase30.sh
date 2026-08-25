#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${C48_PYTHON:-$ROOT/.venv/bin/python}"
LEAN_DIR="$ROOT/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

"$PYTHON_BIN" "$ROOT/ground_zero_work/phase30/phase30_semantic_mutations.py"
"$PYTHON_BIN" "$ROOT/ground_zero_work/phase30/phase30_adversarial_checks.py"

if rg -n '^\s*(sorry|admit|axiom|unsafe)\b|sorryAx|Lean\.ofReduceBool' \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalConcreteMultiplier.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalConcreteMultiplierBound.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalConcreteMultiplierSpecialization.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalMultiplierEndpoint.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/PolynomialRootIntervals.lean" \
  "$LEAN_DIR/Zeta23/Research/JensenWedge/XiNaturalMultiplierCertificate.lean"; then
  echo "FAIL Phase 30 proof escape detected" >&2
  exit 1
fi

(
  cd "$LEAN_DIR"
  lake build Zeta23.Research.JensenWedge.XiNaturalMultiplierCertificate \
    Zeta23.Research.JensenWedge
  lake env lean "$ROOT/ground_zero_work/phase30/Phase30Axioms.lean" \
    > "$TMP_DIR/PHASE30_AXIOM_AUDIT.txt"
)

"$PYTHON_BIN" "$ROOT/ground_zero_work/phase30/verify_phase30_axioms.py" \
  --output "$TMP_DIR/PHASE30_AXIOM_AUDIT.txt"

(
  cd "$LEAN_DIR"
  lake env leanchecker --fresh Zeta23.Research.JensenWedge.XiNaturalMultiplierCertificate
)

echo "PASS Phase 30 xi-specific multiplier and headline verification"
