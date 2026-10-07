from __future__ import annotations

import argparse
import sys
from pathlib import Path

from starter_check.checker import find_repo_root, run_all


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="starter-check",
        description=(
            "Copies starter/ into a temp dir and verifies it is a "
            "self-contained tree: every relative markdown link and "
            "@import resolves inside the copy, nothing references this "
            "repo or starter/ by name, CLAUDE.md is exactly "
            "@AGENTS.md, AGENTS.md links every principle heading "
            "exactly once, and no license file, copyright line or SPDX "
            "tag is present. Also checks the root .claude symlink resolves."
        ),
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path("."),
        help="Anywhere inside this repo (default: current directory).",
    )
    args = parser.parse_args(argv)
    repo_root = find_repo_root(args.repo)

    problems = run_all(repo_root)
    for problem in problems:
        print(problem, file=sys.stderr)

    if problems:
        print(f"starter-check: {len(problems)} problem(s) found", file=sys.stderr)
        return 1

    print("starter-check: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
