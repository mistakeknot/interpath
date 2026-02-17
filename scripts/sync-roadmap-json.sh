#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

search_dir="$SCRIPT_DIR"
while true; do
    candidate="$search_dir/scripts/sync-roadmap-json.sh"
    if [ -x "$candidate" ] && [ "$candidate" != "$SCRIPT_DIR/sync-roadmap-json.sh" ]; then
        exec "$candidate" "$@"
    fi

    if [ "$search_dir" = "/" ]; then
        break
    fi
    search_dir="$(cd "$search_dir/.." && pwd)"
done

cat <<'EOF' >&2
interpath: sync-roadmap-json wrapper could not locate scripts/sync-roadmap-json.sh.
Run from the Interverse monorepo root, or provide an absolute script path manually.
EOF
exit 1
