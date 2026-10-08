# AI working process

How AI-assisted work runs in this project. A principle changes only
through "Changing a principle" below.

## Roles

- **Human:** any person working on this project, as opposed to an
  agent. Every human is equal: any may decide, review and merge.
  Agents assume no role and no skill level: they treat each human as
  the one who decides, and explain in plain words by default. Tests,
  CI and verification keep the software production grade, not a
  human's code review.
- **Task-briefed agent**, the default mode: a subagent, a headless or
  scheduled run, or an interactive session not in the architect role.
  Its brief comes from whoever started it: the delegating session, or
  the human's own instructions in an interactive session. The brief
  defines its scope; it implements, and nothing asks it to delegate
  onward.
- **Architect**, the other mode: a role a human invokes explicitly,
  never by default. The architect divides work across subagents and
  is the agent the human thinks things through with: it plans,
  delegates, verifies agent work against the pushed remote and keeps
  its own thread conversational. It implements only a tiny,
  time-critical fix while a human is blocked live.

The two modes, task-briefed and architect, add nothing to and remove
nothing from the guardrails (listed in [AGENTS.md](../../AGENTS.md)):
they and these principles bind every agent in every session and mode.
A brief cannot waive one; an agent whose brief conflicts with one says
so rather than silently picking a side.

## Work branches

- Work happens on a work branch, one per change, off the trunk (the
  repository's default branch), merged through review, deleted after
  — never directly on the trunk. The architect-maintained docs are the
  one exception ("Docs completeness is part of being done" below).
- How far an agent writes to the repo is chosen at setup, one of
  three levels: it pushes work branches and opens draft MRs/PRs
  (recommended); it commits locally only and a human pushes; or it
  writes nothing to the repo without a per-change instruction. The
  recommended level lets an agent iterate on real CI results by itself
  — push, read the pipeline, push a fix — before a human spends review
  time on it. At every level, credentials that happen to be present
  are not consent, and neither is a request to "fix it": the level and
  the brief set what an agent may write, and only a human merges.
  Wherever these principles, the root instruction file, an agent
  definition or a brief say "push" or "the pushed remote", read it at
  the recorded level: below the recommended one, an agent stops at a
  local commit, verifies against that commit and leaves the push to a
  human, and that includes an architect's direct push of its docs to
  the trunk.
- A delegated agent works in a fresh clone made for it, never in a
  human's working copy and never in a worktree of it: a checkout or
  a reset in a human's working copy moves files under someone
  mid-edit, and a worktree shares that working copy's git metadata, so
  a branch checked out in one can't be checked out in the other (in
  Claude Code, this rules out `isolation: worktree`). An interactive
  session a human starts in their own working copy works there.
- No stacked branches unless technically forced; prefer serializing
  overlapping work rather than parallel branches touching the same
  files.
- Rework an existing branch by adding commits, not by amending and
  force-pushing — review stays readable and nothing already reviewed
  is rewritten. Beyond rebasing an unshared branch (below), a forced
  push is only for scrubbing an accidentally committed secret.
- When the trunk moves under an open branch, how the branch catches
  up follows the repo's merge method, recorded at setup. What decides
  it is whether the trunk must stay linear without squashing:
  - **Squash merges** (the setup default): bring the trunk in with a
    plain `git merge` and push that like any other commit. Once the
    branch is pushed, don't rebase it, and don't force-push except to
    scrub a committed secret. Squashing turns the whole branch, these
    merges included, into a single trunk commit, so the trunk stays
    linear and nothing is rewritten.
  - **Merge commits**, where the trunk keeps every commit and need not
    be linear: the same plain `git merge` and an ordinary push.
  - **A linear trunk without squashing** (rebase or fast-forward-only
    merges): rebase onto the trunk only while the branch is unshared,
    meaning it has no open review and no other clone holds it, or you
    never pushed it; otherwise ask first. Push the result with
    `--force-with-lease`.

  Rewriting a pushed branch strands every other clone, worktree and
  running agent that holds it on commits that no longer exist, can
  detach review comments from the code they were about, and brings
  each conflict back once per replayed commit, where a merge settles
  it once. Update locally and never use the hosting site's
  rebase-update button, which rewrites the remote branch behind every
  local copy; its merge-update button only adds a commit that a normal
  pull picks up. If the update can't be resolved cleanly, stop and
  ask.
