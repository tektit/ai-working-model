"""Parses the gitignored `.neutrality-denylist` file.

One case-insensitive regex per line; `#` starts a comment; blank lines
are skipped. A missing denylist is a failure, not a skip — an empty
denylist would silently disable the whole check.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DenylistEntry:
    pattern: str
    regex: re.Pattern[str]


class DenylistMissing(Exception):
    """Raised when the denylist file does not exist."""


def load_denylist(path: Path) -> list[DenylistEntry]:
    if not path.is_file():
        raise DenylistMissing(str(path))

    entries: list[DenylistEntry] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.append(
            DenylistEntry(pattern=stripped, regex=re.compile(stripped, re.IGNORECASE))
        )
    return entries
