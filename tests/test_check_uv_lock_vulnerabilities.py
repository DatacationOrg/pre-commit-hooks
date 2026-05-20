import shutil
from pathlib import Path

from hooks.check_uv_lock_vulnerabilities import check_vulnerabilities

_DATA = Path(__file__).parent / "data"


def _setup(tmp_path: Path, fixture: str) -> Path:
    src = _DATA / fixture
    shutil.copy(src / "pyproject.toml", tmp_path / "pyproject.toml")
    shutil.copy(src / "uv.lock", tmp_path / "uv.lock")
    return tmp_path


def test_detects_vulnerabilities(tmp_path, monkeypatch):
    monkeypatch.chdir(_setup(tmp_path, "vulnerable"))
    assert check_vulnerabilities() == 1


def test_ignore_until_fixed_suppresses_unfixed_vulnerability(tmp_path, monkeypatch):
    # PYSEC-2022-42969 has no fix available; ignore-until-fixed silences it
    monkeypatch.chdir(_setup(tmp_path, "unfixed_ignored"))
    assert check_vulnerabilities() == 0


def test_no_vulnerabilities(tmp_path, monkeypatch):
    monkeypatch.chdir(_setup(tmp_path, "no_vulnerabilities"))
    assert check_vulnerabilities() == 0
