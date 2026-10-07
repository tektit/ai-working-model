from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """An initialized, empty git repo with no ambient identity needed.

    Tests only ADD to the index (`git add`) and never commit, so no
    author/committer identity is ever required.
    """
    _git(tmp_path, "init", "-q")
    return tmp_path


def write_and_stage(repo: Path, relative_path: str, content: str) -> None:
    path = repo / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    _git(repo, "add", relative_path)


def write_denylist(repo: Path, *lines: str) -> Path:
    path = repo / ".neutrality-denylist"
    path.write_text("\n".join(lines) + "\n")
    return path
