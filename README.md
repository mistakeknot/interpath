# interpath

Product artifact generator for Claude Code — generates roadmaps, PRDs, vision docs, changelogs, and status reports from beads state, brainstorms, and project context.

Companion plugin for [Clavain](https://github.com/mistakeknot/Clavain).

## Install

```bash
claude plugin install interpath@interagency-marketplace
```

## Commands

| Command | Description |
|---------|-------------|
| `/interpath:roadmap` | Generate or refresh project roadmap (writes `docs/roadmap.md` and `docs/roadmap.json`) |
| `/interpath:prd` | Generate or refresh PRD |
| `/interpath:vision` | Generate or refresh vision doc |
| `/interpath:interpath-changelog` | Generate changelog from closed beads |
| `/interpath:interpath-status` | Generate point-in-time status report |

## How It Works

Each command triggers the `artifact-gen` skill which:

1. **Discovers** sources — beads state, brainstorms, PRDs, plans, flux-drive summaries, git log, plugin manifests
2. **Synthesizes** the artifact using the appropriate phase template
3. **Writes** the output to `docs/` (or presents for review)

Sources degrade gracefully — no beads means skip backlog sections, no PRD means skip that input.

## License

MIT
