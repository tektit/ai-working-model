# Decisions

Decision log for this repo's own structure and content — not a
project's decisions (those live in that project's own
`docs/decisions.md`, seeded from `starter/docs/decisions.md`).

## D1: Reject request-compressing proxies (caveman proxy) for agentic coding workloads

**Date:** 2026-09-25
**Status:** accepted

**Context.** Request-compressing proxies claim to cut token cost by
rewriting tool output (logs, diffs, search results) before it reaches
the model, while preserving the provider's prompt cache. One such
proxy, evaluated in local, loopback, official-integration mode
(`CAVEMAN_RECOVERY=mcp`), was tested against real Claude Code traffic
rather than taken on its published benchmarks.

**Decision.** Do not adopt request-compressing proxies for agentic
coding sessions. Replay of real captured sessions showed negligible
body reduction (0.005% pairwise, 0.08–0.35% over a 50-turn sequence),
even though a synthetic positive control confirmed the measurement
harness itself works (98% reduction there). A live A/B on a fixed
read/test/lint/fix task showed the proxy arm using more resources, not
fewer: +222% cache-read tokens, +177% output tokens, more turns, and
roughly 3x the wall time. The mechanism: the model detected
compression markers in tool output and spent extra turns re-verifying
content it no longer trusted, erasing any savings from the
compression itself.

**Consequences.** Context-cost reduction efforts should target context
size and call count — smaller always-loaded context, cheaper session
restart, fewer turns — rather than compressing what's already being
sent. Published vendor savings figures for this class of tool should
be read skeptically when they measure output terseness on short
Q&A prompts rather than tool-output-heavy agentic sessions, since that
is a different mechanism with different economics. This does not rule
out compression approaches that don't risk triggering
model-side re-verification (untested here); it rules out this specific
class as measured.

## D2: Only team-wide, low-friction cost optimizations

**Date:** 2026-09-25
**Status:** accepted

**Context.** Cost levers range from settings and repo structure to
custom tooling around the agent's internals (compaction hooks,
generated handoff notes, local-model sidecars). The latter only helps
the one person who installs and maintains it.

**Decision.** Pursue only optimizations a whole team gets by default:
committed repo structure (lean root instruction file, path-scoped
rules, lean kickoff commands, agent definitions with pinned models),
project or org-managed settings, and the templates in this repo. No
custom tooling that wraps or re-implements the agent's own behaviour.
Measurement tools stay optional instruments, not part of the setup.

**Consequences.** Handoff/compaction hooks and local-model augmentation
are dropped. Every recommendation must name where it is configured for
the team (committed file or managed setting). Personal settings are
used only to trial a lever before it is proposed team-wide.

## D3: Licensing

**Date:** 2026-09-25, revised 2026-10-06
**Status:** accepted

**Context.** This repo is brought to client engagements as bonus
material, and `starter/` is copied into customer repos and changed
there (D5). Its license terms must be explicit, and copying the
starter must put no obligations on the customer.

**Decision.** Everything under `starter/`, docs and code alike, is
MIT-0 (MIT No Attribution, `LICENSE-starter`). Outside `starter/`,
docs (every `*.md` file) are CC-BY-SA-4.0 (`LICENSE-docs`) and code
(`tools/**` and scripts) is Apache-2.0 (`LICENSE`). Copyright held by
Schlomo Schapiro / Tektit Consulting GmbH. No per-file license
headers; the split is recorded once, in `NOTICE`.

**Consequences.** A customer copies, changes and redistributes the
starter with no attribution, notice or share-alike duty; MIT-0's
warranty and liability disclaimer still applies. `starter/` itself
carries no license file and no copyright line: whatever is in it lands
in the customer's repo, where it would sit beside or replace the
customer's own license. `starter-check` fails on either.

## D4: Audience and targets

**Date:** 2026-09-25
**Status:** accepted; the product-owner role sentence superseded by D10

**Context.** The repo was written for one person's own projects. As
consulting material it now needs to work for other teams, including
people who are not engineers and cannot review generated code
themselves.

**Decision.** The audience is non-IT builders of internal expert tools
as well as engineering teams. The supported targets are Claude Code
(Team or Enterprise seats, optionally with API keys) and OpenAI Codex.
The guardrail model is architect mode plus the principles, enforced
mechanically — tests, CI — rather than by review, because a non-IT
user may not be able to review the code at all. The human stays the
product owner: the one who decides and merges.

