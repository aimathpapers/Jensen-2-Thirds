#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON_BIN="${C48_PYTHON:-$ROOT/.venv/bin/python}"
LEAN_DIR="$ROOT/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

"$PYTHON_BIN" "$ROOT/ground_zero_work/phase29/verify_palomar_t5_surface.py" --root "$ROOT"
"$PYTHON_BIN" "$ROOT/ground_zero_work/phase29/palomar_t5_semantic_mutations.py"

ruby -e 'require "yaml"; YAML.safe_load(File.read(ARGV[0]), permitted_classes: [], aliases: false); puts "PASS formalization.yaml parses safely"' \
  "$LEAN_DIR/comparator/formalization-theorem-seven-one.yaml"

if rg -n 'import (Zeta23|ChallengeDeps)' \
    "$LEAN_DIR/comparator/Challenge/TheoremSevenOne.lean"; then
  echo "FAIL candidate-local import reached the trusted challenge" >&2
  exit 1
fi

if rg -n '\b(sorry|admit|unsafe)\b|sorryAx|Lean\.ofReduceBool' \
    "$LEAN_DIR/comparator/Solution/TheoremSevenOne.lean"; then
  echo "FAIL proof escape token in Palomar solution" >&2
  exit 1
fi

(
  cd "$LEAN_DIR"
  lake build Challenge.TheoremSevenOne Solution.TheoremSevenOne
  lake env lean comparator/PrintAxioms/TheoremSevenOne.lean > "$TMP_DIR/axioms.txt"
)
"$PYTHON_BIN" "$ROOT/ground_zero_work/phase29/verify_phase29_axioms.py" < "$TMP_DIR/axioms.txt"

(
  cd "$LEAN_DIR"
  lake env leanchecker --fresh Solution.TheoremSevenOne
)

echo "PASS Phase 29 Palomar T5 package verification"
