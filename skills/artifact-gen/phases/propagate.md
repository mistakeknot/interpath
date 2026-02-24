# Propagation Phase

Auto-generate module-level roadmap files from beads state. Module roadmaps are derived artifacts, not hand-curated — strategic context lives in the root [Demarch Roadmap](../../../../../docs/demarch-roadmap.md).

## How It Works

Run the `generate-module-roadmaps.sh` script from the Demarch root:

```bash
ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
"$ROOT_DIR/scripts/generate-module-roadmaps.sh"
```

The script:
1. Iterates through all module directories under `apps/`, `os/`, `core/`, `interverse/`, `sdk/`
2. Queries beads (`bd list`, `bd blocked`) for items matching each module name
3. Writes `docs/roadmap.md` in each module with open, in-progress, blocked, and recently-closed items
4. Links each module roadmap back to `docs/demarch-roadmap.md` for strategic context
5. Skips modules with no matching beads

## Dry Run

Preview what would be generated without writing files:

```bash
"$ROOT_DIR/scripts/generate-module-roadmaps.sh" --dry-run
```

## Output Format

Each generated `docs/roadmap.md` contains:

```markdown
# <module> Roadmap

> Auto-generated from beads on <date>. Strategic context: [Demarch Roadmap](../../docs/demarch-roadmap.md)

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
- Strategic context (deep dives, research agenda, dependency chains) belongs in the root Demarch Roadmap
- The script is idempotent — safe to run repeatedly
- Run after creating/closing beads to keep module views current
