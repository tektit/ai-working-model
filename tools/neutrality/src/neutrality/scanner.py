"""Scans git-tracked and staged file content against a denylist.

File content is always read from the git INDEX (`git show :path`),
never the working tree — that is what will actually be committed, and
it is what a staged-but-not-yet-committed addition looks like before
any commit exists for it.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from neutrality.denylist import DenylistEntry


@dataclass(frozen=True)
class Hit:
    path: str
    line_number: int
    pattern: str
    line: str


def _git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def tracked_and_staged_files(repo: Path) -> list[str]:
    """The file set to scan: every tracked path plus every staged path.

    `git ls-files` already lists every path currently in the index,
    including newly staged additions, so the staged diff mostly
    overlaps it — the union is kept explicit because it is the
    contract, not because it changes the result in practice.
    """
    tracked = _git(repo, "ls-files").splitlines()
    staged = _git(
        repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR"
    ).splitlines()

    seen: dict[str, None] = {}
    for path in (*tracked, *staged):
        seen[path] = None
    return list(seen)


def read_indexed_content(repo: Path, path: str) -> str | None:
    """The path's content as staged in the index, or None if unreadable.

    Binary files decode-fail and are skipped rather than treated as a
    hit or a hard error.
    """
    result = subprocess.run(
        ["git", "-C", str(repo), "show", f":{path}"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        return result.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


def scan(repo: Path, denylist: list[DenylistEntry]) -> list[Hit]:
    hits: list[Hit] = []
    for path in tracked_and_staged_files(repo):
        content = read_indexed_content(repo, path)
        if content is None:
            continue
        for line_number, line in enumerate(content.splitlines(), start=1):
            for entry in denylist:
                if entry.regex.search(line):
                    hits.append(
                        Hit(
                            path=path,
                            line_number=line_number,
                            pattern=entry.pattern,
                            line=line,
                        )
                    )
    return hits
