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

## Format

```markdown
## D<n>: <title> (<YYYY-MM-DD>)

- **Status:** in force | superseded by D<m>
- **Context:** what forced the decision, in a sentence or two.
- **Decision:** what was chosen.
- **Consequences:** what follows from it, what gets harder, what is
  hard to undo.
```