- By default, what an agent authors says so: each commit carries a
  co-author trailer naming the model, and each MR/PR description a
  generated-with line. Setup records the project's choice; the tool's
  setting carries it where one exists (the root instruction file names
  it per tool). Under squash merges, the per-commit trailers reach the
  trunk only if the host's squash commit message keeps them; whether
  it does depends on the host and its template (UNVERIFIED per host:
  check the template before relying on it).
- A review artifact (an MR/PR description) describes the change **as
  it currently stands**, rewritten on every substantive change — never
  an append-only log of attempts. Humans review a change through its
  description, not its code, so it is written for them: honest,
  complete and current with the diff; stale narration of a superseded
  approach actively misleads. Like any report, it is a claim (see
  "Verify before declaring ready"), which the adversarial review
  checks against the diff on the human's behalf. Read a generated
  description back after creating it: a quoting or templating bug can
  ship a literal placeholder.
- Before pushing further rework to an existing branch, check whether
  it has already been merged — a human can merge while an agent is
  still working. If it has, don't push to a dead branch; start a fresh
  work branch off the now-current trunk instead.

## Only a human merges

An agent never merges a content change and never arms auto-merge on
one — only on pure bookkeeping, and only if a human set that up
themselves. Anything destructive on a shared remote, such as
force-pushing over someone else's work or deleting a branch you
didn't create, needs a human's explicit go-ahead; the one exception
is rebasing an unshared branch (no open review, no other clone; see
"Work branches"). The merge is the moment a human accepts the change;
an agent that merges removes it.

## Live systems need a human's go-ahead

Nothing touches a real, live system (deploy, apply, delete, migrate)
without a human's explicit go-ahead, every time; an earlier go-ahead
does not carry over. Where merging deploys, a merge request is a
deploy request: say so when asking for it. The test suite exists so
the mechanism is verifiable without a live system.

A **paid run** touches a live system too: the account that pays. A
paid run is any script, tool or test run that makes its own model
calls (headless agent sessions, model API calls) or calls another API
billed per use; a session's own work, its subagents included, is not
one. A script bills whatever credential its environment hands it,
possibly another project's key, and a login status may not show
which. So before each paid run, state what it runs, roughly what it
costs and whether a credential is set in its environment (a presence
check, never the value), then ask which account pays; the go-ahead
names that account.

**A read can still do harm.** A diagnostic read puts load on the
system it reads, and parallel sessions multiply that load. Before
probing a live system, look at how much spare capacity it has; keep
heavy calls sequential; address one named node rather than an address
behind a load balancer; give every log read a limit (a time window or
a line count); and when parallel sessions need the same system,
settle who probes it and when.

## Verify before declaring ready

- **Never declare something done, working, or shippable until it is
  empirically verified** — against the pushed remote, a real dry-run,
  or a live check, not against your own memory of what you intended to
  do. State **UNVERIFIED** and go check, rather than presenting a
  confident guess as fact. A claim that can't be checked is labeled as
  such, not smoothed over.
- **A report is a claim, not evidence** — your own, and any agent's,
  an MR/PR description included. Before relying on or relaying a
  number, a line citation, a root cause, or a "pushed" claim, re-check
  it in the current turn: fetch the remote and look at the actual tip
  and diff. Repo state moves underneath you, and agents park mid-task
  more often than they should; the work is often correct while the
  report of it is not.
- **A branch or a review link existing is not evidence that work
  happened — the diff is.** Confirm there actually is a non-empty diff
  against the trunk before treating a change as real.
- Run a test suite once per meaningful change, with its exit code
  captured directly (see
  [platform-notes/test-harnesses.md](platform-notes/test-harnesses.md)).
- When two explanations for a symptom seem equally plausible, don't
  ping-pong between theories — add instrumentation (a timestamped
  value, a self-evidencing log, a direct probe) and let one run
  discriminate.
- Read the artifact that actually drives a decision, not a summary of
  it — a compressed summary or a grep fragment drops exactly the
  discriminating detail that would change the conclusion. A research
  agent's report, a summarizing fetch of a web page and a model's own
  account of what it saw or did are summaries too: confirm a fact that
  drives a decision in the raw primary text or, for what an agent did,
  in the session transcript — summaries have inverted a setting's unit
  and misreported where a tool loads files. For anything
  that will be quoted onward (to a vendor, to settle an argument,
  in a report someone else acts on), read the primary source end to
  end rather than keyword-searching it.
- Before forming a novel hypothesis, search first: grep the project's
  own docs for the symptom, starting with the exact error text in
  [docs/troubleshooting.md](../troubleshooting.md), and name the
  nearest working instance of the same thing to diff against. A
  recorded, already-solved case outranks a fresh theory every time.
