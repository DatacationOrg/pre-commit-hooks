"""Tests for hooks/uv_audit.py"""

import subprocess
from unittest.mock import MagicMock, patch

import pytest

from hooks.uv_audit import main, run_uv_audit


def test_run_uv_audit_success():
    """run_uv_audit returns 0 when uv audit exits cleanly."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    with patch("subprocess.run", return_value=mock_result) as mock_run:
        assert run_uv_audit() == 0
        mock_run.assert_called_once_with(["uv", "audit"], check=False)


def test_run_uv_audit_vulnerability_found():
    """run_uv_audit returns non-zero when uv audit detects vulnerabilities."""
    mock_result = MagicMock()
    mock_result.returncode = 1
    with patch("subprocess.run", return_value=mock_result):
        assert run_uv_audit() == 1


def test_main_exits_with_zero(monkeypatch):
    """main() calls sys.exit with the return code from run_uv_audit."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    with patch("subprocess.run", return_value=mock_result):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0


def test_main_exits_with_nonzero(monkeypatch):
    """main() propagates a non-zero exit code from run_uv_audit."""
    mock_result = MagicMock()
    mock_result.returncode = 2
    with patch("subprocess.run", return_value=mock_result):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 2
