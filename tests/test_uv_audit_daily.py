"""Tests for hooks/uv_audit_daily.py"""

import importlib
import os
import sys
import time
from unittest.mock import MagicMock, mock_open, patch

import pytest


def _reload_module(interval_hours=None):
    """Helper that reloads uv_audit_daily with a given sys.argv."""
    argv = ["uv-audit-daily"]
    if interval_hours is not None:
        argv.append(str(interval_hours))
    with patch.object(sys, "argv", argv):
        import hooks.uv_audit_daily as mod

        importlib.reload(mod)
        return mod


def test_should_run_no_timestamp_file():
    """should_run returns True when the timestamp file does not exist."""
    mod = _reload_module()
    with patch("os.path.isfile", return_value=False):
        assert mod.should_run() is True


def test_should_run_stale_timestamp():
    """should_run returns True when the last run was longer ago than the interval."""
    mod = _reload_module(interval_hours=24)
    old_timestamp = int(time.time()) - (25 * 60 * 60)  # 25 hours ago
    with patch("os.path.isfile", return_value=True), patch(
        "builtins.open", mock_open(read_data=str(old_timestamp))
    ):
        assert mod.should_run() is True


def test_should_run_recent_timestamp(capsys):
    """should_run returns False (and prints a skip message) when within the interval."""
    mod = _reload_module(interval_hours=24)
    recent_timestamp = int(time.time()) - (1 * 60 * 60)  # 1 hour ago
    with patch("os.path.isfile", return_value=True), patch(
        "builtins.open", mock_open(read_data=str(recent_timestamp))
    ):
        result = mod.should_run()
    assert result is False
    captured = capsys.readouterr()
    assert "Skipping" in captured.out


def test_should_run_invalid_timestamp(capsys):
    """should_run treats an invalid timestamp as 0 and returns True."""
    mod = _reload_module()
    with patch("os.path.isfile", return_value=True), patch(
        "builtins.open", mock_open(read_data="not-a-number")
    ):
        result = mod.should_run()
    assert result is True
    captured = capsys.readouterr()
    assert "Invalid timestamp" in captured.err


def test_main_runs_audit_and_updates_timestamp():
    """main() calls uv audit and writes the timestamp on success."""
    mod = _reload_module()
    with patch.object(mod, "should_run", return_value=True), patch.object(
        mod, "run_uv_audit", return_value=0
    ), patch.object(mod, "update_timestamp") as mock_ts:
        with pytest.raises(SystemExit) as exc_info:
            mod.main()
        assert exc_info.value.code == 0
        mock_ts.assert_called_once()


def test_main_skips_timestamp_on_failure():
    """main() does NOT update the timestamp when uv audit fails."""
    mod = _reload_module()
    with patch.object(mod, "should_run", return_value=True), patch.object(
        mod, "run_uv_audit", return_value=1
    ), patch.object(mod, "update_timestamp") as mock_ts:
        with pytest.raises(SystemExit) as exc_info:
            mod.main()
        assert exc_info.value.code == 1
        mock_ts.assert_not_called()


def test_main_skips_when_recent(capsys):
    """main() exits 0 without running audit when should_run returns False."""
    mod = _reload_module()
    with patch.object(mod, "should_run", return_value=False), patch(
        "hooks.uv_audit.run_uv_audit"
    ) as mock_audit:
        with pytest.raises(SystemExit) as exc_info:
            mod.main()
        assert exc_info.value.code == 0
        mock_audit.assert_not_called()


def test_invalid_interval_exits(capsys):
    """Passing a non-integer interval argument exits with code 1."""
    with patch.object(sys, "argv", ["uv-audit-daily", "not-a-number"]):
        with pytest.raises(SystemExit) as exc_info:
            import hooks.uv_audit_daily as mod

            importlib.reload(mod)
    assert exc_info.value.code == 1
