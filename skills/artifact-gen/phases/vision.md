# Vision Doc Synthesis

Using the discovered sources, generate or refresh a vision document.

## Output Structure

### Header

```markdown
# [Project Name] — Vision

**Last updated:** [today's date]
**PRD:** [`docs/PRD.md`](PRD.md)
**Roadmap:** [`docs/roadmap.md`](roadmap.md)
```

### Section 1: The Big Idea

One-paragraph elevator pitch synthesized from PRD problem statement, brainstorms, and README.

### Section 2: Design Principles

3-5 principles that guide all decisions. Derive from:
- Design decisions in CLAUDE.md
- Patterns visible in the codebase
- Explicit statements in brainstorms

Each principle: **Name** — one-sentence explanation.

### Section 3: Current State

Brief snapshot:
- Version and maturity
- Component counts
- Active users / deployments (if known)
- Key milestones achieved

### Section 4: Where We're Going

From roadmap phases and brainstorms:
- Near-term direction (what's being built now)
- Medium-term direction (what comes after)
- Long-term aspiration (the north star)

### Section 5: Constellation

If the project has companion plugins, describe the ecosystem:

| Plugin | Role | Status |
|--------|------|--------|
| ... | ... | ... |

### Section 6: What We Believe

Key bets and assumptions the project makes. Things that, if wrong, would change the direction.

## Writing Guidelines

- Vision docs should inspire but stay grounded in reality
- Reference specific shipped work as evidence for direction
- Keep aspirational sections clearly labeled
- Keep under 150 lines
