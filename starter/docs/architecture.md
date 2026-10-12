# <Project> — architecture (current state)

<!--
Architect-maintained (the list in AGENTS.md is the authority): edited
only by an architect session, by direct push to the trunk, or by setup
in its one seeding change; never from a work branch. A work branch
that invalidates something here flags it instead of editing it.

This file describes CURRENT, SETTLED state — what the system is and
why, right now. Open questions live in ../backlog.md, not here.
-->

Everything here is current and settled. Nothing here restates what
another file owns:

| For | Read |
|---|---|
| What this project is, concepts, worked examples | this project's own `README.md` |
| Vocabulary, defined once, used verbatim | [glossary.md](glossary.md) |
| Principles: engineering, AI working process, context economy | [principles/](principles/) |
| Decisions and rulings, dated, superseded ones kept | [decisions.md](decisions.md) |
| Detailed designs | [design/](design/) |
| Known failures, keyed by their exact error text | [troubleshooting.md](troubleshooting.md) |
| Work in flight, queued, deliberately deferred | [../backlog.md](../backlog.md) |

**Stakeholders:** <!-- Who uses, operates, secures, pays for, and is
legally affected by this system: one entry each, with who speaks for
them. They are consulted; the humans on this project decide. -->

## 1. Guiding principles

<!-- The handful of principles that shape every decision below. Keep
     this short — a paragraph or a bullet each, citing where each one
     actually shows up in the system rather than restating it in the
     abstract. -->

## 2. Shape

<!-- The system's major components/units and how they relate. What's
     structure (few, stable, deliberate) versus what's data (discovered,
     supplied, expected to vary) — see principles/engineering.md's
     "Data vs structure". -->

## 3. Decisions in force

<!-- One subsection per domain (e.g. "access", "delivery", "state").
     Each decision: what was chosen and why, in a sentence, citing
     its entry in decisions.md (e.g. "D3"); a design doc carries the
     why when it needs more room. -->

## 4. Open questions

<!-- Anything genuinely undecided lives in ../backlog.md instead —
     this section exists only to point there, so nobody assumes silence
     here means "settled". -->

See [backlog.md](../backlog.md).
