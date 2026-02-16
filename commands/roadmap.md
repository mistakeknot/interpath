---
name: roadmap
description: Generate or refresh a project roadmap from beads state, brainstorms, plans, and project context. Auto-detects monorepo roots for ecosystem-wide roadmaps.
---

# Generate Roadmap

Invoke the `artifact-gen` skill with artifact type **roadmap**.

The roadmap synthesizes:
- Current project state (version, components, companions)
- Open beads organized by priority into Now/Next/Later phases
- Research agenda from brainstorms and flux-drive summaries
- Blocking relationships and dependency graph

**Monorepo mode:** When run from a monorepo root (e.g., Interverse), this command auto-detects the monorepo context and generates an ecosystem-wide roadmap covering all modules in `hub/`, `plugins/`, and `services/`. Use `/interpath:propagate` to push items back to individual module roadmaps.

Output: `docs/roadmap.md`

Use the Skill tool to invoke `interpath:artifact-gen` with the instruction: "Generate a roadmap artifact."
