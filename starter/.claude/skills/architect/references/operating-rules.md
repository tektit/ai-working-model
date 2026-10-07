# Operating rules

Read before any branch, review or bookkeeping action, before recording
a ruling, and before watching long-running work. Branching, merging,
live systems and verifying agent output are in the principles (linked
from `AGENTS.md`); these rules add what the architect role does.

## Bookkeeping and rulings

- **Bookkeeping is milestone-batched**: the backlog and the
  architecture doc. Never during a human's review or merge windows.
- **Other sessions may have moved these files or items.** Re-read them
  from the remote (or the tracker) immediately before every write and
  before relying on them for a decision. Never write from a stale read.
- **Edit architect-maintained files with small, anchored changes**, and
  check the file's length and section boundaries before pushing. A bad
  bulk rewrite of a long file is easy to miss and expensive to undo.
- **Every ruling gets a dated entry appended to `docs/decisions.md`**,
  after the human's yes. A request that would change a principle is
  not a ruling; it goes through "Changing a principle".

## Supervising long-running work

- When asked to watch long-running work (a pipeline, a test run, an
  agent), use timed checks: not busy-polling, not fire-and-forget.
- An agent that parks itself waiting on its own children is resumed
  with: **collect the results and finish; do not wait again.**
- An agent that stops with an empty or partial report: check the remote
  yourself before concluding anything. The work is often done; the
  report is what failed.
- A pipeline failure is diagnosed from the job's own log, not a
  summary. Before a new hypothesis, search the project's docs for the
  symptom and compare with the nearest working instance.
