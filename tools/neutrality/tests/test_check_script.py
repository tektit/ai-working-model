"""Drives the real tools/neutrality/check.sh against a throwaway repo,
throwaway keys and a throwaway encrypted denylist."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest

CHECK_SH = Path(__file__).resolve().parents[1] / "check.sh"
KEY_ENV_VARS = (
    "SOPS_AGE_KEY",
    "SOPS_AGE_KEY_FILE",
    "SOPS_AGE_SSH_PRIVATE_KEY_FILE",
    "XDG_CONFIG_HOME",
)


@dataclass(frozen=True)
class Keys:
    home: Path
    ssh_recipient: str
    age_recipient: str
    age_secret: str


def _run(*args: str, **kwargs) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, capture_output=True, text=True, **kwargs)


@pytest.fixture(scope="session", autouse=True)
def required_tools() -> None:
    for tool in ("sops", "ssh-keygen", "age-keygen", "git", "uv"):
        if shutil.which(tool) is None:
            pytest.fail(f"{tool} is required on PATH to test check.sh")


@pytest.fixture
def keys(tmp_path: Path) -> Keys:
    home = tmp_path / "home"
    (home / ".ssh").mkdir(parents=True)
    key = home / ".ssh" / "id_ed25519"
    _run("ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-C", "", "-f", str(key))
    ssh_type, ssh_body, *_ = key.with_suffix(".pub").read_text().split()

    age_out = _run("age-keygen").stdout
    age_secret = next(l for l in age_out.splitlines() if l.startswith("AGE-SECRET-KEY-"))
    age_public = subprocess.run(
        ["age-keygen", "-y"], input=age_secret, check=True, capture_output=True, text=True
    ).stdout.strip()
    return Keys(home, f"{ssh_type} {ssh_body} test key", age_public, age_secret)


def _env(home: Path, **extra: str) -> dict[str, str]:
    env = {k: v for k, v in os.environ.items() if k not in KEY_ENV_VARS}
    env["HOME"] = str(home)
    env.update(extra)
    return env


@pytest.fixture
def project(tmp_path: Path, keys: Keys) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _run("git", "init", "-q", cwd=repo)
    (repo / ".sops.yaml").write_text(
        "creation_rules:\n"
        "  - path_regex: ^\\.neutrality-denylist\\.sops$\n"
        "    age:\n"
        f'      - "{keys.ssh_recipient}"\n'
        f"      - {keys.age_recipient}\n"
    )
    plaintext = tmp_path / "list.txt"
    plaintext.write_text("# sample\nacme\n")
    encrypted = _run(
        "sops", "encrypt", "--filename-override", ".neutrality-denylist.sops",
        str(plaintext),
        cwd=repo, env=_env(keys.home),
    ).stdout
    (repo / ".neutrality-denylist.sops").write_text(encrypted)
    _run("git", "add", ".", cwd=repo)
    return repo


def _check(repo: Path, home: Path, **extra_env: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["sh", str(CHECK_SH)], cwd=repo, env=_env(home, **extra_env),
        capture_output=True, text=True,
    )


def _stage(repo: Path, name: str, content: str) -> None:
    (repo / name).write_text(content)
    _run("git", "add", name, cwd=repo)


def test_clean_repo_exits_zero(project: Path, keys: Keys) -> None:
    _stage(project, "notes.md", "nothing sensitive\n")

    result = _check(project, keys.home)

    assert result.returncode == 0, result.stderr
    assert result.stdout == ""


def test_hit_exits_one_and_prints_path_line_pattern(project: Path, keys: Keys) -> None:
    _stage(project, "notes.md", "line one\nworking for Acme Corp\n")

    result = _check(project, keys.home)

    assert result.returncode == 1, result.stderr
    assert result.stdout.strip() == "notes.md:2: acme"


def test_no_key_fails(project: Path, tmp_path: Path) -> None:
    empty_home = tmp_path / "empty-home"
    empty_home.mkdir()

    result = _check(project, empty_home)

    assert result.returncode != 0
    assert result.stdout == ""


def test_ci_age_key_from_environment(project: Path, keys: Keys, tmp_path: Path) -> None:
    keyless_home = tmp_path / "keyless-home"
    keyless_home.mkdir()
    _stage(project, "notes.md", "nothing sensitive\n")

    result = _check(project, keyless_home, SOPS_AGE_KEY=keys.age_secret)

    assert result.returncode == 0, result.stderr
