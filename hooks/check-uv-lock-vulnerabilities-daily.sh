#!/bin/sh
set -eu

# File to track last run per repo
TIMESTAMP_FILE=".git/.pre-commit-uv-lock-last-run"

# Usage: hooks/check-uv-lock-vulnerabilities-daily.sh <interval_hours>
INTERVAL_HOURS="${1:-24}"  # default to 24 hours if not provided

# Convert hours to seconds
MIN_INTERVAL=$(expr "$INTERVAL_HOURS" \* 60 \* 60)

# Check last run
if [ -f "$TIMESTAMP_FILE" ]; then
    LAST_RUN=$(cat "$TIMESTAMP_FILE")
    NOW=$(date +%s)
    DIFF=$(expr "$NOW" - "$LAST_RUN")
    if [ "$DIFF" -lt "$MIN_INTERVAL" ]; then
        echo "Skipping uv.lock vulnerability scan (already ran successfully in the last $INTERVAL_HOURS hours)"
        exit 0
    fi
fi

# Directory of this script (cross-platform)
HOOK_DIR=$(dirname "$0")

# Run the original hook
sh "$HOOK_DIR/check-uv-lock-vulnerabilities.sh"

# Update timestamp
date +%s > "$TIMESTAMP_FILE"
