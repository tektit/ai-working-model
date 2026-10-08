# AGENTS.md

Tektit Consulting's AI working model. This repo has two jobs: it is
the **product** — the starter kit teams copy into new repos — and it
is its own **working area**, where that kit is built, measured and
dogfooded before it ships.

This repo follows its own starter: its engineering and AI-collaboration
principles are [starter/docs/principles/](starter/docs/principles/),
and the root `.claude` is a symlink to `starter/.claude`, so an agent
working in this repo runs the exact same agents, skills, rules and
settings a seeded project would.

## Layout

- `starter/` — the exact tree a user copies into a new repo. Read
  [README.md](README.md) for what's inside and how to seed a new repo
  with it.
- `architecture/decisions.md` — this repo's own decision log (not a
  seeded project's; those get their own).
- `tools/` — check instruments (`neutrality`, `starter-check`), each
  its own `uv` project.
- `backlog.md` — the backlog for THIS repo's own work (owner decides
  and merges; the architect keeps it current) — not to be confused
  with `starter/backlog.md`, which is a template skeleton for seeded
  projects.

## Rules specific to working here

- **Neutrality check before every commit** — see README's "Neutrality
  check" section; no client, customer or private-project identifiers
  anywhere in this repo.
- **`starter/` must stay generic.** Nothing under it may name this
  repo, a client, or reference its own former location, or carry a
  license file or copyright line (its MIT-0 terms live in the root
  `LICENSE-starter`, recorded in `NOTICE`) — run
  `uv run --project tools/starter-check starter-check` before
  committing a change that touches it.
- **Delegated agents work in their own fresh clone, never in the
  human's checkout or a worktree of it** (in Claude Code, under the
  session's scratchpad directory). For the neutrality check, symlink
  the root's gitignored `.neutrality-denylist` into the clone and
  remove the link afterwards; never commit it.
- **Read Claude Code docs raw**: `curl -sL
  https://code.claude.com/docs/en/<page>.md` into the scratchpad, then
  read the section that drives the decision — not through a
  summarizing fetch, which has misreported facts.

The backlog is [backlog.md](backlog.md), at the repo root.