**Consequences.** The instruction layer (`starter/AGENTS.md`, agent
and command definitions) should be tool-neutral rather than
Claude-Code-specific; that portability is not yet built and needs its
own research. The principles need a layer that a non-engineer can
read and apply, distinct from the current engineer-facing wording;
that rewrite is pending the owner's review and is out of scope for
this change.

## D5: Principles are copied into each project and evolve there

**Date:** 2026-09-25
**Status:** accepted

**Context.** A project needs its guardrails reachable without a path
to, or a network fetch from, this repo, and each project's context
differs.

**Decision.** Project setup copies `starter/docs/principles/` into the
project as its starting point; the project's copy then evolves with
the project.
The architect skill points only at the project's own copy, located via
the project's root instruction file.

**Consequences.** No live link back to this repo; improvements flow
back by hand, as lessons. Projects can drift from the model, which is
intended.

## D6: Work tracking is chosen per project at setup

**Date:** 2026-09-25
**Status:** accepted

**Context.** Target owners use git as the backend, with git-triggered
pipelines, but track work in different places (issues on the git host,
a `backlog.md`, Jira, or others).

**Decision.** The architect asks at project setup where work and
project management lives, recommends a default for the situation, and
records the choice in the root instruction file; "the backlog" means
that place from then on.

**Consequences.** The starter kit keeps `backlog.md` only as the
default for owners without a tracker. The skill must not assume any
one tracker.

## D7: The repo runs the starter's config through one `.claude` symlink

**Date:** 2026-10-05
**Status:** accepted

**Context.** This repo dogfoods `starter/.claude` through per-item
symlinks (`agents`, `skills/architect`, `settings.json`); the `setup`
skill and `rules/` were missing. Claude Code has no include mechanism
for skills or agents: nested `.claude/agents` are never discovered
from the root, nested skills only load lazily, and
`permissions.additionalDirectories` grants file access only.

**Decision.** The root `.claude` is a single symlink to
`starter/.claude` (KISS), checked by `starter-check`. Rejected:
committed copies with a drift check (every change shows twice in the
diff), and a local plugin (namespaced `/starter:…` names, cached copy
instead of live edits).

**Consequences.** Every starter skill, agent, rule and setting is live
here with no per-item upkeep. Claude Code's per-machine files are
written into `starter/.claude/` through the link, so the root
`.gitignore` excludes them. Symlinks need a platform that supports
them; Windows is not a target.

## D8: A principle changes only through a human's informed yes

**Date:** 2026-10-05
**Status:** accepted

**Context.** Setup recorded deviations in `AGENTS.md` while the
principles stayed untouched, so the two contradicted each other; and
nothing made sure a human understood what a principle change costs.

**Decision.** Every principle change, in the kit and in a seeded
project, follows "Changing a principle" in the starter's
`ai-working-process.md`: the rule now and after, two or three concrete
situations, the trade-off in business terms, what is hard to undo,
one check question, then the human's yes. The change edits the
principle in place, its one line in `AGENTS.md`, and a dated entry in
the project's `docs/decisions.md` (append-only, shipped by the kit),
in one change. Setup removes every template comment and unused
template section.

**Consequences.** Principles never drift silently and never carry a
second "deviations" layer. A principle change costs the human a few
minutes of reading; rulings that only apply a principle stay cheap.

## D9: Model and effort by the cost of an undetected mistake

**Date:** 2026-10-05
**Status:** accepted; the reviewer's Sonnet pin superseded by D13

**Context.** "Fable only when the owner asks" was caution, not
evidence; the model A/B compared only Sonnet and Opus on bounded
briefs. Agents pin a model, and Opus 5.5 defaults to `medium` effort.

**Decision.** Four tiers, named the same everywhere: cheapest, standard,
strong, top (Claude Code: Haiku, Sonnet, Opus, Fable). The tier is
chosen by what an undetected mistake would cost; the architect picks
the top tier on its own judgment with a one-line reason; effort is
raised before the tier. Each narrow-lane agent pins model and effort
(builder, locator, scribe: Sonnet medium; reviewer: Sonnet high; new
analyst: Opus xhigh, read-only analysis); a delegation overrides the
model only upward; an unpinned agent always gets an explicit model.

