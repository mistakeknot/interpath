---
name: artifact-gen
description: Generate product artifacts (roadmaps, PRDs, vision docs, changelogs, status reports) from beads state, brainstorms, and project context. Routes to artifact-specific phases after shared discovery.
---

# Artifact Generator

<!-- compact: SKILL-compact.md — if it exists in this directory, load it instead of following the multi-file instructions below. The compact version contains the same algorithm in a single file. -->

You are generating a product artifact. Follow these steps exactly.

## Step 1: Determine Artifact Type

The user wants one of: **roadmap**, **prd**, **vision**, **changelog**, **status**

If not clear from the invocation, ask which artifact to generate.

## Step 2: Discover Sources

Read `artifact-gen/phases/discover.md` and execute the discovery phase. This gathers all available project context (beads, brainstorms, plans, manifests, git history).

## Step 3: Generate Artifact

Based on the artifact type, read and follow the corresponding phase file:

| Type | Phase File |
|------|-----------|
| roadmap | `artifact-gen/phases/roadmap.md` |
| prd | `artifact-gen/phases/prd.md` |
| vision | `artifact-gen/phases/vision.md` |
| changelog | `artifact-gen/phases/changelog.md` |
| status | `artifact-gen/phases/status.md` |

## Step 4: Output

Write the generated artifact to the appropriate location (typically `docs/` in the project root). If the file already exists, show a diff summary before overwriting.

## Notes

- Sources degrade gracefully — missing beads, PRDs, or brainstorms are silently skipped
- Always include a metadata header (version, date, cross-references to other docs)
- Prefer factual synthesis over aspirational language
- Link to companion docs where they exist
