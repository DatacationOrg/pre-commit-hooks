import os
import sys
import time

from hooks.check_uv_lock_vulnerabilities import check_vulnerabilities

TIMESTAMP_FILE = ".git/.pre-commit-check-uv-lock-vulnerabilities-daily-last-run"
if len(sys.argv) > 1:
    try:
        INTERVAL_HOURS = int(sys.argv[1])
    except ValueError:
        print(
            f"Invalid interval: '{sys.argv[1]}'. Please provide the interval in hours as an integer.",
            file=sys.stderr,
        )
        sys.exit(1)
else:
    INTERVAL_HOURS = 24
MIN_INTERVAL = INTERVAL_HOURS * 60 * 60


def should_run():
    if os.path.isfile(TIMESTAMP_FILE):
        try:
            with open(TIMESTAMP_FILE, "r") as f:
                last_run = int(f.read().strip())
        except ValueError:
            print(
                f"Invalid timestamp in {TIMESTAMP_FILE}. Re-running the vulnerability scan.",
                file=sys.stderr,
            )
            last_run = 0
        now = int(time.time())
        if now - last_run < MIN_INTERVAL:
            print(
                f"Skipping uv.lock vulnerability scan (already ran successfully in the last {INTERVAL_HOURS} hours)"
            )
            return False
    return True


def update_timestamp():
    with open(TIMESTAMP_FILE, "w") as f:
        f.write(str(int(time.time())))


def main():
    if should_run():
        ret = check_vulnerabilities()
        if ret == 0:
            update_timestamp()
        sys.exit(ret)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
