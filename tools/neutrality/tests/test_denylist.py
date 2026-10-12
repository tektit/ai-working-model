from __future__ import annotations

from pathlib import Path

import pytest

from neutrality.denylist import DenylistMissing, load_denylist


def test_parses_patterns_skips_blank_and_comment_lines(tmp_path: Path) -> None:
    path = tmp_path / ".neutrality-denylist"
    path.write_text(
        "\n".join(
            [
                "# a comment",
                "",
                "acme",
                "  # indented comment",
                "\\bwidgetco\\b",
                "",
            ]
        )
    )

    entries = load_denylist(path)

    assert [e.pattern for e in entries] == ["acme", "\\bwidgetco\\b"]


def test_patterns_are_case_insensitive(tmp_path: Path) -> None:
    path = tmp_path / ".neutrality-denylist"
    path.write_text("acme\n")

    entries = load_denylist(path)

    assert entries[0].regex.search("Contact ACME Corp") is not None


def test_missing_denylist_raises(tmp_path: Path) -> None:
    with pytest.raises(DenylistMissing):
        load_denylist(tmp_path / ".neutrality-denylist")


def test_non_ascii_patterns_are_read_as_utf_8(tmp_path: Path) -> None:
    path = tmp_path / ".neutrality-denylist"
    path.write_text("Müller\n", encoding="utf-8")

    entries = load_denylist(path)

    assert entries[0].regex.search("Kunde Müller GmbH") is not None
