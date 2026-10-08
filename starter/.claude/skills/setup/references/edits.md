# Setup edits: what goes where

Read before drafting. Each file keeps its existing structure; fill it,
don't redesign it. Then remove every template comment (`<!-- ... -->`)
in the files you touch, the architect-maintained markers included (the
list in `AGENTS.md` is the one authority on which files are
architect-maintained), and every template section the project doesn't
use; a section it will fill later keeps its heading. All of setup is
one seeding change.

## `AGENTS.md`

- Replace the purpose placeholder with the human's one or two sentences.
- Add a "Project setup" section right after the purpose, in this shape:

  ```markdown
  ## Project setup

  Recorded by the setup skill; re-run it when any of this changes.

  - **Git:** <host and repository>, trunk `<branch>`; <squash merges:
    a branch catches up by merging the trunk in | no squash: a branch
    you alone use catches up by rebasing>.
  - **Agent writes:** <push work branches and open draft MRs/PRs |
    commit locally only | nothing without a per-change instruction>.
  - **Attribution:** <AI-written commits name the model as co-author,
    MR/PR descriptions carry a generated-with line | the chosen
    policy>.
  - **Time zone:** <zone>, stated with every time shown to people.
  - **Pipeline:** <what runs on each change>; merging to `<branch>`
    <deploys to X | deploys nothing>.
  - **Backlog:** <backlog.md | the tracker and project>. Mapping:
    <next-session pointer, in flight, queued, deliberately deferred,
    done>. Access: <how it reaches a command, never a value>.
  - **Environments:** <names, as in the glossary>.
  - **Principles:** `docs/principles/`; a deviation goes through
    "Changing a principle", with an entry in `docs/decisions.md`.
  ```

- If the backlog is a tracker, change every mention of `backlog.md` in
  this file to point to it.
- Anything "not known yet" stays in the record as exactly that.

## `docs/architecture.md`

- Title: the product's name.
- Purpose: the human's sentences, under the title.
- Stakeholders line: one entry per role, with who speaks for it.
- "Decisions in force": one short subsection each for delivery (git
  host, pipeline, what merging deploys), work tracking, environments,
  and each organization constraint that shapes the design. State what
  was chosen and why, in a sentence, citing its entry in
  `docs/decisions.md`.
- If the backlog is a tracker, point the table row and the "Open
  questions" section at it instead of `backlog.md`.

## `docs/decisions.md`

- One entry per decision in force, D1 onwards, dated today, in the
  file's Format: status "in force", the context from the answer, the
  decision, its consequences.

## `backlog.md`

- If it stays: write "Next session starts here" (setup done, the
  recommended first job), and add every "not known yet" to "Queued" as a
  question naming who could answer it.
- If a tracker replaces it: create the equivalent pinned item there
  only if you have access and the human approved it; otherwise list
  it for the human. Delete `backlog.md`, and change every link to it in
  the repo (search the whole tree, not only the files above).

## `docs/glossary.md`

- Initial terms, one entry each, in the human's words: the product
  name, each environment, each stakeholder role that has a specific
  name here, and domain words the human used that a newcomer would not
  know.
- Don't define general engineering terms; the glossary is for this
  project's own vocabulary.

## `.claude/settings.json`

- Only when the attribution answer is not the default: set
  `attribution` to the chosen text. To hide attribution entirely, set
  `"commit": ""`, `"pr": ""` and `"sessionUrl": false` under it.
  Left unset, Claude Code's default names the model in use, which a
  fixed text could not.

## Not touched

- `docs/principles/`: edited only for a deviation the human stated,
  through "Changing a principle" (SKILL.md step 5).
- Code, pipeline files and settings, except `attribution` above: setup
  records what exists; changing them is later work for an architect
  session.
