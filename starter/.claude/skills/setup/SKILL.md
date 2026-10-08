---
name: setup
description: "Project setup: ask a human a few plain-language questions, then fit the copied docs to the project. Run once in a freshly copied repo, or again when the setup changes. Use only when a human explicitly asks."
disable-model-invocation: true
---

# Project setup

You set up a freshly copied project so every later session works the
same way. You ask, recommend and draft; the human answers, approves
and merges. Assume no skill level: explain in plain words.

## How to talk

- Plain language. Explain each technical term the first time, in one
  clause ("the trunk: the version of the code that counts").
- One question at a time, each with a recommended answer for their
  situation and a two-sentence trade-off. They can simply say "yes".
- Open with two sentences: setup records a few decisions so that later
  sessions work the same way, and it takes a handful of questions.
- Keep each message short. No tool output, no file dumps.

## Observe, then ask

- Facts you can observe, read yourself and confirm in one line instead
  of asking: the git remote and trunk, pipeline files that exist, an
  existing README.
- Everything else is asked ("Ask, don't guess" in the principles): the
  purpose, the people, the tracker, what deploys where, the
  organization's rules, how credentials reach a command.
- Never ask for a secret value, and never write one into a file or
  the chat.

## Before the first question

1. Read the root instruction file (`AGENTS.md`), `docs/architecture.md`,
   the headers of `backlog.md`, and `docs/glossary.md`.
2. If `AGENTS.md` already has a "Project setup" section, this is a
   re-run: show the recorded answers in a few lines, ask what changed,
   and ask only about that.
3. Observe what you can (above) so your questions confirm rather than
   interrogate.
4. Check for personal skills or commands that share a name with the
   project's: `ls ~/.claude/skills ~/.claude/commands 2>/dev/null`,
   compared with the names under `.claude/skills/` (`architect`,
   `setup` and any other; a command's name is its file name without
   `.md`). If one matches, tell the human it silently
   shadows the project's and suggest renaming the personal one.

## The questions, in this order

Read `references/questions.md` before asking the first one. It has, per
question, the plain wording, the recommended default by situation, and
the trade-off.

1. **Product and purpose**: what it does, for whom, what success looks
   like.
2. **Stakeholders**: who uses it, operates it, is responsible for its
   security, pays for it, and is legally affected.
3. **Git host, trunk and merge method**.
4. **Pipeline**: what runs on each change, what merging deploys, and
   where.
5. **Where work and project management lives**: issues on the git host,
   the default `backlog.md`, Jira, or another tracker. This matters
   most: from now on "the backlog" means this place.
6. **Environments**: where the software runs (for example only on a
   laptop, or a test system and production).
7. **Organization constraints**: rules the project must follow (data
   protection, approved vendors or hosting, security policies,
   budget, licenses).
8. **How far agents write to the repo**: push branches and open draft
   review requests, commit locally only, or nothing without a
   per-change instruction.
9. **Commit attribution**: whether AI-written commits and review
   requests say so.
10. **Time zone** for times shown to people.

Last, ask whether the project deliberately differs from any of its
principles. Only the human can say so; don't suggest deviations.

## Propose, approve, write

1. Draft every change first. Read `references/edits.md` for what goes
   where in each file.
2. Show the human a summary: one line per file, what changes, in plain
   language, plus anything recorded as "not known yet". Ask for approval
   or corrections. Write nothing before they approve.
3. Apply the approved changes to:
   - `AGENTS.md`: the purpose line and a "Project setup" record section;
   - `docs/architecture.md`: purpose, stakeholders, decisions in force;
   - `docs/decisions.md`: one dated entry per decision in force;
   - `backlog.md`: seeded, or removed with every link pointing to the
     chosen tracker instead;
   - `docs/glossary.md`: initial terms;
   - `.claude/settings.json`: `attribution`, only when the attribution
     answer is not the default.
4. Remove every template comment (`<!-- ... -->`) in the files you
   touched, the architect-maintained markers included, and every
   template section the project doesn't use. Filled content stays.
5. A deviation the human stated is a principle change: follow
   "Changing a principle" in `docs/principles/ai-working-process.md`
   (the principle, its line in `AGENTS.md` and an entry in
   `docs/decisions.md`, in one change).
6. Check your own result: every relative link in the changed files
   resolves, `grep -rn '<!--' AGENTS.md docs/` (plus `backlog.md` if
   it stays) finds nothing, and no answer appears that the human did
   not give.
7. If the repo has a remote, the changes go on a branch for review and
   a human merges. In a repo with no remote yet, they become the first
   commit, made only after approval.

## Finish

Report in under 10 lines: what was recorded, what is still "not known
yet" and who could answer it, and the next step. The next step is
usually an architect session, which works from what you recorded.
