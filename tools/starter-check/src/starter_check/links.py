"""Finds relative markdown links and `@path` imports that don't resolve.

Operates on a plain directory tree (a copy of `starter/`, or any other
tree) rather than git — the whole point is to check what a *copy*, with
no git history of its own, looks like from the inside.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# [text](target) — target is group 1.
_LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\n]+)\)")

# @path/to/file.md — never preceded by a non-space character, so it
# doesn't match an email address or a shell `"$@"`. Must look path-shaped
# (contains "/" or ".") so a stray "@word" in prose isn't flagged.
_IMPORT_RE = re.compile(r"(?<!\S)@([A-Za-z0-9][A-Za-z0-9_./-]*)")

_URL_SCHEMES = ("http://", "https://", "mailto:", "tel:")


@dataclass(frozen=True)
class BrokenReference:
    file: Path
    line_number: int
    kind: str  # "link" or "import"
    target: str


def _is_external(target: str) -> bool:
    return target.startswith(_URL_SCHEMES) or target.startswith("#")


def _resolve(tree_root: Path, file: Path, target: str) -> Path:
    target = target.split("#", 1)[0].strip()
    if target.startswith("/"):
        return tree_root / target.lstrip("/")
    return file.parent / target


def find_broken_references(tree_root: Path) -> list[BrokenReference]:
    """Every relative link/import under `tree_root`'s `*.md` files whose
    target does not exist inside `tree_root`."""
    problems: list[BrokenReference] = []
    for md_file in sorted(tree_root.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in _LINK_RE.finditer(line):
                target = match.group(1).strip()
                if not target or _is_external(target):
                    continue
                if not _resolve(tree_root, md_file, target).exists():
                    problems.append(
                        BrokenReference(md_file, line_number, "link", target)
                    )
            for match in _IMPORT_RE.finditer(line):
                target = match.group(1).strip()
                if "/" not in target and "." not in target:
                    continue
                if not _resolve(tree_root, md_file, target).exists():
                    problems.append(
                        BrokenReference(md_file, line_number, "import", target)
                    )
    return problems
