from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from conftest import needs_real_symlink

from starter_check.checker import (
    check_claude_md,
    check_links,
    check_no_license_terms,
    check_no_backreferences,
    check_root_symlinks,
    copy_starter,
    find_repo_root,
    run_all,
)


def test_find_repo_root_locates_the_repo_from_a_nested_path(
    repo_root: Path,
) -> None:
    nested = repo_root / "starter" / "docs"

    assert find_repo_root(nested) == repo_root


def test_copy_starter_copies_contents_not_the_directory_itself(
    repo_root: Path, tmp_path: Path
) -> None:
    dest = tmp_path / "copy"
    dest.mkdir()

    copy_starter(repo_root / "starter", dest)

    assert (dest / "AGENTS.md").exists()
    assert not (dest / "starter").exists()


def test_valid_synthetic_starter_has_no_problems(repo_root: Path) -> None:
    assert run_all(repo_root) == []


def test_check_links_catches_a_broken_link(repo_root: Path, tmp_path: Path) -> None:
    (repo_root / "starter" / "AGENTS.md").write_text(
        "See [nope](docs/does-not-exist.md).\n", encoding="utf-8"
    )
    dest = tmp_path / "copy"
    dest.mkdir()
    copy_starter(repo_root / "starter", dest)

    problems = check_links(dest)

    assert any("does-not-exist.md" in p for p in problems)


def test_check_no_backreferences_catches_ai_working_model_mention(
    repo_root: Path, tmp_path: Path
) -> None:
    (repo_root / "starter" / "AGENTS.md").write_text(
        "Defaults come from the ai-working-model repo.\n", encoding="utf-8"
    )
    dest = tmp_path / "copy"
    dest.mkdir()
    copy_starter(repo_root / "starter", dest)

    problems = check_no_backreferences(dest)

    assert any("ai-working-model" in p for p in problems)


def test_check_no_backreferences_catches_starter_slash_mention(
    repo_root: Path, tmp_path: Path
) -> None:
    (repo_root / "starter" / "AGENTS.md").write_text(
        "Copied from starter/ into this repo.\n", encoding="utf-8"
    )
    dest = tmp_path / "copy"
    dest.mkdir()
    copy_starter(repo_root / "starter", dest)

    problems = check_no_backreferences(dest)

    assert any("starter/" in p for p in problems)


def test_run_all_reports_an_unlinked_principle_heading(repo_root: Path) -> None:
    engineering = repo_root / "starter" / "docs" / "principles" / "engineering.md"
    engineering.write_text(engineering.read_text() + "\n## Thin CI\n", encoding="utf-8")

    problems = run_all(repo_root)

    assert any("'Thin CI'" in p and "not linked" in p for p in problems)


def _copy_with(repo_root: Path, tmp_path: Path, rel: str, content: str) -> Path:
    target = repo_root / "starter" / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    dest = tmp_path / "copy"
    dest.mkdir()
    copy_starter(repo_root / "starter", dest)
    return dest


def test_check_no_license_terms_catches_a_root_license_file(
    repo_root: Path, tmp_path: Path
) -> None:
    dest = _copy_with(repo_root, tmp_path, "LICENSE", "MIT-0\n")

    assert check_no_license_terms(dest) == [
        "LICENSE: license file does not belong in the starter"
    ]


def test_check_no_license_terms_catches_a_nested_copying_file(
    repo_root: Path, tmp_path: Path
) -> None:
    dest = _copy_with(repo_root, tmp_path, "docs/COPYING.md", "terms\n")

    problems = check_no_license_terms(dest)

    assert any("docs/COPYING.md" in p for p in problems)


def test_check_no_license_terms_catches_a_copyright_line(
    repo_root: Path, tmp_path: Path
) -> None:
    dest = _copy_with(
        repo_root, tmp_path, "docs/architecture.md", "# A\n\nCopyright 2026 Someone\n"
    )

    problems = check_no_license_terms(dest)

    assert any("docs/architecture.md:3:" in p for p in problems)


def test_check_no_license_terms_catches_an_spdx_tag(
    repo_root: Path, tmp_path: Path
) -> None:
    dest = _copy_with(
        repo_root, tmp_path, "backlog.md", "# B\n<!-- SPDX-License-Identifier: MIT -->\n"
    )

    problems = check_no_license_terms(dest)

    assert any("backlog.md:2:" in p for p in problems)


