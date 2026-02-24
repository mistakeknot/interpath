# interpath

Product artifact generator for Claude Code.

## What this does

interpath generates roadmaps, PRDs, vision documents, changelogs, and status reports by pulling from the actual project state: beads issues, brainstorm docs, existing plans, git history, plugin manifests. The artifacts stay connected to the real work rather than drifting into aspirational fiction, which is the usual failure mode of product documentation.

Sources degrade gracefully. No beads? Skip the backlog sections. No PRD? Skip that input. The artifact still generates with whatever context is available.

## Installation

First, add the [interagency marketplace](https://github.com/mistakeknot/interagency-marketplace) (one-time setup):

```bash
/plugin marketplace add mistakeknot/interagency-marketplace
```

Then install the plugin:

```bash
/plugin install interpath
```

Companion plugin for [Clavain](https://github.com/mistakeknot/Clavain).

## Commands

```
/interpath:roadmap     Generate or refresh the project roadmap
/interpath:prd         Generate or refresh a Product Requirements Document
/interpath:vision      Generate or refresh a vision document
/interpath:changelog   Generate changelog from closed beads
/interpath:status      Generate a point-in-time status report
```

## How it works

Each command triggers the `artifact-gen` skill, which:

1. **Discovers** sources: beads state, brainstorms, PRDs, plans, flux-drive summaries, git log, plugin manifests
2. **Synthesizes** the artifact using the appropriate template
3. **Writes** output to `docs/` (or presents for review)

All artifact types share a single skill with phase-based routing. The discovery phase is shared; the synthesis phase is specific to each artifact type.

## License

MIT