- **"Nothing found" needs proof that the search could find
  something.** A scope the agent can't reach or isn't authorized for
  often answers with nothing, indistinguishable from a scope that is
  really empty. So a "none found" report comes with one successful,
  authenticated call into that same scope. A sum, count or list that
  comes back empty or null is itself something to explain, never a
  silent zero.
- **A factual claim carries its evidence label.** A claim about the
  project's own systems or a vendor's behavior, in the full text of a
  fact or rule or in a report, says how it is known, in these words,
  verbatim: *observed live, <date>*; *read in the code*; *inferred*;
  *reported, unchecked*; *confirmed by <who>, <date>*. The label
  sits in the full text, not in an always-loaded headline. An undated
  claim silently goes stale, and an unlabeled one reads as stronger
  than its evidence; treat an unlabeled claim as UNVERIFIED.

## Every change gets an adversarial review

**Rule:** no MR/PR is called ready, and no later commit added to it
either, before an adversarial review: a reviewer told to find what is
wrong, not to confirm what is right. Docs and config changes are no
exception. The review checks the MR/PR description against the diff,
claim by claim, because a human reviews through the description, not
the code. Once its findings are fixed, a delta review looks only at
the fixes and states for each finding whether it is closed. A delta
review that closes every finding and raises none ends the loop;
anything else goes back for another fix and another delta review.
Until the loop has ended, the change is reported as UNREVIEWED, even
when it is verified.
**Why:** the author, human or agent, reviews what they meant to write,
not what they wrote; small follow-up commits and "just docs" changes
are where unreviewed mistakes slip through, because they look too
small to check.
**How:** the read-only reviewer agent (`.claude/agents/reviewer.md`),
pinned to the top tier, runs both the review and every delta review,
on the highest tier available to the project, never a middle one. Its
findings go back to whoever wrote the change; the reviewer never
fixes them itself.

## Docs completeness is part of being done

A change that makes a README, the root instruction file, a glossary,
or a design doc stale or incomplete fixes it in the same change —
sweep for every assertion the change invalidates. "Docs follow-up
later" is a rejected pattern; a doc that's wrong is worse than a doc
that doesn't exist, because it's trusted.

The root instruction file ([AGENTS.md](../../AGENTS.md)) is the
always-loaded summary of the guardrails, the principles, the agents
and model tiers, and the per-tool settings. A change that adds,
removes, renames or changes one of those (a principle, an agent
definition, a skill, a setting it describes) updates `AGENTS.md` in
the same change. **How:** a drift check, where the project has one,
enforces the principles part mechanically (every principle heading
linked exactly once); the reviewer checks the rest. The same holds for
any always-loaded index of facts whose full text lives elsewhere:
every headline reads the same, word for word, in the index and in the
file holding its full text, occurs once in each, and changes in both
places together. Hand-kept pairs drift, so propose a drift check of
the same shape once the project has such an index.

The architect-maintained docs (listed in [AGENTS.md](../../AGENTS.md),
the one authority) are edited only by an architect session, by direct
push to the trunk, or by setup in its one seeding change; a work
branch that invalidates something in one of them flags it instead of
editing it. That direct-push channel carries docs only, so it can't
smuggle in a behavior change unreviewed. An agent definition or skill
that needs this list points at it rather than copying it; where a
copy can't be avoided, every copy is identical and changes with the
list in the same change, since a copy that drifts leaves one agent
free to edit a file another treats as protected.

[docs/decisions.md](../decisions.md) is append-only: an entry is
written after a human's yes, in the same change as what it records
(a principle edit on its work branch, a ruling, a decision an
architect session records).

## Ask, don't guess

Facts outside what an agent can observe are asked, never guessed or
researched: org facts (licenses, contracts, vendors, existing
systems), a human's preferences, the business goal and constraints,
budgets and deadlines, and the local environment and how credentials
reach a command. One question to the person who knows is far cheaper
than a string of failed guesses, and a researched answer about this
organization is still a guess. "Not known yet" is a valid answer;
record it as exactly that.

An answer is written into the fact it settles, labeled *confirmed by
<who>, <date>*. Pages, tables or numbering schemes that track
questions have no place in the repo, since they outlive their context:
an open question is one backlog item, and an unknown is stated
plainly where it matters. Team-facing docs spell names and terms out
rather than using abbreviations only their author knows.

## Stay on the job

One job per session or brief. A finding outside it becomes one
backlog item and a one-line mention, never a detour: a detour spends
context and a human's review attention on work nobody asked for, and
the backlog keeps the finding from getting lost.

## Specs and plans are not repo content

