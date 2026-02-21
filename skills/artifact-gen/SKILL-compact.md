# Artifact Generator (compact)

Generate product artifacts from project state. Supports: **roadmap**, **monorepo-roadmap**, **propagate**, **prd**, **vision**, **changelog**, **status**.

## Algorithm

### Step 1: Discover Sources (gather in parallel)

| Source | How |
|--------|-----|
| Plugin manifest | Read `.claude-plugin/plugin.json` for version, name, description |
| Component counts | `ls skills/*/SKILL.md`, `ls commands/*.md`, `ls agents/*/*.md` |
| Beads state | `bd stats`, `bd list --status=open`, `bd list --status=closed` (last 40), `bd blocked` |
| Brainstorms | Glob `docs/brainstorms/*.md`, read first 20 lines each |
| PRDs & Plans | Glob `docs/PRD.md`, `docs/prds/*.md`, `docs/plans/*.md`, read first 30 lines each |
| Vision doc | Read `docs/${module}-vision.md` (fallback: `docs/vision.md`) |
| Existing artifact | Read the current version of the target doc (for diffing) |
| Git activity | `git log --oneline -20`, `git tag --sort=-version:refname | head -5` |
| Companions | Check `~/.claude/plugins/cache/interagency-marketplace/*/` for installed plugins |

Skip any source that's unavailable — degrade gracefully.

### Step 2: Generate by Type

| Type | Output | Key Sections |
|------|--------|-------------|
| **roadmap** | `docs/${module}-roadmap.md` + `docs/roadmap.json` | Where We Are (counts, companions), Shipped Work, Phased Roadmap (Now/Next/Later from beads), Research Agenda, Companion Status, Open Beads Summary, Dependency Graph |
| **monorepo-roadmap** | `docs/interverse-roadmap.md` + `docs/roadmap.json` | Monorepo ecosystem snapshot, rollup now/next/later with module tags |
| **propagate** | Updated module `docs/${module}-roadmap.md` files | Reads `docs/roadmap.json` and updates sub-repo roadmap sections |
| **prd** | `docs/PRD.md` | Problem, Product Overview, Core Capabilities (by lifecycle phase), Architecture (components, routing, hooks, companions), Non-Goals, Success Metrics, Open Questions |
| **vision** | `docs/${module}-vision.md` | What It Is, Core Conviction, Audience, Operating Principles, What's Working/Not |
| **changelog** | `docs/CHANGELOG.md` | Group closed beads by version/date, categorize by type (feature/fix/chore) |
| **status** | `docs/STATUS.md` | Health metrics, shipped this week, blockers, next priorities |

### Step 3: Output

Write to `docs/` in the project root. If file exists, show diff summary before overwriting.

**Header format:**
```markdown
# [Project] [Type]
**Version:** [from plugin.json]
**Last updated:** [today]
```

## Guidelines

- Be factual, not aspirational — describe what IS, not what could be
- Use counts and versions, not qualitative claims
- Link to source files where possible
- Keep each item to 1-2 lines

---

*For detailed phase instructions or specific artifact templates, read SKILL.md and its phases/ directory.*
