---
name: artifact-gen
description: Generate product artifacts (roadmaps, PRDs, vision, changelogs, status) from beads, brainstorms, and project context. Phase-routed after shared discovery.
---

# Artifact Generator

<!-- compact: SKILL-compact.md — if it exists in this directory, load it instead of following the multi-file instructions below. The compact version contains the same algorithm in a single file. -->

You are generating a product artifact. Follow these steps exactly.

## Step 1: Determine Artifact Type and Context

The user wants one of: **roadmap**, **prd**, **vision**, **changelog**, **status**, **cuj**, **monorepo-roadmap**, **propagate**

If not clear from the invocation, ask which artifact to generate.

### Monorepo Auto-Detection

If the user requests a **roadmap** and the CWD appears to be a monorepo root, automatically use the **monorepo-roadmap** path instead. A directory is a monorepo root if it has **both**:
- A `.beads/` database (or beads CLI available with data)
- At least one top-level subdirectory that itself contains sub-directories with `.claude-plugin/plugin.json` or `CLAUDE.md` files

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
| cuj | `artifact-gen/phases/cuj.md` |
| monorepo-roadmap | `artifact-gen/phases/roadmap-monorepo.md` (template-then-fill) |
| propagate | `artifact-gen/phases/roadmap-monorepo.md` → `artifact-gen/phases/propagate.md` |

For **propagate**: first generate the monorepo roadmap, then run the propagation phase to push items to sub-module roadmaps.

## Step 4: Output (Canonical Witness)

Each artifact type has **exactly one canonical path**. Always overwrite that path; never write a dated, versioned, or branched variant alongside it. This is the canonical-witness rule (sylveste-a4oj.7 / SCRIP-2): without it, multiple "witnesses" of the same artifact accumulate and downstream readers consume different versions.

### Canonical paths

| Type | Canonical Path | Notes |
|------|----------------|-------|
| roadmap | `docs/${module}-roadmap.md` + `docs/roadmap.json` | `${module}` = repo/project short name (e.g., `sylveste`, `interverse`). |
| prd | `docs/PRD.md` | Single project. |
| vision | `docs/${module}-vision.md` | Same `${module}` convention as roadmap. |
| changelog | `docs/CHANGELOG.md` or `CHANGELOG.md` (project-dependent) | Whichever already exists; if neither, prefer `CHANGELOG.md` at project root. |
| status | `docs/STATUS.md` | Single project. |
| cuj | `docs/cujs/<cuj-slug>.md` | Per-CUJ file; each CUJ's slug is its canonical witness. |
| monorepo-roadmap | `docs/${module}-roadmap.md` at the monorepo root (e.g., `docs/interverse-roadmap.md`) | |
| propagate | `docs/roadmap.md` in each sub-module | |

### Overwrite rules

1. **Always write to the canonical path.** Don't suffix the filename with the date, ISO timestamp, or run identifier (`roadmap-2026-05-06.md`, `vision-20260506T1430.md`, etc.). Versioning is git's job, not the filename's.
2. **Detect orphan interpath witnesses before regenerating.** An orphan is a file matching the pattern `docs/${module}-{roadmap,vision}-<DATE>.md` or `docs/${module}-{roadmap,vision}-<TIMESTAMP>.md` (date/timestamp suffix on a name that's otherwise the canonical pattern) — i.e., something a previous interpath run produced under an aberrant naming variant. If found, move the orphan to `docs/.archive/${YYYY-MM-DD}/` before writing the new canonical file. **Important:** do NOT touch hand-curated parallel docs that share a related name but are clearly separate intentional documents (e.g., `docs/roadmap-v1.md` as a release-goals planning doc, `docs/vision-2030.md` as a long-horizon strategy doc). Heuristics: a hand-curated doc is tracked in git for many commits, has a substantively different first paragraph, or is referenced from CLAUDE.md/AGENTS.md/README.md. When in doubt, leave the file alone and report it to the user instead of archiving.
3. **Diff summary before overwrite is courtesy, not a gate.** When the canonical file exists, you may print a brief diff summary (e.g., "+15 lines, -8 lines, 3 new beads referenced") before writing. This is informational; do not branch into "should I overwrite?" — the answer is always yes for canonical paths.
4. **Git is the version archive.** A reader who wants prior versions runs `git log -- docs/sylveste-roadmap.md` and `git show <sha>:docs/sylveste-roadmap.md`. The on-disk file is always the latest.

## Step 5: Consistency Check (Roadmap only)

After writing a **roadmap** or **monorepo-roadmap** artifact, run a bead consistency check:

1. Extract all `iv-*` IDs from the generated roadmap markdown
2. For each ID, verify a bead exists: `bd show <id>` should return success
3. Check for open beads NOT referenced in the roadmap: `bd list --status=open` and cross-reference
4. Report discrepancies inline at the end of the generation output:
   - **ERROR** — Roadmap references an ID with no corresponding bead (indicates stale or typo'd ID)
   - **WARNING** — Open beads exist that aren't mentioned in the roadmap (may need placement or are intentionally excluded)
   - **INFO** — "Recently completed" IDs whose bead is not yet closed

If there are zero errors, print a one-line confirmation: "Roadmap-bead consistency: all IDs verified."

If the standalone audit script exists at `scripts/audit-roadmap-beads.sh`, you may call it instead of performing the checks manually. Both approaches produce equivalent results.

Skip this step for non-roadmap artifacts (prd, vision, changelog, status).

## Notes

- Sources degrade gracefully — missing beads, PRDs, or brainstorms are silently skipped
- Always include a metadata header (version, date, cross-references to other docs)
- Prefer factual synthesis over aspirational language
- Link to companion docs where they exist
