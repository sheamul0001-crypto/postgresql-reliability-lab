#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/../../.env"
BACKUP_FILE="${1:?Usage: restore.sh <path/to/backup.sql.gz>}"
LOG="$(dirname "$0")/../../logs/restore.log"

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG"; }

log "INFO  restore started file=$BACKUP_FILE"

gunzip -c "$BACKUP_FILE" | docker exec -i pg_lab psql \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB"

log "INFO  restore complete"
