# Source Catalog

Discoverable source types for artifact generation. Each source has glob patterns and extraction rules.

## Sources

| Source | Glob Pattern | Extraction |
|--------|-------------|------------|
| Plugin manifest | `.claude-plugin/plugin.json` | JSON parse: name, version, description |
| Beads stats | `bd stats` | CLI output: open/closed/blocked counts |
| Open beads | `bd list --status=open` | CLI output: ID, title, priority, status |
| Closed beads | `bd list --status=closed` | CLI output: ID, title, type, close date |
| Blocked beads | `bd blocked` | CLI output: ID, title, blocked-by |
| Brainstorms | `docs/brainstorms/*.md` | First 20 lines: title, summary |
| PRD | `docs/PRD.md` | Full read |
| Plans | `docs/plans/*.md` | First 30 lines: title, scope |
| Vision | `docs/vision.md` | Full read |
| Roadmap | `docs/roadmap.md` | Full read (for refresh context) |
| Flux-drive summaries | `docs/research/flux-drive/*/summary.md` | First 20 lines: findings |
| Git log | `git log --oneline -20` | Recent commits |
| Git tags | `git tag --sort=-version:refname` | Recent versions |
| Skills | `skills/*/SKILL.md` | Count + names |
| Commands | `commands/*.md` | Count + names |
| Agents | `agents/*/*.md` | Count + names |
| Companions | `~/.claude/plugins/cache/*/[name]/*/scripts/*.sh` | Installed status |

## Monorepo Sources

Additional sources available when running from a monorepo root (see `discover-monorepo.md`):

| Source | Glob Pattern | Extraction |
|--------|-------------|------------|
| Module manifests | `{hub,plugins,services}/*/.claude-plugin/plugin.json` | JSON parse: name, version, description per module |
| Sub-roadmaps | `{hub,plugins,services}/*/docs/roadmap.md` | First 40 lines: title, current focus |
| Sub-beads | `{hub,plugins,services}/*/.beads/` | `cd <module> && bd stats`: per-module counts |
| Monorepo brainstorms | `docs/brainstorms/*.md` | First 20 lines: title, summary |
| Monorepo PRDs | `docs/prds/*.md` | First 30 lines: title, scope |
| Monorepo plans | `docs/plans/*.md` | First 30 lines: title, scope |
| Monorepo product docs | `docs/product/*.md` | First 20 lines: title, summary |
| Monorepo CLAUDE.md | `CLAUDE.md` | Structure section: canonical module list |

## Graceful Degradation

Every source is optional. When a source is unavailable:
- CLI sources (bd, git): catch non-zero exit, note "not available"
- File sources: glob returns empty, note "not found"
- The artifact phase handles missing context by omitting the corresponding section or noting "data not available"
