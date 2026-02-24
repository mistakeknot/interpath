---
name: propagate
description: Auto-generate module-level roadmaps from beads state
---

# Propagate Roadmap

Auto-generate `docs/roadmap.md` files for each module from beads state.

This command runs `scripts/generate-module-roadmaps.sh` from the Demarch monorepo root. It:

1. Iterates through all modules in `apps/`, `os/`, `core/`, `interverse/`, `sdk/`
2. Queries beads for items matching each module name
3. Generates `docs/roadmap.md` per module with open/in-progress/blocked/recently-closed items
4. Links each module roadmap back to the root `docs/demarch-roadmap.md`
5. Reports a summary of what was created, updated, or skipped

**Prerequisites:** Run from the Demarch monorepo root directory. Requires `bd` (beads CLI).

Output: Auto-generated `docs/roadmap.md` files in each module directory.

```bash
ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
"$ROOT_DIR/scripts/generate-module-roadmaps.sh"
```

Use `--dry-run` to preview without writing files.
