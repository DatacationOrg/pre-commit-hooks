import subprocess
import sys


def check_vulnerabilities() -> int:
    result = subprocess.run(["uv", "audit", "--frozen"])
    return result.returncode


def main():
    sys.exit(check_vulnerabilities())


if __name__ == "__main__":
    main()
