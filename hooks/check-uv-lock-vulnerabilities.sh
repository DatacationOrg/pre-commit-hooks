#!/usr/bin/env bash
set -e

# Name of temporary requirements file
REQ_FILE="requirements-check-uv-lock-vulnerabilities.txt"

# Create a temporary requirements file
uv export --format=requirements-txt > "$REQ_FILE"

# Remove -e . if it exists
if [[ -f "$REQ_FILE" ]]; then
    sed -i '/^-e \.$/d' "$REQ_FILE"
fi

# Run pip-audit
uvx pip-audit -r "$REQ_FILE" --progress-spinner on

# Remove temporary requirements file
rm "$REQ_FILE"
