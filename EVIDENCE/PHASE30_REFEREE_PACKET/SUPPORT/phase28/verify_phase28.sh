#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${C48_PYTHON:-$ROOT/.venv/bin/python}"
LEAN_ROOT="$ROOT/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

"$PYTHON" "$ROOT/ground_zero_work/phase28/phase28_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase26/t2_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase26/t3_horizontal_concavity_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase26/t5_saddle_main_ratio_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase26/t5_gamma_ratio_stirling_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase26/t6_manuscript_cauchy_mutations.py"

(
  cd "$LEAN_ROOT"
  lake build Zeta23.Research.JensenWedge.ManuscriptTheoremSevenOne \
    Zeta23.Research.JensenWedge
  lake env lean "$ROOT/ground_zero_work/phase28/Phase28Axioms.lean" \
    > "$TMP_DIR/PHASE28_AXIOM_AUDIT.txt"
)

"$PYTHON" "$ROOT/ground_zero_work/phase28/verify_phase28_axioms.py" \
  --output "$TMP_DIR/PHASE28_AXIOM_AUDIT.txt"

if rg -n '^\s*(sorry|admit|axiom|unsafe)\b' \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/ManuscriptTheoremSevenOne.lean"; then
  echo "FAIL Phase 28 proof escape detected" >&2
  exit 1
fi

echo "PASS Phase 28 literal T5 verification"
