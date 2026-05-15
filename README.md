# pre-commit-hooks

Custom pre-commit hooks for Datacation to check Python dependency vulnerabilities managed by [uv](https://github.com/astral-sh/uv).

## Hooks

### `uv-audit` ✨

Checks your `uv.lock` for vulnerabilities using [`uv audit`](https://docs.astral.sh/uv/reference/cli/#uv-audit) (introduced in uv 0.11.0).

- **Runs:** Every pre-commit
- **Requires:** uv ≥ 0.11.0
- **Script:** [`hooks/uv_audit.py`](hooks/uv_audit.py)

### `uv-audit-daily` ✨

Checks your `uv.lock` for vulnerabilities using `uv audit`, but only if the last successful run was more than 24 hours ago (configurable).

- **Runs:** Every pre-commit, but skips if run in the last interval
- **Requires:** uv ≥ 0.11.0
- **Script:** [`hooks/uv_audit_daily.py`](hooks/uv_audit_daily.py)
- **Interval:** Default 24 hours (can be set via argument)

### `check-uv-lock-vulnerabilities` *(deprecated)*

Checks your `uv.lock` for vulnerabilities using [`pip-audit`](https://github.com/pypa/pip-audit).
Prefer the `uv-audit` hook for new projects.

- **Runs:** Every pre-commit
- **Script:** [`hooks/check_uv_lock_vulnerabilities.py`](hooks/check_uv_lock_vulnerabilities.py)

### `check-uv-lock-vulnerabilities-daily` *(deprecated)*

Checks your `uv.lock` for vulnerabilities, but only if the last successful run was more than 24 hours ago (configurable).
Prefer the `uv-audit-daily` hook for new projects.

- **Runs:** Every pre-commit, but skips if run in the last interval
- **Script:** [`hooks/check_uv_lock_vulnerabilities_daily.py`](hooks/check_uv_lock_vulnerabilities_daily.py)
- **Interval:** Default 24 hours (can be set via argument)

## Usage

Add this repo to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/datacation/pre-commit-hooks
  rev: <commit-or-tag>
  hooks:
    - id: uv-audit
    # or (throttled — only runs if last successful run was more than N hours ago)
    - id: uv-audit-daily
      args: ["24"] # change this number to adjust the interval in hours, ex. weekly: 168
```

To ignore specific vulnerabilities, pass `--ignore` flags via `args`:

```yaml
    - id: uv-audit
      args: ["--ignore", "GHSA-xxxx-xxxx-xxxx"]
```

### Migration from `check-uv-lock-vulnerabilities`

If you were using the old `pip-audit`-based hooks, switch to the `uv audit`-based equivalents:

| Old hook | New hook |
|---|---|
| `check-uv-lock-vulnerabilities` | `uv-audit` |
| `check-uv-lock-vulnerabilities-daily` | `uv-audit-daily` |

The new hooks require **uv ≥ 0.11.0** and do not depend on `pip-audit`. Any `ignore-vuln` entries previously configured under `[tool.pip-audit]` in `pyproject.toml` should be passed as `--ignore` args in your `.pre-commit-config.yaml` instead.
