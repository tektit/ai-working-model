"""Keeps `AGENTS.md` and the principle docs from drifting apart.

Every `##` heading in the three principle docs is one principle, and
`AGENTS.md` carries exactly one line per principle, linking that
heading by its GitHub anchor. This module checks that mapping both
ways: each heading is linked exactly once, and each anchored link to a
principle doc lands on a heading.
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

PRINCIPLE_FILES = tuple(
    Path("docs/principles") / name
    for name in ("engineering.md", "ai-working-process.md", "context-economy.md")
)
AGENTS_MD = Path("AGENTS.md")

_LINK_RE = re.compile(r"\[[^\]\n]*\]\(([^)\s]+)\)")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
# GitHub slugs the rendered text; these would be slugged from the raw
# source and silently get the wrong anchor.
_UNSUPPORTED_MARKUP = (("_", "underscore"), ("](", "inline link"))


@dataclass(frozen=True)
class AnchoredLink:
    line_number: int
    file: Path
    anchor: str


def github_slug(heading: str) -> str:
    """The anchor GitHub generates for a heading: lowercased, every
    character but word characters, hyphens and spaces dropped, spaces
    turned into hyphens."""
    kept = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return kept.replace(" ", "-")


def principle_headings(text: str) -> list[str]:
    """The `##` headings of a markdown text, outside code fences and
    HTML comments."""
    headings: list[str] = []
    in_fence = False
    for line in _HTML_COMMENT_RE.sub("", text).splitlines():
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and line.startswith("## "):
            headings.append(line[3:].strip())
    return headings


def anchored_principle_links(tree_root: Path) -> list[AnchoredLink]:
    """Every link in `AGENTS.md` to a principle doc that carries an
    anchor, with the target normalized relative to `tree_root`."""
    agents_md = tree_root / AGENTS_MD
    links: list[AnchoredLink] = []
    text = agents_md.read_text(encoding="utf-8")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in _LINK_RE.finditer(line):
            target, _, anchor = match.group(1).partition("#")
            if not anchor or not target:
                continue
            resolved = (agents_md.parent / target).resolve()
            for principle_file in PRINCIPLE_FILES:
                if resolved == (tree_root / principle_file).resolve():
                    links.append(AnchoredLink(line_number, principle_file, anchor))
    return links


def check_principle_links(tree_root: Path) -> list[str]:
    if not (tree_root / AGENTS_MD).is_file():
        return [f"{AGENTS_MD}: missing"]

    problems: list[str] = []
    headings: dict[tuple[Path, str], str] = {}
    for principle_file in PRINCIPLE_FILES:
        path = tree_root / principle_file
        if not path.is_file():
            problems.append(f"{principle_file.as_posix()}: missing")
            continue
        for heading in principle_headings(path.read_text(encoding="utf-8")):
            unsupported = [
                name for token, name in _UNSUPPORTED_MARKUP if token in heading
            ]
            if unsupported:
                problems.append(
                    f"{principle_file.as_posix()}: heading {heading!r} uses unsupported "
                    f"markup ({', '.join(unsupported)}); its anchor cannot "
                    "be computed reliably"
                )
                continue
            key = (principle_file, github_slug(heading))
            if key in headings:
                problems.append(
                    f"{principle_file.as_posix()}: heading {heading!r} has duplicate "
                    f"anchor #{key[1]} (also {headings[key]!r}); rename one"
                )
                continue
            headings[key] = heading

    linked_at: dict[tuple[Path, str], list[int]] = defaultdict(list)
    for link in anchored_principle_links(tree_root):
        key = (link.file, link.anchor)
        if key not in headings:
            problems.append(
                f"{AGENTS_MD}:{link.line_number}: link to "
                f"{link.file}#{link.anchor} matches no heading"
            )
            continue
        linked_at[key].append(link.line_number)

    for (principle_file, slug), heading in headings.items():
        lines = linked_at.get((principle_file, slug), [])
        if not lines:
            problems.append(
                f"{AGENTS_MD}: principle {heading!r} in {principle_file.as_posix()} "
                f"is not linked (expected a link to {principle_file.as_posix()}#{slug})"
            )
        elif len(lines) > 1:
            where = ", ".join(str(n) for n in lines)
            problems.append(
                f"{AGENTS_MD}:{where}: principle {heading!r} in "
                f"{principle_file.as_posix()} is linked {len(lines)} times; link it once"
            )
    return problems