def test_check_no_license_terms_ignores_prose_about_licenses(
    repo_root: Path, tmp_path: Path
) -> None:
    dest = _copy_with(
        repo_root,
        tmp_path,
        "docs/architecture.md",
        "Ask about budget limits, licenses, deadlines.\n",
    )

    assert check_no_license_terms(dest) == []


def test_check_claude_md_accepts_exact_content(
    repo_root: Path, tmp_path: Path
) -> None:
    dest = tmp_path / "copy"
    dest.mkdir()
    copy_starter(repo_root / "starter", dest)

    assert check_claude_md(dest) == []


def test_check_claude_md_rejects_extra_content(
    repo_root: Path, tmp_path: Path
) -> None:
    (repo_root / "starter" / "CLAUDE.md").write_text(
        "@AGENTS.md\n\nExtra note.\n", encoding="utf-8"
    )
    dest = tmp_path / "copy"
    dest.mkdir()
    copy_starter(repo_root / "starter", dest)

    problems = check_claude_md(dest)

    assert len(problems) == 1
    assert "CLAUDE.md" in problems[0]


def test_check_claude_md_reports_missing_file(tmp_path: Path) -> None:
    assert check_claude_md(tmp_path) == ["CLAUDE.md: missing"]


def test_check_root_symlinks_passes_for_valid_symlinks(repo_root: Path) -> None:
    assert check_root_symlinks(repo_root, repo_root / "starter") == []


def _remove_link(link: Path) -> None:
    """Removes the fixture's link: a symlink unlinks, a junction rmdirs."""
    if link.is_symlink():
        link.unlink()
    else:
        link.rmdir()


def test_check_root_symlinks_reports_a_missing_link(repo_root: Path) -> None:
    _remove_link(repo_root / ".claude")

    problems = check_root_symlinks(repo_root, repo_root / "starter")

    assert len(problems) == 1
    assert "missing" in problems[0]
    assert "Working on Windows" in problems[0]


def test_check_root_symlinks_reports_the_git_stub_file(repo_root: Path) -> None:
    _remove_link(repo_root / ".claude")
    (repo_root / ".claude").write_text("starter/.claude", encoding="utf-8")

    problems = check_root_symlinks(repo_root, repo_root / "starter")

    assert len(problems) == 1
    assert "without symlink support" in problems[0]
    assert "Working on Windows" in problems[0]


def test_check_root_symlinks_reports_a_copied_directory(repo_root: Path) -> None:
    _remove_link(repo_root / ".claude")
    shutil.copytree(repo_root / "starter" / ".claude", repo_root / ".claude")

    problems = check_root_symlinks(repo_root, repo_root / "starter")

    assert len(problems) == 1
    assert "copied directory" in problems[0]
    assert "Working on Windows" in problems[0]


@pytest.mark.skipif(sys.platform != "win32", reason="junctions exist only on Windows")
def test_check_root_symlinks_accepts_a_junction(repo_root: Path) -> None:
    _remove_link(repo_root / ".claude")
    subprocess.run(
        [
            "cmd", "/c", "mklink", "/J",
            str(repo_root / ".claude"), str(repo_root / "starter" / ".claude"),
        ],
        check=True,
        capture_output=True,
    )
    assert not (repo_root / ".claude").is_symlink()

    assert check_root_symlinks(repo_root, repo_root / "starter") == []


@needs_real_symlink
def test_check_root_symlinks_reports_a_dangling_symlink(repo_root: Path) -> None:
    (repo_root / ".claude").unlink()
    (repo_root / ".claude").symlink_to(
        repo_root / "starter" / "does-not-exist", target_is_directory=True
    )

    problems = check_root_symlinks(repo_root, repo_root / "starter")

    assert any("dangling" in p for p in problems)


@needs_real_symlink
def test_check_root_symlinks_reports_a_symlink_pointing_outside_starter(
    repo_root: Path,
) -> None:
    outside = repo_root / "outside"
    outside.mkdir()
    (repo_root / ".claude").unlink()
    (repo_root / ".claude").symlink_to(outside, target_is_directory=True)

    problems = check_root_symlinks(repo_root, repo_root / "starter")

    assert any("outside starter/" in p for p in problems)


def test_run_all_against_the_real_starter() -> None:
    """The actual instrument this tool ships for: run every check
    against this repo's real `starter/`, not a synthetic fixture."""
    real_repo_root = find_repo_root(Path(__file__))

    problems = run_all(real_repo_root)

    assert problems == []
