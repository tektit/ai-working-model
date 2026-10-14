# Decisions

The project's decisions, one dated entry each. Every decision in force in
[architecture.md](architecture.md) cites its entry here; every ruling
and every principle change gets one too (see "Changing a principle" in
[principles/ai-working-process.md](principles/ai-working-process.md)).
Append-only: an entry is written after a human's yes, in the same
change as what it records. Entries are numbered D1, D2, … in order and
dated. An entry is never deleted: a superseded one stays, marked with
the entry that superseded it.

A deliberate omission (something left out of the system or the docs
on purpose) is a decision too: its entry gives the reason, so a later
session doesn't add it back as a fix, and any count or list that would
include it says so ("four of five, see D<n>").

An entry is lean: the decision, one line of why, what it replaces, and
links to its evidence (the PR, the design doc, the commit). The
evidence stays where it lives; an entry carries no incident narrative,
no measurements and no list of what was carried out. A decision that
needs more room gets a design doc, linked.

## Format

```markdown
## D<n>: <title> (<YYYY-MM-DD>)

- **Status:** in force | superseded (in whole or in part) by D<m>
- **Context:** why it was needed, one or two sentences.
- **Decision:** what was chosen; replaces D<m>, in whole or in part,
  where it does.
- **Consequences:** what gets harder, what is hard to undo.
- **Evidence:** links to the PR, the design doc, the commit.
```
