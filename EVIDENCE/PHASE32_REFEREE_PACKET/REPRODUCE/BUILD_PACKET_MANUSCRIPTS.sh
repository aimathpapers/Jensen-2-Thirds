#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TECTONIC="${C48_TECTONIC:-$(command -v tectonic || true)}"
if [[ -z "$TECTONIC" || ! -x "$TECTONIC" ]]; then
  printf '%s
' 'FAIL: Tectonic is required for manuscript replay' >&2
  exit 2
fi
TMP_DIR="$(mktemp -d -t jensen-phase-m-pdf.XXXXXX)"
trap 'rm -rf "$TMP_DIR"' EXIT
export SOURCE_DATE_EPOCH="1787572800"
"$TECTONIC" -X compile "$ROOT/PAPER/source/JENSEN_TWO_THIRDS_MAIN.tex" --outdir "$TMP_DIR"
"$TECTONIC" -X compile "$ROOT/PAPER/source/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.tex" --outdir "$TMP_DIR"
cmp "$TMP_DIR/JENSEN_TWO_THIRDS_MAIN.pdf" "$ROOT/PAPER/JENSEN_TWO_THIRDS_MAIN.pdf"
cmp "$TMP_DIR/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf" "$ROOT/PAPER/JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT.pdf"
printf '%s
' 'PASS extraction-local deterministic manuscript replay'
