#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PYTHON="${C48_PYTHON:-$ROOT/.venv/bin/python}"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

"$PYTHON" "$ROOT/ground_zero_work/phase25/verify_phase25_metadata.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/phase25_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/hermite_genocchi_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/elementary_cube_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/hypergeometric_property_tests.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/hypergeometric_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/branch_interval_certificates.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/branch_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/finite_free_property_tests.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/finite_free_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase24/verify_interval_certificates.py"
"$PYTHON" "$ROOT/ground_zero_work/phase24/verify_mathematica_evidence.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/arb_acb_verification.py" \
  --output "$TMP_DIR/ARB_ACB_RESULTS.json"
cmp "$ROOT/ground_zero_work/phase25/ARB_ACB_RESULTS.json" \
  "$TMP_DIR/ARB_ACB_RESULTS.json"
"$PYTHON" "$ROOT/ground_zero_work/phase25/arb_acb_verification.py" \
  --output "$TMP_DIR/ARB_ACB_RESULTS_SECOND.json"
cmp "$TMP_DIR/ARB_ACB_RESULTS.json" "$TMP_DIR/ARB_ACB_RESULTS_SECOND.json"
"$PYTHON" "$ROOT/ground_zero_work/phase25/arb_acb_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/effectivity_ledger.py" --check
"$PYTHON" "$ROOT/ground_zero_work/phase25/effectivity_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/analytic_adapters_semantic_mutations.py"
"$PYTHON" "$ROOT/ground_zero_work/phase24/manuscript_equation_regression.py"
"$PYTHON" "$ROOT/ground_zero_work/phase25/manuscript_semantic_mutations.py"

TECTONIC="${C48_TECTONIC:-$(command -v tectonic)}"
if [[ -z "$TECTONIC" ]]; then
  printf '%s\n' 'FAIL: tectonic is required for manuscript verification' >&2
  exit 1
fi
mkdir -p "$TMP_DIR/manuscript"
"$TECTONIC" -X compile "$ROOT/paper/JENSEN_TWO_THIRDS_MAIN.tex" \
  --outdir "$TMP_DIR/manuscript" --keep-logs --keep-intermediates
"$TECTONIC" -X compile "$ROOT/paper/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex" \
  --outdir "$TMP_DIR/manuscript" --keep-logs --keep-intermediates
"$PYTHON" "$ROOT/ground_zero_work/phase25/manuscript_release_checks.py" \
  --pdf-dir "$TMP_DIR/manuscript"
"$PYTHON" "$ROOT/ground_zero_work/phase25/reproducibility_behavioral_mutations.py"
C48_TECTONIC="$TECTONIC" \
  "$PYTHON" "$ROOT/ground_zero_work/phase25/verify_reproducibility_inventory.py"

LEAN_ROOT="$ROOT/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
(
  cd "$LEAN_ROOT"
  lake build Zeta23.Research.JensenWedge.HermiteGenocchiCube \
    Zeta23.Research.JensenWedge.HermiteGenocchiFTC \
    Zeta23.Research.JensenWedge.ComplexHermiteGenocchi \
    Zeta23.Research.JensenWedge.ElementaryCubeCalculus \
    Zeta23.Research.JensenWedge.TerminatingHypergeometric \
    Zeta23.Research.JensenWedge.QuantitativeBranch \
    Zeta23.Research.JensenWedge.FiniteFreeAdapters \
    Zeta23.Research.JensenWedge.AnalyticAdapters \
    Zeta23.Research.JensenWedge
  lake env lean "$ROOT/ground_zero_work/phase25/Phase25Axioms.lean" \
    > "$TMP_DIR/PHASE25_AXIOM_AUDIT.txt"
)

"$PYTHON" "$ROOT/ground_zero_work/phase25/verify_phase25_axioms.py" \
  --output "$TMP_DIR/PHASE25_AXIOM_AUDIT.txt"
cmp "$ROOT/ground_zero_work/phase25/PHASE25_AXIOM_AUDIT.txt" \
  "$TMP_DIR/PHASE25_AXIOM_AUDIT.txt"

if rg -n '^\s*(sorry|admit|axiom|unsafe)\b' \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/HermiteGenocchiCube.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/HermiteGenocchiFTC.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/ComplexHermiteGenocchi.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/ElementaryCubeCalculus.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/TerminatingHypergeometric.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/QuantitativeBranch.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/FiniteFreeAdapters.lean" \
  "$LEAN_ROOT/Zeta23/Research/JensenWedge/AnalyticAdapters.lean"
then
  printf '%s\n' 'FAIL: proof escape in Phase-25 formal sources' >&2
  exit 1
fi

echo "PASS Phase 25 formal, exact, interval, effectivity, manuscript, reproducibility, and semantic gates"
