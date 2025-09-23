#!/usr/bin/env bash
set -euo pipefail

# Name of temporary requirements file
REQ_FILE="requirements-check-uv-lock-vulnerabilities.txt"

# Define cleanup function
cleanup() {
    if [[ -f "$REQ_FILE" ]]; then
        rm -f "$REQ_FILE"
    fi
}

# Ensure cleanup runs on script exit, error, or interrupt
trap cleanup EXIT

# Create a temporary requirements file
uv export --format=requirements-txt > "$REQ_FILE"

# Remove -e . if it exists
if [[ -f "$REQ_FILE" ]]; then
    sed -i '/^-e \.$/d' "$REQ_FILE"
fi

# Run pip-audit
uvx pip-audit -r "$REQ_FILE" --progress-spinner on
