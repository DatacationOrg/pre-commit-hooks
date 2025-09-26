#!/bin/sh
set -eu

REQ_FILE="requirements-check-uv-lock-vulnerabilities.txt"

cleanup() {
    if [ -f "$REQ_FILE" ]; then
        rm -f "$REQ_FILE"
    fi
}

trap cleanup EXIT

uv export --format=requirements-txt > "$REQ_FILE"

if [ -f "$REQ_FILE" ]; then
    # Remove lines exactly matching "-e ."
    sed -i '/^-e \.$/d' "$REQ_FILE"
fi

uvx pip-audit -r "$REQ_FILE" --progress-spinner on
