# Setup questions

Read before asking the first question. For each: what to observe
first, how to ask, the recommended default, the trade-off to explain,
and where the answer goes (details in `edits.md`).

## 1. Product and purpose

- **Ask:** "In a sentence or two: what should this do, and for whom?
  How will you know it works well?"
- **Default:** none. This one is always the human's words. Offer to
  tighten their wording, and confirm the result.
- **Goes to:** `AGENTS.md` purpose line; `docs/architecture.md` title
  and purpose.

## 2. Stakeholders

- **Ask** one role at a time: who uses it, who keeps it running, who is
  responsible for security, who pays, who could be legally affected
  (for example because it handles personal data).
- **Default:** for a small internal tool one person often holds most
  roles. Say so and confirm, but ask about security and legal
  separately: those are the ones most often forgotten.
- **Goes to:** the stakeholders line in `docs/architecture.md`, with who
  speaks for each role.

## 3. Git host and trunk

The trunk is the repository's default branch: the version of the code
that counts. Explain that once, then say "trunk".

- **Observe first:** the configured remote and its default branch.
- **Ask:** "Your code lives on <host>, and <branch> is the version that
  counts. Is that right?" With no remote: "Where does your team keep
  code (for example GitHub, GitLab, or a company server)?"
- **Default:** the host the team already uses; `main` as the default
  branch.
- **Goes to:** `AGENTS.md` "Project setup"; `docs/architecture.md`
  decisions.

## 4. Pipeline and what merging deploys

- **Observe first:** pipeline files in the repo.
- **Ask:** "When a change is merged, what happens automatically? Is
  anything tested, and is anything deployed, and where?"
- **Say plainly** whether merging to the trunk deploys. If it does,
  every merge is a release.
- **Default:** if there is no pipeline, one that runs the tests on
  every change before anything deploys automatically. Tests gate
  everything; no skill level is assumed of whoever reviews.
- **Goes to:** `AGENTS.md` "Project setup"; `docs/architecture.md`
  decisions.

## 5. Where work and project management lives

This matters most: from now on "the backlog" means this place.

- **Ask:** "Where do you and your team keep track of what's planned and
  in progress?"
- **Recommend by situation:**
  - One person working alone with no tracker: `backlog.md` in the repo. It needs no
    extra account and travels with the code, but it is not built for
    assigning work or notifying other people.
  - A team that already uses a tracker (issues on the git host, Jira or
    similar): that tracker. People keep working where they already are,
    but the architect needs read and write access to it, which someone
    has to set up.
  - A small team with no tracker: issues on the git host. They sit next
    to the code at no extra cost, but they are weaker than a dedicated
    tool for planning across many projects.
- **Agree the mapping** of the backlog's parts onto that place: the
  "Next session starts here" pointer, in flight, queued (in order: the
  roadmap), "Deliberately deferred" (each with why and its revive
  trigger), and recently done. In a tracker this is usually one pinned
  item plus labels or a board.
- **Ask how access reaches a command** (which tool, how it is signed
  in). Credentials are pure injection: record how they are provided,
  never a value.
- **Goes to:** `AGENTS.md` "Project setup"; `backlog.md` seeded or
  removed.

## 6. Environments

- **Ask:** "Where does this run? Only on your computer, on a shared
  server, or in separate test and live versions?"
- **Default:** a tool used by one person can start with one.
  Anything others rely on gets a test environment next to production,
  so changes are tried before users see them. The trade-off is roughly
  double the running cost against catching problems before users do.
- **Goes to:** `docs/architecture.md` decisions; each environment's name
  in `docs/glossary.md`, spelled exactly as the human uses it.

## 7. Organization constraints

- **Ask** one area at a time, and only what applies: personal or
  confidential data, approved vendors or hosting, security policies,
  budget limits, licenses, deadlines.
- **Default:** none. Never assume a constraint and never assume there
  is none; "not known yet" plus who could answer is a good record.
- **Goes to:** `docs/architecture.md` decisions (each constraint that
  shapes the design); open ones to the backlog.

## Deviations from the principles

- **Ask:** "The project starts with a set of engineering and working
  principles. Is there anything your organization does differently on
  purpose?"
- **Default:** no deviations. Don't suggest any.
- **Goes to:** `docs/principles/`, its line in `AGENTS.md` and an
  entry in `docs/decisions.md`, after "Changing a principle"
  (SKILL.md step 5).
