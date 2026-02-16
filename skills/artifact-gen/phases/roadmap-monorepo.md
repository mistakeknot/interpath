# Monorepo Roadmap Synthesis

Using the monorepo discovery context, generate a unified Interverse roadmap that aggregates across all modules.

## Output Structure

### Header

```markdown
# Interverse Roadmap

**Modules:** [count] | **Open beads:** [count] | **Last updated:** [today's date]
**Structure:** [`CLAUDE.md`](../CLAUDE.md)
```

### Section 1: Ecosystem Snapshot

A table of all modules with their current state:

```markdown
## Ecosystem Snapshot

| Module | Location | Version | Status | Roadmap | Open Beads |
|--------|----------|---------|--------|---------|------------|
| clavain | hub/clavain | X.Y.Z | active | yes | N |
| interflux | plugins/interflux | X.Y.Z | active | yes | N |
| ... | ... | ... | ... | ... | ... |
```

**Status** values:
- `active` — has recent commits and/or open beads
- `stable` — no recent activity, appears complete
- `early` — has manifest but limited development
- `planned` — referenced in docs but no manifest

### Section 2: Roadmap — Now / Next / Later

Aggregate from monorepo beads, organized by priority:

```markdown
## Roadmap

### Now (P0–P1)
- [module] **beads-xxx** Description of critical/high-priority item
- [module] **beads-yyy** Description (blocked by beads-zzz)

### Next (P2)
- [module] **beads-xxx** Description of medium-priority item

### Later (P3–P4)
- [module] **beads-xxx** Description of backlog/aspirational item
```

For each item:
- Tag with `[module]` prefix identifying which module it relates to
- Include bead ID for traceability
- Note blocking relationships inline
- Items that span multiple modules get tagged with all relevant modules

### Section 3: Module Highlights

For each module that **has** a `docs/roadmap.md`, provide a 2-3 line summary of its current focus:

```markdown
## Module Highlights

### clavain (hub/clavain)
Current focus: [synthesized from roadmap]. Key items: [2-3 highlights].

### interflux (plugins/interflux)
Current focus: [synthesized from roadmap]. Key items: [2-3 highlights].
```

Only include modules with existing roadmaps.

### Section 4: Research Agenda

Synthesize from monorepo-level brainstorms, PRDs, and plans:

```markdown
## Research Agenda

- **[topic]** — [1-line summary from brainstorm/plan] ([source file])
- **[topic]** — [1-line summary] ([source file])
```

### Section 5: Cross-Module Dependencies

Blocking relationships between beads, especially those spanning modules:

```markdown
## Cross-Module Dependencies

- **beads-xxx** (interlock) blocks **beads-yyy** (clavain) — [reason]
- **beads-aaa** (intermute) blocks **beads-bbb** (interlock) — [reason]
```

If no cross-module blocking exists, note "No cross-module blockers identified."

### Section 6: Modules Without Roadmaps

List modules that lack `docs/roadmap.md`, with their bead count:

```markdown
## Modules Without Roadmaps

| Module | Location | Open Beads | Notes |
|--------|----------|------------|-------|
| interline | plugins/interline | 0 | statusline renderer |
| interwatch | plugins/interwatch | 2 | doc freshness monitoring |
```

### Section 7: Keeping Current

```markdown
## Keeping Current

```
# Regenerate this roadmap
/interpath:roadmap    (from Interverse root)

# Propagate items to subrepo roadmaps
/interpath:propagate  (from Interverse root)
```
```

## Writing Guidelines

- Be factual — use counts, versions, and bead IDs, not qualitative claims
- Tag every item with its module so readers can filter mentally
- Keep each item to 1-2 lines
- Link to source files where possible
- Target 200-400 lines (larger than single-project due to scope)
- Sections for which no data is available should say "No data available" rather than being omitted
- Sort modules alphabetically within tables
