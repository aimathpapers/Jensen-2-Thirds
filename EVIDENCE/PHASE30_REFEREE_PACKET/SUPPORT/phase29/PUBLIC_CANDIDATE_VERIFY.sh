#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

python3 "$ROOT/verification/verify_candidate.py"

(
  cd "$ROOT"
  lake build Challenge.TheoremSevenOne Solution.TheoremSevenOne
  lake env lean comparator/PrintAxioms/TheoremSevenOne.lean > "$TMP_DIR/axioms.txt"
)

python3 "$ROOT/verification/verify_axioms.py" < "$TMP_DIR/axioms.txt"

(
  cd "$ROOT"
  lake env leanchecker --fresh Solution.TheoremSevenOne
)

echo "PASS T5 public candidate verification"
