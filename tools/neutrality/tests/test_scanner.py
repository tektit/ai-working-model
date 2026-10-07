from __future__ import annotations

from pathlib import Path

from neutrality.denylist import load_denylist
from neutrality.scanner import scan, tracked_and_staged_files

from conftest import write_and_stage, write_denylist


def test_clean_repo_has_no_hits(repo: Path) -> None:
    write_and_stage(repo, "README.md", "Hello world.\nNothing sensitive here.\n")
    denylist = load_denylist(write_denylist(repo, "acme"))

    hits = scan(repo, denylist)

    assert hits == []


def test_finds_hit_with_path_and_line_number(repo: Path) -> None:
    write_and_stage(repo, "notes.md", "line one\nworking for Acme Corp\nline three\n")
    denylist = load_denylist(write_denylist(repo, "acme"))

    hits = scan(repo, denylist)

    assert len(hits) == 1
    assert hits[0].path == "notes.md"
    assert hits[0].line_number == 2
    assert hits[0].pattern == "acme"


def test_finds_hit_in_staged_but_not_yet_committed_file(repo: Path) -> None:
    # No commit exists at all yet; the file only ever lives in the index.
    write_and_stage(repo, "docs/design.md", "internal project: widgetco\n")
    denylist = load_denylist(write_denylist(repo, "widgetco"))

    hits = scan(repo, denylist)

    assert [h.path for h in hits] == ["docs/design.md"]


def test_multiple_patterns_and_multiple_files(repo: Path) -> None:
    write_and_stage(repo, "a.md", "mentions acme here\n")
    write_and_stage(repo, "b.md", "mentions widgetco here\n")
    write_and_stage(repo, "c.md", "mentions neither\n")
    denylist = load_denylist(write_denylist(repo, "acme", "widgetco"))

    hits = scan(repo, denylist)

    assert {h.path for h in hits} == {"a.md", "b.md"}


def test_word_boundary_pattern_does_not_match_substring(repo: Path) -> None:
    write_and_stage(repo, "a.md", "evaluation continues\n")
    denylist = load_denylist(write_denylist(repo, r"\bual\b"))

    hits = scan(repo, denylist)

    assert hits == []


def test_reads_content_from_index_not_working_tree(repo: Path) -> None:
    write_and_stage(repo, "a.md", "clean content\n")
    # Modify the working tree WITHOUT re-staging: the index still holds
    # the clean version, and that is what must be scanned.
    (repo / "a.md").write_text("mentions acme now\n")
    denylist = load_denylist(write_denylist(repo, "acme"))

    hits = scan(repo, denylist)

    assert hits == []


def test_tracked_and_staged_files_lists_indexed_paths(repo: Path) -> None:
    write_and_stage(repo, "a.md", "content\n")
    write_and_stage(repo, "sub/b.md", "content\n")

    paths = tracked_and_staged_files(repo)

    assert set(paths) == {"a.md", "sub/b.md"}


def test_binary_file_is_skipped_not_errored(repo: Path) -> None:
    path = repo / "blob.bin"
    path.write_bytes(b"\xff\xfe\x00acme\x00\xff")
    import subprocess

    subprocess.run(["git", "-C", str(repo), "add", "blob.bin"], check=True)
    denylist = load_denylist(write_denylist(repo, "acme"))

    hits = scan(repo, denylist)

    assert hits == []
