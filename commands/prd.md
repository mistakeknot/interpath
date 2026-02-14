---
name: prd
description: Generate or refresh a Product Requirements Document from project state, brainstorms, and beads
---

# Generate PRD

Invoke the `artifact-gen` skill with artifact type **prd**.

The PRD synthesizes:
- Problem statement from vision doc and brainstorms
- Product overview with component counts
- Core capabilities grouped by workflow stage
- Architecture including companion ecosystem
- Non-goals from design decisions
- Success metrics from beads stats

Output: `docs/PRD.md`

Use the Skill tool to invoke `interpath:artifact-gen` with the instruction: "Generate a PRD artifact."
