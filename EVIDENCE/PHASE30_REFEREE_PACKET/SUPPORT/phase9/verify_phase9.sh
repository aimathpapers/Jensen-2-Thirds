#!/usr/bin/env bash
set -euo pipefail

phase9_dir="$(cd "$(dirname "$0")" && pwd)"
workspace_root="$(cd "$phase9_dir/../.." && pwd)"
symbolic="$workspace_root/ground_zero_work/c48_jensen/symbolic"
artifact="$symbolic/saddle_main_term.json"
tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT
export PYTHONPYCACHEPREFIX="$tmp_dir/pycache"

if ! python3 -c 'import sympy; assert sympy.__version__ == "1.14.0"' \
    >/dev/null 2>&1; then
  echo "missing pinned Phase-9 dependencies" >&2
  echo "install ground_zero_work/c48_jensen/symbolic/requirements.lock" >&2
  exit 2
fi

python3 -m py_compile "$symbolic/saddle_main_term.py"
python3 "$symbolic/saddle_main_term.py" --output "$tmp_dir/saddle_main_term.json"
cmp "$artifact" "$tmp_dir/saddle_main_term.json"

"$workspace_root/ground_zero_work/phase8/verify_phase8.sh"

echo "Phase 9 verification PASS"
echo "  exact saddle-main coefficients 2 and -6 reproduced"
echo "  chain-rule fifth coefficient -12 reproduced"
echo "  full C1 assembly is not discharged by Phase 9"
echo "  h6 and the Jensen wedge are not discharged by Phase 9"
