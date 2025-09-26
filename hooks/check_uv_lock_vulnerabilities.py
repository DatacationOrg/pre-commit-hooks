import subprocess
import tempfile
import os
import sys

def main():
    # Create a temporary requirements file
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as req_file:
        req_file_path = req_file.name
        try:
            # Export requirements using uv
            subprocess.run(
                ["uv", "export", "--format=requirements-txt"],
                stdout=req_file,
                check=True
            )
            req_file.flush()

            # Remove '-e .' if it exists
            with open(req_file_path, 'r') as f:
                lines = f.readlines()
            with open(req_file_path, 'w') as f:
                for line in lines:
                    if line.strip() != '-e .':
                        f.write(line)

            # Run pip-audit
            subprocess.run(
                ["uvx", "pip-audit", "-r", req_file_path, "--progress-spinner", "on"],
                check=True
            )
        finally:
            if os.path.exists(req_file_path):
                os.remove(req_file_path)

if __name__ == "__main__":
    sys.exit(main())
