# Output Templates

Structural templates for each artifact type. These define the expected sections, not the exact wording.

## Common Header

All artifacts start with:
```markdown
# [Project Name] — [Artifact Type]

**Version:** [from plugin.json]
**Last updated:** [today's date]
```

Cross-references to related docs where they exist.

## Roadmap Template

1. Where We Are (snapshot)
2. Roadmap — Now / Next / Later
3. Research Agenda
4. Companion Status (table)
5. Open Beads Summary (table)
6. Dependency Graph
7. Keeping Current

Target: 100-200 lines

## Monorepo Roadmap Template

1. Ecosystem Snapshot (module table: name, location, version, status, roadmap?, open beads)
2. Roadmap — Now / Next / Later (aggregated from monorepo beads, tagged by module)
3. Module Highlights (2-3 lines per module with existing roadmap)
4. Research Agenda (from monorepo brainstorms and plans)
5. Cross-Module Dependencies (blocking relationships spanning modules)
6. Modules Without Roadmaps (table with bead counts)
7. Keeping Current (regeneration instructions)

Target: 200-400 lines

## PRD Template

1. Problem Statement
2. Product Overview
3. Core Capabilities (by workflow stage)
4. Architecture (plugin structure, routing, hooks, companions)
5. Non-Goals
6. Success Metrics
7. Open Questions

Target: under 250 lines

## Vision Template

1. The Big Idea
2. Design Principles (3-5)
3. Current State
4. Where We're Going
5. Constellation (companion ecosystem)
6. What We Believe

Target: under 150 lines

## Changelog Template

Grouped by version (most recent first):
- Added / Changed / Fixed / Removed

Target: under 200 lines

## Status Report Template

1. Health Summary (metrics table)
2. What Shipped
3. What's In Progress
4. What's Blocked
5. Risks and Concerns
6. Next Actions

Target: under 100 lines
