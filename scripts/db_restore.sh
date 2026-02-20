#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: ./scripts/db_restore.sh backups/filename.sql.gz"
  exit 1
fi

if [[ -z "${DATABASE_URL:-}" ]]; then
  echo "DATABASE_URL is required"
  exit 1
fi

INFILE="$1"

gunzip -c "$INFILE" | psql "$DATABASE_URL"

echo "Restore completed from: $INFILE"
