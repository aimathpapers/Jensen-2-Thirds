#!/usr/bin/env bash
set -euo pipefail

phase18_dir="$(cd "$(dirname "$0")" && pwd)"
workspace_root="$(cd "$phase18_dir/../.." && pwd)"
lean_root="$workspace_root/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
elan_root="${ELAN_HOME:-$workspace_root/Kimi_Agent_Riemann Lean Exploration/.elan}"
lake_bin="$elan_root/bin/lake"
python_bin="${C48_PYTHON:-python3}"
symbolic="$workspace_root/ground_zero_work/c48_jensen/symbolic"
numerics="$workspace_root/ground_zero_work/c48_jensen/numerics"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
export PYTHONPYCACHEPREFIX="$tmp_dir/pycache"

if [[ ! -x "$lake_bin" ]]; then
  echo "missing pinned Lake proxy: $lake_bin" >&2
  exit 2
fi

if ! "$python_bin" -c 'import sympy; assert sympy.__version__ == "1.14.0"' \
    >/dev/null 2>&1; then
  echo "missing pinned SymPy 1.14.0; set C48_PYTHON to the pinned interpreter" >&2
  exit 2
fi

"$python_bin" -m py_compile "$symbolic/sixth_saddle.py"
"$python_bin" "$symbolic/sixth_saddle.py" \
  --output "$tmp_dir/sixth_saddle.json"
cmp "$symbolic/sixth_saddle.json" "$tmp_dir/sixth_saddle.json"
"$python_bin" "$symbolic/saddle_derivative_tower.py" \
  --output "$tmp_dir/saddle_derivative_tower.json"
cmp "$symbolic/saddle_derivative_tower.json" \
  "$tmp_dir/saddle_derivative_tower.json"
python3 "$numerics/effectivity_diagnostic.py" \
  --output "$tmp_dir/effectivity_diagnostic.json"
cmp "$numerics/effectivity_diagnostic.json" \
  "$tmp_dir/effectivity_diagnostic.json"

(
  cd "$lean_root"
  env ELAN_HOME="$elan_root" "$lake_bin" build Zeta23.Research.JensenWedge
  env ELAN_HOME="$elan_root" "$lake_bin" env leanchecker \
    Zeta23.Research.JensenWedge
  env ELAN_HOME="$elan_root" "$lake_bin" env lean \
    "$phase18_dir/Phase18Axioms.lean"

  if rg -n '\b(sorry|admit|axiom|unsafe|native_decide|implemented_by)\b' \
      Zeta23/Research/JensenWedge.lean \
      Zeta23/Research/JensenWedge; then
    echo "escape scan failed" >&2
    exit 3
  fi
)

if rg -n -F 'generalizes verbatim' \
    "$workspace_root/ground_zero_work/phase11/C48_SIXTH_RESIDUAL.md" \
    "$workspace_root/ground_zero_work/phase17/C48_SIXTH_STABILITY_AND_ASSEMBLY.md"; then
  echo "stale multiplier wording found" >&2
  exit 4
fi

echo "Phase 18 verification PASS"
echo "  exact derivative tower and complex-main denominator reproduced"
echo "  positive-orthant uniqueness kernel-checked"
echo "  printed Holland epsilon threshold used accurately"
echo "  complex analytic lemma remains paper mathematics; see Phase 20 GORTTW gate"
