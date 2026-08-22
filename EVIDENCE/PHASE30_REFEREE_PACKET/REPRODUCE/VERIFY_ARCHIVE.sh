#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-packet}"
python3 "$ROOT/VERIFY_BUNDLE.py"
python3 "$ROOT/VERIFY_ANCESTRY.py"
bash "$ROOT/REPRODUCE/BUILD_PACKET_MANUSCRIPTS.sh"

if [[ "$MODE" == packet ]]; then
  printf '%s\n' 'PASS extraction-local packet, ancestry, and manuscript replay'
  exit 0
fi
if [[ "$MODE" != quick && "$MODE" != full ]]; then
  printf '%s\n' 'usage: VERIFY_ARCHIVE.sh [packet|quick|full]' >&2
  exit 2
fi
BUNDLE="$ROOT/AUDIT/CANDIDATE_HISTORY.bundle"
if [[ ! -f "$BUNDLE" ]]; then
  printf '%s\n' "FAIL: $MODE requires the full audit archive history bundle" >&2
  exit 2
fi
PYTHON_BIN="${C48_PYTHON:-}"
if [[ -z "$PYTHON_BIN" || ! -x "$PYTHON_BIN" ]]; then
  printf '%s\n' 'FAIL: set C48_PYTHON to the pinned Python executable' >&2
  exit 2
fi
TMP_DIR="$(mktemp -d -t jensen-phase-m-repo.XXXXXX)"
trap 'rm -rf "$TMP_DIR"' EXIT
git clone --quiet --branch phase-m-candidate "$BUNDLE" "$TMP_DIR/repository"
if [[ "$MODE" == quick ]]; then
  C48_PYTHON="$PYTHON_BIN" C48_TECTONIC="${C48_TECTONIC:-$(command -v tectonic)}" \
    bash "$TMP_DIR/repository/reproduce/VERIFY_ALL.sh" quick
else
  ELAN_ROOT="${C48_ELAN_HOME:-${ELAN_HOME:-$HOME/.elan}}"
  LEAN_PROJECT="$TMP_DIR/repository/Kimi_Agent_Riemann Lean Exploration/zeta-23-lean"
  (
    cd "$LEAN_PROJECT"
    env ELAN_HOME="$ELAN_ROOT" "$ELAN_ROOT/bin/lake" exe cache get
    env ELAN_HOME="$ELAN_ROOT" "$ELAN_ROOT/bin/lake" build \
      Zeta23.Research.JensenWedge
  )
  C48_PYTHON="$PYTHON_BIN" C48_TECTONIC="${C48_TECTONIC:-$(command -v tectonic)}" \
    C48_ELAN_HOME="$ELAN_ROOT" \
    bash "$TMP_DIR/repository/reproduce/VERIFY_ALL.sh" full
fi
printf '%s\n' "PASS extraction-local audit repository $MODE replay"
