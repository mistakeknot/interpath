---
name: roadmap
description: Generate or refresh a project roadmap from beads state, brainstorms, plans, and project context
---

# Generate Roadmap

Invoke the `artifact-gen` skill with artifact type **roadmap**.

The roadmap synthesizes:
- Current project state (version, components, companions)
- Open beads organized by priority into Now/Next/Later phases
- Research agenda from brainstorms and flux-drive summaries
- Blocking relationships and dependency graph

Output: `docs/roadmap.md`

Use the Skill tool to invoke `interpath:artifact-gen` with the instruction: "Generate a roadmap artifact."
