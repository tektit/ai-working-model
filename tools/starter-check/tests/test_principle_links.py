from __future__ import annotations

from pathlib import Path

import pytest

from starter_check.principle_links import (
    PRINCIPLE_FILES,
    check_principle_links,
    github_slug,
)


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    """A tree whose AGENTS.md links every principle heading exactly
    once — valid as built. Tests rewrite one file to provoke one
    problem at a time."""
    principles = tmp_path / "docs" / "principles"
    principles.mkdir(parents=True)
    (principles / "engineering.md").write_text(
        "# Engineering principles\n\n"
        "## Fail early and loudly\n\nRule.\n\n"
        "## Respect deliberate patterns; open decisions stay open\n\nRule.\n", encoding="utf-8"
    )
    (principles / "ai-working-process.md").write_text(
        "# AI working process\n\n## Ask, don't guess\n\nRule.\n", encoding="utf-8"
    )
    (principles / "context-economy.md").write_text(
        "# Context economy\n\n"
        "```markdown\n## Not a heading, inside a fence\n```\n\n"
        "## Shrink and skip; never compress\n\nRule.\n", encoding="utf-8"
    )
    (tmp_path / "AGENTS.md").write_text(
        "# AGENTS.md\n\n"
        "- Stop loudly — [Fail early and loudly]"
        "(docs/principles/engineering.md#fail-early-and-loudly).\n"
        "- Open stays open — [Respect deliberate patterns]"
        "(docs/principles/engineering.md"
        "#respect-deliberate-patterns-open-decisions-stay-open).\n"
        "- Ask — [Ask, don't guess]"
        "(docs/principles/ai-working-process.md#ask-dont-guess).\n"
        "- Shrink — [Shrink and skip]"
        "(docs/principles/context-economy.md#shrink-and-skip-never-compress).\n"
        "- All of them: [engineering.md](docs/principles/engineering.md).\n", encoding="utf-8"
    )
    return tmp_path


def _agents_md(tree: Path) -> Path:
    return tree / "AGENTS.md"


@pytest.mark.parametrize(
    ("heading", "slug"),
    [
        ("Fail early and loudly", "fail-early-and-loudly"),
        ("Ask, don't guess", "ask-dont-guess"),
        (
            "Respect deliberate patterns; open decisions stay open",
            "respect-deliberate-patterns-open-decisions-stay-open",
        ),
        (
            "The tested procedure IS the shipped procedure",
            "the-tested-procedure-is-the-shipped-procedure",
        ),
        (
            "Delegation: objectives, not a lookup table",
            "delegation-objectives-not-a-lookup-table",
        ),
        ("Thin CI — no logic", "thin-ci--no-logic"),
    ],
)
def test_github_slug(heading: str, slug: str) -> None:
    assert github_slug(heading) == slug


def test_principle_files_are_the_three_principle_docs() -> None:
    assert [p.name for p in PRINCIPLE_FILES] == [
        "engineering.md",
        "ai-working-process.md",
        "context-economy.md",
    ]


def test_every_heading_linked_once_is_clean(tree: Path) -> None:
    assert check_principle_links(tree) == []


def test_an_unlinked_heading_is_reported_by_name(tree: Path) -> None:
    path = tree / "docs" / "principles" / "engineering.md"
    path.write_text(path.read_text() + "\n## Thin CI\n\nRule.\n", encoding="utf-8")

    problems = check_principle_links(tree)

    assert len(problems) == 1
    assert "'Thin CI'" in problems[0]
    assert "not linked" in problems[0]
    assert "#thin-ci" in problems[0]


def test_an_anchor_matching_no_heading_is_reported(tree: Path) -> None:
    agents = _agents_md(tree)
    agents.write_text(
        agents.read_text()
        + "- Gone — [Old](docs/principles/engineering.md#no-such-principle).\n", encoding="utf-8"
    )

    problems = check_principle_links(tree)

    assert len(problems) == 1
    assert "#no-such-principle" in problems[0]
    assert "AGENTS.md:8" in problems[0]
    assert "no heading" in problems[0]


def test_a_heading_linked_twice_is_reported_by_name(tree: Path) -> None:
    agents = _agents_md(tree)
    agents.write_text(
        agents.read_text()
        + "- Again — [Ask](docs/principles/ai-working-process.md#ask-dont-guess).\n", encoding="utf-8"
    )

    problems = check_principle_links(tree)

    assert len(problems) == 1
    assert repr("Ask, don't guess") in problems[0]
    assert "2 times" in problems[0]


def test_a_heading_inside_a_code_fence_is_not_a_principle(tree: Path) -> None:
    assert not any(
        "Not a heading" in p for p in check_principle_links(tree)
    )


def test_a_level_three_heading_is_not_a_principle(tree: Path) -> None:
    path = tree / "docs" / "principles" / "engineering.md"
    path.write_text(path.read_text() + "\n### A detail\n\nText.\n", encoding="utf-8")

    assert check_principle_links(tree) == []


def test_a_missing_principle_file_is_reported(tree: Path) -> None:
    (tree / "docs" / "principles" / "context-economy.md").unlink()

    problems = check_principle_links(tree)

    assert any(
        "docs/principles/context-economy.md: missing" in p for p in problems
    )


def test_a_missing_agents_md_is_reported(tree: Path) -> None:
    _agents_md(tree).unlink()

    assert check_principle_links(tree) == ["AGENTS.md: missing"]


def test_a_heading_inside_an_html_comment_is_not_a_principle(tree: Path) -> None:
    path = tree / "docs" / "principles" / "engineering.md"
    path.write_text(
        path.read_text() + "\n<!--\n## Template heading\n-->\n<!-- ## Inline -->\n", encoding="utf-8"
    )

    assert check_principle_links(tree) == []


def test_a_duplicate_slug_within_a_file_is_reported_by_name(tree: Path) -> None:
    path = tree / "docs" / "principles" / "engineering.md"
    path.write_text(path.read_text() + "\n## Fail early, and loudly\n\nRule.\n", encoding="utf-8")

    problems = check_principle_links(tree)

    assert len(problems) == 1
    assert "duplicate anchor #fail-early-and-loudly" in problems[0]
    assert "'Fail early, and loudly'" in problems[0]


@pytest.mark.parametrize(
    "heading",
    ["Use _emphasis_ here", "See [the docs](other.md)"],
)
def test_heading_markup_the_slugger_cannot_handle_fails_loudly(
    tree: Path, heading: str
) -> None:
    path = tree / "docs" / "principles" / "engineering.md"
    path.write_text(path.read_text() + f"\n## {heading}\n\nRule.\n", encoding="utf-8")

    problems = check_principle_links(tree)

    assert any(
        "unsupported markup" in p and repr(heading) in p for p in problems
    )
