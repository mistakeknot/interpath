---
name: all
description: Refresh all docs that need refreshing — reads interwatch drift state and regenerates High/Certain confidence items
---

# Refresh All Stale Docs

Reads the interwatch drift scan results and refreshes all documents at **High** or **Certain** confidence.

## Algorithm

1. **Read drift state:**
   ```bash
   DRIFT_FILE=".interwatch/drift.json"
   if [ ! -f "$DRIFT_FILE" ]; then
       echo "No drift state found. Run /interwatch:watch first to scan for doc drift."
       exit 0
   fi
   ```

2. **Extract items needing refresh:** Parse the JSON for watchables with confidence `High` or `Certain`:
   ```bash
   python3 -c "
   import json, sys
   data = json.load(open('$DRIFT_FILE'))
   for name, w in data.get('watchables', {}).items():
       if w.get('confidence') in ('High', 'Certain'):
           print(json.dumps({'name': name, 'path': w['path'], 'confidence': w['confidence'], 'score': w['score'], 'generator': w.get('generator', ''), 'generator_args': w.get('generator_args', {})}))
   "
   ```

3. **If nothing needs refresh**, tell the user: "All docs are fresh (no High/Certain drift detected)."

4. **For each item needing refresh**, invoke the appropriate generator skill sequentially:
   - If `generator` is `interpath:artifact-gen`: use the Skill tool to invoke `interpath:artifact-gen` with the artifact type from `generator_args.type`
   - If `generator` is `interdoc:interdoc`: use the Skill tool to invoke `interdoc:interdoc`
   - For any other generator: tell the user the generator name and skip it

5. **Display summary** after all refreshes:
   ```
   Refresh Complete
   ────────────────────────────
   ✓ roadmap     docs/interverse-roadmap.md    (was High, score 33)
   ✓ vision      docs/interverse-vision.md     (was High, score 13)
   ────────────────────────────
   Refreshed: 2 | Skipped: 0
   ```

6. **Re-run the drift scan** after refreshing to update state:
   ```bash
   python3 interverse/interwatch/scripts/interwatch-scan.py > .interwatch/drift.json 2>/dev/null
   ```

## Options

- `--include-medium` — Also refresh Medium confidence items (default: only High/Certain)
- `--dry-run` — Show what would be refreshed without invoking generators
