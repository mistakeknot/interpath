---
name: propagate
description: Propagate Interverse roadmap items to each subrepo's roadmap
---

# Propagate Roadmap

Invoke the `artifact-gen` skill with artifact type **propagate**.

This command is designed for the Interverse monorepo root. It:

1. Ensures a monorepo-level roadmap exists (generates one if not)
2. Iterates through all modules in `hub/`, `plugins/`, `services/`
3. For modules with existing roadmaps: refreshes them and adds a "From Interverse Roadmap" section with relevant monorepo-level items
4. For modules without roadmaps but with 3+ relevant beads: generates a minimal roadmap
5. Reports a summary of what was updated, created, or skipped

**Prerequisites:** Run from the Interverse monorepo root directory.

Output: Updated `docs/roadmap.md` files in each affected module.

If needed, refresh the monorepo rollup first:

```bash
ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
ROADMAP_SYNC="${CLAUDE_PLUGIN_ROOT}/scripts/sync-roadmap-json.sh"
if [ -z "${CLAUDE_PLUGIN_ROOT:-}" ] || [ ! -x "$ROADMAP_SYNC" ]; then
    ROADMAP_SYNC="$ROOT_DIR/plugins/interpath/scripts/sync-roadmap-json.sh"
fi
if [ ! -x "$ROADMAP_SYNC" ]; then
    echo "Could not find interpath roadmap sync wrapper" >&2
    exit 1
fi
"$ROADMAP_SYNC"
``` 

Use the Skill tool to invoke `interpath:artifact-gen` with the instruction: "Generate a propagate artifact."
