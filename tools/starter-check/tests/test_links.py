from __future__ import annotations

from pathlib import Path

from starter_check.links import find_broken_references


def test_resolving_relative_link_is_not_a_problem(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "glossary.md").write_text("# Glossary\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("See [glossary](docs/glossary.md).\n", encoding="utf-8")

    assert find_broken_references(tmp_path) == []


def test_broken_relative_link_is_reported(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("See [nope](docs/missing.md).\n", encoding="utf-8")

    problems = find_broken_references(tmp_path)

    assert len(problems) == 1
    assert problems[0].kind == "link"
    assert problems[0].target == "docs/missing.md"
    assert problems[0].line_number == 1


def test_external_link_is_skipped(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text(
        "See [external](https://example.com/page) for more.\n", encoding="utf-8"
    )

    assert find_broken_references(tmp_path) == []


def test_same_page_anchor_is_skipped(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Jump to [section](#a-section).\n", encoding="utf-8")

    assert find_broken_references(tmp_path) == []


def test_link_with_fragment_resolves_the_file_part(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "glossary.md").write_text("# Glossary\n", encoding="utf-8")
    (tmp_path / "README.md").write_text(
        "See [term](docs/glossary.md#term).\n", encoding="utf-8"
    )

    assert find_broken_references(tmp_path) == []


def test_directory_link_resolves_if_directory_exists(tmp_path: Path) -> None:
    (tmp_path / "docs" / "design").mkdir(parents=True)
    (tmp_path / "README.md").write_text("See [designs](docs/design/).\n", encoding="utf-8")

    assert find_broken_references(tmp_path) == []


def test_valid_import_is_not_a_problem(tmp_path: Path) -> None:
    (tmp_path / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")

    assert find_broken_references(tmp_path) == []


def test_broken_import_is_reported(tmp_path: Path) -> None:
    (tmp_path / "CLAUDE.md").write_text("@MISSING.md\n", encoding="utf-8")

    problems = find_broken_references(tmp_path)

    assert len(problems) == 1
    assert problems[0].kind == "import"
    assert problems[0].target == "MISSING.md"


def test_bash_positional_all_is_not_mistaken_for_an_import(
    tmp_path: Path,
) -> None:
    (tmp_path / "notes.md").write_text(
        'Use `if [[ cond ]]; then main "$@"; fi` in bash.\n', encoding="utf-8"
    )

    assert find_broken_references(tmp_path) == []


def test_stray_at_word_without_path_shape_is_ignored(tmp_path: Path) -> None:
    (tmp_path / "notes.md").write_text("Reach out @someone about this.\n", encoding="utf-8")

    assert find_broken_references(tmp_path) == []


def test_relative_link_resolves_against_its_own_file_directory(
    tmp_path: Path,
) -> None:
    (tmp_path / "starter" / "docs" / "design").mkdir(parents=True)
    (tmp_path / "starter" / "docs" / "architecture.md").write_text(
        "See [design/](design/).\n", encoding="utf-8"
    )

    assert find_broken_references(tmp_path) == []


def test_relative_link_up_a_level_resolves(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "backlog.md").write_text("# Backlog\n", encoding="utf-8")
    (tmp_path / "docs" / "architecture.md").write_text(
        "See [backlog.md](../backlog.md).\n", encoding="utf-8"
    )

    assert find_broken_references(tmp_path) == []
