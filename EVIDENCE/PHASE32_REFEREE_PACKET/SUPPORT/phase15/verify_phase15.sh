#!/usr/bin/env bash
set -euo pipefail

phase15_dir="$(cd "$(dirname "$0")" && pwd)"
workspace_root="$(cd "$phase15_dir/../.." && pwd)"
lean_root="$workspace_root/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
elan_root="${ELAN_HOME:-$workspace_root/Kimi_Agent_Riemann Lean Exploration/.elan}"
lake_bin="$elan_root/bin/lake"

if [[ ! -x "$lake_bin" ]]; then
  echo "missing pinned Lake proxy: $lake_bin" >&2
  exit 2
fi

(
  cd "$lean_root"
  env ELAN_HOME="$elan_root" "$lake_bin" build Zeta23.Research.JensenWedge
  env ELAN_HOME="$elan_root" "$lake_bin" env leanchecker Zeta23.Research.JensenWedge
  env ELAN_HOME="$elan_root" "$lake_bin" env lean "$phase15_dir/Phase15Axioms.lean"

  if rg -n '\b(sorry|admit|axiom|unsafe|native_decide|implemented_by)\b' \
      Zeta23/Research/JensenWedge.lean \
      Zeta23/Research/JensenWedge; then
    echo "escape scan failed" >&2
    exit 3
  fi
)

echo "Phase 15 verification PASS"
echo "  saddle weights, triangular equivalence, and inverse kernel-checked"
echo "  full C1 branch proof assembled at paper level"
echo "  final Jensen theorem remains blocked on radius constants and review"

