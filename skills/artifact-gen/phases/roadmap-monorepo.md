# Monorepo Roadmap Synthesis

Using the monorepo discovery context, generate a unified project roadmap that aggregates across all modules.

## Preferred Output Pair

- `docs/<project>-roadmap.md` (human-readable)
- `docs/roadmap.json` (machine-readable canonical output, source-of-truth)

## Templated Generation Flow

Most roadmap sections are **deterministic** — tables, bead lists, dependency chains, and counts are computed directly from `docs/roadmap.json` and `bd --json` output. Only 3 sections need LLM judgment. This flow saves ~13K tokens vs. regenerating everything from scratch.

### Step 1: Generate canonical JSON (already done by command)

The calling command has already run `sync-roadmap-json.sh`. If `docs/roadmap.json` is missing, run:

```bash
ROADMAP_SYNC="${CLAUDE_PLUGIN_ROOT}/scripts/sync-roadmap-json.sh"
if [ -z "${CLAUDE_PLUGIN_ROOT:-}" ] || [ ! -x "$ROADMAP_SYNC" ]; then
    echo "Warning: CLAUDE_PLUGIN_ROOT not set or sync script not found" >&2
else
    bash "$ROADMAP_SYNC"
fi
```

### Step 2: Run the deterministic templater (optional)

If a template script exists (e.g., from a companion plugin like interleave), use it to produce a markdown file with `<!-- LLM:SECTION_NAME -->` placeholder markers. Otherwise, skip directly to the manual synthesis approach in Step 4's fallback.

```bash
ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
# Try interleave companion if available
TEMPLATE_SCRIPT=""
for _candidate in \
    "${CLAUDE_PLUGIN_ROOT:-}/../interleave/scripts/template-roadmap-md.sh" \
    "$ROOT_DIR/scripts/template-roadmap-md.sh"; do
    if [ -f "$_candidate" ]; then
        TEMPLATE_SCRIPT="$_candidate"
        break
    fi
done
if [ -n "$TEMPLATE_SCRIPT" ]; then
    bash "$TEMPLATE_SCRIPT" "$ROOT_DIR/docs/roadmap.json"
else
    echo "No template script found — using manual synthesis" >&2
fi
```

If the template script runs, it produces a roadmap markdown with `<!-- LLM:SECTION_NAME -->` placeholder markers for sections needing LLM judgment. All other sections (header, ecosystem table, Now items, Later items, cross-deps, modules without roadmaps, keeping current) are fully rendered.

### Step 3: Read the templated output

Read `docs/interverse-roadmap.md`. It will contain up to 3 LLM placeholder markers. If the template script populated all module highlights from `roadmap.json`, there may be fewer than 3.

### Step 4: Fill LLM placeholders

For each `<!-- LLM:SECTION_NAME -->` block found in the output:

**NEXT_GROUPINGS** — Dispatch a **Sonnet 4.6** subagent (semantic grouping needs stronger judgment):
- Input: the JSON array of P2 items embedded in the placeholder comment
- Task: group items under 5-10 thematic headings
- Format: markdown with **bold headings** and bullet items using the `- [module] **id** title` format
- Heuristic hints: items sharing a `[module]` tag or dependency chain likely belong together
- Keep each group to 2-8 items; avoid single-item groups

**MODULE_HIGHLIGHTS** — Dispatch a **Haiku** subagent:
- Input: list of modules needing highlights (embedded in the placeholder) + their open items from Now/Next sections
- Task: write 2-3 sentence summary per module describing current focus
- Format: `### module (location)\nvX.Y.Z. Summary.\n`
- Use factual language based on item titles, not aspirational claims

**RESEARCH_AGENDA** — Dispatch a **Haiku** subagent:
- Input: brainstorm/plan file titles + existing research items (embedded in the placeholder)
- Task: synthesize into 10-15 thematic bullets covering active research threads
- Format: `- **Topic** — 1-line summary`
- Group related brainstorms under a single bullet where appropriate

### Step 5: Write final output

Replace each `<!-- LLM:SECTION_NAME ... END LLM:SECTION_NAME -->` block with the subagent output. Write the final `docs/interverse-roadmap.md`.

### Fallback: Manual synthesis

If the template script fails (missing `jq`, broken `bd`, etc.), fall back to the manual synthesis approach below. The script will print diagnostic errors to stderr.

## Manual Output Structure (templater recovery path)

Use this structure if Step 2 fails. This is the traditional approach where the LLM generates everything.

### Header

```markdown
# [Project Name] Roadmap

**Modules:** [count] | **Open beads:** [count] | **Last updated:** [today's date]
**Structure:** [`CLAUDE.md`](../CLAUDE.md)
```

### Section 1: Ecosystem Snapshot

A table of all modules from `roadmap.json .modules[]`, sorted alphabetically:

| Module | Location | Version | Status | Roadmap | Open Beads |
|--------|----------|---------|--------|---------|------------|

### Section 2: Roadmap — Now / Next / Later

From beads, tagged with `[module]` prefix:
- **Now (P0-P1):** critical/high-priority items
- **Next (P2):** grouped under thematic headings
- **Later (P3+):** backlog/aspirational items

### Section 3: Module Highlights

2-3 line summaries per module from `roadmap.json .module_highlights[]`.

### Section 4: Research Agenda

Synthesized from brainstorms, plans, and `roadmap.json .research_agenda[]`.

### Section 5: Cross-Module Dependencies

Blocking relationships spanning modules.

### Section 6: Modules Without Roadmaps

From `roadmap.json .modules_without_roadmaps[]`.

### Section 7: Keeping Current

Regeneration instructions.

### Canonical machine output: `docs/roadmap.json`

The JSON artifact generated by `sync-roadmap-json.sh` is the source-of-truth for cross-repo tooling.

## Writing Guidelines

- Be factual — use counts, versions, and bead IDs, not qualitative claims
- Tag every item with its module so readers can filter mentally
- Keep each item to 1-2 lines
- Link to source files where possible
- Target 200-400 lines (larger than single-project due to scope)
- Sections for which no data is available should say "No data available" rather than being omitted
- Sort modules alphabetically within tables