A spec (the what/why) and a plan (the how, task by task) are **session
working documents**. They exist while the work does, they steer it,
and they are not committed anywhere in the repo.

The reason is what committed docs are *for*: they're the grounding
truth for whoever reads the repo next, human or AI. A spec is stale
the moment its implementation lands — it describes an intention, while
everything else in the repo now describes the result. Committing it
anyway means the repo starts lying to the next reader.

What genuinely survives a change goes to one of three places instead:

- A lasting architectural decision → an entry in
  [docs/decisions.md](../decisions.md), and a design doc if it needs
  more room — not a spec repurposed.
- The task breakdown and how each task was verified → the review
  artifact's description, which "Work branches" already requires to
  stay current.
- Deferred work or an open question → the project's backlog, never an
  ephemeral hand-off message that gets lost when the session ends.

## Changing a principle

These principles evolve with the project, but none changes silently:
not by the architect, not by setup, not as a side effect of other
work. Wording alone hides what a change costs, so the proposal to the
human shows:

- the rule now and the rule after;
- two or three concrete situations in this project, and what an agent
  does in each before and after;
- the trade-off in business terms: what gets faster or cheaper, what
  gets riskier, who is affected;
- what becomes hard to undo.

Then one check question built on a concrete scenario, so the human
confirms the consequence, not just the wording. Only after their yes
is the principle edited, on a work branch, in one change that also
updates the principle's line in [AGENTS.md](../../AGENTS.md) and
appends a dated entry to [docs/decisions.md](../decisions.md).

A **ruling** is a human's decision on how a principle applies here,
without changing it. It gets a dated entry appended to
[docs/decisions.md](../decisions.md) and applies project-wide, not
only where it was raised.

Example: the human wants no test-first for a prototype. Now, per
"Test first" in [engineering.md](engineering.md), every behavior
change starts with a failing test; after, prototype code ships
untested, and a pricing bug is found by a customer instead of by CI.
The first weeks go faster; if the prototype becomes the product, its
tests are retrofitted. Check question: "If the prototype becomes the
product, the missing tests cost about a week. Acceptable?"

## Delegation: objectives, not a lookup table

Whether to work inline or hand off to a subagent, spawn fresh or
resume, and which model to use are judgment calls made in service of
a few objectives — re-evaluate against these rather than applying a
rule mechanically past the point it stops serving them:

- **Keep the thread responsive while a human is live.** A long inline
  tool sequence makes someone watch output they didn't ask to watch;
  background work keeps a live conversation conversational.
- **Keep the delegating session's context lean.** It should consume
  conclusions, not the file dumps and search noise it took to reach
  them.
- **Spend the lowest model tier that's adequate** — one objective
  among several, never the only one.
- **Correctness always wins.** Never economize on model, delegation,
  or shortcuts where a mistake is costly — verification against the
  pushed remote is what makes cheaper delegation safe in the first
  place.
- **Preserve built-up context.** An agent that already investigated an
  area holds context a fresh one would have to rebuild from scratch.

From weighing these together, a few heuristics follow:

- A one-off probe or a lookup you can answer directly stays inline —
  a background agent's own spin-up cost would exceed the task, and
  there's no one waiting on you to hide it behind. An open-ended
  investigation sweep, or building an artifact (a patch, a doc
  rewrite, bookkeeping), is substantial enough to delegate — especially
  with a human live in the thread.
- Prefer resuming a still-relevant agent over spawning a fresh one for
  a closely related follow-up; spawn fresh when the area has genuinely
  moved on.
- Pick the model tier by what an undetected mistake would cost, not
  by the task's label. Four tiers, named the same everywhere (the root
  instruction file maps them to models per tool):
  - **cheapest:** a fully specified edit that a diff check catches;
  - **standard:** a bounded brief whose mistakes tests or checks
    catch;
  - **strong**, the session default: judgment across several parts,
    with mistakes visible in review;
  - **top:** mistakes that would be silent and expensive — a novel
    design that is expensive to change later (data model, security
    boundary, interfaces), every adversarial review and delta review,
    the analysis behind a principle change, the consistency pass
    after a series of rule edits, a tie-break when two strong-tier
    attempts disagree or fail.

  A precise brief that avoids rework is worth more than a cheap model
  that has to be corrected twice.
- A narrow-lane agent runs on the model and effort pinned in its
  definition. A delegation overrides the model only to raise the
  tier, stating the reason in one line, or, where the pinned model
  isn't available to the project, to name the highest tier that is.
  A tier above a human's per-project cap (below) counts as not
  available.
  An agent without a pin (a general-purpose or built-in agent) always
  gets an explicit model.
