# pre-commit-hooks

Custom pre-commit hooks for Datacation to check Python dependency vulnerabilities managed by [uv](https://github.com/astral-sh/uv).

## Hooks

### `check-uv-lock-vulnerabilities`

Checks your `uv.lock` for vulnerabilities using [`uv audit`](https://docs.astral.sh/uv/reference/cli/#uv-audit).

- **Runs:** Every pre-commit
- **Script:** [`hooks/check_uv_lock_vulnerabilities.py`](hooks/check_uv_lock_vulnerabilities.py)

### `check-uv-lock-vulnerabilities-daily`

Checks your `uv.lock` for vulnerabilities, but only if the last successful run was more than 24 hours ago (configurable).

- **Runs:** Every pre-commit, but skips if run in the last interval
- **Script:** [`hooks/check_uv_lock_vulnerabilities_daily.py`](hooks/check_uv_lock_vulnerabilities_daily.py)
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

## Dependency Cooldown (Supply Chain Attack Prevention)

To prevent supply chain attacks, this hook respects the `exclude-newer` setting in your `pyproject.toml`. This ensures that newly published packages are subject to a cooldown period before they can be resolved, giving the community time to identify malicious releases.

Add the following to your `pyproject.toml`:

```toml
[tool.uv]
exclude-newer = "P7D"
```

This enforces a 7-day cooldown on dependency resolution, meaning only packages published more than 7 days ago will be considered. The `uv audit` command respects this setting via `--frozen`, so developers will not be blocked from committing due to vulnerability fixes that are still within the cooldown period.

## Ignoring Vulnerabilities

To ignore specific vulnerability advisories, add the following to your `pyproject.toml`:

```toml
[tool.uv-audit]
ignore = ["GHSA-xxxx-xxxx-xxxx", "PYSEC-2024-xxxx"]
```
