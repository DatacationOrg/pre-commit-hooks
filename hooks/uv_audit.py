import subprocess
import sys


def run_uv_audit() -> int:
    """Run uv audit and return the exit code."""
    result = subprocess.run(["uv", "audit"], check=False)
    return result.returncode


def main():
    sys.exit(run_uv_audit())


if __name__ == "__main__":
    main()
