#!/usr/bin/env bash
set -euo pipefail

phase17_dir="$(cd "$(dirname "$0")" && pwd)"
workspace_root="$(cd "$phase17_dir/../.." && pwd)"
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
  env ELAN_HOME="$elan_root" "$lake_bin" env lean "$phase17_dir/Phase17Axioms.lean"

  if rg -n '\b(sorry|admit|axiom|unsafe|native_decide|implemented_by)\b' \
      Zeta23/Research/JensenWedge.lean \
      Zeta23/Research/JensenWedge; then
    echo "escape scan failed" >&2
    exit 3
  fi
)

echo "Phase 17 verification PASS"
echo "  sixth-order geometric tail and supporting finite algebra kernel-checked"
echo "  internal theorem assembly complete"
echo "  independent analytic and algebraic reviews remain hard release gates"

