---
name: artifact-gen
description: Generate product artifacts (roadmaps, PRDs, vision docs, changelogs, status reports) from beads state, brainstorms, and project context. Routes to artifact-specific phases after shared discovery.
---

# Artifact Generator

<!-- compact: SKILL-compact.md — if it exists in this directory, load it instead of following the multi-file instructions below. The compact version contains the same algorithm in a single file. -->

You are generating a product artifact. Follow these steps exactly.

## Step 1: Determine Artifact Type and Context

The user wants one of: **roadmap**, **prd**, **vision**, **changelog**, **status**, **monorepo-roadmap**, **propagate**

If not clear from the invocation, ask which artifact to generate.

### Monorepo Auto-Detection

If the user requests a **roadmap** and the CWD appears to be a monorepo root, automatically use the **monorepo-roadmap** path instead. A directory is a monorepo root if it has **both**:
- A `.beads/` database
- Subdirectories (`hub/*/`, `plugins/*/`, or `services/*/`) containing `.claude-plugin/plugin.json` files

AND it does **not** itself have a `.claude-plugin/plugin.json` at its root.

If the CWD is a monorepo root and the user requested "roadmap", treat it as "monorepo-roadmap".

## Step 2: Discover Sources

Based on the artifact type:

- **For single-project types** (roadmap, prd, vision, changelog, status): Read `artifact-gen/phases/discover.md` and execute the discovery phase.
- **For monorepo types** (monorepo-roadmap, propagate): Read `artifact-gen/phases/discover-monorepo.md` and execute the monorepo discovery phase.

## Step 3: Generate Artifact

Based on the artifact type, read and follow the corresponding phase file:

| Type | Phase File |
|------|-----------|
| roadmap | `artifact-gen/phases/roadmap.md` |
| prd | `artifact-gen/phases/prd.md` |
| vision | `artifact-gen/phases/vision.md` |
| changelog | `artifact-gen/phases/changelog.md` |
| status | `artifact-gen/phases/status.md` |
| monorepo-roadmap | `artifact-gen/phases/roadmap-monorepo.md` (template-then-fill) |
| propagate | `artifact-gen/phases/roadmap-monorepo.md` → `artifact-gen/phases/propagate.md` |

For **propagate**: first generate the monorepo roadmap, then run the propagation phase to push items to sub-module roadmaps.

## Step 4: Output

Write the generated artifact to the appropriate location (typically `docs/` in the project root). If the file already exists, show a diff summary before overwriting.

## Notes

- Sources degrade gracefully — missing beads, PRDs, or brainstorms are silently skipped
- Always include a metadata header (version, date, cross-references to other docs)
- Prefer factual synthesis over aspirational language
- Link to companion docs where they exist
