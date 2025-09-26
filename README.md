# pre-commit-hooks

Custom pre-commit hooks for Datacation to check Python dependency vulnerabilities managed by [uv](https://github.com/astral-sh/uv).

## Hooks

### `check-uv-lock-vulnerabilities`

Checks your `uv.lock` for vulnerabilities using [`pip-audit`](https://github.com/pypa/pip-audit).

- **Runs:** Every pre-commit
- **Script:** [`hooks/check-uv-lock-vulnerabilities.py`](hooks/check-uv-lock-vulnerabilities.py)

### `check-uv-lock-vulnerabilities-daily`

Checks your `uv.lock` for vulnerabilities, but only if the last successful run was more than 24 hours ago (configurable).

- **Runs:** Every pre-commit, but skips if run in the last interval
- **Script:** [`hooks/check-uv-lock-vulnerabilities-daily.py`](hooks/check-uv-lock-vulnerabilities-daily.py)
- **Interval:** Default 24 hours (can be set via argument)

## Usage

Add this repo to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/datacation/pre-commit-hooks
  rev: <commit-or-tag>
  hooks:
    - id: check-uv-lock-vulnerabilities
    # or
    - id: check-uv-lock-vulnerabilities-daily
      args: ["24"] # change this number to adjust the interval in hours, ex. weekly: 168
```
