#!/usr/bin/env sh
# The repo's neutrality check: decrypts the committed denylist through a
# named pipe (sops exec-file) and hands it to neutrality-check.
set -eu

case "$(uname -s)" in
    MINGW* | MSYS* | CYGWIN* | Windows_NT)
        echo "check.sh: the encrypted check runs only on macOS and Linux; the" \
            "denylist's key holders do not use Windows. On Windows run" \
            "'neutrality-check --denylist <your own list>' instead." >&2
        exit 2
        ;;
esac

for tool in sops uv git; do
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
