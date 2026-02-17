# Propagation Phase

After generating the monorepo roadmap, push relevant items back down to each sub-module's roadmap. This ensures every module's roadmap reflects both its own state and its place in the Interverse ecosystem.

## Prerequisites

The monorepo roadmap is expected at `docs/roadmap.json` in the Interverse root. If missing or stale, regenerate it first:

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

If JSON is unavailable, fallback to `docs/roadmap.md`.
If neither exists, generate first using `discover-monorepo.md` → `roadmap-monorepo.md`.

## Step 1: Identify Relevant Beads Per Module

For each module in the monorepo, find monorepo-level beads that reference it:
- Match module name (e.g., "interflux", "clavain", "intermute") in bead title or description
- Match module path (e.g., "plugins/interflux", "hub/clavain") in bead content
- Include beads that list the module as blocked-by or blocking

```bash
# Prefer canonical monorepo JSON for authoritative references.
if [ -f "docs/roadmap.json" ]; then
  cat docs/roadmap.json
else
  echo "WARN: docs/roadmap.json not available; falling back to docs/roadmap.md"
  cat docs/roadmap.md
fi

# For each module, search monorepo beads
for dir in hub/*/  plugins/*/  services/*/; do
    module=$(basename "${dir%/}")
    matches=$(bd list --status=open 2>/dev/null | grep -ic "$module" || echo "0")
    if [ "$matches" -gt 0 ]; then
        echo "MODULE: $module — $matches relevant monorepo beads"
    fi
done
```

## Step 2: Update Existing Roadmaps

For each module that **has** a `docs/roadmap.md`:

1. `cd` into the module directory
2. Run the standard single-project discovery (`discover.md` phase) to gather the module's own context
3. Regenerate the roadmap using the standard `roadmap.md` phase
4. **Append** a new section at the end (before "Keeping Current" if it exists):

```markdown
## From Interverse Roadmap

Items from the [Interverse roadmap](../../../docs/roadmap.json) that involve this module:

- **beads-xxx** [P1] Description of cross-cutting item
- **beads-yyy** [P2] Description of dependency on this module
```

If no monorepo beads reference this module, add:

```markdown
## From Interverse Roadmap

No monorepo-level items currently reference this module.
```

## Step 3: Generate Minimal Roadmaps

For modules that **lack** a `docs/roadmap.md` but have **3 or more** beads referencing them (either in the module's own `.beads/` or in monorepo beads):

1. `cd` into the module directory
2. Run the standard single-project discovery (`discover.md` phase)
3. Generate a minimal roadmap with just:
   - Header (name, version, date)
   - Where We Are (from plugin manifest)
   - Open Beads Summary (from local and monorepo beads)
   - From Interverse Roadmap section
   - Keeping Current section
4. Create `docs/roadmap.md` in the module directory (create `docs/` if needed)

## Step 4: Summary Report

After processing all modules, output a summary:

```markdown
## Propagation Summary

### Updated (existing roadmaps refreshed)
- hub/clavain — 5 monorepo items added
- plugins/interflux — 3 monorepo items added

### Created (new minimal roadmaps)
- plugins/interline — 4 beads, new roadmap generated

### Skipped (no roadmap, fewer than 3 beads)
- plugins/interwatch — 1 bead (threshold: 3)

### No Changes
- plugins/interpub — 0 relevant monorepo beads
```

## Guidelines

- Preserve existing roadmap content — only add/update the "From Interverse Roadmap" section
- Don't duplicate items that already appear in the module's own roadmap sections
- Use relative paths for cross-references between monorepo and module roadmaps
- If the module's `docs/` directory doesn't exist, create it before writing the roadmap
- Report what was done so the user can review changes