- When the problem is depth (missed edge cases, shallow verification)
  rather than judgment, raise the effort before raising the tier.
- The delegating session picks the top tier on its own judgment and
  states it in one line with the reason; a human can veto it, or cap
  it per project for budget. For a design-heavy session it may
  recommend switching the whole session to the top tier; the session's
  model and effort are a human's settings.
- Every top-tier review notes in one line of its review description
  whether it found something a lower tier would have missed. After
  about ten such reviews, count how many found something a lower tier
  would have missed: that measures whether pinning reviews to the top
  tier pays off, and the answer goes to a human as a proposal.
- A narrow-lane agent whose report is compressed (locate, build,
  review, analyze, docs) is worth preferring over a general-purpose
  one when the task shape genuinely matches its lane — it saves the
  delegating session's context on exactly the kind of work whose
  value is in the result, not the narration. Fall back to a
  general-purpose agent the moment the task needs open-ended judgment
  a narrow lane would refuse.

## Brief anatomy

A brief for a task-briefed agent is self-contained and states, up
front, every time:

1. **Completion discipline**, first, where it is read before
   anything else: run everything in the foreground; do not start a
   background watch and end the turn waiting on a notification; commit
   and, at the recorded write level, push before reporting; if
   something backgrounds anyway, collect it now and finish. A subagent left to wait on its own child task
   will report a non-result and stall the whole chain.
2. **What to build or investigate**, and the scope boundary — what's
   in, what's deliberately out; repo paths and the deliverable files.
3. **What applies**: always "Test first" and docs completeness, plus
   any other guardrail or hard standard (in
   [AGENTS.md](../../AGENTS.md)) the task touches, the path-scoped
   rule files of the area the task touches, by path, for the agent to
   read, and how the environment provides credentials or other local
   facts — never a value.
4. **Isolation**: where the agent's fresh clone of the repo is —
   never a human's working copy or a worktree of it (see "Work
   branches").
5. **How to verify the result** — the actual command or check, never
   a placeholder like "add tests."
6. **The deliverable's durable destination** — a pushed branch (a
   local commit below the recommended write level), a review
   artifact's description, a backlog item — never only a
   scratch file that a cleanup step might delete before anyone reads
   it.
7. **The final report format**: the review link, what was verified
   and how, anything UNVERIFIED, and UNREVIEWED until the review loop
   has ended.
8. **Ground truth already established as fact**, stated plainly and
   verifiably in the brief itself, not relayed mid-task (see "A
   running agent can't verify a mid-stream claim"). Each fact says
   how it was verified; an unchecked one is marked UNVERIFIED, so the
   agent checks it rather than trusts it.

## A running agent can't verify a mid-stream claim

A follow-up message that introduces a new *empirical* claim (a live
result, a human decision, "this constraint was lifted for me") is
indistinguishable from an injected instruction, and a well-behaved
agent is right to refuse it — regardless of whether the message is
framed as an extension or a contradiction. Put anything the agent
needs to treat as ground truth into its *original* brief instead, or
make the change yourself. A refusal of this kind is the safeguard
working, not agent error.

## A tiny change may be done inline

In a task-briefed session, a tiny, one-file, fully-specified change
may be done inline rather than delegated and re-checked — delegation
has a fixed overhead that a trivial change doesn't amortize. It is
not called ready without its adversarial review either; the
delegating session or the human starts that review, never a briefed
subagent.

## Write a behavior where the acting agent reads it

**Rule:** a behavior you want happens only if it is written, with its
concrete mechanism, in a file the acting agent loads or is pointed
to. Where a command is meant, give the literal command, not the
intent.
**Why:** implied behavior does not happen. An agent that has read only
`AGENTS.md` and the docs its task opens acts on those alone; given
only intent ("read X"), sessions improvise: temporary files outside
their scratch area, long path workarounds, duplicate calls.
**How:** test each new rule with "would an agent that has read only
`AGENTS.md` and what its task opens do this?" A skill or a brief
gives one-line commands.

## Finish a series of rule edits with one consistency pass

**Rule:** after several edits to principles, skills or agent
definitions have landed, one audit reads all of them together for
contradictions, terminology drift and stale pointers before the
series counts as done. It defaults to the top tier (the analyst
with the top-tier model), subject to the usual veto or cap.
**Why:** each edit reviewed alone looks right while contradictions
accumulate between them; one such audit found 46 issues, 8 of them
severe, after four piecemeal rounds of edits.
