#!/usr/bin/env sh
# The repo's neutrality check: decrypts the committed denylist through a
# named pipe (sops exec-file) and hands it to neutrality-check.
set -eu

for tool in sops uv; do
    command -v "$tool" >/dev/null 2>&1 || {
        echo "check.sh: required tool not found on PATH: $tool" >&2
        exit 2
    }
done

repo=$(git rev-parse --show-toplevel)
tool_dir=$(cd "$(dirname "$0")" && pwd)
encrypted="$repo/.neutrality-denylist.sops"

NEUTRALITY_REPO="$repo" NEUTRALITY_TOOL_DIR="$tool_dir" \
    sops exec-file "$encrypted" \
    'uv run --project "$NEUTRALITY_TOOL_DIR" neutrality-check --repo "$NEUTRALITY_REPO" --denylist {}'
