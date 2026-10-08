---
paths:
  - ".claude/rules/**"
---

# Path-scoped rules

The root instruction file (`AGENTS.md`) is always loaded, so it stays
small (see `../../docs/principles/context-economy.md`). A rule that
only matters for one area of the tree (a subsystem's own
conventions, a language-specific style rule, a directory with unusual
constraints) does not belong there; it belongs in a path-scoped rule
instead, so it's loaded only when it's actually relevant.

A rule file without a `paths` header loads in every session, so only
a rule that truly applies everywhere omits it; this README has one, so
it loads only when a rule file is read or edited.

Claude Code loads rule files scoped by path under `.claude/rules/`;
other tools have their own mechanism. Claude Code documents that a
rule loads when the session reads, writes or edits a matching file
with its file tools. Beyond that:

- a read through a shell command has been observed both to load a
  matching rule and not to, depending on the tool version;
- in another copy of the repo, such as a delegated agent's own clone,
  no rule was observed to load;
- a subagent gets the starting session's instructions, not those of
  its working directory.

So never rely on a rule loading by itself: before working in an
area, read its rule file explicitly, and a brief names, by path, the
rule files of the area its task touches for the agent to read (Brief
anatomy in `../../docs/principles/ai-working-process.md`).

Scope a rule's path glob to its area: a directory or a file type,
never a list of single files (the next file of that kind is missed),
and never a catch-all such as `docs/**` or `**/*.md`. A catch-all
loads the rule on every read of any doc; with several rules scoped
that way, one docs-only read was computed to pull in about 100 KB of
rules.

The principle, regardless of mechanism:

- One rule file per scope that genuinely needs its own conventions —
  not one file per tiny fact; a handful of related rules for the same
  area belong together.
- State the rule the same way `../../docs/principles/engineering.md`
  does: a short rule, why it matters if it's not obvious, how to apply
  it.
- If a rule turns out to apply everywhere, it doesn't belong here
  either — promote it into the root `AGENTS.md`, or into
  `docs/principles/` if it is a principle (through "Changing a
  principle").
