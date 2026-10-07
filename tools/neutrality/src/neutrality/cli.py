from __future__ import annotations

import argparse
import sys
from pathlib import Path

from neutrality.denylist import DenylistMissing, load_denylist
from neutrality.scanner import scan

DENYLIST_FILENAME = ".neutrality-denylist"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="neutrality-check",
        description=(
            "Scans git-tracked and staged files for client, customer or "
            "private-project identifiers listed in .neutrality-denylist."
        ),
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path("."),
        help="Repository root to scan (default: current directory).",
    )
    args = parser.parse_args(argv)
    repo = args.repo.resolve()

    try:
        denylist = load_denylist(repo / DENYLIST_FILENAME)
    except DenylistMissing as exc:
        print(
            f"neutrality-check: denylist file missing, expected at {exc} "
            "— a missing denylist is a failure, not a skip",
            file=sys.stderr,
        )
        return 2

    hits = scan(repo, denylist)
    for hit in hits:
        print(f"{hit.path}:{hit.line_number}: {hit.pattern}")

    return 1 if hits else 0


if __name__ == "__main__":
    raise SystemExit(main())
