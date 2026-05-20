import subprocess
import sys
import tomllib


def check_vulnerabilities() -> int:
    try:
        with open("pyproject.toml", "rb") as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        config = {}

    # Extract ignore list from [tool.uv-audit] (default to empty)
    audit_config = config.get("tool", {}).get("uv-audit", {})
    ignore_vuln_list = audit_config.get("ignore", [])

    # Build uv audit arguments
    args = ["uv", "audit", "--frozen"]

    # Add ignore flags if any
    for vuln in ignore_vuln_list:
        args.extend(["--ignore", vuln])

    # Run uv audit
    result = subprocess.run(args)
    return result.returncode


def main():
    sys.exit(check_vulnerabilities())


if __name__ == "__main__":
    main()
