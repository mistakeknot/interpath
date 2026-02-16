# Monorepo Discovery Phase

Gather all available context from the Interverse monorepo. Each source is optional — skip gracefully if unavailable. This phase extends the single-project discovery with cross-module and aggregate data.

## Source 1: Monorepo Identity

Read the monorepo `CLAUDE.md` for the canonical structure section — this defines the module list and naming conventions.

```bash
head -80 CLAUDE.md 2>/dev/null || echo "monorepo CLAUDE.md: not available"
```

## Source 2: Module Inventory

Scan `hub/*/`, `plugins/*/`, `services/*/` for plugin manifests. For each module, extract name, version, and description.

```bash
for dir in hub/*/  plugins/*/  services/*/; do
    manifest=""
    if [ -f "${dir}.claude-plugin/plugin.json" ]; then
        manifest="${dir}.claude-plugin/plugin.json"
    elif [ -f "${dir}plugin.json" ]; then
        manifest="${dir}plugin.json"
    fi
    if [ -n "$manifest" ]; then
        echo "MODULE: ${dir%/}"
        jq -r '"  name: \(.name) | version: \(.version) | desc: \(.description // "none")"' "$manifest" 2>/dev/null
    fi
done
```

Record the total module count.

## Source 3: Per-Module Roadmaps

For each discovered module, check for `docs/roadmap.md`:

```bash
for dir in hub/*/  plugins/*/  services/*/; do
    roadmap="${dir}docs/roadmap.md"
    if [ -f "$roadmap" ]; then
        echo "=== ROADMAP: ${dir%/} ==="
        head -40 "$roadmap"
        echo "---"
    fi
done
```

Note which modules have roadmaps and which don't.

## Source 4: Monorepo Beads

Gather aggregate bead state from the monorepo root:

```bash
# Overall stats
bd stats 2>/dev/null || echo "monorepo beads: not available"

# All open beads with priorities
bd list --status=open 2>/dev/null || echo "open beads: not available"

# Blocked beads
bd blocked 2>/dev/null || echo "blocked beads: not available"

# In-progress beads
bd list --status=in_progress 2>/dev/null || echo "in-progress beads: not available"
```

## Source 5: Sub-Module Beads

For each module with a `.beads/` directory, gather per-module stats:

```bash
for dir in hub/*/  plugins/*/  services/*/; do
    if [ -d "${dir}.beads" ]; then
        echo "=== BEADS: ${dir%/} ==="
        (cd "${dir}" && bd stats 2>/dev/null) || echo "  stats: not available"
    fi
done
```

## Source 6: Monorepo-Level Documents

Glob for planning and research documents at the monorepo root:

- `docs/brainstorms/*.md` — read first 20 lines of each
- `docs/plans/*.md` — read first 30 lines of each
- `docs/prds/*.md` — read first 30 lines of each
- `docs/product/*.md` — read first 20 lines of each

Use Glob tool to discover these, then Read the first N lines of each.

## Source 7: Git Activity

```bash
# Recent commits from monorepo root
git log --oneline -20 2>/dev/null || echo "git: not available"

# Recent tags
git tag --sort=-version:refname 2>/dev/null | head -10 || echo "tags: none"
```

## Source 8: Cross-Module Dependencies

Look for blocking relationships in open beads that reference multiple modules. Check bead titles and descriptions for module names (clavain, interflux, intermute, interlock, etc.).

```bash
bd list --status=open 2>/dev/null | grep -iE "(clavain|inter[a-z]+|tldr|tuivision)" || echo "no cross-module references found"
```

## Output

Compile all discovered sources into a structured context. Note:
- Total module count and which have manifests
- Which modules have roadmaps vs. which don't
- Monorepo bead counts and priority distribution
- Per-module bead counts (where available)
- Key themes from brainstorms and plans
- Cross-module blocking relationships

Pass this full context to the `roadmap-monorepo.md` synthesis phase.
