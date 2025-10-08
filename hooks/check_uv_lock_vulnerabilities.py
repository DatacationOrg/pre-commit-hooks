import os
import subprocess
import sys
import tempfile
from pip_audit._cli import audit


def check_vulnerabilities() -> int | str | None:
    # Create a temporary requirements file
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".txt", delete=False
    ) as req_file:
        req_file_path = req_file.name
        try:
            # Export requirements using uv
            subprocess.run(
                ["uv", "export", "--format=requirements-txt"],
                stdout=req_file,
                check=True,
            )
            req_file.flush()

            # Remove '-e .' if it exists
            with open(req_file_path, "r") as f:
                lines = f.readlines()
            with open(req_file_path, "w") as f:
                for line in lines:
                    if line.strip() != "-e .":
                        f.write(line)

            # Run pip-audit
            sys.argv = [
                "pip-audit",
                "-r",
                req_file_path,
                "--disable-pip",
                "--require-hashes",
            ]
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
