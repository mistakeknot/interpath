# Artifact Generator (compact)

Generate product artifacts from project state. Supports: **roadmap**, **monorepo-roadmap**, **propagate**, **prd**, **vision**, **changelog**, **status**, **cuj**.

In Codex, resolve this skill's symlink and set `INTERPATH_ROOT` to two directories
above the skill directory. Resolve phases/references from the skill directory;
run plugin scripts by absolute path from the target project's working directory.
Report missing scripts without installing them. Claude Code may use
`CLAUDE_PLUGIN_ROOT` as `INTERPATH_ROOT`.

## Algorithm

### Step 1: Discover Sources (gather in parallel)

| Source | How |
|--------|-----|
| Plugin manifest | Read `.claude-plugin/plugin.json` for version, name, description |
| Component counts | `ls skills/*/SKILL.md`, `ls commands/*.md`, `ls agents/*/*.md` |
| Beads state | `bd stats`, `bd list --status=open`, `bd list --status=closed` (last 40), `bd blocked` |
| Brainstorms | Glob `docs/brainstorms/*.md`, read first 20 lines each |
| PRDs & Plans | Glob `docs/PRD.md`, `docs/prds/*.md`, `docs/plans/*.md`, read first 30 lines each |
| Vision doc | Read `docs/${module}-vision.md` |
| Existing artifact | Read the current version of the target doc (for diffing) |
| Git activity | `git log --oneline -20`, `git tag --sort=-version:refname | head -5` |
| Companions | Check `~/.claude/plugins/cache/interagency-marketplace/*/` for installed plugins |

Skip any source that's unavailable — degrade gracefully.

### Step 2: Generate by Type

| Type | Output | Key Sections |
|------|--------|-------------|
| **roadmap** | `docs/${module}-roadmap.md` + `docs/roadmap.json` | Where We Are (counts, companions), Shipped Work, Phased Roadmap (Now/Next/Later from beads), Research Agenda, Companion Status, Open Beads Summary, Dependency Graph |
| **monorepo-roadmap** | `docs/${module}-roadmap.md` + `docs/roadmap.json` | Use the actual monorepo name; ecosystem snapshot, rollup now/next/later with module tags |
| **propagate** | Updated module `docs/roadmap.md` files | Reads `docs/roadmap.json` and updates sub-repo roadmap sections |
| **prd** | `docs/PRD.md` | Problem, Product Overview, Core Capabilities (by lifecycle phase), Architecture (components, routing, hooks, companions), Non-Goals, Success Metrics, Open Questions |
| **vision** | `docs/${module}-vision.md` | What It Is, Core Conviction, Audience, Operating Principles, What's Working/Not |
| **changelog** | Existing changelog path; otherwise `CHANGELOG.md` | Group closed beads by version/date, categorize by type (feature/fix/chore) |
| **status** | `docs/STATUS.md` | Health metrics, shipped this week, blockers, next priorities |
| **cuj** | `docs/cujs/<journey-slug>.md` | Why It Matters, The Journey (prose), Success Signals (typed table), Known Friction Points |

### Step 3: Output (Canonical Witness)

Canonical paths are defaults for authorized generation. Explicit user destinations,
templates, and preservation instructions take precedence. Archive only a proven
earlier generated copy of this artifact when that cleanup is in scope; preserve
unrelated local edits and leave ambiguous files alone.

Always write to the exact canonical path in the table above. Overwrite in place — never suffix the filename with a date or ISO timestamp (e.g., NOT `sylveste-roadmap-2026-05-06.md`). If a date/timestamp-suffixed orphan from a previous interpath run exists, move it to `docs/.archive/${YYYY-MM-DD}/` before writing. Do NOT touch hand-curated parallel docs that share a related name (e.g., `docs/roadmap-v1.md` as release-goals planning) — those are intentional separate documents. Diff summary before overwrite is courtesy, not a gate. Rule and rationale: sylveste-a4oj.7 / SCRIP-2 (medieval scriptorium canonical-witness pattern).

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
