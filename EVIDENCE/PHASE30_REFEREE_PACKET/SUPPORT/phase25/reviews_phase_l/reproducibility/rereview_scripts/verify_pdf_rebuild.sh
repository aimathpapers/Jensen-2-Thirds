#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  printf '%s\n' 'usage: verify_pdf_rebuild.sh EXTRACTED_PACKET' >&2
  exit 2
fi

PACKET="$(cd "$1" && pwd)"
TECTONIC="${C48_TECTONIC:-$(command -v tectonic || true)}"
if [[ -z "$TECTONIC" || ! -x "$TECTONIC" ]]; then
  printf '%s\n' 'FAIL: Tectonic is required' >&2
  exit 2
fi

TMP_DIR="$(mktemp -d -t phase-l-pdf-rebuild.XXXXXX)"
trap 'rm -rf "$TMP_DIR"' EXIT

CANDIDATE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8"))["candidate_commit"])' "$PACKET/BUNDLE_METADATA.json")"
git init --quiet "$TMP_DIR/repository"
git -C "$TMP_DIR/repository" fetch --quiet \
  "$PACKET/CANDIDATE_HISTORY.bundle" \
  refs/heads/phase-l-candidate:refs/heads/phase-l-candidate
git -C "$TMP_DIR/repository" checkout --quiet --detach "$CANDIDATE"

mkdir -p "$TMP_DIR/first" "$TMP_DIR/second"
C48_TECTONIC="$TECTONIC" \
  bash "$TMP_DIR/repository/reproduce/BUILD_MANUSCRIPTS.sh" "$TMP_DIR/first"
C48_TECTONIC="$TECTONIC" \
  bash "$TMP_DIR/repository/reproduce/BUILD_MANUSCRIPTS.sh" "$TMP_DIR/second"

for name in JENSEN_TWO_THIRDS_MAIN JENSEN_TWO_THIRDS_TECHNICAL_SUPPLEMENT; do
  cmp "$TMP_DIR/first/$name.pdf" "$TMP_DIR/second/$name.pdf"
  cmp "$TMP_DIR/first/$name.pdf" "$TMP_DIR/repository/output/pdf/$name.pdf"
  cmp "$TMP_DIR/first/$name.pdf" "$PACKET/manuscript/$name.pdf"
  creation="$(TZ=UTC pdfinfo "$TMP_DIR/first/$name.pdf" | sed -n 's/^CreationDate:[[:space:]]*//p')"
  if [[ "$creation" != 'Mon Aug 17 12:00:00 2026 UTC' ]]; then
    printf '%s\n' "FAIL: unexpected PDF CreationDate for $name: $creation" >&2
    exit 1
  fi
done

printf '%s\n' \
  'PASS two fresh PDF builds are mutually identical and match candidate/packet PDFs; fixed creation timestamp confirmed'
