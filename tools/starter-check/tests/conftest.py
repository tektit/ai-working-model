from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ERROR_PRIVILEGE_NOT_HELD = 1314


def make_dir_link(link: Path, target: Path) -> str:
    """Makes `link` point at the directory `target`: a symlink when the
    account may create one, else (Windows only, error 1314: the account
    lacks the "Create symbolic links" right) a directory junction.
    Returns "symlink" or "junction" so callers know which they got."""
    try:
        link.symlink_to(target, target_is_directory=True)
        return "symlink"
    except OSError as error:
        if sys.platform != "win32" or error.winerror != ERROR_PRIVILEGE_NOT_HELD:
            raise
    subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        check=True,
        capture_output=True,
    )
    return "junction"


def _can_create_symlinks() -> bool:
    with tempfile.TemporaryDirectory() as tmp:
        try:
            (Path(tmp) / "link").symlink_to(Path(tmp), target_is_directory=True)
        except OSError:
            return False
    return True


CAN_CREATE_SYMLINKS = _can_create_symlinks()
needs_real_symlink = pytest.mark.skipif(
    not CAN_CREATE_SYMLINKS,
    reason='account lacks the Windows "Create symbolic links" right '
    "(error 1314); this test needs a real symlink, not a junction",
)


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def repo_root(tmp_path: Path) -> Path:
    """A synthetic repo root: `.git` marker plus a minimal, VALID
    `starter/` tree — a copy of it should pass every check untouched.
    Tests mutate individual files to provoke one failure at a time.
    """
    root = tmp_path / "repo"
    starter = root / "starter"
    (starter / "docs" / "design").mkdir(parents=True)
    (starter / "docs" / "principles").mkdir(parents=True)
    (starter / ".claude" / "agents").mkdir(parents=True)
    (starter / ".claude" / "skills" / "architect").mkdir(parents=True)

    (starter / "AGENTS.md").write_text(
        "# Agents\n\nSee [docs/architecture.md](docs/architecture.md) and "
        "[backlog.md](backlog.md).\n\n"
        "- [Fail early](docs/principles/engineering.md#fail-early).\n"
        "- [Roles](docs/principles/ai-working-process.md#roles).\n"
        "- [Read less](docs/principles/context-economy.md#read-less).\n", encoding="utf-8"
    )
    (starter / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    (starter / "backlog.md").write_text("# Backlog\n", encoding="utf-8")
    (starter / "docs" / "architecture.md").write_text(
        "# Architecture\n\nSee [../backlog.md](../backlog.md).\n", encoding="utf-8"
    )
    (starter / "docs" / "design" / "README.md").write_text("# Design docs\n", encoding="utf-8")
    (starter / "docs" / "principles" / "engineering.md").write_text(
        "# Engineering\n\n## Fail early\n", encoding="utf-8"
    )
    (starter / "docs" / "principles" / "ai-working-process.md").write_text(
        "# AI working process\n\n## Roles\n", encoding="utf-8"
    )
    (starter / "docs" / "principles" / "context-economy.md").write_text(
        "# Context economy\n\n## Read less\n", encoding="utf-8"
    )
    (starter / ".claude" / "agents" / "builder.md").write_text("builder\n", encoding="utf-8")
    (starter / ".claude" / "skills" / "architect" / "SKILL.md").write_text(
        "skill\n", encoding="utf-8"
    )

    root.mkdir(exist_ok=True)
    _git(root, "init", "-q")

    make_dir_link(root / ".claude", starter / ".claude")

    return root
