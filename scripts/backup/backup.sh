#!/usr/bin/env bash
set -euo pipefail

source "$(dirname "$0")/../../.env"

BACKUP_DIR="$(dirname "$0")/../../backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="$BACKUP_DIR/${POSTGRES_DB}_${TIMESTAMP}.sql.gz"
LOG="$(dirname "$0")/../../logs/backup.log"

mkdir -p "$BACKUP_DIR"

log() { echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) $*" | tee -a "$LOG"; }

log "INFO  backup started filename=$FILENAME"

docker exec pg_lab pg_dump \
    -U "$POSTGRES_USER" \
    "$POSTGRES_DB" | gzip > "$FILENAME"

SIZE=$(du -sh "$FILENAME" | cut -f1)
log "INFO  backup complete size=$SIZE"

find "$BACKUP_DIR" -name "*.sql.gz" -mtime +7 -delete
log "INFO  retention cleanup done"
