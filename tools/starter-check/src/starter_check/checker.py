"""Verifies that `starter/` is a self-contained tree a user can copy
into a brand new repo.

Five checks run against a plain COPY of `starter/`'s contents in a
temp dir (never the real `starter/` in place, and never this repo's
own git history):

1. Every relative markdown link and `@path` import resolves inside the
   copy — nothing points at a file this repo has but the copy doesn't.
2. Nothing in the copy references this repo by name or the `starter/`
   directory itself — a copied file must read as belonging to the NEW
   repo, with no back-reference to where it came from.
3. `CLAUDE.md` is exactly `@AGENTS.md`.
4. `AGENTS.md` links every `##` heading of the three principle docs
   exactly once, and every anchored link to them lands on a heading.

5. The copy carries no license file (any name starting `LICENSE`,
   `LICENCE`, `COPYING` or `NOTICE`) and no copyright line or SPDX tag
   — whatever is in it lands in the new repo beside, or in place of,
   that repo's own license.

A sixth check runs against the real repo, not the copy: the root
`.claude` symlink resolves to a real directory inside `starter/`.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from starter_check.links import find_broken_references
from starter_check.principle_links import check_principle_links

FORBIDDEN_TOKENS = ("ai-working-model", "starter/")
CLAUDE_MD_EXPECTED = "@AGENTS.md"
LICENSE_FILE_PREFIXES = ("license", "licence", "copying", "notice")
LICENSE_LINE_PATTERN = re.compile(
    r"\bcopyright\s*(\(c\)|©)?\s*\d{4}|©\s*\d{4}|SPDX-License-Identifier",
    re.IGNORECASE,
)
ROOT_SYMLINKS = (Path(".claude"),)


def find_repo_root(start: Path) -> Path:
    """Walks upward from `start` for the first directory holding both a
    `starter/` subdirectory and `.git` — this repo's root."""
    start = start.resolve()
    candidates = [start] if start.is_dir() else [start.parent]
    candidates += list(candidates[0].parents)
    for candidate in candidates:
        if (candidate / "starter").is_dir() and (candidate / ".git").exists():
            return candidate
    raise RuntimeError(f"could not locate the repo root above {start}")


def copy_starter(starter_dir: Path, dest: Path) -> None:
    """Copies `starter/`'s CONTENTS into `dest`, exactly as a user would
    when seeding a new repo — `dest` then IS the new repo's root."""
    for item in sorted(starter_dir.iterdir()):
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, symlinks=True)
        else:
            shutil.copy2(item, target)


def git_init(dest: Path) -> None:
    subprocess.run(
        ["git", "init", "-q"], cwd=dest, check=True, capture_output=True
    )


def check_links(tree_root: Path) -> list[str]:
    return [
        f"{ref.file.relative_to(tree_root)}:{ref.line_number}: "
        f"broken {ref.kind} -> {ref.target}"
        for ref in find_broken_references(tree_root)
    ]


def check_no_backreferences(tree_root: Path) -> list[str]:
    problems: list[str] = []
    for path in sorted(tree_root.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(tree_root)
        for line_number, line in enumerate(text.splitlines(), start=1):
            for token in FORBIDDEN_TOKENS:
                if token in line:
                    problems.append(
                        f"{rel}:{line_number}: references {token!r}: "
                        f"{line.strip()}"
                    )
    return problems


def check_claude_md(tree_root: Path) -> list[str]:
    claude_md = tree_root / "CLAUDE.md"
    if not claude_md.exists():
        return ["CLAUDE.md: missing"]
    content = claude_md.read_text(encoding="utf-8").strip()
    if content != CLAUDE_MD_EXPECTED:
        return [
            f"CLAUDE.md: expected exactly {CLAUDE_MD_EXPECTED!r}, "
            f"got {content!r}"
        ]
    return []


def check_no_license_terms(tree_root: Path) -> list[str]:
    problems: list[str] = []
    for path in sorted(tree_root.rglob("*")):
        rel = path.relative_to(tree_root)
        if not path.is_file() or ".git" in rel.parts:
            continue
        if path.name.lower().startswith(LICENSE_FILE_PREFIXES):
            problems.append(f"{rel}: license file does not belong in the starter")
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            if LICENSE_LINE_PATTERN.search(line):
                problems.append(
                    f"{rel}:{line_number}: copyright or license tag: "
                    f"{line.strip()}"
                )
    return problems


def check_root_symlinks(repo_root: Path, starter_dir: Path) -> list[str]:
    problems: list[str] = []
    starter_real = starter_dir.resolve()
    for rel in ROOT_SYMLINKS:
        link = repo_root / rel
        if not link.is_symlink():
            problems.append(f"{rel}: not a symlink")
            continue
        if not link.exists():
            problems.append(f"{rel}: symlink is broken (dangling)")
            continue
        resolved = link.resolve()
        try:
            resolved.relative_to(starter_real)
        except ValueError:
            problems.append(f"{rel}: resolves outside starter/ ({resolved})")
    return problems


def run_all(repo_root: Path) -> list[str]:
    starter_dir = repo_root / "starter"
    problems: list[str] = []
    with tempfile.TemporaryDirectory(prefix="starter-check-") as tmp:
        dest = Path(tmp)
        copy_starter(starter_dir, dest)
        git_init(dest)
        problems += check_links(dest)
        problems += check_no_backreferences(dest)
        problems += check_claude_md(dest)
        problems += check_principle_links(dest)
        problems += check_no_license_terms(dest)
    problems += check_root_symlinks(repo_root, starter_dir)
    return problems