**Consequences.** Fable costs about 2.5x Opus per token (2026-10).
Every top-tier review notes whether it found something a lower tier
would have missed; after about ten, revisit the top tier's scope.
Quota weight per model on Team seats stays unknown.

## D10: Every agent obeys `AGENTS.md`; every human is equal

**Date:** 2026-10-05
**Status:** accepted; the "about 1k words" figure for `AGENTS.md`
superseded by D13

**Context.** Guardrails lived partly in the architect skill, so a
plain session never saw them; the principles read as optional
"defaults"; the docs used human, owner and product owner for one
concept.

**Decision.** The starter's `AGENTS.md`, loaded by every session and
every working subagent, carries the guardrails plus one line per
principle with a link to its section (about 1k words), not the full
principle text (about 7k tokens, and ignored by Codex as an import).
`starter-check` fails when a principle heading is missing, duplicated
or dangling there. The engineering principles are binding; stack
specifics live in platform notes, all kept. A session not in the
architect role is task-briefed; the architect role is division of
labour plus the agent a human thinks things through with. Every human
is equal: any may decide, review and merge; agents assume no role and
no skill level and explain in plain words. This replaces D4's "the
human stays the product owner"; D4's audience stays as decided.

**Consequences.** Guardrails bind every session at a cost of about 1k
always-loaded words. Whether one-line rules steer a plain session as
well as full text is judgment, not measured.

## D11: Lessons from the 2026-10-05 retrospective

**Date:** 2026-10-05
**Status:** accepted; the rule-loading sentence superseded by D13

**Context.** In one session the human repeatedly found behavior that
was implied but written nowhere an agent reads it; piecemeal rule
edits piled up 46 contradictions until one top-tier audit; summaries
(a research agent, a fetch tool) inverted two Claude Code facts. A
separate cost-optimization session contributed measured findings on
root-file size, tool listings, path-scoped rule loading and settings
precedence.

**Decision.** New starter principles: write a behavior, with its
literal command, where the acting agent reads it; finish a series of
rule edits with one consistency pass, top tier by default. "Verify"
treats research reports, fetch summaries and a model's self-report as
claims; brief facts say how they were verified. Context economy:
tool, MCP and plugin listings count as always-loaded; path-scoped
rules load only through file tools in the starting checkout, so a
brief names the area's rule files; a committed setting overrides user
settings, personal values go in the uncommitted project-local file.
Setup warns when a personal skill or command shadows the project's.

**Consequences.** The architect states after each merged change
whether the next job belongs in a fresh session. The effect of
disabling unused tool listings, and of compact command output on a
whole session, is not measured.

## D12: A paid run needs a go-ahead naming who pays

**Date:** 2026-10-05
**Status:** accepted

**Context.** On 2026-09-25 the model A/B and the caveman live runs
(scripted `claude -p` calls) were billed to the wrong account, and
the login status did not show which. No principle covered spending on
a model account.

**Decision.** Through "Changing a principle": a paid run (a script,
tool or test run making its own model calls, or calling another
per-use-billed API) touches a live system, the account that pays.
Before each one an agent states what runs, its rough cost and whether
a credential is set in its environment, and asks which account pays;
the go-ahead names that account, per run, like any live-system
go-ahead. The starter's "Live systems" principle and its guardrail
line in `AGENTS.md` carry it.

**Consequences.** No paid run starts unattended, overnight runs
included, until a human names the account. A session's own work and
its subagents are unaffected. Seeded projects that copied the
principles before this change don't get it automatically (D5). The
2026-09-25 owner ruling "no more paid experiments" stays in force on
top of this.

## D13: Lessons from comparing two other working setups

**Date:** 2026-10-08
**Status:** proposed

**Context.** A comparison of this kit with two AI working setups in
real use found practices the kit lacked: known failures keyed by error
text, evidence labels on claims, proof of reach before reporting
absence, load discipline for read-only probes, a recorded write level
for agents, a commit attribution policy, a precedence rule for
auto-memory, adversarial review of every change. It also found the
kit stating things that contradicted observed behavior or each other:
rebase plus forced push as the only branch update, rules that "never"
load through the shell, isolation in "a clone or worktree".

