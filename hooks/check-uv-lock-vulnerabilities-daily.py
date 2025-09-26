import os
import sys
import time
import subprocess

# File to track last run per repo
TIMESTAMP_FILE = ".git/.pre-commit-uv-lock-last-run"

# Usage: hooks/check-uv-lock-vulnerabilities-daily.py <interval_hours>
INTERVAL_HOURS = int(sys.argv[1]) if len(sys.argv) > 1 else 24  # default to 24 hours

# Convert hours to seconds
MIN_INTERVAL = INTERVAL_HOURS * 60 * 60

# Check last run
if os.path.isfile(TIMESTAMP_FILE):
    with open(TIMESTAMP_FILE, "r") as f:
        try:
            last_run = int(f.read().strip())
        except ValueError:
            last_run = 0
    now = int(time.time())
    diff = now - last_run
    if diff < MIN_INTERVAL:
        print(f"Skipping uv.lock vulnerability scan (already ran successfully in the last {INTERVAL_HOURS} hours)")
        sys.exit(0)

# Directory of this script
hook_dir = os.path.dirname(os.path.abspath(__file__))

# Run the original hook
subprocess.check_call(["uv", "run", os.path.join(hook_dir, "check-uv-lock-vulnerabilities.sh")])

# Update timestamp
with open(TIMESTAMP_FILE, "w") as f:
    f.write(str(int(time.time())))
