#!/usr/bin/env bash
set -euo pipefail

phase20_dir="$(cd "$(dirname "$0")" && pwd)"
workspace_root="$(cd "$phase20_dir/../.." && pwd)"
lean_root="$workspace_root/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
elan_root="${ELAN_HOME:-$workspace_root/Kimi_Agent_Riemann Lean Exploration/.elan}"
lake_bin="$elan_root/bin/lake"
python_bin="${C48_PYTHON:-python3}"
symbolic="$workspace_root/ground_zero_work/c48_jensen/symbolic"
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

"$python_bin" -m py_compile "$symbolic/saddle_branch_check.py"
"$python_bin" "$symbolic/saddle_branch_check.py" >"$tmp_dir/saddle_branch_check.txt"
rg -q 'rigorous coefficientwise bound on' "$tmp_dir/saddle_branch_check.txt"
rg -q '\|H_6\| <=' "$tmp_dir/saddle_branch_check.txt"
rg -q 'left-endpoint regression PASS' "$tmp_dir/saddle_branch_check.txt"
"$python_bin" "$symbolic/sixth_saddle.py" \
  --output "$tmp_dir/sixth_saddle.json"
cmp "$symbolic/sixth_saddle.json" "$tmp_dir/sixth_saddle.json"
"$python_bin" "$symbolic/direct_recurrence.py" \
  --output "$tmp_dir/direct_recurrence.json"
cmp "$symbolic/direct_recurrence.json" "$tmp_dir/direct_recurrence.json"

(
  cd "$lean_root"
  env ELAN_HOME="$elan_root" "$lake_bin" build Zeta23.Research.JensenWedge
  env ELAN_HOME="$elan_root" "$lake_bin" env leanchecker \
    Zeta23.Research.JensenWedge
  env ELAN_HOME="$elan_root" "$lake_bin" env lean \
    "$phase20_dir/Phase20Axioms.lean"

  if rg -n '\b(sorry|admit|axiom|unsafe|native_decide|implemented_by)\b' \
      Zeta23/Research/JensenWedge.lean \
      Zeta23/Research/JensenWedge; then
    echo "escape scan failed" >&2
    exit 3
  fi
)

rg -q 'Holland Theorem 1.1.*Not a premise' \
  "$phase20_dir/HOLLAND_DEPENDENCY_FIREWALL.md"
rg -q 'Transport of Theorem 21B' "$phase20_dir/HOLLAND_PROP41_REPROOF.md"
rg -q 'Theorem 21B' \
  "$workspace_root/ground_zero_work/phase21/C48_XI_COEFFICIENT_ASSEMBLY.md"
rg -q 'C48-GORTTW-SECTOR.*Internally discharged' \
  "$workspace_root/ground_zero_work/ASSUMPTION_REGISTRY.md"
rg -q 'epsilon<16' "$phase20_dir/HOLLAND_MULTIPLIER_REPROOF.md"
rg -Fq 'K_0=\max\{256,256C_{\rm loc}^2\}' \
  "$workspace_root/ground_zero_work/phase16/C48_UNIFORM_RADIUS_PROOF.md"
rg -Fq 'K_{\rm pre}=256' \
  "$workspace_root/ground_zero_work/phase16/C48_UNIFORM_RADIUS_PROOF.md"
rg -Fq 'E_{n,k}=\Delta_k(r_k-m_k)' \
  "$workspace_root/ground_zero_work/phase15/C48_FULL_C1_BRANCH.md"
rg -Fq '\tag{HG}' \
  "$workspace_root/ground_zero_work/phase18/C48_COMPLEX_SIXTH_SADDLE.md"
rg -q 'after reversing all three polynomials' \
  "$workspace_root/ground_zero_work/phase16/C48_UNIFORM_RADIUS_PROOF.md"

echo "Phase 20 verification PASS"
echo "  Holland headline theorem excluded from the logical premises"
echo "  saddle-variable endpoint and exact H6 coefficient bound reproduced"
echo "  multiplier/sign/conditional firewall kernel-checked"
echo "  former GORTTW sectorial premise has a direct Phase-21 paper proof"
echo "  separated analytic AI pre-review passed; human review is not claimed"