**Decision.** The human ruled on four setup questions. Branch updates
follow the merge method, with squash merges the setup default: under
squash or plain merge commits, a branch catches up by merging the
trunk in (under squash those merges never reach the trunk); only a
trunk that must be linear without squashing rebases, and only an
unshared branch (no open review, no other clone), pushed with
`--force-with-lease`. Agents at most push work branches and open draft
MRs/PRs, the recommended of three write levels, so they can iterate on
real CI results before a human reviews; present credentials are not
consent, and below that level every "push" in the kit, the
architect's direct trunk push included, becomes a local commit a
human pushes. AI-written commits name the model as co-author and
MR/PR descriptions carry a generated-with line, by default; in Claude
Code that is the unset `attribution` setting, a default rather than
an enforced policy. Auto-memory never points into the working copy.
Adversarial and delta reviews run on the highest tier available,
never a middle one, so the reviewer agent is pinned to the top tier.
Folded in with these: a `docs/troubleshooting.md` skeleton;
evidence labels and the reach proof in "Verify"; load discipline in
"Live systems"; answers recorded in the facts they settle, no question
pages; local hooks as feedback, never the gate; times with an explicit
zone; deliberate omissions recorded as decisions; a new principle
"Every change gets an adversarial review"; a new principle "The repo
is shared truth; auto-memory is personal"; rule globs scoped to their
area, never a catch-all; never relying on a rule loading by itself;
one isolation rule, a fresh clone, stated the same everywhere; one
list of architect-maintained files that agent definitions point at.

**Consequences.** Setup asks three more questions (write level,
attribution, time zone) and the merge method, and `attribution` is the
one setting it may write. The starter's `AGENTS.md` grows from about
1,090 to 1,220 words (186 lines), which replaces D10's "about 1k
words". Every MR/PR now costs at least two top-tier reviewer runs,
the adversarial review and a delta review, plus one more delta review
for each round that leaves a finding open; each run costs more than
it did on the standard tier (the top tier is about 2.5x the strong
tier per token, D9), and the stop condition, a delta review that
closes every finding and raises none, is what bounds the total. A
drift check between a fact index and the files holding the full text
stays written guidance: the starter ships no facts, so a check in
`starter-check` would test nothing, and seeded projects don't get
`tools/`. The fact storage model (headlines in the root file versus
one fact per file) is not decided here; the "Facts that bite"
placeholder stays as it is until the two approaches are evaluated for
answer quality. Seeded projects don't get any of this automatically
(D5).

## D14: Stated design goals for humans and agents

**Date:** 2026-10-08
**Status:** proposed

**Context.** The principles said what to do, rule by rule, but not
what the whole model is built to achieve, so neither a human nor an
agent could weigh one rule against another, cost included.

**Decision.** Six design goals, derived from the existing principles
and adding no rule of their own: quality first; the human decides
and merges; cost-aware by design (the cheapest adequate tier per job
and the top tier for reviews and novel design, a budgeted
always-loaded context, a test suite or pipeline run once per change,
decisions batched at milestones); transparent (attribution, the
decision log, current MR/PR descriptions, evidence labels); the
tested procedure IS the shipped procedure; portable and neutral. They
live in the starter's `docs/principles/design-goals.md`, each with
the principles that carry it and one line on what it asks of a human
and one on what it asks of an agent. The README names them, and the
starter's `AGENTS.md` links them in one line. Where cost and
correctness pull apart, correctness wins, as "Delegation" already
says.

**Consequences.** A new principle or a change to one is checked
against the goals it serves. The goals are not covered by
`starter-check`'s principle-line drift check, so the reviewer keeps
their "carried by" references current. The starter's `AGENTS.md`
grows by one line.

## Format

```
## D<n>: <short title>

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | superseded by D<m>

**Context.** What prompted this — the situation that made a decision
necessary, stated as fact, not narrated as an argument.

**Decision.** What was decided, stated plainly.

**Consequences.** What this makes easier, what it makes harder, and
anything it forecloses that's worth knowing later.
```

Entries are numbered sequentially and never renumbered; a superseded
entry stays, marked superseded, pointing at what replaced it.
