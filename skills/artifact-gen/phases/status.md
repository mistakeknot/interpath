# Status Report Synthesis

Using the discovered sources, generate a point-in-time health snapshot.

## Output Structure

### Header

```markdown
# [Project Name] — Status Report

**Date:** [today's date]
**Version:** [from plugin.json]
**Period:** [last 7 days or since last report]
```

### Section 1: Health Summary

One-line overall assessment, then a metrics table:

| Metric | Value |
|--------|-------|
| Open beads | N |
| Closed (this period) | N |
| Blocked | N |
| P0/P1 open | N |
| Version | X.Y.Z |
| Components | N skills, N agents, N commands |

### Section 2: What Shipped

List of beads closed in the period, grouped by type:
- Features
- Bug fixes
- Tasks

### Section 3: What's In Progress

Active beads (status=in_progress) with owner and age.

### Section 4: What's Blocked

Blocked beads with what's blocking them.

### Section 5: Risks and Concerns

Derive from:
- High-priority beads that haven't moved
- Stale beads (open > 14 days without activity)
- Dependency chains longer than 3

### Section 6: Next Actions

Top 3-5 items from `bd ready` (available to work on).

## Writing Guidelines

- Pure facts — no opinions or predictions
- Include bead IDs for traceability
- Keep under 100 lines
- Suitable for async team updates
