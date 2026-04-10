# Running the Pipeline

How to start, monitor, and complete a pipeline run.

## Pre-Flight Checklist

Before running, verify:

1. **Config exists:** `.afternoon/config.json` with valid project, styleTarget, characters, priming, completionMarker
2. **Story overview exists:** The file referenced by `config.storyOverview` exists (mandatory — orchestrator exits with FATAL if missing)
3. **Outlines exist:** `.afternoon/outlines/` contains at least one `chapter-*.md` file with beat plans
4. **Style target exists:** The file referenced by `config.priming.styleTarget` exists
5. **Anti-slop files exist:** All paths in `config.priming.antiSlop` exist
6. **Craft files exist:** All paths in `config.priming.craft` exist
7. **Voice sheets exist:** The directory at `config.characters.voiceSheets` exists and contains character files
8. **Materials exist (if set):** All paths in `config.materials` array exist

Quick check:
```bash
cat .afternoon/config.json | python3 -c "
import json, sys, os
c = json.load(sys.stdin)
checks = [
    ('.afternoon/config.json', True),
    (c.get('storyOverview','MISSING'), os.path.exists(c.get('storyOverview',''))),
    (c['priming']['styleTarget'], os.path.exists(c['priming']['styleTarget'])),
    (c['characters']['voiceSheets'], os.path.isdir(c['characters']['voiceSheets'])),
]
for p in c['priming']['antiSlop'] + c['priming']['craft'] + c.get('materials', []):
    checks.append((p, os.path.exists(p)))
for path, ok in checks:
    print(f'{'✓' if ok else '✗'} {path}')
"
```

## Starting the Pipeline

```bash
./afternoon-start.sh
```

The start script:
1. Verifies `.afternoon/config.json` exists
2. Verifies `.afternoon/outlines/` has at least one outline
3. Creates the logs directory (`logs/afternoon/`)
4. Dispatches the orchestrator agent
5. Monitors output for the completion marker (`===AFTERNOON DONE===`)
6. Retries up to 3 times on failure

## Monitoring Progress

While the pipeline runs:

### Check which chapter/agent is active
```bash
cat .afternoon/manifest.json | python3 -c "import json,sys; m=json.load(sys.stdin); print(f\"{m.get('currentChapter','?')} / {m.get('currentAgent','?')} — {m.get('chaptersCompleted',0)} done\")"
```

### Watch for new files
```bash
ls -lt .afternoon/chapters/*/v*.md 2>/dev/null | head -10
```

### Check agent completion
```bash
for f in .afternoon/agents/*/status.json; do
  agent=$(echo "$f" | cut -d/ -f3)
  status=$(python3 -c "import json; print(json.load(open('$f'))['status'])" 2>/dev/null || echo "no-status")
  echo "$agent: $status"
done
```

### Check logs
```bash
tail -50 logs/afternoon/*.log 2>/dev/null
```

## Completion

The pipeline is done when:
1. The orchestrator outputs `===AFTERNOON DONE===`
2. All chapters have `final.md` files in `.afternoon/chapters/{chapterId}/`
3. The manifest shows `"status": "completed"`

Final output files:
```
.afternoon/chapters/
├── chapter-1/
│   ├── v1.md          # Writer raw draft
│   ├── v2.md          # After slophunter
│   ├── v2g.md         # After grounder
│   ├── grounding-map.json
│   ├── grounding-gate-notes.json   # If grounding-gate enabled
│   ├── v3.md          # After expander
│   ├── final.md       # Assembled chapter
│   ├── slophunter-notes.json
│   ├── grounder-notes.json
│   └── style-notes.json
├── chapter-2/
│   └── ...
└── chapter-3/
    └── ...
```

## Running a Subset of Chapters

To run only specific chapters:
1. Remove outlines you don't want from `.afternoon/outlines/` (or move them elsewhere temporarily)
2. The orchestrator processes whatever outlines are present

## Adding Chapters After a Run

If you want to add more chapters after a completed run:
1. Add new outline files to `.afternoon/outlines/`
2. Update manifest.json: set `"status": "in-progress"`, remove the new chapters from anywhere they might appear
3. Restart the pipeline — the orchestrator will detect unprocessed outlines

## Environment Notes

- **Model costs:** The specialist agents use gpt-5.4 and the orchestrator uses claude-sonnet-4.6. A typical 5000-word chapter costs roughly 500K-1M tokens total across the full run.
- **Time:** Expect 15-30 minutes per chapter in the default flow. Enabling the grounding-gate adds another audit/revision surface and can push long chapters higher.
- **Disk:** Each chapter produces ~100KB of artifacts (drafts + notes + memory). Minimal disk usage.
- **Network:** Plan-verifier uses web search for craft knowledge. Writer and planner may use web search for character/location research. Other agents are offline.
- **Extra artifacts when grounding-gate is enabled:** `grounding-gate-notes*.json`, `grounding-gate-scratchpad*.md`, `v2g-r*.md`, `grounding-map*.json`, and `grounder-revision-r*-notes.json`.
