# starter-check

Verifies that `starter/` is genuinely self-contained: the exact tree a
user copies into a brand new repo, with nothing left pointing back at
this one.

## Running it

```sh
cd tools/starter-check
uv run starter-check [--repo PATH]
```

Copies `starter/`'s contents into a temp dir, runs `git init` there,
and checks:

1. Every relative markdown link and `@path` import resolves inside the
   copy.
2. No file references this repo (`ai-working-model`) or the `starter/`
   directory by name — a copied file must read as belonging to the new
   repo.
3. `CLAUDE.md` is exactly `@AGENTS.md`.
4. `AGENTS.md` and the principles have not drifted apart: every `##`
   heading in `docs/principles/{engineering,ai-working-process,context-economy}.md`
   is linked from `AGENTS.md` exactly once, by its GitHub anchor
   (`docs/principles/engineering.md#fail-early-and-loudly`), and every
   anchored link to those files lands on an existing heading. Headings
   inside code fences and HTML comments don't count; two headings with
   the same anchor in one file, or a heading with underscores or an
   inline link (which would be mis-slugged), are reported. Each problem
   names the heading or the link line.
5. No license file (any file name starting `LICENSE`, `LICENCE`,
   `COPYING` or `NOTICE`, at any depth) and no copyright line or
   `SPDX-License-Identifier` tag: the starter's license terms live in
   the root `LICENSE-starter`, recorded in `NOTICE`, and a copy must
   not drop its own into the new repo. Plain prose about licenses is
   fine.
6. The root `.claude` symlink (checked against the real repo, not the
   copy) resolves to a real directory inside `starter/`.

Exit codes: `0` clean, `1` problems found (each printed to stderr).

## Testing

```sh
cd tools/starter-check
uv run pytest -q
```

Most tests build synthetic fixtures under `tmp_path`; one test runs the
full check against this repo's real `starter/` — the same thing `uv run
starter-check` does.
