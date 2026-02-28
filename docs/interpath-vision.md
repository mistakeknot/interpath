# interpath — Vision and Philosophy

**Version:** 0.1.0
**Last updated:** 2026-02-28

## What interpath Is

interpath is a product artifact generator for Claude Code projects. It produces roadmaps, PRDs, vision documents, changelogs, and status reports by reading actual project state — beads issues, brainstorm docs, git history, plugin manifests — rather than asking you to describe it. The artifacts are connected to evidence. They don't drift into aspirational fiction because they don't start from a blank page.

The interface is six commands routed through a single skill (`artifact-gen`) with a shared discovery phase. All artifact types read the same sources; the synthesis phase is what differs. Missing sources degrade gracefully — no beads means roadmap sections that would have used them are skipped, not errored. Output lands in `docs/` in the target project.

## Why This Exists

Documentation is the failure mode of every agent-powered project. Docs written by hand fall behind reality. Docs generated without grounding produce aspirational fiction. interpath occupies the middle position: synthesis from structured state. Beads are closed, brainstorms are filed, git history accumulates — interpath reads that corpus and produces artifacts that reflect what actually happened and what is actually planned. The artifacts are receipts, not narratives.

## Design Principles

1. **Evidence over aspiration.** Every generated artifact cites its sources. Roadmap items trace to beads. Changelog entries trace to closed issues and git tags. No section is written from scratch if a source exists.

2. **Graceful degradation.** A project with no beads, no PRDs, and no brainstorms still gets a usable artifact. Sources are discovered opportunistically; absence is silently handled, not a blocker.

3. **Single skill, phase-based routing.** Discovery is shared across all artifact types. The synthesis phase is where types diverge. This keeps the skill surface narrow and makes the discovery logic reusable as new artifact types are added.

4. **Output to docs/, not to chat.** Artifacts are files, not conversations. The output location is deterministic. Downstream tooling (interwatch for freshness monitoring, interleave for templating) can depend on it.

5. **Self-application.** Demarch uses interpath to generate its own docs. If interpath can't produce a coherent roadmap for the Interverse monorepo from beads state, the tool isn't ready. Self-building is the acceptance criterion.

## Scope

**Does:** roadmap, PRD, vision, changelog, status report. Monorepo-aware roadmap with propagation to sub-module docs. Reads beads, brainstorms, plans, git log, plugin manifests. Writes to `docs/`. Bead consistency check after roadmap generation.

**Does not:** manage beads (that's Clavain), monitor freshness (that's interwatch), provide templates for new docs (that's interleave), run automatically on events (no hooks — interpath is invoked on demand).

## Direction

- Expand artifact type coverage: ADRs, sprint retrospectives, and dependency graphs are the near-term candidates
- Tighten consistency enforcement: post-generation audit linking every roadmap item to a live bead, surfacing drift before it accumulates
- Formalize the companion surface: interwatch consuming interpath outputs for freshness signals, interleave pulling interpath templates as a canonical source
