# Tektit Consulting AI working model

Tektit Consulting's AI working model: a starting point for teams —
including non-IT people — building internal tools with AI coding
agents under engineering guardrails. It targets Claude Code and OpenAI
Codex, and distills engineering and AI-collaboration principles from
real projects rather than theory, so that other repos stay repos, not
philosophy.

Every rule here earned its place: it traces back to something that
actually happened on a real project, generalized until no
project-specific detail remained. Nothing is aspirational.

## License

Everything under `starter/`, docs and code alike, is licensed under
[MIT-0](LICENSE-starter) (MIT No Attribution): copy it into any
project, change it, and owe nothing, not even attribution. Outside
`starter/`, documentation (every `*.md` file) is licensed under
[CC-BY-SA-4.0](LICENSE-docs) and code (`tools/**` and scripts) under
[Apache-2.0](LICENSE). See [NOTICE](NOTICE) for the split by path.

## Purpose

Two jobs, one repo:

1. **A foundation for new repos and new projects.** `starter/` turns
   the principles into a starter kit, so a new repo begins with
   binding principles and the right shape instead of a blank page,
   whichever client or codebase it's for. A seeded project changes a
   principle only through its "Changing a principle" process.
2. **A place for architect-level thinking that doesn't belong in a project repo.** A project's own `AGENTS.md`, design docs and backlog
   describe *that* project. Cross-project judgment — what keeps
   recurring, what's worth changing about how sessions run — belongs
   here instead, so it doesn't pollute project repos with material that
   isn't about them.

## Layout

This repo dogfoods its own starter kit: its principles are `starter/`'s,
reached via the root `AGENTS.md`, and its agents, skills, rules and
settings are `starter/.claude/`'s, reached via the single root
`.claude` → `starter/.claude` symlink — see `AGENTS.md` for how this
repo itself is organized.

| Path | Contents |
|---|---|
| `starter/` | The exact tree a user copies into a new repo — everything below is inside it. |
| `starter/docs/principles/engineering.md` | Engineering principles: fail loudly, trust the PATH, credentials as pure injection, test first, and the rest — one rule, one reason, one way to apply it. |
| `starter/docs/principles/ai-working-process.md` | The AI working process: roles, work branches, merging, verification, delegation, briefing, and the lessons that shaped them. |
| `starter/docs/principles/context-economy.md` | Why always-loaded context, reads, dumps and long sessions drive cost, with the measured effect of each lever. |
| `starter/docs/principles/platform-notes/*.md` | Terse, reusable lessons and tool choices scoped to one platform (bash, containers, GitLab CI, Kubernetes/ArgoCD, Python, Terraform, test harnesses) — generalized past any one incident. |
| `starter/AGENTS.md`, `starter/CLAUDE.md`, `starter/.claude/`, `starter/docs/` | A root instruction file with the guardrails and one line per principle, subagent definitions, the architect and setup skills, and `docs/` skeletons including the decision log `docs/decisions.md` — everything a new repo needs to begin on this foundation. |
| `architecture/decisions.md` | This repo's own decision log (D1 onwards): why the starter is shaped the way it is. |
| `tools/` | The two check tools: `neutrality` (no client or private identifiers) and `starter-check` (`starter/` stays generic and its links resolve). Not part of the distilled model. |

## How to seed a new repo

1. Copy the whole `starter/` tree's contents into the new repo's root
   (`AGENTS.md`, `CLAUDE.md`, `backlog.md`, `docs/`, `.claude/`) and
   run the setup skill to fill in the project-specific parts. `AGENTS.md`
   stays small by design — the guardrails and one line per principle,
   each linking the full rule — so keep it that way rather than
   inlining content back into it.
2. Keep `.claude/agents/` and `.claude/skills/architect/` as-is; adjust
   an agent's lane only if the project genuinely needs a different
   one.
3. Fill in the `docs/` skeletons: `architecture.md` and `backlog.md`
   (architect-maintained, direct-push, never via a work branch — see
   `docs/principles/ai-working-process.md`), the append-only
   `decisions.md`, `glossary.md`, and `design/README.md`. Every
   decision in force in `architecture.md` cites its dated entry in
   `decisions.md`.
4. Use `.claude/rules/README.md`'s path-scoped rules for anything
   that applies to one area of the tree, instead of growing the root
   file.

None of this is copied once and forgotten — see below.

## How principles get updated

This repo is fed by the projects it seeds, not the reverse. When a
project surfaces a real, generalizable lesson — something that cost
time or broke something, then got fixed — that lesson flows back here,
stripped of the project's own names, dates and incident numbers, and
folded into the relevant principle or platform note. A rule that
turns out to be wrong, or too specific to generalize, gets corrected
or removed here too; this isn't a one-way accumulation.

Two things do NOT flow back here:

- **Incidents.** Keep the lesson, drop the incident — no client name,
  MR number, hostname, cloud account or date. If a lesson cannot be
  stated without them, it's not generalizable yet; leave it in the
  project.
- **Open decisions.** A question a project deliberately left open
  stays open there. This repo records settled principles, not pending
  arguments.

## Vocabulary

Where a source used a deliberate, exact phrase — "pure injection",
"the tested procedure IS the shipped procedure" — that phrase is kept
verbatim here too. Don't rephrase it into a synonym; the exactness is
the point (see "One word per concept" in `starter/docs/principles/engineering.md`).

## Neutrality check

This repo must never contain client, customer or private-project
identifiers. `tools/neutrality/` scans every git-tracked and staged
file against a local, gitignored denylist
(`.neutrality-denylist`, one case-insensitive regex per line) and
fails on any hit. To install it as a pre-commit hook:

```sh
cat > .git/hooks/pre-commit <<'EOF'
#!/usr/bin/env sh
set -eu
cd "$(git rev-parse --show-toplevel)"
uv run --project tools/neutrality neutrality-check
EOF
chmod +x .git/hooks/pre-commit
```
