from __future__ import annotations

from pathlib import Path

from neutrality.cli import main

from conftest import write_and_stage, write_denylist


def test_clean_repo_exits_zero_and_prints_nothing(repo: Path, capsys) -> None:
    write_and_stage(repo, "README.md", "Nothing sensitive.\n")
    write_denylist(repo, "acme")

    rc = main(["--repo", str(repo)])

    assert rc == 0
    captured = capsys.readouterr()
    assert captured.out == ""


def test_hit_exits_one_and_prints_file_line_pattern(repo: Path, capsys) -> None:
    write_and_stage(repo, "notes.md", "line one\nworking for Acme Corp\n")
    write_denylist(repo, "acme")

    rc = main(["--repo", str(repo)])

    assert rc == 1
    captured = capsys.readouterr()
    assert captured.out.strip() == "notes.md:2: acme"


def test_missing_denylist_exits_two_with_clear_message(repo: Path, capsys) -> None:
    write_and_stage(repo, "README.md", "content\n")

    rc = main(["--repo", str(repo)])

    assert rc == 2
    captured = capsys.readouterr()
    assert "denylist" in captured.err.lower()
    assert "missing" in captured.err.lower()


def test_defaults_repo_to_current_directory(repo: Path, capsys, monkeypatch) -> None:
    write_and_stage(repo, "README.md", "content\n")
    write_denylist(repo, "acme")
    monkeypatch.chdir(repo)

    rc = main([])

    assert rc == 0
