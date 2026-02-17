---
name: roadmap
description: Generate or refresh a project roadmap from beads state, brainstorms, plans, and project context. Auto-detects monorepo roots for ecosystem-wide roadmaps.
---

# Generate Roadmap

Invoke the `artifact-gen` skill with artifact type **roadmap**.

Before generating the roadmap, run the interpath wrapper so the canonical JSON generator is refreshed from the monorepo context:

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

The roadmap synthesizes:
- Current project state (version, components, companions)
- Open beads organized by priority into Now/Next/Later phases
- Research agenda from brainstorms and flux-drive summaries
- Blocking relationships and dependency graph

**Monorepo mode:** When run from a monorepo root (e.g., Interverse), this command auto-detects the monorepo context and generates an ecosystem-wide roadmap covering all modules in `hub/`, `plugins/`, and `services/`. Use `/interpath:propagate` to push items back to individual module roadmaps.

Output:
- `docs/roadmap.md` (human-facing view)
- `docs/roadmap.json` (machine-readable canonical source, for downstream tooling)
- `docs/roadmap.json` is guaranteed from `plugins/interpath/scripts/sync-roadmap-json.sh` and should be treated as the canonical feed.

Use the Skill tool to invoke `interpath:artifact-gen` with the instruction: "Generate a roadmap artifact."
