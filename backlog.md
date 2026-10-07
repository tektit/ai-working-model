# Backlog

Humans decide and merge; the architect keeps this current.

## Next session starts here

- **v1.0.0, the initial release (2026-10-06):** `starter/` is MIT-0, so customers copy it with no obligations (D3); measurement tools, research notes and experiment logs were stripped, their conclusions kept in the decisions; git history squashed to one commit. A top-tier pre-release review found no identifier leaks.
- **No more paid experiments** (ruling 2026-09-25); D12 makes every paid run need a go-ahead naming the paying account.
- Start with the human's field-trial report (Waiting on the human). Also one check: `starter/.claude/rules/README.md` has a `paths` header; confirm it no longer appears among the loaded instructions in a fresh session's transcript (`jq` over the session's `.jsonl`, attachment type `instructions`).
- Then Next item 1 (one line in the architect skill).

## In flight

- Nothing.

## Waiting on the human

- Publish v1.0.0: push it to its remote. Publishing can't be undone, so it is the human's step.
- Field trial: the human seeds a new client repo with the starter and reports back (from 2026-10-06). Before copying, add the client's name to `.neutrality-denylist`. It is the first real setup run, so it revives the deferred "Setup's open questions".

## Next

1. Board hygiene (measured): finished entries left in "In flight" cost kickoff reads; move them to "Done (recent)" promptly, keep entries with owed work. One line in the architect skill.
2. Evidence to fold in when these sections are next touched (no change on its own): reading reference sections by trigger cut kickoff reads ~24 KB to 11 KB ("Read the part"); on a required tool's auth failure (401/403, publickey, missing username) stop, name the tool, walk the human through setup, never continue on partial data (fail early, credentials; architect kickoff); lean kickoff −45% context, 3 vs 23 tool calls; summary-line/full-text drift needs a 1:1 mechanical check.
3. Team rollout playbook: which settings are committed per repo vs set by an org admin (managed settings), which MCP servers and plugins a project enables (D11), measured levers only.
4. Plain-language layer for the principles (D4) — re-check whether D10's "plain words by default" already covers it.

## Deliberately deferred

- **Codex enablement** — Claude only for now; kept cheap by `AGENTS.md` as the single instruction source. Remaining: Codex agent definitions, config and skill path, verified in a real Codex setup (`disable-model-invocation`, `references/`, repo-committed skill discovery). The earlier parity research was dropped at v1.0.0; redo it from the official docs. Revive at the first Codex client.
- **SOPS-encrypted neutrality denylist** (age recipient = SSH ed25519 key) — revive when a second machine or a second person needs the denylist; publishing alone doesn't, the denylist stays local.
- **Release checklist** — v1.0.0 ran a top-tier identifier review of the whole tree by hand. Revive before the second release, as one rule line in the root `AGENTS.md`.
- **Measurement instruments and research** — the usage, proxy and model A/B tools, their data and the research notes were stripped at v1.0.0 and are gone with the squashed history; D1, D2, D9 and D11 keep their conclusions. Revive when a decision needs a new measurement; build the instrument fresh for that question.
- **Local-model retrieval over docs** — dropped under D2 for team use; revive only if a platform offers it natively.
- **Handoff/compaction tooling** — dropped under D2.
- **`omitClaudeMd` for narrow helpers** — would cut each subagent's always-loaded context but drop the guardrails D10 relies on; revive only if subagent start-up cost is measured to matter and guardrails reach them another way.
- **`CLAUDE.md` = `@AGENTS.md` vs native `AGENTS.md` reading** — newer Claude Code reads `AGENTS.md` natively; the import stays while team versions vary. Revive when every team runs a version that reads it.
- **Setup's open questions** — left open on purpose; revive at the first real setup run (the field trial): (1) in a repo with no remote, should setup's approved changes be the first commit, stay uncommitted, or wait until setup helps create the remote so they go through review; (2) should setup draft the project `README.md` from the purpose and stakeholder answers, or leave it to the first architect session; (3) when a tracker replaces `backlog.md`, should setup ever write to that tracker, or only list what the owner creates there.
- **Quota-only check of one-line rules** (Team seat, no API key: does a plain session follow the one-line rules in `AGENTS.md`, e.g. fail loudly in a shell script?) — no problem observed yet. Revive when a plain session is seen ignoring a one-line rule.
- **Skill argument trap check** — Claude Code substitutes `$0`, `$1`, `$ARGUMENTS` in a skill or command body with the user's arguments (measured in another session: an awk `$0` became the argument, a step silently printed nothing). A `starter-check` rule would fail on them in `starter/.claude/{skills,agents}` bodies unless marked intended; none today (grep-verified 2026-10-05). Revive when a skill or command misbehaves from it, or one needs a literal `$`+digit.
- **Re-check the MCP lever** in D11 / context-economy "Always-loaded" — UNVERIFIED peer report: tool search is on by default, so disabling MCP servers may save only deferred tool names plus server instructions, not the ~54k session start. Revive when someone acts on that lever or the section is next touched; read the raw Claude Code docs first, correct through "Changing a principle" if it overstates.

## Open assumptions to check

- Tektit holds the copyright to everything in `starter/` (one git author; nothing copied word for word from a client's or employer's work); MIT-0 only covers what Tektit owns. The human to confirm.
- Client contracts' IP terms don't conflict with handing over the starter under MIT-0. Whoever handles Tektit's contracts to confirm.
- The model A/B's synthetic tasks represent real subagent work well enough to set a team default.
- Quota weights per model on Team seats are unknown; cost comparisons use the CLI's API-equivalent cost as a proxy.
- Client teams accept committed `.claude/settings.json` / `.codex/config.toml`; some orgs may require admin-managed settings only.
- One-line rules in `AGENTS.md` steer a plain session about as well as the full principle text (judgment, D10).
- The top tier earns its ~2.5x: evidence log — 2026-10-05 principles audit (analyst on Fable) found 46 issues, 8 high, after several piecemeal rounds; a standard-tier reviewer then still caught one blocker in the fix; 2026-10-06 pre-release review (reviewer on Fable) found a spend detail and three stale statements after a standard-tier strip, no identifier leaks. Revisit after about ten top-tier runs.
