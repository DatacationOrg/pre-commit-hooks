import os
import subprocess
import sys
import tempfile
import tomllib

from pip_audit._cli import audit

try:
    with open("pyproject.toml", "rb") as f:
        config = tomllib.load(f)
except FileNotFoundError:
    config = {}
# Extract ignore list (default to empty)
ignore_list = config.get("tool", {}).get("pip-audit", {}).get("ignore-vuln", [])


def check_vulnerabilities() -> int | str | None:
    # Create a temporary requirements file
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".txt", delete=False
    ) as req_file:
        req_file_path = req_file.name
        try:
            # Export requirements using uv
            subprocess.run(
                [
                    "uv",
                    "export",
                    "--format=requirements-txt",
                    "--all-groups",
                    "--locked",
                    "--no-emit-local",
                ],
                stdout=req_file,
                check=True,
            )
            req_file.flush()

            # Build pip-audit arguments
            args = [
                "pip-audit",
                "-r",
                req_file_path,
                "--disable-pip",
                "--require-hashes",
            ]
            # Add ignore-vuln flags if any
            for vuln in ignore_list:
                args.extend(["--ignore-vuln", vuln])

            # Run pip-audit
            sys.argv = args
            try:
                audit()
            except SystemExit as e:
                return e.code
            return 0
        finally:
            if os.path.exists(req_file_path):
                try:
                    os.remove(req_file_path)
                except PermissionError:
                    pass
                    # Leak temp file on Windows


def main():
    sys.exit(check_vulnerabilities())


if __name__ == "__main__":
    main()
