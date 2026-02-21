# Roadmap Synthesis

Using the discovered sources, generate a roadmap document with these sections:

## Preferred Output Pair

- `docs/${module}-roadmap.md` (human-readable)
- `docs/roadmap.json` (machine-readable canonical output)

## Output Structure

### Header

```markdown
# [Project Name] Roadmap

**Version:** [from plugin.json]
**Last updated:** [today's date]
**Vision:** [`docs/${module}-vision.md`](${module}-vision.md)
**PRD:** [`docs/PRD.md`](PRD.md)
```

### Section 1: Where We Are

Synthesize from:
- Plugin manifest (component counts, version)
- Beads stats (open/closed counts)
- Companion plugin status
- Git activity (recent tags, commit frequency)

Include two subsections:
- **What's Working** — shipped capabilities, stable features
- **What's Not Working Yet** — known gaps, unresolved patterns

### Section 2: Roadmap (Phased)

Organize into phases based on beads priorities and blocking relationships:

- **Now (P0-P1)** — actively blocked or critical issues
- **Next (P2)** — medium priority, planned for near-term
- **Later (P3-P4)** — backlog, aspirational, research-dependent

For each item, include:
- Bead ID (if from beads)
- One-line description
- Blocking relationships (if any)
- Source (bead, brainstorm, PRD goal)

### Section 3: Research Agenda

Synthesize from brainstorms and flux-drive summaries:
- Active research threads
- Open questions
- Evaluation criteria

### Section 4: Companion Status

Table of companion plugins with:
- Name
- Version
- Status (shipped/planned/concept)
- One-line description

### Section 5: Open Beads Summary

Compact table of all open beads:
- ID | Title | Priority | Status | Blocked By

### Section 6: Dependency Graph

ASCII or text representation of blocking relationships between open beads.

### Section 7: Keeping Current

Brief note on how to refresh this roadmap:
```
Run `/interpath:roadmap` to regenerate from current project state.
```

### Canonical machine output: `docs/roadmap.json`

Generate a machine-readable artifact that includes the same roadmap content as structured objects.

```json
{
  "project": "<project-name>",
  "kind": "single-project-roadmap",
  "version": "<plugin-version>",
  "generated_at": "<ISO-8601>",
  "where_we_are": {
    "version": "<plugin-version>",
    "open_beads": 0,
    "closed_beads": 0,
    "blocked_beads": 0,
    "companion_count": 0
  },
  "roadmap": {
    "now": [],
    "next": [],
    "later": []
  },
  "research_agenda": [],
  "companion_status": [],
  "open_beads_summary": [],
  "dependency_graph": [],
  "last_updated": "<today's date>"
}
```

Item records used in `roadmap.now`, `roadmap.next`, and `roadmap.later`:

```json
{
  "id": "iv-xxxx",
  "title": "Item title",
  "source": "bead|brainstorm|prd|plan|roadmap|other",
  "source_file": "docs/brainstorms/2026-..md",
  "phase": "now|next|later",
  "priority": "P0|P1|P2|P3|P4",
  "status": "open|blocked|in_progress",
  "blockers": ["iv-aaaa", "iv-bbbb"],
  "module": "clavain",
  "notes": "short reason, dependencies, or key constraint"
}
```

This JSON is the machine source for roll-up tools; markdown is generated from it.

## Writing Guidelines

- Be factual, not aspirational — describe what IS, not what could be
- Use counts and versions, not qualitative claims
- Link to source files where possible
- Keep each item to 1-2 lines
- Total document should be 100-200 lines
