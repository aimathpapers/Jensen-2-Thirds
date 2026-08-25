#!/usr/bin/env bash
set -euo pipefail

PHASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$PHASE_DIR/../.." && pwd)"
PYTHON_BIN="${C48_PYTHON:-$ROOT/.venv/bin/python}"
LEAN_ROOT="$ROOT/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"

"$PYTHON_BIN" "$PHASE_DIR/verify_interval_certificates.py"
"$PYTHON_BIN" "$PHASE_DIR/verify_mathematica_evidence.py"
"$PYTHON_BIN" "$PHASE_DIR/release_checks.py"
"$PYTHON_BIN" "$PHASE_DIR/mutation_tests.py"
"$PYTHON_BIN" "$PHASE_DIR/manuscript_equation_regression.py"

(
  cd "$LEAN_ROOT"
  lake build Zeta23.Research.JensenWedge
)

if rg -n '^\s*(sorry|admit|axiom|unsafe)\b' \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/QuotientAdapter.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/HermiteGenocchiCube.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/ComplexHermiteGenocchi.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/ElementaryCubeBounds.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/SaddleBounds.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/JensenPolynomial.lean"
then
  printf '%s\n' 'FAIL: proof escape in Phase-24 Lean sources' >&2
  exit 1
fi

printf '%s\n' 'PASS Phase 24 formalization, interval, and mutation gates'
