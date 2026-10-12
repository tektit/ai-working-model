# neutrality

Scans every git-tracked and staged file in this repo for client,
customer or private-project identifiers, so none leak into a repo that
gets shared with other clients. See the root README's "Neutrality
check" section for the encrypted denylist, `check.sh` and the
pre-commit hook to install.

## Running it

```sh
cd tools/neutrality
uv run neutrality-check --denylist PATH [--repo PATH]
```

Reads the denylist (one case-insensitive regex per line) from the
file given by `--denylist`, once; it is unaware of SOPS. The repo's
entry point is `check.sh`, which supplies the decrypted list. Prints
one `file:line: pattern` line per hit. Exit codes: `0` clean, `1` hits found, `2` denylist file missing.

## Testing

```sh
cd tools/neutrality
uv run pytest -q
```

Tests build synthetic git repos under `tmp_path` — never scan this
repo's real content or denylist.
