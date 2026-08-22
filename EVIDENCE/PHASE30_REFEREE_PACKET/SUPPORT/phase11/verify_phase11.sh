#!/usr/bin/env bash
set -euo pipefail

phase11_dir="$(cd "$(dirname "$0")" && pwd)"
workspace_root="$(cd "$phase11_dir/../.." && pwd)"
symbolic="$workspace_root/ground_zero_work/c48_jensen/symbolic"
artifact="$symbolic/sixth_saddle.json"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
export PYTHONPYCACHEPREFIX="$tmp_dir/pycache"

if ! python3 -c 'import sympy; assert sympy.__version__ == "1.14.0"' \
    >/dev/null 2>&1; then
  echo "missing pinned Phase-11 dependencies" >&2
  echo "install ground_zero_work/c48_jensen/symbolic/requirements.lock" >&2
  exit 2
fi

python3 -m py_compile "$symbolic/sixth_saddle.py"
python3 "$symbolic/sixth_saddle.py" --output "$tmp_dir/sixth_saddle.json"
cmp "$artifact" "$tmp_dir/sixth_saddle.json"

"$workspace_root/ground_zero_work/phase10/verify_phase10.sh"

echo "Phase 11 verification PASS"
echo "  exact sixth saddle-main coefficient 24 reproduced"
echo "  chain-rule h6 coefficient 48 reproduced"
echo "  paper residual derivation awaits review"
echo "  critical-point root radius is not discharged by Phase 11"
