# Propagation Phase

Auto-generate module-level roadmap files from beads state. Module roadmaps are derived artifacts, not hand-curated — strategic context lives in the root project roadmap.

## How It Works

Run the `generate-module-roadmaps.sh` script from the interpath plugin:

```bash
PROPAGATE_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/generate-module-roadmaps.sh"
if [ -z "${CLAUDE_PLUGIN_ROOT:-}" ] || [ ! -x "$PROPAGATE_SCRIPT" ]; then
    echo "Warning: CLAUDE_PLUGIN_ROOT not set or script not found" >&2
    exit 1
fi
bash "$PROPAGATE_SCRIPT"
```

The script:
1. Auto-detects directories containing sub-modules (by `.claude-plugin/plugin.json` or `CLAUDE.md`)
2. Queries beads (`bd list`, `bd blocked`) for items matching each module name
3. Writes `docs/roadmap.md` in each module with open, in-progress, blocked, and recently-closed items
4. Links each module roadmap back to the root project roadmap for strategic context
5. Skips modules with no matching beads

## Dry Run

Preview what would be generated without writing files:

```bash
bash "$PROPAGATE_SCRIPT" --dry-run
```

## Output Format

Each generated `docs/roadmap.md` contains:

```markdown
# <module> Roadmap

> Auto-generated from beads on <date>. Strategic context: [Project Roadmap](../../docs/roadmap.md)

## In Progress
- <bead lines>

## Blocked
- <bead lines>

## Open Items
- <bead lines>

## Recently Closed
- <bead lines>
```

## Guidelines

- Module roadmaps are auto-generated — do not hand-edit them
- Strategic context (deep dives, research agenda, dependency chains) belongs in the root project roadmap
- The script is idempotent — safe to run repeatedly
- Run after creating/closing beads to keep module views current
