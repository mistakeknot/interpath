---
name: vision
description: Generate or refresh a vision document from PRD, brainstorms, and project state
---

# Generate Vision Doc

Invoke the `artifact-gen` skill with artifact type **vision**.

The vision doc synthesizes:
- Big idea from PRD and README
- Design principles from CLAUDE.md and codebase patterns
- Current state snapshot
- Direction from roadmap phases and brainstorms
- Companion ecosystem constellation
- Key bets and assumptions

Output: `docs/${repo}-vision.md` (preferred), plus compatibility `docs/vision.md`

Use the Skill tool to invoke `interpath:artifact-gen` with the instruction: "Generate a vision artifact."
