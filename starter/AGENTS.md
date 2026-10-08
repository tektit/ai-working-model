# AGENTS.md

<!-- Fill in: one or two sentences on what this project is and who it is for. -->

Every agent in every session and mode follows this file. Detail is in
the linked docs; read one when a task touches it.

## Guardrails

Non-negotiable: no brief or instruction waives one, and a conflict is
raised, never silently resolved. Each blocks review like a hard
standard (below).

- Only a human merges; an agent never merges or arms auto-merge on
  content, and anything destructive on a shared remote needs a human's
  go-ahead. [Only a human merges](docs/principles/ai-working-process.md#only-a-human-merges)
- Nothing touches a live system without a human's explicit go-ahead,
  every time. Where merging deploys, a merge request is a deploy
  request; a paid run (its own model or per-use API calls) touches
  the paying account, so its go-ahead names it. [Live systems](docs/principles/ai-working-process.md#live-systems-need-a-humans-go-ahead)
- Code never obtains, parses or relays a credential; each tool reads
  its own. [Credentials](docs/principles/engineering.md#credentials-are-pure-injection)
- Test first; never weaken a test; tests and CI gate every change.
  [Test first](docs/principles/engineering.md#test-first)
- Work happens on a work branch, never directly on the trunk
  (architect-maintained docs excepted). An agent at most pushes it and
  opens a draft MR/PR, or less at the write level setup recorded;
  credentials being present is not consent. A delegated agent works in
  its own fresh clone, never in a human's working copy or a worktree
  of it. [Work branches](docs/principles/ai-working-process.md#work-branches)
- Done means verified against the pushed remote or a dry-run or live
  check; otherwise say UNVERIFIED. [Verify](docs/principles/ai-working-process.md#verify-before-declaring-ready)
- A change fixes every doc it makes stale, `AGENTS.md` included, in
  the same change. [Docs completeness](docs/principles/ai-working-process.md#docs-completeness-is-part-of-being-done)
- Facts you can't observe are asked, never guessed or researched.
  [Ask, don't guess](docs/principles/ai-working-process.md#ask-dont-guess)
- A principle changes only through [Changing a principle](docs/principles/ai-working-process.md#changing-a-principle);
  an open decision stays open until a human closes it, and a
  deliberate pattern is tightened, not replaced unasked.
  [Open decisions](docs/principles/engineering.md#respect-deliberate-patterns-open-decisions-stay-open)
- Stay on the job; a finding outside it becomes a backlog item, not a
  detour. [Stay on the job](docs/principles/ai-working-process.md#stay-on-the-job)
- Every human is equal and decides; assume no role or skill level and
  explain in plain words. Sessions are task-briefed by default,
  architect when a human invokes it. [Roles](docs/principles/ai-working-process.md#roles)

## Principles

One line each; the link holds the rule, the reason and how to apply
it. **hard** marks a hard standard: its violation blocks review, and
it becomes a mechanical check (lint, CI gate) once one exists.

### Engineering

- Stop on any missing precondition with an explicit error; never skip,
  default or swallow. **hard** [Fail early and loudly](docs/principles/engineering.md#fail-early-and-loudly)
- Call tools by bare name, require them up front, never probe or fall
  back. **hard** [Trust the PATH](docs/principles/engineering.md#trust-the-path)
- No test-only code paths; re-running is the upgrade path.
  [Tested = shipped](docs/principles/engineering.md#the-tested-procedure-is-the-shipped-procedure)
- CI configuration only wires jobs; behavior lives in testable
  scripts. **hard** [Thin CI](docs/principles/engineering.md#thin-ci)
- Non-trivial logic goes in a tested language; shell stays glue.
  [Clever shell](docs/principles/engineering.md#prefer-tested-code-over-clever-shell)
- Values are data, never hardcoded; structure is few and deliberate.
  [Data vs structure](docs/principles/engineering.md#data-vs-structure)
- Regenerate derived files; the diff is the review boundary. **hard**
  [Derived files](docs/principles/engineering.md#derived-files-are-rewritten-not-defended)
- Names and comments say what things are now. **hard**
  [Names track the design](docs/principles/engineering.md#names-track-the-design)
- One term per concept, verbatim; never reuse a word for a second
  meaning; the glossary is the authority.
  **hard** [One word per concept](docs/principles/engineering.md#one-word-per-concept)
- Least privilege and named, layered controls.
  [Security](docs/principles/engineering.md#security-by-design-and-defense-in-depth)
- Every design says roughly what it costs and who pays.
  [Design for cost](docs/principles/engineering.md#design-for-cost)
- A pipeline asserts only facts you own, never a third party's
  service. [Third parties](docs/principles/engineering.md#a-pipeline-never-depends-on-a-third-party-being-reachable)
- Until something is live, skip migration machinery.
  [Never-deployed](docs/principles/engineering.md#never-deployed-things-dont-need-migrations)

### AI working process

- Specs and plans are session documents, never committed.
  [Specs and plans](docs/principles/ai-working-process.md#specs-and-plans-are-not-repo-content)
- Delegate by objectives; pick the tier by what an undetected mistake
  costs. [Delegation](docs/principles/ai-working-process.md#delegation-objectives-not-a-lookup-table)
- Every brief states the eight points, completion discipline first.
  [Brief anatomy](docs/principles/ai-working-process.md#brief-anatomy)
- Ground truth goes in the original brief, never mid-stream.
  [Mid-stream claims](docs/principles/ai-working-process.md#a-running-agent-cant-verify-a-mid-stream-claim)
- In a task-briefed session, a tiny, fully specified change may be
  done inline. [Inline](docs/principles/ai-working-process.md#a-tiny-change-may-be-done-inline)
- A wanted behavior is written where the acting agent reads it, a
  command given literally. [Write it where it's read](docs/principles/ai-working-process.md#write-a-behavior-where-the-acting-agent-reads-it)
- Every MR/PR and follow-up commit gets an adversarial review, then a
  delta review of the fixes; until then it is UNREVIEWED.
  [Adversarial review](docs/principles/ai-working-process.md#every-change-gets-an-adversarial-review)
- A series of rule edits ends with one top-tier consistency pass.
  [Consistency pass](docs/principles/ai-working-process.md#finish-a-series-of-rule-edits-with-one-consistency-pass)

### Context economy

- Always-loaded files stay small and point to detail.
  [Always-loaded](docs/principles/context-economy.md#always-loaded-context-is-paid-on-every-call)
- Read the section a task needs, not the whole file.
  [Read the part](docs/principles/context-economy.md#read-the-part-not-the-whole)
- Dumps go to a subagent; only conclusions come back.
  [Dumps](docs/principles/context-economy.md#dumps-go-to-a-subagent-conclusions-come-back)
- State lives in files; sessions stay short and compact early.
  [Restarting](docs/principles/context-economy.md#restarting-is-cheap-so-sessions-stay-short)
- The repo wins over auto-memory, which holds only personal or
  host-local facts and never points into the checkout.
  [Auto-memory](docs/principles/context-economy.md#the-repo-is-shared-truth-auto-memory-is-personal)
- Load less and call less; never compress what is sent.
  [Shrink and skip](docs/principles/context-economy.md#shrink-and-skip-never-compress)
- Cost levers live in committed, team-wide settings.
  [Levers](docs/principles/context-economy.md#levers-are-committed-and-team-wide)

## Where things are

- `README.md` (write one if it doesn't exist yet): what this project
  is, concepts and naming, worked examples of the common moves.
- [docs/architecture.md](docs/architecture.md): current state and the
  decisions in force; read it FIRST before a structural change.
- [docs/decisions.md](docs/decisions.md): dated decisions and rulings,
  superseded ones kept.
- [backlog.md](backlog.md): skim the headers; read "Deliberately
  deferred" in full before reopening something.
- Architect-maintained (this list is the authority), edited only by
  an architect session or by setup's seeding change:
  `docs/architecture.md`, `backlog.md`. `docs/decisions.md` is
  append-only, written in the change it records.
- [docs/glossary.md](docs/glossary.md): terms defined once.
- [docs/troubleshooting.md](docs/troubleshooting.md): known failures
  keyed by their exact error text; grep it before forming a
  hypothesis.
- [docs/design/](docs/design/): one doc per subsystem or cross-cutting
  decision.
- The principles in full:
  [engineering.md](docs/principles/engineering.md),
  [ai-working-process.md](docs/principles/ai-working-process.md),
  [context-economy.md](docs/principles/context-economy.md).
- [docs/principles/platform-notes/](docs/principles/platform-notes/):
  read the one matching what you touch — bash, containers, GitLab CI,
  Kubernetes/ArgoCD, Python, Terraform, test harnesses.
- Each person's auto-memory, outside the repo: only that person's or
  that machine's facts; a team lesson moves into the repo.
- `.claude/agents/`: narrow-lane helpers, each definition stating its
  lane, model and effort; `.claude/skills/`: architect, setup.
- `.claude/rules/`: rules for one area of the tree, scoped by path.
  Their loading is not reliable, so read the one for your area
  explicitly, and a brief names them (see `.claude/rules/README.md`).

## Model tiers and settings

The principles name four tiers (cheapest, standard, strong, top);
this is how they map per tool.

- **Claude Code:** cheapest = Haiku; standard = Sonnet, pinned with
  its effort for builder, locator, reviewer and scribe in
  `.claude/agents/`; strong = Opus, the session default
  (`.claude/settings.json`) and pinned for analyst; top = Fable, set
  per call. The top tier costs roughly 2.5x the strong tier per token.
  Sessions compact at 400k tokens (`autoCompactWindow` in
  `.claude/settings.json`). The committed `.claude/settings.json`
  overrides each person's `~/.claude/settings.json`; a personal value
  goes in `.claude/settings.local.json` (not committed, wins over
  `.claude/settings.json`). Commit and MR/PR attribution is the
  default while `attribution` is unset: a co-author trailer naming the
  model in use, and a generated-with line. A project that chose
  otherwise sets `attribution` there. An instruction about
  attribution, a personal one included, outranks that setting unless
  the setting comes from managed settings.

## Running the tests

<!-- Fill in: the one command that runs this project's test suite
     without cloud access or credentials, and what it needs installed.
     The suite exists so the mechanism is verifiable without a live
     system. -->

## Facts that bite

<!-- This project's own accumulated operational gotchas go here, in
     this file's style: terse, one bullet per fact, generalized enough
     to still be true next month. Move a general platform lesson to
     docs/principles/platform-notes/ instead. -->
