---
name: cuj
description: Generate or refresh a Critical User Journey from PRDs, brainstorms, and project state
---

# Generate CUJ

Invoke the `artifact-gen` skill with artifact type **cuj**.

The CUJ synthesizes:
- Journey motivation from PRD and vision doc
- Prose narrative from brainstorms and existing docs
- Typed success signals from PRD metrics and beads
- Known friction points from open beads and brainstorms

Output: `docs/cujs/<journey-slug>.md`

Use the Skill tool to invoke `interpath:artifact-gen` with the instruction: "Generate a CUJ artifact."
