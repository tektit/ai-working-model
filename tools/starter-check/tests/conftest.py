from __future__ import annotations

import subprocess
from pathlib import Path

import pytest


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
        "- [Read less](docs/principles/context-economy.md#read-less).\n"
    )
    (starter / "CLAUDE.md").write_text("@AGENTS.md\n")
    (starter / "backlog.md").write_text("# Backlog\n")
    (starter / "docs" / "architecture.md").write_text(
        "# Architecture\n\nSee [../backlog.md](../backlog.md).\n"
    )
    (starter / "docs" / "design" / "README.md").write_text("# Design docs\n")
    (starter / "docs" / "principles" / "engineering.md").write_text(
        "# Engineering\n\n## Fail early\n"
    )
    (starter / "docs" / "principles" / "ai-working-process.md").write_text(
        "# AI working process\n\n## Roles\n"
    )
    (starter / "docs" / "principles" / "context-economy.md").write_text(
        "# Context economy\n\n## Read less\n"
    )
    (starter / ".claude" / "agents" / "builder.md").write_text("builder\n")
    (starter / ".claude" / "skills" / "architect" / "SKILL.md").write_text(
        "skill\n"
    )

    root.mkdir(exist_ok=True)
    _git(root, "init", "-q")

    (root / ".claude").symlink_to(starter / ".claude", target_is_directory=True)

    return root
